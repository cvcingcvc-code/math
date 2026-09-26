# Sensitivity comparison

The complete machine-readable grid is in `sensitivity.csv` and `formulation_results.json`.

## Reliability perturbation

For each model, `R` was multiplied by `[0.0, 0.5, 0.8, 1.0, 1.2]` and clipped to `[0,1]`. The 54 records without observable Evidence remained missing under every model.

- **A** and **D** respond continuously to lower `R`; at `R=0`, their score is exactly zero while status remains `DEFINED` for an observed Raw Signal.
- **B** changes linearly but retains a high score at `R=0` (for Raw L6: 5.5 at λ=0.5 and 5.0 at λ=1.0). This is weak suppression of unsupported high Raw values.
- **C** converts low-R records to `ABSTAIN`; with the development slice's common `R=0.375`, baseline coverage is 0/16 at τ=0.5. This is conservative and exposes the cost in coverage.
- **D, γ=2** is most severe near zero; **D, γ=0.5** is most forgiving. All observed records remain defined, so reliability sensitivity changes magnitude rather than missingness.

## Component ablation

Removing the prompt component raises output for A, B, and D because all 16 observed records are prompt-induced. Removing context has no effect on this observed slice's factor pattern, except for C: without context penalty, `R` rises to 0.75 and all 16 records pass τ=0.5. This demonstrates that C's result is threshold-sensitive and that context has no independently identified variation in the current data.

## Stability interpretation

All non-gated variants preserve the Raw rank ordering in the observed slice (rank stability 1.0 wherever defined). This is expected because every observed record has the same `R=0.375`; it is not evidence that the formula is calibrated or predictive. The gated model has no accepted sample-in records at its preregistered threshold, so rank stability is undefined.
