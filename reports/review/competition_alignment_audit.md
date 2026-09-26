# 赛题—模型对齐与证据边界审查（Development Candidate）

## 1. 赛题—问题—模型—输出映射

| 赛题要求 | 当前数据实际可观察 | 冻结模型解决什么 | 最终输出如何回答 | 当前不能支持 |
|---|---|---|---|---|
| 评价 AI 辅助学习中的可观察增量价值 | 学生轮文本、Task/Evidence provisional 标签、AI 引导/上下文/置信字段 | 把 Observed Performance 分解为 Evidence Reliability 与 Adjusted Evaluation，并在证据无效时拒绝给分 | Raw/Adjusted Score 与 Evidence Support 同时报告，解释“分数稳定但支撑变薄” | 学生真实能力真值、无 AI 反事实、严格 AI 因果增量、正式 AIV、学生排名 |
| 识别评价失真来源 | 54/70 条不能形成 L1–L6 Student Evidence；可判读 16 条全部 prompt-induced | 通过显式权重 `(observable × confidence × prompt/context factors)` 表示支持度下降 | `LOW_SUPPORT` 与 `NO_EFFECTIVE_EVIDENCE`，以及 sensitivity/ablation/counterexamples | 不能把任一因子解释成已识别的因果效应 |
| 提供可审查的评价方法 | 公式、固定参数范围、逐条 Explain、What-if、Ablation | deterministic model，可独立复现 | Demo/Paper/PPT 共享 artifact | Human Gate 暂缓，当前不是 Formal Validation |

**结论：PASS（叙事层面）**。Problem、Model、Results、Demo、Paper、PPT 都围绕“AI 增量价值评价必须先确认 Evidence Support”展开。最大风险不是模型脱离赛题，而是把“形成性、证据支持层评价”说成了“真实 AI 增量价值已被识别”。

## 2. Measurement Boundary

| CAN CLAIM | CANNOT CLAIM |
|---|---|
| 当前观察记录中哪些 Student Evidence 可判读，以及支持度有多强 | True Ability 真值 |
| Raw Score 与 Reliability-adjusted Score 的透明关系 | 学生长期稳定能力 |
| `NO_EFFECTIVE_EVIDENCE` 表示当前记录无法支持有效归因 | 把缺证据当作低能力或 0 分 |
| 在当前开发切片和假设范围内，Score 与 Support 如何变化 | 严格 causal AI effect、AI 相对于无 AI 的增量 |
| 当前框架能否作为形成性诊断的结构化接口 | Formal AIV、学生排名或高风险决策 |

## 3. 54 条 NO_EFFECTIVE_EVIDENCE 的成因

统计来自 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录，原因允许重叠：

- `student_evidence_bloom` 缺失或不可判读：54/54（其中 `NO_EVIDENCE` 19，`UNDETERMINED` 35）。这是进入该状态的直接数学条件。
- `context_truncated=true`：28/54，与上述缺失高度重叠。
- `prompt_induced=true`：37/54。它降低可靠性，但单独不会把可判读记录变成零权重。
- `confidence=low`：51/54，是当前不确定性的重要伴随信号。
- `task_actor=ai`：37/54；`task_actor=unknown/空`：6/54。它们提示归因困难，但不是单独的零权重规则。

**解释：D，多种因素共同造成。** 数据显示直接触发来自 Evidence 缺失/未确定，且常与上下文不足、AI 引导和低置信重叠。当前数据不能把 54 条进一步分解成“模型设计错误”或“AI 场景因果不足”的唯一比例；因此不能选择 A/B/C 中的单一答案。

## 4. 三个最值得展示的真实案例

### A_high_raw_high_evidence（P108）

- raw: `6`
- evidence reliability: `0.375`
- adjusted: `2.25`
- evaluation status: `LOW_SUPPORT`
- 正向因素：observable Student Evidence
- 负向因素：prompt-induced
- 非技术解释：“这条记录看起来表现很高，但仍有可判读证据；模型保留分数，同时明确支持度只有中等。”

### B_high_raw_low_evidence（P105）

- raw: `2`
- evidence reliability: `0.375`
- adjusted: `0.75`
- evaluation status: `LOW_SUPPORT`
- 正向因素：observable Student Evidence
- 负向因素：prompt-induced
- 非技术解释：“任务看起来很难，但学生证据只有 L2；模型不让高任务难度直接冒充高学习证据。”

### C_no_effective_evidence（P072）

- raw: `None`
- evidence reliability: `0.000`
- adjusted: `None`
- evaluation status: `NO_EFFECTIVE_EVIDENCE`
- 正向因素：none
- 负向因素：prompt-induced; context-truncated; low-confidence
- 非技术解释：“记录里没有足够可判读的学生证据，所以系统拒绝给出一个看似精确的分数。”

## 5. Reliability contribution decomposition

冻结公式为 `R = I(observable) × c × (1−0.5·prompt) × (1−0.5·context)`。下表是实际乘法因子，不是 LLM 解释：

