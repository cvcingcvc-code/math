# Model Failure Summary

| Candidate | Observed failure or limitation | Evidence state |
|---|---|---|
| Current Evidence Reliability Model | Formal human labels, formal outcome fit, and parameter stability are unavailable; all readable evidence is prompt-induced in the development slice. | PASS_WITH_LIMITATION / PENDING |
| Raw-only Baseline | Does not model evidence reliability; its apparent score is not a formal accuracy result. | PASS_WITH_LIMITATION |
| Rule-based gated | Abstains on P108 (R=0.375) and on all 16 observed evidence records at threshold 0.5, producing zero defined scored outputs. | PASS_WITH_LIMITATION |
| A multiplicative | Produces a defined score for low-R observed evidence rather than abstaining; missing records are handled safely as `NO_EFFECTIVE_EVIDENCE`. | PASS_WITH_LIMITATION |
| B additive | Weak attenuation can preserve high scores despite low reliability; lambda choice is not outcome-validated. | PASS_WITH_LIMITATION |
| D nonlinear | Gamma changes attenuation substantially; preferred gamma is not identified and boundary behavior is assumption-driven. | PASS_WITH_LIMITATION |
| Simple Linear Baseline | No artifact received. | PENDING |
| ML Challengers | No artifact, split, tuning log, or result received. | PENDING |

## Cross-cutting failures

The common development slice contains 70 records, only 16 readable evidence records, and 54 no-effective-evidence records. Existing formulation runs use the same provisional input but do not provide a formal holdout outcome, so fit rankings are descriptive rather than selection evidence. The external artifact is synthetic/controlled and explicitly structural transfer only; it cannot validate educational generalization.
