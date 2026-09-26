# COMPETITION_FIGURE / VISUAL_EVIDENCE PLANNING

日期：2026-09-26  
责任范围：COMPETITION_FIGURE / VISUAL_EVIDENCE PLANNING  
模式：只读审计；未修改主线文件，未重新计算研究结果，未制作 PPT。

## 0. 证据边界

- 项目根目录：`C:\Users\lin\Documents\Codex\2026-09-25\yu`。
- 当前唯一可用于本轮图表叙事的数值主线：70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 开发记录。
- 16 条记录有可判读 Student Evidence，54 条为 `NO_EVIDENCE/UNDETERMINED`；可判读的 16 条全部为 `prompt_induced=true`、`context_truncated=false`、`confidence=medium`、`task_actor=ai`。
- Raw ABL/HOT/Task-Evidence Gap = `3.5625 / 0.375 / 1.125`；Raw effective weight/coverage = `16 / 0.228571`；基线修正后 effective weight/coverage = `6 / 0.085714`，coverage 分母固定为 `N=70`。
- `HUMAN_R1=0/70 VALID`、`HUMAN_R2=0/70`、Formal Gate=`NOT_RUN`，`AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED`。
- 所有图的页脚和图注必须保留：`AI_PROVISIONAL · DEVELOPMENT_ONLY · Formal Gate NOT_RUN`，并说明不支持正式 AIV、因果效应、准确率、排名或学生真实能力结论。

## 【国赛最终 6 图】

### Figure 1

- **Figure ID**：F1
- **Title**：Observed Evidence → Reliability → Adjusted Evaluation → Decision
- **Question answered**：模型总流程是什么？Reliability 在哪一步进入模型，证据不足时如何停止判断？
- **X axis**：流程阶段（左→右：Observed logs → Raw Signal/Evidence screening → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision）。
- **Y axis**：无数值纵轴；用上下分支表示 `ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE`，另画灰色 `AI Increment` 分支并标为 `NOT_SUPPORTED`。
- **Data source**：`docs/model_presentation/final_model_overview.md`、`model_component_table.md`、`model_equations.md`、`reports/development/core_figure_5_model_flow.svg`。
- **Expected message**：Raw 信号不直接进入结论；先检查 Evidence 是否可判读，再用 `w_i=I(observable_i)c_i(1−lambda_prompt p_i)(1−lambda_context t_i)` 计算支持度，最后才形成 Adjusted/Decision。`NO_EFFECTIVE_EVIDENCE` 是未定义/拒绝给分，不是 0 分；AI Increment 理论分支当前不进入结果。
- **Paper placement**：方法部分主图（模型定义之后）。
- **Demo placement**：首页流程主视觉，置于结果卡之前。
- **PPT placement**：第 1 张/开场图。
- **Risk of misinterpretation**：现有 `core_figure_5_model_flow.svg` 只有“Support check/Bounds/AIV”抽象框，没有显式画出 Raw、Reliability、Adjusted、Support/Coverage；观众可能误以为 AIV 已被计算。最小修复是重画成上述同构流程，并将 AIV 末端灰显为 `NOT_SUPPORTED`。

### Figure 2

- **Figure ID**：F2
- **Title**：Raw Evidence Is Not the Same as Supported Evidence
- **Question answered**：为什么 Raw 不够？同一 Raw 等级在支持度不足时会发生什么？
- **X axis**：逐记录 Raw Student Evidence 等级 `L1–L6`。
- **Y axis**：逐记录 `Adjusted contribution = Raw × Reliability`；不是 aggregate adjusted score。
- **Data source**：`reports/development/development_metrics.csv`、`reports/development/explain_records.json`、`reports/development/raw_adjusted_metrics.csv`、`reports/development/counterexamples.csv`。
- **Expected message**：P108 的 Raw=`L6`、`R=0.375`、有效贡献=`2.25`；P105 的 Raw=`L2`、`R=0.375`、有效贡献=`0.75`。旁注 `54/70` 条没有可判读 Evidence，因此不应被画成低 Raw 点。侧卡同时写 `effective weight 16→6`、`coverage 0.228571→0.085714`。
- **Paper placement**：结果部分“Raw vs Reliability-adjusted”主图。
- **Demo placement**：首页结果卡 1：`P108: L6 → LOW_SUPPORT/ABSTAIN`。
- **PPT placement**：答辩第 2 张；用 P108 口头讲 20–30 秒。
- **Risk of misinterpretation**：现有 `raw_vs_adjusted_scatter.svg` 点重叠、缺少 tick/case 标签，并把 `adjusted contribution` 容易误读成 aggregate score；54 条 `NO_EFFECTIVE_EVIDENCE` 未显式出现。最小修复是标注 P108/P105、加 `R=0.375` 与 `N=70`，把未定义记录放在单独的“not plotted / NO_EFFECTIVE_EVIDENCE”注释区，不填成 0。所有 16 点共享同一 R，必须注明这是公共缩放开发切片，不是异质性拟合或准确率图。

