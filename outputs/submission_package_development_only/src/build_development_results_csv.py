"""Build the DEVELOPMENT_ONLY result tables for the competition candidate package.

Inputs : data/annotations/ai/pilot_ai_provisional.csv (AI_PROVISIONAL, 70 rows)
         reports/development/partial_identification_grid.csv (693 cells)
Outputs: reports/submission/development_results_record_level.csv
         reports/submission/development_results_summary.csv

Rules:
- No model changes; weights use the frozen formula at the baseline
  theta0 = (lambda_prompt=0, lambda_context=0, r_medium=0.75).
- AIV and ranking are NOT computed: formal Gate has not passed.
- Zero effective weight is NO_EFFECTIVE_EVIDENCE, never 0.
This is NOT a formal competition ranking result.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
GRID = ROOT / "reports" / "development" / "partial_identification_grid.csv"
OUT = ROOT / "reports" / "submission"
LEVELS = {"L1", "L2", "L3", "L4", "L5", "L6"}
PENDING = "NOT_AVAILABLE_PENDING_FORMAL_GATE"
LP, LC, RM = 0.0, 0.0, 0.75
BANNER = {
    "annotation_source": "AI_PROVISIONAL",
    "development_status": "DEVELOPMENT_ONLY",
    "formal_gate_eligible": "false",
    "claim_boundary": "NOT A FORMAL COMPETITION RESULT OR RANKING",
}


def weight(r):
    if r["student_evidence_bloom"] not in LEVELS:
        return 0.0
    c = RM if r["confidence"] == "medium" else (1.0 if r["confidence"] == "high" else 0.5)
    return c * (1 - LP * (r["prompt_induced"] == "true")) * (1 - LC * (r["context_truncated"] == "true"))


def fmt(x):
    return "" if x is None else repr(float(x))


def main():
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8-sig")))
    assert all(r["annotation_source"] == "AI_PROVISIONAL" for r in rows)
    OUT.mkdir(parents=True, exist_ok=True)

    record_fields = ["record_id", "evidence_class", "student_evidence_bloom", "task_bloom",
                     "evidence_level_numeric", "confidence", "prompt_induced", "context_truncated",
                     "baseline_weight", "enters_score", "record_score_status",
                     "AIV", "ranking", *BANNER]
    with (OUT / "development_results_record_level.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=record_fields)
        w.writeheader()
        for r in sorted(rows, key=lambda x: x["record_id"]):
            ev = r["student_evidence_bloom"]
            readable = ev in LEVELS
            wt = weight(r)
            w.writerow({
                "record_id": r["record_id"],
                "evidence_class": "READABLE_EVIDENCE" if readable else ev,
                "student_evidence_bloom": ev,
                "task_bloom": r["task_bloom"],
                "evidence_level_numeric": ev[1] if readable else "",
                "confidence": r["confidence"],
                "prompt_induced": r["prompt_induced"],
                "context_truncated": r["context_truncated"],
                "baseline_weight": fmt(wt),
                "enters_score": str(readable and wt > 0).lower(),
                "record_score_status": "IN_SCORE_DENOMINATOR" if readable and wt > 0
                else "NOT_SCORED_" + ("ZERO_WEIGHT" if readable else ev),
                "AIV": PENDING,
                "ranking": PENDING,
                **BANNER,
            })

    grid = list(csv.DictReader(GRID.open(encoding="utf-8-sig")))
    defined = [g for g in grid if g["valid_or_undefined"] == "True"]
    undefined = [g for g in grid if g["valid_or_undefined"] != "True"]
    base = next(g for g in grid if float(g["lambda_prompt"]) == LP and float(g["lambda_context"]) == LC
                and float(g["r_medium"]) == RM)

    def rng(key):
        vals = [float(g[key]) for g in defined]
        return min(vals), max(vals)

    summary = [
        ("records_total", "70-record denominator", len(rows), ""),
        ("readable_evidence", "L1-L6", sum(r["student_evidence_bloom"] in LEVELS for r in rows), ""),
        ("no_evidence", "NO_EVIDENCE", sum(r["student_evidence_bloom"] == "NO_EVIDENCE" for r in rows), ""),
        ("undetermined", "UNDETERMINED", sum(r["student_evidence_bloom"] == "UNDETERMINED" for r in rows), ""),
        ("grid_cells", "parameter grid", len(grid), ""),
        ("grid_defined", "effective weight > 0", len(defined), ""),
        ("grid_undefined", "NO_EFFECTIVE_EVIDENCE", len(undefined), ""),
        ("ABL_baseline", "Score @ theta0", base["adjusted_ABL"], ""),
        ("HOT_baseline", "Score @ theta0", base["adjusted_HOT"], ""),
        ("Gap_baseline", "Score @ theta0", base["adjusted_gap"], ""),
        ("effective_weight_baseline", "Support @ theta0", base["effective_weight"], ""),
        ("effective_coverage_baseline", "Support @ theta0; denominator 70", base["effective_coverage"], ""),
    ]
    for key, label in (("adjusted_ABL", "ABL"), ("adjusted_HOT", "HOT"), ("adjusted_gap", "Gap"),
                       ("effective_weight", "effective_weight"), ("effective_coverage", "effective_coverage")):
        lo, hi = rng(key)
        summary.append((f"{label}_range_defined", "min..max over defined cells", lo, hi))
    summary += [("AIV", "formal only", PENDING, ""), ("ranking", "formal only", PENDING, "")]

    with (OUT / "development_results_summary.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "scope", "value", "value_max", *BANNER])
        for q, scope, v, v2 in summary:
            w.writerow([q, scope, v, v2, *BANNER.values()])
    print("wrote reports/submission/development_results_record_level.csv")
    print("wrote reports/submission/development_results_summary.csv")
    print("DEVELOPMENT_ONLY / AI_PROVISIONAL / AIV and ranking NOT_AVAILABLE_PENDING_FORMAL_GATE")


if __name__ == "__main__":
    main()
