# CURRENT HANDOFF

## PROJECT ROOT
`C:\Users\lin\Documents\Codex\2026-09-25\yu`

## CURRENT HEAD / BRANCH / GIT STATUS
- HEAD: `a54a98ecf1d672efcd8a866bd924fbb803e0df06`
- Branch: `master`
- Status: untracked user-facing/non-core files remain (`paper/submission_candidate.html/.pdf`, selected audit SVG/JSON/CSV files, `slides/`). Do not overwrite or delete them.

## CURRENT RESEARCH STAGE
S4 Pilot Annotation Gate — `BLOCKED_BY_HUMAN_ANNOTATION`.

## CURRENT DELIVERY STAGE
Development-only submission candidate is reproducible; formal Gate, formal AIV, team-ID naming, and final packaging remain open.

## COMPLETED
Reliability model, Raw vs Adjusted, sensitivity, M0–M3 ablation, counterexamples, core closure, independent numerical verification, and development paper/demo artifacts.

## IN_PROGRESS
Human R1 then 24+ hour wait then R2; afterward run `python src/run_s4_gate.py`.

## BLOCKED
No real human labels; `reports/annotation_gate_report.json` is PENDING. Formal AIV and ranking are unavailable.

## DEFERRED
Formal measurement/AIV, causal models, full annotation, and any new model unrelated to the Gate blocker.

## CORE NUMBERS
Development-only: 70 records, 16 readable Evidence; ABL/HOT/Gap = 3.5625/0.375/1.125; raw effective coverage 16/70, adjusted example coverage 6/70.

## MODEL DEFINITION
`w_i = I(observable_i) × c_i × (1−λ_prompt prompt_i) × (1−λ_context context_i)`; zero support is `NO_EFFECTIVE_EVIDENCE`, not 0.

## CURRENT DATA IDENTITY
`data/annotations/ai/pilot_ai_provisional.csv`; `AI_PROVISIONAL`, `DEVELOPMENT_ONLY`, `formal_gate_eligible=false`. Canonical Pilot is `data/processed/pilot_sample.csv`, N=140.

## FORMAL GATE STATUS
PENDING; threshold file is preregistered and immutable. Formal mode must be rejected until Gate PASS.

## LATEST OUTPUTS
`reports/development/research_core_closure.*`, `raw_adjusted_metrics.csv`, `ablation_results.csv`, `counterexamples.csv`, `reports/RESEARCH_GATE_STATUS.md`, and development submission CSVs.

## P0/P1 ISSUES
P0: human R1/R2 missing. P1: team-ID naming/package completion and paper claim audit.

## NEXT 3 ACTIONS
1. Obtain real R1.
2. After 24+ hours obtain R2 and run Gate.
3. If Gate PASS, regenerate formal artifacts; otherwise narrow claims and keep development status.

## FILES NEXT WINDOW MUST READ
`AGENTS.md`; `handoff/PROJECT_STATE.md`; `handoff/DECISIONS.md`; `handoff/NEXT_TASK.md`; `handoff/ARTIFACT_INDEX.md`; `handoff/CURRENT_HANDOFF.md`; `FORMAL_GATE_SWITCH.md`; `reports/RESEARCH_GATE_STATUS.md`.

## DO NOT REDO
Do not rerun completed development experiments, use old 56-row Pilot data, fabricate human labels, alter thresholds, or claim Formal AIV.

## GATE RUNNER SAFETY
`src/run_s4_gate.py` now preserves existing R1/R2 files, uses the frozen single-annotator test-retest pair by default, and calls the test-retest wrapper for reporting. Empty labels correctly remain PENDING; the current run passed 21/21 integrity checks.

## NEW WINDOW START (5–10 lines)
Read `AGENTS.md`, `handoff/CURRENT_HANDOFF.md`, and current Git HEAD/status. Restore disk state. Treat marked DONE steps as complete. Continue the first unfinished P0/P1/main-line task. Keep development and formal inputs separate. Do not rerun items under DO NOT REDO. Do not bypass the Formal Gate.
