# Competition Paper Narrative Draft

> **状态与适用范围**：本文是论文结果表达与答辩叙事草稿。当前数值来自 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 数据，`formal_gate_eligible=false`。它们用于展示识别问题与方法行为，不是正式研究结论、统计置信区间、因果效应、正式 AIV 或学生排名。

## 1. Problem Background

AI 已经进入学习过程。学生提交的文本可能同时受到学生自身思考、AI 提问与提示、AI 内容重组、上下文缺失和来源不确定性的影响。于是，评价者看到的是一个由多种生成过程混合形成的结果，而不是一个可以直接等同于学生能力的纯粹观测。

这带来一个关键区别：**看到学生提交了什么，不等于观察到了多少可信的学生证据。** 如果评价只对最终文本打分，可能把 AI 的引导结构误当成学生的独立表现；如果评价只报告一个稳定分数，也可能掩盖支撑该分数的有效 Evidence 已经非常稀薄。

本研究关注的是 AI 辅助学习中的可观察交互与学习表现证据。当前 AIV 的定位是形成性教学诊断，不把它直接解释为学生长期稳定能力、无 AI 学习增益或 AI 的因果效果。

## 2. Research Question

在 AI 参与的学习环境中，当学生证据受到 prompt 引导、上下文缺失和标注不确定性影响时，如何构建一个**不把不可识别问题伪装成精确估计**的评价框架？

具体而言，本研究先问：

1. 哪些观察记录可以被保留为可解释的 Student Evidence？
2. 在透明、可审查的偏差假设下，评价分数和证据支持的可行范围如何变化？
3. 如何在证据不足时返回“不可定义”或“无法识别”，而不是填入一个看似完整的 0 分？

## 3. Measurement Problem: Why This Is Not Primarily a Prediction Problem

本问题首先是 measurement / identifiability problem，而不是 prediction problem。

预测问题通常假设目标、标签和数据生成关系足够明确，然后优化预测误差。但当前项目面对的是更早的一层问题：观察到的学生文本中，哪些成分可归因于学生可观察表现，哪些成分可能来自 AI prompt 或重组，哪些记录因为上下文不足、来源不可比或标注不确定而不应进入有效证据分母？

如果这些边界没有被确认，机器学习模型可能只是更精确地拟合一个混合标签，不能解决“分数由什么证据支撑”的问题。因此，本研究不为了显得复杂而加入机器学习，而是先进行证据筛选、来源审计和可识别性诊断。

## 4. Identification Strategy: Why Partial Identification / Bounds

当前数据缺少可用于识别 correction coefficient 的充分交叉支持：在开发数据中，16 条可判读 Evidence 全部具有 `prompt_induced=true`、`task_actor=ai`、`confidence=medium`、`context_truncated=false`。因此，不能从这些数据估计 prompt correction、context correction 或 confidence reliability 的唯一数值。

本研究采用 Partial Identification / Bounds：不假设真正的 correction coefficient 已知，而是给出一组透明的 assumption / sensitivity parameters：

- `lambda_prompt`
- `lambda_context`
- `r_medium`

在一组明确的参数集合 `Theta` 下，计算结果是否稳定、有效证据支持是否充足，以及哪些参数区域使评价失去定义。这里的区间是 **assumption-based identification interval**，不是统计置信区间，也不是参数估计的置信范围。

## 5. Mathematical Model

对每条可判读 Evidence 定义：

```text
w_i(theta) = I(student_evidence_bloom_i in L1...L6)
             * c_i
             * (1 - lambda_prompt * prompt_i)
             * (1 - lambda_context * context_i)
```

其中：

- `I(...)` 表示只有 Student Evidence 属于 L1–L6 时才进入有效 Evidence 分母；`NO_EVIDENCE` 与 `UNDETERMINED` 不被强行转为低分。
- `c_i` 是透明的 reliability penalty：high 为 1，medium 为 `r_medium`，low 为 0.5。
- `prompt_i` 与 `context_i` 分别表示 prompt 引导和上下文截断指示变量。
- 所有 `lambda` 与 `r_medium` 都是假设/敏感性参数，不是 learned probabilities、estimated causal parameters 或 calibrated correction coefficients。

主要指标为：

```text
ABL(theta)  = sum(w_i * Bloom_i) / sum(w_i)
HOT(theta)  = sum(w_i * I(Bloom_i >= L4)) / sum(w_i)
Gap(theta)  = sum(w_i * (Task_i - Bloom_i)) / sum(w_i)
```

同时报告：

- `effective evidence weight = sum(w_i)`
- `effective coverage = sum(w_i) / total records`

当 `sum(w_i)=0` 时，模型返回 `NO_EFFECTIVE_EVIDENCE`；ABL、HOT、Gap 在该假设下为 **undefined under assumption**，不能写成 0。

## 6. Development Findings

当前开发入口使用 70 条 `AI_PROVISIONAL` 记录，其中 16 条进入 L1–L6。基线参数为 `lambda_prompt=0`、`lambda_context=0`、`r_medium=0.75`，得到：

