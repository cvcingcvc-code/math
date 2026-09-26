# Research Story Summary

> **Review status:** `HUMAN_REVIEW_REQUIRED_BEFORE_PHASE_2`
>
> **Evidence status:** `AI_PROVISIONAL / DEVELOPMENT_ONLY / Evidence Level 1 (descriptive and structural)`
>
> **Formal status:** `HUMAN_R1=0/70 VALID; HUMAN_R2=0/70; Formal Gate=NOT_RUN; AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED`
>
> **Scope:** 本文件只收敛研究问题、模型必要性、唯一核心结论、五条验证路径和证据边界。它不修改 UI、论文主体、模型参数、阈值、人工标注或 Formal Gate。

## 1. 一句话研究问题

> 在观测证据缺失、冲突或可信度不一致时，如何避免把 `Raw Signal` 直接当成可信结论，并构建一个显式报告 `Evidence Reliability`、`Support/Coverage`，且能在证据不足时降权或 `ABSTAIN` 的可审查评价框架？

这是一个 **measurement / identifiability** 问题。研究对象是 AI 辅助学习中的可观察交互与学生表现证据，不是已识别的真实能力、长期学习增益或 AI 因果效果。当前数据不能支持把 `Raw Signal` 写成 `Delta_raw`，因为没有合法配对的 `Outcome_AI` 与 `Outcome_baseline`。

## 2. 为什么需要这个研究

朴素评价把链条写成：

```text
Observed Result -> Score / Decision
```

这条链默认观测结果本身已经是可靠证据。AI 参与的学习记录可能同时含有学生表达、AI prompt 引导、上下文缺失、来源冲突、延迟信息和低置信标注。于是，`Raw Signal` 高不代表支撑它的学生证据同样充分。

本研究把链条展开为：

```text
Observed Evidence
    -> Raw Signal
    -> Evidence Reliability
    -> Adjusted Evaluation
    -> Support / Coverage
    -> Decision
```

每层解决一个不同问题：

| 层 | 要回答的问题 | 当前含义 |
|---|---|---|
| `Observed Evidence` | 实际看到了什么？ | 先区分可观察、缺失和不可判读记录 |
| `Raw Signal` | 原始表现信号有多高？ | Student Evidence Bloom 的 L1–L6；不是 AI 增量 |
| `Evidence Reliability` | 这条信号有多少支持依据？ | 透明的支持权重；不是校准概率 |
| `Adjusted Evaluation` | 弱支持如何影响评价？ | `Raw × Reliability`，低支持不被放大 |
| `Support / Coverage` | 还有多少有效支撑？ | `S=Σw_i`、`C_eff=Σw_i/N`，当前 `N=70` |
| `Decision` | 是否应作判断？ | `ACCEPT`、`ABSTAIN` 或 `NO_EFFECTIVE_EVIDENCE` |

因此，Reliability 不是给 Raw 分数再加一个装饰性系数，而是把“表现有多高”和“这条表现有多少可审查支撑”拆成两个量。当前 `R` 仍是开发假设下的支持权重，不能解释成概率、因果系数或真实能力校准。

## 3. 一句话核心模型

> 仅当 `Student Evidence` 可判读时令 `I(observable_i)=1`，再按置信度、prompt 风险和上下文风险计算 `w_i=I_i c_i(1-λ_prompt p_i)(1-λ_context t_i)`；用 `Adjusted_i=Raw_i×w_i` 与 `S=Σw_i`、`C_eff=S/N` 同时报告分数和证据支持，支持不足时降为 `LOW_SUPPORT/ABSTAIN`，有效证据为零时返回 `NO_EFFECTIVE_EVIDENCE`，而不是填入 0 分。

当前开发模型链为：

```text
Observed Evidence
  -> Raw Signal
  -> Reliability weight
  -> Adjusted contribution
  -> Support / effective coverage
  -> ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE
```

理论上的增量分支单独保留：

```text
Delta_raw = Outcome_AI - Outcome_baseline
Delta_reliable = Delta_raw × R
```

由于当前不存在合法配对的两个 outcome，这条分支目前是 `NOT_SUPPORTED`，不进入开发版 Adjusted Score。

## 4. 唯一核心结论

> 在当前 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录和声明的参数范围内，显式加入 `Evidence Reliability` 能把 `Raw Performance` 与 `Evidence Support` 分开：归一化分数可以保持稳定，而有效支持从 `16` 降到 `6`、有效覆盖从 `0.228571` 降到 `0.085714`；当支持归零时，模型拒绝伪造一个 0 分并返回 `NO_EFFECTIVE_EVIDENCE`。因此，**Score Stability ≠ Evidence Support Stability**。

