# PAPER_EVIDENCE_CHAIN / CLAIM_TO_EVIDENCE AUDIT

- 审计对象：`paper/submission_candidate.md`（`paper/development_submission_candidate.md` 内容同主版本的前 58 行）
- 审计根目录：`C:\Users\lin\Documents\Codex\2026-09-25\yu`
- 审计日期：2026-09-26
- 本报告是只读审计产物；没有修改 `src/`、`data/`、`paper/`、`reports/demo/`、`handoff/`、Human R1/R2、Formal Gate、模型参数或阈值。
- 状态词严格采用本轮要求：`SUPPORTED`、`PARTIALLY_SUPPORTED`、`DEVELOPMENT_ONLY`、`NOT_SUPPORTED`、`NOT_RUN`。

## 0. 总体判定

当前论文已经形成一条**开发版测量链**：赛题中的 AI 辅助学习评价问题 → 可观察 Student Evidence 假设 → 透明 Reliability 权重 → Raw/Adjusted 与 Support/Coverage → sensitivity、ablation、反例和结构迁移 → `Score Stability ≠ Evidence Support Stability`。这条链在 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录上可复算。

它还没有形成正式 AI Increment 识别链。`HUMAN_R1/R2` 尚未产生有效结果，Formal Gate 为 `PENDING/NOT_RUN`，当前没有合法配对的 `Outcome_AI` 与 `Outcome_baseline`，因此不能从 Adjusted、Support 或 Coverage 推出 AI 因果增量、真实学习增益或学生排名。

### 高优先级残余风险（交接补充）

1. **P1：AI provisional 来源追踪未完全闭合。** `reports/development/provenance_separation_audit.json` 的 `source_trace_findings` 记录：尚未找到生成 `pilot_ai_provisional.csv` 的可复现脚本/逐行决策日志；16 条可判读记录又正好是 provisional Evidence L1–L6 的筛选幸存者，并共享 `prompt_induced=true`、`task_actor=ai`、`confidence=medium` 等字段。因此 C5 的“公共缩放结构”可以复算，但不能把这 16 条的同质性解释成已识别的 prompt 因果效应或独立风险分布。最小修复建议：由 MAIN_RESEARCH / CONVERGENCE 归档生成规则、逐行来源和人工复核记录后，再决定是否扩大解释范围；本窗口不改标签。
2. **P1：canonical `ai_context_text` 存在未来内容泄漏边界。** `handoff/PROJECT_STATE.md`、`handoff/BLOCKERS.md` 登记 S4-F01：该列在部分记录中对应当前轮之后的 AI 内容；目前已从盲标路径隔离，但任何下游重新使用都可能污染 Task/Evidence、复制/改写和相似性判断。最小修复建议：继续只使用按时间顺序重建的前文上下文，并在后续数据字典/输入检查中保持该列禁用；本窗口不改数据。

### 当前唯一主数据身份

| 层 | 当前身份 | 关键数字/状态 | 证据位置 |
|---|---|---|---|
| 开发输入 | `data/annotations/ai/pilot_ai_provisional.csv` | 70 条；`AI_PROVISIONAL`；`DEVELOPMENT_ONLY` | `reports/development/development_results.json` |
| 可判读 Evidence | 同上 | 16 条 L1–L6；`NO_EVIDENCE=19`；`UNDETERMINED=35`；54 条无有效 Evidence | `reports/verification/core_numbers_source_of_truth.json` |
| 人工 Gate | `data/annotations/human/pilot_worksheet_A.csv` / `data/annotations/human/pilot_worksheet_A_retest.csv` | R1/R2 当前均无完整有效标签；Gate `PENDING`；`formal_gate_eligible=false` | `reports/annotation_gate_report.json`、`FORMAL_GATE_SWITCH.md` |
| 开发模型 | `w_i=I(observable_i)c_i(1-λ_prompt p_i)(1-λ_context t_i)` | 当前 16 条可判读 Evidence 全部 `prompt_induced=true`、`context_truncated=false`、`confidence=medium` | `reports/development/provenance_separation_audit.json` |
| 外部迁移 | BTC-USD 历史公开数据/受控信息缺失情景 | 1,698 条；只作结构迁移；不是教育结果或交易策略 | `experiments/transfer_finance/transfer_validation.json`、`experiments/transfer_finance/information_missing_validation.json` |

