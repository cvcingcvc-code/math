# AI 辅助标注审计（70/70）

- 生成时间：2026-09-26T11:42:08
- 数据身份：**AI_ASSISTED / DEVELOPMENT_ONLY / formal_gate_eligible=false**
- **NOT FORMAL HUMAN VALIDATION**：这不是 HUMAN_R1/R2，不得进入 Formal Human Gate，也不得与人工标签混合计算一致性。
- 输入范围：仅使用盲标表可见列（record_id、student_text、prior_ai_context、context_truncated）；未读取人类已填标签列，未使用 AI_PROVISIONAL 预标注作为答案来源。
- 规则依据：`annotation_manual_v0.1.md` + 冻结的 `annotation_clarification_v0.1.1.md`。

## 1. 完成情况

- 记录数：70；record_id 唯一：70；漏行/重复：0。
- 必填字段空值：0；枚举违规：0；输入字段（student_text/prior_ai_context 等）与来源逐项一致。

## 2. 标签分布

| Task Bloom | n |
|---|---:|
| L1 | 4 |
| L2 | 22 |
| L3 | 4 |
| L4 | 15 |
| L5 | 4 |
| L6 | 1 |
| STATUS:NOT_APPLICABLE | 2 |
| STATUS:UNDETERMINED | 18 |

| Student Evidence | n |
|---|---:|
| L1 | 5 |
| L2 | 18 |
| L3 | 4 |
| L4 | 7 |
| L5 | 4 |
| L6 | 1 |
| STATUS:NO_EVIDENCE | 28 |
| STATUS:UNDETERMINED | 3 |

- **NO_EVIDENCE = 28**；**UNDETERMINED（Student 轴）= 3**。
- Task 轴 UNDETERMINED = 18；Task NOT_APPLICABLE = 2。

## 3. 置信度与复核

- confidence 分布（取两轴及角色/来源最低者）：{'medium': 31, 'high': 20, 'low': 19}
- task_confidence：{'high': 32, 'medium': 21, 'low': 17}；evidence_confidence：{'high': 43, 'medium': 24, 'low': 3}
- needs_second_review=true：**50** 条（所有 medium/low 均置 true，符合手册第六节）。
- prompt_induced=true：41 条（仅统计赋级记录）。
- content_relation 分布：{'independent': 32, 'reworked_with_addition': 7, 'copied_verbatim': 4, 'reworked_without_addition': 2, 'not_comparable': 1}
- correctness 分布：{'not_assessable': 27, 'correct': 10, 'partially_correct': 2}

## 4. 歧义类型

| ambiguity_type | n |
|---|---:|
| level_boundary | 28 |
| none | 20 |
| task_unspecified | 17 |
| source_attribution | 5 |
| correctness_uncertain | 4 |
| prompt_induced | 2 |
| other | 1 |
| context_missing | 1 |

## 5. 主要边界类型

- **首轮主题/标题式陈述**：15 条（P001/P002/P005/P006/P007/P008/P009/P010/P031/P052/P089/P096/P121/P127/P131）任务对象不可恢复，Task=UNDETERMINED、Student=NO_EVIDENCE；另有 P004 单字母选项、P050 选项复述。
- **搬运与复述**：copied_verbatim 4 条（P050/P059/P061/P076）、reworked_without_addition 2 条（P024/P097）→ Student=NO_EVIDENCE；这类记录是 AI 辅助环境中最容易被误计为证据的类型。
- **强脚手架下的短答**：P088“更真实”、P077“BD”、P104“根据概率大小来判断？”：仅给出结论或选择，无机制说明；分别记 L2 弱证据、NO_EVIDENCE、UNDETERMINED。
- **正确性与等级分离**：P014 关键要素不完整、P032“小样本适合判别分析”与前文冲突，均只调整 correctness，不降 Bloom 等级。
- **上下文截断/不可读**：P020 回答对象不在窗口内（context_missing）；P053 文本错乱无法定位操作 → Student=UNDETERMINED。
- **近重复记录**：P137 与 P138 文本几乎相同（不同 record_id），本轮按各自记录独立编码，未做去重。

## 6. 身份与不可用声明

- 本文件所有标签由 AI 辅助生成，`annotation_source=AI_ASSISTED`，`annotation_status=DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。
- 不得用于正式 Human Gate、正式一致性系数、Formal AIV、学生排名或因果结论；不得改写为人工标注。
- 人工 R1 检查点哈希、R2 空白状态与 `validation/gate_thresholds.json` 均未修改（见元数据 `source_hashes` / `untouched`）。
