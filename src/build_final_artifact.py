"""Build the single development artifact used by paper/demo/figures.

This script consumes only AI_PROVISIONAL records and applies the frozen,
deterministic reliability formula. It never calls an LLM and never reads
human worksheets. The output is explicitly development-only.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/annotations/ai/pilot_ai_provisional.csv"
OUT = ROOT / "outputs"
REPORT = ROOT / "reports/development"
LEVELS = {f"L{i}": i for i in range(1, 7)}
CONF = {"high": 1.0, "medium": 0.75, "low": 0.5}
FACTORS = ("-20%", "-10%", "baseline", "+10%", "+20%")


def b(v: object) -> bool:
    return str(v).strip().lower() == "true"


def score_frame(df: pd.DataFrame, lp: float = 0.5, lc: float = 0.5,
                r_medium: float = 0.75, r_high: float = 1.0,
                r_low: float = 0.5) -> tuple[pd.DataFrame, dict]:
    d = df.copy()
    d["raw_score"] = d["student_evidence_bloom"].map(LEVELS)
    d["observable"] = d["raw_score"].notna()
    d["confidence_reliability"] = d["confidence"].map({"high": r_high, "medium": r_medium, "low": r_low}).fillna(r_low)
    d["evidence_reliability"] = (
        d["observable"].astype(float) * d["confidence_reliability"]
        * (1 - lp * d["prompt_induced"].map(b).astype(float))
        * (1 - lc * d["context_truncated"].map(b).astype(float))
    )
    d["adjusted_score"] = d["raw_score"] * d["evidence_reliability"]
    d["evaluation_status"] = "NO_EFFECTIVE_EVIDENCE"
    d.loc[d["observable"] & (d["evidence_reliability"] >= 0.75), "evaluation_status"] = "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT"
    d.loc[d["observable"] & (d["evidence_reliability"] < 0.75) & (d["evidence_reliability"] > 0), "evaluation_status"] = "LOW_SUPPORT"
    total = float(d["evidence_reliability"].sum())
    defined = total > 0
    aggregate = {
        "raw_score": float(d.loc[d.observable, "raw_score"].mean()) if d.observable.any() else None,
        "adjusted_score": float(d["adjusted_score"].sum() / total) if defined else None,
        "evidence_reliability": total / len(d),
        "effective_weight": total,
        "effective_coverage": total / len(d),
        "evaluation_status": "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT" if defined else "NO_EFFECTIVE_EVIDENCE",
        "included_evidence_count": int(d.observable.sum()),
    }
    return d, aggregate


def explanation(row: pd.Series) -> tuple[list[str], list[str], str]:
    positive = []
    negative = []
    if pd.notna(row.raw_score):
        positive.append(f"student_evidence_bloom={row.student_evidence_bloom}")
    if row.confidence == "high":
        positive.append("confidence=high")
    for col, label in (("prompt_induced", "prompt_induced"), ("context_truncated", "context_truncated")):
        if b(row[col]):
            negative.append(label)
    if row.confidence == "low":
        negative.append("confidence=low")
    if row.evaluation_status == "NO_EFFECTIVE_EVIDENCE":
        text = "No effective evidence: student evidence is not an observable L1-L6 level or its deterministic weight is zero."
    else:
        text = (f"Raw Evidence {row.student_evidence_bloom} contributes with deterministic reliability "
                f"{row.evidence_reliability:.3f}; adjusted contribution is raw score multiplied by that reliability.")
    return positive, negative, text


def main() -> int:
    OUT.mkdir(exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    if len(data) != 70 or set(data.annotation_source) != {"AI_PROVISIONAL"} or set(data.annotation_status) != {"DEVELOPMENT_ONLY"}:
        raise ValueError("unexpected development input identity")
    detailed, adjusted = score_frame(data)
    records = []
    for _, row in detailed.iterrows():
        pos, neg, text = explanation(row)
        records.append({"record_id": row.record_id, "raw_score": None if pd.isna(row.raw_score) else float(row.raw_score),
                        "evidence_reliability": float(row.evidence_reliability),
                        "adjusted_score": None if pd.isna(row.adjusted_score) else float(row.adjusted_score),
                        "evaluation_status": row.evaluation_status, "positive_factors": pos,
                        "negative_factors": neg, "explanation": text,
                        "annotation_source": row.annotation_source, "annotation_status": row.annotation_status})
    explain_path = REPORT / "explain_records.json"
    explain_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    # Three parameters already present in the frozen sensitivity model.
    params = {"lambda_prompt": 0.5, "lambda_context": 0.5, "r_medium": 0.75}
    what_if = []
    for name, baseline in params.items():
        for factor in FACTORS:
            mult = {"-20%": 0.8, "-10%": 0.9, "baseline": 1.0, "+10%": 1.1, "+20%": 1.2}[factor]
            value = baseline * mult
            kwargs = {"lp": params["lambda_prompt"], "lc": params["lambda_context"], "r_medium": params["r_medium"]}
            if name == "lambda_prompt": kwargs["lp"] = value
            elif name == "lambda_context": kwargs["lc"] = value
            else: kwargs["r_medium"] = value
            _, agg = score_frame(data, **kwargs)
            what_if.append({"parameter": name, "change": factor, "value": value,
                            "delta_reliability": agg["evidence_reliability"] - adjusted["evidence_reliability"],
                            "delta_adjusted_score": None if agg["adjusted_score"] is None else agg["adjusted_score"] - adjusted["adjusted_score"],
                            "evaluation_status_changed": agg["evaluation_status"] != adjusted["evaluation_status"],
                            "core_conclusion_changed": abs((agg["adjusted_score"] or 0) - (adjusted["adjusted_score"] or 0)) > 1e-9,
                            "adjusted_score": agg["adjusted_score"], "evaluation_status": agg["evaluation_status"]})
    what_if_path = REPORT / "what_if_sensitivity.csv"
    pd.DataFrame(what_if).to_csv(what_if_path, index=False, encoding="utf-8-sig")

    raw_metrics = json.loads((REPORT / "research_core_closure.json").read_text(encoding="utf-8"))
    ablation = pd.read_csv(REPORT / "ablation_results.csv", encoding="utf-8-sig").to_dict(orient="records")
    counter = pd.read_csv(REPORT / "counterexamples.csv", encoding="utf-8-sig").to_dict(orient="records")
    transfer_path = ROOT / "experiments/transfer_finance/transfer_validation.json"
    transfer_raw = json.loads(transfer_path.read_text(encoding="utf-8")) if transfer_path.exists() else None
    shadow_path = ROOT / "experiments/transfer_finance/live_shadow/live_shadow_summary.json"
    shadow_raw = json.loads(shadow_path.read_text(encoding="utf-8")) if shadow_path.exists() else None
    transfer = {
        "source_artifact": "experiments/transfer_finance/transfer_validation.json",
        "status": "SYNCED_EXISTING_RESULT" if transfer_raw else "NOT_AVAILABLE",
        "structural_transfer": "PRELIMINARY_SUPPORT",
        "reliability_separation": "WEAK_PARTIAL_SUPPORT",
        "sensitivity_robustness": "DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT",
        "risk_coverage_improvement": "NOT_SUPPORTED",
        "trading_advantage": "NOT_SUPPORTED_CLAIM",
        "paper_use": "small external validation only; not a trading strategy",
        "source_overall_status": transfer_raw.get("overall_status") if transfer_raw else None,
        "sample_size": transfer_raw.get("sample_size") if transfer_raw else None,
        "binance_shadow": {"status": "INDEPENDENT_PUBLIC_DATA_ONLY" if shadow_raw else "NOT_PRESENT",
                           "source_artifact": "experiments/transfer_finance/live_shadow/live_shadow_summary.json" if shadow_raw else None,
                           "sample_size": shadow_raw.get("sample_size") if shadow_raw else None,
                           "private_api_required": shadow_raw.get("private_api_required") if shadow_raw else None,
                           "trading_performed": False,
                           "main_model_parameters_modified": False,
                           "short_term_returns_in_main_conclusion": False},
    }
    development_results = {
        "data_identity": "AI_PROVISIONAL / DEVELOPMENT_ONLY",
        "sample_count": len(data), "raw_summary": raw_metrics["raw"],
        "reliability_summary": {"mean_record_reliability": adjusted["evidence_reliability"], "effective_weight": adjusted["effective_weight"]},
        "adjusted_summary": {**raw_metrics["adjusted"], "aggregate_adjusted_score": adjusted["adjusted_score"]},
        "explain_output": "reports/development/explain_records.json",
        "explain_records": records,
    }
    limitations = ["Human Gate 未完成，当前结果不是正式验证结果。", "AI_PROVISIONAL 标签不替代 HUMAN_VALIDATED。", "Transfer 仅为结构迁移演示，不支持交易优势。", "不推断因果 AIV、长期能力或学生排名。"]
    artifact = {"metadata": {"status": "RESEARCH_CORE_FROZEN_FOR_SUBMISSION", "annotation_source": "AI_PROVISIONAL",
                              "annotation_status": "DEVELOPMENT_ONLY", "formal_gate_eligible": False,
                              "model": "Observed Performance -> Evidence Reliability -> Adjusted Evaluation -> Evaluability"},
                "data_identity": {"source": "data/annotations/ai/pilot_ai_provisional.csv", "sample_count": len(data),
                                  "human_gate_status": "NOT_RUN", "formal_aiv_status": "NOT_AVAILABLE_PENDING_FORMAL_GATE"},
                "model_parameters": {"lambda_prompt": 0.5, "lambda_context": 0.5, "confidence_weights": CONF,
                                     "evaluation_statuses": ["DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT", "LOW_SUPPORT", "NO_EFFECTIVE_EVIDENCE"]},
                "raw_summary": raw_metrics["raw"], "reliability_summary": {"mean_record_reliability": adjusted["evidence_reliability"], "effective_weight": adjusted["effective_weight"]},
                "adjusted_summary": {**raw_metrics["adjusted"], "aggregate_adjusted_score": adjusted["adjusted_score"]},
                "explain_output": "reports/development/explain_records.json", "sensitivity": {"what_if": "reports/development/what_if_sensitivity.csv", "parameters": list(params), "rows": what_if},
                "ablation": ablation, "counterexamples": counter,
                "figures": {"raw_vs_adjusted": "reports/development/raw_vs_adjusted_scatter.svg",
                            "reliability_distribution": "reports/development/evidence_reliability_distribution.svg",
                            "parameter_sensitivity": "reports/development/parameter_sensitivity.svg",
                            "ablation": "reports/development/ablation_comparison.svg",
                            "counterexamples": "reports/development/counterexamples.svg"},
                "development_results": development_results,
                "human_validation": {"status": "PENDING_REAL_HUMAN_R1_R2", "formal_gate_status": "NOT_RUN", "formal_gate_eligible": False},
                "transfer_validation": transfer,
                "limitations": limitations,
                "human_validation_status": "PENDING_REAL_HUMAN_R1_R2", "transfer_validation_status": transfer["status"]}
    final_path = OUT / "final_results.json"
    final_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"final_results": str(final_path), "explain_records": str(explain_path), "what_if": str(what_if_path), "records": len(records), "what_if_rows": len(what_if)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
