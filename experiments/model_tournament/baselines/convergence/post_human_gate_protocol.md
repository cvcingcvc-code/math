# Post-Human-Gate Baseline Re-test Protocol

## Purpose and stop condition

This file is a protocol only. It does not execute a Formal Gate, calculate a Human Truth metric, alter a threshold, or overwrite development results. Start only after the frozen 70-record Gate slice has valid HUMAN_R1 and HUMAN_R2 under the existing test–retest design and the Formal Gate has reached its declared status. If the Gate fails or required labels are invalid, report that status and do not silently treat AI provisional labels as truth.

## Frozen comparison set

Use exactly the same 70 core records and the same record IDs as the existing tournament. Preserve the original input identity, row order/key mapping, missingness codes, and declared analysis denominator. Join the validated human labels by the frozen key, never by row position alone. Keep all four candidates unchanged:

1. Current Evidence Reliability Model: `w=I(obs)c(1−0.5p)(1−0.5t)`.
2. Raw-only: `w=I(obs)`.
3. Simple Linear Weighted: `w=I(obs) clip(c−0.25p−0.25t,0,1)`.
4. Simple Rule / Threshold: the fixed L4/confidence/risk rule from the tournament.

Also rerun any challenger already present in the parent tournament using its frozen formula. Do not add a challenger, tune a coefficient, select a threshold from the human labels, or change the main model while measuring it.

## Required inputs and audit record

Record the Git HEAD, input paths, SHA-256 hashes, exact 70-record key list, human label schema/version, Gate decision, and whether the human labels are valid for each metric. Keep AI provisional fields separate from HUMAN_R1/R2 fields. Report invalid, ambiguous, or unresolved human labels using the frozen Gate rules; do not impute them without a preregistered rule.

## Metrics to calculate after the Gate

Calculate each metric for Current, Raw-only, Linear, Rule, and existing challengers on the same rows. Use the same outcome definition and positive class for every candidate. Report point estimates, numerator/denominator, and undefined status when a denominator is zero.

| Metric | Protocol |
|---|---|
| Accuracy | Exact model decision versus the validated human target on eligible rows. If the target is ordinal/multiclass, report the predeclared multiclass definition rather than collapsing labels after seeing results. |
| Sensitivity / Recall | True positive rate for the predeclared positive/support class; state the class and denominator. Do not call coverage a recall. |
| Specificity | True negative rate when a negative/unsupported class is formally defined and has eligible labels; otherwise mark not applicable. |
| Precision | Positive predictive value when the positive class and eligible denominators are defined; otherwise mark not applicable. |
| Coverage | Accepted/defined decisions divided by all 70 records; publish the denominator and separate effective coverage `Σw/70`. |
| Abstention rate | `NO_EFFECTIVE_EVIDENCE` or other declared abstentions divided by all eligible records. Report it together with coverage and error. |
| Risk–coverage | At the fixed declared decision rule, report error among accepted rows versus coverage. If a curve is authorized, use only preregistered fixed thresholds and do not optimize on the Gate labels. |
| Calibration | Only if a validated target and a predeclared probability mapping exist. Current `Reliability` is not a calibrated probability; do not apply Brier/ECE language to raw weights without that mapping. |
| Failure-case agreement | Revisit P108, P105, P072, and P035 with human labels. Report exact agreement, disagreement type, and whether the case was eligible; do not call an AI-provisional disagreement a model error without the human target. |

Also report the existing descriptive metrics (Aggregate Evidence Score, HOT, Task–Evidence Gap, Effective Weight, and effective coverage) unchanged, so the post-Gate table remains comparable to `../baseline_results.csv`.

## Reporting and comparison rules

- Put all four candidates in one table with the same rows, target, exclusions, and denominators.
- Report uncertainty or exact counts appropriate to the Gate sample; do not rank candidates from a single metric without the preregistered comparison rule.
- Keep `NO_EFFECTIVE_EVIDENCE` distinct from a negative human label. Abstention is a decision state, not a zero score.
- If a model has no eligible positive or negative labels, mark the relevant metric undefined instead of manufacturing a value.
- Preserve the development table as an historical artifact. Write a new post-Gate result file rather than overwriting `../baseline_results.csv` or `../baseline_results.json`.
- Any claim about generalization, formal AIV, causal AI effect, or student ranking remains outside this protocol unless separately authorized by the frozen research design.

## Required decision record

The post-Gate report must answer separately: (1) whether adding a Reliability layer changes human-target agreement, abstention quality, or risk–coverage under the frozen protocol; and (2) whether the multiplicative form differs materially from the linear challenger under the same target and sample. If the linear challenger is not lower on a preregistered metric, record that result without changing the main model retrospectively.
