"""B010: single-coder test-retest worksheet (round 2 for the same human coder).

Context: the project owner competes alone, so a second independent human coder
may not exist. This builds a round-2 worksheet for the SAME coder so that
intra-rater (test-retest) reliability can be measured honestly. It is NOT
inter-rater reliability and must never be reported as such (D007).

Design:
  * same 70 record_ids, same student_text / prior_ai_context as round 1
    (copied from pilot_worksheet_A.csv, so content cannot drift);
  * a DIFFERENT seeded order to weaken recall of round-1 decisions;
  * blank label columns; no AI prelabel, agent, path, semester or student id;
  * never overwrites round-1 files.

The Gate analyzer merges on record_id, so row order does not affect results.

Usage:
  python src/build_retest_worksheet.py            # build + self-check
  python src/build_retest_worksheet.py --check    # self-check only
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
HUMAN = ROOT / "data" / "annotations" / "human"
ROUND1 = HUMAN / "pilot_worksheet_A.csv"
ROUND2 = HUMAN / "pilot_worksheet_A_retest.csv"
REPORT = ROOT / "work" / "retest_build_report.json"
RETEST_SEED = 20260926  # differs from round-1 seed 20260925
CONTENT = ["record_id", "student_text", "prior_ai_context", "context_truncated"]
MASKED = ["agent_type", "path_case", "semester", "student_id", "task_bloom_ai",
          "student_evidence_bloom_ai", "pilot_sampling_strata", "review_sample_type"]


def spearman_positions(a: list[str], b: list[str]) -> float:
    pa = {r: i for i, r in enumerate(a)}
    pb = {r: i for i, r in enumerate(b)}
    return float(pd.Series([pa[r] for r in a]).corr(pd.Series([pb[r] for r in a]), method="spearman"))


def check(r1: pd.DataFrame, r2: pd.DataFrame) -> dict:
    j = r1[CONTENT].merge(r2[CONTENT], on="record_id", suffixes=("_1", "_2"))
    label_cols = [c for c in r1.columns if c not in ["case_order"] + CONTENT]
    return {
        "rows_round1": int(len(r1)), "rows_round2": int(len(r2)),
        "same_record_set": set(r1.record_id) == set(r2.record_id),
        "record_id_unique": bool(r2.record_id.is_unique),
        "content_identical": bool(all((j[f"{c}_1"] == j[f"{c}_2"]).all() for c in CONTENT[1:])),
        "same_columns_as_round1": list(r1.columns) == list(r2.columns),
        "labels_blank": bool(all(r2[c].astype(str).str.strip().eq("").all() for c in label_cols)),
        "leaked_columns": [c for c in MASKED if c in r2.columns],
        "order_spearman_vs_round1": round(spearman_positions(list(r1.record_id), list(r2.record_id)), 4),
        "same_position_count": int(sum(x == y for x, y in zip(r1.record_id, r2.record_id))),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    r1 = pd.read_csv(ROUND1, dtype=str, keep_default_na=False)

    if not args.check:
        if ROUND2.exists():
            filled = pd.read_csv(ROUND2, dtype=str, keep_default_na=False)
            if filled["task_bloom"].str.strip().ne("").any():
                print(f"refuse: {ROUND2.name} already carries labels; not overwriting.")
                return 1
        ids = list(r1.record_id)
        random.Random(RETEST_SEED).shuffle(ids)
        r2 = r1.set_index("record_id").loc[ids].reset_index()
        label_cols = [c for c in r1.columns if c not in ["case_order"] + CONTENT]
        r2[label_cols] = ""
        r2["case_order"] = range(1, len(r2) + 1)
        r2 = r2[list(r1.columns)]
        r2.to_csv(ROUND2, index=False, encoding="utf-8-sig")

    r2 = pd.read_csv(ROUND2, dtype=str, keep_default_na=False)
    res = check(r1, r2)
    ok = (res["same_record_set"] and res["record_id_unique"] and res["content_identical"]
          and res["same_columns_as_round1"] and res["labels_blank"] and not res["leaked_columns"])
    res.update({"seed": RETEST_SEED, "pass": ok,
                "reliability_type": "intra-rater test-retest (single human coder); NOT inter-rater"})
    REPORT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in res.items():
        print(f"  {k}: {v}")
    print(f"-> {REPORT.relative_to(ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
