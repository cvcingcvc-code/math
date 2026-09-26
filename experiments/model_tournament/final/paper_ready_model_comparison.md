# Model Comparison and Selection

The model tournament protocol was frozen before reviewing candidate results. All candidates were required to use the same development input and to declare their provenance, perturbations, missingness handling, counterexamples, and parameter-selection history. The currently available comparison is development-only because the formal human annotation Gate has not passed.

The candidate set includes the Current Evidence Reliability Model, a raw-only baseline, a gated rule baseline, alternative multiplicative/additive/nonlinear formulations, and pending simple-linear and machine-learning challengers. On the available 70-record provisional slice, 16 records contain readable evidence and 54 are `NO_EFFECTIVE_EVIDENCE`. This makes the development comparison informative for behavior under evidence support, but insufficient for formal predictive fit.

The alternatives make different trade-offs. The gated rule abstains on the fixed low-reliability counterexample (P108, R=0.375), providing the strongest safety behavior, but at the current threshold it produces zero defined outputs for the 16 observed evidence records. Additive lambda=0.5 has the smallest development RMSE against the raw score among tested alternatives (0.3125), while preserving rank order; this is a descriptive structural comparison, not an outcome-accuracy result. The multiplicative model provides transparent attenuation and explicit missing-evidence handling, while nonlinear forms provide stronger attenuation as gamma increases. Raw-only remains a useful reference for the cost of reliability correction.

No model dominates across fit, safety, coverage, interpretability, transfer, and complexity. The correct conclusion is **NO_SINGLE_DOMINANT_MODEL**. The gated rule is appropriate when abstention safety is prioritized; additive lambda=0.5 is a comparison point when closeness to raw scores is prioritized; the current reliability model is appropriate for development-time evidence-support diagnostics under its provisional boundary. None should be described as a formal AIV or causal model.

## Robustness and alternative specification

The formulation runner uses fixed parameter grids and common sensitivity and ablation procedures. Rank stability against raw scores is 1.0 for the defined alternatives in the development slice, but common perturbation, missingness, and parameter-resampling results are not yet complete for all candidates. Existing external-transfer material is synthetic/controlled and structural only; it does not establish educational transfer.

## Limitations and next gate

Formal model selection requires valid HUMAN_R1/R2 labels, a passed Formal Gate, a frozen outcome holdout, the same perturbation and missingness manifests for every candidate, parameter stability analysis, and completed simple-linear and ML challenger artifacts. Until then, pending dimensions remain pending and no accuracy-based champion is selected.
