"""S4-Pilot Annotation Gate: generate the Gate Report from returned worksheets.

Consumes the blinded worksheets produced by src/build_annotation_worksheets.py and
answers the eight Gate questions in handoff/NEXT_TASK.md.

Integrity rules enforced here:
  * No labels are invented. Missing cells stay missing and are reported.
  * Reliability is never computed across the two AI passes. Only returned human
    worksheets are read (D007/D008).
  * Thresholds come from validation/gate_thresholds.json. While preregistered is
    false the Gate is reported as NOT AUTO-DECIDABLE; thresholds are never
    adjusted to fit the observed values.

Usage:
  python src/annotation_gate_report.py --a <wsA.csv> --b <wsB.csv>
  python src/annotation_gate_report.py --selftest     # synthetic software test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from csv_safe_read import read_worksheet
from reliability import (agreement_rate, bootstrap_ci, cohen_kappa,
                         krippendorff_alpha, weighted_kappa)

ROOT = Path(__file__).resolve().parents[1]
KEY = ROOT / "data" / "annotations" / "_keys" / "pilot_worksheet_key.csv"
THRESH = ROOT / "validation" / "gate_thresholds.json"
NO_PRIOR = "[NO_PRIOR_AI_TURN_IN_SOURCE_EXPORT]"

LEVELS = ["L1", "L2", "L3", "L4", "L5", "L6"]
TIERS = ["Low", "Mid", "High"]
FOLD = {"L1": "Low", "L2": "Low", "L3": "Mid", "L4": "Mid", "L5": "High", "L6": "High"}
TASK_STATES = ["NOT_APPLICABLE", "UNDETERMINED"]
EVID_STATES = ["NO_EVIDENCE", "NOT_APPLICABLE", "UNDETERMINED"]

ALLOWED = {
    "speaker_role_check": {"student", "ai", "system", "unknown"},
    "task_bloom": set(LEVELS) | set(TASK_STATES),
    "student_evidence_bloom": set(LEVELS) | set(EVID_STATES),
    "task_confidence": {"high", "medium", "low"},
    "evidence_confidence": {"high", "medium", "low"},
    "confidence": {"high", "medium", "low"},
    "task_source": {"student_request", "ai_prompt", "embedded_question", "system", "mixed", "unknown"},
    "task_actor": {"student", "ai", "both", "unknown"},
    "content_relation": {"independent", "reworked_with_addition", "copied_verbatim",
                         "reworked_without_addition", "not_comparable"},
    "partial_rewrite": {"true", "false"},
    "prompt_induced": {"true", "false"},
    "scaffold_share": {"high", "medium", "low", "none"},
    "correctness": {"correct", "incorrect", "partially_correct", "not_assessable"},
    "needs_second_review": {"true", "false"},
}
AMBIGUITY_CODES = {"role_boundary", "source_attribution", "context_missing", "task_unspecified",
                   "level_boundary", "multi_operation", "prompt_induced", "copy_suspected",
                   "duplicate", "link_only", "correctness_uncertain", "other", "none"}
REQUIRED_ALWAYS = ["speaker_role_check", "task_bloom", "task_confidence",
                   "student_evidence_bloom", "evidence_confidence",
                   "confidence", "reason", "ambiguity_type", "needs_second_review"]


def norm(v) -> str:
    return str(v).strip()


def load(path: Path) -> pd.DataFrame:
    df = read_worksheet(path)
    for c in df.columns:
        df[c] = df[c].map(norm)
    # Never allow provisional AI annotations into the formal human Gate path.
    if {"annotation_source", "annotation_status"}.issubset(df.columns):
        if set(df["annotation_source"]) == {"AI_PROVISIONAL"} or set(df["annotation_status"]) == {"DEVELOPMENT_ONLY"}:
            raise ValueError(
                "AI_PROVISIONAL / DEVELOPMENT_ONLY data cannot be used as formal Gate input"
            )
    return df


def completeness(df: pd.DataFrame, coder: str) -> dict:
    c = {"coder": coder, "n_rows": int(len(df)), "missing_required": {}, "invalid_values": {},
         "conditional_gaps": {}}
    for col in REQUIRED_ALWAYS:
        miss = int((df[col] == "").sum()) if col in df.columns else len(df)
        if miss:
            c["missing_required"][col] = miss
    for col, allowed in ALLOWED.items():
        if col not in df.columns:
            continue
        bad = df[col][(df[col] != "") & (~df[col].str.lower().isin(allowed))]
        if len(bad):
            c["invalid_values"][col] = {k: int(v) for k, v in bad.value_counts().items()}
    # conditional requirements from clarification V0.1.1
    cond = {
        "task_source": df["task_bloom"].str.upper().isin(LEVELS),
        "task_actor": df["task_bloom"].str.upper().isin(LEVELS),
        "evidence_span": df["student_evidence_bloom"].str.upper().isin(LEVELS),
        "content_relation": df["student_evidence_bloom"].str.upper().isin(LEVELS),
        "correctness": df["student_evidence_bloom"].str.upper().isin(LEVELS),
        "prompt_induced": df["student_evidence_bloom"].str.upper().isin(LEVELS),
        "speaker_role_check": pd.Series(True, index=df.index),
    }
    for col, mask in cond.items():
        if col in df.columns:
            gap = int((mask & (df[col] == "")).sum())
            if gap:
                c["conditional_gaps"][col] = gap
    bad_amb = df["ambiguity_type"][(df["ambiguity_type"] != "") &
                                  (~df["ambiguity_type"].str.lower().str.split(";")
                                   .explode().str.strip().isin(AMBIGUITY_CODES))]
    if len(bad_amb):
        c["invalid_values"]["ambiguity_type"] = {k: int(v) for k, v in bad_amb.value_counts().items()}
    valid = 1.0
    if len(df):
        ok_rows = 0
        for _, r in df.iterrows():
            if any(r[c] == "" for c in REQUIRED_ALWAYS if c in df.columns):
                continue
            if any(r[c] != "" and r[c].lower() not in ALLOWED[c] for c in ALLOWED if c in df.columns):
                continue
            ok_rows += 1
        valid = ok_rows / len(df)
    c["valid_row_rate"] = round(valid, 4)
    return c


def axis_stats(a: pd.Series, b: pd.Series, label: str, cluster=None) -> dict:
    """Agreement for one axis: nominal over all values, ordinal over L1-L6 only."""
    av, bv = list(a), list(b)
    both = [(x, y) for x, y in zip(av, bv) if x != "" and y != ""]
    out = {"axis": label, "n_pairwise_usable": len(both)}
    if not both:
        return out
    x, y = [p[0] for p in both], [p[1] for p in both]
    out["agreement_rate"] = round(agreement_rate(x, y), 4)
    out["cohen_kappa_nominal"] = round(cohen_kappa(x, y), 4)
    out["krippendorff_alpha_nominal"] = round(
        krippendorff_alpha(list(zip(x, y)), "nominal"), 4)

    numeric = [(u, v) for u, v in zip(x, y) if u in LEVELS and v in LEVELS]
    out["n_both_numeric_L1_L6"] = len(numeric)
    if numeric:
        nx, ny = [p[0] for p in numeric], [p[1] for p in numeric]
        out["ordinal_subset_denominator_share"] = round(len(numeric) / len(both), 4)
        out["weighted_kappa_quadratic"] = round(weighted_kappa(nx, ny, "quadratic", LEVELS), 4)
        out["krippendorff_alpha_ordinal"] = round(
            krippendorff_alpha(list(zip(nx, ny)), "ordinal", LEVELS), 4)
        # interval metric needs numeric positions; L1..L6 -> 1..6
        out["krippendorff_alpha_interval"] = round(
            krippendorff_alpha(list(zip([int(v[1]) for v in nx], [int(v[1]) for v in ny])),
                               "interval", [1, 2, 3, 4, 5, 6]), 4)

    # three-tier fold, non-level states kept as their own categories
    fx = [FOLD.get(v, v) for v in x]
    fy = [FOLD.get(v, v) for v in y]
    out["three_tier_order"] = TIERS + sorted(set(fx) | set(fy) - set(TIERS))
    out["three_tier_agreement_rate"] = round(agreement_rate(fx, fy), 4)
    out["three_tier_cohen_kappa"] = round(cohen_kappa(fx, fy), 4)
    out["three_tier_krippendorff_alpha"] = round(
        krippendorff_alpha(list(zip(fx, fy)), "nominal"), 4)

    numeric_fx = [(u, v) for u, v in zip(fx, fy) if u in TIERS and v in TIERS]
    if numeric_fx:
        tx, ty = [p[0] for p in numeric_fx], [p[1] for p in numeric_fx]
        out["three_tier_weighted_kappa"] = round(weighted_kappa(tx, ty, "quadratic", TIERS), 4)
        out["three_tier_ordinal_alpha"] = round(
            krippendorff_alpha(list(zip(tx, ty)), "ordinal", TIERS), 4)

    lo, hi = bootstrap_ci(x, y, cluster=cluster, level="nominal")
    out["alpha_nominal_ci95"] = [round(lo, 4), round(hi, 4)]
    if numeric:
        lo2, hi2 = bootstrap_ci([p[0] for p in numeric], [p[1] for p in numeric], level="ordinal", order=LEVELS)
        out["alpha_ordinal_subset_ci95"] = [round(lo2, 4), round(hi2, 4)]
    return out


def confusion(x, y, order) -> tuple[dict, list]:
    order = list(order)
    cm = pd.crosstab(pd.Series(x, name="A"), pd.Series(y, name="B"))
    table = {i: {j: int(cm.loc[i, j]) if (i in cm.index and j in cm.columns) else 0
                 for j in order} for i in order}
    pairs = []
    for i in order:
        for j in order:
            if i < j and table[i][j]:
                pairs.append({"pair": f"{i}|{j}", "n": table[i][j]})
    pairs.sort(key=lambda d: -d["n"])
    return table, pairs


def distributions(df: pd.DataFrame, coder: str) -> dict:
    out = {}
    for col in ["task_bloom", "student_evidence_bloom", "task_confidence", "evidence_confidence",
                "confidence", "content_relation", "prompt_induced", "scaffold_share",
                "correctness", "task_source", "task_actor", "needs_second_review",
                "speaker_role_check"]:
        if col in df.columns:
            out[col] = {k: int(v) for k, v in df[col][df[col] != ""].value_counts().items()}
    amb = df["ambiguity_type"][df["ambiguity_type"] != ""].str.lower().str.split(";").explode().str.strip()
    out["ambiguity_type"] = {k: int(v) for k, v in amb.value_counts().items()}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=Path)
    ap.add_argument("--b", type=Path)
    ap.add_argument("--key", type=Path, default=KEY)
    ap.add_argument("--out", type=Path, default=ROOT / "reports" / "annotation_gate_report.md")
    ap.add_argument("--json", type=Path, default=ROOT / "reports" / "annotation_gate_report.json")
    ap.add_argument("--selftest", action="store_true",
                    help="synthetic software test; output is stamped NOT a research result")
    args = ap.parse_args()

    synthetic = args.selftest
    if synthetic:
        rng = np.random.default_rng(11)
        key = load(args.key)
        n = len(key)
        base = rng.choice(LEVELS + ["UNDETERMINED"], size=n, p=[.06, .16, .2, .2, .11, .05, .22])
        def jitter(v):
            if rng.random() < 0.72:
                return v
            pool = LEVELS + ["UNDETERMINED", "NO_EVIDENCE", "NOT_APPLICABLE"]
            return rng.choice(pool)
        A = pd.DataFrame({"record_id": key["record_id"], "task_bloom": base,
                          "student_evidence_bloom": [jitter(v) if v in LEVELS else "NO_EVIDENCE" for v in base]})
        B = pd.DataFrame({"record_id": key["record_id"], "task_bloom": [jitter(v) for v in base],
                          "student_evidence_bloom": [jitter(jitter(v)) if v in LEVELS else "NO_EVIDENCE" for v in base]})
        for d, tag in ((A, "A"), (B, "B")):
            d["speaker_role_check"] = "student"
            d["task_confidence"] = "high"; d["evidence_confidence"] = "high"
            d["confidence"] = "high"; d["reason"] = f"synthetic coder {tag}"
            d["ambiguity_type"] = "none"; d["needs_second_review"] = "false"
            d["task_source"] = "student_request"; d["task_actor"] = "student"
            d["evidence_span"] = "synthetic"; d["content_relation"] = "independent"
            d["correctness"] = "not_assessable"; d["prompt_induced"] = "false"
            d["elapsed_sec"] = "30"
        args.out = ROOT / "work" / "_selftest_gate_report.md"
        args.json = ROOT / "work" / "_selftest_gate_report.json"
    else:
        if not args.a or not args.b:
            ap.error("--a and --b are required unless --selftest")
        A, B = load(args.a), load(args.b)

    key = load(args.key)
    thresholds = json.loads(THRESH.read_text(encoding="utf-8"))
    thr = thresholds["thresholds"]
    prereg = bool(thresholds.get("preregistered"))

    m = A.merge(B, on="record_id", suffixes=("_A", "_B"))
    m = m.merge(key[["record_id", "agent_type", "path_case", "semester", "student_id",
                     "review_sample_type", "task_bloom_ai"]], on="record_id", how="left")

    comp = [completeness(A, "A"), completeness(B, "B")]
    cluster = m["student_id"].tolist() if "student_id" in m.columns else None

    stats = {}
    for axis in ["task_bloom", "student_evidence_bloom"]:
        stats[axis] = axis_stats(m[f"{axis}_A"], m[f"{axis}_B"], axis, cluster=cluster)

    xA = [FOLD.get(v, v) for v in m["task_bloom_A"]]
    xB = [FOLD.get(v, v) for v in m["task_bloom_B"]]
    yA = [FOLD.get(v, v) for v in m["student_evidence_bloom_A"]]
    yB = [FOLD.get(v, v) for v in m["student_evidence_bloom_B"]]
    both_ok = [(i, a1, a2) for i, (a1, b1, a2, b2) in
               enumerate(zip(xA, xB, yA, yB)) if a1 == b1 and a2 == b2 and a1 != "" and a2 != ""]
    diverge = sum(1 for _, t, e in both_ok if t != e)
    gap = {"n_records_both_coders_agree": len(both_ok),
           "n_task_tier_ne_evidence_tier": diverge,
           "divergence_rate": round(diverge / len(both_ok), 4) if both_ok else None}

    numeric_both = m[(m["task_bloom_A"].isin(LEVELS)) & (m["task_bloom_B"].isin(LEVELS)) &
                     (m["student_evidence_bloom_A"].isin(LEVELS)) &
                     (m["student_evidence_bloom_B"].isin(LEVELS))].copy()
    if len(numeric_both):
        numeric_both["gap_A"] = numeric_both["task_bloom_A"].str[1].astype(int) - \
                                numeric_both["student_evidence_bloom_A"].str[1].astype(int)
        numeric_both["gap_B"] = numeric_both["task_bloom_B"].str[1].astype(int) - \
                                numeric_both["student_evidence_bloom_B"].str[1].astype(int)
        numeric_gap = {"n": int(len(numeric_both)),
                       "mean_gap_A": round(float(numeric_both["gap_A"].mean()), 3),
                       "mean_gap_B": round(float(numeric_both["gap_B"].mean()), 3)}
    else:
        numeric_gap = {"n": 0}

    task_cm, task_pairs = confusion(list(m["task_bloom_A"]), list(m["task_bloom_B"]),
                                    LEVELS + TASK_STATES)
    ev_cm, ev_pairs = confusion(list(m["student_evidence_bloom_A"]),
                                list(m["student_evidence_bloom_B"]), LEVELS + EVID_STATES)

    per_agent = {}
    if "agent_type" in m.columns:
        for agent, grp in m.groupby("agent_type"):
            ga = grp[(grp["task_bloom_A"].isin(LEVELS)) & (grp["student_evidence_bloom_A"].isin(LEVELS))]
            gb = grp[(grp["task_bloom_B"].isin(LEVELS)) & (grp["student_evidence_bloom_B"].isin(LEVELS))]
            per_agent[agent] = {
                "n_records": int(len(grp)),
                "n_both_numeric_A": int(len(ga)), "n_both_numeric_B": int(len(gb)),
                "mean_task_minus_evidence_A": round(float(ga["task_bloom_A"].str[1].astype(int).mean()
                                                          - ga["student_evidence_bloom_A"].str[1].astype(int).mean()), 3) if len(ga) else None,
                "mean_task_minus_evidence_B": round(float(gb["task_bloom_B"].str[1].astype(int).mean()
                                                          - gb["student_evidence_bloom_B"].str[1].astype(int).mean()), 3) if len(gb) else None,
                "no_evidence_A": int((grp["student_evidence_bloom_A"] == "NO_EVIDENCE").sum()),
            }

    sec = pd.to_numeric(m.get("elapsed_sec_A", pd.Series(dtype=str)), errors="coerce")
    sec = sec.dropna()
    cost = {"reported_rows": int(len(sec)),
            "median_sec_per_record": round(float(sec.median()), 1) if len(sec) else None,
            "total_minutes_A": round(float(sec.sum()) / 60, 1) if len(sec) else None}
    need2 = int((m["needs_second_review_A"].str.lower() == "true").sum())
    workload = {"needs_second_review_A": need2,
                "rate": round(need2 / len(m), 4) if len(m) else None,
                "medium_or_low_confidence_A": int(m["confidence_A"].str.lower().isin(["medium", "low"]).sum())}

    r6 = stats["task_bloom"].get("krippendorff_alpha_nominal")
    r3 = stats["task_bloom"].get("three_tier_krippendorff_alpha")
    e6 = stats["student_evidence_bloom"].get("krippendorff_alpha_nominal")
    e3 = stats["student_evidence_bloom"].get("three_tier_krippendorff_alpha")

    def verdict(ok):
        if not prereg:
            return "NOT AUTO-DECIDABLE (阈值未预注册)"
        return "PASS" if ok else "FAIL"

    answers = [
        ("Q1 六级标注是否可执行？",
         f"valid_row_rate A={comp[0]['valid_row_rate']} B={comp[1]['valid_row_rate']}; "
         f"Task alpha={r6} Evidence alpha={e6}; "
         f"UNDETERMINED Task={_rate(m['task_bloom_A'], 'UNDETERMINED'):.3f} "
         f"Evidence={_rate(m['student_evidence_bloom_A'], 'UNDETERMINED'):.3f}",
         verdict(comp[0]["valid_row_rate"] >= thr["completeness_valid_value_min"]
                 and comp[1]["valid_row_rate"] >= thr["completeness_valid_value_min"]
                 and _rate(m["task_bloom_A"], "UNDETERMINED") <= thr["undetermined_rate_max_per_axis"])),
        ("Q2 三阶是否明显更稳？",
         f"Task 六级={r6} -> 三阶={r3}; Evidence 六级={e6} -> 三阶={e3}",
         verdict((r3 or -9) >= (r6 or 9) and (e3 or -9) >= (e6 or 9))),
        ("Q3 Task/Evidence 双轴是否有实际信息价值？",
         f"两标注者均一致的记录 {gap['n_records_both_coders_agree']} 条，其中 Task 阶 ≠ Evidence 阶 "
         f"{gap['n_task_tier_ne_evidence_tier']} 条（{gap['divergence_rate']}）",
         verdict((gap["divergence_rate"] or 0) > 0)),
        ("Q4 哪些类别最常混淆？",
         f"Task: {task_pairs[:4]}; Evidence: {ev_pairs[:4]}",
         "需负责人判定"),
        ("Q5 UNDETERMINED / NO_EVIDENCE 比例？",
         f"Task U={_rate(m['task_bloom_A'], 'UNDETERMINED'):.3f} "
         f"NA={_rate(m['task_bloom_A'], 'NOT_APPLICABLE'):.3f}; "
         f"Evidence U={_rate(m['student_evidence_bloom_A'], 'UNDETERMINED'):.3f} "
         f"NO_EVIDENCE={_rate(m['student_evidence_bloom_A'], 'NO_EVIDENCE'):.3f}",
         "需负责人判定"),
        ("Q6 人工成本是否可接受？",
         f"中位 {cost['median_sec_per_record']} 秒/条；A 合计 {cost['total_minutes_A']} 分钟；"
         f"需二审 {workload['needs_second_review_A']} 条（{workload['rate']}）",
         verdict(cost["median_sec_per_record"] is not None
                 and cost["median_sec_per_record"] <= thr["median_sec_per_record_max"])),
        ("Q7 智能体路径偏差是否出现初步证据？",
         "见 per-agent 描述性表（不得作因果解释）",
         "需负责人判定"),
        ("Q8 是否允许进入模块 A 全量实验？",
         "需 Q1–Q7 全部可判定并通过，且由负责人签署",
         "需负责人判定"),
    ]

    lines = []
    if synthetic:
        lines += ["> **警告：合成软件测试。** 本文件由 `--selftest` 生成的随机标签产生，",
                  "> **不是人工标注结果，不是研究结果，不得引用。**", ""]
    lines += [
        "# S4-Pilot Annotation Gate Report",
        "",
        f"- 输入 A：`{args.a}`",
        f"- 输入 B：`{args.b}`",
        f"- 阈值文件：`validation/gate_thresholds.json`（preregistered={prereg})",
        f"- 记录数（A∩B）：{len(m)}",
        "- D008 合规：本报告只读取人工工作表，不跨 AI 预标注计算一致性。",
        "",
        "## 1. 完整性",
        "",
    ]
    lines.append("```json")
    lines.append(json.dumps(comp, ensure_ascii=False, indent=2))
    lines.append("```")
    lines += ["", "## 2. 各轴一致性", "", "```json",
              json.dumps(stats, ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 3. Task × Evidence 信息价值", "", "```json",
              json.dumps({"tier_gap": gap, "numeric_gap": numeric_gap}, ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 4. 混淆矩阵（A 行 × B 列）", "", "**Task Bloom**", "```json",
              json.dumps(task_cm, ensure_ascii=False, indent=2), "```",
              "", "**Student Evidence Bloom**", "```json",
              json.dumps(ev_cm, ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 5. 分智能体描述性 gap（不构成因果证据）", "", "```json",
              json.dumps(per_agent, ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 6. 成本与复核工作量", "", "```json",
              json.dumps({"cost": cost, "workload": workload}, ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 7. 标注者分布", "", "```json",
              json.dumps({"A": distributions(A, "A"), "B": distributions(B, "B")},
                         ensure_ascii=False, indent=2), "```"]
    lines += ["", "## 8. Gate 问题回答", "", "| 问题 | 观察 | 判定 |", "|---|---|---|"]
    for q, obs, v in answers:
        lines.append(f"| {q} | {obs} | {v} |")
    lines += ["", "## 9. 阈值与结论边界", "",
              f"- preregistered = **{prereg}**。" + ("" if prereg else
              " 在负责人确认阈值前，本报告不给出 Gate 通过判定。"),
              "- 阈值不得在查看上述数值后回改。",
              "- 组间差异为描述性；Pilot 为分层/定向样本，不得解释为路径效应或 AI 因果增量。",
              "- 本报告不产生 AIV、CTQ、DHI 或任何学生级排名。"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    payload = {"synthetic_software_test": synthetic, "n": len(m), "preregistered": prereg,
               "completeness": comp, "axis_stats": stats, "tier_gap": gap,
               "numeric_gap": numeric_gap, "task_confusion": task_cm,
               "evidence_confusion": ev_cm, "per_agent": per_agent,
               "cost": cost, "workload": workload,
               "gate_answers": [{"q": q, "observation": o, "verdict": v} for q, o, v in answers]}
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"wrote {args.json}")
    for q, o, v in answers:
        print(f"  {q} -> {v}")
    return 0


def _rate(series: pd.Series, value: str) -> float:
    s = series[series != ""]
    return float((s == value).sum()) / len(s) if len(s) else float("nan")


if __name__ == "__main__":
    raise SystemExit(main())