## 1. Claim → Evidence Matrix

> `Current evidence` 只记录已存在的文件事实；`Support status` 是当前证据对该 Claim 的支持等级，不是模型质量评分。`DEVELOPMENT_ONLY` 表示该 Claim 在开发数据/假设网格上有产物，但不能升级为 Formal。

| ID / Claim（论文当前表述） | Mathematical definition | Required evidence | Current evidence | Experiment | Figure/Table | Data identity | Support status | Allowed wording | Forbidden wording |
|---|---|---|---|---|---|---|---|---|---|
| **C1**：AI 辅助学习文本混合学生思考、AI 引导、上下文缺失和标注不确定性；本文建立先确认 Student Evidence、再报告 Reliability/Adjusted 的证据支持框架（`paper/submission_candidate.md:L8`）。 | 每条记录经过 `Student Evidence → w_i → Adjusted/Evaluability`；框架评价的是可观察证据支持，不直接观测 True Ability。 | 需要问题定义、分析单位、Student/AI 话语边界和目标构念边界。 | `research/research_spec.md` 明确日志是可观察过程证据；`docs/claim_boundary.md` 明确不等同长期能力/因果效应；模型流程已冻结。 | 研究规格与模型流程审查；不是效果实验。 | `reports/development/core_figure_5_model_flow.svg`；`docs/model_presentation/model_pipeline.md`。 | 研究规格 + 70 条开发切片；尚无独立学习 outcome。 | **PARTIALLY_SUPPORTED** | “面向 AI 增量价值评价的可观察证据支持框架”“形成性诊断接口”。 | “已识别真实 AI 增量”“测得学生真实能力”“已证明学习提升”。 |
| **C2**：70 条开发记录中 16 条有可判读 Student Evidence；`NO_EVIDENCE/UNDETERMINED` 不填成低分，零权重返回 `NO_EFFECTIVE_EVIDENCE`（`L12`）。 | `I_i=1{y_i∈{L1,…,L6}}`；若 `Σw_i=0`，状态为 `NO_EFFECTIVE_EVIDENCE`，不是 `0`。 | 逐记录标签、缺失状态、零权重保护、完整分母。 | 70 条中 16 readable、54 `NO_EFFECTIVE_EVIDENCE`；独立复算和 Demo 一致；缺失未被压成低分。 | `run_all.py` 开发链、`src/run_partial_identification.py` 零权重分支、独立 bounds 复算。 | `reports/development/core_figure_2_support_heatmap.svg`；`reports/development/core_figure_4_bounds_support.svg`。 | `AI_PROVISIONAL / DEVELOPMENT_ONLY` 70 条；不是 140 条全量人工样本。 | **DEVELOPMENT_ONLY** | “在 70 条开发记录中，16 条可判读，54 条无有效证据；系统显式拒绝给分。” | “16 条人工真值”“70 条代表 140 条 Pilot”“NO_EFFECTIVE_EVIDENCE 等于低能力/0 分”。 |
| **C3**：冻结 Reliability 权重公式（`L16`）。 | `w_i=I(observable_i)c_i(1-λ_prompt p_i)(1-λ_context t_i)`；`S=Σw_i`；`C_eff=S/N`。 | 公式实现、参数身份、边界状态、参数是否校准。 | 公式与展示版方程一致；`c_i`、`λ_prompt`、`λ_context` 是手设/敏感性参数；当前 readable rows 无 prompt=false 对照、无 context 变异。 | `reports/development/reliability_sensitivity.csv`、`reports/development/what_if_sensitivity.csv`、`reports/reliability_component_audit.md`。 | `docs/model_presentation/model_equations.md`；`reports/development/evidence_reliability_distribution.svg`。 | 70 条 `AI_PROVISIONAL`；16 条全为 `prompt_induced=true`、`context_truncated=false`、`confidence=medium`。 | **DEVELOPMENT_ONLY** | “透明、确定性、可复算的支持权重”“参数范围内的敏感性假设”。 | “R 是校准概率”“λ 是因果系数”“已估计 prompt/context 的独立效应”。 |
| **C4**：Raw/Adjusted 数字保持相同，Effective weight 与 coverage 下降（`L18–24`）。 | `ABL=mean(y_i)`；`HOT=share(y_i≥4)`；`Gap=mean(task_i-y_i)`；Raw support `=16`；Adjusted support `=Σw_i=6`；`C_eff=Σw_i/70`。 | 同一输入、明确分子/分母、独立数值复算。 | `ABL=3.5625`、`HOT=0.375`、`Gap=1.125`；support `16→6`；coverage `0.228571→0.085714`；与 source of truth 一致。 | `reports/development/raw_adjusted_metrics.csv`；`src/verification/recompute_bounds.py`；`reports/verification/core_numbers_source_of_truth.json`。 | 论文表（`L18–24`）；`reports/development/raw_vs_adjusted_scatter.svg`。 | 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY`；coverage 分母为全部 70 条开发记录。 | **DEVELOPMENT_ONLY** | “开发切片上的描述性 Raw/Adjusted 指标；effective coverage 的分母是 70。” | “Adjusted accuracy”“性能提升”“Adjusted Score 就是 AI Increment”。 |
| **C5**：核心现象是 Score 保持稳定而 Evidence Support 下降（`L26`）。 | 当 readable rows 共享相同乘法因子时，`Σ(w_i y_i)/Σw_i` 不变，而 `Σw_i` 与 `C_eff` 下降。 | 需要逐记录风险字段有足够身份、公共缩放的数学复算、有限参数结果和反例。 | 16 条 readable 全部 prompt-induced、context 未截断、confidence=medium；在有效网格中 ABL/HOT/Gap 稳定，support 下降。`research_core_closure` 明确这是公共缩放结构，不是有效性/因果证据。 | sensitivity、partial-identification grid、core closure；693 格中 660 defined、33 undefined。 | `reports/development/core_figure_4_bounds_support.svg`；`reports/development/partial_identification_summary.json`。 | `AI_PROVISIONAL / DEVELOPMENT_ONLY`；未覆盖异质 prompt/context 组合。 | **DEVELOPMENT_ONLY** | “在当前 70 条切片和声明假设下，Score 稳定但 Evidence Support 下降；稳定性来自公共缩放结构。” | “分数稳定证明测量有效/模型稳健/跨人群稳健”“AI 导致 support 下降”“普遍规律”。 |
| **C6**：`lambda_prompt`、`lambda_context`、`r_medium` 在 `-20%/-10%/baseline/+10%/+20%` what-if 网格内不改变核心分数/状态，support 更敏感（`L28–30`）。 | 有限集合 `G={λ_prompt,λ_context,r_medium}` 的参数扰动；比较 `Δscore`、`Δsupport`、状态翻转和排名变化。 | 预先声明的网格、每格输出、未调参、状态/排名检查。 | 15 行 what-if 均有；±20% 扰动无状态/排名翻转；context 扰动在当前切片为零，因为 readable rows 没有 context 变异。 | `reports/development/what_if_sensitivity.csv`；`reports/robustness/parameter_perturbation.csv` and `reports/robustness/parameter_perturbation_summary.json`。 | `reports/development/parameter_sensitivity.svg`；`reports/development/core_figure_3_prompt_vs_effective_evidence.svg`。 | `AI_PROVISIONAL / DEVELOPMENT_ONLY`；不是概率校准或外部验证。 | **DEVELOPMENT_ONLY** | “在声明的有限参数网格内，核心状态保持，support 更敏感。” | “参数已被数据识别/校准”“对任意数据和范围都稳健”“敏感性证明外部有效性”。 |
| **C7**：M0–M3 逐步加入 confidence、prompt、context 修正，主要说明 Support 变化（`L32–34`）。 | M0→M1→M2→M3；对应 support `16→12→6→6`，归一化 Score 不变。 | 共用同一记录集、每个组件有对照、组件无变异时标明不可识别。 | 消融 CSV 支持上述 support 路径；M2→M3 不变；context 在 readable 集合无变异；accuracy audit 缺 `prediction/true_label`。 | `reports/development/ablation_results.csv`；`reports/development/accuracy_coverage_audit.json`（`NOT_SUPPORTED`）。 | `reports/development/ablation_comparison.svg`。 | 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY`。 | **DEVELOPMENT_ONLY** | “消融定位冻结公式中的支持量变化；context 目前是压力情景。” | “confidence/prompt/context 的独立因果效应”“预测准确率提高”“消融证明了模型更好”。 |
| **C8**：替代模型 A/B/C/D 用于 Robustness Check，不构成唯一最优或预测/因果优越性（`L36–53`）。 | A `S_raw×R`；B `S_raw−λ(1−R)`；C `R<τ⇒ABSTAIN`；D `S_raw×R^γ`。参数均为固定/预注册结构比较。 | 公共输入、无结果调参、共同缺失规则、独立目标或 holdout 才能比较优越性。 | `experiments/model_tournament/formulations/formulation_results.json` 标明 `tuning:none`；`experiments/model_tournament/final/model_selection_evidence.md` 判定 `NO_SINGLE_DOMINANT_MODEL`；无 HUMAN outcome/holdout，ML/simple linear challengers 亦未完成。 | `experiments/model_tournament/formulations/run_tournament.py`；formulation results、counterexamples、sensitivity。 | `experiments/model_tournament/final/model_comparison_matrix.csv`；`experiments/model_tournament/formulations/model_tradeoffs.md`。 | 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY`；外部结构回放也非教育 outcome。 | **DEVELOPMENT_ONLY** | “替代函数在弱证据下产生不同结构行为；乘法模型作为透明固定参考。” | “乘法模型唯一最优/预测最优/因果优越”“按当前 RMSE 选择冠军”“最佳 threshold/最佳 γ 已被验证”。 |
| **C9**：P105、P108、P072、P035 展示高 Raw、低 support、上下文截断和 `NO_EFFECTIVE_EVIDENCE` 的组合（`L55–57`）。 | 逐记录 `raw_score`、`R`、`adjusted_score`、状态；`R=0` 时不生成 adjusted score。 | 真实记录 ID、原始字段、规则映射、Outcome 或 true label（若要说对错）。 | 4 条记录均可从 `reports/development/counterexamples.csv` 重建；全部 `AI_PROVISIONAL / DEVELOPMENT_ONLY`；没有 prediction/true_label，不能判断预测正确。 | `reports/development/counterexamples.csv`、`reports/perturbation/counterfactual_cases.csv`。 | `reports/development/counterexamples.svg`；`docs/model_presentation/failure_cases_story.md`。 | 70 条开发切片中的 4 个记录；不是人工验证或总体代表性样本。 | **DEVELOPMENT_ONLY** | “开发反例展示模型如何保留、降权或拒绝给分。” | “反例证明预测正确/错误”“P108 代表真实高能力”“prompt/context 已造成因果影响”。 |
| **C10**：External Transfer Validation 只给出结构迁移的初步/部分支持，不能声称交易优势（`L59–69`）。 | 在另一种 Raw Signal 上复用 `Raw→Reliability→Adjusted→ACCEPT/ABSTAIN`；比较 reliability separation、coverage/error、敏感性。 | 外部数据身份、无重新调参、未来信息隔离、结果与失败边界。 | BTC-USD 1,698 条历史数据：reliability separation 有限支持；sensitivity 支持；risk–coverage improvement 不支持；三种策略中 C 策略为 unsupported；信息缺失 Gate 3 不支持。 | `experiments/transfer_finance/transfer_validation.json`、`experiments/transfer_finance/cross_strategy_validation.json`、`experiments/transfer_finance/information_missing_validation.json`。 | `experiments/transfer_finance/figure1_raw_vs_adjusted.svg`、`experiments/transfer_finance/figure2_reliability_distribution.svg`、`experiments/transfer_finance/figure3_risk_coverage.svg`、`experiments/transfer_finance/figure4_cases.svg`。 | 外部历史/合成受控证据；`EXTERNAL_TRANSFER`，不是教育主数据。 | **PARTIALLY_SUPPORTED** | “小型外部结构迁移/压力测试；部分支持 reliability separation 与 sensitivity。” | “教育普适性证明”“跨领域/跨人群普遍有效”“交易策略成功”“金融结果证明教育因果有效”。 |
| **C11**：Human Gate 未完成，缺正式 HUMAN_VALIDATED、充分非 AI 对照、独立 learning outcome、可靠原生 session；外部迁移不提升教育正式验证等级（`L71–73`）。 | Formal 进入条件：真实 R1/R2 → Gate PASS → `formal_gate_eligible=true` → 才能重算正式结果。 | R1/R2 完整标签、test-retest Gate、预注册阈值、独立 outcome、session 身份。 | `reports/annotation_gate_report.json` 为 `PENDING`；`FORMAL_GATE_SWITCH.md` 明确 fail-closed；项目状态列出 B001/B004/B003 等开放限制。 | 尚未运行正式 Gate；仅有完整性/自测与开发复现。 | `reports/annotation_gate_report.json`；`FORMAL_GATE_SWITCH.md`；`handoff/PROJECT_STATE.md`。 | 人工工作表当前无完整有效标签；开发输入仍为 AI provisional。 | **SUPPORTED** | “当前正式 Gate 未完成，教育主结果保持 development-only。” | “Formal 已通过”“Human R1/R2 已验证模型”“External Transfer 升级了教育正式等级”。 |
| **C12**：应同时报告 Raw、Evidence Reliability、Adjusted 和 Evaluability；16/70 readable、54 `NO_EFFECTIVE_EVIDENCE`；Score stability ≠ Evidence Support stability（`L75–77`）。 | 输出向量 `(Raw, R, Adjusted, Support/Coverage, status)`；状态为 development-only。 | 指标定义、统一分母、结果复算、状态标签、限制。 | 论文表、source of truth、core closure、Demo payload 一致；但均来自 70 条 AI provisional。 | `run_all.py` 开发复现（6 steps/32 checks）；独立复算；core closure。 | 论文 Raw/Adjusted 表；Figure 4；`reports/development/research_core_closure.md`。 | `AI_PROVISIONAL / DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。 | **DEVELOPMENT_ONLY** | “开发版方法论结论：评价结果要同时报告数值与证据支持。” | “方法已正式验证/能排序学生/提高准确率/证明学习增益”。 |
| **C13**：术语与状态语义：Raw Signal 是 Student Evidence；Reliability 是支持权重而非概率；Adjusted 不等于 AI Increment；Coverage 分母为 N=70；证据不足可 `ABSTAIN`，无有效支持为 `NO_EFFECTIVE_EVIDENCE`（`L79–81`）。 | `Score_adj=Σ(w_i y_i)/Σw_i`（`Σw_i>0`）；`Support=Σw_i`；`C_eff=Σw_i/N`；`Delta_reliable` 需先有 `Delta_raw`。 | 冻结 metric dictionary、零权重分支、ABSTAIN 与 ACCEPT 的同时 coverage/error 约束。 | `docs/metric_dictionary.md`、`docs/model_presentation/model_equations.md`、`docs/model_presentation/model_component_table.md` 一致；accuracy audit 明确不支持“准确率提升”。 | 开发状态路由、counterfactual cases、zero-weight guard；无 paired accuracy/error 的正式验证。 | `docs/model_presentation/model_component_table.md`；`reports/development/explain_records.json`。 | 开发语义已冻结；R 与参数仍未校准。 | **SUPPORTED**（定义/接口层） | “Support weight”“证据不足时拒绝/暂缓判断”“coverage 必须带分母”。 | “R 是概率”“ABSTAIN 自动提高准确率”“无支持等于零分”“Adjusted=AI Increment”。 |
| **C14**：正式 AI 增量当前不可识别；`Delta_raw=Outcome_AI−Outcome_baseline` 需要合法配对 baseline（`L83`）。 | `Delta_raw=Outcome_AI−Outcome_baseline`；`Delta_reliable=Delta_raw×R` 仅在 `Delta_raw` 已识别且 R 有定义时可谈。 | 可比 AI/non-AI 条件、独立学习 outcome、时间顺序、有效 baseline、人工 Gate 后标签、识别设计。 | 当前 pilot 没有 paired `Outcome_AI`/`Outcome_baseline`；`AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED`；Formal AIV 为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。 | 没有正式增量实验；`FORMAL_GATE_SWITCH.md` 只规定未来切换流程。 | `docs/metric_dictionary.md`；`FORMAL_GATE_SWITCH.md`；`reports/verification/formal_preflight.json`。 | 教育主数据 70 条 AI provisional；无 paired outcome。 | **NOT_SUPPORTED**（Formal 计算本身为 `NOT_RUN`） | “当前只能报告 evidence-support / observed performance；正式增量待 Gate 与 outcome 设计。” | “Adjusted Score 是 AI increment”“AI 造成学习提升”“长期学习增益/因果 effect 已估计”。 |

