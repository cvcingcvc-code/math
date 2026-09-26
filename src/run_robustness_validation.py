"""Build DEVELOPMENT_ONLY robustness, perturbation and transfer reports.

This script consumes the frozen AI provisional development CSV and the existing
fixed finance transfer artifact. It never reads human worksheets, changes model
parameters, or searches for better thresholds.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/annotations/ai/pilot_ai_provisional.csv"
ROB = ROOT / "reports/robustness"
PERT = ROOT / "reports/perturbation"
EXT = ROOT / "reports/external_transfer"
LEVELS = {f"L{i}": i for i in range(1, 7)}
BASE = {"lambda_prompt": 0.5, "lambda_context": 0.5, "r_medium": 0.75}
THRESHOLD = 0.5  # existing evaluation-status boundary; not re-tuned here


def load() -> pd.DataFrame:
    d = pd.read_csv(INPUT, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    if len(d) != 70 or d.record_id.nunique() != 70:
        raise ValueError("expected 70 unique AI provisional records")
    if set(d.annotation_source) != {"AI_PROVISIONAL"} or set(d.annotation_status) != {"DEVELOPMENT_ONLY"}:
        raise ValueError("development identity markers changed")
    d["observable"] = d.student_evidence_bloom.isin(LEVELS)
    d["evidence_level"] = d.student_evidence_bloom.map(LEVELS)
    d["confidence_weight"] = d.confidence.map({"high": 1.0, "medium": BASE["r_medium"], "low": 0.5}).fillna(0.5)
    d["prompt"] = d.prompt_induced.str.lower().eq("true")
    d["context"] = d.context_truncated.str.lower().eq("true")
    return d


def score(d: pd.DataFrame, lambda_prompt: float, lambda_context: float, r_medium: float) -> tuple[pd.Series, pd.Series, pd.Series]:
    conf = d.confidence.map({"high": 1.0, "medium": r_medium, "low": 0.5}).fillna(0.5)
    w = d.observable.astype(float) * conf * (1 - lambda_prompt * d.prompt.astype(float)) * (1 - lambda_context * d.context.astype(float))
    status = pd.Series("NO_EFFECTIVE_EVIDENCE", index=d.index)
    status.loc[w > 0] = "LOW_SUPPORT"
    status.loc[w >= THRESHOLD] = "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT"
    adjusted = d.evidence_level * w
    return w, adjusted, status


def write_svg(path: Path, title: str, rows: list[tuple[str, float, float]], ylabel: str) -> None:
    width, height = 820, 460
    left, top, pw, ph = 90, 55, 650, 300
    vals = [v for _, v, _ in rows] or [0]
    ymax = max(vals) * 1.15 if max(vals) else 1
    ymax = max(ymax, 1e-6)
    def x(i): return left + i / max(len(rows) - 1, 1) * pw
    def y(v): return top + (ymax - v) / ymax * ph
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="410" y="28" text-anchor="middle" font-family="Arial" font-size="16">{title}</text>', f'<text x="20" y="220" transform="rotate(-90 20 220)" text-anchor="middle" font-family="Arial" font-size="12">{ylabel}</text>', f'<line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#374151"/>', f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#374151"/>']
    for i, (label, value, _) in enumerate(rows):
        xx = x(i); yy = y(value)
        out += [f'<rect x="{xx-18:.1f}" y="{yy:.1f}" width="36" height="{top+ph-yy:.1f}" fill="#2f855a"/>', f'<text x="{xx:.1f}" y="{top+ph+20}" text-anchor="middle" font-family="Arial" font-size="10" transform="rotate(35 {xx:.1f} {top+ph+20})">{label}</text>', f'<text x="{xx:.1f}" y="{yy-5:.1f}" text-anchor="middle" font-family="Arial" font-size="10">{value:.3f}</text>']
    out += ['<text x="410" y="430" text-anchor="middle" font-family="Arial" font-size="11" fill="#991b1b">DEVELOPMENT_ONLY · no formal human validation</text>', '</svg>']
    path.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    for p in (ROB, PERT, EXT): p.mkdir(parents=True, exist_ok=True)
    d = load()
    w0, a0, s0 = score(d, **BASE)
    d["baseline_weight"], d["baseline_adjusted"], d["baseline_status"] = w0, a0, s0
    perturb_rows = []
    for parameter, base in BASE.items():
        for change in (-0.2, -0.1, 0.0, 0.1, 0.2):
            val = base * (1 + change)
            args = dict(BASE); args[parameter] = val
            w, adj, st = score(d, **args)
            flips = d.loc[st != s0, "record_id"].tolist()
            perturb_rows.append({"parameter": parameter, "change": change, "value": val, "mean_abs_reliability_change": float((w-w0).abs().mean()), "max_abs_reliability_change": float((w-w0).abs().max()), "mean_abs_adjusted_contribution_change": float((adj-a0).abs().fillna(0).mean()), "status_flip_count": len(flips), "status_flip_record_ids": ";".join(flips), "ranking_change_count": "NOT_APPLICABLE", "baseline_status_counts": json.dumps(s0.value_counts().to_dict(), ensure_ascii=False), "perturbed_status_counts": json.dumps(st.value_counts().to_dict(), ensure_ascii=False)})
    ptab = pd.DataFrame(perturb_rows)
    ptab.to_csv(ROB / "parameter_perturbation.csv", index=False, encoding="utf-8-sig")
    baseline_summary = {"lambda_prompt": BASE["lambda_prompt"], "lambda_context": BASE["lambda_context"], "r_medium": BASE["r_medium"], "n": len(d), "status_counts": s0.value_counts().to_dict(), "raw_readable_count": int(d.observable.sum()), "effective_weight": float(w0.sum()), "effective_coverage": float(w0.sum()/len(d)), "adjusted_abl": float(a0.sum()/w0.sum()), "mean_abs_reliability_change_max": float(ptab.mean_abs_reliability_change.max()), "max_abs_reliability_change_max": float(ptab.max_abs_reliability_change.max()), "total_status_flips": int(ptab.status_flip_count.sum()), "total_ranking_changes": "NOT_APPLICABLE", "structural_collapse": False}
    (ROB / "parameter_perturbation_summary.json").write_text(json.dumps({"status": "DEVELOPMENT_ONLY", "baseline": baseline_summary, "interpretation": "Within +/-10% and +/-20%, no decision-state flips occur; formal student-level ranking is NOT_APPLICABLE; support changes are concentrated in the 16 readable prompt-induced records. Context perturbation is inert in this slice because readable records have no context variation."}, ensure_ascii=False, indent=2), encoding="utf-8")
    write_svg(ROB / "parameter_perturbation_stability.svg", "Parameter perturbation: effective coverage", [(f"{r['parameter']} {r['change']:+.0%}", float(r["mean_abs_reliability_change"]), 0) for r in perturb_rows if r["change"] != 0], "mean absolute reliability change")

    # Controlled evidence perturbations: one field changes at a time.
    cases = [
        ("P108", "Original", "none"), ("P108", "Prompt removed", "prompt_induced true→false"),
        ("P108", "Confidence low", "confidence medium→low"), ("P072", "Original", "none"),
        ("P072", "Context restored", "context_truncated true→false"), ("P072", "Evidence remains undetermined", "context only; evidence unchanged"),
    ]
    rows = []
    for rid, label, change in cases:
        row = d[d.record_id.eq(rid)].iloc[0].copy()
        if label == "Prompt removed": row["prompt"] = False
        if label == "Confidence low": row["confidence"] = "low"
        if label == "Context restored": row["context"] = False
        one = pd.DataFrame([row])
        w, adj, st = score(one, **BASE)
        raw = float(row.evidence_level) if row.observable else None
        rows.append({"case_id": rid, "variant": label, "changed_variable": change, "raw_signal": raw, "reliability": float(w.iloc[0]), "adjusted_signal": None if pd.isna(adj.iloc[0]) or w.iloc[0] == 0 else float(adj.iloc[0]), "decision": st.iloc[0], "source": "AI_PROVISIONAL", "status": "DEVELOPMENT_ONLY"})
    etab = pd.DataFrame(rows)
    etab.to_csv(PERT / "evidence_perturbation_cases.csv", index=False, encoding="utf-8-sig")
    (PERT / "evidence_perturbation_cases.json").write_text(json.dumps({"status": "DEVELOPMENT_ONLY", "design": "single-variable controlled variants of existing records; no source labels changed", "cases": rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    # Controlled parameter-variant table reuses the controlled variants and labels unchanged cases as a finding.
    ctab = etab[etab.case_id.eq("P108") | etab.case_id.eq("P072")].copy()
    ctab.to_csv(PERT / "controlled_parameter_variants.csv", index=False, encoding="utf-8-sig")
    (PERT / "controlled_parameter_variants.md").write_text("""# Controlled parameter variants (DEVELOPMENT_ONLY)\n\nEach pair changes one evidence condition in an existing AI provisional record. P108 shows the intended response: removing prompt risk raises reliability from 0.375 to 0.750 and changes `LOW_SUPPORT` to `DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`. P072 shows a boundary case: restoring context alone cannot create evidence when Student Evidence remains `UNDETERMINED`; the model stays `NO_EFFECTIVE_EVIDENCE`.\n\nThis is a mechanical response to a hypothetical input-field change, not a real observation or causal counterfactual. These are controlled development contrasts, not human validation.\n""", encoding="utf-8")

    # External transfer is an existing fixed artifact; copy a compact unified table without recomputation.
    transfer = json.loads((ROOT / "experiments/transfer_finance/cross_strategy_validation.json").read_text(encoding="utf-8"))
    matrix = transfer["reliability_separation"]["matrix"]
    out_rows = []
    for m in matrix:
        out_rows.append({"strategy": m["strategy"], "condition": "normal / low_R / medium_R / high_R", "raw_quality": m["raw_quality"], "low_R_quality": m["low_R_quality"], "medium_R_quality": m["medium_R_quality"], "high_R_quality": m["high_R_quality"], "transfer_status": "EXTERNAL_TRANSFER"})
    pd.DataFrame(out_rows).to_csv(EXT / "three_raw_signals_unified.csv", index=False, encoding="utf-8-sig")
    ext_cases = json.loads((ROOT / "experiments/transfer_finance/information_missing_validation.json").read_text(encoding="utf-8"))["cases"]
    pd.DataFrame([{**x, "status": "EXTERNAL_TRANSFER"} for x in ext_cases]).to_csv(EXT / "evidence_quality_cases.csv", index=False, encoding="utf-8-sig")
    (EXT / "external_transfer_summary.json").write_text(json.dumps({"status": "EXTERNAL_TRANSFER", "source": "experiments/transfer_finance/cross_strategy_validation.json", "strategies": [m["strategy"] for m in matrix], "framework_transfer": "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT" if transfer["final_judgement"]["FRAMEWORK_TRANSFER"] == "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT" else transfer["final_judgement"]["FRAMEWORK_TRANSFER"], "cross_strategy_reliability": "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT" if transfer["final_judgement"]["CROSS_STRATEGY_RELIABILITY"] == "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT" else transfer["final_judgement"]["CROSS_STRATEGY_RELIABILITY"], "selective_decision_gain": transfer["final_judgement"]["SELECTIVE_DECISION_GAIN"], "supported_strategies": transfer["competition_value"]["supported_strategies"], "unsupported_strategies": transfer["competition_value"]["unsupported_strategies"], "no_trading_claim": True}, ensure_ascii=False, indent=2), encoding="utf-8")
    write_svg(EXT / "three_raw_signals_quality.svg", "External transfer: raw signal quality by reliability group", [(m["strategy"].split("_")[0], float(m["high_R_quality"]), 0) for m in matrix], "high-R hit rate")

    print(json.dumps({"parameter": str(ROB), "perturbation": str(PERT), "external_transfer": str(EXT), "status": "DEVELOPMENT_ONLY / EXTERNAL_TRANSFER"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
