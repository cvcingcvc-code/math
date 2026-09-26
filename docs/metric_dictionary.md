# Metric dictionary (frozen vocabulary)

## Scope

These definitions apply across the paper, reports, validation code, and Demo. Current values derived from AI prelabels are `DEVELOPMENT_ONLY`; they are not human-validated measurements.

| Term | Formal definition | Interpretation / boundary |
|---|---|---|
| `Outcome_AI` | An observed outcome measured under an AI-assisted condition. | Requires a defined outcome variable and an identifiable AI condition. Not present in the current pilot table. |
| `Outcome_baseline` | A comparable observed outcome under a specified baseline condition (for example, no-AI, before, or matched control). | Must be measured on a comparable unit and scale. No such paired baseline is present in the current pilot table. |
| `Delta_raw` / `Observed Increment` | `Delta_raw = Outcome_AI - Outcome_baseline`. | Answers the observed difference only. It is not a causal effect or true learning gain. Current status: `NOT_SUPPORTED`. |
| `Raw Score` | The score computed from observed Student Evidence levels before reliability weighting. In the current development model, ABL/HOT/Gap are descriptive evidence scores. | A score of observed evidence, not an AI increment. |
| `Raw Signal` | The underlying observed evidence signal used to form a Raw Score. | Current Raw Signal is Student Evidence Bloom coding; it is not `Delta_raw`. |
| `Evidence Reliability` (`R`) | A bounded support weight attached to an observed evidence contribution. Current development form: `w_i = I(observable_i)c_i(1-λ_prompt p_i)(1-λ_context t_i)`. | A measurement-support factor, not a calibrated probability and not a causal coefficient. |
| `Evidence Support` | `S = Σ_i w_i`, the total effective evidence weight. | Quantity of weighted support. It is not the same as row coverage. |
| `Coverage` | `C = n_observed / N` for unweighted coverage, or `C_eff = Σ_i w_i / N` for effective coverage. `N` is all records in the declared analysis input, including records with no/undetermined evidence. | Current development denominator is 70 records. The denominator must be reported with every coverage value. |
| `Adjusted Score` | A reliability-weighted score, e.g. `Score_adj = Σ_i w_i y_i / Σ_i w_i`, when `Σ_i w_i > 0`. | Not interchangeable with an increment. If support is zero, return `NO_EFFECTIVE_EVIDENCE`; do not substitute zero. |
| `Reliable AI Increment` | `Delta_reliable = Delta_raw × R`, only if a valid `Delta_raw` exists and `R` is defined for that increment. | Current status: `NOT_SUPPORTED`; do not relabel adjusted evidence scores as this quantity. |
| `ACCEPT` | A decision state emitted only when the declared score is defined and its support/quality rules pass. | Must be reported with accepted error/accuracy and coverage. |
| `ABSTAIN` | A decision state emitted when evidence is insufficient, conflicting, or fails the declared support rule. | Must be reported with abstention rate / coverage. It cannot be presented as accuracy improvement by filtering alone. |

## Non-equivalences

- `Evidence Reliability` is not a probability unless externally calibrated; current `c_i`, `λ_prompt`, and `λ_context` are assumptions/sensitivity parameters.
- `Evidence Support` and `Coverage` differ: support is a weight sum; coverage divides a count or weight by all input records.
- `Adjusted Score` is not `Reliable AI Increment`; the latter requires a separately identified `Delta_raw`.
- `Raw Signal` is not automatically an AI increment. A signal becomes `Delta_raw` only after a valid baseline pairing is specified.

## Current identification statement

`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`. The current pilot contains AI-assisted interaction evidence and provisional labels, but no paired `Outcome_AI` and `Outcome_baseline` suitable for the formal subtraction above.