| 案例 | observable | confidence 因子 | prompt 因子 | context 因子 | R |
|---|---:|---:|---:|---:|---:|
| P108 | 1 | 0.75 | 0.50 | 1.00 | 0.375 |
| P105 | 1 | 0.75 | 0.50 | 1.00 | 0.375 |
| P072 | 0 | 0.50 | 0.50 | 0.50 | 0.000 |

P108/P105 的 0.375 来自 `1×0.75×0.50×1.00`；P072 的直接屏蔽来自 `observable=0`，其余风险因子只能作为原因证据，不能在公式中补回分数。

## 6. Sensitivity 收口

1. `lambda_prompt` 与 `r_medium` 在 ±20% What-if 下只改变支持度，ABL/HOT/Gap 保持不变。
2. `lambda_context` 在当前可判读切片没有变异，因此当前 What-if 不改变结果；这不是 context 已被验证无影响。
3. evaluation status 在 15 个 What-if 条件中没有频繁翻转；极端 `lambda_prompt=1` 的无定义边界来自既有 bounds，而非本轮新增 sweep。
4. 当前结论依赖“Score 的公共缩放结构”，但不依赖某一个精确的 λ 才成立。
5. 最敏感的是 Evidence Support（effective weight/coverage），不是归一化 Score。

## 7. Ablation 收口

- M0→M1：加入 confidence 后 Support 从 16 降至 12，说明不确定性信息不能省略；Score 不变。
- M1→M2：加入 prompt 因子后 Support 从 12 降至 6，说明 AI 引导风险是当前最有区分力的支持层因素；Score 不变。
- M2→M3：context 在当前可判读记录中无变异，Support 与 Score 不变；保留它是为了在未来有上下文截断记录时保持公式闭合，不是宣称当前已估计其独立效应。
- observable gate：去掉它会把 NO_EVIDENCE/UNDETERMINED 当成可评分行，造成 Support 失真并破坏 `NO_EFFECTIVE_EVIDENCE` 语义。

## 8. External Transfer 定位

金融实验增强的主张只有：**Raw Output 不应脱离 Evidence Quality 单独解释**。它是结构迁移压力测试，支持 reliability separation 与 sensitivity ranking 的部分结构，不支持 risk–coverage improvement、交易优势或教育因果通用定理。建议保留在正文一小段“外部结构迁移验证”，完整曲线和金融字段降到 appendix。

## 9. 评委视角三分钟逻辑

1. **赛题问题**：AI 进入学习后，最终文本同时受学生表现和 AI 引导影响，直接给一个分数可能把引导结果当成学生增量价值。
2. **传统评价缺陷**：只看 Score，不检查 Score 有多少可归因的学生 Evidence。
3. **真实反例**：P105 的任务是 L5，但 Student Evidence 只有 L2，且带 prompt 风险；只看任务难度会高估表现。
4. **数学模型**：先用 `observable` 筛 Evidence，再用 confidence、prompt、context 因子计算 Reliability，最后形成 Adjusted Evaluation；权重为零时拒绝评分。
5. **为什么可信**：公式透明、逐条 Explain、What-if 与 M0–M3 消融都复用同一确定性模型，结果可独立重算。
6. **最终能解决什么**：在形成性诊断中同时告诉评委/教师“表现数值是多少”和“这个数值有多少证据支持”，并把证据不足显式标出来。
7. **当前证据边界**：70 条开发记录仍未通过 Human Gate，不能推出 True Ability、正式 AIV 或 causal AI effect；金融实验仅是结构迁移压力测试。

## 10. 模块分级

### CORE

- Measurement problem 定义
- Raw → Reliability → Adjusted deterministic model
- `NO_EFFECTIVE_EVIDENCE` gate
- Explain / What-if / Sensitivity / Ablation
- 真实反例
- 统一 artifact 与 Demo/Paper/PPT 一致性

### SUPPORTING

- Human Gate protocol and status boundary
- Provenance separation audit
- External Transfer Validation 的小段结构迁移证据

### APPENDIX

- 金融完整曲线、record-level transfer 表
- 完整参数网格与独立复算文件
- Binance public-data shadow log
- 工程 manifest、untracked audit、长版审计记录

### REMOVE

- 任何把 transfer 写成交易优势的表述
- 把 AI provisional 结果写成 Human validation 的表述
- 不能直接服务赛题解释的工程过程细节
- 任何新增模型、SHAP/LIME、复杂 Dashboard 或额外 sweep

## 11. 论文最需要修改的三个地方

1. 将摘要和结论中的“AI 增量价值”统一改成“AI 增量价值评价的证据支持框架”，避免读者误解为已识别 causal effect。
2. 在主结果页紧邻 `3.5625 / 0.375 / 1.125` 放置 `16/70 readable`、`effective weight 16→6` 和 `NO_EFFECTIVE_EVIDENCE 54/70`，让赛题价值直接可见。
3. Transfer Validation 放正文一小段并加“结构迁移压力测试”限定，完整金融结果移入 appendix。

## 审查结论

赛题—模型映射：**PASS**。最大偏离风险是把形成性、证据支持层的评价框架说成真实 AI 因果增量价值。当前最高收益动作是按上面三个点做最小文字修复，然后冻结 Development Candidate。