## 2. 六项越界专项审计

### 2.1 Development 结果写成 Formal

- **当前判断：主论文正文基本合规。** 开头 `L3–4`、结果 `L26`、限制 `L71–73`、结尾 `L83` 都保留 `DEVELOPMENT_ONLY`、`AI_PROVISIONAL`、`formal_gate_eligible=false` 或 `NOT_SUPPORTED`。
- **硬证据：** `reports/annotation_gate_report.json` 为 `PENDING`；`FORMAL_GATE_SWITCH.md` 要求真实 R1/R2、Gate PASS 和缺陷关闭后才可切换。
- **风险：** `outputs/`、PPT、Demo 或答辩口头稿若截掉 banner，会把 C2/C4/C5/C6/C7/C8/C9/C12 误读成正式结果。
- **最小修复建议：** 所有衍生表、图、caption 和口头稿首次出现数字时追加一句：`AI_PROVISIONAL / DEVELOPMENT_ONLY；N=70；formal_gate_eligible=false`。不改主线数据。

### 2.2 Observable performance 写成 true learning

- **当前判断：主论文没有直接作此越界，且 `L8/L73/L83` 明确区分。**
- **硬证据：** `research/research_spec.md` 第 6 节把“交互中可见表现证据”与长期能力、学习增量分开；`docs/claim_boundary.md` 禁止 true ability/learning gain。
- **最小修复建议：** 把所有派生材料中的“表现”限定为“可观察交互表现证据”；保留 `not true learning` 尾注。不要把 `ABL/HOT` 改名为能力分数。

