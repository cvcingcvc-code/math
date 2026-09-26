"""Build the development-only core research closure artifacts.

The script reuses the frozen transparent reliability formula already used by
``run_reliability_sensitivity.py``.  It adds auditable Raw/Adjusted metrics,
an explicit M0-M3 ablation table, and record-level counterexamples.  It never
reads human worksheets and never marks provisional results as formal evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
OUT = ROOT / "reports" / "development"
LEVELS = {f"L{i}": i for i in range(1, 7)}
HIGH = {"L4", "L5", "L6"}
CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.75, "low": 0.5}


def flag(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def metrics(data: pd.DataFrame, lambda_prompt: float, lambda_context: float,
            use_confidence: bool) -> dict[str, object]:
    d = data.copy()
    d["task_level"] = d["task_bloom"].map(LEVELS)
    d["evidence_level"] = d["student_evidence_bloom"].map(LEVELS)
    d["observable"] = d["evidence_level"].notna()
    d["prompt"] = flag(d["prompt_induced"])
    d["context"] = flag(d["context_truncated"])
    confidence = d["confidence"].map(CONFIDENCE_WEIGHT).fillna(0.5) if use_confidence else 1.0
    d["weight"] = (
        d["observable"].astype(float)
        * confidence
        * (1.0 - lambda_prompt * d["prompt"].astype(float))
        * (1.0 - lambda_context * d["context"].astype(float))
    )
    evidence = d[d["observable"]]
    total = float(d["weight"].sum())
    gap_rows = d[d["observable"] & d["task_level"].notna()]
    gap_weight = float(gap_rows["weight"].sum())
    defined = total > 0
    return {
        "ABL": float((d["evidence_level"] * d["weight"]).sum() / total) if defined else None,
        "HOT": float((d["evidence_level"].ge(4).astype(float) * d["weight"]).sum() / total) if defined else None,
        "Task_Evidence_Gap": float(((d["task_level"] - d["evidence_level"]) * d["weight"]).sum() / gap_weight) if gap_weight else None,
        "effective_weight": total,
        "effective_coverage": total / len(d),
        "included_evidence_count": int(len(evidence)),
        "status": "DEFINED" if defined else "NO_EFFECTIVE_EVIDENCE",
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    if len(data) != 70 or data["record_id"].nunique() != 70:
        raise ValueError("expected 70 unique development records")
    if set(data["annotation_source"]) != {"AI_PROVISIONAL"} or set(data["annotation_status"]) != {"DEVELOPMENT_ONLY"}:
        raise ValueError("development identity markers changed")

    raw = metrics(data, 0.0, 0.0, use_confidence=False)
    adjusted = metrics(data, 0.5, 0.5, use_confidence=True)
    rows = []
    for metric in ("ABL", "HOT", "Task_Evidence_Gap"):
        r, a = raw[metric], adjusted[metric]
        rows.append({
            "metric": metric,
            "raw": r,
            "adjusted": a,
            "absolute_change": None if r is None or a is None else a - r,
            "relative_change": None if r in (None, 0) or a is None else (a - r) / r,
            "effective_weight": adjusted["effective_weight"],
            "effective_coverage": adjusted["effective_coverage"],
            "status": adjusted["status"],
        })
    for metric in ("effective_weight", "effective_coverage", "included_evidence_count"):
        rows.append({
            "metric": metric,
            "raw": raw[metric],
            "adjusted": adjusted[metric],
            "absolute_change": adjusted[metric] - raw[metric],
            "relative_change": (adjusted[metric] - raw[metric]) / raw[metric] if raw[metric] else None,
            "effective_weight": adjusted["effective_weight"],
            "effective_coverage": adjusted["effective_coverage"],
            "status": adjusted["status"],
        })
    pd.DataFrame(rows).to_csv(OUT / "raw_adjusted_metrics.csv", index=False, encoding="utf-8-sig")

    models = [
        ("M0_No_correction", 0.0, 0.0, False),
        ("M1_Confidence_only", 0.0, 0.0, True),
        ("M2_Confidence_Prompt", 0.5, 0.0, True),
        ("M3_Confidence_Prompt_Context", 0.5, 0.5, True),
    ]
    ablation_rows = []
    for name, lp, lc, use_confidence in models:
        m = metrics(data, lp, lc, use_confidence)
        ablation_rows.append({"model": name, "lambda_prompt": lp, "lambda_context": lc,
                              "confidence_weighting": use_confidence, **m})
    pd.DataFrame(ablation_rows).to_csv(OUT / "ablation_results.csv", index=False, encoding="utf-8-sig")

    data["task_level"] = data["task_bloom"].map(LEVELS)
    data["evidence_level"] = data["student_evidence_bloom"].map(LEVELS)
    data["prompt"] = flag(data["prompt_induced"])
    data["context"] = flag(data["context_truncated"])
    data["confidence_weight"] = data["confidence"].map(CONFIDENCE_WEIGHT).fillna(0.5)
    data["reliability_weight"] = (
        data["evidence_level"].notna().astype(float) * data["confidence_weight"]
        * (1 - 0.5 * data["prompt"].astype(float))
        * (1 - 0.5 * data["context"].astype(float))
    )
    data["effective_contribution"] = data["evidence_level"].fillna(0) * data["reliability_weight"]
    case_specs = [
        ("Case_A_high_task_prompt_risk", "P105", "Task L5 appears high while student Evidence is L2; prompt-induced risk is present."),
        ("Case_B_raw_score_low_support", "P108", "Raw Evidence is L6, but all readable Evidence in this development slice is prompt-induced."),
        ("Case_C_context_truncated", "P072", "Task is L4 but Evidence is undetermined with truncated context; the model refuses to score it."),
        ("Case_D_low_confidence_context_risk", "P035", "Task is L6 but Evidence is undetermined, low confidence, and context-truncated."),
    ]
    case_rows = []
    for case_type, record_id, interpretation in case_specs:
        row = data.loc[data.record_id.eq(record_id)].iloc[0]
        observable = pd.notna(row.evidence_level)
        if not observable:
            adjusted_interpretation = "NO_EFFECTIVE_EVIDENCE: no adjusted score"
            reason = "student_evidence_bloom is not L1-L6"
        elif row.reliability_weight < 1:
            adjusted_interpretation = f"retained at Evidence L{int(row.evidence_level)} with reduced weight"
            reason = "confidence/prompt/context correction lowers contribution"
        else:
            adjusted_interpretation = f"retained at Evidence L{int(row.evidence_level)}"
            reason = "observable evidence with full effective weight"
        case_rows.append({
            "case_type": case_type,
            "record_id": record_id,
            "raw_interpretation": interpretation,
            "risk_factor": ";".join([x for x, present in [("prompt_induced", row.prompt), ("context_truncated", row.context), ("low_confidence", row.confidence == "low")] if present]) or "none",
            "reliability_weight": float(row.reliability_weight),
            "effective_evidence_contribution": float(row.effective_contribution),
            "adjusted_interpretation": adjusted_interpretation,
            "decision_reason": reason,
            "annotation_source": row.annotation_source,
            "annotation_status": row.annotation_status,
        })
    pd.DataFrame(case_rows).to_csv(OUT / "counterexamples.csv", index=False, encoding="utf-8-sig")

    report = f"""# 研究核心闭环验收（开发版）

