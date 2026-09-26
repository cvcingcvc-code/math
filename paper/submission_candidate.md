# 教育 AI 交互证据的可信评价：Score 与 Evidence Support 分离报告（Submission Candidate）

> **Development Only.** 本文所有数值来自 70 条 `AI_PROVISIONAL` 开发标注，`annotation_status=DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。正式人工 R1/R2 Gate 尚未完成。文中结果用于说明方法行为与识别边界，**不是**正式研究结论、统计置信区间、AI 因果效应、正式 AIV 或学生排名。
>
> 底稿：`reports/paper/competition_paper_narrative_draft.md`；数字唯一来源：`reports/verification/core_numbers_source_of_truth.json`。

## 摘要

AI 进入学习过程后，学生提交的文本混合了学生自身思考、AI 提示与重组、上下文缺失和标注不确定性。本文把问题定位为测量与可识别性问题，而非预测问题：先判断哪些记录构成可判读的学生 Evidence，再在透明假设参数下同时报告 Score（ABL、HOT、Gap）与 Evidence Support（effective evidence weight、effective coverage）。当有效证据权重为零时，模型返回 `NO_EFFECTIVE_EVIDENCE`，而不是 0 分。开发数据（70 条记录，16 条可判读 Evidence，693 个参数组合，其中 33 个无定义）显示：Score 在全部有定义组合中保持不变（ABL=3.5625，HOT=0.375，Gap=1.125），而 effective coverage 在有定义组合中从 0.2286 变化到 0.0057。核心结论是：**Score 数值稳定，不代表支持它的 Evidence Support 稳定。**

## 1. Problem Background

AI 已经进入学习过程。评价者看到的是多种生成过程混合形成的结果，而不是可直接等同于学生能力的纯粹观测。**看到学生提交了什么，不等于观察到了多少可信的学生证据。** 只对最终文本打分，可能把 AI 的引导结构误当作学生的独立表现；只报告一个稳定分数，则可能掩盖支撑分数的有效 Evidence 已经非常稀薄。

本研究的 AIV 定位是形成性教学诊断，不解释为学生长期稳定能力、无 AI 学习增益或 AI 的因果效果，也不用于高风险排名。

## 2. Research Question

在学生证据受到 prompt 引导、上下文缺失和标注不确定性影响时，如何构建一个**不把不可识别问题伪装成精确估计**的评价框架？

1. 哪些观察记录可以保留为可判读的 Student Evidence？
2. 在透明、可审查的偏差假设下，Score 与 Evidence Support 的可行范围如何变化？
3. 证据不足时，如何返回“无定义”，而不是填入看似完整的 0 分？

## 3. Measurement Problem

这首先是 measurement / identifiability problem。预测方法假设目标与标签已明确，而本问题更早一层：学生文本中哪些成分可归因于学生，哪些可能来自 AI 引导，哪些记录因上下文不足或来源不可判而不应进入有效证据。边界未确认时，更复杂的模型只会更精确地拟合一个混合标签。

开发数据的证据分层（70 条）：

| 类别 | 条数 | 处理 |
|---|---:|---|
| 可判读 Evidence（L1–L6） | 16 | 进入 Score 计算 |
| `NO_EVIDENCE` | 19 | 不进入，不视为低分 |
| `UNDETERMINED` | 35 | 不进入，不推断补齐 |

`NO_EVIDENCE`、`UNDETERMINED` 与可判读 Evidence 不混用。

## 4. Identification Strategy

16 条可判读 Evidence 全部具有 `prompt_induced=true`、`context_truncated=false`、`confidence=medium`、`task_actor=ai`。数据中不存在对照变化，因此无法估计 prompt、context 或 confidence 修正系数的唯一值。

本文采用 Partial Identification / Bounds：不假设修正系数已知，而是在透明参数集合 Θ 上计算结果：

- `lambda_prompt` ∈ [0, 1]，步长 0.05（21 个值）
- `lambda_context` ∈ [0, 1]，步长 0.10（11 个值）
- `r_medium` ∈ {0.5, 0.75, 1.0}

共 21×11×3 = 693 个参数组合。所得区间是 **assumption-based identification interval**，不是统计置信区间，参数也不是估计或校准值。

## 5. Mathematical Model

对每条记录 i 定义可靠性权重：

```text
w_i(θ) = I(student_evidence_bloom_i ∈ L1…L6)
         · c_i(r_medium)
         · (1 − lambda_prompt · prompt_i)
         · (1 − lambda_context · context_i)
