# Paper Claim Audit

Audit basis: `paper/submission_candidate.md`, development CSV/JSON artifacts, figures, `FORMAL_GATE_SWITCH.md`, and current handoff state.

| Claim | Source in paper | Supporting experiment | Supporting artifact | Status | Required correction |
|---|---|---|---|---|---|
| Development model separates score from evidence support | Results / discussion | Core closure and sensitivity | `research_core_closure.md`, `reliability_sensitivity.csv` | SUPPORTED_WITH_LIMITATION | Keep development-only scope and denominator 70 explicit. |
| ABL/HOT/Gap are 3.5625/0.375/1.125 | Results | Independent reproduction | `core_numbers_source_of_truth.json`, summary CSV | SUPPORTED | Keep values tied to AI_PROVISIONAL development input. |
| Score stability proves measurement validity | Any occurrence | None | No supporting artifact | OVERSTATED | Replace with score stability under this slice; state it does not establish validity. |
| Formal AIV or ranking is available | AIV/ranking sections | None; Gate PENDING | `annotation_gate_report.json` | UNSUPPORTED | Use `NOT_AVAILABLE_PENDING_FORMAL_GATE`; do not add estimates. |
| AI provisional labels are human truth | Annotation/method wording | None | `pilot_ai_provisional.csv` | UNSUPPORTED | Label as `AI_PROVISIONAL` and `LLM_EXPLORATORY_NOT_HUMAN`. |
| Evidence Support coverage falls as prompt penalty rises | Figure 4 / discussion | Lambda prompt sensitivity | `reliability_sensitivity.csv`, Figure 4 | SUPPORTED_WITH_LIMITATION | Explain finite grid and current prompt/context composition. |

## High-priority risks

1. Any formal AIV/ranking language before human R1/R2 and Gate PASS blocks submission.
2. Causal or validity wording exceeds the descriptive development evidence.
3. Figure captions must distinguish Score Stability from Evidence Support Stability and state the 70-record denominator.

## Submission decision

**Block formal-claim submission** until the Gate is complete. A development-only candidate may proceed only with the limitations above visible.
