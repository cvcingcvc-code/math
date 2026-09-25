"""Indicator feasibility audit (label-free).

Question: on the real data structure, can ABL / HOT / CTQ / MAB be computed
at the unit the model defines them (student / session_proxy), and with what
precision?  Uses only data/processed/clean_interactions.csv structure.

Does NOT use any Bloom label, human or AI.  The optional evidence-yield
scenario reads the AI exploratory prelabel ONLY as a clearly marked
assumption (LLM_EXPLORATORY_NOT_HUMAN, D007) and is reported separately.

Outputs: reports/indicator_feasibility_audit.md, .json
"""
import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data/processed/clean_interactions.csv"
PRELABEL = ROOT / "data/processed/pilot_ai_prelabel.csv"
OUT_MD = ROOT / "reports/indicator_feasibility_audit.md"
OUT_JSON = ROOT / "reports/indicator_feasibility_audit.json"

LEVELS = {"L1", "L2", "L3", "L4", "L5", "L6"}
MERGE_WINDOW_MIN = 30  # sensitivity only; not a session definition


def dist(s):
    q = s.quantile([.25, .5, .75, .9]).tolist()
    return {"n": int(s.size), "mean": round(float(s.mean()), 3), "p25": q[0],
            "median": q[1], "p75": q[2], "p90": q[3], "max": int(s.max())}


def share(mask):
    return round(float(mask.mean()), 4)


def audit_semester(d):
    st = d[d.speaker_role == "student"]
    per_sess = st.groupby("session_id").size()
    all_sess = d.groupby("session_id").size()
    per_sess = per_sess.reindex(all_sess.index, fill_value=0)
    trans = (per_sess - 1).clip(lower=0)

    per_stu_turns = st.groupby("student_id").size()
    per_stu_sess = d.groupby("student_id")["session_id"].nunique()
    known = d[d.agent_type.fillna("unknown") != "unknown"]
    m_s = known.groupby("student_id")["agent_type"].nunique().reindex(
        per_stu_sess.index, fill_value=0)
    stu_ctq_sessions = per_sess[per_sess >= 2].rename("x").to_frame().join(
        d.drop_duplicates("session_id").set_index("session_id")["student_id"]
    ).groupby("student_id").size().reindex(per_stu_sess.index, fill_value=0)

    # session-merge sensitivity: consecutive rows of same student within window
    rows = d.drop_duplicates("session_id")[["student_id", "session_id", "timestamp", "agent_type"]].copy()
    rows["ts"] = pd.to_datetime(rows["timestamp"], errors="coerce")
    rows = rows.sort_values(["student_id", "ts"])
    gap = rows.groupby("student_id")["ts"].diff().dt.total_seconds() / 60
    same_agent = rows.groupby("student_id")["agent_type"].shift() == rows["agent_type"]
    has_prev = gap.notna()

    return {
        "students": int(per_stu_sess.size),
        "session_proxies": int(all_sess.size),
        "student_turns": int(st.shape[0]),
        "student_turns_per_session": dist(per_sess),
        "sessions_with_ge2_student_turns": share(per_sess >= 2),
        "sessions_with_ge3_student_turns": share(per_sess >= 3),
        "transitions_total": int(trans.sum()),
        "student_turns_per_student": dist(per_stu_turns),
        "sessions_per_student": dist(per_stu_sess),
        "students_with_ge1_ctq_session": share(stu_ctq_sessions >= 1),
        "students_with_ge_turns": {k: share(per_stu_turns.reindex(per_stu_sess.index, fill_value=0) >= k)
                                   for k in (3, 5, 10, 20)},
        "mab_distinct_known_agents_per_student": {str(k): int(v) for k, v in m_s.value_counts().sort_index().items()},
        "students_with_ge2_known_agents": share(m_s >= 2),
        "agent_catalog_observed": sorted(known.agent_type.unique().tolist()),
        "unknown_agent_turn_share": share(d.agent_type.fillna("unknown") == "unknown"),
        "merge_sensitivity": {
            "consecutive_row_pairs": int(has_prev.sum()),
            f"share_gap_le_{MERGE_WINDOW_MIN}min": round(float((gap[has_prev] <= MERGE_WINDOW_MIN).mean()), 4),
            f"share_gap_le_{MERGE_WINDOW_MIN}min_same_agent": round(float(((gap <= MERGE_WINDOW_MIN) & same_agent)[has_prev].mean()), 4),
        },
        "_per_stu_turns": per_stu_turns,
    }


def evidence_yield_scenario():
    """ASSUMPTION ONLY: evidence-bearing share from AI exploratory prelabel."""
    p = pd.read_csv(PRELABEL, encoding="utf-8-sig")
    assert set(p.annotator_type) == {"LLM_EXPLORATORY_NOT_HUMAN"}
    out = {}
    for sem, g in p.groupby("semester"):
        k = int(g.student_evidence_bloom.isin(LEVELS).sum())
        n = int(len(g))
        # Wilson 95% interval for the yield proportion
        z, ph = 1.96, k / n
        c = (ph + z * z / (2 * n)) / (1 + z * z / n)
        h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        out[sem] = {"n": n, "levelled": k, "yield": round(ph, 4),
                    "wilson95": [round(c - h, 4), round(c + h, 4)]}
    return out


