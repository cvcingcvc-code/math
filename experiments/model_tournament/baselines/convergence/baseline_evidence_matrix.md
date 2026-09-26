# Baseline evidence matrix

## Status and scope

This is a convergence document for the already completed baseline tournament. It adds no model, parameter search, threshold search, or result. The source is the existing `../baseline_results.json`, `../baseline_results.csv`, and `../baseline_record_results.csv`; the common input is the 70-record `AI_PROVISIONAL / DEVELOPMENT_ONLY` slice. Human R1/R2 are both incomplete, the Formal Gate is `NOT_RUN`, and no Human Truth metric is available.

The matrix uses the same descriptive quantities throughout:

- `y_i`: Student Evidence Bloom level L1–L6 mapped to 1–6; `I_i=1` only for an observable level.
- `p_i`: `prompt_induced`; `t_i`: `context_truncated`; `c_i`: confidence weight high=1, medium=.75, low=.5.
- Aggregate Evidence Score: `Σ_i w_i y_i / Σ_i w_i` when support is positive. It is not `Delta_raw`, AIV, learning gain, or prediction accuracy.
- Effective Weight: `Σ_i w_i`. Effective Coverage: `Σ_i w_i / 70`; the denominator includes all 70 records, including missing/undetermined evidence.
- `SUPPORTED`, `LOW_SUPPORT`, and `NO_EFFECTIVE_EVIDENCE` are row decisions. The parent CSV's model-level aggregate status is emitted when total weight is positive; it only means that the aggregate score is defined, not that all rows are supported.

## Unified comparison

| Candidate | Mathematical formula / rule | Variables used | Reliability used? | Effective Weight | Aggregate Evidence Score | Row decision distribution (`SUPPORTED / LOW_SUPPORT / NO_EFFECTIVE_EVIDENCE`) |
|---|---|---|---|---:|---:|---:|
| Current Evidence Reliability Model | `w_i=I_i c_i(1−0.5p_i)(1−0.5t_i)`; `w≥.75` → `SUPPORTED`, `0<w<.75` → `LOW_SUPPORT`, `w=0` → `NO_EFFECTIVE_EVIDENCE` | Evidence, confidence, prompt, context | Yes, multiplicative | 6.000 | 3.5625 | `0 / 16 / 54` |
| Raw-only | `w_i=I_i`; observable → `SUPPORTED`, missing/undetermined → `NO_EFFECTIVE_EVIDENCE` | Evidence | No | 16.000 | 3.5625 | `16 / 0 / 54` |
| Simple Linear Weighted | `w_i=I_i clip(c_i−0.25p_i−0.25t_i,0,1)`; same fixed `.75` status cutoff as current model | Evidence, confidence, prompt, context | Yes, additive | 8.000 | 3.5625 | `0 / 16 / 54` |
| Simple Rule / Threshold | Missing → `NO_EFFECTIVE_EVIDENCE`; observable L4–L6 with confidence high/medium and no prompt/context risk → `SUPPORTED`; other observable → `LOW_SUPPORT`; descriptive weight is `I_i` | Evidence, confidence, prompt, context | No numeric Reliability; uses a rule | 16.000 raw observable mass | 3.5625 | `0 / 16 / 54` |

For all four candidates, HOT is `.375` and Task–Evidence Gap is `1.125`. The 16 readable records are all medium confidence, `prompt_induced=true`, and `context_truncated=false`. Therefore all weighting functions apply a common factor to the readable scores, making the aggregate score identical. This is a common-scaling property of this development slice, not a performance tie and not evidence that the formulas are interchangeable.

## What the current evidence supports

| Candidate | Supported now | Not supported now |
|---|---|---|
| Current model | A separate support quantity changes the raw observable mass from 16 to 6 and routes every readable row to `LOW_SUPPORT` under the declared assumptions. High raw Evidence can be retained while support is reported as limited. | Its multipliers are not calibrated probabilities. The current slice does not identify an independent context effect, a multiplicative interaction, or a prediction advantage. |
| Raw-only | A transparent raw descriptive score and explicit missing-evidence handling. | It cannot distinguish an observable L6 record with prompt risk from one with independent support. Its 16 `SUPPORTED` rows are rule outputs, not validated labels. |
| Linear | A simple additive reliability alternative can reproduce the current model's row statuses and score on this slice, with weight 8. | It has not been compared on Human Truth; the chosen .25 deductions are not estimated. Equality of current scores cannot select between additive and multiplicative form. |
| Rule | A fixed rule can reproduce the current categorical statuses and preserves `NO_EFFECTIVE_EVIDENCE` for missing Evidence. | It has no graded support mass and mixes Evidence level with support quality. It cannot establish calibration, accuracy, or a risk–coverage advantage. |

## Stable interpretation for paper and defense

The defensible statement is: **Raw-only loses the distinction between observed Evidence level and Evidence support. A Reliability layer is useful as a development-stage accounting of that distinction. The current data do not establish that the multiplicative formulation is required; the simple linear challenger reaches the same descriptive score and row statuses on the available slice.**

The matrix must remain marked `DEVELOPMENT_ONLY` until the Human Gate is completed. No row above is a Human Truth label, and the 70-record Gate slice must not be generalized to all 140 Pilot records.
