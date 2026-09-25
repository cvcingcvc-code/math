# 认知证据标注规则手册 · Pilot 执行澄清件 V0.1.1

版本：V0.1.1｜基线：`docs/annotation/annotation_manual_v0.1.md`（SHA-256 `F8E42B177E5DFF335F7C42C58B2B4A1C80666E3C5CE89226305AE5904C64F119`，未改动）
状态：**冻结并用于正式人工 Pilot**（2026-09-25 19:40，真实人工标签产生前确认）。本版本冻结后不得根据第一轮标注结果临时修改；若确需修改，必须升版本号并将修改后的样本作为新的验证阶段处理。
依据：`reports/pilot_rule_failure_report.md` 记录的 8 个规则失败点。这些失败点来自 **AI 探索性预标注**，不是人工标注证据，也不能当作人工一致性结果。

## 0. 本文件的性质与边界

1. V0.1.1 **不修改** V0.1 的任何构念、等级定义、允许值、置信度规则或拒绝规则。
2. V0.1.1 只做一件事：把 V0.1 中已隐含、但在原文本下无法被两名标注者独立复现的判断，写成**可执行的判定程序**。
3. **V0.2 仍然保留给真实人类 pilot 结束后的修订**（V0.1 第 七.2.8 条）。V0.1.1 不预设 V0.2 的任何结论。
4. 若 V0.1.1 与 V0.1 冲突，**以 V0.1 的构念为准**；该冲突须写入 `handoff/BLOCKERS.md` 并回到 Gate，不得由标注者自行裁定。
5. V0.1.1 不放宽下列冻结约束：双轴独立、AI 内容不自动归学生、low 拒绝确定标签、未知不填 L1、保留初始双标与裁决轨迹、日志不直接代表长期能力。
6. V0.1.1 不引入任何数值阈值（时间窗、相似度）。V0.1 第 十 节明确要求这些由真实 pilot 决定。

## 1. 判定流水线（固定顺序，不可跳步）

每条记录固定按 S1→S8 判定；**后一步不得回改前一步的结论**。此顺序是 V0.1 第 七.2.4 条"先定角色/来源，再定两轴"的可执行化。

| 步 | 判定 | 产出字段 |
|---|---|---|
| S1 | 发送角色 | `speaker_role` |
| S2 | 内容来源（是否搬运） | `content_relation` |
| S3 | 任务识别 + 执行者 | `task_source`、`task_actor` |
| S4 | Task Bloom | `task_bloom`、`task_confidence` |
| S5 | 学生新增判定 | `evidence_span`、`partial_rewrite`、`prompt_induced`、`scaffold_share` |
| S6 | Student Evidence Bloom | `student_evidence_bloom`、`evidence_confidence` |
| S7 | 正确性（与等级分离） | `correctness` |
| S8 | 置信度与歧义 | `confidence`、`ambiguity_type`、`needs_second_review` |

## 2. 上下文窗口与 U / N/A 边界（关闭失败点 1）

**最低前文**：当前 turn 之前最近的 AI 轮（最多 2 条）+ 最近的学生轮（若存在）。

- `prior_ai_context` **只取** `source_row_id` 内、当前 turn **之前**（`turn_index_in_session` 更小）的 AI 轮，按索引升序拼接；超过 2 条则截断并置 `context_truncated=true`。
- **禁止**使用当前 turn **之后**的任何 AI 文本作为上下文。这是硬性禁令，见 `handoff/BLOCKERS.md` B006。
- 无前文时记为 `[NO_PRIOR_AI_TURN_IN_SOURCE_EXPORT]`，不得用任何其他内容替代。

**U 与 N/A 的判定顺序**（先问是否教育任务，再问是否可恢复）：

| 顺序 | 问题 | 结论 |
|---|---|---|
| 1 | 文本是否承载教育语境下的任务？ | 否 → `Task=NOT_APPLICABLE` |
| 2 | 任务对象与预期操作能否从窗口前文恢复？ | 否 → `Task=UNDETERMINED` |
| 3 | 能否定位到某级的必要条件？ | 是 → 赋 L1–L6；否 → `UNDETERMINED` |

- 单字母选项、标题、课程代码、"重点是什么"一类条目：**默认落入顺序 2**，除非窗口前文直接给出对象与操作。
- 纯系统通知、平台状态、纯社交寒暄 → `NOT_APPLICABLE`，不得记 U。
- Student 轴同理：角色可判但无可归属证据 → `NO_EVIDENCE`；关键前文缺失导致无法判断是否有新增 → `UNDETERMINED`。二者不得互换。

## 3. 任务来源与执行者（关闭失败点 2）

新增两字段，必须填写：

- `task_source` ∈ {`student_request`, `ai_prompt`, `embedded_question`, `system`, `mixed`, `unknown`}
- `task_actor` ∈ {`student`, `ai`, `both`, `unknown`}

**Task Bloom 按任务本身要求什么认知操作判定，不按谁执行判定。**

