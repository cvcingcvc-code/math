"""S4 Pilot Annotation Gate: single entry point.

Steps:
  1. verify canonical data integrity (frozen invariants + defect register)
  2. build blinded human worksheets (safe to re-run; never overwrites source data)
  3. if returned annotations exist, produce the Gate Report

Run:
  python src/run_s4_gate.py
  python src/run_s4_gate.py --scope all
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
    ap.add_argument("--coders", nargs="+", default=["A", "B"])
    ap.add_argument("--human-dir", type=Path, default=HUMAN,
                    help="directory scanned for returned worksheets")
    ap.add_argument("--a", type=Path, help="returned worksheet for coder A")
    ap.add_argument("--b", type=Path, help="returned worksheet for coder B")
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

    print("\n--- step 2: build blinded worksheets ---")
    cmd = [str(SRC / "build_annotation_worksheets.py"), "--scope", args.scope,
           "--coders", *args.coders]
    if run(cmd):
        print("worksheet build FAILED; stopping.")
        return 1

    print("\n--- step 3: gate report ---")
    import pandas as pd

    def has_labels(path: Path) -> bool:
        if not path.exists():
            return False
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        return "task_bloom" in df.columns and int(df["task_bloom"].astype(str).str.strip().ne("").sum()) > 0

    if args.a and args.b:
        filled = [args.a, args.b]
    else:
        candidates = sorted(args.human_dir.glob("*.csv"))
        filled = [p for p in candidates if has_labels(p)]
        filled.sort(key=lambda p: p.stat().st_mtime)

    if len(filled) < 2:
        print(f"  {len(filled)} worksheet(s) carry labels; need exactly 2 independent coders.")
        print("  PENDING: human annotation not returned yet -> Gate Report not generated.")
        print("  This is the expected state until annotators return their files.")
        print("  When they do, re-run this script or pass --a <fileA> --b <fileB>.")
        return 0
    if len(filled) > 2 and not (args.a and args.b):
        print(f"  found {len(filled)} labelled worksheets; pass --a and --b to disambiguate:")
        for p in filled:
            print(f"    {p}")
        return 2

    print(f"  coder A: {filled[0]}\n  coder B: {filled[1]}")
    cmd = [str(SRC / "annotation_gate_report.py"), "--a", str(filled[0]), "--b", str(filled[1])]
    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())