### 2.3 Adjusted Score 写成 AI increment

- **当前判断：主论文明确禁止，未发现主稿直接违规句。** `L81–83` 和 `docs/metric_dictionary.md` 均明确 `Adjusted Score ≠ Reliable AI Increment`。
- **最小修复建议：** 对任何出现 “AI 增量/增量价值” 的标题或摘要，改成“AI 增量价值评价的证据支持框架”；若上下文是在报数值，使用“Adjusted evidence score/support”并附识别边界。

### 2.4 相关/伴随关系写成因果

- **当前判断：主论文已写明非因果，但组件审计显示当前只能做结构关联/假设敏感性。** 16 条 readable rows 全部 `prompt_induced=true`，没有 prompt 对照；context 没有可判读变异。
- **硬证据：** `reports/reliability_component_audit.md` 将 `λ_prompt`、`λ_context` 标为 `WEAKLY_JUSTIFIED_COMPONENT`；`reports/development/provenance_separation_audit.json` 说明来源与筛选/映射可能混合。
- **最小修复建议：** 将“prompt 风险导致/造成 support 下降”统一降为“在 prompt 惩罚假设下 support 下降”；将“context effect”降为“当前未识别，仅保留公式分支”。

### 2.5 External Transfer 写成普适性证明

- **当前判断：主论文已限定为“小型外部结构迁移验证”，没有写交易优势；仍需防止 `structural transfer：初步支持` 被单独摘出。**
- **硬证据：** BTC-USD transfer 中 risk–coverage `supported=false`；三种策略的 C strategy 为 unsupported；information-missing Gate 3 为 `supported=false`；`reports/external_transfer/external_transfer_summary.json` 只给 structural/partial。 
- **最小修复建议：** 图表/摘要统一写“外部结构压力测试（非教育泛化）”；把 transfer 完整曲线放附录，正文保留失败边界。

