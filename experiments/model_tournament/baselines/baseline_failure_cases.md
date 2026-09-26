# Baseline failure and counterexample cases

All cases are `AI_PROVISIONAL / DEVELOPMENT_ONLY` observations, not independently adjudicated errors. “Failure” below means a structural information loss or a disagreement under the declared protocol. The record-level values are in `baseline_record_results.csv`.

| Case | Input facts | Main candidate | Baseline A | Baseline B | Baseline C | What it shows |
|---|---|---|---|---|---|---|
| P108 — high raw evidence with prompt risk | Evidence L6, medium confidence, prompt=true, context=false | `w=.375`, `LOW_SUPPORT` | `w=1`, `SUPPORTED` | `w=.5`, `LOW_SUPPORT` | `LOW_SUPPORT`, no graded weight | Raw-only treats the highest observable level as fully supported despite the declared prompt risk. B and C recover the same caution at different complexity. |
| P105 — high task, lower student evidence | Task L5, Evidence L2, medium confidence, prompt=true | `w=.375`, `LOW_SUPPORT` | `w=1`, `SUPPORTED` | `w=.5`, `LOW_SUPPORT` | `LOW_SUPPORT` | Task demand cannot substitute for student Evidence. Raw-only knows L2 but has no quality distinction for its contribution. |
| P072 — context truncated and Evidence undetermined | Task L4, Evidence `UNDETERMINED`, prompt=true, context=true, low confidence | `NO_EFFECTIVE_EVIDENCE` | same | same | same | Missing-evidence behavior does **not** distinguish the models when every challenger preserves the observable gate. The refusal to score is a shared data rule, not unique proof of multiplicative reliability. |
| P035 — high task, unscorable evidence | Task L6, Evidence `UNDETERMINED`, prompt=true, context=true, low confidence | `NO_EFFECTIVE_EVIDENCE` | same | same | same | A high Task label cannot rescue absent Student Evidence; all models correctly leave the score undefined. |

## Fixed perturbation cases

The seven selected readable records are P094, P040, P030, P118, P039, P083, and P033. Flipping their prompt flag moves the main model from `LOW_SUPPORT` to `SUPPORTED` on all seven and moves its effective coverage from 6/70 to 8.625/70. Baseline A has zero decision or score change because it ignores risk flags. Baseline B also flips seven statuses, with smaller score and support changes. Baseline C flips four statuses because its `SUPPORTED` rule also requires Evidence L4–L6; it has no numeric score/support change. These are controlled edits of the input, not claims that the original flags are wrong.

The alternating ±1 Evidence-level perturbation moves every model's aggregate score from 3.5625 to 3.5, with no status flips in this selected set. This confirms that the raw signal drives the reported score across all four methods. It does not validate the Bloom labels.

## Model-specific unresolved cases

- **Raw-only:** loses any distinction between observable evidence that has high versus low confidence or a flagged prompt/context risk. Its 16/70 `SUPPORTED` count is a modeling choice, not 16 validated records.
- **Linear:** in this development slice it exactly matches the main candidate's 16 `LOW_SUPPORT` and 54 missing statuses, while assigning each readable contribution 0.5 instead of 0.375. Without heterogeneous evidence or external truth, the observed slice cannot decide which amount is better.
- **Rule:** matches the main candidate's statuses in this slice but cannot express graded support. Its L4 criterion also makes status depend on Evidence level, so status is not a pure support-quality label.
- **Main candidate:** stronger reaction to the risk-flag perturbation is a sensitivity cost as well as a measurement feature. The current 16 readable records all have prompt=true, context=false, medium confidence; the full multiplicative interaction and separate context penalty are therefore not empirically identified here.
