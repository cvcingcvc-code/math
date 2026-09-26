# Model Tournament Protocol

**Status:** FROZEN BEFORE CANDIDATE FINAL-RESULT REVIEW  
**Freeze date:** 2026-09-26  
**Project root:** `C:\Users\lin\Documents\Codex\2026-09-25\yu`  
**Protocol owner:** independent evaluator (`MODEL_TOURNAMENT_EVALUATOR`)

## 1. Purpose and non-negotiable rules

This tournament compares candidate measurement models under one predeclared evaluation contract. The evaluator does not modify the main model, manufacture missing results, or treat development-only outputs as formal evidence.

A candidate is evaluated only on artifacts that identify input data, executable code/configuration, split policy, perturbation/missingness/counterexample/transfer manifests, parameter selection history, and status. The canonical comparison unit is the same record-level task and aggregation rule. If a candidate cannot consume the common input without a documented adapter, it is `PENDING` rather than receiving an easier substitute.

Current project boundaries are binding: formal human labels and Formal Gate outputs are not available. AI-provisional/development results are development evidence only and must never be relabeled as formal validation.

## 2. Common evaluation harness

Unless a candidate-specific preregistration already exists, all candidates use:

1. **Primary data:** `data/processed/pilot_sample.csv` (N=140) for development comparison; the Gate subset (N=70) only with the same frozen subset manifest for every candidate.
2. **Labels:** the same frozen label source for the run. At present this is AI-provisional/development-only evidence; no candidate may claim HUMAN_R1/R2 or Formal Gate support.
3. **Splits:** one fixed record-level split manifest, with no record in more than one split. Grouped or temporal splits must be shared and declared before scoring.
4. **Perturbations:** the same seeded operators and severities: evidence deletion, confidence downgrade, admissible prompt/context attribution flips, irrelevant-text addition, ordering jitter within allowed session proxies, and agent-type unknown masking.
5. **Missing data:** the same masks and rates (at minimum 10%, 25%, 50%, MCAR-like and observed-risk masks), with no holdout-tuned imputation.
6. **Counterexamples:** the same frozen record IDs and synthetic stress cases, scored without candidate-specific filtering.
7. **External transfer:** the same predeclared external dataset and feature schema. If unavailable or outcome-free, the dimension is `PENDING`, not zero.
8. **Runtime accounting:** the same hardware/runtime convention; complexity includes fitted parameters, tuning evaluations, inference latency, and required dependencies.

Every output includes a machine-readable manifest with dataset hashes, code revision, seeds, split IDs, parameter history, and status.

## 3. Dimensions and scoring rules

Scores are recorded as raw measurements plus an ordinal status. No single weighted total determines the winner.

### 3.1 Fit / Main Metric

- **How measured:** On the frozen holdout, report the preregistered task metric: continuous tasks report MAE/RMSE and calibration; ordinal/categorical tasks report macro-F1/balanced accuracy and ordinal agreement; partial-identification models report interval coverage and width alongside the declared score. Include confidence or bootstrap intervals.
- **Data source:** Common primary data and frozen holdout labels; formal labels only after Formal Gate PASS.
- **Direction:** Higher is better for agreement, balanced accuracy, calibration quality, and coverage; lower is better for MAE/RMSE and interval width conditional on coverage.
- **Failure:** Missing holdout result, leakage, post-hoc metric choice, or no improvement over a declared trivial baseline within uncertainty while making stronger claims.

### 3.2 Robustness

- **How measured:** Recompute the main metric over the common perturbation suite; report absolute/relative degradation, worst-case degradation, and rank stability.
- **Data source:** Same holdout and frozen perturbation manifest.
- **Direction:** Higher retained metric and rank stability; lower degradation.
- **Failure:** Undefined behavior, catastrophic degradation under a plausible perturbation, or unequal perturbations.

### 3.3 Sensitivity

- **How measured:** Vary every declared parameter over the common grid; report elasticity, sign/rank reversals, and valid-grid fraction. Parameters are fixed before holdout review.
- **Data source:** Common data, frozen grid, and preregistration.
- **Direction:** Higher valid-grid coverage and conclusion stability; lower unintended elasticity and reversal rate.
- **Failure:** Hidden parameters, post-hoc grid selection, unexplained discontinuity, or small plausible changes reversing conclusions without warning.

### 3.4 Ablation Behavior

- **How measured:** Remove components one at a time under shared definitions (raw-only, reliability/confidence, prompt/context correction, and any predeclared candidate component). Report metric deltas and expected-direction behavior.
- **Data source:** Same records, split, and labels; only the named component changes.
- **Direction:** Higher when necessary components improve the declared metric or known failure; lower for unexplained dependence on one component.
- **Failure:** Irreproducible ablation, claimed component unused, theoretically required component has no effect, or holdout-tuned component changes.

