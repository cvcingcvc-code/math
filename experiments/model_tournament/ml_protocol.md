# Simple data-driven challenger protocol

**Status:** `DEVELOPMENT_ONLY` · `INSUFFICIENT_FOR_STRONG_ML_CLAIM`

## Question

Can a simple model predict whether a record will receive a readable Student Evidence label (`L1`–`L6`) from fields available before the provisional evidence label? This is an auxiliary development task for comparison. It does not estimate AIV, learning gain, or causal AI effect.

## Data identity and gate

- Input: `data/annotations/ai/pilot_ai_provisional.csv`, 70 unique Gate records.
- Target: `student_evidence_bloom in {L1,...,L6}`; 16 positives and 54 `NO_EVIDENCE/UNDETERMINED` records.
- Target source is `AI_PROVISIONAL / DEVELOPMENT_ONLY`; HUMAN_R1 = 0/70 valid, HUMAN_R2 = 0/70, Formal Gate = `NOT_RUN`.
- The other 70 Canonical Pilot records have no matching labels and cannot be used as a scored holdout.
- No true Development/Validation/Holdout/External three-way split exists for this target. Repeated stratified 4-fold CV (25 repeats) is development evidence only.

## Models

1. Logistic Regression, class-balanced, `C=1`, no search.
2. Shallow Decision Tree, class-balanced, `max_depth=2`, `min_samples_leaf=5`.
3. Random Forest, 100 trees, `max_depth=3`, `min_samples_leaf=4`, class-balanced; exploratory because the positive sample is only 16.

Features were restricted to pre-label fields: text length, agent/speaker confidence, context truncation, semester, length stratum, question form, surface Bloom cue, and path case. Label-derived fields (`student_evidence_bloom`, confidence, prompt/context attribution, content relation, and task Bloom) were excluded.

## Evaluation

Reported metrics are accuracy, balanced accuracy, F1, ROC-AUC, Brier score and log loss. Stability uses fold standard deviation, semester leave-one-cohort transfer, and 20%/40% test-time feature missingness. Coefficients, shallow rules and RF importance are associational only. External outcome transfer is `NOT_EVALUABLE` because no independent labeled dataset exists.

## Handcrafted comparison boundary

The current Evidence Reliability model is a post-label measurement transform (`w_i` applied after Evidence is observed). It is not a pre-label predictor. Direct predictive superiority between that transform and these classifiers is therefore unidentified. The existing handcrafted score, support, abstention and sensitivity results are reported alongside the ML metrics without pretending they are the same task.

## Reproduction

```text
py experiments/model_tournament/run_ml_tournament.py
```

Outputs include the input/claim metadata, all fold metrics, interpretation artifacts, and failure cases. No human annotation files are read as labels and no project model or threshold is changed.
