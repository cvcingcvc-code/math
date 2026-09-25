"""S4 side task: metric computability audit (no Bloom labels used as facts).

Question answered: given the REAL structure of clean_interactions.csv
(session_proxy = one export row, D010), which candidate indicators
(ABL / HOT / CTQ / DHI / MAB) are computable, for how many students,
and with how much data per student?

Everything in section A-C is a structural FACT computed from the data.
Section D is an explicitly labelled SCENARIO: it varies an assumed
NO_EVIDENCE rate r; the LLM-exploratory prelabel rate is shown only as
one reference point and is NOT a human label (D007/D008).

Usage: python src/metric_feasibility.py
Outputs: reports/metric_feasibility.md, work/metric_feasibility.json
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data/processed/clean_interactions.csv"
PRELABEL = ROOT / "data/processed/pilot_ai_prelabel.csv"
OUT_MD = ROOT / "reports/metric_feasibility.md"
OUT_JSON = ROOT / "work/metric_feasibility.json"

GAP_MIN = [5, 30, 120]          # candidate time gaps for "same real session" sensitivity
R_GRID = [0.4, 0.5, 0.6, 0.7, 0.8]  # assumed NO_EVIDENCE/U rate among student turns
MIN_EVID = [3, 5, 10]           # candidate minimum evidence turns for a student-level estimate


def dist(s: pd.Series, bins, labels):
    c = pd.cut(s, bins=bins, labels=labels, right=True).value_counts().reindex(labels).fillna(0)
    return {k: int(v) for k, v in c.items()}


def p_at_least(k: int, m: int, q: float) -> float:
    """P(Binomial(k, q) >= m) — independence assumption, scenario only."""
    from math import comb
    return sum(comb(k, j) * q**j * (1 - q) ** (k - j) for j in range(m, k + 1))


def main() -> None:
    d = pd.read_csv(CLEAN, encoding="utf-8-sig", dtype={"student_id": str})
    d["timestamp"] = pd.to_datetime(d["timestamp"], errors="coerce")
    stu = d[d["speaker_role"] == "student"]
    res: dict = {"input_rows": len(d), "student_turns": len(stu)}

    # ---- A. session_proxy level (FACT) ----
    sess = stu.groupby(["semester", "session_id"]).agg(
        student_id=("student_id", "first"),
        k=("turn_id", "size"),
        agent=("agent_type", "first"),
        ts=("timestamp", "min"),
    ).reset_index()
    A = {}
    for sem, g in sess.groupby("semester"):
        A[sem] = {
            "sessions": int(len(g)),
            "student_turns_per_session_dist": dist(g.k, [0, 1, 2, 4, 9, 10**6], ["1", "2", "3-4", "5-9", ">=10"]),
            "median_student_turns": float(g.k.median()),
            "share_sessions_k>=2 (CTQ upper bound)": round(float((g.k >= 2).mean()), 4),
            "within_session_transitions_upper_bound": int((g.k - 1).clip(lower=0).sum()),
        }
    res["A_session_proxy"] = A

    # ---- B. student level (FACT) ----
    known = sess[~sess.agent.fillna("unknown").isin(["unknown", ""])]
    stud = sess.groupby(["semester", "student_id"]).agg(n_sess=("session_id", "size"), n_turns=("k", "sum")).reset_index()
    mab = known.groupby(["semester", "student_id"]).agent.nunique().rename("m_known")
    stud = stud.merge(mab, on=["semester", "student_id"], how="left").fillna({"m_known": 0})
    B = {}
    for sem, g in stud.groupby("semester"):
        B[sem] = {
            "students": int(len(g)),
            "student_turns_per_student_dist": dist(g.n_turns, [0, 2, 4, 9, 19, 10**6], ["1-2", "3-4", "5-9", "10-19", ">=20"]),
            "median_student_turns": float(g.n_turns.median()),
            "sessions_per_student_dist": dist(g.n_sess, [0, 1, 2, 5, 10**6], ["1", "2", "3-5", ">=6"]),
            "known_agent_count_dist(MAB m_s)": {str(int(k)): int(v) for k, v in g.m_known.value_counts().sort_index().items()},
            "agent_catalog_observed": sorted(known[known.semester == sem].agent.unique().tolist()),
        }
    res["B_student"] = B

    # ---- C. does session_proxy cut real sessions? (FACT, time-gap sensitivity) ----
    C = {}
    s2 = sess.dropna(subset=["ts"]).sort_values(["semester", "student_id", "ts"])
    s2["gap_min"] = s2.groupby(["semester", "student_id"]).ts.diff().dt.total_seconds() / 60
    s2["same_agent"] = s2.agent.eq(s2.groupby(["semester", "student_id"]).agent.shift())
    for sem, g in s2.groupby("semester"):
        gg = g.dropna(subset=["gap_min"])
        C[sem] = {f"consecutive_rows_gap<={m}min_same_agent": int(((gg.gap_min <= m) & gg.same_agent).sum()) for m in GAP_MIN}
        C[sem]["consecutive_row_pairs"] = int(len(gg))
        C[sem]["missing_timestamp_sessions"] = int(sess[(sess.semester == sem)].ts.isna().sum())
    res["C_proxy_boundary"] = C

    # ---- D. SCENARIO: assumed evidence rate -> computability ----
    ref = None
    if PRELABEL.exists():
        p = pd.read_csv(PRELABEL, encoding="utf-8-sig")
        nonlevel = p.student_evidence_bloom.isin(["NO_EVIDENCE", "UNDETERMINED", "NOT_APPLICABLE"]).mean()
        ref = {"llm_exploratory_nonlevel_rate": round(float(nonlevel), 4),
               "note": "LLM_EXPLORATORY_NOT_HUMAN, stratified pilot (not a population estimate)"}
    res["D_reference_rate"] = ref
    D = []
    for r in R_GRID:
        q = 1 - r
        row = {"assumed_nonlevel_rate_r": r}
        for sem in sorted(sess.semester.unique()):
            ks = sess[sess.semester == sem].k
            row[f"{sem}_E[sessions with >=2 evidence turns] (CTQ-definable)"] = round(float(sum(p_at_least(int(k), 2, q) for k in ks)), 1)
            ns = stud[stud.semester == sem].n_turns
            for m in MIN_EVID:
                row[f"{sem}_E[students with >={m} evidence turns]"] = round(float(sum(p_at_least(int(n), m, q) for n in ns)), 1)
        D.append(row)
    res["D_scenario"] = D
    res["D_assumptions"] = ["student turns independently carry level evidence with prob 1-r (no clustering)",
                            "r is not estimated; grid is sensitivity only", "no human labels were used"]

    OUT_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_MD.write_text(render(res), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))


def render(res: dict) -> str:
    L = ["# 指标可计算性审计（S4 旁路任务）", "",
         "> 生成：`python src/metric_feasibility.py`。A–C 节是由 `clean_interactions.csv` 直接统计得到的**结构事实**；"
         "D 节是**情景分析**，没有使用任何人工标签，也不是标注结果。session 指 session_proxy（一个原始导出行，D010）。", ""]
    L += ["## A. session_proxy 内部结构（事实）", "", "| 学期 | sessions | 学生轮/session 分布 | 中位数 | k≥2 占比（CTQ 上界） | 可用跃迁数上界 |", "|---|---:|---|---:|---:|---:|"]
    for sem, a in res["A_session_proxy"].items():
        L.append(f"| {sem} | {a['sessions']} | {a['student_turns_per_session_dist']} | {a['median_student_turns']} | "
                 f"{a['share_sessions_k>=2 (CTQ upper bound)']} | {a['within_session_transitions_upper_bound']} |")
    L += ["", "## B. 学生层（事实）", ""]
    for sem, b in res["B_student"].items():
        L += [f"**{sem}**：学生 {b['students']} 人；学生轮中位数 {b['median_student_turns']}；",
              f"- 每人学生轮分布：{b['student_turns_per_student_dist']}",
              f"- 每人 session 数分布：{b['sessions_per_student_dist']}",
              f"- 已知 agent 去重数（MAB 的 m_s）：{b['known_agent_count_dist(MAB m_s)']}；观测到的 catalog：{b['agent_catalog_observed']}", ""]
    L += ["## C. session_proxy 是否切断了真实会话（事实，时间间隔敏感性）", "",
          "统计同一学生相邻两个 proxy 之间的间隔，且 agent 相同的对数。数量越大，说明“一行＝一个 session”越可能把一次连续学习切成多段。", ""]
    for sem, c in res["C_proxy_boundary"].items():
        L.append(f"- {sem}：{c}")
    L += ["", "## D. 情景：假设非等级比例 r 时的可计算规模（非事实、非标注）", ""]
    if res["D_reference_rate"]:
        L.append(f"参考点（仅作参考）：LLM 探索性预标注中非等级比例 = {res['D_reference_rate']['llm_exploratory_nonlevel_rate']}"
                 f"（{res['D_reference_rate']['note']}）。")
    L += ["假设：" + "；".join(res["D_assumptions"]) + "。", ""]
    keys = list(res["D_scenario"][0].keys())
    L.append("| " + " | ".join(keys) + " |")
    L.append("|" + "---|" * len(keys))
    for row in res["D_scenario"]:
        L.append("| " + " | ".join(str(row[k]) for k in keys) + " |")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