- `ABL = 3.5625`
- `HOT = 0.375`
- `Gap = 1.125`
- effective evidence weight = `12.0`
- effective coverage = `0.1714`

在有效参数网格中，ABL、HOT、Gap 基本保持不变：

- ABL 的范围约为 `3.5625–3.5625`
- HOT 的范围约为 `0.375–0.375`
- Gap 的范围约为 `1.125–1.125`

但是，effective evidence weight 从 `16.0` 下降到 `0.4`，effective coverage 从 `0.2286` 下降到 `0.0057`。这说明分数的数值稳定并不代表支撑分数的证据数量和有效性稳定。

这里不能把稳定性解释为 prompt 的因果效应已经被估计。更准确的表述是：在当前开发样本的完全分离结构下，惩罚项以近似共同倍数作用于所有可判读 Evidence，因而归一化后的分数不变，但总支持权重会下降。

## 7. Extreme Case: When Evaluation Loses Definition

当前所有可判读 Evidence 都具有 `prompt_induced=true`。当 `lambda_prompt=1` 时，每条可判读 Evidence 的 prompt 因子都变为 0，因而：

```text
sum(w_i) = 0
```

模型返回 `NO_EFFECTIVE_EVIDENCE`。此时 ABL/HOT/Gap 不是 0，而是 **undefined under assumption**。

这个极端情形的意义不是“分数变差”，而是：当评价完全依赖被 prompt 引导的可判读记录时，评价可能失去定义。Bounds 方法因此不仅给出一个数值范围，也给出一条明确的识别边界。

## 8. What the Findings Mean

本研究最核心的表达是：

> **Score Stability ≠ Evidence Support Stability.**

传统评价可能只问：“评价分数是否稳定？” AI 参与后还必须问：“这个分数背后是否仍然存在足够可信的学生证据？”

当前开发结果显示，分数可以在一组参数变化下保持不变，同时有效证据支持快速下降，甚至在极端假设下归零并使指标失去定义。因此，论文和 Demo 应将 Score 与 Evidence Support 分开报告，而不是用一个稳定分数替代证据审计。

## 9. Limitations and Identification Boundaries

当前所有结果均标记为 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。目前不能宣称：

- 正式研究结论；
- 学生真实能力或长期稳定能力；
- prompt causal effect 或 agent causal effect；
- 正式 AI 增量价值或正式 AIV；
- 学生排名或高风险奖惩依据。

当前完全分离结构只能谨慎描述为：`selection + annotation-rule + provisional-label + mapping mixture`。它不能直接解释为 prompt correction effect、agent effect 或真实教育因果效应。

具体限制包括：

1. 正式人工 R1/R2 尚未完成，Gate 尚未产生正式通过结论；
2. 当前可判读 Evidence 没有 `prompt_induced=false`、`context_truncated=true`、low/high confidence 和非 AI actor 的充分支持；
3. 没有独立无 AI 学习 outcome、可靠原生 session_id 和可比 treatment/control；
4. 当前开发文件部分逐条生成决策无法完整复现，来源分离仍有未解决部分；
5. 70 条 development 结果不能外推为 140 条正式人工标注结论；
6. `r_medium` 只是透明假设范围，不是校准后的可靠性参数。

## 10. Formal Validation Path

正式闭环保持冻结顺序：

```text
Human R1
→ at least 24h
→ Human R2
→ test-retest reliability
→ Gate
→ Gate PASS + formal_gate_eligible=true
→ Formal Support Audit
→ Formal Bounds
→ Demo
→ Final Paper
```

其中 R2 是同一标注者的 test-retest reliability，不得包装为 inter-rater reliability。正式人工结果回来后，以统一输入接口替换开发数据源，重跑 reliability、Gate、support audit、bounds、stress tests 和最终图表；不得覆盖或改写当前 development artifacts。

## 11. Demo and Paper Story

Demo 不应把用户注意力只放在 ABL/HOT/Gap 的数字上。推荐顺序为：

1. 先显示观察记录中有多少进入 L1–L6；
2. 再显示当前参数假设和 effective evidence support；
3. 同时报告 Score 与 Support；
4. 拖动 `lambda_prompt` 时，展示分数近似不动而 support 下降；
5. 到达 `lambda_prompt=1` 时明确显示 `NO_EFFECTIVE_EVIDENCE`，而非 0；
6. 最后说明当前结果是 development-only，正式人工标签回来后才能进入 formal gate。

论文的主线不应是“我们算出了一个更精确的分数”，而应是：我们识别出 AI 参与后评分中的测量与识别边界，并用 Partial Identification / Bounds 把“数值稳定”和“证据充分”拆开报告。

## 12. One-Sentence Takeaway

在 AI 辅助学习中，可信评价不能只报告分数是否稳定，还必须报告支撑分数的学生证据是否仍然存在、可解释且足够充分；当这一点无法识别时，模型应诚实地给出边界或拒绝定义，而不是伪装成精确结论。
