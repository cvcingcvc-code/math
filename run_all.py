"""Minimal DEVELOPMENT_ONLY reproduction chain.

AI_PROVISIONAL development data
  -> development metrics            (src/run_development_experiment.py)
  -> reliability sensitivity        (src/run_reliability_sensitivity.py)
  -> bounds grid, Figure 4, Demo payload (src/run_partial_identification.py --mode development)
  -> independent recomputation      (src/verification/recompute_bounds.py)
  -> core closure (src/build_core_closure.py)
  -> consistency checks + core report (reports/submission/run_all_report.json)

This script never reads human R1/R2 labels. `--mode formal` only delegates to the
frozen fail-closed Gate check, which refuses while the Gate is not PASS; see
FORMAL_GATE_SWITCH.md.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "reports" / "submission" / "run_all_report.json"

REQUIRED_INPUTS = [
    "data/annotations/ai/pilot_ai_provisional.csv",
    "src/development_data.py",
    "src/run_development_experiment.py",
    "src/run_reliability_sensitivity.py",
    "src/run_partial_identification.py",
    "src/verification/recompute_bounds.py",
    "src/build_development_results_csv.py",
    "src/build_core_closure.py",
]

STEPS = [
    ["src/run_development_experiment.py"],
    ["src/run_reliability_sensitivity.py"],
    ["src/run_partial_identification.py", "--mode", "development"],
    ["src/verification/recompute_bounds.py"],
    ["src/build_development_results_csv.py"],
    ["src/build_core_closure.py"],
]

# Frozen development expectations (reports/verification/core_numbers_source_of_truth.json).
EXPECTED = {
    "total_records": 70,
    "interpretable_evidence_count": 16,
    "no_evidence_count": 19,
    "undetermined_count": 35,
    "parameter_grid_size": 693,
    "defined_grid_count": 660,
    "undefined_grid_count": 33,
}
TOL = 1e-9


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def check_outputs():
    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    truth = load("reports/verification/core_numbers_source_of_truth.json")
    for key, value in EXPECTED.items():
        add(f"source_of_truth.{key}=={value}", truth.get(key) == value, str(truth.get(key)))
    for key, value in (("abl", 3.5625), ("hot", 0.375), ("gap", 1.125)):
        lo, hi = truth[f"{key}_min"], truth[f"{key}_max"]
        add(f"{key.upper()} stable at {value}", abs(lo - value) < TOL and abs(hi - value) < TOL, f"{lo}..{hi}")
    add("effective_weight range 0.4..16.0",
        abs(truth["effective_weight_min_nonzero"] - 0.4) < TOL and abs(truth["effective_weight_max"] - 16.0) < TOL)
    add("coverage denominator is 70 records",
        abs(truth["effective_coverage_max"] - 16.0 / 70) < TOL and abs(truth["effective_coverage_min_nonzero"] - 0.4 / 70) < TOL)
    add("status labels", truth.get("status") == "AI_PROVISIONAL"
        and truth.get("annotation_status") == "DEVELOPMENT_ONLY"
        and truth.get("formal_gate_eligible") is False)

    demo = load("reports/demo/demo_payload.json")
    add("demo labels", demo.get("annotation_source") == "AI_PROVISIONAL"
        and demo.get("annotation_status") == "DEVELOPMENT_ONLY"
        and demo.get("formal_gate_eligible") is False)
    mp = demo.get("measurement_problem", {})
    add("demo records/evidence == 70/16", mp.get("records") == 70 and mp.get("readable_evidence") == 16, str(mp))

    svg = (ROOT / "reports/development/core_figure_4_bounds_support.svg").read_text(encoding="utf-8")
    for token in ("lambda_prompt", "lambda_context = 0.00", "r_medium = 0.75", "/ 70 development records",
                  "NO_EFFECTIVE_EVIDENCE", "not a causal effect", "AI_PROVISIONAL / DEVELOPMENT_ONLY"):
        add(f"figure4 contains '{token}'", token in svg)

    html = (ROOT / "reports/demo/index.html").read_text(encoding="utf-8")
    for token in ("DEVELOPMENT_ONLY", "AI_PROVISIONAL", "NO_EFFECTIVE_EVIDENCE", "70 development records"):
        add(f"demo html contains '{token}'", token in html)

    gate = load("reports/annotation_gate_report.json")
    add("formal gate not passed (expected while R1/R2 pending)", gate.get("gate_status") != "PASS",
        str(gate.get("gate_status")))

    import csv
    rec = list(csv.DictReader((ROOT / "reports/submission/development_results_record_level.csv").open(encoding="utf-8-sig")))
    add("result csv: 70 records, 16 scored",
        len(rec) == 70 and sum(r["enters_score"] == "true" for r in rec) == 16)
    add("result csv: AIV/ranking pending, labels kept",
        all(r["AIV"] == r["ranking"] == "NOT_AVAILABLE_PENDING_FORMAL_GATE"
            and r["annotation_source"] == "AI_PROVISIONAL" and r["development_status"] == "DEVELOPMENT_ONLY"
            and r["formal_gate_eligible"] == "false" for r in rec))

    closure = load("reports/development/research_core_closure.json")
    add("core closure frozen for submission",
        closure.get("status") == "RESEARCH_CORE_FROZEN_FOR_SUBMISSION"
        and closure.get("formal_gate_eligible") is False)
    add("core closure retains provisional boundary",
        closure.get("readable_evidence_all_prompt_induced") is True
        and closure.get("readable_evidence_prompt_false_count") == 0)
    add("ablation/counterexample artifacts present",
        all((ROOT / p).exists() for p in [
            "reports/development/raw_adjusted_metrics.csv",
            "reports/development/ablation_results.csv",
            "reports/development/counterexamples.csv",
            "reports/development/research_core_closure.md",
        ]))
    return checks


def main():
    if "--mode" in sys.argv and sys.argv[sys.argv.index("--mode") + 1:][:1] == ["formal"]:
        # Delegate to the frozen fail-closed Gate check; never bypass it here.
        proc = subprocess.run([sys.executable, "src/run_partial_identification.py", "--mode", "formal"],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        print((proc.stdout + proc.stderr).strip())
        print("RUN_ALL_FORMAL_BLOCKED" if proc.returncode else "formal step exited 0")
        return proc.returncode or 0
    missing = [p for p in REQUIRED_INPUTS if not (ROOT / p).exists()]
    if missing:
        print("RUN_ALL_BLOCKED: missing inputs:\n  " + "\n  ".join(missing))
        return 2
    steps = []
    for step in STEPS:
        proc = subprocess.run([sys.executable, *step], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        steps.append({"step": " ".join(step), "exit_code": proc.returncode})
        print(f"[{proc.returncode}] {' '.join(step)}")
        if proc.returncode != 0:
            print(proc.stdout[-2000:], proc.stderr[-2000:])
            break
    ok_steps = all(s["exit_code"] == 0 for s in steps) and len(steps) == len(STEPS)
    checks = check_outputs() if ok_steps else []
    failed = [c for c in checks if not c["pass"]]
    report = {
        "annotation_source": "AI_PROVISIONAL",
        "annotation_status": "DEVELOPMENT_ONLY",
        "formal_gate_eligible": False,
        "claim_boundary": "Development-only reproduction; not formal Gate, AIV, ranking or causal evidence.",
        "steps": steps,
        "checks": checks,
        "result": "PASS" if ok_steps and not failed else "FAIL",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"checks: {len(checks) - len(failed)}/{len(checks)} passed; result={report['result']}")
    for c in failed:
        print("FAILED:", c["check"], c["detail"])
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
