# Alternative formulation definitions

Status: `DEVELOPMENT_ONLY`, input `AI_PROVISIONAL`, 70 records. This experiment is independent of the frozen production implementation and uses no human labels.

## Common objects

- Raw Signal `S_raw`: Student Evidence Bloom level L1–L6 mapped to 1–6. `NO_EVIDENCE` and `UNDETERMINED` have no numeric raw signal.
- Reliability `R`: the frozen development support weight, `confidence × (1 − 0.5 prompt_induced) × (1 − 0.5 context_truncated)`, bounded to `[0,1]`. It is a support weight, not a calibrated probability.
- Missing raw signal always returns `NO_EFFECTIVE_EVIDENCE`; no formulation fills a missing value.

## Registered structures

| Model | Formula / decision rule | Registered values | Intended behavior |
|---|---|---:|---|
| A | `S_adj = S_raw × R` | none | Fixed multiplicative control, no retuning. |
| B | `S_adj = S_raw − λ(1−R)` | λ = 0.5, 1.0 | Additive penalty with small predeclared grid. |
| C | If `R < τ`, `ABSTAIN`; otherwise `S_raw` | τ = 0.5 | Explicit low-support abstention. |
| D | `S_adj = S_raw × R^γ` | γ = 0.5, 1.0, 2.0 | Concave, linear, and convex reliability response. |

All structures receive the same sample-in, perturbation, ablation, missing-evidence, counterexample, extreme-R, stability, and external-transfer suites. No parameter was selected from an outcome.

## Evaluation meaning

There is no independent truth label or paired outcome in the current pilot. “Sample-in performance” therefore means preservation or modification of the observed Raw Signal, measured with coverage, output mean, RMSE to Raw, and rank stability. It is not accuracy and not causal performance.
