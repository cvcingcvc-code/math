# PROJECT NOW

## last updated
2026-09-26

## current Git HEAD
667ecf7e25226366014687aa0ff77cbd80d8df34

## current phase
VISUAL_EVIDENCE_CONVERGENCE = DONE / UI_POLISH_PENDING

## completed stages
Development measurement closure; model vocabulary convergence; judge-facing story, overview, component table, validation story, QA, script; education-only Demo rewrite; final F1–F6 visual evidence convergence.

## current formal status
HUMAN_R1=0/70 VALID; HUMAN_R2=0/70; Formal Gate=NOT_RUN; AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED.

## frozen / do not redo
Do not change model parameters, R1/R2, thresholds, research direction, or PPT. Do not invent baseline, truth, accuracy, or causal increment.

## current main goal
Make Model → Demo → Paper → Judge Defense use one evidence-aware evaluation vocabulary.

## execution order
1. Keep canonical docs and demo consistent. 2. Owner completes frozen HUMAN R1/R2. 3. Run Gate. 4. Only after PASS replace development values with formal values.

## current blockers
Real human R1/R2 labels are missing; no paired Outcome_AI/Outcome_baseline.

## top 10 competition risks
1 topic fit; 2 data support; 3 model necessity; 4 mathematical closure; 5 validation strength; 6 paper density; 7 figure interpretation; 8 demo/paper consistency; 9 PPT avoiding development log; 10 one strong core result.

## authoritative files
`docs/metric_dictionary.md`, `docs/claim_boundary.md`, `docs/model_presentation/final_model_overview.md`, `outputs/final_results.json`, `reports/demo/index.html`, `paper/submission_candidate.md`, `reports/model_paper_consistency_audit.md`.

## final visual state
`VISUAL_EVIDENCE_CONVERGENCE = DONE`; final F1–F6 are under `reports/visual_evidence/final/`. Paper main chain uses F1–F5, F6 is external structural transfer/limitations, and Demo home uses F1–F3.
## Robustness / perturbation round (2026-09-26)
- Parameter perturbation, evidence perturbation, counterfactual, and fixed external transfer artifacts generated.
- Education outputs remain DEVELOPMENT_ONLY; external finance outputs remain EXTERNAL_TRANSFER.
- No human labels, thresholds, frozen parameters, or Formal Gate rules changed.
- run_all.py 32/32 PASS; development submission consistency PASS.
- Unique remaining formal blocker is real HUMAN_R1/R2 and Formal Gate.
