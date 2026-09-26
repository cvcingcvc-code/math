# Core Model Comparison Table

**Status:** `DEVELOPMENT_ONLY`; no ranking or champion designation.

| Candidate | Research-question alignment | Interpretability | Missing-evidence behavior | Robustness / sensitivity | Additional assumptions / complexity |
|---|---|---|---|---|---|
| Current Evidence Reliability Model | Strong: separates observed performance from support quality | Strong: component-wise, auditable | `NO_EFFECTIVE_EVIDENCE` when support is absent; weak support attenuates contribution | Development sensitivity/ablation support structural checks; formal validation pending | Low structural complexity; weights are assumptions, not calibrated probabilities |
| Raw-only Baseline | Partial: observed signal only | Very high simplicity | Does not distinguish unsupported evidence | Fixed reference, not a reliability stress test | Lowest complexity; omits support modeling |
| Rule-based Gated Baseline | Strong for abstention-oriented decisions | Strong `ACCEPT / ABSTAIN` rule | Explicit abstention; current threshold has zero defined outputs on observed evidence | Strong available counterexample behavior; threshold-sensitive | Threshold and discontinuity; no outcome-validated threshold |
| Multiplicative Formulation | Strong: proportional attenuation matches the support question | Strong direct scaling | Explicit undefined state; tends toward zero as support decreases | Structural behavior is transparent; formal outcome test pending | No added attenuation parameter |
| Additive Formulation (lambda=0.5, 1.0) | Partial: score-scale-dependent penalty | Moderate | Missing rows undefined; low-support outputs can remain high | Lambda-dependent behavior; no outcome-based selection | Lambda and score-scale assumptions |
| Nonlinear Formulation (gamma=0.5, 1.0, 2.0) | Partial/strong: alternative attenuation shapes | Moderate | Missing rows undefined; stronger attenuation for larger gamma | Functional-form sensitivity; gamma not identified | Gamma and curvature assumption |

## Reading rule

The columns are decision dimensions, not additive points. Different candidates are useful under different operating conditions. The table therefore supports `NO_SINGLE_DOMINANT_MODEL`, while the current model remains the primary development structure for the stated research question.