这是一条 Level 1 的描述性、结构性结论。它说明框架在当前开发切片上的行为和审计语义，不说明乘法形式是唯一最优，不说明权重已经校准，不说明预测准确率提高，也不说明 AI 带来了因果学习增益。

### 当前证据等级

- **最高等级：** `Level 1 — descriptive / structural development evidence`。
- **输入身份：** 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录；16 条可判读 Evidence，54 条为 `NO_EVIDENCE` 或 `UNDETERMINED`，后者进入 `NO_EFFECTIVE_EVIDENCE`。
- **关键结构：** 16 条可判读记录均为 `prompt_induced=true`、`context_truncated=false`、`confidence=medium`、`task_actor=ai`。因此当前切片只支持公共缩放行为，不能单独识别 prompt、context、confidence 或 actor 的独立效应。
- **形式状态：** `HUMAN_R1=0/70 VALID`、`HUMAN_R2=0/70`、`Formal Gate=NOT_RUN`、`formal_gate_eligible=false`。

### 可以说什么

- Raw Signal 与 Evidence Support 是不同的量，应同时报告。
- 在当前声明参数网格内，归一化 `ABL/HOT/Gap` 保持约为 `3.5625/0.375/1.125`，而有效权重与覆盖率下降。
- Reliability layer 能在开发版规则下降低弱证据的有效贡献，并保留 `NO_EFFECTIVE_EVIDENCE` / `ABSTAIN` 语义。
- 当前模型的行为、消融路径、局部参数敏感性、困难案例和有限结构迁移均可复算。

### 不可以说什么

- 不能把 Adjusted Score、Support 或 Coverage 写成 `AI Increment`、正式 AIV、真实学习增益或因果效果。
- 不能把 `R` 写成校准概率、真实可靠度或能力估计。
- 不能把开发版案例写成预测“正确/错误”，因为没有独立 true outcome。
- 不能把当前 70 条 Gate 样本外推为 140 条正式人工标注结果，也不能产生学生排名。
- 不能声称当前乘法结构、ML challenger 或外部金融实验胜出或具有普适性。

### Human Gate 完成后可以升级什么

若同一标注者按冻结协议完成 R1、至少间隔 24 小时完成独立 R2，且 Formal Gate 通过，可以把标注 test-retest reliability 和由此产生的支持审计升级为正式验证输入。Gate PASS 仍不会自动识别 AI 因果增量；要讨论 `Delta_raw` 或正式 AIV，还需要合法配对的 `Outcome_AI` / `Outcome_baseline`、独立 outcome 和相应识别设计。

## 5. 五重验证：五条路径攻击同一个核心结论

统一描述：

> **One research question, one core model, and five independent lines of validation.**
>
> **一个研究问题，一个核心模型，五条相互补充的验证路径。**

| Validation | 它攻击的质疑 | 当前证据与结果 | 它支持核心结论的哪一部分 | 边界 |
|---|---|---|---|---|
| **1. Baseline Comparison** | “Reliability 层其实没必要。” | Raw-only、简单线性、规则基线与主模型在当前同质切片上的归一化分数均为 `3.5625`；Raw-only 把 16 条可判读记录都标成 `SUPPORTED`，主模型把它们标成 `LOW_SUPPORT`，并把有效权重记为 `16→6`。 | Reliability layer 增加了 Raw-only 没有的支持语义和 graded support；它回答“为什么不能只报 Raw”。 | 不是 winner 赛；同分来自公共缩放。没有 human truth、accuracy 或 predictive superiority 证据，不能证明乘法形式必需。 |
| **2. Ablation** | “公式里的 Reliability / Gate 模块只是装饰。” | `M0→M1→M2→M3` 的有效权重为 `16→12→6→6`；归一化分数不变。prompt 模块承担当前主要支持下降；context 在可判读记录中没有变异，因此 M2/M3 相同。 | 证明组件确实改变 support accounting 和拒判边界，而不是只出现在公式里。 | 不能把模块差异解释成独立因果效应；context 作用在当前切片不可识别。 |
| **3. Sensitivity / Robustness** | “结果只是某个参数点碰巧调出来的。” | 单变量 `±10%/±20%` 扰动产生 `0` 个 decision-state flips；归一化分数保持，support 变化；学生 ranking 为 `NOT_APPLICABLE`。 | 支持局部结构稳定性，并显示“分数稳定、支持变化”不是单点展示。 | 这是有限声明网格，不是统计置信区间或全局稳健性；context 平坦是数据缺变异，不是已证明无作用。 |
| **4. Counterexample / Failure Analysis** | “遇到最困难的记录时模型就没有用。” | 成功/边界：P108 `Raw=L6`、`R=.375`、贡献 `2.25` → `LOW_SUPPORT/ABSTAIN`；P072、P035 无可判读 Evidence → `NO_EFFECTIVE_EVIDENCE`，不填 0。失败边界：没有 true outcome，无法检验 abstain 后是否正确；当前可判读记录同质。 | 直接检验高 Raw、缺失证据、低置信和上下文风险下的拒判语义。 | 这是结构性案例，不是准确率或真实错误率；不能选择性写成“模型预测正确”。 |
| **5. External Transfer** | “模型只是为当前教育数据硬写的。” | BTC 历史纸面模拟在三种 Raw Signal 上复用 `Raw→Reliability→Adjusted→ACCEPT/ABSTAIN`；A/B 具有有限结构支持，C 是失败边界；information-missing Gate 1/2 支持，Gate 3 不支持。 | 说明同一接口在性质不同的 Raw Signal 上可以运行，并在证据下降时降低 coverage/增加 abstention。 | `EXTERNAL_TRANSFER / DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`；不是教育泛化、交易优势或普适性证据。 |

