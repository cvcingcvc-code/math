"""B010 option (b): single-annotator test-retest path for the S4 Pilot Gate.

Context: manual V0.1 assumes two independent human coders; the project lead
competes alone (handoff/BLOCKERS.md B010). This script supports the declared
fallback design:

  Round 1 (R1): the lead fills data/annotations/human/pilot_worksheet_A.csv
               (unchanged file, existing blind order).
  Round 2 (R2): >= 24h later, WITHOUT opening R1, the lead fills a second
               blind worksheet with a DIFFERENT seeded order (this script).

The resulting statistic is INTRA-rater (test-retest) reliability. It is NOT
inter-rater agreement and must never be reported as two coders (D007/D008).
It measures rule stability for one coder, not rule transferability.

Read-only for all existing files. Writes only:
  build  -> data/annotations/human/pilot_worksheet_R2.csv
            work/solo_retest_build_report.json
  report -> reports/solo_retest_gate_report.md|.json   (via annotation_gate_report.py)

Usage:
  python src/solo_retest_gate.py build
  python src/solo_retest_gate.py report --r1 <R1_submitted.csv> --r2 <R2_submitted.csv>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
HUMAN = ROOT / "data" / "annotations" / "human"
R1_BLANK = HUMAN / "pilot_worksheet_A.csv"
# Canonical R2 blank = the file produced (and self-checked) by build_retest_worksheet.py.
# Same seed/shuffle -> identical order; `build` here is kept only as a guarded fallback.
R2_BLANK = HUMAN / "pilot_worksheet_A_retest.csv"
R2_SEED = 20260926          # differs from worksheet seed 20260925 -> different order
MIN_GAP_HOURS = 24

BANNER = (
    "> **DESIGN = SINGLE-ANNOTATOR TEST-RETEST (intra-rater).**\n"
    "> 下文中的 “coder A / coder B” 分别指**同一名人工标注者**的第 1 轮与第 2 轮盲标。\n"
    "> 这是重测信度，**不是评定者间一致性**；不证明规则可被他人复现。(B010, D007, D008)\n"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def build(args) -> int:
    r1 = pd.read_csv(R1_BLANK, dtype=str, keep_default_na=False)
    label_cols = [c for c in r1.columns if c not in
                  ("case_order", "record_id", "student_text", "prior_ai_context", "context_truncated")]
    if r1[label_cols].apply(lambda s: s.str.strip().ne("")).any().any():
        print("NOTE: pilot_worksheet_A.csv already carries labels; R2 is still built from its "
              "visible columns only, labels are dropped.")
    if R2_BLANK.exists() and not args.force:
        print(f"{R2_BLANK.relative_to(ROOT)} exists; refusing to overwrite (use --force only if blank).")
        return 1

    visible = r1[["record_id", "student_text", "prior_ai_context", "context_truncated"]].copy()
    order = list(visible.index)
    random.Random(R2_SEED).shuffle(order)
    r2 = visible.loc[order].reset_index(drop=True)
    r2.insert(0, "case_order", range(1, len(r2) + 1))
    for c in label_cols:
        r2[c] = ""
    r2 = r2[list(r1.columns)]
    r2.to_csv(R2_BLANK, index=False, encoding="utf-8-sig")

    pos1 = {rid: i for i, rid in enumerate(r1["record_id"])}
    pos2 = {rid: i for i, rid in enumerate(r2["record_id"])}
    ids = list(pos1)
    rank_corr = pd.Series([pos1[i] for i in ids]).corr(pd.Series([pos2[i] for i in ids]), method="spearman")
    report = {
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "r1_file": str(R1_BLANK.relative_to(ROOT)), "r1_sha256": sha(R1_BLANK),
        "r2_file": str(R2_BLANK.relative_to(ROOT)), "r2_sha256": sha(R2_BLANK),
        "rows": int(len(r2)), "seed": R2_SEED,
        "same_record_set": set(r1["record_id"]) == set(r2["record_id"]),
        "same_columns": list(r1.columns) == list(r2.columns),
        "order_spearman_r1_vs_r2": round(float(rank_corr), 4),
        "same_position_count": int(sum(pos1[i] == pos2[i] for i in ids)),
        "min_gap_hours": MIN_GAP_HOURS,
    }
    out = ROOT / "work" / "solo_retest_build_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["same_record_set"] and report["same_columns"] else 1


def report(args) -> int:
    for p in (args.r1, args.r2):
        if not p.exists():
            print(f"missing: {p}"); return 1
    gap_h = (args.r2.stat().st_mtime - args.r1.stat().st_mtime) / 3600
    # Never emit a research-looking report while either real worksheet is blank.
    for p in (args.r1, args.r2):
        frame = pd.read_csv(p, dtype=str, keep_default_na=False)
        label_cols = [c for c in frame.columns if c not in
                      ("case_order", "record_id", "student_text", "prior_ai_context", "context_truncated")]
        if not frame[label_cols].apply(lambda s: s.str.strip().ne("")).any().any():
            print(f"refusing report: {p} has no real annotation labels")
            return 1
    if gap_h < MIN_GAP_HOURS and not args.allow_short_gap:
        print(f"R2 saved only {gap_h:.1f}h after R1 (< {MIN_GAP_HOURS}h). "
              "Protocol violation; rerun with --allow-short-gap to report it anyway (it will be flagged).")
        return 1
    md = ROOT / "reports" / "solo_retest_gate_report.md"
    js = ROOT / "reports" / "solo_retest_gate_report.json"
    rc = subprocess.call([sys.executable, str(ROOT / "src" / "annotation_gate_report.py"),
                          "--a", str(args.r1), "--b", str(args.r2),
                          "--out", str(md), "--json", str(js)], cwd=ROOT)
    if rc:
        return rc
    flag = "" if gap_h >= MIN_GAP_HOURS else f"> **PROTOCOL FLAG:** R1→R2 间隔仅 {gap_h:.1f} h（要求 ≥ {MIN_GAP_HOURS} h）。\n"
    md.write_text(BANNER + flag + f"> R1→R2 文件保存间隔：{gap_h:.1f} h\n\n" + md.read_text(encoding="utf-8"),
                  encoding="utf-8")
    d = json.loads(js.read_text(encoding="utf-8"))
    d["design"] = {"type": "single_annotator_test_retest", "inter_rater": False,
                   "gap_hours": round(gap_h, 2), "min_gap_hours": MIN_GAP_HOURS,
                   "r1_sha256": sha(args.r1), "r2_sha256": sha(args.r2)}
    js.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"-> {md.relative_to(ROOT)} (design banner prepended)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--force", action="store_true")
    r = sub.add_parser("report")
    r.add_argument("--r1", type=Path, required=True)
    r.add_argument("--r2", type=Path, required=True)
    r.add_argument("--allow-short-gap", action="store_true")
    args = ap.parse_args()
    return build(args) if args.cmd == "build" else report(args)


if __name__ == "__main__":
    sys.exit(main())