### Figure 3

- **Figure ID**：F3
- **Title**：Evidence Degradation Changes Support; Missing Evidence Triggers Refusal
- **Question answered**：Evidence 变差以后模型发生什么？恢复某一个字段是否足以恢复判断？
- **X axis**：受控条件/反事实变体（P108：Original → Prompt removed → Confidence low；P072：Original → Context restored → Evidence remains undetermined）。
- **Y axis**：Reliability `R` 与 `Adjusted contribution`；Decision 用点形/颜色标注（`SUPPORTED / LOW_SUPPORT / NO_EFFECTIVE_EVIDENCE`）。
- **Data source**：`reports/perturbation/evidence_perturbation_cases.csv`、`reports/perturbation/counterfactual_cases.csv`、`docs/model_presentation/validation_story.md`。
- **Expected message**：P108 去掉 prompt 风险时 `R: 0.375→0.75`、有效贡献 `2.25→4.5`、状态 `LOW_SUPPORT→SUPPORTED`；把 confidence 降为 low 时 `R=0.25`、有效贡献=`1.5`，仍为 `LOW_SUPPORT`。P072 即使恢复 context，Evidence 仍 `UNDETERMINED`，所以仍为 `NO_EFFECTIVE_EVIDENCE`。模型不会用“补字段”制造不存在的学生证据。
- **Paper placement**：结果部分“evidence degradation / counterfactual”小节；图注必须写 controlled development contrast。
- **Demo placement**：首页结果卡 3 或 Scenario 面板，展示“恢复上下文仍拒绝判断”。
- **PPT placement**：答辩第 3 张；用它解释降权、拒判和“不等于 0 分”。
- **Risk of misinterpretation**：这些是已有记录上的受控开发对照，不是随机实验、因果效应或人工真值验证；P072 没有真实新证据，只是字段恢复情景。最小修复是用 paired/slope plot 显示“changed_variable”，在标题/图注中加入 `controlled contrast, AI_PROVISIONAL`，禁止写成 causal improvement。

### Figure 4

- **Figure ID**：F4
- **Title**：Local Parameter Perturbation: Score/Status Stable, Support Moves
- **Question answered**：参数稍微变化时模型是否稳定？哪一个输出最敏感？
- **X axis**：一因素扰动 `−20% / −10% / baseline / +10% / +20%`；右侧边界面板可用 `lambda_prompt=0…1`。
- **Y axis**：左面板为 `mean |ΔR|` 或 `effective coverage`，并标 `status flips`/`rank changes`；右面板为 normalized Score 与 effective coverage 双轴。`lambda_prompt=1` 处标 `NO_EFFECTIVE_EVIDENCE (undefined)`，不绘制为 0 分。
- **Data source**：`reports/robustness/parameter_perturbation.csv`、`parameter_perturbation_summary.json`、`reports/development/what_if_sensitivity.csv`、`reports/development/core_figure_4_bounds_support.svg`、`partial_identification_summary.json`。
- **Expected message**：±10/±20% 扰动下 `status_flip_count=0`、`ranking_change_count=0`；最大 mean absolute reliability change 约 `0.017143`，最大记录级变化 `0.075`。支持度会变化，而 ABL/HOT/Gap 在当前公共缩放切片内不变。`lambda_context` 的平线来自可判读记录没有 context 变异，代表 `NOT_IDENTIFIED`，不是“context 已证明无效”。在更宽的 lambda_prompt 压力范围内，support 可降到 0 并转为 `NO_EFFECTIVE_EVIDENCE`。
- **Paper placement**：稳健性/敏感性小节；作为 F3 后的结构检验。
- **Demo placement**：参数滑块/What-if 面板，不放首页首屏。
- **PPT placement**：3 分钟不展示；5 分钟答辩或备份页展示。
- **Risk of misinterpretation**：有限参数网格不是统计置信区间，也不是校准结果；公共缩放造成 Score 平线，不能解释为模型验证。现有 `parameter_sensitivity.svg` 的纵轴是 `Δ mean reliability`，不能用“score stability”标题替代；`reliability_sensitivity.svg` 还含有 `nan` 坐标。最小修复是重画双面板，并明确 `finite development stress test`、`context NOT_IDENTIFIED`、`no calibration`。

