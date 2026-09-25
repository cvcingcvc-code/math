"""S4-Pilot Gate: canonical data integrity verification (read-only).

Checks the canonical Pilot V1 against frozen decisions in handoff/DECISIONS.md,
and registers data defects that would invalidate a human annotation round.

Emits no labels and modifies no source data.

Usage:  python src/verify_pilot_integrity.py
Exit :  0 = all invariant checks pass, 1 = at least one invariant violated
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

PILOT_N, QUEUE_N, HARD_N, RANDOM_N = 140, 70, 50, 20
MANUAL = ROOT / "docs" / "annotation" / "annotation_manual_v0.1.md"
TEMPLATE = ROOT / "docs" / "annotation" / "pilot_annotation_template.csv"
SHA_MANUAL = "F8E42B177E5DFF335F7C42C58B2B4A1C80666E3C5CE89226305AE5904C64F119"
SHA_TEMPLATE = "2E4C9FBD8D2273211F9B2D8194F0716B79470F50B685CD07D45E18A5231F021B"
NO_PRIOR = "[NO_PRIOR_AI_TURN_IN_SOURCE_EXPORT]"

checks: list[tuple[str, bool, str]] = []
findings: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, bool(ok), detail))


def finding(fid: str, severity: str, title: str, detail: str, evidence: dict) -> None:
    findings.append({"id": fid, "severity": severity, "title": title,
                     "detail": detail, "evidence": evidence})


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def norm(s) -> str:
    return " ".join(str(s).split())


def main() -> int:
    pilot = pd.read_csv(PROC / "pilot_sample.csv", dtype=str, keep_default_na=False)
    pre = pd.read_csv(PROC / "pilot_ai_prelabel.csv", dtype=str, keep_default_na=False)
    queue = pd.read_csv(PROC / "pilot_human_review_queue.csv", dtype=str, keep_default_na=False)
    ci = pd.read_csv(PROC / "clean_interactions.csv", dtype=str, keep_default_na=False)

    # ---------- frozen invariants ----------
    check("D005 Pilot N == 140", len(pilot) == PILOT_N, f"actual={len(pilot)}")
    pid = list(pilot["pilot_id"])
    want = [f"P{i:03d}" for i in range(1, PILOT_N + 1)]
    check("pilot_id unique", len(set(pid)) == len(pid), f"n_unique={len(set(pid))}")
    check("pilot_id == P001..P140", set(pid) == set(want),
          f"missing={sorted(set(want) - set(pid))[:5]} foreign={sorted(set(pid) - set(want))[:5]}")
    check("D006 no legacy pilot id scheme", not [i for i in pid if "-" in i or i.upper().startswith("OLD")])

    # analysis unit: one record == one student turn
    n_student = int(pilot["speaker_role"].eq("student").sum())
    check("all pilot records are student turns (unit = student turn)",
          n_student == PILOT_N, f"student={n_student}/{PILOT_N}")

    check("prelabel N == Pilot N", len(pre) == PILOT_N, f"actual={len(pre)}")
    check("prelabel record_id set == pilot_id set", set(pre["record_id"]) == set(pid),
          f"foreign={sorted(set(pre['record_id']) - set(pid))[:5]}")
    check("D007 prelabel annotator_type == LLM_EXPLORATORY_NOT_HUMAN",
          set(pre["annotator_type"]) == {"LLM_EXPLORATORY_NOT_HUMAN"},
          f"actual={sorted(set(pre['annotator_type']))}")

    check("queue N == 70", len(queue) == QUEUE_N, f"actual={len(queue)}")
    check("queue record_id subset of Pilot", set(queue["record_id"]).issubset(set(pid)),
          f"foreign={sorted(set(queue['record_id']) - set(pid))[:5]}")
    check("queue record_id unique", queue["record_id"].is_unique,
          f"n_unique={queue['record_id'].nunique()}")
    vc = queue["review_sample_type"].value_counts().to_dict()
    check("queue = 50 hard + 20 random audit",
          vc.get("HARD_CASE", 0) == HARD_N and vc.get("RANDOM_NORMAL_AUDIT", 0) == RANDOM_N, f"actual={vc}")
    check("queue manual_version == V0.1", set(queue["manual_version"]) == {"V0.1"},
          f"actual={sorted(set(queue['manual_version']))}")

    check("manual V0.1 sha256 matches CHANGELOG",
          sha256(MANUAL).upper() == SHA_MANUAL, f"actual={sha256(MANUAL).upper()}")
    check("template sha256 matches CHANGELOG",
          sha256(TEMPLATE).upper() == SHA_TEMPLATE, f"actual={sha256(TEMPLATE).upper()}")

    agent_vc = pilot["agent_type"].value_counts(dropna=False).to_dict()
    check("D011 unknown agent retained in pilot",
          (agent_vc.get("unknown", 0) + agent_vc.get("", 0)) > 0, f"unknown_n={agent_vc.get('unknown', 0)}")

    # ---------- independent reconstruction of prior AI context ----------
    ci = ci.sort_values(["source_row_id", "turn_index_in_session"]).reset_index(drop=True)
    by_turn = {r["turn_id"]: i for i, r in ci.iterrows()}
    recon = {}
    for _, p in pilot.iterrows():
        i = by_turn.get(p["turn_id"])
        if i is None:
            recon[p["pilot_id"]] = None
            continue
        before = ci.iloc[:i]
        before = before[before["source_row_id"] == p["source_row_id"]]
        txt = [norm(t) for t in before.loc[before["speaker_role"] == "ai", "ai_text"] if norm(t)]
        recon[p["pilot_id"]] = norm(" ".join(txt))
    check("all pilot turns located in clean_interactions",
          all(v is not None for v in recon.values()),
          f"missing={[k for k, v in recon.items() if v is None][:5]}")

    recon_df = pd.DataFrame({"record_id": list(recon), "recon": list(recon.values())})

    def prior_consistency(df: pd.DataFrame, label: str) -> None:
        m = df.merge(recon_df, on="record_id", how="left")
        claimed_empty = m["prior_ai_context"].map(norm) == NO_PRIOR
        truly_empty = m["recon"].map(norm).eq("")
        agree = int((claimed_empty == truly_empty).sum())
        check(f"{label}: prior_ai_context empty/non-empty agrees with reconstruction",
              agree == len(m), f"{agree}/{len(m)}")
        ne = m[~claimed_empty]
        ok = ne.apply(lambda r: norm(r["prior_ai_context"])[:200] in norm(r["recon"])
                      or norm(r["recon"])[:200] in norm(r["prior_ai_context"]), axis=1)
        check(f"{label}: non-empty prior_ai_context matches reconstruction",
              int(ok.sum()) == len(ne), f"{int(ok.sum())}/{len(ne)}")

    prior_consistency(pre, "prelabel")
    prior_consistency(queue, "queue")

    # ---------- defect register ----------
    # F01: ai_context_text is not prior context; it is the AI reply that FOLLOWS
    # the student turn => future-content leakage if used for annotation.
    ctx_rows = []
    for _, p in pilot.iterrows():
        i = by_turn[p["turn_id"]]
        act = norm(p["ai_context_text"])
        before = ci.iloc[:i]
        before = before[before["source_row_id"] == p["source_row_id"]]
        prior = [norm(t) for t in before.loc[before["speaker_role"] == "ai", "ai_text"] if norm(t)]
        after = ci.iloc[i + 1:]
        after = after[after["source_row_id"] == p["source_row_id"]]
        fut = [norm(t) for t in after.loc[after["speaker_role"] == "ai", "ai_text"] if norm(t)]
        ctx_rows.append({
            "pilot_id": p["pilot_id"],
            "no_prior_ai_turn": len(prior) == 0,
            "nonempty": act != "",
            "matches_future": any(act == x for x in fut),
            "prefix_of_future": any(x.startswith(act[:120]) for x in fut) if act else False,
        })
    c = pd.DataFrame(ctx_rows)
    n_impossible = int((c["no_prior_ai_turn"] & c["nonempty"]).sum())
    if n_impossible:
        finding(
            "S4-F01", "HIGH",
            "pilot_sample.csv::ai_context_text carries FUTURE AI content (leakage)",
            "ai_context_text is non-empty for rows that have no preceding AI turn in the "
            "source export, and matches/prefixes the AI turn that FOLLOWS the student turn. "
            "It is therefore the AI reply to the same turn, not prior context. Using it as "
            "annotation context leaks the AI answer into Task/Evidence judgement.",
            {"rows_impossible_as_prior": n_impossible,
             "rows_exact_match_future": int(c["matches_future"].sum()),
             "rows_prefix_of_future": int(c["prefix_of_future"].sum()),
             "examples": c.loc[c["no_prior_ai_turn"] & c["nonempty"], "pilot_id"].tolist()[:5]},
        )

    # F02: the human review queue is not blind
    prelabel_cols = ["task_bloom", "student_evidence_bloom", "confidence", "reason",
                     "content_source_attribution"]
    leaked = [col for col in prelabel_cols if col in queue.columns
              and int((queue[col].astype(str).str.len() > 0).sum()) > 0]
    if leaked:
        finding(
            "S4-F02", "HIGH",
            "pilot_human_review_queue.csv is not a blind annotation form",
            "The queue already contains AI prelabels in the columns a human must fill, plus "
            "agent/path identifiers. Manual V0.1 section 7.3 requires round 1 to be blind to "
            "automatic labels and to mask path/brand names. Handing this file to annotators "
            "would anchor them. A separate blinded worksheet is required.",
            {"leaked_columns": leaked,
             "annotator_id": sorted(set(queue["annotator_id"]))[:3],
             "agent_type_present": "agent_type" in queue.columns,
             "path_case_present": "path_case" in queue.columns},
        )

    # ---------- report ----------
    w = max(len(n) for n, _, _ in checks)
    failed = 0
    print("=" * 78)
    print("S4-PILOT GATE :: CANONICAL DATA INTEGRITY")
    print("=" * 78)
    for name, ok, detail in checks:
        if not ok:
            failed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {name.ljust(w)}  {detail}".rstrip())
    print()
    print(f"INVARIANT CHECKS: {len(checks) - failed}/{len(checks)} passed")
    print()
    print(f"DEFECT REGISTER: {len(findings)} open")
    for f in findings:
        print(f"  [{f['severity']}] {f['id']}: {f['title']}")
        print(f"        {f['detail']}")
        print(f"        evidence={json.dumps(f['evidence'], ensure_ascii=False)}")

    out = ROOT / "work" / "s4_integrity_report.json"
    out.write_text(json.dumps({
        "pilot_n": len(pilot), "prelabel_n": len(pre), "queue_n": len(queue),
        "pilot_semester": pilot["semester"].value_counts().to_dict(),
        "pilot_agent": agent_vc,
        "prelabel_task_bloom": pre["task_bloom"].value_counts().to_dict(),
        "prelabel_student_evidence": pre["student_evidence_bloom"].value_counts().to_dict(),
        "checks_total": len(checks), "checks_failed": failed,
        "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in checks],
        "findings": findings,
        "manual_sha256": sha256(MANUAL), "template_sha256": sha256(TEMPLATE),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n-> {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
