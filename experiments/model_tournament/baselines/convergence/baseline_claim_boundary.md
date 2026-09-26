# Baseline claim boundary

## Two separate model-necessity questions

### A. Is a Reliability layer necessary?

**Current development answer: it has a supported use, but not a formally validated performance claim.** Raw-only assigns full unit support to every observable Evidence level. P108 is the clearest structural example: Evidence L6 with medium confidence and `prompt_induced=true` is `SUPPORTED` under Raw-only, while the current model reports weight `.375` and `LOW_SUPPORT`. The Reliability layer therefore adds an explicit support-risk dimension and makes effective coverage (`6/70`) visible beside the raw observable mass (`16/70`).

This evidence supports the measurement argument that a raw Evidence level alone can omit a declared risk factor. It does not support claims of higher accuracy, causal validity, calibrated probability, or improved learning evaluation.

### B. Is the current multiplicative formulation necessary?

**Current development answer: no.** The simple linear challenger uses the same variables, reaches the same aggregate score (`3.5625`), and produces the same row decisions (`16 LOW_SUPPORT`, `54 NO_EFFECTIVE_EVIDENCE`) in this slice. The Rule challenger also reproduces the categorical distribution, although it lacks graded support. The readable records have no variation in prompt/context/confidence combinations, so the slice cannot distinguish a multiplicative interaction from a simpler additive factor.

The multiplicative expression remains a transparent candidate because it decomposes support into named factors and supports sensitivity analysis. Its form is a design assumption awaiting heterogeneous cases and Human Gate evaluation, not a result established by the current tournament.

## Allowed and disallowed statements

| Topic | Allowed wording | Do not write |
|---|---|---|
| Raw-only | “Raw-only ignores declared Evidence risk; P108 is a structural example.” | “Raw-only is inaccurate” or “Reliability has proven higher accuracy” before Human Truth exists. |
| Reliability layer | “The development comparison supports reporting Reliability alongside Raw Evidence and effective coverage.” | “Reliability is a calibrated probability,” “Reliability proves AI value,” or “Reliability measures true ability.” |
| Multiplicative form | “The multiplicative form is an interpretable candidate that remains to be tested against a simpler linear form.” | “The multiplicative form is necessary,” “the main model is proven to outperform the linear form,” or any ranking claim. |
| Current metrics | “All four methods give Evidence Score 3.5625 on the 70-record development slice; support mass differs.” | “The methods have equal accuracy,” because accuracy is not computable. |
| Missing Evidence | “All four preserve `NO_EFFECTIVE_EVIDENCE` for 54 undetermined rows.” | Treating missing evidence as a zero score or claiming this alone validates Reliability. |
| Human Gate | “Accuracy, sensitivity, specificity, precision, calibration, and risk–coverage remain pending Human Gate.” | Filling any of those metrics from AI provisional labels. |

## Evidence hierarchy

1. **Observed in current development artifact:** score, effective weight, coverage, status counts, fixed perturbation responses, and the four case cards.
2. **Structural interpretation:** Raw-only cannot encode risk; a Reliability layer can encode it; current factor variation is insufficient to identify the multiplicative form.
3. **Pending validation:** model agreement with Human Truth, error trade-offs, calibration, abstention quality, and any external transfer claim.

The financial transfer artifact is not a common evaluation set for these education candidates. It uses a different raw signal, Reliability construction, target, and outcome, so it cannot resolve either model-necessity question.

## Paper-ready paragraph

> In a development-only 70-record comparison, Raw-only, a simple linear Reliability challenger, a fixed rule, and the current Evidence Reliability model all produced an aggregate Evidence Score of 3.5625. Raw-only treated all 16 readable records as supported, whereas the current model reduced effective weight from 16 to 6 and classified those records as low support under the declared prompt and confidence assumptions. The linear challenger produced the same row decisions and score with weight 8. Thus the comparison motivates a Reliability layer for separating observed Evidence from support, but does not establish that the current multiplicative form is necessary or more accurate. Formal comparison remains pending Human R1/R2 and Gate completion.
