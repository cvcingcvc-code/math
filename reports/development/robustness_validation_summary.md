# Robustness validation summary

**Scope:** DEVELOPMENT_ONLY for education records and DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT for the fixed historical finance simulation. Human R1/R2 remain 0/70 and Formal Gate is NOT_RUN. No parameter, threshold, annotation, or research direction was changed.

## 1. Parameter Perturbation

Baseline is λ_prompt=0.50, λ_context=0.50, r_medium=0.75. The ±10% and ±20% one-at-a-time perturbations produce zero decision-state flips; formal student-level ranking is NOT_APPLICABLE across 70 records. Baseline states are 16 LOW_SUPPORT and 54 NO_EFFECTIVE_EVIDENCE; adjusted ABL remains 3.5625. Maximum mean absolute reliability change is 0.017143 and maximum record-level change is 0.075. Effective support is the sensitive quantity; context perturbation is inert because the 16 readable records have no context variation. This is development-stage structural stability on the current development slice, not parameter calibration, population-level robustness, or external robustness.

Artifact: 
eports/robustness/parameter_perturbation.csv.

## 2. Evidence Perturbation

Single-variable controls use existing records. P108 (L6, prompt-induced, medium confidence) moves from reliability 0.375 / adjusted 2.25 / LOW_SUPPORT to 0.750 / 4.50 / DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT; this is a mechanical response to a hypothetical input-field change, not a real observation or causal effect when prompt risk is removed. Lowering confidence to low moves it to 0.250 / 1.50 and retains LOW_SUPPORT. P072 remains NO_EFFECTIVE_EVIDENCE when only context is restored because Student Evidence is still UNDETERMINED.

Artifact: 
eports/perturbation/evidence_perturbation_cases.csv.

## 3. Controlled Parameter Variants

P108 is a controlled parameter variant: changing one input field makes the frozen formula mechanically raise its support status. P072 is a boundary variant: restoring context alone does not manufacture evidence because the observable gate remains closed while Student Evidence is UNDETERMINED.

## 4. External Transfer

The existing fixed historical BTC-USD paper simulation was summarized for three Raw Signals: 7-day momentum, RSI14 mean reversion, and MA20/50 trend. Framework transfer and cross-strategy reliability separation are DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT in the existing artifact; selective decision gain is PARTIAL. A/B show high-R quality above low-R; C does not. Controlled missing, delayed, conflicting, and low-trust evidence reduce reliability and increase abstention, while Gate 3 (low-R decisions having higher future error) is NOT_SUPPORTED. No trading advantage claim is made.

Artifacts: 
eports/external_transfer/three_raw_signals_unified.csv, 
eports/external_transfer/evidence_quality_cases.csv.

## 5. Failure / Boundary Findings

- 54/70 records have no effective evidence; this is the clearest refusal boundary.
- Parameter changes do not flip states in this slice because all readable records share the same 0.375 baseline weight.
- Context response cannot be independently assessed from the readable subset.
- External strategy C does not show the desired reliability ordering.
- Raw and adjusted scores can remain numerically aligned under common scaling while support falls; score stability is not evidence-support stability.

## 6. What these experiments support

The frozen Raw Signal → Reliability → Adjusted Signal → Decision/Abstention chain is operational under declared perturbations. It reacts directionally to controlled evidence quality changes and can return NO_EFFECTIVE_EVIDENCE. The same structural pattern runs on three fixed external Raw Signal types in historical paper simulation.

## 7. What these experiments do NOT support

They do not establish formal human annotation reliability, causal AI increment, true learning gain, calibrated probability, educational universality, or trading profitability. External transfer is auxiliary structural evidence only.