| 情形 | Task | Student |
|---|---|---|
| AI 提问，学生回答 | 按 AI 所问判（`ai_prompt` / `ai`） | 按学生回答判 |
| 学生转述 AI 的问题 | 按该问题判，`task_source=ai_prompt`（转述不改变任务） | 无本人操作则 `NO_EVIDENCE` |
| 学生请求 AI 生成方案 | 按请求目标判，`task_actor=ai` | 裸请求 → `NO_EVIDENCE`，不默认 L1 |
| 学生提出方案，AI 执行 | 按方案任务判，`task_actor=both` | 按学生方案判 |
| 任务对象/执行者仍不明确 | `UNDETERMINED` + `task_unspecified` | 相应轴按 S5 判 |

## 4. 学生"新增操作"门槛（关闭失败点 3）

赋 Student 轴 L1–L6 之前，必须完成三步，缺一不可：

1. **定位 `evidence_span`**：学生文本中承载该认知操作的可引用片段。**无 span 不得赋级。**
2. **判断 `content_relation`** ∈ {`independent`, `reworked_with_addition`, `copied_verbatim`, `reworked_without_addition`, `not_comparable`}
3. **映射**：

| content_relation | Student 轴 |
|---|---|
| `independent` | 满足某级必要条件 → 赋该级 |
| `reworked_with_addition` | **新增部分本身**满足某级必要条件 → 赋该级，并置 `partial_rewrite=true` |
| `copied_verbatim` | `NO_EVIDENCE`（V0.1 第 一.4.3 条：直接搬运不得计入） |
| `reworked_without_addition` | `NO_EVIDENCE` |
| `not_comparable` | `UNDETERMINED` |

**"部分改写"边界（可复现判据）**：
- 属于 `reworked_without_addition`：换标题、调整段落顺序、同义替换、增删连接词与套话、把前文长句拆成短句。
- 属于 `reworked_with_addition`：新增**至少一个前文未出现的实质关系、条件、步骤、约束或分解**。
- 判断只依据窗口内可见前文；前文缺失 → `not_comparable`，不得凭写作风格推断来源（V0.1 第 二 节已禁止）。

## 5. 脚手架与学生证据分开编码（关闭失败点 4）

- `prompt_induced` ∈ {`true`, `false`}：该学生的可见操作是否由前文 AI 提示直接触发。
- `scaffold_share` ∈ {`high`, `medium`, `low`, `none`}：前文已提供多少推理骨架（`high` = 前文已给出完整推理链条，学生只填充事实）。

规则：

1. 强引导下**完成的操作仍然赋级**，不得因 `prompt_induced=true` 自动降为 `NO_EVIDENCE`。
2. 也不得把 `scaffold_share=high` 的完成与独立生成混为一类而不标注。
3. 报告时必须能按 `prompt_induced` 与 `scaffold_share` 分层复算，否则该维度视同未编码。
4. 前文 AI 内容本身**永远不计入**学生证据（V0.1 第 二 节）。

## 6. 复合任务、分段与短回合（关闭失败点 5）

- **默认单标签**：按"完成任务不可缺少的**主导**认知操作"判；`task_bloom` 与 `student_evidence_bloom` 各填一个值。
- **触发分段**（满足任一）：① 任务含两个及以上必须由**不同**认知操作才能完成的子任务；② 学生文本包含由不同认知操作完成的**多个独立证据段**。
- **分段规则**：`record_id` 加后缀 `#s01`、`#s02`；`parent_turn_id` 指回原 turn。**分段不增加发送次数**，不得用来虚增 turn 数或证据量。
- **短回合**：**不设长度阈值**。长度不是判据；判据是能否定位到认知操作。一个词在有明确前文时可为 L1，无前文时为 `UNDETERMINED`。
- 主导操作无法在规则下排他确定 → `UNDETERMINED`，**不取最大值**。

## 7. 正确性与等级分离（关闭失败点 6）

- 新增 `correctness` ∈ {`correct`, `incorrect`, `partially_correct`, `not_assessable`}。
- **Bloom 等级只编码操作结构，不编码正确性。** 错误的高阶操作仍是该高阶（V0.1 L3/L5 边界规则已如此规定）。
- **禁止**"因为算错所以降一级"。`correctness` 只用于下游误差传播分析，不进入 Bloom 标签、不进入一致性分母。
- 在不引入标准答案就无法判断时 → `not_assessable`。

## 8. L3–L6 最小判据与边界（关闭失败点 7）

从高到低检验；某级**完整性检验**未通过则降一级再检验。

| 级 | 完整性检验（必要且可检验） |
|---|---|
| L6 | 目标/约束 **+** 超出可见已有方案的实质结构 **+** 可实施说明，三元齐备 |
| L5 | 评价对象 **+** 标准 **+** 相关证据 **+** 判断，四元齐备 |
| L4 | 至少一个前文未提供的实质关系/分解/冲突，并说明其对问题的作用 |
| L3 | 已知规则或程序在具体输入上的可追溯执行（输入→规则→输出可见） |

