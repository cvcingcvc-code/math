# Reliability component source audit

Scope: frozen development formula only; no weight or threshold changes.

| Component | Why it exists | Current source/evidence | Status |
|---|---|---|---|
| `I(observable)` | Prevent no/undetermined Student Evidence from entering a score | Annotation schema and explicit `NO_EFFECTIVE_EVIDENCE` rule | **SUPPORTED_WITH_LIMITATION**; human validation pending |
| `c_i` confidence weight | Reduce contribution of low-confidence coding | Hand-specified sensitivity assumption (`high=1`, `medium=.75`, `low=.5`) | **WEAKLY_JUSTIFIED_COMPONENT**; not calibrated |
| `λ_prompt p_i` | Represent possible prompt-induced support risk | Development slice has all readable evidence prompt-induced; no independent contrast | **WEAKLY_JUSTIFIED_COMPONENT**; association only |
| `λ_context t_i` | Represent truncated-context support risk | No independent variation among readable evidence in current slice | **WEAKLY_JUSTIFIED_COMPONENT**; sensitivity-only |

Weights are frozen assumptions, not result-driven estimates. Existing sensitivity/ablation are finite stress tests; they do not identify unique weights or prove predictive validity. Human R1/R2 can validate labels and test-retest reliability, but cannot by itself identify an AI causal increment.
