# Failure Case Cards — development-only reuse pack

All four cards use the existing `AI_PROVISIONAL / DEVELOPMENT_ONLY` rows and existing tournament decisions. They are illustrative structural cases, not Human Truth, false-positive labels, or causal evidence. `Raw-only`, `Main`, `Linear`, and `Rule` refer only to the four fixed candidates in the parent tournament.

## Card P108 — high Raw Evidence with prompt risk

| Field | Value |
|---|---|
| Raw Evidence | L6 |
| Confidence | medium; Evidence confidence medium |
| Prompt-induced | true |
| Context-truncated | false |
| Other risk fields | `ambiguity_type=prompt_induced`; `scaffold_share=high`; `content_relation=reworked_with_addition`; correctness not assessable |
| Raw-only decision | `SUPPORTED`; weight 1.000 |
| Main model decision | `LOW_SUPPORT`; weight .375 |
| Linear model decision | `LOW_SUPPORT`; weight .500 |
| Rule decision | `LOW_SUPPORT`; raw observable mass 1.000, no graded Reliability |

**Problem illustrated:** a high observed Evidence level can carry prompt-induced support risk. Raw-only cannot express that distinction; the Reliability layer can report it explicitly.

**Paper wording:** “In development case P108, Raw-only treated an L6 Evidence record as supported, while the Reliability-aware candidates retained the level but marked its support as limited because prompt-induced risk was present.”

**Do not conclude:** that the prompt caused the Evidence, that the main decision is more accurate, or that this single record validates the multiplicative formula.

## Card P105 — task demand is not Student Evidence

| Field | Value |
|---|---|
| Raw Evidence | L2 |
| Confidence | medium; Evidence confidence medium |
| Prompt-induced | true |
| Context-truncated | false |
| Other risk fields | Task L5, `ambiguity_type=prompt_induced`; `scaffold_share=high`; `content_relation=reworked_with_addition`; correctness not assessable |
| Raw-only decision | `SUPPORTED`; weight 1.000 |
| Main model decision | `LOW_SUPPORT`; weight .375 |
| Linear model decision | `LOW_SUPPORT`; weight .500 |
| Rule decision | `LOW_SUPPORT`; raw observable mass 1.000 |

**Problem illustrated:** Task difficulty (L5) does not replace the observed Student Evidence level (L2), and Raw-only has no separate support-quality channel.

**Paper wording:** “P105 separates Task level from Student Evidence: a high Task level coexists with L2 observed Evidence, while the reliability-aware candidates report limited support.”

**Do not conclude:** that the student failed a high-level task, that the AI caused the lower Evidence, or that any candidate has a validated error on this record.

## Card P072 — truncated context and undetermined Evidence

| Field | Value |
|---|---|
| Raw Evidence | `UNDETERMINED` (no numeric Raw Evidence) |
| Confidence | low; Evidence confidence low |
| Prompt-induced | true |
| Context-truncated | true |
| Other risk fields | Task L4; `ambiguity_type=prompt_induced;context_missing`; `content_relation=not_comparable`; `scaffold_share=medium`; correctness not assessable |
| Raw-only decision | `NO_EFFECTIVE_EVIDENCE` |
| Main model decision | `NO_EFFECTIVE_EVIDENCE` |
| Linear model decision | `NO_EFFECTIVE_EVIDENCE` |
| Rule decision | `NO_EFFECTIVE_EVIDENCE` |

**Problem illustrated:** when Student Evidence is undetermined, all four candidates preserve an undefined state instead of substituting a zero. This shared behavior is missing-evidence discipline, not unique evidence that the multiplicative layer is needed.

**Paper wording:** “P072 was routed to `NO_EFFECTIVE_EVIDENCE` because Student Evidence was undetermined under truncated context; the score was not replaced by zero.”

**Do not conclude:** that the student had no ability, that the AI caused the missingness, or that the shared abstention demonstrates model accuracy.

## Card P035 — high Task level but unscorable Evidence

| Field | Value |
|---|---|
| Raw Evidence | `UNDETERMINED` (no numeric Raw Evidence) |
| Confidence | low; Evidence confidence low |
| Prompt-induced | true |
| Context-truncated | true |
| Other risk fields | Task L6; `ambiguity_type=prompt_induced;context_missing`; `content_relation=not_comparable`; `scaffold_share=medium`; correctness not assessable |
| Raw-only decision | `NO_EFFECTIVE_EVIDENCE` |
| Main model decision | `NO_EFFECTIVE_EVIDENCE` |
| Linear model decision | `NO_EFFECTIVE_EVIDENCE` |
| Rule decision | `NO_EFFECTIVE_EVIDENCE` |

**Problem illustrated:** a high Task label cannot rescue missing Student Evidence. The four candidates agree because the observable-evidence gate is shared.

**Paper wording:** “P035 shows why a high Task label does not justify imputing Student Evidence when context is truncated and Evidence is undetermined.”

**Do not conclude:** that the student produced no Evidence, that the task was completed at L6, or that agreement across models is a validated classification result.

## Reuse rule

These cards can be reused in the paper, Demo, PPT, and defense only with the `AI_PROVISIONAL / DEVELOPMENT_ONLY` label and the stated limitations. After Human Gate, each card must be rechecked against the corresponding human labels before any accuracy or agreement language is added.
