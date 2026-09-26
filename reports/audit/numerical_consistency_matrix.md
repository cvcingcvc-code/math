# Numerical Consistency Matrix

Audit date: 2026-09-26. Project root: `C:\Users\lin\Documents\Codex\2026-09-25\yu`.

Read-only audit artifact. No `src/`, `data/`, `paper/`, `reports/demo/`, `handoff/`, Human R1/R2, Formal Gate, model parameters, or thresholds were modified.

## Source of Truth

- Development input: `data/annotations/ai/pilot_ai_provisional.csv` (70 rows; `AI_PROVISIONAL / DEVELOPMENT_ONLY`).
- Independent numerical verification: `reports/verification/core_numbers_source_of_truth.json` and `reports/verification/independent_bounds_summary.json`.
- Unified derived artifact: `outputs/final_results.json`; Raw = M0 (no correction), Adjusted = M3 (confidence + prompt + context).
- `reports/demo/demo_payload.json` raw_metrics is theta0/M1 (lambda_prompt=0, lambda_context=0, r_medium=.75; 12/70), so it is not M0 raw (16/70).

## Matrix

| Metric | Source of Truth | Code value | Report value | Paper value | Demo value | Status | Notes |
|---|---|---|---|---|---|---|---|
| Total development records | data/annotations/ai/pilot_ai_provisional.csv; core_numbers_source_of_truth.json | 70 | 70 | 70 | 70 | CONSISTENT | Development denominator is 70; Canonical Pilot V1 remains 140. |
| Readable Evidence (L1-L6) | core_numbers_source_of_truth.json | 16 | 16 | 16 | 16 | CONSISTENT | Independent recomputation and displays agree. |
| NO_EVIDENCE | pilot_ai_provisional.csv | 19 | 19 | not separately reported | not separately reported | NOT_APPLICABLE | Paper and Demo use the aggregate 54 no-effective-evidence count. |
| UNDETERMINED | pilot_ai_provisional.csv | 35 | 35 | not separately reported | not separately reported | NOT_APPLICABLE | Paper and Demo use the aggregate 54 no-effective-evidence count. |
| NO_EFFECTIVE_EVIDENCE total | pilot_ai_provisional.csv; research_core_closure | 54 (=19+35) | 54 | 54 | 54 derived from 70-16 / status panel | CONSISTENT | Never encoded as score zero. |
| Parameter grid / defined / undefined | run_partial_identification.py; independent_bounds_summary.json | 693 / 660 / 33 | 693 / 660 / 33 | 693 / 33 (defined implicit) | 693 / 33 | CONSISTENT | 21 prompt values x 11 context values x 3 r_medium values. |
| ABL Raw / Adjusted | raw_adjusted_metrics.csv; final_results.json | 3.5625 / 3.5625 | 3.5625 / 3.5625 | 3.5625 / 3.5625 | 3.5625 | CONSISTENT | Descriptive score on the development slice. |
| HOT Raw / Adjusted | raw_adjusted_metrics.csv; final_results.json | 0.375 / 0.375 | 0.375 / 0.375 | 0.375 / 0.375 | 0.375 | CONSISTENT | - |
| Task/Evidence Gap Raw / Adjusted | raw_adjusted_metrics.csv; final_results.json | 1.125 / 1.125 | 1.125 / 1.125 | 1.125 / 1.125 | 1.125 in payload; not separately shown on main page | CONSISTENT | - |
| Raw effective weight (M0) | ablation_results.csv M0; final_results.json.raw_summary | 16.0 | 16.0 | 16.0 | 12.0 in demo_payload.raw_metrics | CONFLICT | Demo raw_metrics is confidence-only theta0/M1 (lambda_prompt=0, lambda_context=0, r_medium=.75), not M0 raw. |
| Adjusted effective weight (M3) | ablation_results.csv M3; final_results.json.adjusted_summary | 6.0 | 6.0 | 6.0 | 6.0 in payload stress C | CONSISTENT | M3 uses confidence + prompt + context. |
| Raw effective coverage (M0 = 16/70) | ablation_results.csv M0; final_results.json.raw_summary | 0.228571 | 0.228571 | 0.228571 | 0.171429 in demo_payload.raw_metrics | CONFLICT | Same Demo raw/baseline naming problem as the preceding row. |
| Adjusted effective coverage (M3 = 6/70) | ablation_results.csv M3; final_results.json.adjusted_summary | 0.085714 | 0.085714 | 0.085714 | 0.085714 in payload stress C | CONSISTENT | Denominator is all 70 development records. |
| Effective weight bounds | core_numbers_source_of_truth.json | 0.4-16.0 | 0.4-16.0 | 0.4-16.0 | 0.4-16.0 | CONSISTENT | - |
| Effective coverage bounds | core_numbers_source_of_truth.json | 0.005714-0.228571 | 0.005714-0.228571 | 0.0057-0.2286 | 0.005714-0.228571 | CONSISTENT | - |
| Reliability support | pilot_ai_provisional.csv; final_results.json | 16 readable; each readable R=0.375; M3 weight=6 | same | 16 -> 6 support | P105/P108 R=0.375; interactive support | CONSISTENT | R is a support weight, not a probability. |
| Sensitivity (15 what-if rows) | what_if_sensitivity.csv; final_results.json | 15 rows; no state flips | 15 rows; core conclusion unchanged | 15-row description | parameter controls / +/-20% note | CONSISTENT | Development parameter grid only; not calibration. |
| Ablation M0 -> M3 effective weight | ablation_results.csv | 16 -> 12 -> 6 -> 6 | 16 -> 12 -> 6 -> 6 | 16 -> 12 -> 6 -> 6 | 16 -> 12 -> 6 -> 6 | CONSISTENT | Context has no variation in readable rows. |
| Counterexamples P105/P108/P072/P035 | counterexamples.csv; final_results.json.counterexamples | P105/P108 numeric; P072/P035 no effective evidence | same | four IDs and explanations | main Demo numeric/status cards | CONFLICT | failure_cases/development_candidates.json sets all four raw_score and adjusted_score fields to null. |
| Failure case accuracy / true labels | accuracy_coverage_audit.json; failure_cases README | NOT_RUN (prediction and true_label missing) | NOT_SUPPORTED | development examples only | no formal outcome | NOT_RUN | Cannot claim correct/incorrect predictions or accuracy gain. |
| Formal Gate status | annotation_gate_report.json; FORMAL_GATE_SWITCH.md | PENDING; fail-closed | PENDING / NOT_RUN | NOT_RUN | NOT_RUN | CONSISTENT | No formal coefficient or AIV is generated. |
| Human R1 / R2 status | human worksheets; PROJECT_STATE.md | R1=0/70 VALID; R2=0/70 | same | PENDING_REAL_HUMAN_R1_R2 | not complete | CONSISTENT | AI_ASSISTED 70/70 does not substitute for Human R1/R2. |
| External Transfer historical core | transfer_validation.json | n=1698; threshold=.65; risk-coverage improvement=false | same | small structural transfer; no trading claim | not in education Demo | CONSISTENT | Auxiliary external validation only. |
| External information-missing gates | information_missing_validation.json; cross_strategy_validation.json | Gate1 SUPPORTED; Gate2 SUPPORTED; Gate3 NOT SUPPORTED | same | preliminary/weak partial support with failure boundary | not shown in main Demo | CONSISTENT | Do not present as universal generalization. |
| Binance live shadow | live_shadow_summary.json | 10 records; 0 evaluated; INSUFFICIENT_DATA | same | not used as education conclusion | not shown | CONSISTENT | Public-data shadow only. |
| Input identity / hash | pilot_ai_provisional.csv; pilot_ai_provisional_meta.json | 70 rows; SHA256 recorded in audit | source paths agree; most reports omit hash | final_results source path | payload source path | CONSISTENT | Identity is clear, but clean rebuild from Canonical Pilot is not available. |
| Primary parameters | build_final_artifact.py; final_results.json | lambda_prompt=.5; lambda_context=.5; r_medium=.75 | M3 same; bounds range explicit | formula consistent; defaults not always shown | UI defaults lambda_prompt=0, lambda_context=0, r_medium=.75 | CONFLICT | Demo default is theta0/M1 while artifact adjusted summary is M3. |
| Full Code -> Data -> Experiment -> Figure -> Demo -> Paper chain | run_all.py; builders; Demo/Paper | run_all has six steps and does not call final artifact/figure/Paper/Demo builders | 32/32 only covers development checks | Paper is separately generated/synced | main Demo is hard-coded; package Demo is a separate dynamic implementation | NOT_RUN | Core experiment chain is reproducible; full derivative chain is not proven by one entry point. |
| Submission package vs current Paper/Demo | outputs/final_results.json; current paper/ and reports/demo/; outputs/submission_package_development_only/ | current artifact and current files | package contains older generated Paper/Demo | current files are newer | package Demo uses its own demo_payload and older UI | STALE | Package files are not byte-identical to current Paper/Demo; package payload is numerically aligned but presentation/source wiring is older. |
| Git provenance receipt | current HEAD; experiment_runner_consistency.json | 667ecf7e25226366014687aa0ff77cbd80d8df34 | old receipt records a54a98ecf1d672efcd8a866bd924fbb803e0df06 | no embedded HEAD | no embedded HEAD | STALE | Old receipt cannot certify current HEAD. |
| Paper inventory receipt | current paper directory; paper_numeric_consistency.md | paper/*.md/.html/.pdf exist | old audit says paper directory absent | current files exist | - | STALE | Numeric audit itself is stale about file inventory. |
| Provisional label generation provenance | pilot_ai_provisional_meta.json; provenance_separation_audit.json | metadata only; no generation script or row-level generation log | audit records no reproducible script | Paper cites result file only | Demo cites payload only | NOT_RUN | Can recompute from frozen 70-row file, not clean-rebuild from Canonical Pilot. |
| Runtime vs requirements | requirements.txt; current runtime | Python 3.14.2 / pandas 3.0.1 / numpy 2.4.1 | requirements says Python 3.13 / pandas 3.0.6 / numpy 2.5.3 | not stated | not stated | NOT_RUN | Clean run should use the declared environment and record versions. |

## Status counts

- `CONSISTENT`: 20 rows
- `STALE`: 3 rows
- `CONFLICT`: 4 rows
- `NOT_APPLICABLE`: 2 rows
- `NOT_RUN`: 4 rows

## Highest-risk evidence

1. **Demo raw/baseline semantics (HIGH):** `reports/demo/demo_payload.json:L104-L114` reports 12.0/0.171428 for raw_metrics/baseline_support, while `outputs/final_results.json:L20-L40` reports M0 Raw 16.0/0.228571.
2. **Failure-case export (HIGH):** `reports/failure_cases/development_candidates.json:L9-L44` writes null raw/adjusted values for P105, P108, P072, and P035; the core counterexample CSV, final artifact, and Paper/Demo have numeric values for P105/P108.
3. **Full-chain provenance (HIGH):** `run_all.py:L37-L45` does not call final artifact/figure/Paper/Demo builders. `reports/demo/index.html:L11` is a source comment; the main page has no `fetch(`.
4. **Input-generation traceability (HIGH):** `reports/development/provenance_separation_audit.json:L105` records that no reproducible generation script was found; `pilot_ai_provisional_meta.json:L12` contains metadata only.

## Git / handoff snapshot

- HEAD: `667ecf7e25226366014687aa0ff77cbd80d8df34`; branch: `master`.
- The audit observed a non-clean worktree: 11 tracked modified paths and 235 untracked entries (including the pre-existing and newly written audit artifacts).
- `handoff/PROJECT_NOW.md`: HUMAN_R1=0/70 VALID; HUMAN_R2=0/70; Formal Gate=NOT_RUN.
- `handoff/PROJECT_STATE.md`: Canonical Pilot V1=140; Gate core sample=70; development input=70 provisional rows.
- `handoff/NEXT_TASK.md`: complete real R1 -> R2 test-retest, then run `python src/run_s4_gate.py`.
- `reports/annotation_gate_report.json:L2-L25`: PENDING; no formal reliability coefficient.

## Reproducibility assessment

### Reproduced

`python run_all.py` has six exit-code-0 steps; `reports/submission/run_all_report.json` reports 32/32 checks; independent recomputation reproduces 70/16/19/35, 693/660/33, ABL/HOT/Gap, and weight/coverage bounds.

### Not closed

- Provisional CSV generation has no executable rebuild script; Canonical data -> provisional data is broken.
- `run_all.py` does not generate the current final artifact, five current figures, current Paper, or current Demo.
- There are two Demo implementations: the main hard-coded `reports/demo/index.html` and a separate package Demo that dynamically reads a payload.
- The old experiment-runner receipt has a different HEAD, and the old paper numeric receipt says the paper directory is absent.
- The current runtime differs from the declared requirements verification combination.

## Seeds, parameters, inputs, outputs

- Core development chain is deterministic and has no random sampling dependency.
- Worksheet seeds: R1=`20260925` (`src/build_annotation_worksheets.py:L32`); R2=`20260926` (`src/build_retest_worksheet.py:L35`).
- Gate synthetic self-test uses NumPy seed 11 (`src/annotation_gate_report.py:L244`); it is not formal Gate data.
- Bounds: lambda_prompt 0..1 step .05; lambda_context 0..1 step .10; r_medium={.5,.75,1.0}.
- Adjusted default: lambda_prompt=.5; lambda_context=.5; r_medium=.75; confidence high=1, medium=.75, low=.5.
- Core outputs: `reports/development/`, `reports/submission/`, `reports/verification/`; final artifact: `outputs/final_results.json`.
- Final artifact does not carry input SHA256, Git HEAD, environment versions, or a Paper/Demo manifest.

## Minimal clean-environment chain

1. `cd C:\Users\lin\Documents\Codex\2026-09-25\yu`
2. `py -3.13 -m venv .venv`
3. `.venv\Scripts\python -m pip install --only-binary=:all: -r requirements.txt`
4. `.venv\Scripts\python run_all.py`
5. Verify `reports/submission/run_all_report.json`: `result=PASS`, six steps, 32/32 checks.
6. Inspect independent bounds, Raw/Adjusted, Ablation, and Counterexamples.
7. `.venv\Scripts\python run_all.py --mode formal` is an expected fail-closed check while the Gate is not PASS; do not use it to create formal numbers.
8. Separately run the existing final artifact/figure builders and verify that Paper/Demo use the same `outputs/final_results.json`; this is currently outside `run_all.py`.

## Minimal repair suggestions for MAIN_RESEARCH / CONVERGENCE

1. Unify Demo names for theta0/M1 (12/70) and Raw/M0 (16/70); if both remain, label both explicitly.
2. Repair or quarantine null outputs in `reports/failure_cases/development_candidates.json`.
3. Add final artifact, figure, Paper, and Demo steps to the documented reproducibility chain, or record them as post-processing with an input hash.
4. Record input SHA256, Git HEAD, Python/package versions, and output manifest; do not change data, thresholds, or model.
5. Regenerate the paper numeric audit; mark the old paper-inventory claim stale.