### 2.6 实验没有支持的漂亮结论

- **已查到的硬缺口：** `reports/development/accuracy_coverage_audit.json` 为 `NOT_SUPPORTED`，缺 `prediction` 与 `true_label`；因此没有准确率提升证据。
- **未发现主论文直接声称：** 学生能力提升、Formal AIV、交易优势、因果 effect、普适性、排名有效性；主稿反而明确禁止这些说法。
- **需要压低的漂亮表达：** “sensitivity robustness：支持”只能解释成“声明网格内的状态/排序未翻转”；“primary structure and fixed control”只能是结构选择记录，不能变成“最佳模型”。
- **最小修复建议：** 任何派生文本删去“准确率提升、性能优越、泛化已证实、模型已验证”四类句式；保留数值与实验范围。

## 3. 【论文最值得保留的 5 个 Claim】

1. **C1（框架定位）**：把赛题落到“可观察证据支持”，先于正式 AIV，且不越过真实能力/因果边界。
2. **C2（证据门控）**：70 条开发记录中仅 16 条可判读；缺证据不降成低分，零支持输出 `NO_EFFECTIVE_EVIDENCE`。
3. **C4（可复算数字表）**：ABL/HOT/Gap 的 Raw/Adjusted 数字与 `effective weight 16→6`、`coverage 0.228571→0.085714` 一一对应，且有独立复算。
4. **C5（核心发现）**：在声明的开发切片与公共缩放结构下，Score 稳定而 Evidence Support 下降；这正是论文最清晰的测量警示。
5. **C14（识别边界）**：明确 `Outcome_AI−Outcome_baseline` 尚未具备合法配对，正式 AI Increment 仍 `NOT_SUPPORTED`，防止把 Adjusted 误写成增量。

