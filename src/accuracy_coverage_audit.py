"""Fail-closed accuracy/error versus coverage audit.

The audit requires a validated truth column and a decision/prediction column.
Without those columns it emits NOT_SUPPORTED rather than treating filtered
records as evidence of improved accuracy.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--input", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--prediction", default="prediction"); ap.add_argument("--truth", default="true_label"); ap.add_argument("--decision", default="decision")
    a = ap.parse_args(); frame = pd.read_csv(a.input, dtype=str, keep_default_na=False)
    missing = [c for c in (a.prediction, a.truth) if c not in frame.columns]
    payload = {"audit": "accuracy_coverage", "status": "NOT_SUPPORTED", "result_scope": "DEVELOPMENT_ONLY", "input": str(a.input), "n": len(frame), "coverage_denominator": len(frame), "missing_required_columns": missing}
    if not missing:
        valid = frame[a.prediction].ne("") & frame[a.truth].ne("")
        accepted = valid
        if a.decision in frame.columns: accepted = valid & frame[a.decision].str.upper().eq("ACCEPT")
        n = int(accepted.sum()); payload.update({"status":"COMPUTED", "accepted_n":n, "coverage": n/len(frame) if len(frame) else None, "abstention_rate": 1-n/len(frame) if len(frame) else None, "accepted_accuracy": float((frame.loc[accepted,a.prediction]==frame.loc[accepted,a.truth]).mean()) if n else None, "accepted_error_rate": float((frame.loc[accepted,a.prediction]!=frame.loc[accepted,a.truth]).mean()) if n else None})
    a.out.parent.mkdir(parents=True, exist_ok=True); a.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"); print(json.dumps(payload, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
