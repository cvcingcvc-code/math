# Claim boundary and crosscheck

Status: current values are `DEVELOPMENT_ONLY`; Human R1/R2 and Formal Gate are `WAITING_FOR_HUMAN`.

## Supported within the current evidence

- Observable Student Evidence records have different levels of evidence support.
- The transparent reliability weighting changes effective support and can yield `NO_EFFECTIVE_EVIDENCE`.
- In the current provisional slice, score stability and evidence-support stability can diverge under the declared sensitivity grid.
- Low-support or conflicting records can be routed to `ABSTAIN`, provided coverage and abstention are reported together.
- Sensitivity and ablation describe behavior of the frozen formula under stated assumptions.
- A future Human Gate can test annotation test-retest reliability; it is not inter-rater reliability under the frozen design.

## Not supported

- `Delta_raw = Outcome_AI - Outcome_baseline` for the current pilot: **NOT_SUPPORTED**.
- Any claim that AI increased true learning ability, caused learning improvement, or produced a long-term learning gain.
- A formal AI Increment, formal AIV, student ranking, policy effect, or general education effect.
- Calibrated probabilistic meaning for `R`; current reliability weights are not empirically calibrated probabilities.
- Accuracy improvement from abstention without paired accuracy/error, coverage, and abstention reporting.
- Generalization from the 70-record Gate sample to all 140 Pilot records.
- Financial transfer as evidence of educational causal validity; it remains secondary/appendix structural validation.

## Language crosscheck targets

Any paper/report sentence using “AI 增量”, “提升能力”, “学习增益”, “因果效果”, “正式 AIV”, or “准确率提升” must be qualified by the boundary above. Existing development numbers must retain `AI_PROVISIONAL` and `DEVELOPMENT_ONLY` labels until Gate PASS.