本报告只使用 70 条 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 记录，不能替代人工 R1/R2、正式 Gate 或 Formal AIV。

## 当前模型

`w_i = I(observable_i) × c_i × (1 − λ_prompt prompt_i) × (1 − λ_context context_i)`。

`observable_i` 指 Student Evidence 为 L1–L6；NO_EVIDENCE 与 UNDETERMINED 权重为 0。置信度权重为 high=1.0、medium=0.75、low=0.5。权重和为 0 时返回 `NO_EFFECTIVE_EVIDENCE`，不填 0 分。

## 六个结论问题

1. **是否存在 measurement problem？** 是。70 条中只有 {raw['included_evidence_count']} 条可判读 Evidence，{70 - raw['included_evidence_count']} 条为 NO_EVIDENCE/UNDETERMINED；且可判读集合全部 `prompt_induced=true`，说明可观察证据与引导路径完全分离。
2. **校正是否改变分数？** 在当前切片和公共缩放结构下，ABL={raw['ABL']:.4f}、HOT={raw['HOT']:.4f}、Gap={raw['Task_Evidence_Gap']:.4f} 保持不变；支持量从 {raw['effective_weight']:.4f} 降为 {adjusted['effective_weight']:.4f}。
3. **影响最大的风险因素是什么？** 当前可识别的主要风险是 prompt-induced evidence；context 风险在可判读 16 条中没有变异，因此只能作为压力情景，不能从本切片估计其独立影响。
4. **Score 与 Evidence Support 是否不同稳定？** 是。有效参数区间中分数稳定，但 effective coverage 从 {raw['effective_coverage']:.6f} 降至 {adjusted['effective_coverage']:.6f}；支持度比得分更敏感。
5. **模型发现了 Raw Score 无法表达的问题吗？** 是。Raw Score 会把 P108 的 L6 当成可直接解释的高证据，而校正模型同时报告其 prompt 风险和有限支持；P072/P035 则直接拒绝给出分数。
6. **是否支持 Formal AIV？** 否。缺少完成的人工 Gate、可比 AI/non-AI 条件、前后测与独立学习结果；Formal AIV 继续保持 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

## 消融结果

见 `ablation_results.csv`。M0–M3 都使用同一批 70 条记录；消融用于定位风险因素，不用于证明 M3 的预测准确率。

## 反例

见 `counterexamples.csv`。四条记录全部来自原始 development CSV，未人工编造；其中没有 `prompt_induced=false` 且 Evidence 可判读的记录，因此当前数据不能支持“独立 Evidence”案例。

## 冻结状态

Reliability Model、Raw/Adjusted、Sensitivity、Ablation、Counterexamples 和研究结论均已形成可复现产物，可标记为 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`。正式 Gate 与 AIV 扩展仍必须等待人工 R1/R2。
"""
    (OUT / "research_core_closure.md").write_text(report, encoding="utf-8")
    summary = {"status": "RESEARCH_CORE_FROZEN_FOR_SUBMISSION", "formal_gate_eligible": False,
               "outputs": ["raw_adjusted_metrics.csv", "ablation_results.csv", "counterexamples.csv", "research_core_closure.md"],
               "raw": raw, "adjusted": adjusted, "readable_evidence_all_prompt_induced": bool(data.loc[data.evidence_level.notna(), "prompt"].all()),
               "readable_evidence_prompt_false_count": int((~data.loc[data.evidence_level.notna(), "prompt"]).sum())}
    (OUT / "research_core_closure.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