def main():
    d = pd.read_csv(CLEAN, encoding="utf-8-sig", dtype={"student_id": str})
    res, scen = {}, evidence_yield_scenario()
    for sem, g in d.groupby("semester"):
        r = audit_semester(g)
        turns = r.pop("_per_stu_turns")
        y = scen[sem]["yield"]
        exp_ev = turns * y
        # worst-case (p=.5) binomial SE of a per-student HOT proportion
        r["scenario_expected_evidence_turns_per_student"] = {
            "yield_assumed": y,
            "median": round(float(exp_ev.median()), 2),
            "share_students_ge5": share(exp_ev >= 5),
            "share_students_ge10": share(exp_ev >= 10),
            "hot_worst_case_se_at_median": round(0.5 / math.sqrt(max(exp_ev.median(), 1)), 3),
        }
        res[sem] = r

    payload = {"source": str(CLEAN.relative_to(ROOT)), "labels_used": "none (structure only)",
               "scenario_source": "pilot_ai_prelabel.csv (LLM_EXPLORATORY_NOT_HUMAN; assumption, not evidence)",
               "evidence_yield_ai_prelabel": scen, "by_semester": res}
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    L = ["# 指标可计算性审计（无标签，结构层面）", "",
         "输入：`data/processed/clean_interactions.csv`（7028 turns）。**未使用任何 Bloom 标签。**",
         "第 4 节情景使用 AI 探索性预标注的“有等级证据比例”，仅作假设，不是人工结果（D007）。",
         "复现：`python src/indicator_feasibility_audit.py`", ""]
    L += ["## 1. 分析单位的规模", "",
          "| 指标 | " + " | ".join(res) + " |", "|---|" + "---:|" * len(res)]
    rows = [("学生数", "students"), ("session_proxy 数", "session_proxies"), ("学生轮数", "student_turns"),
            ("转移总数（CTQ 可用 Δ 数，未扣无证据轮）", "transitions_total")]
    for lab, k in rows:
        L.append(f"| {lab} | " + " | ".join(str(res[s][k]) for s in res) + " |")
    L += ["", "## 2. CTQ（会话内相邻学生证据跃迁）", "",
          "| 指标 | " + " | ".join(res) + " |", "|---|" + "---:|" * len(res)]
    for lab, f in [("每 session 学生轮 中位数", lambda r: r["student_turns_per_session"]["median"]),
                   ("每 session 学生轮 p90", lambda r: r["student_turns_per_session"]["p90"]),
                   ("≥2 学生轮的 session 占比", lambda r: r["sessions_with_ge2_student_turns"]),
                   ("≥3 学生轮的 session 占比", lambda r: r["sessions_with_ge3_student_turns"]),
                   ("至少 1 个可算 CTQ session 的学生占比", lambda r: r["students_with_ge1_ctq_session"])]:
        L.append(f"| {lab} | " + " | ".join(str(f(res[s])) for s in res) + " |")
    L += ["", "注意：上表只是**上限**。CTQ 需要相邻两轮都有 L1–L6 学生证据；NO_EVIDENCE/U 轮会进一步打断序列。", "",
          "## 3. ABL / HOT（学生级比例）与 MAB", "",
          "| 指标 | " + " | ".join(res) + " |", "|---|" + "---:|" * len(res)]
    for lab, f in [("每生学生轮 中位数", lambda r: r["student_turns_per_student"]["median"]),
                   ("每生学生轮 p25", lambda r: r["student_turns_per_student"]["p25"]),
                   ("学生轮 ≥5 的学生占比", lambda r: r["students_with_ge_turns"][5]),
                   ("学生轮 ≥10 的学生占比", lambda r: r["students_with_ge_turns"][10]),
                   ("每生 session 中位数", lambda r: r["sessions_per_student"]["median"]),
                   ("已知 agent ≥2 的学生占比（MAB>1/K）", lambda r: r["students_with_ge2_known_agents"]),
                   ("unknown agent turn 占比", lambda r: r["unknown_agent_turn_share"])]:
        L.append(f"| {lab} | " + " | ".join(str(f(res[s])) for s in res) + " |")
    for s in res:
        L.append(f"\n{s} 已知 agent 目录：{', '.join(res[s]['agent_catalog_observed'])}；每生去重已知 agent 数分布：{res[s]['mab_distinct_known_agents_per_student']}")
    L += ["", "## 4. 情景（假设）：若有等级证据比例 ≈ AI 预标注值", "",
          "| 学期 | 预标注有等级比例 | Wilson 95% | 每生期望证据轮中位数 | ≥5 证据轮学生占比 | ≥10 占比 | 中位学生 HOT 最坏 SE |",
          "|---|---:|---|---:|---:|---:|---:|"]
    for s in res:
        e, sc = scen[s], res[s]["scenario_expected_evidence_turns_per_student"]
        L.append(f"| {s} | {e['yield']} ({e['levelled']}/{e['n']}) | {e['wilson95']} | {sc['median']} | {sc['share_students_ge5']} | {sc['share_students_ge10']} | {sc['hot_worst_case_se_at_median']} |")
    L += ["", "该比例来自 AI 探索性预标注且 Pilot 为定向抽样，**不能代表总体**；这里只用来展示量级。", "",
          "## 5. session_proxy 合并敏感性（B003）", ""]
    for s in res:
        m = res[s]["merge_sensitivity"]
        L.append(f"- {s}：同一学生相邻导出行 {m['consecutive_row_pairs']} 对；间隔 ≤{MERGE_WINDOW_MIN} 分钟占 {m[f'share_gap_le_{MERGE_WINDOW_MIN}min']}，其中同 agent 占 {m[f'share_gap_le_{MERGE_WINDOW_MIN}min_same_agent']}。")
    L += ["", "30 分钟窗口仅为敏感性参数，不是 session 定义；合并与否须作为预注册的稳健性分支。"]
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(OUT_MD.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
