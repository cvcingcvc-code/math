# Submission candidate claim cross-check (development-only)

This audit follows the paper-claim review protocol and uses the current
`paper/submission_candidate.md`, source-of-truth JSON, core-closure outputs,
model code, and `FORMAL_GATE_SWITCH.md`. It does not modify formal data,
thresholds, or Gate logic.

| Claim | Source in paper | Supporting experiment | Supporting artifact | Status | Required correction |
|---|---|---|---|---|---|
| All reported numbers come from 70 AI provisional development records | Opening disclaimer; Sections 3–6 | Development loader identity checks | `data/annotations/ai/pilot_ai_provisional.csv`; `reports/development/development_results.json` | SUPPORTED | Keep the development-only banner visible in every exported derivative. |
| ABL/HOT/Gap = 3.5625/0.375/1.125 | Abstract; Section 6 | Independent bounds recomputation | `reports/verification/core_numbers_source_of_truth.json`; `reports/development/raw_adjusted_metrics.csv` | SUPPORTED | Keep tied to the provisional input and do not call them formal AIV. |
| Effective coverage ranges from 0.2286 to 0.0057 | Abstract; Sections 6 and 10 | 693-cell partial-identification grid | `reports/verification/independent_bounds_summary.json`; `reports/development/partial_identification_grid.csv` | SUPPORTED_WITH_LIMITATION | Wording now states this is a range across defined parameter combinations, not one empirical time path. |
| Score remains stable while Evidence Support changes | Abstract; Sections 6–10 | Sensitivity, ablation, and core closure | `reports/development/research_core_closure.md`; `reliability_sensitivity.csv`; Figure 4 | SUPPORTED_WITH_LIMITATION | State that stability is caused by the current common-scaling structure and is not validity or causal evidence. |
| M0–M3 identify where support changes | Section 6, ablation paragraph | Core-closure ablation | `reports/development/ablation_results.csv` | SUPPORTED_WITH_LIMITATION | Context has no variation among readable Evidence; do not claim an independently estimated context effect. |
| P105/P108/P072/P035 are representative counterexamples | Section 6, counterexample paragraph | Record-level case extraction | `reports/development/counterexamples.csv` | SUPPORTED_WITH_LIMITATION | Label every case as AI_PROVISIONAL development evidence; do not generalize to the 140-record Pilot. |
| `NO_EFFECTIVE_EVIDENCE` is undefined, not zero | Sections 5, 6, 9 | Zero-weight guard and Figure 4 | `src/run_partial_identification.py`; `reports/development/core_figure_4_bounds_support.svg` | SUPPORTED | Preserve the undefined state in figures, Demo, and paper tables. |
| The development chain is reproducible | Section 7 | Six-step run and clean-clone rerun | `run_all.py`; `reports/submission/run_all_report.json` | SUPPORTED | Paper wording updated from the stale 5-step/29-check description to 6 steps/32 checks. |
| Formal AIV, ranking, or causal effect is available | Opening disclaimer; Section 8 | No supporting formal experiment; Gate is PENDING | `reports/annotation_gate_report.json`; `FORMAL_GATE_SWITCH.md` | UNSUPPORTED if stated | Keep `NOT_AVAILABLE_PENDING_FORMAL_GATE`; do not produce formal AIV or ranking before Gate PASS. |

## Submission decision

The development-only candidate is internally consistent after the wording
repairs. Formal-claim submission remains blocked by missing human R1/R2 and a
pending Gate. The current evidence supports a measurement-reliability
demonstration, not a formal AI incremental-value claim.
