#!/usr/bin/env python3
"""Binance public-market-data forward/shadow validation.

This module has no account, private, trading, margin, futures, transfer,
or withdrawal endpoints. It records research decisions only.
"""
from __future__ import annotations
import csv, json, math, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent
LOG = OUT / "live_shadow_log.csv"
STATE = OUT / "live_shadow_state.json"
SUMMARY = OUT / "live_shadow_summary.json"
CONTEXT = OUT / "binance_daily_context.csv"

# Frozen historical-transfer parameters. This is a new live-shadow version;
# changing them requires a new parameter/model version and must not overwrite history.
PARAMETER_VERSION = "transfer_finance_v1_frozen_2026-09-26"
MODEL_VERSION = "btc_usdt_7d_momentum_market_evidence_v1"
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
DAILY_INTERVAL = "1d"
ABSTAIN_THRESHOLD = 0.65
WEIGHTS = {"completeness": 0.30, "agreement": 0.30, "stability": 0.20, "calibration": 0.20}
PUBLIC_BASE = "https://data-api.binance.vision"
KLINES_PATH = "/api/v3/klines"
# An explicit allow-list prevents accidental private/trading endpoint use.
ALLOWED_HOST = "data-api.binance.vision"
ALLOWED_PATH = "/api/v3/klines"

CSV_FIELDS = [
    "timestamp", "symbol", "close", "volume", "raw_signal", "reliability",
    "completeness", "agreement", "stability", "calibration", "adjusted_signal",
    "decision", "evaluation_status", "future_return", "raw_signal_correct",
    "adjusted_signal_correct", "accepted_sample", "abstained_sample",
    "parameter_version", "model_version", "source_endpoint", "capture_mode",
]


def fail_if_unsafe() -> None:
    # Require an explicit safe setting if supplied; default is safe public-only mode.
    raw = os.environ.get("LIVE_ORDERING_ENABLED")
    if raw is None:
        print("UNSAFE_PERMISSION_DETECTED")
        raise SystemExit(2)
    raw = raw.strip().lower()
    if raw != "false":
        print("UNSAFE_PERMISSION_DETECTED")
        raise SystemExit(2)
    # The code intentionally contains no private API key/secret or order endpoint.
    # Do not read or print BINANCE_API_KEY / BINANCE_API_SECRET.


def public_get(params: dict) -> list:
    """GET only from Binance's official public klines endpoint."""
    url = PUBLIC_BASE + ALLOWED_PATH + "?" + urlencode(params)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != ALLOWED_HOST or parsed.path != ALLOWED_PATH:
        print("UNSAFE_PERMISSION_DETECTED")
        raise SystemExit(2)
    req = Request(url, headers={"User-Agent": "external-transfer-validation/1.0"}, method="GET")
    with urlopen(req, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"public market-data request failed: HTTP {response.status}")
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list):
        raise RuntimeError("unexpected Binance kline response")
    return payload


def utc_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def now_ms() -> int:
    return utc_ms(datetime.now(timezone.utc))