### Figure 5

- **Figure ID**：F5
- **Title**：Component Ablation and the Refusal Boundary
- **Question answered**：哪些组件真正改变支持度？模型什么时候拒绝判断？
- **X axis**：左面板模型组件序列 `M0 → M1 → M2 → M3`；右面板案例 `P105 / P108 / P072 / P035`。
- **Y axis**：左面板 effective weight/effective coverage；右面板以 Reliability 与离散 Decision 状态表示（`R=0` 的记录必须标注“score undefined / NO_EFFECTIVE_EVIDENCE”，不能画成普通 0 分）。
- **Data source**：`reports/development/ablation_results.csv`、`reports/development/counterexamples.csv`、`reports/development/explain_records.json`、`reports/failure_cases/development_candidates.json`。
- **Expected message**：M0/M1/M2/M3 的 effective weight/coverage 为 `16/.228571 → 12/.171429 → 6/.085714 → 6/.085714`，ABL/HOT/Gap 都保持 `3.5625/.375/1.125`。confidence 与 prompt 组件减少 unsupported contribution；context 在当前可判读子集无变异，因此 M2→M3 不变。P072/P035 进入 `NO_EFFECTIVE_EVIDENCE`；P105/P108 保留 Raw 但为 `LOW_SUPPORT`。这说明“支持度/拒判”行为，不说明预测准确率或模型唯一优越。
- **Paper placement**：消融 + failure boundary 结果小节；可作为正文第 5 张。
- **Demo placement**：Failure/Decision 面板；首页只取 P072 一个结果卡，不显示完整消融图。
- **PPT placement**：3 分钟不单独展示；若需要替换 F2，则作为答辩第 3 张。
- **Risk of misinterpretation**：当前四个案例没有 `true_label/outcome`，不能叫“错误案例/正确案例”；model tournament 结论为 `NO_SINGLE_DOMINANT_MODEL`，不能做“主模型胜出”图。现有 `ablation_comparison.svg` 没有数值标签和分数稳定线，`counterexamples.svg` 的零柱无法区分“拒绝判断”和数值 0。最小修复是做两面板/表格化图，写清 `development-only`、`no true outcome`、`context effect not identified`。

### Figure 6

- **Figure ID**：F6
- **Title**：External Structural Transfer: Reliability Ordering Is Partial
- **Question answered**：External Transfer 能说明什么，不能说明什么？
- **X axis**：外部固定信号的 Reliability group：`low / medium / high`。
- **Y axis**：Raw direction quality / hit rate；每个策略一组颜色，附 `n` 与 `transfer_status`。
- **Data source**：`reports/external_transfer/three_raw_signals_unified.csv`、`experiments/transfer_finance/cross_strategy_validation.json`。可选的 full/missing 机制条带来自 `experiments/transfer_finance/information_missing_validation.json`。
- **Expected message**：A_7d_momentum `low=.4647, high=.4841`、B_RSI14 `low=.4876, high=.5212`，支持 high-R 优于 low-R 的结构性分离；C_MA20/50 `low=.5214, high=.4705`，不支持该排序。结论是框架在不同固定信号上有部分结构迁移，存在清楚的边界，不是教育效果验证，也不是交易优势。若加入 full/missing 条带，只能说 mean R `.6027→.4077`、coverage `.394→.00118`、abstain `.606→.9988`，并注明 Gate 3（low-R future error 更高）未支持。
- **Paper placement**：External Transfer 验证/限制小节，建议正文最后一张或附录首图；不能放成教育主结果。
- **Demo placement**：不放首页；放 Validation/Boundary 页面。
- **PPT placement**：3 分钟不展示；评委追问“是否可迁移”时展示。
- **Risk of misinterpretation**：BTC 历史 paper simulation 使用 synthetic/controlled evidence，`risk–coverage improvement` 未支持；C 策略反例必须保留；不得出现 trading advantage、收益提升或教育泛化表述。现有 `three_raw_signals_quality.svg` 只画 high-R，遗漏 low/medium，容易误导。最小修复是重画完整 low/medium/high 矩阵并给 C 明确标 `unsupported`，图注写 `EXTERNAL_TRANSFER / DEVELOPMENT_ONLY / no trading claim`。

## 3 分钟答辩只展示哪 3 张

