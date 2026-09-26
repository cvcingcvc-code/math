# Model Tradeoff Report

## Evaluation status

The frozen protocol was written before reviewing candidate results. Current artifacts are `AI_PROVISIONAL / DEVELOPMENT_ONLY`; Formal HUMAN_R1/R2 are 0/70 valid and the Formal Gate is pending. Therefore fit to a formal outcome, parameter stability, and outcome-based external transfer remain `PENDING` for every candidate.

## Received candidates

- Current Evidence Reliability Model: development artifacts and independent numerical verification received.
- Raw-only Baseline: received as the raw ablation of the same development pipeline.
- Rule-based Baseline: received as the fixed gated formulation (`C_gated`, threshold 0.5).
- Alternative Mathematical Formulations: received for multiplicative, additive (`lambda=0.5,1.0`), and nonlinear (`gamma=0.5,1.0,2.0`) forms.
- Simple Linear Baseline: `PENDING`.
- ML Challengers: `PENDING`.

## Pareto tradeoff

No single dominant model can be declared. The gated rule has the clearest safety behavior: on the fixed low-reliability counterexample (P108, raw=6, R=0.375) it abstains, while the multiplicative, additive, and nonlinear alternatives return defined scores. Its cost is zero defined outputs for the 16 currently observed evidence records at the threshold, so it is unusable as a general scoring model without a predeclared threshold/coverage policy.

The additive lambda=0.5 formulation has the smallest development RMSE against the raw score among tested alternatives (0.3125) and preserves rank stability, but this is not a validated outcome metric and the correction is comparatively weak. The current multiplicative model gives transparent attenuation and correct `NO_EFFECTIVE_EVIDENCE` handling for 54 missing records, but its score is structurally stable because all 16 readable records share the same provisional provenance pattern; that is not evidence of generalization.

The nonlinear family offers a tunable attenuation curve. Increasing gamma reduces outputs more strongly, but no formal outcome or predeclared clinical/educational target identifies a preferred gamma. Raw-only is the simplest reference and is useful for isolating what reliability correction changes, not as an automatically preferred model.

## Operating conditions

- Use the current model only for development-time evidence-support diagnostics under its explicit provisional boundary.
- Use the gated rule when abstention safety is prioritized and low coverage is acceptable.
- Use additive lambda=0.5 only as a development comparison point where closeness to raw scores is the stated objective.
- Do not select an ML challenger or claim transfer until it supplies the common split, leakage audit, and reproducible outputs.

Decision label: **NO_SINGLE_DOMINANT_MODEL**.
