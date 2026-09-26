# ML Challenger Final Handoff

**Status:** `ML_CHALLENGER / FINAL_HANDOFF`  
**Final claim state:** `INSUFFICIENT_FOR_STRONG_ML_CLAIM`  
**Purpose:** preserve a development robustness/model challenge for `MAIN_RESEARCH / CONVERGENCE` without changing the formal Evidence Reliability Model.  
**Window state:** `FROZEN / HANDOFF_COMPLETE` — no further models, tuning, or experiments in this window unless `MAIN_RESEARCH` explicitly requests new evidence.

## 1. Data identity and formal boundary

| Item | Recorded state |
|---|---|
| Development records | 70 unique Gate records |
| Positive records | 16 readable provisional Evidence labels (`L1`–`L6`) |
| Negative/undefined records | 54 `NO_EVIDENCE` or `UNDETERMINED` |
| Label identity | `AI_PROVISIONAL / DEVELOPMENT_ONLY` |
| HUMAN R1 | 0/70 valid |
| HUMAN R2 | 0/70 valid |
| Formal Human Gate | `NOT_RUN` |
| True validation/holdout | Not available |
| External labeled transfer | Not available; remaining 70 Pilot records are unlabeled |

The target is a proxy for **readable provisional Evidence**, not learning gain, AIV, causal AI effect, or human truth. The run manifest records Git HEAD `667ecf7e25226366014687aa0ff77cbd80d8df34` and input hashes in `ml_results.json`.

## 2. Models actually tested

1. **Logistic Regression** — class-balanced, `C=1`, max 2000 iterations.
2. **Shallow Decision Tree** — class-balanced, `max_depth=2`, `min_samples_leaf=5`.
3. **Random Forest exploratory** — 100 trees, `max_depth=3`, `min_samples_leaf=4`; exploratory because only 16 positives exist.

No other model, hyperparameter search, AutoML, neural network, XGBoost search, or optimization was run in this final challenger handoff.

Pre-label features were text length, agent/speaker confidence, context truncation, semester, length stratum, question form, surface Bloom cue, and path case. Label-derived fields were excluded.

## 3. All recorded experiment metrics

The complete fold-level record is retained in `ml_results.csv` and `ml_results.json`: 300 repeated-CV rows (3 models × 100 folds), 6 semester-transfer rows, and 9 missingness rows. The tables below report every aggregate and stress-run metric emitted by the experiment; no model or metric is omitted.

### 3.1 Repeated stratified cross-validation

Repeated 4-fold CV × 25 repeats = 100 folds per model. Values are mean ± fold SD.

| Model | Accuracy | Balanced accuracy | F1 | ROC-AUC | Brier | Log loss |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.875915 ± 0.072783 | 0.862541 ± 0.092290 | 0.757802 ± 0.130937 | 0.953915 ± 0.044753 | 0.090794 ± 0.035439 | 0.317908 ± 0.108382 |
| Shallow Decision Tree | 0.919444 ± 0.058611 | 0.901195 ± 0.114824 | 0.814726 ± 0.176275 | 0.913942 ± 0.106858 | 0.073493 ± 0.055742 | 1.075900 ± 1.895063 |
| Random Forest exploratory | 0.922190 ± 0.066379 | 0.894245 ± 0.113757 | 0.823291 ± 0.168200 | 0.928352 ± 0.085920 | 0.123528 ± 0.023253 | 0.416854 ± 0.050383 |

### 3.2 Test-time feature missingness

These are fixed 4-fold stress runs with the stated feature mask, not additional training or tuning.

