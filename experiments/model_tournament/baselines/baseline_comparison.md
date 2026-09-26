# Baseline comparison and model-necessity audit

**Status:** `AI_PROVISIONAL / DEVELOPMENT_ONLY`; `formal_gate_eligible=false`; no HUMAN R1/R2, Formal Gate, formal AIV, prediction accuracy or causal AI increment is inferred. Four candidates use exactly the same 70 records. Main metric is descriptive aggregate Student Evidence Score, accompanied by support and decision coverage; it is not ground-truth performance.

## Unified results

| Candidate | Aggregate Evidence Score | HOT / Gap | Weight / effective coverage (N=70) | `SUPPORTED / LOW_SUPPORT / NO_EFFECTIVE_EVIDENCE` | Main difference |
|---|---:|---:|---:|---:|---|
| Current main | 3.5625 | .375 / 1.125 | 6 / .085714 | 0 / 16 / 54 | Multiplicative support; every readable row has weight .375. |
| A Raw-only | 3.5625 | .375 / 1.125 | 16 / .228571 | 16 / 0 / 54 | Treats every readable row as fully supported. |
| B Linear | 3.5625 | .375 / 1.125 | 8 / .114286 | 0 / 16 / 54 | Same status decisions here with simpler additive weighting; every readable row has weight .5. |
| C Rule | 3.5625 | .375 / 1.125 | 16 / .228571 raw mass | 0 / 16 / 54 | Same status decisions here without a graded support measure. |

All four scores are equal because the 16 readable records share prompt=true, context=false, medium confidence, so each weighting scheme applies a constant factor to every included score. This is a **degenerate common-scaling slice**. The numerical equality is neither accuracy parity nor proof that any formula is valid. Score stability conceals the change from 16 raw contributions to 6 effective units under the main assumptions.

## Required comparison dimensions

| Dimension | Finding |
|---|---|
| Main metric | All 3.5625; no observed-score advantage for the main candidate. |
| Sensitivity | On a fixed seven-record prompt-flag flip, main score changes +.133152 and coverage +.0375; B changes +.078526 and +.025; A and C score/coverage remain unchanged. Main and B each flip seven statuses; C flips four; A zero. This measures responsiveness, not correctness. |
| Missing evidence | All return `NO_EFFECTIVE_EVIDENCE` for 54/70 rows. This shared observability rule is essential, but does not establish unique value for the main reliability formula. |
| Counterexamples | P108 and P105 expose Raw-only's support overstatement. P072 and P035 show the shared refusal to score undetermined Evidence. See `baseline_failure_cases.md`. |
| Noise perturbation | Shifting the same seven Evidence levels by ±1 gives score 3.5 for all, status flips 0. Flag-flip contribution-order stability (Kendall-like sign concordance on comparable untied pairs) is main .7474, A 1.0, B .9540, C 1.0. Stable A/C scores under a risk-flag edit also mean those models ignore that information. |
| Stability | The existing main parameter grid has 60 defined and 15 undefined cells; every defined aggregate score is 3.5625 while effective weight spans 2–16. Baselines have fixed rules; the common perturbations above are their sensitivity/stability check. The grid's score invariance follows from common scaling, not robust validity. |
| Interpretability | A is simplest but omits support risk. C is a plain decision list, though it conflates level and quality. B's additive deductions are inspectable. Main exposes confidence/prompt/context components and quantitative support, but its factors and multipliers are assumptions. |
| Complexity | A: one observable gate and mean. C: one observable gate plus fixed L4/confidence/risk decisions. B: three additive terms and clipping. Main: three multiplicative factors plus weighted aggregation and status threshold. No fitted model appears in this tournament. |
| External transfer | `NOT_SUPPORTED_FOR_COMPARISON`: the available finance study changes signal, reliability and target, and has no matched education baseline or human truth. It cannot establish a winner here. |
| Accuracy / classification sensitivity | `NOT_COMPUTABLE_NO_HUMAN_TRUTH` for every candidate; accepted error and risk–coverage improvement are likewise unmeasured. |

## Answers to the five model-necessity questions

1. **Why is Raw-only insufficient?** It can preserve undefined Evidence, but P108 (Evidence L6, prompt-induced, medium confidence) gets full support `w=1` and `SUPPORTED`. It has no channel to report the distinction between evidence level and evidence quality. This is a structural limitation, not a measured accuracy failure.
2. **What does Reliability add?** The main candidate exposes a separate, continuous support mass (`16→6`, coverage `.228571→.085714` on denominator 70) and explains why a high Raw level can still have low support. It also makes the conclusion conditional on chosen penalties; `R` is not a calibrated probability. Missing-evidence refusal is shared by the challengers and cannot be credited uniquely to Reliability.
3. **Can a simple linear model reach similar effects?** Yes in this slice. Baseline B has the same score and all 70 status decisions as the main candidate, while giving support mass 8 rather than 6. Under the fixed flag perturbation it is less reactive. The data do not adjudicate 8 versus 6; claiming the main product form is necessary would overstate the evidence.
4. **Where do simple models fail?** A ignores confidence and risk flags; C provides no graded mass and mixes Evidence level with quality; B can differ from the multiplicative candidate when prompt and context risks co-occur, especially near zero after additive clipping. The current readable records lack such variation, so the latter two are structural scenario limits rather than observed errors.
5. **Is the main complexity justified?** Its quantitative, component-wise support accounting is useful if the intended output must report assumption-sensitive support. Its empirical superiority is **not demonstrated**. For the current slice, B is a serious simpler challenger and C reproduces the categorical decisions. The argument for retaining the main model is transparency of support decomposition and future testability, not a higher observed metric.

## Which results may enter the paper

As a **development-only baseline challenge**, the paper may state: same 70 AI-provisional records; all models yield ABL 3.5625; Raw-only labels 16 as supported versus the main's 16 low-support; the main weight is 6 versus Raw's 16 and linear's 8; simple linear and rule baselines match current categorical statuses; the main form is not empirically superior on the available slice. Include denominator 70 and the pending Human Gate wherever these numbers appear. The P108/P105/P072/P035 cases may be illustrative with provisional labels. Do not state improved accuracy, learned reliability, generalization, formal AIV, or causal AI value.

## Important problem found

The comparison reveals a direct model-necessity limitation: **the currently readable development evidence has no factor heterogeneity**, so the main candidate's extra multiplicative complexity cannot be validated against a simpler additive or rule model using current observed outcomes. Its greater response to risk-flag perturbation could be desirable caution or unwanted instability; independent human validation and heterogeneous cases are needed to decide. This does not invalidate the reported arithmetic, but it would overturn any claim that current development results prove the main form is uniquely required.