```

- `I(·)`：只有可判读 Evidence 进入；`NO_EVIDENCE`、`UNDETERMINED` 的权重为 0，但仍计入分母 N。
- `c_i`：透明可靠性惩罚，high=1，medium=`r_medium`，low=0.5。
- `prompt_i`、`context_i`：prompt 引导与上下文截断的指示变量。

**Score（结果层）**，仅在 Σw_i > 0 时定义：

```text
ABL(θ) = Σ w_i · Bloom_i / Σ w_i
HOT(θ) = Σ w_i · I(Bloom_i ≥ L4) / Σ w_i
Gap(θ) = Σ_{i: Task_i defined} w_i · (Task_i − Bloom_i) / Σ_{i: Task_i defined} w_i
```

**Evidence Support（支持层）**：

```text
effective evidence weight = Σ w_i
effective coverage        = Σ w_i / N,   N = 70（全部 development records）
```

**effective coverage 的分母是全部 70 条 development records，不是 16 条可判读 Evidence。** 因此 coverage 同时反映“有多少记录可判读”和“可判读记录在假设下保留多少权重”。

**无定义规则**：Σw_i = 0 时返回 `NO_EFFECTIVE_EVIDENCE`，ABL/HOT/Gap 为 undefined under assumption，不平滑、不插值、不填 0。

**公共缩放命题**：若所有可判读 Evidence 的 (confidence, prompt, context) 取值相同，则 w_i = k(θ)·I_i，k(θ) 在分子分母中约去，Score 与 θ 无关，而 Σw_i = 16·k(θ) 随 θ 变化。这是代数结构，不是经验发现，更不是因果效应。

## 6. Development Findings (Development Only)

基线 θ₀ = (lambda_prompt=0, lambda_context=0, r_medium=0.75)：

| 指标 | 值 | 层 |
|---|---:|---|
| ABL | 3.5625 | Score |
| HOT | 0.375 | Score |
| Gap | 1.125 | Score |
| effective evidence weight | 12.0（=16×0.75） | Support |
| effective coverage | 0.1714（=12.0/70） | Support |

693 个参数组合中，660 个有定义，33 个无定义。有定义组合上的结果：

| 指标 | 最小 | 最大 |
|---|---:|---:|
| ABL | 3.5625 | 3.5625 |
| HOT | 0.375 | 0.375 |
| Gap | 1.125 | 1.125 |
| effective evidence weight | 0.4 | 16.0 |
| effective coverage | 0.0057 | 0.2286 |

（Score 的极差仅为浮点误差量级，约 1e-16。）

**Figure 4**（`reports/development/core_figure_4_bounds_support.svg`）：横轴为 `lambda_prompt`，固定 `lambda_context=0.00`、`r_medium=0.75`。红线为归一化 Score，保持 1.00；蓝线为 effective coverage，从 0.1714 下降。在 `lambda_prompt=1.00` 处标记 `NO_EFFECTIVE_EVIDENCE`，Score 不绘制。

解释：当前 16 条可判读 Evidence 的参数相关字段完全相同，满足第 5 节公共缩放条件，所以 Score 稳定是**结构必然**，不能解释为模型稳健性或 prompt 的因果作用。

### 消融与典型反例

在同一批 70 条开发记录上，M0（无校正）、M1（仅置信度）、M2（置信度+prompt）、M3（置信度+prompt+context）的 ABL/HOT/Gap 均为 3.5625/0.375/1.125；effective weight 依次为 16、12、6、6。当前可判读 Evidence 全部带 prompt 风险，context 在可判读集合中没有变异，因此这组消融定位了支持度变化，却不能估计 context 的独立经验效应。完整表见 `reports/development/ablation_results.csv`。

四条反例均直接来自开发输入：P105 的 Task L5 与 Evidence L2 同时带 prompt 风险；P108 的 Raw Evidence 为 L6 但支持度有限；P072 因 context 截断而为 `UNDETERMINED`；P035 同时低置信、context 截断且无法形成有效 Evidence。后两条返回 `NO_EFFECTIVE_EVIDENCE`，不被填成低分。完整记录见 `reports/development/counterexamples.csv`。

## 7. Robustness / Sensitivity

1. **无定义边界**：33 个无定义组合全部位于 `lambda_prompt=1.0`（11 个 lambda_context × 3 个 r_medium）。此时 16 条 Evidence 的 prompt 因子全部为 0，返回 `NO_EFFECTIVE_EVIDENCE`。
2. **Support 的敏感性**：effective weight 在有定义组合上的中位数为 5.8，四分位数为 3.15 与 8.85。Support 对假设高度敏感，Score 则不敏感。
3. **独立复算**：`src/verification/recompute_bounds.py` 不依赖主实现，独立复现了 70/16/693/660/33 及全部边界值。
4. **异质性检查**：现有真实开发数据中，可判读 Evidence 的 prompt、context 和 confidence 均无变化，**不支持**异质 Evidence 的经验对比。本文没有修改标注，也没有构造合成数据冒充真实结果。
5. **可复现性**：从仓库根目录执行 `python run_all.py` 即可重跑完整开发链路（6 步）并完成 32 项一致性检查；干净克隆复现同样通过。开发版结果表见 `reports/submission/development_results_record_level.csv`，其中 AIV 与 ranking 均为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。环境、命令与边界见 `reports/submission/reproduction_notes.md`，字段定义见 `docs/data_dictionary.md`。这些检查只验证一致性与口径，不是效果验证。

## 8. Limitations

当前**不能**宣称：正式研究结论；学生真实或长期能力；prompt/agent 的因果效应；正式 AI 增量价值或正式 AIV；学生排名或高风险决策依据。

1. 正式人工 R1/R2 未完成，Gate 未产生结论。R2 为同一标注者的 test-retest，不是评分者间一致性。
2. 可判读 Evidence 缺少 `prompt_induced=false`、`context_truncated=true`、low/high confidence 和非 AI actor 的支持。
3. 完全分离结构可能混合了 selection、标注规则、临时标签和字段映射效应，不能解释为 prompt 修正效应。
4. 缺少独立的无 AI 学习 outcome、可靠原生 session_id 和可比 treatment/control。
5. 70 条开发结果不能外推到 140 条正式人工标注。
6. `r_medium` 与各 λ 只是透明假设范围，不是校准参数。

## 9. Competition Deployment / Demo

Demo：`reports/demo/index.html`（读取 `reports/demo/demo_payload.json`，需通过本地 HTTP 服务打开）。

1. 顶部横幅显示 `DEVELOPMENT_ONLY · AI_PROVISIONAL`；
2. 展示 70 条记录中有 16 条进入 L1–L6；
3. 拖动 `lambda_prompt`、`lambda_context`、`r_medium`；
4. 同时显示 Score（ABL/HOT/Gap）与 Evidence Support（effective weight / 70 development records）；
5. `lambda_prompt=1` 时状态变为 `NO_EFFECTIVE_EVIDENCE`，Score 不显示为 0。

正式切换流程见 `FORMAL_GATE_SWITCH.md`：人工 R1/R2 → test-retest → Gate → Gate PASS 后以 `--mode formal` 重跑 → 替换本文 Development Only 表格。

## 10. Conclusion

在 AI 辅助学习中，可信评价不能只报告分数是否稳定，还必须报告支撑分数的学生证据是否存在、可判读且足够充分。开发数据展示了这种分离：Score 恒定，Evidence Support 在有定义参数组合中从 0.2286 变化到 0.0057，并在极端假设下变为 `NO_EFFECTIVE_EVIDENCE`。**Score 数值稳定，不代表支持它的 Evidence Support 稳定。** 以上结论只描述方法行为；正式效果须等人工 Gate 通过后验证。

## 附录 A：数字来源

| 数字 | 来源文件 |
|---|---|
| 70 / 16 / 19 / 35 | `reports/verification/raw_input_recount.json` |
| 693 / 660 / 33、Score 与 Support 边界 | `reports/verification/core_numbers_source_of_truth.json` |
| 基线 12.0 / 0.1714 | `reports/development/partial_identification_grid.csv` |
| Gate 状态 PENDING | `reports/annotation_gate_report.json` |