| Condition | Model | Accuracy | Balanced accuracy | F1 | ROC-AUC | Brier | Log loss |
|---|---|---:|---:|---:|---:|---:|---:|
| Clean | Logistic | 0.871429 | 0.872685 | 0.756757 | 0.946759 | 0.090806 | 0.326501 |
| Clean | Tree | 0.900000 | 0.847222 | 0.774194 | 0.953704 | 0.074459 | 0.226945 |
| Clean | RF | 0.871429 | 0.806713 | 0.709677 | 0.928241 | 0.125942 | 0.423231 |
| 20% missing | Logistic | 0.785714 | 0.795139 | 0.634146 | 0.877315 | 0.138791 | 0.427475 |
| 20% missing | Tree | 0.814286 | 0.791667 | 0.648649 | 0.877315 | 0.150816 | 0.475007 |
| 20% missing | RF | 0.800000 | 0.716435 | 0.562500 | 0.872685 | 0.149709 | 0.476232 |
| 40% missing | Logistic | 0.714286 | 0.726852 | 0.545455 | 0.786458 | 0.200263 | 0.627784 |
| 40% missing | Tree | 0.714286 | 0.726852 | 0.545455 | 0.796296 | 0.238540 | 0.743844 |
| 40% missing | RF | 0.742857 | 0.701389 | 0.526316 | 0.820602 | 0.167791 | 0.516200 |

### 3.3 Internal semester transfer stress test

This is cohort transfer within the same 70-record development source, not external validation.

| Train → test | Model | Accuracy | Balanced accuracy | F1 | ROC-AUC | Brier | Log loss |
|---|---|---:|---:|---:|---:|---:|---:|
| 2025秋 → 2026春 | Logistic | 0.833333 | 0.848214 | 0.700000 | 0.897321 | 0.147745 | 0.456324 |
| 2025秋 → 2026春 | Tree | 0.888889 | 0.928571 | 0.800000 | 0.928571 | 0.103338 | 0.374591 |
| 2025秋 → 2026春 | RF | 0.916667 | 0.901786 | 0.823529 | 0.950893 | 0.134382 | 0.448362 |
| 2026春 → 2025秋 | Logistic | 0.970588 | 0.937500 | 0.933333 | 0.990385 | 0.060638 | 0.242308 |
| 2026春 → 2025秋 | Tree | 0.941176 | 0.918269 | 0.875000 | 0.918269 | 0.055948 | 1.153960 |
| 2026春 → 2025秋 | RF | 0.588235 | 0.687500 | 0.500000 | 0.932692 | 0.185220 | 0.549565 |

### 3.4 Interpretability and failure evidence

- Logistic coefficients, tree rules, and RF feature importance are stored in `ml_interpretability.md`; they are associations, not causal effects.
- The shallow tree's dominant rule uses standardized text length and context truncation.
- RF's largest recorded importances are text length and context truncation; this is not a causal attribution.
- The complete disagreement list is in `ml_failure_cases.md`. Recurrent high-confidence disagreements include P051 (predicted readable while the provisional target is not) and P024 (predicted not readable while the provisional target is readable). They are not human-label errors.

## 4. Final conclusion

`INSUFFICIENT_FOR_STRONG_ML_CLAIM`.

The ML challenger is a **robustness and model challenge**, not a model-selection winner. Development CV numbers do not prove that ML is better than the handcrafted model. The models cannot replace the current formal Evidence Reliability Model, and no current result justifies changing that model. The apparent fit is bounded by 16 positive AI-provisional labels, repeated resampling of the same 70 records, missingness degradation, and unstable Random Forest cohort transfer.

The handcrafted model's current evidence is different in kind: it reports explicit support decomposition, effective coverage, and fail-closed `NO_EFFECTIVE_EVIDENCE` after an Evidence label is present. Its empirical superiority over ML is also **not** established by this experiment. The correct study-level status is challenge completed, winner unselected.

## 5. Text for MAIN_RESEARCH

### Paper paragraph (English)

“As a development-only robustness challenge, we compared logistic regression, a depth-2 decision tree, and an exploratory random forest on a proxy target indicating whether an AI-provisional record received readable Student Evidence (16 positives among 70 Gate records). Repeated four-fold cross-validation produced apparently strong discrimination, but performance degraded under feature missingness and the random forest showed unstable cohort transfer. Because the labels were AI_PROVISIONAL rather than human-validated, no true holdout or external labeled set was available, and the handcrafted Evidence Reliability model is a post-label support transformation rather than a pre-label predictor, these results do not establish ML superiority, formal AIV validity, or causal AI benefit. We retain the ML models as robustness challengers and keep the handcrafted model unchanged.”

### 30-second defense statement (中文)