def to_float(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def quantile(xs: list[float], q: float) -> float:
    vals = sorted(x for x in xs if x is not None and math.isfinite(x))
    if not vals:
        return 0.0
    pos = (len(vals) - 1) * q
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    if lo == hi:
        return vals[lo]
    return vals[lo] + (vals[hi] - vals[lo]) * (pos - lo)


def sign(x: float) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def fetch_daily_context() -> tuple[list[dict], str]:
    rows = public_get({"symbol": SYMBOL, "interval": DAILY_INTERVAL, "limit": 220})
    parsed = []
    for row in rows:
        if len(row) < 7:
            continue
        parsed.append({
            "open_time": int(row[0]), "open": to_float(row[1]), "high": to_float(row[2]),
            "low": to_float(row[3]), "close": to_float(row[4]), "volume": to_float(row[5]),
            "close_time": int(row[6]),
        })
    parsed = [r for r in parsed if r["close"] is not None and r["volume"] is not None]
    if len(parsed) < 100:
        raise RuntimeError(f"insufficient daily context: {len(parsed)}")
    # The current incomplete daily bar is usable for the current signal, but never
    # enters calibration, which is calculated only from completed bars.
    capture = now_ms()
    complete = [r for r in parsed if r["close_time"] < capture]
    if len(complete) < 100:
        raise RuntimeError("insufficient completed daily context")
    return parsed, datetime.fromtimestamp(capture / 1000, timezone.utc).isoformat()


def compute_features(daily: list[dict], capture_ms: int, observed_close: float | None = None) -> dict:
    # Restrict context to bars that had opened by this record timestamp. If the
    # current daily candle is incomplete, replace its close with the observed
    # close from this exact 1-minute record. This prevents batch-fetch leakage.
    available = [r for r in daily if r["open_time"] <= capture_ms]
    if len(available) < 15:
        raise RuntimeError("need at least 15 available daily closes")
    if observed_close is not None and available[-1]["close_time"] >= capture_ms:
        available = [dict(r) for r in available]
        available[-1]["close"] = observed_close
    current = available[-1]
    closes = [r["close"] for r in available]
    if len(closes) < 15:
        raise RuntimeError("need at least 15 daily closes")
    raw_signal = math.tanh((closes[-1] / closes[-8] - 1.0) / 0.05)

    # Evidence calculations use the available daily series. Calibration excludes
    # the current incomplete day and therefore cannot use any future outcome.
    completed = [r for r in available if r["close_time"] < capture_ms]
    cc = [r["close"] for r in completed]
    if len(cc) < 100:
        raise RuntimeError("need at least 100 completed daily closes")
    returns = [cc[i] / cc[i - 1] - 1.0 for i in range(1, len(cc))]

    # Completeness: proportion of expected 1-day bars in the latest 30 completed bars.
    tail = completed[-30:]
    expected = 30
    unique_days = len({r["open_time"] // 86400000 for r in tail})
    completeness = min(1.0, unique_days / expected)

    def mom(k: int) -> float:
        # Agreement is evaluated at the same observed close as Raw Signal.
        return closes[-1] / closes[-1-k] - 1.0
    dirs = [sign(mom(k)) for k in (3, 7, 14)]
    nonzero = [d for d in dirs if d != 0]
    agreement = (sum(d == sign(mom(7)) for d in nonzero) / len(nonzero)) if nonzero else 0.0

    vol20 = math.sqrt(mean((x - mean(returns[-20:])) ** 2 for x in returns[-20:]))
    vols = []
    for i in range(20, len(returns) + 1):
        w = returns[i-20:i]
        vols.append(math.sqrt(mean((x - mean(w)) ** 2 for x in w)))
    q90 = quantile(vols[-180:], 0.90)
    stability = max(0.0, min(1.0, 1.0 - (vol20 / q90 if q90 > 0 else 0.5)))

    # Past-hit calibration: signal at day t predicts return t+1. Only completed
    # outcomes strictly before the current capture are included.
    hist_raw = []
    for i in range(7, len(cc)):
        hist_raw.append(math.tanh((cc[i] / cc[i-7] - 1.0) / 0.05))
    hits = []
    for j in range(len(hist_raw) - 1):
        next_ret = cc[8 + j] / cc[7 + j] - 1.0
        hits.append(1.0 if sign(hist_raw[j]) * sign(next_ret) > 0 else 0.0)
    calibration = mean(hits[-90:]) if len(hits) >= 30 else 0.5

    reliability = max(0.0, min(1.0,
        WEIGHTS["completeness"] * completeness
        + WEIGHTS["agreement"] * agreement
        + WEIGHTS["stability"] * stability
        + WEIGHTS["calibration"] * calibration))
    return {
        "raw_signal": raw_signal, "completeness": completeness, "agreement": agreement,
        "stability": stability, "calibration": calibration, "reliability": reliability,
        "adjusted_signal": raw_signal * reliability,
    }


def fetch_live_rows() -> list[dict]:
    rows = public_get({"symbol": SYMBOL, "interval": INTERVAL, "limit": 10})
    out = []
    for row in rows:
        if len(row) < 7:
            continue
        close, volume = to_float(row[4]), to_float(row[5])
        if close is None or volume is None:
            continue
        out.append({"timestamp_ms": int(row[0]), "timestamp": datetime.fromtimestamp(int(row[0]) / 1000, timezone.utc).isoformat(),
                    "close": close, "volume": volume, "close_time_ms": int(row[6])})
    return out


def load_log() -> list[dict]:
    if not LOG.exists():
        return []
    with LOG.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_log(rows: list[dict]) -> None:
    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader(); w.writerows(rows)


def maybe_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def update_future_returns(rows: list[dict], capture_ms: int) -> None:
    """Backfill only matured records; current features are never recomputed."""
    for rec in rows:
        if rec.get("future_return") not in (None, "", "null"):
            continue
        try:
            ts = int(datetime.fromisoformat(rec["timestamp"].replace("Z", "+00:00")).timestamp() * 1000)
        except Exception:
            continue
        target = ts + 86400000
        if capture_ms < target + 60000:
            continue
        try:
            future = public_get({"symbol": SYMBOL, "interval": INTERVAL, "startTime": target, "endTime": target + 60000, "limit": 1})
        except Exception:
            continue
        if not future:
            continue
        future_close = to_float(future[0][4]); entry = maybe_float(rec.get("close"))
        if future_close is None or entry in (None, 0):
            continue
        fr = future_close / entry - 1.0
        rs, adj = maybe_float(rec.get("raw_signal")), maybe_float(rec.get("adjusted_signal"))
        rec["future_return"] = f"{fr:.12g}"
        rec["raw_signal_correct"] = "1" if rs is not None and sign(rs) * sign(fr) > 0 else "0"
        rec["adjusted_signal_correct"] = "1" if adj is not None and sign(adj) * sign(fr) > 0 else "0"
        rec["evaluation_status"] = "EVALUATED"


def fnum(v):
    return None if v in (None, "", "null") else float(v)


def build_summary(rows: list[dict], capture_iso: str, source_status: str) -> dict:
    n = len(rows)
    accepted = [r for r in rows if r.get("decision") == "ACCEPT"]
    abstained = [r for r in rows if r.get("decision") == "ABSTAIN"]
    evaluated = [r for r in rows if r.get("evaluation_status") == "EVALUATED"]
    def quality(sub, field):
        vals = [int(r[field]) for r in sub if r.get(field) in ("0", "1", 0, 1)]
        return (sum(vals) / len(vals)) if vals else None
    rs = [fnum(r.get("reliability")) for r in rows]; rs = [x for x in rs if x is not None]
    groups = {}
    for name, pred in [("low", lambda x: x < 0.60), ("medium", lambda x: 0.60 <= x < 0.75), ("high", lambda x: x >= 0.75)]:
        sub = [r for r in rows if fnum(r.get("reliability")) is not None and pred(fnum(r.get("reliability")))]
        groups[name] = {"n": len(sub), "evaluated_n": sum(r.get("evaluation_status") == "EVALUATED" for r in sub),
                        "pending_n": sum(r.get("evaluation_status") != "EVALUATED" for r in sub),
                        "raw_hit_rate": quality(sub, "raw_signal_correct"), "adjusted_hit_rate": quality(sub, "adjusted_signal_correct")}
    status = "SUPPORTED" if n >= 30 and len(evaluated) >= 20 else ("PARTIAL_SUPPORT" if len(evaluated) >= 1 else "INSUFFICIENT_DATA")
    return {
        "study_type": "External Transfer Validation / Binance public-data forward shadow",
        "symbol": SYMBOL, "capture_timestamp": capture_iso, "source_status": source_status,
        "data_source": PUBLIC_BASE + KLINES_PATH, "private_api_required": False,
        "sample_size": n, "date_range": [rows[0]["timestamp"], rows[-1]["timestamp"]] if rows else [],
        "raw_signal": "tanh(7-day close return / 0.05)",
        "reliability_formula": "0.30 completeness_30d + 0.30 agreement(3/7/14d) + 0.20 stability(rolling volatility) + 0.20 calibration(90d past hit rate)",
        "adjusted_signal": "raw_signal * R_market; abstain if R_market < 0.65",
        "sample_count": n, "coverage": (len(accepted) / n if n else None),
        "abstain_rate": (len(abstained) / n if n else None),
        "reliability_distribution": {"n": len(rs), "mean": mean(rs) if rs else None,
            "p10": quantile(rs, .10) if rs else None, "p50": quantile(rs, .50) if rs else None,
            "p90": quantile(rs, .90) if rs else None, "min": min(rs) if rs else None, "max": max(rs) if rs else None},
        "high_medium_low_results": groups,
        "accepted_quality": {"n": len(accepted), "evaluated_n": sum(r.get("evaluation_status") == "EVALUATED" for r in accepted), "raw_hit_rate": quality(accepted, "raw_signal_correct"), "adjusted_hit_rate": quality(accepted, "adjusted_signal_correct")},
        "abstained_quality": {"n": len(abstained), "evaluated_n": sum(r.get("evaluation_status") == "EVALUATED" for r in abstained), "raw_hit_rate": quality(abstained, "raw_signal_correct"), "adjusted_hit_rate": quality(abstained, "adjusted_signal_correct")},
        "evaluated_n": len(evaluated), "pending_future_return_n": n - len(evaluated),
        "parameter_version": PARAMETER_VERSION, "model_version": MODEL_VERSION,
        "forward_validation_status": status,
        "overall_status": status,
        "lookahead_control": "Features and decisions are frozen at capture; future_return is backfilled only after target timestamp + 24h.",
        "future_data_used_in_features": False,
        "future_return_backfill_only": True,
        "open_candle_policy": "latest observed daily close may be incomplete for raw signal; calibration uses completed daily bars only",
    }


def main() -> int:
    fail_if_unsafe()
    capture_ms = now_ms(); capture_iso = datetime.fromtimestamp(capture_ms / 1000, timezone.utc).isoformat()
    old = load_log()
    daily, context_capture = fetch_daily_context()
    CONTEXT.write_text("open_time,close,volume,close_time\n" + "\n".join(f"{r['open_time']},{r['close']},{r['volume']},{r['close_time']}" for r in daily) + "\n", encoding="utf-8")
    live = fetch_live_rows()
    seen = {r.get("timestamp") for r in old}
    rows = old[:]
    for item in live:
        if item["timestamp"] in seen:
            continue
        # Calculate each row at its own observed timestamp. The +60s margin
        # marks a 1-minute candle as observed after its close boundary.
        row_features = compute_features(daily, item["timestamp_ms"] + 60000, observed_close=item["close"])
        decision = "ABSTAIN" if row_features["reliability"] < ABSTAIN_THRESHOLD else "ACCEPT"
        rows.append({
            "timestamp": item["timestamp"], "symbol": SYMBOL, "close": f"{item['close']:.12g}", "volume": f"{item['volume']:.12g}",
            "raw_signal": f"{row_features['raw_signal']:.12g}", "reliability": f"{row_features['reliability']:.12g}",
            "completeness": f"{row_features['completeness']:.12g}", "agreement": f"{row_features['agreement']:.12g}",
            "stability": f"{row_features['stability']:.12g}", "calibration": f"{row_features['calibration']:.12g}",
            "adjusted_signal": f"{row_features['adjusted_signal']:.12g}", "decision": decision,
            "evaluation_status": "PENDING_FUTURE_RETURN", "future_return": "", "raw_signal_correct": "", "adjusted_signal_correct": "",
            "accepted_sample": "1" if decision == "ACCEPT" else "0", "abstained_sample": "1" if decision == "ABSTAIN" else "0",
            "parameter_version": PARAMETER_VERSION, "model_version": MODEL_VERSION,
            "source_endpoint": PUBLIC_BASE + KLINES_PATH, "capture_mode": "LIVE_PUBLIC_1M_SNAPSHOT",
        }); seen.add(item["timestamp"])
    update_future_returns(rows, capture_ms)
    rows.sort(key=lambda r: r.get("timestamp", ""))
    save_log(rows)
    state = {"security_mode": "PUBLIC_MARKET_DATA_ONLY", "LIVE_ORDERING_ENABLED": False, "private_api_required": False,
             "allowed_endpoint": PUBLIC_BASE + KLINES_PATH, "symbol": SYMBOL, "interval": INTERVAL,
             "daily_context_interval": DAILY_INTERVAL, "last_capture_timestamp": capture_iso,
             "last_daily_context_capture": context_capture, "parameter_version": PARAMETER_VERSION, "model_version": MODEL_VERSION,
             "orders_submitted": 0, "orders_cancelled": 0, "account_or_balance_requests": 0,
             "notes": "No API key, secret, account, order, margin, futures, transfer, or withdrawal interface is used."}
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    summary = build_summary(rows, capture_iso, "OK_PUBLIC_BINANCE_DATA_API")
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": summary["forward_validation_status"], "sample_count": summary["sample_count"], "new_records": len(rows)-len(old), "coverage": summary["coverage"], "abstain_rate": summary["abstain_rate"]}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