1. **F1**：先让评委看懂 Raw → Reliability → Adjusted → Support/Coverage → Decision 的链条，以及 AIV 分支目前被挡住。
2. **F2**：用 P108 说明“Raw=L6 不等于高支持”，同时给出 54/70 无有效 Evidence 的覆盖边界。
3. **F3**：用 P108 的 prompt/置信度对照和 P072 的 context-only 恢复说明“证据变差会降权，证据仍不可判读就拒绝判断”。

F4、F5、F6 在 3 分钟中只口头报一句：参数扰动无状态/排名翻转；组件消融只改变支持量；External Transfer 仅为部分结构迁移。不要在 3 分钟中展示金融图或完整参数网格。

## 论文必须展示哪 4–6 张

- **正文必放 5 张：F1、F2、F3、F4、F5。** 这五张闭合“问题→模型→证据变化→稳定性→组件/拒判”主线。
- **F6 作为第 6 张可放验证/限制小节或附录首图**。如果论文篇幅只能容纳 5 张，F6 放附录，不得删掉图注中的 `partial structural transfer / no trading claim`。
- 论文正文的所有开发数值旁边必须同时出现：`AI_PROVISIONAL`、`DEVELOPMENT_ONLY`、`N=70`、`Formal Gate NOT_RUN`。

## Demo 首页只展示哪 3 个结果

1. **P108：高 Raw、低支持**：`Raw L6 → R=.375 → Adjusted contribution=2.25 → LOW_SUPPORT / ABSTAIN`。
2. **总体支持坍缩**：`Raw effective weight 16 → adjusted effective weight 6`，`coverage .228571 → .085714`，但 ABL/HOT/Gap 仍为 `3.5625/.375/1.125`；旁注“Score stability ≠ Evidence Support stability”。
3. **P072：拒绝伪精确**：Evidence=`UNDETERMINED`、context truncated；`NO_EFFECTIVE_EVIDENCE`，不显示 0 分；即使只恢复 context，仍不生成分数。

首页不放 External Transfer、完整消融表、金融收益/风险曲线或任何正式 AIV/准确率卡片。

## 4. 现有图的保留、降级和删除建议

### 可作为 F1–F6 数据基础，但需按上面最小修复重绘/重排

- `reports/development/core_figure_5_model_flow.svg` → F1 草图。
- `reports/development/raw_vs_adjusted_scatter.svg` → F2 草图。
- `reports/development/core_figure_4_bounds_support.svg` → F4 右侧边界面板草图。
- `reports/development/ablation_comparison.svg` → F5 左侧柱图草图。
- `reports/perturbation/evidence_perturbation_cases.csv` → F3 数据接口。
- `reports/external_transfer/three_raw_signals_unified.csv` → F6 数据接口。

### 只作附录/审计，不进 6 图主集

- `reports/development/core_figure_2_support_heatmap.svg`：大量 `n=0`，图中“zero cells shown as 0”容易被误读为测量为零；它更适合证据缺口审计。
- `reports/development/evidence_reliability_distribution.svg`：把 `NO_EFFECTIVE_EVIDENCE` 与数值 R=0 混在 0 桶，且首柱存在越界渲染（`y=-42`）；不适合主叙事。
- `reports/development/parameter_sensitivity.svg`：纵轴是 `Δ mean reliability`，不能直接回答“分数是否稳定”；context 平线只表示当前子集无变异。
- `reports/robustness/parameter_perturbation_stability.svg`：标题/纵轴语义错配，修复前不使用。

### 建议删除或停止引用（本窗口不执行删除）

- `reports/development/core_figure_3_prompt_vs_effective_evidence.svg`：只画 effective coverage 随 lambda_prompt 下降，与 F4 右侧边界面板重复。
- `reports/development/reliability_sensitivity.svg`：含 `nan` 坐标，且只画 adjusted ABL，语义与当前敏感性问题不匹配。
- `reports/development/counterexamples.svg`：P072/P035 的零柱无法表达“undefined/refusal”，应改为带状态的案例表/点图。
- `experiments/transfer_finance/figure1_raw_vs_adjusted.svg`、`figure2_reliability_distribution.svg`、`figure3_risk_coverage.svg`、`figure4_cases.svg`：文字占位图，不是真实绘制，不进入核心图。
- `reports/external_transfer/three_raw_signals_quality.svg`：只画 high-R hit rate，遗漏 low/medium 且未标 C 的失败边界；重画前不使用。

## 5. 未完成实验的数据接口（不编造结果）