### 3.5 Missing Evidence Handling

- **How measured:** Score the common missingness suite. Report valid-output coverage, abstention/`NO_EFFECTIVE_EVIDENCE` rate, conditional error/calibration, and whether missingness is treated as negative evidence.
- **Data source:** Frozen masks and observed-data provenance.
- **Direction:** Higher calibrated coverage, valid abstention, and correct uncertainty; lower unsupported confident outputs and missingness error.
- **Failure:** Silent row deletion, holdout-label imputation, unjustified missing-as-zero, or confident scoring without evidence support.

### 3.6 Counterexample Safety

- **How measured:** Run all candidates on the frozen set: contradiction, future-content leakage, unknown-agent, prompt-only, no-evidence, and adversarially plausible synthetic cases. Report unsafe decisions, abstention correctness, and trace.
- **Data source:** Versioned counterexample manifest and source spans.
- **Direction:** Higher safe handling and correct abstention; lower unsafe decisions and unsupported claims.
- **Failure:** Known counterexample yields unjustified confidence, future content is used as past evidence, or failing cases are hidden.

### 3.7 Parameter Stability

- **How measured:** Refit/rerun across bootstrap samples, fixed resamples, temporal slices, and allowed perturbations. Report medians, interval widths, sign consistency, and range adherence.
- **Data source:** Common data and frozen resampling/slice manifest.
- **Direction:** Higher sign/range consistency and reproducibility; lower scale-normalized dispersion.
- **Failure:** Large unexplained drift, search-driven boundary hits, unstable signs, or unequal selection budgets.

### 3.8 External Transfer

- **How measured:** Apply the frozen candidate without retraining, or with only predeclared calibration, to the same external data. Report schema compatibility, performance/calibration, missingness behavior, and internal-to-external degradation.
- **Data source:** One common external dataset and frozen feature map. Outcome-free transfer reports execution only and remains pending for outcome validation.
- **Direction:** Higher valid execution, calibration, and retained conclusions; lower degradation and unsupported extrapolation.
- **Failure:** External data selected after results, undocumented candidate-specific preprocessing, or transfer claims without outcomes.

### 3.9 Interpretability

- **How measured:** An independent reviewer traces a fixed record sample to source evidence, contributions, uncertainty, and abstention reason. Report traceability, faithfulness checks, and reviewer agreement.
- **Data source:** Common records, source spans, explanation artifacts, and blinded review form.
- **Direction:** Higher traceability, faithfulness, and agreement; lower unexplained output proportion.
- **Failure:** Evidence used cannot be identified, explanation contradicts computation, or interpretation requires unavailable labels.

### 3.10 Complexity

- **How measured:** Record parameter count, effective degrees of freedom where available, tuning/search evaluations, runtime footprint, inference latency, and human/data prerequisites.
- **Data source:** Reproducibility manifest, code revision, configuration history, and runtime logs.
- **Direction:** Lower complexity at comparable validated performance; added complexity is justified only by documented safety, robustness, or transfer gain.
- **Failure:** Undocumented search, greater complexity without validated benefit, or unreproducible dependencies.

## 4. Anti-bias and selection-bias audit

For every candidate record: holdout peeking; selective reporting; number of variants/search burden; validation leakage; unequal data difficulty; incumbent favoritism; and development/formal status inflation. Dataset hashes, row IDs, masks, and label versions must match. Any unresolved violation makes the affected dimension `FAILED_EVIDENCE` and blocks a model-selection claim.

## 5. Decision rule without a single total score

The final report must provide a raw metric matrix with uncertainty and provenance; Pareto analysis over fit, robustness, missing-evidence safety, transfer, interpretability, and complexity; strengths, weaknesses, failure modes, operating conditions; and all pending dimensions.

If one candidate is non-dominated and has no unresolved safety or evidence failure, it may be preferred for the stated use case with its trade-offs. If candidates trade off dimensions, report `NO_SINGLE_DOMINANT_MODEL` and state each operating range. “Highest accuracy” alone is never sufficient. Better fit cannot compensate for unsafe missing-evidence or counterexample behavior without a restricted-use condition.

## 6. Required result states

- `PASS`: reproducible evidence meets the preregistered requirement.
- `PASS_WITH_LIMITATION`: reproducible evidence is materially bounded.
- `PENDING`: result not produced or common input unavailable.
- `FAILED_EVIDENCE`: missing provenance, common-harness violation, leakage, or safety-gate failure.

No result may be fabricated or imputed to replace `PENDING`.

## 7. Freeze record

This file is the frozen protocol. Any amendment requires a new version, a dated reason, and a statement that the amendment was made before or after affected results were viewed. Existing scores are not silently recomputed under changed rules.
