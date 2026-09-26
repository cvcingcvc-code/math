# RESEARCH GATE STATUS

Generated from disk state on 2026-09-26.

## Current research stage

**S4 Pilot Annotation Gate — BLOCKED**. HUMAN_R1 is 0/70 valid (raw filled 1/70 but invalid and cleared), HUMAN_R2 is 0/70, and AI_ASSISTED is 70/70 DEVELOPMENT_ONLY. `reports/annotation_gate_report.json` remains PENDING; Formal AIV is unavailable.

## Stage assessment

| Stage | Status | Evidence / limitation |
|---|---|---|
| Reliability Model | PASS_WITH_LIMITATION | Reproducible model artifacts exist, but inputs are AI_PROVISIONAL and DEVELOPMENT_ONLY. |
| Raw vs Adjusted | PASS_WITH_LIMITATION | `raw_adjusted_metrics.csv`; current 16 readable records share a prompt-induced structure, so no broad causal interpretation. |
| Sensitivity | PASS_WITH_LIMITATION | `reliability_sensitivity.csv` covers lambda_prompt 0,.25,.50,.75,1 and context grid; finite development stress test only. |
| Ablation | PASS_WITH_LIMITATION | M0–M3 are present in `ablation_results.csv`; no predictive validation or formal labels. |
| Counterexamples | PASS_WITH_LIMITATION | Four record-level counterexamples are saved; no independent-evidence case exists in this slice. |
| Human R1/R2 Validation | BLOCKED | HUMAN_R1 = 0/70 VALID; HUMAN_R2 = 0/70; AI_ASSISTED 70/70 is not a formal substitute. |
| Formal Measurement Model | NOT_STARTED | Requires Gate PASS and formal inputs. |
| Formal AIV | BLOCKED | Explicitly `NOT_AVAILABLE_PENDING_FORMAL_GATE`. |
| Demo / Paper / PPT / Submission | PASS_WITH_LIMITATION | Development-only candidate materials exist; team ID, formal evidence, and some delivery packaging remain open. |

## Required next task

Have the same human complete R1, freeze and record its SHA-256, wait at least 24 hours, complete R2, then run `python src/run_s4_gate.py`. Do not run substitute AI labels or rerun frozen development experiments.

## Defer now

Formal AIV, student ranking, full formal annotation, CTQ/DHI freeze, PSM/DID, causal claims, and any new model that does not resolve the human Gate blocker.

## Submission Closure

**Not allowed** for a fully supported formal submission. A development-only candidate can be packaged with explicit limitations, but the formal Gate and AIV sections must remain blocked.
