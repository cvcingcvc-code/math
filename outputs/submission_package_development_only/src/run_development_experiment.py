"""Minimal DEVELOPMENT_ONLY model -> metrics -> result files.

This is a transparent row-level exploratory score, not a trained classifier.
It reuses Module C's ABL/HOT candidates and reports coverage/uncertainty and
prompt-induced/context-risk indicators. It must never be used as formal Gate
input or as a final research claim.

Run from the project root:
    python src/run_development_experiment.py
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from development_data import load_annotation_data  # noqa: E402

OUT_DIR = ROOT / "reports" / "development"
OUT_CSV = OUT_DIR / "development_metrics.csv"
OUT_JSON = OUT_DIR / "development_results.json"

BLOOM_SCORE = {f"L{i}": i for i in range(1, 7)}
VALID_EVIDENCE = set(BLOOM_SCORE)
HIGH_EVIDENCE = {"L4", "L5", "L6"}
BANNER = ["DEVELOPMENT_ONLY", "AI_PROVISIONAL", "NOT FOR FORMAL GATE OR FINAL CLAIMS"]


def numeric_or_na(value: str):
    return BLOOM_SCORE.get(value)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_annotation_data("development")
    if len(data) != 70 or not data["record_id"].is_unique:
        raise ValueError("development input must contain 70 unique record_id values")
    if set(data["annotation_source"]) != {"AI_PROVISIONAL"}:
        raise ValueError("input identity changed: annotation_source")
    if set(data["annotation_status"]) != {"DEVELOPMENT_ONLY"}:
        raise ValueError("input identity changed: annotation_status")

    result = data[["record_id", "task_bloom", "student_evidence_bloom", "task_confidence",
                   "evidence_confidence", "confidence", "task_actor", "task_source",
                   "prompt_induced", "context_truncated", "content_relation",
                   "annotation_source", "annotation_status"]].copy()
    result["task_level"] = result["task_bloom"].map(numeric_or_na)
    result["evidence_level"] = result["student_evidence_bloom"].map(numeric_or_na)
    result["evidence_observable"] = result["student_evidence_bloom"].isin(VALID_EVIDENCE)
    result["evidence_high_order"] = result["student_evidence_bloom"].isin(HIGH_EVIDENCE)
    result["task_evidence_gap"] = result["task_level"] - result["evidence_level"]
    result["prompt_induced_flag"] = result["prompt_induced"].eq("true")
    result["context_truncated_flag"] = result["context_truncated"].eq("true")
    result["development_score"] = result["evidence_level"].where(result["evidence_observable"])
    result["development_score_0_1"] = ((result["development_score"] - 1) / 5).where(result["evidence_observable"])

    eligible = result[result["evidence_observable"]]
    metrics = {
        "rows": int(len(result)),
        "evidence_coverage": round(float(result["evidence_observable"].mean()), 6),
        "evidence_high_order_share_among_observed": round(float(eligible["evidence_high_order"].mean()), 6) if len(eligible) else None,
        "abl_mean_observed": round(float(eligible["evidence_level"].mean()), 6) if len(eligible) else None,
        "abl_median_observed": float(eligible["evidence_level"].median()) if len(eligible) else None,
        "task_evidence_gap_mean_observed": round(float(eligible["task_evidence_gap"].mean()), 6) if len(eligible) else None,
        "prompt_induced_share": round(float(result["prompt_induced_flag"].mean()), 6),
        "context_truncated_share": round(float(result["context_truncated_flag"].mean()), 6),
        "low_confidence_share": round(float(result["confidence"].isin(["low"]).mean()), 6),
        "task_actor_counts": {str(k): int(v) for k, v in result["task_actor"].value_counts(dropna=False).items()},
    }

    result["result_scope"] = "DEVELOPMENT_ONLY"
    result["result_source"] = "AI_PROVISIONAL"
    result["claim_boundary"] = "NOT FOR FORMAL GATE OR FINAL CLAIMS"
    result = result[["result_scope", "result_source", "claim_boundary", "record_id",
                     "task_level", "evidence_level", "evidence_observable",
                     "evidence_high_order", "task_evidence_gap", "development_score",
                     "development_score_0_1", "task_confidence", "evidence_confidence",
                     "confidence", "task_actor", "task_source", "prompt_induced_flag",
                     "context_truncated_flag", "content_relation", "annotation_source",
                     "annotation_status"]]
    result.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    payload = {
        "banner": BANNER,
        "data_mode": "development",
        "input": "data/annotations/ai/pilot_ai_provisional.csv",
        "model": "transparent_row_level_development_score",
        "model_definition": {
            "evidence_level": "L1..L6 -> 1..6; NO_EVIDENCE/UNDETERMINED excluded from ABL/HOT denominator",
            "ABL": "mean observed student_evidence_bloom numeric level",
            "HOT": "share of observed evidence in L4/L5/L6",
            "coverage": "share of rows with observable L1..L6 evidence",
            "gap": "task_level - evidence_level on observed rows",
        },
        "metrics": metrics,
        "field_limits": [
            "No student_id, semester, session_id/session_proxy, or verified agent_type in this input: no student-level aggregation, CTQ, DHI, MAB, or agent-type comparison.",
            "No human R1/R2 labels: no reliability, calibration, formal Gate, or claim of validated model performance.",
            "task_actor and prompt_induced are descriptive pathway flags, not causal agent effects.",
        ],
        "formal_gate_eligible": False,
        "results_csv": str(OUT_CSV.relative_to(ROOT)),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(BANNER))
    print(f"rows={len(result)}")
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print("formal_gate_eligible=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
