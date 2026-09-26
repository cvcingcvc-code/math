# Baseline model specification — development only

## Scope and identity

This independent challenger experiment uses only `data/annotations/ai/pilot_ai_provisional.csv`: 70 unique records, `AI_PROVISIONAL`, `DEVELOPMENT_ONLY`, `formal_gate_eligible=false`. It never reads or changes HUMAN R1/R2, the Formal Gate, frozen thresholds, the main implementation, the Demo, or the paper. Run `python experiments/model_tournament/baselines/baseline_models.py` from the project root. The script records the input SHA-256 and Git HEAD in `baseline_results.json` and checks that its local main-model recomputation matches the existing development totals (score 3.5625, weight 6, coverage 6/70).

The common analysis unit is a student turn. `y_i` is Student Evidence Bloom L1–L6 as 1–6; `I_i=1` only for such an observable level. `NO_EVIDENCE` and `UNDETERMINED` retain an undefined score and zero weight. `p_i` and `t_i` are prompt-induced and context-truncated indicators. `c_i` is high=1, medium=0.75, low=0.5. `N=70` always includes missing/undetermined records. Every weighted score is `Σw_i y_i / Σw_i`, undefined at zero total weight. HOT is `Σw_i I(y_i≥4)/Σw_i`. Task–Evidence Gap uses only rows with both levels and its own weight denominator.

The main metric here is **aggregate observable Evidence Score**, alongside effective weight, effective coverage (`Σw_i/70`), row-status coverage, HOT, and Gap. It is descriptive evidence, not an observed AI increment or prediction accuracy. Accuracy and classification sensitivity require independent truth and are reported as not computable. All coefficients and thresholds below were fixed before inspecting tournament results; no search or fitting is performed.

## Fixed candidates

| Model | Formula / decision | Inputs | Interpretation and limitation |
|---|---|---|---|
| Current main candidate | `w_i = I_i c_i(1−0.5p_i)(1−0.5t_i)`; `SUPPORTED` if `w_i≥0.75`, `LOW_SUPPORT` if `0<w_i<0.75`, else `NO_EFFECTIVE_EVIDENCE` | Evidence, confidence, prompt, context | Quantifies how each declared support factor reduces contribution. The factors and cutoff are assumptions, not calibrated probabilities. |
| Baseline A — Raw-only | `w_i=I_i`; observable → `SUPPORTED`, missing → `NO_EFFECTIVE_EVIDENCE` | Evidence only | Best possible raw score simplicity. It preserves missingness, but cannot express that an observable L6 contribution may have low support. |
| Baseline B — Simple Linear Weighted | `w_i=I_i clip(c_i−0.25p_i−0.25t_i,0,1)`; same fixed 0.75 status cutoff as the main candidate | Evidence, confidence, prompt, context | Additive, transparent alternative. The two 0.25 deductions are a simple equal-risk design choice, not estimated or selected from outcomes. It can reach zero and changes differently when risks co-occur. |
| Baseline C — Simple Rule / Threshold | Missing → `NO_EFFECTIVE_EVIDENCE`; observable L4–L6 with confidence high/medium and neither risk → `SUPPORTED`; any other observable row → `LOW_SUPPORT`. For its descriptive score, `w_i=I_i`. | Evidence, confidence, prompt, context | Uses the pre-existing L4 HOT boundary, no optimized cutoff. It routes cases but supplies no graded reliability mass; its reported `effective_weight=16` is an **unweighted observable count**, not quality-adjusted support. It mixes evidence level with support status, unlike the main status rule. |

The main and Baseline B use the existing 0.75 decision cutoff solely for a comparable status rule; no threshold is tuned to labels. Baseline C has no calibrated probability or numeric reliability. A and C's `effective_weight` should be read as raw observable mass. Each model is a Challenger, never a replacement or an official revision.

## Shared evaluation protocol

1. Same 70 records and exact missingness handling. Report aggregate score, HOT, Gap, support mass, effective coverage with denominator 70, and `SUPPORTED / LOW_SUPPORT / NO_EFFECTIVE_EVIDENCE` counts.
2. Same fixed record cases P108, P105, P072, P035; classify disagreements without calling them true or false predictions.
3. Same deterministic perturbation: SHA-256 rank of observable `record_id`, first seven records. Seven is 10% of all 70 records and 43.75% of the 16 readable records. Flip each selected `prompt_induced` flag, then separately shift its Evidence level by alternating ±1 with clipping to L1–L6. Recompute all models, aggregate score, coverage, decision flips, and contribution-order stability. These are stress scenarios, not empirical error-rate estimates.
4. Main-only parameter grid (`λ_prompt`, `λ_context` in `{0,.25,.5,.75,1}` and `r_medium` in `{.5,.75,1}`) checks the existing assumption sensitivity. Baseline coefficients and thresholds stay fixed. A model's response to the shared perturbations is the common sensitivity comparison.
5. Accuracy, accepted error, and classification sensitivity are `NOT_COMPUTABLE_NO_HUMAN_TRUTH`; no human labels or paired outcomes are available. External financial transfer uses another raw signal, reliability construction and decision target, so a fair paired education-baseline comparison is `NOT_SUPPORTED_FOR_COMPARISON`.

`baseline_results.csv` provides model-level results, `baseline_record_results.csv` permits per-record audit, and `baseline_results.json` contains metadata, perturbations, model definitions and the main sensitivity grid. The results must retain `DEVELOPMENT_ONLY` in any paper use.
