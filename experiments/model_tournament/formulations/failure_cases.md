# Failure cases and required checks

All cases are generated from the same 70-record `AI_PROVISIONAL` development input plus a fixed synthetic extreme-R grid. Detailed rows are in `counterexamples.csv` and `extreme_R.csv`.

| Check | A: multiplicative | B: additive | C: gated | D: nonlinear |
|---|---|---|---|---|
| `R → 0`, Raw high | Score → 0 | Score remains Raw−λ | `ABSTAIN` | Score → 0 |
| `R → 1` | Returns Raw | Returns Raw | `ACCEPT`, Raw | Returns Raw |
| Raw high, R low | Strongly downweights | Can remain misleadingly high | Refuses below τ | γ controls suppression |
| Raw low, R high | Retains low Raw | Near Raw | Accepts Raw | Near Raw |
| Missing Evidence | `NO_EFFECTIVE_EVIDENCE` | `NO_EFFECTIVE_EVIDENCE` | `NO_EFFECTIVE_EVIDENCE` | `NO_EFFECTIVE_EVIDENCE` |

## Observed counterexamples

- `P108` has Raw L6 and `R=0.375`: A gives 2.25; B gives 5.6875 (λ=.5) or 5.375 (λ=1); C abstains; D gives 3.674 (γ=.5), 2.25 (γ=1), or 0.844 (γ=2). B is the least protective against a high Raw / low-support record.
- `P072` and `P035` have no numeric Evidence. Every structure returns `NO_EFFECTIVE_EVIDENCE`; this is the required no-false-precision behavior.

## External transfer

The three fixed cases from the existing small BTC structural-transfer artifact are replayed for every structure. They are synthetic/controlled evidence and remain `DEVELOPMENT_ONLY`; future outcomes are present in the source artifact but no predictive claim is made here. Case-level outputs are in `external_transfer.json`. The transfer suite tests formula behavior on a different signal scale, not educational validity or trading advantage.