“我们做了一个克制的 ML challenger，只测试逻辑回归、浅层决策树和探索性的随机森林，目标是预测 70 条开发记录里哪些被 AI 临时标成可判读 Evidence。交叉验证表面指标不低，但正样本只有 16 条，缺失特征后明显下降，随机森林跨学期也不稳定；而且标签不是人工真值。这个实验的作用是做稳健性和反例挑战，不是选冠军，也不能证明 ML 优于当前 Evidence Reliability 模型，所以正式主模型不变。”

### Concise comparison table

| Dimension | ML challengers | Handcrafted Evidence Reliability model |
|---|---|---|
| Data requirement | Needs enough labeled examples and a genuine validation/holdout; current run has 16 AI-provisional positives only | Requires an observed Evidence label plus declared support factors; current version is development-only |
| Interpretability | Logistic coefficients/tree rules/RF importance are inspectable associations; RF is hardest to trace | Explicit component-wise formula, contribution and support accounting |
| Small-sample risk | High; repeated CV is not independent evidence and RF transfer is unstable | Arithmetic is reproducible, but factor assumptions and homogeneous current slice limit validation |
| Missing-evidence behavior | Predictors can still output probabilities unless an abstention policy is added; performance falls under feature missingness | Explicit fail-closed `NO_EFFECTIVE_EVIDENCE` when support is undefined/zero |
| Abstention behavior | Not learned or formally calibrated in this challenger | Declared support states and abstention are part of the model contract |
| Current empirical evidence | Development proxy metrics only; no formal accuracy, external transfer, or winner claim | Development support metrics and sensitivity/ablation evidence; no formal AIV or causal claim |
| Role in this study | Robustness/model challenge; exploratory pre-label comparator | Current formal research line; retained unchanged |

## 6. Reuse instructions and blockers

MAIN_RESEARCH may cite only the bounded paragraph and table above, with `DEVELOPMENT_ONLY` and `INSUFFICIENT_FOR_STRONG_ML_CLAIM` labels. Do not convert the CV values into formal validation, claim an ML winner, replace the handcrafted model, or infer causality. There is no computational blocker to citing this experiment; the only citation limitation is the unresolved evidence boundary (AI provisional labels, no human Gate, no independent external holdout).

## 7. MAIN_RESEARCH citation paths

Use these files as the source of record:

- Final handoff and bounded paper/defense wording: `experiments/model_tournament/ML_CHALLENGER_HANDOFF.md`
- Frozen protocol and data/split rules: `experiments/model_tournament/ml_protocol.md`
- Complete row-level metrics and run metadata: `experiments/model_tournament/ml_results.csv` and `experiments/model_tournament/ml_results.json`
- Coefficients, shallow rules, and RF associations: `experiments/model_tournament/ml_interpretability.md`
- Complete disagreement cases: `experiments/model_tournament/ml_failure_cases.md`
- Handcrafted comparison and model-necessity boundary: `experiments/model_tournament/ml_vs_handcrafted.md`

## 8. Explicit non-claims

This handoff does **not** support: an ML winner; ML superiority over the handcrafted model; replacement of the Evidence Reliability Model; formal predictive accuracy; generalization to all 140 Pilot records; calibrated reliability probabilities; Formal AIV; learning gain; or causal AI effect. The CV target is AI provisional readability only.

## 9. Git and file status at freeze

- Project root: `C:\Users\lin\Documents\Codex\2026-09-25\yu`
- Branch: `master`
- Git HEAD at freeze: `667ecf7e25226366014687aa0ff77cbd80d8df34`
- The six challenger evidence files above and this handoff are present under `experiments/model_tournament/`.
- `git status --short --branch` reports branch `master` with existing project modifications and untracked project artifacts, including `experiments/`; these pre-existing changes are not part of a claim that the ML challenger is committed or formally promoted.
- No `paper/`, `src/`, `validation/`, Formal Gate, or HUMAN R1/R2 file was changed by the final handoff action.

## Source files checked

- `ml_protocol.md`
- `ml_results.csv`
- `ml_results.json`
- `ml_interpretability.md`
- `ml_failure_cases.md`
- `ml_vs_handcrafted.md`
