"""DEVELOPMENT_ONLY Evidence Reliability / Bias Correction sensitivity model.

This is a transparent measurement sensitivity analysis, not a trained model and
not formal AIV/Gate evidence. It applies reliability weights to observable
student evidence only, then recomputes ABL, HOT, effective coverage and the
Task/Evidence gap over a small predeclared parameter grid.

Run from the project root:
    python src/run_reliability_sensitivity.py
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from development_data import load_annotation_data  # noqa: E402

OUT_DIR = ROOT / "reports" / "development"
OUT_CSV = OUT_DIR / "reliability_sensitivity.csv"
OUT_JSON = OUT_DIR / "reliability_model.json"
OUT_PNG = OUT_DIR / "reliability_sensitivity.svg"

BLOOM_SCORE = {f"L{i}": i for i in range(1, 7)}
OBSERVED = set(BLOOM_SCORE)
HIGH = {"L4", "L5", "L6"}
PROMPT_LAMBDAS = [0.0, 0.25, 0.5, 0.75, 1.0]
CONTEXT_LAMBDAS = [0.0, 0.5, 1.0]
CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.75, "low": 0.5}
BANNER = ["DEVELOPMENT_ONLY", "AI_PROVISIONAL", "NOT FOR FORMAL GATE OR FINAL CLAIMS"]


def weighted_mean(values: pd.Series, weights: pd.Series):
    denominator = float(weights.sum())
    return float((values * weights).sum() / denominator) if denominator else None


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_annotation_data("development")
    if len(data) != 70 or not data["record_id"].is_unique:
        raise ValueError("development input must contain 70 unique record_id values")
    if set(data["annotation_source"]) != {"AI_PROVISIONAL"}:
        raise ValueError("input identity changed: annotation_source")
    if set(data["annotation_status"]) != {"DEVELOPMENT_ONLY"}:
        raise ValueError("input identity changed: annotation_status")

    d = data[["record_id", "task_bloom", "student_evidence_bloom", "confidence",
              "prompt_induced", "context_truncated", "annotation_source",
              "annotation_status"]].copy()
    d["task_level"] = d["task_bloom"].map(BLOOM_SCORE)
    d["evidence_level"] = d["student_evidence_bloom"].map(BLOOM_SCORE)
    d["evidence_observable"] = d["student_evidence_bloom"].isin(OBSERVED)
    d["evidence_high_order"] = d["student_evidence_bloom"].isin(HIGH)
    d["prompt_flag"] = d["prompt_induced"].eq("true")
    d["context_flag"] = d["context_truncated"].eq("true")
    d["confidence_weight"] = d["confidence"].map(CONFIDENCE_WEIGHT).fillna(CONFIDENCE_WEIGHT["low"])

    rows = []
    for lp in PROMPT_LAMBDAS:
        for lc in CONTEXT_LAMBDAS:
            d["reliability_weight"] = (
                d["evidence_observable"].astype(float)
                * d["confidence_weight"]
                * (1.0 - lp * d["prompt_flag"].astype(float))
                * (1.0 - lc * d["context_flag"].astype(float))
            )
            evidence = d[d["evidence_observable"]]
            gap = d[d["evidence_observable"] & d["task_level"].notna()].copy()
            gap["gap"] = gap["task_level"] - gap["evidence_level"]
            total_weight = float(d["reliability_weight"].sum())
            evidence_weight = float(evidence["reliability_weight"].sum())
            rows.append({
                "result_scope": "DEVELOPMENT_ONLY",
                "result_source": "AI_PROVISIONAL",
                "claim_boundary": "NOT FOR FORMAL GATE OR FINAL CLAIMS",
                "lambda_prompt": lp,
                "lambda_context": lc,
                "adjusted_abl": weighted_mean(evidence["evidence_level"], evidence["reliability_weight"]),
                "adjusted_hot": weighted_mean(evidence["evidence_high_order"].astype(float), evidence["reliability_weight"]),
                "effective_evidence_coverage": evidence_weight / len(d),
                "effective_sample_weight": total_weight,
                "adjusted_task_evidence_gap": weighted_mean(gap["gap"], gap["reliability_weight"]),
                "raw_abl": float(evidence["evidence_level"].mean()),
                "raw_hot": float(evidence["evidence_high_order"].mean()),
                "raw_evidence_coverage": float(d["evidence_observable"].mean()),
                "raw_task_evidence_gap": float(gap["gap"].mean()),
                "prompt_flagged_rows": int(d["prompt_flag"].sum()),
                "context_flagged_rows": int(d["context_flag"].sum()),
                "low_confidence_rows": int(d["confidence"].eq("low").sum()),
            })

    result = pd.DataFrame(rows)
    result.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    baseline = result[(result.lambda_prompt == 0.0) & (result.lambda_context == 0.0)].iloc[0]
    prompt_only = result[result.lambda_context == 0.0]
    context_only = result[result.lambda_prompt == 0.0]
    payload = {
        "banner": BANNER,
        "data_mode": "development",
        "input": "data/annotations/ai/pilot_ai_provisional.csv",
        "model": "transparent_evidence_reliability_weight_sensitivity",
        "formal_gate_eligible": False,
        "formula": "w_i = I(observable_i) * c_i * (1 - lambda_prompt * prompt_i) * (1 - lambda_context * truncation_i)",
        "definitions": {
            "observable": "student_evidence_bloom in L1..L6; NO_EVIDENCE/UNDETERMINED receive zero weight",
            "c_i": "confidence weight: high=1.0, medium=0.75, low=0.5",
            "adjusted_abl": "sum(w_i * evidence_level_i) / sum(w_i)",
            "adjusted_hot": "sum(w_i * I(evidence_level_i in L4..L6)) / sum(w_i)",
            "effective_evidence_coverage": "sum(w_i) / 70",
            "adjusted_task_evidence_gap": "weighted mean(task_level - evidence_level) where both levels are observable",
        },
        "parameter_grid": {
            "lambda_prompt": PROMPT_LAMBDAS,
            "lambda_context": CONTEXT_LAMBDAS,
            "sensitivity_note": "Small finite grid; no unique penalty claim is made.",
        },
        "confidence_weight_assumption": CONFIDENCE_WEIGHT,
        "baseline_raw": {k: baseline[k] for k in ["raw_abl", "raw_hot", "raw_evidence_coverage", "raw_task_evidence_gap"]},
        "prompt_only_range": {
            "adjusted_abl_min": float(prompt_only.adjusted_abl.min()),
            "adjusted_abl_max": float(prompt_only.adjusted_abl.max()),
            "adjusted_hot_min": float(prompt_only.adjusted_hot.min()),
            "adjusted_hot_max": float(prompt_only.adjusted_hot.max()),
        },
        "context_only_range": {
            "adjusted_abl_min": float(context_only.adjusted_abl.min()),
            "adjusted_abl_max": float(context_only.adjusted_abl.max()),
            "adjusted_hot_min": float(context_only.adjusted_hot.min()),
            "adjusted_hot_max": float(context_only.adjusted_hot.max()),
        },
        "field_limits": [
            "No human R1/R2 labels: weights are not empirically calibrated reliability probabilities.",
            "No student_id/session/verified agent_type: no student-level or agent-level correction is attempted.",
            "Prompt and truncation flags are association/risk flags, not causal effects.",
            "This model does not calculate AIV and cannot establish a formal research conclusion.",
        ],
        "results_csv": str(OUT_CSV.relative_to(ROOT)),
        "results_png": str(OUT_PNG.relative_to(ROOT)),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    make_plot(result)
    print("\n".join(BANNER))
    print(f"rows={len(d)}; parameter_conditions={len(result)}")
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_PNG.relative_to(ROOT)}")
    print("formal_gate_eligible=False")
    return 0


def make_plot(result: pd.DataFrame) -> None:
    """Write a dependency-free SVG so the required plot needs no plotting package."""
    width, height = 760, 440
    left, top, plot_w, plot_h = 80, 50, 620, 300
    x0, x1 = min(PROMPT_LAMBDAS), max(PROMPT_LAMBDAS)
    y0, y1 = 2.5, 4.0

    def x(value: float) -> float:
        return left + (value - x0) / (x1 - x0) * plot_w

    def y(value: float) -> float:
        return top + (y1 - value) / (y1 - y0) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="380" y="25" text-anchor="middle" font-family="Arial" font-size="16" fill="#111827">DEVELOPMENT_ONLY / AI_PROVISIONAL: adjusted ABL sensitivity</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#374151"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#374151"/>',
        f'<text x="390" y="395" text-anchor="middle" font-family="Arial" font-size="13" fill="#111827">lambda_prompt</text>',
        f'<text x="18" y="205" transform="rotate(-90 18 205)" text-anchor="middle" font-family="Arial" font-size="13" fill="#111827">adjusted ABL</text>',
    ]
    for tick in PROMPT_LAMBDAS:
        xx = x(tick)
        parts += [f'<line x1="{xx:.1f}" y1="{top + plot_h}" x2="{xx:.1f}" y2="{top + plot_h + 6}" stroke="#374151"/>',
                  f'<text x="{xx:.1f}" y="{top + plot_h + 24}" text-anchor="middle" font-family="Arial" font-size="11" fill="#111827">{tick:g}</text>']
    for tick in [2.5, 3.0, 3.5, 4.0]:
        yy = y(tick)
        parts += [f'<line x1="{left - 6}" y1="{yy:.1f}" x2="{left}" y2="{yy:.1f}" stroke="#374151"/>',
                  f'<text x="{left - 12}" y="{yy + 4:.1f}" text-anchor="end" font-family="Arial" font-size="11" fill="#111827">{tick:g}</text>',
                  f'<line x1="{left}" y1="{yy:.1f}" x2="{left + plot_w}" y2="{yy:.1f}" stroke="#d1d5db"/>']
    colors = {0.0: "#2563eb", 0.5: "#d97706", 1.0: "#dc2626"}
    for lc, group in result.groupby("lambda_context"):
        group = group.sort_values("lambda_prompt")
        points = " ".join(f"{x(float(row.lambda_prompt)):.1f},{y(float(row.adjusted_abl)):.1f}" for row in group.itertuples())
        color = colors.get(float(lc), "#111827")
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        for row in group.itertuples():
            parts.append(f'<circle cx="{x(float(row.lambda_prompt)):.1f}" cy="{y(float(row.adjusted_abl)):.1f}" r="4" fill="{color}"/>')
        ly = 85 + int(float(lc) * 24)
        parts.append(f'<line x1="535" y1="{ly}" x2="555" y2="{ly}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="562" y="{ly + 4}" font-family="Arial" font-size="11" fill="#111827">lambda_context={float(lc):g}</text>')
    parts.append('<text x="380" y="425" text-anchor="middle" font-family="Arial" font-size="11" fill="#991b1b">NOT FOR FORMAL GATE OR FINAL CLAIMS</text>')
    parts.append('</svg>')
    OUT_PNG.write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