如果后续 Human Gate 或正式实验完成，图表只替换同一字段接口，不改变图的逻辑：

- **F1 interface**：`annotation_source`、`annotation_status`、`formal_gate_status`、`AI_increment_status`、`observable`、`reliability_components`、`decision`。
- **F2 interface**：逐记录 `record_id, raw_evidence_level, reliability, adjusted_contribution, decision, source_status`；无有效证据记录必须显式保留为 `NO_EFFECTIVE_EVIDENCE`，不能填 0。
- **F3 interface**：`pair_id, variant_id, changed_variable, before_value, after_value, raw, reliability, adjusted, decision, contrast_type`；当前 `contrast_type=controlled_development`, 不是 causal。
- **F4 interface**：`parameter, change, value, score_metrics, effective_weight, effective_coverage, status_flip_count, ranking_change_count, identifiability_note`；需要同时存局部扰动和极端 undefined boundary。
- **F5 interface**：`component_set, score_metrics, effective_weight, effective_coverage, status_counts`；案例字段另存 `true_label/outcome`，在为空时禁止 accuracy/error 语句。
- **F6 interface**：`domain, signal_or_strategy, reliability_group, n, quality_metric, source_type, transfer_status, limitation`；教育数据与外部金融数据不得合并成一个 pooled accuracy。

## 6. 问题—证据位置—最小修复建议（只读窗口）

| 问题 | 证据位置 | 最小修复建议 |
|---|---|---|
| 主流程没有显式 Raw/Reliability/Adjusted/Support-Coverage | `reports/development/core_figure_5_model_flow.svg`；`docs/model_presentation/final_model_overview.md` | 由 MAIN_RESEARCH / CONVERGENCE 重画 F1，末端灰显 `AI Increment NOT_SUPPORTED`。 |
| Raw/Adjusted 图缺少数值与 undefined 语义 | `reports/development/raw_vs_adjusted_scatter.svg`；`raw_adjusted_metrics.csv` | 标 P108/P105、写 per-record contribution、补 54/70 `NO_EFFECTIVE_EVIDENCE` 注释和 `N=70`。 |
| 反事实图尚未形成主图 | `reports/perturbation/evidence_perturbation_cases.csv` | 生成 F3 paired/slope plot，明确 `controlled development contrast`，不写因果。 |
| 敏感性图问题与纵轴不匹配 | `reports/development/parameter_sensitivity.svg`；`reports/robustness/parameter_perturbation_stability.svg` | 用 F4 双面板：局部 ±20% 稳定性 + lambda_prompt 极端边界；注明 context `NOT_IDENTIFIED`。 |
| 消融图不能单独表达组件作用和分数稳定 | `reports/development/ablation_comparison.svg`；`ablation_results.csv` | 加数值标签和 ABL/HOT/Gap 恒定注释；将 context 作用限定为“当前切片不可独立识别”。 |
| Failure 图把拒判画成 0 高柱 | `reports/development/counterexamples.svg`；`counterexamples.csv` | 改为状态表/注释点图，把 `NO_EFFECTIVE_EVIDENCE` 与数值 0 分离。 |
| Reliability 分布图有混桶和渲染缺陷 | `reports/development/evidence_reliability_distribution.svg` | 不进主集；若保留附录，分开 `undefined/refusal` 与数值 reliability，并修复 y 轴。 |
| Heatmap 的 n=0 容易被读成真实零 | `reports/development/core_figure_2_support_heatmap.svg` | 只作附录审计；将“未观察到”与“值为零”用不同符号。 |
| External Transfer 图只画 high-R | `reports/external_transfer/three_raw_signals_quality.svg`；`three_raw_signals_unified.csv` | 重画 low/medium/high 完整矩阵，保留 C 不支持边界和 no-trading 限定。 |
| 金融占位图/模型 tournament 易引入错误主张 | `experiments/transfer_finance/figure1–4.svg`；`experiments/model_tournament/final/model_selection_evidence.md` | 停止引用；保留为附录/审计，不能写“主模型胜出”或交易优势。 |

## 7. 结论

最终核心视觉证据只围绕一个主张组织：**分数本身必须和支持它的 Evidence Support 一起报告；支持不足时降低贡献或拒绝判断。** 现有开发证据支持方法行为、边界和结构压力测试，但不支持正式人工验证、AI 因果增量、预测准确率、学生排名或金融收益结论。后续主线窗口只需按本报告的 F1–F6 接口重绘和排版，不应改模型、参数、阈值、Human R1/R2 或 Formal Gate。