## 4. 【必须降级表达的 Claim】

以下不是要求改模型，只是把结论缩回实验实际支持的范围：

- **C3**：Reliability 是“支持权重/透明假设”，不是“可信概率”；prompt/context 不能写成已估计独立风险。
- **C5/C6**：把“稳定/稳健”限定为 70 条 AI provisional 切片与已列参数网格；禁止外推到总体、人群或未来数据。
- **C7**：消融只能定位 Support 的结构变化；不能说某组件提升准确率、产生独立因果效应，尤其 context 当前无变异。
- **C8**：替代模型只是结构比较；保留乘法模型是透明、无新增参数的操作选择，不是性能冠军或唯一最优。
- **C9**：反例是路由/拒判示例；没有 true label/outcome，不能写预测对错或真实能力。
- **C10**：External Transfer 只能叫小型结构迁移/压力测试；保留第三策略和 risk–coverage 失败边界。
- **C12**：方法论结论只在 development-only 语境成立；“可用”应改为“可用于形成性诊断原型/待 Gate 验证”。

## 5. 【应该删除的 Claim】

主论文当前未发现必须删除的正向句；它已在 `L38/L49/L53/L73/L81/L83` 主动排除下列说法。若这些句子出现在 PPT、Demo、摘要、答辩或旧稿中，应删除而不是仅加弱限定：

