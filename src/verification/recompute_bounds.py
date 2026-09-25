"""Independent read-only reproduction of the development bounds results.

This script intentionally does not import the production bounds implementation.
It reads the AI provisional CSV, reconstructs the declared Cartesian grid, and
writes cross-check artifacts under reports/verification/.
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
OUT = ROOT / "reports" / "verification"
LEVELS = {f"L{i}" for i in range(1, 7)}


def read_rows():
    with INPUT.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise RuntimeError("provisional CSV is empty")
    return rows


def quantiles(values):
    xs = sorted(float(x) for x in values)
    def q(p):
        if not xs:
            return None
        pos = (len(xs) - 1) * p
        lo, hi = math.floor(pos), math.ceil(pos)
        if lo == hi:
            return xs[lo]
        return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)
    return {"min": xs[0], "q25": q(0.25), "median": q(0.5), "q75": q(0.75), "max": xs[-1]}


def independent_metric(rows, lambda_prompt, lambda_context, r_medium):
    values = []
    for row in rows:
        evidence = row["student_evidence_bloom"]
        if evidence not in LEVELS:
            continue
        level = int(evidence[1])
        task = int(row["task_bloom"][1]) if row["task_bloom"] in LEVELS else None
        confidence = row["confidence"]
        base_confidence = {"high": 1.0, "medium": r_medium, "low": 0.5}.get(confidence)
        if base_confidence is None:
            raise ValueError(f"unexpected confidence={confidence!r}")
        prompt = row["prompt_induced"].strip().lower() == "true"
        context = row["context_truncated"].strip().lower() == "true"
        weight = base_confidence * (1 - lambda_prompt * prompt) * (1 - lambda_context * context)
        values.append({"level": level, "task": task, "weight": weight})
    total = sum(item["weight"] for item in values)
    result = {
        "lambda_prompt": lambda_prompt,
        "lambda_context": lambda_context,
        "r_medium": r_medium,
        "effective_weight": total,
        "effective_coverage": total / len(rows),
        "defined": total > 0,
        "undefined_reason": "" if total > 0 else "NO_EFFECTIVE_EVIDENCE",
    }
    if total == 0:
        result.update({"ABL": None, "HOT": None, "Gap": None})
        return result
    result["ABL"] = sum(item["level"] * item["weight"] for item in values) / total
    result["HOT"] = sum((item["level"] >= 4) * item["weight"] for item in values) / total
    gap_values = [item for item in values if item["task"] is not None]
    gap_denominator = sum(item["weight"] for item in gap_values)
    result["Gap"] = (sum((item["task"] - item["level"]) * item["weight"] for item in gap_values) / gap_denominator
                     if gap_denominator else None)
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def raw_recount(rows):
    readable = [r for r in rows if r["student_evidence_bloom"] in LEVELS]
    recount = {
        "total_records": len(rows),
        "student_evidence_bloom": dict(Counter(r["student_evidence_bloom"] for r in rows)),
        "interpretable_evidence_count": len(readable),
        "no_evidence_count": sum(r["student_evidence_bloom"] == "NO_EVIDENCE" for r in rows),
        "undetermined_count": sum(r["student_evidence_bloom"] == "UNDETERMINED" for r in rows),
        "prompt_induced": dict(Counter(r["prompt_induced"] for r in rows)),
        "context_truncated": dict(Counter(r["context_truncated"] for r in rows)),
        "confidence": dict(Counter(r["confidence"] for r in rows)),
        "task_actor": dict(Counter(r["task_actor"] for r in rows)),
        "task_source": dict(Counter(r["task_source"] for r in rows)),
        "readable_prompt_induced": dict(Counter(r["prompt_induced"] for r in readable)),
        "readable_context_truncated": dict(Counter(r["context_truncated"] for r in readable)),
        "readable_confidence": dict(Counter(r["confidence"] for r in readable)),
        "readable_task_actor": dict(Counter(r["task_actor"] for r in readable)),
        "readable_task_source": dict(Counter(r["task_source"] for r in readable)),
        "status": {
            "annotation_source": sorted(set(r["annotation_source"] for r in rows)),
            "annotation_status": sorted(set(r["annotation_status"] for r in rows)),
            "formal_gate_eligible": False,
        },
    }
    return recount


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    recount = raw_recount(rows)
    write_json(OUT / "raw_input_recount.json", recount)
    fields = ["category", "value", "count"]
    with (OUT / "raw_input_recount.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for category, counts in (
            ("student_evidence_bloom", recount["student_evidence_bloom"]),
            ("prompt_induced", recount["prompt_induced"]),
            ("context_truncated", recount["context_truncated"]),
            ("confidence", recount["confidence"]),
            ("task_actor", recount["task_actor"]),
            ("task_source", recount["task_source"]),
        ):
            for value, count in sorted(counts.items()):
                writer.writerow({"category": category, "value": value, "count": count})

    prompt_values = [round(i / 20, 2) for i in range(21)]
    context_values = [round(i / 10, 2) for i in range(11)]
    reliability_values = [0.5, 0.75, 1.0]
    grid = [independent_metric(rows, lp, lc, rm)
            for lp in prompt_values for lc in context_values for rm in reliability_values]
    with (OUT / "independent_bounds_reproduction.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(grid[0]))
        writer.writeheader()
        writer.writerows(grid)

    defined = [row for row in grid if row["defined"]]
    undefined = [row for row in grid if not row["defined"]]
    weights = [row["effective_weight"] for row in grid]
    nonzero_weights = [x for x in weights if x > 0]
    coverages = [row["effective_coverage"] for row in grid if row["effective_coverage"] > 0]
    summary = {
        "independent_implementation": True,
        "input": str(INPUT.relative_to(ROOT)).replace("\\", "/"),
        "status": {"annotation_source": "AI_PROVISIONAL", "annotation_status": "DEVELOPMENT_ONLY", "formal_gate_eligible": False},
        "raw_recount": recount,
        "parameter_space": {
            "lambda_prompt": {"min": 0.0, "max": 1.0, "step": 0.05, "count": len(prompt_values)},
            "lambda_context": {"min": 0.0, "max": 1.0, "step": 0.10, "count": len(context_values)},
            "r_medium": reliability_values,
            "theoretical_grid_size": len(prompt_values) * len(context_values) * len(reliability_values),
        },
        "grid_counts": {"total": len(grid), "defined": len(defined), "undefined": len(undefined)},
        "bounds": {
            "ABL": {"min": min(row["ABL"] for row in defined), "max": max(row["ABL"] for row in defined)},
            "HOT": {"min": min(row["HOT"] for row in defined), "max": max(row["HOT"] for row in defined)},
            "Gap": {"min": min(row["Gap"] for row in defined), "max": max(row["Gap"] for row in defined)},
            "effective_weight": quantiles(nonzero_weights),
            "effective_coverage": quantiles(coverages),
        },
        "undefined_examples": undefined[:3],
        "stability": {
            "ABL_all_defined_equal": len({round(row["ABL"], 12) for row in defined}) == 1,
            "HOT_all_defined_equal": len({round(row["HOT"], 12) for row in defined}) == 1,
            "Gap_all_defined_equal": len({round(row["Gap"], 12) for row in defined}) == 1,
            "all_readable_prompt_induced": all(r["prompt_induced"] == "true" for r in rows if r["student_evidence_bloom"] in LEVELS),
            "all_readable_context_not_truncated": all(r["context_truncated"] == "false" for r in rows if r["student_evidence_bloom"] in LEVELS),
            "all_readable_confidence_medium": all(r["confidence"] == "medium" for r in rows if r["student_evidence_bloom"] in LEVELS),
            "reason": "Every readable row has the same prompt/context/confidence factors, so parameter-dependent factors are a common multiplier and cancel in normalized metrics.",
        },
    }
    write_json(OUT / "independent_bounds_summary.json", summary)

    # Minimal source-of-truth object, kept separate from the detailed summary.
    source = {
        "total_records": len(rows),
        "interpretable_evidence_count": recount["interpretable_evidence_count"],
        "no_evidence_count": recount["no_evidence_count"],
        "undetermined_count": recount["undetermined_count"],
        "parameter_grid_size": len(grid),
        "defined_grid_count": len(defined),
        "undefined_grid_count": len(undefined),
        "abl_min": summary["bounds"]["ABL"]["min"],
        "abl_max": summary["bounds"]["ABL"]["max"],
        "hot_min": summary["bounds"]["HOT"]["min"],
        "hot_max": summary["bounds"]["HOT"]["max"],
        "gap_min": summary["bounds"]["Gap"]["min"],
        "gap_max": summary["bounds"]["Gap"]["max"],
        "effective_weight_min_nonzero": summary["bounds"]["effective_weight"]["min"],
        "effective_weight_max": summary["bounds"]["effective_weight"]["max"],
        "effective_weight_median": summary["bounds"]["effective_weight"]["median"],
        "effective_coverage_min_nonzero": summary["bounds"]["effective_coverage"]["min"],
        "effective_coverage_max": summary["bounds"]["effective_coverage"]["max"],
        "effective_coverage_median": summary["bounds"]["effective_coverage"]["median"],
        "all_interpretable_prompt_induced": summary["stability"]["all_readable_prompt_induced"],
        "data_source": str(INPUT.relative_to(ROOT)).replace("\\", "/"),
        "status": "AI_PROVISIONAL",
        "annotation_status": "DEVELOPMENT_ONLY",
        "formal_gate_eligible": False,
    }
    write_json(OUT / "core_numbers_source_of_truth.json", source)
    print(json.dumps({"records": len(rows), "readable": recount["interpretable_evidence_count"], "grid": len(grid), "defined": len(defined), "undefined": len(undefined), "bounds": summary["bounds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