| 常见误判 | 正确判定 | 判据 |
|---|---|---|
| 出现"分析/评价/创新"动词即取高级 | 按判据检验 | 动词不是证据（V0.1 第 一.1 条） |
| 应用公式后又比较 | L3 还是 L4 | 比较是否产出前文未给的**实质关系** |
| 给出评价但没有可定位标准 | 至多 L4 | L5 需要标准真实参与判断 |
| 按公式重算并说"不一致" | L3；若把结果与标准相连形成判断则 L5 | V0.1 L5 边界规则 |
| 比较并选出最佳**现成**方案 | L5 | 不是创造 |
| 换名、换参数、堆叠工具名 | 不构成 L6 | 无实质结构新增 |
| 照搬 AI 完整方案 | `NO_EVIDENCE` | `copied_verbatim` |
| 学生做出高阶但错误的操作 | 保持该高阶 | 正确性单独记 `correctness` |

## 9. speaker / 来源 / 智能体不确定（关闭失败点 8）

- `speaker_confidence < 0.8` **不自动改判**；进入复核。`speaker_role=Unknown` 时 Student 轴为 `UNDETERMINED`（V0.1 已定）。
- `agent_type=unknown` **必须保留**（D011）；不得删除，不得按课程名/文件名反推 agent。
- **三个"未知"必须分开记录，不得合并**：① speaker 未知；② 内容来源未知；③ Bloom 不可判。字段：`speaker_unknown_reason`、`source_unknown_reason`。
- **盲标要求**：`agent_type` 与 `path_case` 对标注者**遮蔽**（V0.1 第 七.3 条"避免路径名称诱导"）。分析侧另表保存映射。

## 10. 执行表字段（V0.1 第 七.1 条授权）

V0.1 允许"执行窗口另建映射/审计表"。V0.1.1 定义**执行表 = V0.1 的 8 列最小表 + 下列字段**：

`task_source`, `task_actor`, `evidence_span`, `content_relation`, `partial_rewrite`, `prompt_induced`, `scaffold_share`, `correctness`, `speaker_unknown_reason`, `source_unknown_reason`, `context_truncated`, `elapsed_sec`(可选)

分离要求：**标注者可见字段**（8 列 + 上列）与**分析侧遮蔽字段**（`agent_type`、`path_case`、`pilot_sampling_strata`、AI 预标注、`review_sample_type`）必须落在不同文件，不得同表下发。

## 11. 变更追溯（V0.1 → V0.1.1）

| 失败点 | V0.1 原文位置 | V0.1.1 处理 | 是否改变判级语义 |
|---|---|---|---|
| 1 Task 指代不完整、U/N/A 边界 | 第 一.4、第 五 | 第 2 节：判定顺序 + 最低上下文窗口 | 否 |
| 2 任务对象/执行者分歧 | 第 一.4.2、第 五 | 第 3 节：`task_source`/`task_actor` + 决策表 | 否 |
| 3 "新操作"门槛不可操作 | 第 一.4.3、第 二 | 第 4 节：`evidence_span` + `content_relation` 映射 | 否 |
| 4 脚手架影响未分开 | 第 五、决策表 | 第 5 节：`prompt_induced`/`scaffold_share` | 否 |
| 5 复合任务与短回合 | 第 一.1 | 第 6 节：分段触发条件、无长度阈值 | 否 |
| 6 正确性与层级混淆 | L1–L6 各边界规则 | 第 7 节：`correctness` 独立字段 | 否 |
| 7 L3/L4/L5/L6 边界 | 四、L1–L6 | 第 8 节：完整性检验 + 误判表 | 否 |
| 8 speaker/agent/source 不确定 | 第 二、第 六 | 第 9 节：三未知分离 + 盲标 | 否 |

## 12. V0.1.1 **没有**决定、留给真实 pilot 的事项

不得声称以下任一已解决：

- 具体数值阈值（时间窗、文本相似度、脚手架比例）。
- 各等级实际混淆率、`UNDETERMINED` / `NO_EVIDENCE` 实际比例。
- 两名标注者能否在 `evidence_span` 上一致定位。
- 人工成本（每条耗时）与停止标准、样本量。
- 六级与三阶在一致性、拒判率、信息损失上的实际取舍。
- `prompt_induced` / `scaffold_share` 分层的实际分布。
- 智能体路径偏差是否存在（仍为待检验机制假设，非结论）。

## 13. 与冻结决策的一致性

| 决策 | V0.1.1 是否触碰 |
|---|---|
| D003 双轴分轴标注 | 保持 |
| D007 不得把 AI 标注称为人工标注 | 保持；本文件依据的失败点来自 AI 预标注，已声明 |
| D008 人工标注完成前不计算正式 Kappa/Alpha | 保持；V0.1.1 不产生任何一致性数值 |
| D011 unknown agent 保留并报告 | 第 9 节强化 |
| D013 算法由真实失败点驱动 | 本文件即由失败点驱动，未先选方法 |
| D014 重大方向改变须经 Gate Review | 本文件为执行澄清，非方向改变；已于 2026-09-25 19:40 在真实人工标签产生前冻结并确认 |