- “Formal AIV 已得到/模型已通过 Gate/可以给学生排名”；
- “Adjusted Score 是 AI increment、学习增益或真实能力提升”；
- “prompt/context 惩罚已经识别出因果影响”；
- “ABSTAIN 带来准确率提升”；
- “External Transfer 证明普适性、教育因果有效或交易优势”；
- “乘法模型已被证明唯一最优/预测优越”。

## 6. 【目前证据最强的一张表】

**论文 Raw / Reliability / Adjusted 表（`paper/submission_candidate.md:L18–24`）**。

理由：每个数字都能回溯到 `reports/development/raw_adjusted_metrics.csv` 和 `reports/verification/core_numbers_source_of_truth.json`；`ABL/HOT/Gap`、support、coverage 的分子/分母可独立复算，且 `coverage` 已能明确写成 `effective weight / 70 development records`。限制是它仍然是 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 描述表。

## 7. 【目前证据最强的一张图】

**`reports/development/core_figure_4_bounds_support.svg`（Score stability vs evidence support）**。

理由：红线（归一化 Score）与蓝线（`effective weight/70`）直接对应 `reports/development/partial_identification_summary.json` 和 693 格参数扫描；图中明确标出 `lambda_context=0`、`r_medium=0.75`、`lambda_prompt=1` 时 `NO_EFFECTIVE_EVIDENCE`，并写明 Score undefined 而非 0。限制是它表达的是 assumption-based sensitivity behavior，不是统计置信区间、因果效果或外部稳健性。