五条验证不是五个彼此独立的研究结论。它们共同检查同一个命题：**如果 Raw Signal 与证据支持被混为一谈，系统会在弱证据、缺失证据或不同信息质量下给出过度确定的评价；Reliability layer 能把这条差异显式化并允许拒判。**

## 6. 其他实验的正确位置

| 实验/模块 | 位置 | 允许的表述 |
|---|---|---|
| **ML Challenger** | `Challenger / Supplementary Comparison` | 做过逻辑回归、浅层树和探索性随机森林的开发挑战；由于只有 16 个 AI provisional 正例、无共同 human holdout、缺失特征后性能下降且跨学期不稳定，结论是 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`、`NO_SINGLE_DOMINANT_MODEL`。不得选 ML winner。 |
| **Alternative Formulations** | `Structural Robustness / Alternative Formulation Check` | 比较乘法、加法、gated、nonlinear 的支持衰减行为；保留乘法只因研究问题对齐、透明、缺失证据语义清楚，不是因为已证明预测或因果最优。 |
| **Human Gate** | `Evidence Upgrade / Formal Validation` | 它回答 provisional AI evidence 能否升级为正式标注支持；当前 R1/R2 为空，Gate 未运行。同一标注者重测是 test-retest，不是 inter-rater。 |
| **Finance Shadow** | `External Transfer Case Study / Demonstration` | 只演示 Raw→Reliability→Adjusted→Decision 的结构迁移；不发展成交易研究，不改变教育主线或冻结参数。 |

## 7. 当前最强证据

当前最强证据不是“实验数量多”，而是同一条可复算链上的相互吻合：

- 独立复算与统一 source of truth 复现 `70 / 16 / 54`、`ABL/HOT/Gap=3.5625/0.375/1.125`、`effective weight=16→6`、`coverage=.228571→.085714`；
- `693` 个参数网格中 `660` 个 defined、`33` 个 undefined，零支持时保留 `NO_EFFECTIVE_EVIDENCE`；
- `run_all.py` 的开发检查为 `32/32 PASS`，paper/demo/fact artifact 的一致性检查为 PASS；
- Figure / case evidence 清楚显示高 Raw 可以伴随低 support，缺失 Evidence 不被填成 0。

这些证据支持“框架语义和结构行为可复算”，不支持形式有效性、因果效果或普适性。另有两个必须保留的削弱项：16 条 readable 记录是同质幸存者，且 provisional 标签的生成脚本/逐行日志尚未完全闭合。

## 8. 当前最大证据缺口

最大缺口是 **正式人工证据链尚未闭环**：真实 `HUMAN_R1/R2` 均为 0/70，Formal Gate 尚未运行，因此无法升级 test-retest reliability、正式支持指标或 Formal AIV。更根本的 AI 增量识别缺口是：没有合法配对的 `Outcome_AI` / `Outcome_baseline`、独立 learning outcome 和可靠原生 session。

即便 Human Gate 通过，也只能升级人工标注支持与正式验证层；它不会自动证明 AI 造成学习增益。当前还缺少 `prompt=false`、`context_truncated=true`、high/low confidence、非 AI actor 的充分交叉支持，所以 `λ_prompt`、`λ_context`、`r_medium` 仍是敏感性假设。

## 9. 论文准备怎样讲这个故事

论文按“问题如何被回答”组织，而不是按文件生成顺序：

1. **Introduction：** `Raw observation ≠ reliable evidence`，提出 measurement / identifiability gap 与研究问题。
2. **Problem Formulation：** 定义 Observed Evidence、Raw Signal、Reliability、Adjusted Evaluation、Support/Coverage、Decision，并明确 Adjusted ≠ AI Increment。
3. **Core Model：** 给出 `w_i`、Adjusted、Support/Coverage 和 zero-support fail-closed 规则，用人话解释每一层。
4. **Validation Design：** 先说明研究采用五条互补攻击路径，而非依赖一次结果。
5. **Results：** 按 Baseline、Ablation、Sensitivity/Robustness、Counterexample、External Transfer 排列结果。
6. **Discussion：** 解释为何 Score 可以稳定而 Support 下降，何时应 `ACCEPT`、`ABSTAIN` 或 `NO_EFFECTIVE_EVIDENCE`。
7. **Limitations：** 前置 AI provisional 标签、Human Gate、无 paired outcome、同质 readable slice、External Transfer 边界。
8. **Conclusion：** 只回到唯一核心结论，不扩大为 AI 学习因果或跨域普适性。

现有 paper candidate 已大体使用这条词汇链；正式整合时必须继续保持 `Adjusted Score`、`Reliable AI Increment`、`Formal AIV` 三者不混用，并在首次出现 coverage 时写明分母是全部 70 条 development records。

## 10. Demo 准备怎样讲这个故事

Demo 复制论文顺序，保持同一数据源和同一边界：

1. **Screen 1 — Research Question：** `Can a high observed signal always be trusted?`
2. **Screen 2 — Why Raw Is Not Enough：** 展示 P108 的 high Raw + weak support；并注明是 development example。
3. **Screen 3 — Core Model：** `Raw → Reliability → Adjusted → Support/Coverage → Decision`，标出 `NO_EFFECTIVE_EVIDENCE` 不等于 0。
4. **Screen 4 — Five-Line Validation：** 五个模块各回答一个攻击问题，不一次堆所有数字。
5. **Screen 5 — Interactive Case：** 切换 Normal / Missing / Conflicting / Low Trust，显示 Raw、Reliability、Adjusted、Decision。
6. **Screen 6 — Claim Boundary：** 分开显示 Supported、Development Only、Waiting for Human Gate、Not Supported。

Demo 只读统一事实源；任何数字都必须能追到开发 artifact。现有视觉验收已通过，但历史副本/旧审计曾出现双实现或 raw baseline 口径差异，进入 Evidence Integration 前应先确认单一 payload 版本，不应在本 summary 中把旧副本当作当前结论。

## 11. Human Review gate

本文件建议 Human Review 只确认四件事：

1. 研究问题是否保持在“证据支持评价框架”的范围内；
2. 唯一核心结论是否采用“`Score Stability ≠ Evidence Support Stability` + reliability 显式化”的措辞；
3. 五条验证是否作为同一结论的互补攻击路径，而不是五个并列成果；
4. 在 Human Gate 前，所有结果是否继续标为 `AI_PROVISIONAL / DEVELOPMENT_ONLY`。

在这四点确认前，本轮不进入 Paper 主体重写、统一前端数据层或 Demo UI 重新设计。

## 12. Source map

| Story element | Current authoritative source |
|---|---|
| Claim boundary / allowed wording | `docs/claim_boundary.md` |
| Metric vocabulary | `docs/metric_dictionary.md` |
| Core model | `docs/model_presentation/final_model_overview.md`, `docs/model_presentation/model_component_table.md` |
| Validation stories | `docs/model_presentation/validation_story.md`, `docs/model_presentation/failure_cases_story.md`, `experiments/model_tournament/baselines/convergence/baseline_evidence_matrix.md` |
| Main numbers | `reports/verification/core_numbers_source_of_truth.json`, `outputs/final_results.json` |
| Independent reproduction | `reports/verification/reproduction_review.md`, `reports/verification/development_submission_consistency.json` |
| Human/Formal boundary | `handoff/PROJECT_STATE.md`, `handoff/CURRENT_HANDOFF.md`, `FORMAL_GATE_SWITCH.md` |
| External transfer | `reports/external_transfer/external_transfer_summary.json`, `experiments/transfer_finance/transfer_validation.json`, `experiments/transfer_finance/information_missing_validation.json` |
| ML challenger | `experiments/model_tournament/ML_CHALLENGER_HANDOFF.md` |
| Alternative formulations | `experiments/model_tournament/final/core_model_comparison_table.md`, `experiments/model_tournament/final/model_selection_evidence.md` |

## 13. Pending next phase (after Human Review)

After this summary is accepted, the next bounded phase is:

1. Write `docs/research_story/research_rationale.md` and `main_conclusion.md` from this approved wording.
2. Write `docs/research_story/five_line_validation.md` and `reports/integration/claim_validation_matrix.md` with claim-to-evidence boundaries.
3. Reconcile the currently flagged Demo/source-of-truth version differences before any frontend data integration.
4. Only then update paper structure and the unified Demo data layer.

No model, data, labels, thresholds, UI, or paper body was changed in this phase.
