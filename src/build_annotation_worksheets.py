"""S4-Pilot Gate: build BLIND human annotation worksheets.

Fixes two defects found by src/verify_pilot_integrity.py:
  S4-F01  pilot_sample.csv::ai_context_text is the AI reply that FOLLOWS the
          student turn (future content). This builder never uses it; prior
          context is reconstructed strictly from clean_interactions turn order.
  S4-F02  pilot_human_review_queue.csv embeds AI prelabels and agent/path
          identifiers, so it cannot be handed to annotators. This builder emits
          a blinded worksheet instead and keeps the mapping in a separate key.

Read-only with respect to source data. Writes new files only.

Usage:
  python src/build_annotation_worksheets.py --scope gate70 --coders A B
  python src/build_annotation_worksheets.py --scope all    --coders A B
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
HUMAN = ROOT / "data" / "annotations" / "human"
KEYS = ROOT / "data" / "annotations" / "_keys"
NO_PRIOR = "[NO_PRIOR_AI_TURN_IN_SOURCE_EXPORT]"
MANUAL_VERSION = "V0.1.1"
SEED = 20260925

# Fields the annotator must fill. "always" = every row; others are conditional.
BLANK_ALWAYS = [
    "speaker_role_check", "task_bloom", "task_confidence",
    "student_evidence_bloom", "evidence_confidence",
    "confidence", "reason", "ambiguity_type", "needs_second_review",
]
BLANK_CONDITIONAL = [
    "task_source", "task_actor", "evidence_span", "content_relation",
    "partial_rewrite", "prompt_induced", "scaffold_share", "correctness",
    "speaker_unknown_reason", "source_unknown_reason", "elapsed_sec",
]
VISIBLE_FIELDS = ["case_order", "record_id", "student_text", "prior_ai_context", "context_truncated"]

# Analysis-side only; must never appear in an annotator-visible file.
MASKED_FIELDS = ["agent_type", "agent_confidence", "path_case", "semester", "student_id",
                 "turn_id", "source_row_id", "pilot_sampling_strata", "review_sample_type",
                 "review_priority_score", "human_review_reason", "text_length_chars",
                 "task_bloom_ai", "student_evidence_bloom_ai"]


def reconstruct_prior_context(ci: pd.DataFrame) -> dict[str, tuple[str, bool]]:
    """Strictly-prior AI text per turn_id, from source-row turn order.

    Returns {turn_id: (text, truncated)}. Truncation at 2 prior AI turns is a
    declared V0.1.1 window rule, not a silent edit.
    """
    ci = ci.sort_values(["source_row_id", "turn_index_in_session"]).reset_index(drop=True)
    out: dict[str, tuple[str, bool]] = {}
    for src, grp in ci.groupby("source_row_id", sort=False):
        prior_ai: list[str] = []
        for _, row in grp.iterrows():
            txt = " ".join(str(row["ai_text"]).split())
            truncated = False
            if row["speaker_role"] == "ai":
                prior_ai.append(txt)
            else:
                kept = [t for t in prior_ai if t][-2:]
                truncated = len([t for t in prior_ai if t]) > 2
                out[row["turn_id"]] = (" ".join(kept) if kept else NO_PRIOR, truncated)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["gate70", "all"], default="gate70")
    ap.add_argument("--coders", nargs="+", default=["A", "B"])
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    pilot = pd.read_csv(PROC / "pilot_sample.csv", dtype=str, keep_default_na=False)
    pre = pd.read_csv(PROC / "pilot_ai_prelabel.csv", dtype=str, keep_default_na=False)
    queue = pd.read_csv(PROC / "pilot_human_review_queue.csv", dtype=str, keep_default_na=False)
    ci = pd.read_csv(PROC / "clean_interactions.csv", dtype=str, keep_default_na=False)

    prior = reconstruct_prior_context(ci)

    scope_ids = (list(queue["record_id"]) if args.scope == "gate70" else list(pilot["pilot_id"]))
    scope_ids = sorted(set(scope_ids), key=lambda x: int(x[1:]))

    p = pilot.set_index("pilot_id")
    q = queue.set_index("record_id")
    a = pre.set_index("record_id")

    rows = []
    for rid in scope_ids:
        pv, pr, ai = p.loc[rid], q.loc[rid] if rid in q.index else None, a.loc[rid]
        text, trunc = prior.get(pv["turn_id"], (NO_PRIOR, False))
        rows.append({
            "record_id": rid,
            "student_text": pv["student_text"],
            "prior_ai_context": text,
            "context_truncated": str(trunc).lower(),
            # analysis-side (kept in the key only)
            "_semester": pv["semester"],
            "_student_id": pv["student_id"],
            "_turn_id": pv["turn_id"],
            "_source_row_id": pv["source_row_id"],
            "_agent_type": pv["agent_type"],
            "_agent_confidence": pv["agent_confidence"],
            "_text_length_chars": pv["text_length_chars"],
            "_path_case": ai["path_case"],
            "_pilot_sampling_strata": ai["pilot_sampling_strata"],
            "_task_bloom_ai": ai["task_bloom"],
            "_student_evidence_bloom_ai": ai["student_evidence_bloom"],
            "_in_review_queue": "true" if rid in q.index else "false",
            "_review_sample_type": (pr["review_sample_type"] if pr is not None else ""),
            "_review_priority_score": (pr["review_priority_score"] if pr is not None else ""),
            "_human_review_reason": (pr["human_review_reason"] if pr is not None else ""),
        })
    base = pd.DataFrame(rows)

    # blind, seeded order (identical across coders so disagreement is comparable)
    order = list(base.index)
    random.Random(args.seed).shuffle(order)
    base = base.loc[order].reset_index(drop=True)

    report = {"scope": args.scope, "n_records": len(base), "seed": args.seed,
              "coders": args.coders, "manual_version": MANUAL_VERSION, "files": [], "checks": {}}

    for coder in args.coders:
        df = base[["record_id", "student_text", "prior_ai_context", "context_truncated"]].copy()
        df.insert(0, "case_order", range(1, len(df) + 1))
        for col in BLANK_ALWAYS + BLANK_CONDITIONAL:
            df[col] = ""
        df = df[VISIBLE_FIELDS + BLANK_ALWAYS + BLANK_CONDITIONAL]
        path = HUMAN / f"pilot_worksheet_{coder}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        report["files"].append(str(path.relative_to(ROOT)))
        report["checks"][f"coder_{coder}"] = {
            "rows": int(len(df)),
            "leaked_columns": [c for c in MASKED_FIELDS if c in df.columns],
            "empty_label_columns": [c for c in BLANK_ALWAYS + BLANK_CONDITIONAL
                                    if df[c].astype(str).str.len().sum() == 0],
        }

    key = base[["record_id"] + [c for c in base.columns if c.startswith("_")]].copy()
    key.columns = [c.lstrip("_") if c.startswith("_") else c for c in key.columns]
    key.insert(0, "case_order", range(1, len(key) + 1))
    key["manual_version"] = MANUAL_VERSION
    keypath = KEYS / "pilot_worksheet_key.csv"
    key.to_csv(keypath, index=False, encoding="utf-8-sig")
    report["files"].append(str(keypath.relative_to(ROOT)))

    # verify blindness
    leaked = []
    for coder in args.coders:
        cols = pd.read_csv(HUMAN / f"pilot_worksheet_{coder}.csv", dtype=str, nrows=0).columns
        leaked += [c for c in MASKED_FIELDS if c in cols]
    report["checks"]["blindness"] = {"leaked_columns": sorted(set(leaked)), "blind": not leaked}
    report["checks"]["agent_unknown_in_scope"] = int((base["_agent_type"] == "unknown").sum())
    report["checks"]["records_without_prior_ai"] = int((base["prior_ai_context"] == NO_PRIOR).sum())

    out = ROOT / "work" / "worksheet_build_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"scope={args.scope}  records={len(base)}  coders={args.coders}")
    for f in report["files"]:
        print(f"  wrote {f}")
    print(f"  blindness: {report['checks']['blindness']}")
    print(f"  records without prior AI context: {report['checks']['records_without_prior_ai']}")
    print(f"  agent_type=unknown in scope: {report['checks']['agent_unknown_in_scope']}")
    print(f"-> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())