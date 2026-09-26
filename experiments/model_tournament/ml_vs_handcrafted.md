# ML challengers versus the handcrafted Evidence Reliability model

## Decision status

`INSUFFICIENT_FOR_STRONG_ML_CLAIM` · `DEVELOPMENT_ONLY` · `NO_SINGLE_DOMINANT_MODEL`

The three simple models ran on 70 AI-provisional records. Their target was readability of the provisional Evidence label, not a validated outcome. The handcrafted model computes a reliability-weighted score after an Evidence label exists, so it cannot be treated as a competing pre-label classifier.

## Predictive development evidence

| Model | Accuracy | Balanced accuracy | F1 | ROC-AUC | Brier | ROC-AUC SD | Evidence status |
|---|---:|---:|---:|---:|---:|---:|---|
| Logistic Regression | 0.876 | 0.863 | 0.758 | 0.954 | 0.091 | 0.045 | development only |
| Shallow Decision Tree | 0.919 | 0.901 | 0.815 | 0.914 | 0.073 | 0.107 | development only |
| Random Forest | 0.922 | 0.894 | 0.823 | 0.928 | 0.124 | 0.086 | exploratory only |

Values are means over 100 folds from repeated 4-fold CV. The high apparent fit is not a strong ML claim: there are only 16 positive targets, folds are resamples of the same 70 records, and the target is AI provisional.

## Robustness and transfer

- With 20% feature missingness, balanced accuracy fell to 0.795 (Logistic), 0.792 (Tree), and 0.716 (RF).
- With 40% missingness, it fell to 0.727, 0.727, and 0.701 respectively. Random Forest degraded fastest from its clean robustness run.
- Leave-one-semester transfer was available only as an internal cohort stress test, not external validation. Balanced accuracy was 0.848/0.938 for Logistic, 0.929/0.918 for Tree, and 0.902/0.688 for RF in the two directions. The RF reversal is an overfitting warning.
- True external transfer is unavailable: the unlabeled remaining 70 records and finance artifacts do not provide a matched education outcome.

## Handcrafted model behavior

On the current development slice, the handcrafted formula gives ABL `3.5625`, HOT `0.375`, and Gap `1.125`; it reduces raw observable weight `16` to effective weight `6` and effective coverage `6/70 = 0.085714`. It returns `NO_EFFECTIVE_EVIDENCE` for 54 undetermined/no-evidence records. These are support accounting and abstention behaviors, not classification accuracy.

All 16 readable rows share the same provisional pattern (prompt-induced, context available, medium confidence), so normalized score equality across raw and adjusted forms is a common-scaling artifact. The current data cannot show that multiplicative reliability is predictively better than a simpler rule or linear correction.

## What the evidence supports

- Simple models can reproduce a development readability proxy from pre-label metadata, with substantial missingness degradation.
- The shallow tree has the best mean balanced accuracy in this proxy task; the RF has the highest raw accuracy/F1 but weaker calibration and unstable cohort transfer.
- The handcrafted model's real advantage is explicit support decomposition and fail-closed missing Evidence handling. Its empirical predictive superiority is not demonstrated.
- ML is better suited to exploratory pre-label screening; it is less interpretable and can output confident predictions when evidence is absent unless an abstention policy is added.

## Failure cases and paper boundary

High-confidence disagreements include P051 (all models tend to predict readable while the provisional target is not) and P024 (models tend to predict not readable while the provisional target is readable). These are disagreements with an AI provisional target, not confirmed human-label errors. Coefficients/rules/feature importance are associations, not causes.

Paper-safe wording: “In a development-only proxy task with 16 positive AI-provisional labels, simple models were feasible but unstable under missingness and cohort transfer; no formal accuracy or model superiority claim was made.” Do not report these numbers as formal validation, AIV, causal effect, or generalization to all 140 records.

## Current defect check

No new material defect in the handcrafted arithmetic was found. The challenger exposes a model-selection limitation: the present readable slice lacks heterogeneous reliability-factor combinations, so the main formula's extra complexity is not empirically identifiable against a simpler linear or rule baseline.