## 8. 【还缺哪一个实验才能闭环】

若目标是把当前开发版链条闭到**正式 AI Increment**，最小的单一实验应是：

> **在完成冻结的 Human R1/R2 test-retest Gate 后，预注册一项可比 AI / non-AI 条件的配对学习结果实验：有处理前基线、独立（撤去 AI）即时与延迟/迁移 outcome、明确时间顺序和对照，且结果标签与 Evidence 记录可合法配对。**

它一次性补上 C11/C14 缺失的人工测量可信度、`Outcome_AI`/`Outcome_baseline`、独立学习 outcome 和识别条件。仅完成 Human Gate 可以验证标注可靠性，但不能单独证明 AI 因果增量；仅做 transfer 或 sensitivity 也不能替代该实验。

## 9. 评委从题目走到结论的逻辑链（11 步）

1. **题目对象**：评价 AI 辅助学习中的增量价值，但先问日志中的分数是否有可归因的学生证据。
2. **观测边界**：当前能观察的是学生交互文本中的 Evidence，不是长期真实能力；AI 话语、上下文缺失和标注不确定性要分开。
3. **核心假设**：仅 L1–L6 的可判读 Student Evidence 进入评分；`NO_EVIDENCE/UNDETERMINED` 不等于低分。
4. **开发数据**：70 条 `AI_PROVISIONAL` 记录中只有 16 条可判读，54 条进入 `NO_EFFECTIVE_EVIDENCE`。
5. **数学模型**：用 `I(observable)×confidence×(1-λ_prompt p)×(1-λ_context t)` 计算支持权重；它是 support，不是概率/因果系数。
6. **输出结构**：同时报告 Raw Score、Evidence Reliability、Adjusted Score、Support/Coverage 和 `ABSTAIN/NO_EFFECTIVE_EVIDENCE` 状态。
7. **验证动作**：对同一冻结输入做参数敏感性、M0–M3 消融、替代函数比较和记录级反例检查。
8. **主要结果**：当前切片中 ABL/HOT/Gap 保持 `3.5625/0.375/1.125`，support 从 `16` 降至 `6`，coverage 从 `0.228571` 降至 `0.085714`。
9. **结果解释**：这是 readable rows 的公共缩放结构和声明参数网格下的开发现象；它说明 Score 与 Evidence Support 可能分离。
10. **外部边界**：BTC-USD 只提供小型结构迁移压力测试，存在部分支持和失败 Gate，不能升级为教育普适性或因果证据。
11. **结论等级**：当前可保留的是 development-only 的 evidence-support 方法论结论；正式 AI Increment、真实学习增益和学生排名必须等待 Human Gate 与配对独立 outcome 实验。

## 10. 最小修复清单（不改主线）

1. 任何 derived figure/table/caption 首次出现数字时，带上 `AI_PROVISIONAL / DEVELOPMENT_ONLY / N=70`。
2. 把“sensitivity robustness：支持”统一限定为“声明参数网格内无状态/排名翻转”。
3. 把“prompt/context 导致”统一改成“在 prompt/context 惩罚假设下”。
4. 在 External Transfer 标题或图注中追加“结构迁移压力测试，不是教育普适性证明”。
5. 保留 `Adjusted Score ≠ AI Increment`、`AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED` 和 `formal_gate_eligible=false` 原样语义。

**审计结论：** 开发版 evidence chain 可复算、可审计；Formal AI Increment chain 尚未闭环。主论文没有发现必须直接改写的越界正向 Claim，但派生材料必须执行上述最小措辞收缩。

