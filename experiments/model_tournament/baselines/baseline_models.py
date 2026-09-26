"""Transparent baseline tournament for the development-only evidence model.

This module is intentionally isolated from the production model.  It reads the
70-record AI provisional development slice, validates its identity, recomputes
the frozen main candidate, and evaluates three fixed challengers:

* Baseline A: raw observable evidence only;
* Baseline B: an additive linear reliability score;
* Baseline C: a fixed L4 rule with no learned threshold.

No human worksheet is read and no production artifact is modified.  The script
writes all tournament artifacts beside this file.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
OUT = Path(__file__).resolve().parent
LEVELS = {f"L{i}": i for i in range(1, 7)}
CONFIDENCE = {"high": 1.0, "medium": 0.75, "low": 0.5}
MAIN_LAMBDA_PROMPT = 0.5
MAIN_LAMBDA_CONTEXT = 0.5
MAIN_STATUS_THRESHOLD = 0.75
RULE_HIGH_LEVEL = 4
NOISE_N = 7


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_input() -> list[dict[str, str]]:
    with INPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 70 or len({row["record_id"] for row in rows}) != 70:
        raise ValueError("expected exactly 70 unique development records")
    if {row["annotation_source"] for row in rows} != {"AI_PROVISIONAL"}:
        raise ValueError("baseline input is not AI_PROVISIONAL")
    if {row["annotation_status"] for row in rows} != {"DEVELOPMENT_ONLY"}:
        raise ValueError("baseline input is not DEVELOPMENT_ONLY")
    return rows


def evidence_level(row: dict[str, str]) -> int | None:
    return LEVELS.get(str(row.get("student_evidence_bloom", "")).strip())


def task_level(row: dict[str, str]) -> int | None:
    return LEVELS.get(str(row.get("task_bloom", "")).strip())


def main_weight(row: dict[str, str]) -> float:
    level = evidence_level(row)
    if level is None:
        return 0.0
    confidence = CONFIDENCE.get(str(row.get("confidence", "")).lower(), 0.5)
    return (confidence
            * (1.0 - MAIN_LAMBDA_PROMPT * float(bool_value(row.get("prompt_induced"))))
            * (1.0 - MAIN_LAMBDA_CONTEXT * float(bool_value(row.get("context_truncated")))))


def linear_weight(row: dict[str, str]) -> float:
    """Simple additive score; clipping is the only non-linearity."""
    if evidence_level(row) is None:
        return 0.0
    confidence = CONFIDENCE.get(str(row.get("confidence", "")).lower(), 0.5)
    prompt = float(bool_value(row.get("prompt_induced")))
    context = float(bool_value(row.get("context_truncated")))
    # c_i - .25 prompt - .25 context; the confidence term is the fixed
    # transparent mapping high=1, medium=.75, low=.5.
    return max(0.0, min(1.0, confidence - 0.25 * prompt - 0.25 * context))


def raw_weight(row: dict[str, str]) -> float:
    return 1.0 if evidence_level(row) is not None else 0.0


def rule_status(row: dict[str, str]) -> str:
    """Predeclared rule: L4+ with no visible risk is supported."""
    level = evidence_level(row)
    if level is None:
        return "NO_EFFECTIVE_EVIDENCE"
    confidence = str(row.get("confidence", "")).lower()
    risk = bool_value(row.get("prompt_induced")) or bool_value(row.get("context_truncated"))
    if level >= RULE_HIGH_LEVEL and confidence in {"high", "medium"} and not risk:
        return "SUPPORTED"
    return "LOW_SUPPORT"


def status_for_weight(weight: float) -> str:
    if weight <= 0.0:
        return "NO_EFFECTIVE_EVIDENCE"
    if weight >= MAIN_STATUS_THRESHOLD:
        return "SUPPORTED"
    return "LOW_SUPPORT"


def aggregate(rows: list[dict[str, Any]], weight_key: str, status_key: str) -> dict[str, Any]:
    total = sum(float(row[weight_key]) for row in rows)
    observable = [row for row in rows if row["raw_score"] is not None]
    weighted_scores = sum(float(row["raw_score"]) * float(row[weight_key])
                          for row in rows if row["raw_score"] is not None)
    hot = sum((1.0 if row["raw_score"] >= 4 else 0.0) * float(row[weight_key])
              for row in rows if row["raw_score"] is not None)
    gap_rows = [row for row in rows if row["raw_score"] is not None and row["task_level"] is not None]
    gap_weight = sum(float(row[weight_key]) for row in gap_rows)
    gap = (sum((row["task_level"] - row["raw_score"]) * float(row[weight_key]) for row in gap_rows)
           / gap_weight if gap_weight else None)
    score = weighted_scores / total if total > 0 else None
    hot_rate = hot / total if total > 0 else None
    status_counts = Counter(row[status_key] for row in rows)
    return {
        "main_metric": "aggregate_evidence_score",
        "aggregate_evidence_score": score,
        "raw_score_mean": (sum(row["raw_score"] for row in observable) / len(observable)
                            if observable else None),
        "hot_rate": hot_rate,
        "task_evidence_gap": gap,
        "effective_weight": total,
        "effective_coverage": total / len(rows),
        "observable_count": len(observable),
        "decision_coverage_supported": status_counts["SUPPORTED"] / len(rows),
        "status_counts": dict(status_counts),
        "missing_evidence_count": status_counts["NO_EFFECTIVE_EVIDENCE"],
        "low_support_count": status_counts["LOW_SUPPORT"],
        "supported_count": status_counts["SUPPORTED"],
        "aggregate_status": "SUPPORTED" if total > 0 else "NO_EFFECTIVE_EVIDENCE",
    }


def evaluate(rows: list[dict[str, str]], model: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    detailed: list[dict[str, Any]] = []
    for source in rows:
        row = dict(source)
        row["raw_score"] = evidence_level(source)
        row["task_level"] = task_level(source)
        if model == "MAIN":
            weight = main_weight(source)
            status = status_for_weight(weight)
        elif model == "BASELINE_A_RAW_ONLY":
            weight = raw_weight(source)
            status = "SUPPORTED" if weight > 0 else "NO_EFFECTIVE_EVIDENCE"
        elif model == "BASELINE_B_LINEAR":
            weight = linear_weight(source)
            status = status_for_weight(weight)
        elif model == "BASELINE_C_RULE":
            weight = raw_weight(source)
            status = rule_status(source)
        else:
            raise ValueError(model)
        row["weight"] = weight
        row["status"] = status
        detailed.append(row)
    return detailed, aggregate(detailed, "weight", "status")


def stable_observable_ids(rows: list[dict[str, str]], n: int = NOISE_N) -> list[str]:
    candidates = [row["record_id"] for row in rows if evidence_level(row) is not None]
    ranked = sorted(candidates, key=lambda x: hashlib.sha256(("noise-v1:" + x).encode()).hexdigest())
    return ranked[: min(n, len(ranked))]


def perturb(rows: list[dict[str, str]], ids: list[str], mode: str) -> list[dict[str, str]]:
    result = [dict(row) for row in rows]
    by_id = {row["record_id"]: row for row in result}
    for index, record_id in enumerate(ids):
        row = by_id[record_id]
        if mode == "risk_flag_flip_10pct":
            row["prompt_induced"] = "false" if bool_value(row["prompt_induced"]) else "true"
        elif mode == "evidence_level_shift_10pct":
            current = evidence_level(row)
            if current is not None:
                shifted = max(1, min(6, current + (1 if index % 2 == 0 else -1)))
                row["student_evidence_bloom"] = f"L{shifted}"
        else:
            raise ValueError(mode)
    return result


def decision_flip_count(base: list[dict[str, Any]], changed: list[dict[str, Any]]) -> int:
    return sum(a["status"] != b["status"] for a, b in zip(base, changed))


def score_order_stability(base: list[dict[str, Any]], changed: list[dict[str, Any]]) -> float | None:
    pairs: list[tuple[float, float]] = []
    for left, right in zip(base, changed):
        if left["raw_score"] is not None and right["raw_score"] is not None:
            pairs.append((float(left["raw_score"]) * float(left["weight"]),
                          float(right["raw_score"]) * float(right["weight"])))
    if len(pairs) < 2:
        return None
    concordant = discordant = comparable = 0
    for i, (a1, b1) in enumerate(pairs):
        for a2, b2 in pairs[i + 1:]:
            da, db = a1 - a2, b1 - b2
            if da == 0 or db == 0:
                continue
            comparable += 1
            if da * db > 0:
                concordant += 1
            else:
                discordant += 1
    return (concordant - discordant) / comparable if comparable else 1.0


def run_noise(rows: list[dict[str, str]], models: list[str]) -> dict[str, Any]:
    ids = stable_observable_ids(rows)
    result: dict[str, Any] = {"selected_record_ids": ids, "n": len(ids), "protocol": "fixed SHA-256 rank; no tuning"}
    for mode in ("risk_flag_flip_10pct", "evidence_level_shift_10pct"):
        changed_rows = perturb(rows, ids, mode)
        mode_result: dict[str, Any] = {}
        for model in models:
            base_detail, base_agg = evaluate(rows, model)
            new_detail, new_agg = evaluate(changed_rows, model)
            old_score = base_agg["aggregate_evidence_score"]
            new_score = new_agg["aggregate_evidence_score"]
            mode_result[model] = {
                "base_aggregate_evidence_score": old_score,
                "perturbed_aggregate_evidence_score": new_score,
                "delta_aggregate_evidence_score": None if old_score is None or new_score is None else new_score - old_score,
                "base_effective_coverage": base_agg["effective_coverage"],
                "perturbed_effective_coverage": new_agg["effective_coverage"],
                "decision_flip_count": decision_flip_count(base_detail, new_detail),
                "score_order_stability": score_order_stability(base_detail, new_detail),
            }
        result[mode] = mode_result
    return result


def main_parameter_sensitivity(rows: list[dict[str, str]]) -> dict[str, Any]:
    values = {"lambda_prompt": [0.0, 0.25, 0.5, 0.75, 1.0],
              "lambda_context": [0.0, 0.25, 0.5, 0.75, 1.0],
              "r_medium": [0.5, 0.75, 1.0]}
    scores: list[float] = []
    weights: list[float] = []
    undefined = 0
    for lp in values["lambda_prompt"]:
        for lc in values["lambda_context"]:
            for rm in values["r_medium"]:
                detailed: list[dict[str, Any]] = []
                for source in rows:
                    raw = evidence_level(source)
                    confidence = {"high": 1.0, "medium": rm, "low": 0.5}.get(str(source.get("confidence", "")).lower(), 0.5)
                    weight = 0.0 if raw is None else confidence * (1 - lp * float(bool_value(source.get("prompt_induced")))) * (1 - lc * float(bool_value(source.get("context_truncated"))))
                    detailed.append({"raw_score": raw, "weight": weight, "task_level": task_level(source), "status": status_for_weight(weight)})
                agg = aggregate(detailed, "weight", "status")
                if agg["aggregate_evidence_score"] is None:
                    undefined += 1
                else:
                    scores.append(agg["aggregate_evidence_score"])
                    weights.append(agg["effective_weight"])
    return {"grid": values, "grid_size": 75, "defined_cells": len(scores), "undefined_cells": undefined,
            "aggregate_evidence_score_range": [min(scores), max(scores)] if scores else [None, None],
            "effective_weight_range": [min(weights), max(weights)] if weights else [None, None],
            "interpretation": "Main-model parameter sensitivity only; no baseline threshold was tuned."}


def git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "UNKNOWN"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    keys = list(rows[0])
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_input()
    models = ["MAIN", "BASELINE_A_RAW_ONLY", "BASELINE_B_LINEAR", "BASELINE_C_RULE"]
    details: dict[str, list[dict[str, Any]]] = {}
    aggregates: dict[str, dict[str, Any]] = {}
    for model in models:
        details[model], aggregates[model] = evaluate(rows, model)

    # The existing main-model development artifact must agree with this local
    # recomputation before a comparison is written.
    expected = {"aggregate_evidence_score": 3.5625, "effective_weight": 6.0, "effective_coverage": 6.0 / 70.0}
    for key, value in expected.items():
        if not math.isclose(float(aggregates["MAIN"][key]), value, rel_tol=0, abs_tol=1e-12):
            raise AssertionError(f"main recomputation mismatch for {key}")

    aggregate_rows = []
    for model in models:
        item = aggregates[model]
        aggregate_rows.append({"model": model, **{k: v for k, v in item.items() if k != "status_counts"},
                               "status_counts": json.dumps(item["status_counts"], ensure_ascii=False, sort_keys=True),
                               "accuracy": "NOT_COMPUTABLE_NO_HUMAN_TRUTH",
                               "classification_sensitivity": "NOT_COMPUTABLE_NO_HUMAN_TRUTH",
                               "external_transfer": "NOT_SUPPORTED_FOR_COMPARISON"})
    write_csv(OUT / "baseline_results.csv", aggregate_rows)

    record_rows = []
    for model in models:
        for row in details[model]:
            record_rows.append({"model": model, "record_id": row["record_id"], "raw_score": row["raw_score"],
                                "weight": row["weight"], "status": row["status"],
                                "task_level": row["task_level"], "prompt_induced": row["prompt_induced"],
                                "context_truncated": row["context_truncated"], "confidence": row["confidence"]})
    write_csv(OUT / "baseline_record_results.csv", record_rows)

    noise = run_noise(rows, models)
    comparison = {
        "models": models,
        "main_model": {"formula": "w=I(obs)c(1-0.5p)(1-0.5t)", "status_rule": "w>=0.75 SUPPORTED; 0<w<0.75 LOW_SUPPORT; w=0 NO_EFFECTIVE_EVIDENCE"},
        "baseline_a": {"formula": "w=I(obs)", "status_rule": "observable SUPPORTED; missing NO_EFFECTIVE_EVIDENCE"},
        "baseline_b": {"formula": "w=clip(c-0.25p-0.25t,0,1)", "status_rule": "same fixed 0.75 status cutoff as main"},
        "baseline_c": {"formula": "decision rule: L4-L6 and confidence in {high,medium} and p=t=false -> SUPPORTED; observable otherwise LOW_SUPPORT; missing NO_EFFECTIVE_EVIDENCE", "threshold_source": "existing HOT/high-level boundary L4; predeclared, not tuned"},
        "aggregate_results": aggregates,
        "noise_perturbation": noise,
        "main_parameter_sensitivity": main_parameter_sensitivity(rows),
        "missing_evidence_protocol": "All methods preserve missing/undetermined evidence as NO_EFFECTIVE_EVIDENCE; no zero substitution.",
        "counterexample_protocol": "Disagreements are development structural cases, not false/true labels; human Gate is pending.",
        "external_transfer": {"status": "NOT_SUPPORTED_FOR_COMPARISON", "reason": "No paired educational outcome or human truth; finance artifact is secondary structural transfer only."},
    }
    metadata = {"experiment_id": "BASELINE_MODEL_TOURNAMENT_V1", "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "git_head": git_head(), "input_file": str(INPUT.relative_to(ROOT)).replace("\\", "/"),
                "input_sha256": sha256_file(INPUT), "sample_count": len(rows), "input_identity": "AI_PROVISIONAL / DEVELOPMENT_ONLY",
                "formal_gate_eligible": False, "parameters": {"main_lambda_prompt": MAIN_LAMBDA_PROMPT, "main_lambda_context": MAIN_LAMBDA_CONTEXT,
                "main_status_threshold": MAIN_STATUS_THRESHOLD, "rule_high_level": RULE_HIGH_LEVEL, "noise_n": NOISE_N},
                "outputs": ["baseline_models.py", "baseline_models.md", "baseline_results.csv", "baseline_results.json", "baseline_record_results.csv", "baseline_failure_cases.md", "baseline_comparison.md"]}
    payload = {"metadata": metadata, "comparison": comparison}
    (OUT / "baseline_results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"experiment_id": metadata["experiment_id"], "output": str(OUT), "models": models, "records": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
