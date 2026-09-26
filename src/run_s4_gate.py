"""S4 Pilot Annotation Gate: single entry point.

Steps:
  1. verify canonical data integrity (frozen invariants + defect register)
  2. verify the frozen R1/R2 worksheets without overwriting them
  3. if returned annotations exist, produce the single-annotator test-retest report

Run:
  python src/run_s4_gate.py
  python src/run_s4_gate.py --scope all

The formal design is frozen as R1 ``pilot_worksheet_A.csv`` followed by R2
``pilot_worksheet_A_retest.csv`` at least 24 hours later.  The retained blank
worksheet B is not a second human coder.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HUMAN = ROOT / "data" / "annotations" / "human"


def run(args: list[str]) -> int:
    print(f"\n$ {' '.join(args)}")
    return subprocess.call([sys.executable] + args, cwd=ROOT)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["gate70", "all"], default="gate70")
    ap.add_argument("--coders", nargs="+", default=["A"],
                    help="legacy worksheet build option; existing R1/R2 are never overwritten")
    ap.add_argument("--human-dir", type=Path, default=HUMAN,
                    help="directory scanned for returned worksheets")
    ap.add_argument("--a", type=Path, help="returned worksheet for coder A")
    ap.add_argument("--b", type=Path, help="returned R2 worksheet")
    args = ap.parse_args()

    print("=" * 78)
    print("S4 PILOT ANNOTATION GATE")
    print("=" * 78)

    print("\n--- step 0: reliability self-tests ---")
    if run([str(SRC / "reliability.py")]):
        print("reliability self-tests FAILED; stopping.")
        return 1

    print("\n--- step 1: canonical data integrity ---")
    if run([str(SRC / "verify_pilot_integrity.py")]):
        print("integrity invariants FAILED; stopping.")
        return 1

    print("\n--- step 2: verify frozen R1/R2 worksheets ---")
    r1_default = HUMAN / "pilot_worksheet_A.csv"
    r2_default = HUMAN / "pilot_worksheet_A_retest.csv"
    if not r1_default.exists():
        cmd = [str(SRC / "build_annotation_worksheets.py"), "--scope", args.scope,
               "--coders", "A"]
        if run(cmd):
            print("worksheet build FAILED; stopping.")
            return 1
    else:
        print(f"  preserving existing R1: {r1_default.relative_to(ROOT)}")
    if r2_default.exists():
        print(f"  preserving existing R2: {r2_default.relative_to(ROOT)}")
    else:
        print("  R2 worksheet is not present; run build_retest_worksheet.py before annotation.")

    print("\n--- step 3: gate report ---")
    sys.path.insert(0, str(SRC))
    from csv_safe_read import read_worksheet

    def has_labels(path: Path) -> bool:
        if not path.exists():
            return False
        df = read_worksheet(path)
        return "task_bloom" in df.columns and int(df["task_bloom"].astype(str).str.strip().ne("").sum()) > 0

    filled = [args.a, args.b] if args.a and args.b else [r1_default, r2_default]
    filled = [p for p in filled if p and has_labels(p)]

    if len(filled) < 2:
        print(f"  {len(filled)} worksheet(s) carry labels; need both frozen R1 and R2.")
        print("  PENDING: human annotation not returned yet -> Gate Report not generated.")
        print("  This is the expected state until the test-retest rounds are returned.")
        print("  When they do, re-run this script or pass --a <R1> --b <R2>.")
        return 0
    print(f"  R1: {filled[0]}\n  R2: {filled[1]}")
    cmd = [str(SRC / "solo_retest_gate.py"), "report", "--r1", str(filled[0]), "--r2", str(filled[1])]
    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
