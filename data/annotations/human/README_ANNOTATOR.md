# Pilot 人工标注执行说明（标注者必读）

配套文件：`pilot_worksheet_A.csv`、`pilot_worksheet_B.csv`（UTF-8 BOM，可用 Excel 直接打开）

在开始之前，**必须依次读完**：

1. `docs/annotation/annotation_manual_v0.1.md` —— 规则本体（构念与等级定义）
2. `docs/annotation/annotation_clarification_v0.1.1.md` —— 可执行判定程序（判定顺序、字段、边界）

两者冲突时以 V0.1 的构念为准，并立即停止、向负责人报告，不要自行裁定。

---

## 一、这次要做的是什么

对 **70 条**学生与 AI 的交互记录做布鲁姆**双轴**认知标注：

- **Task Bloom**：这个任务本身要求什么认知操作（L1–L6 / `NOT_APPLICABLE` / `UNDETERMINED`）
- **Student Evidence Bloom**：这名学生**在本条中实际展示了**什么认知证据（L1–L6 / `NO_EVIDENCE` / `NOT_APPLICABLE` / `UNDETERMINED`）

两轴**独立判断**。不得因为 Task 是 L5 就把 Student 也填 L5。

**这不是**给学生的能力打分，也不是评价 AI 回答质量。你只记录"这条文本里能观察到什么"。

---

## 二、盲标纪律（必须遵守）

1. **第 1 轮看不到任何自动标签**。工作表里没有 AI 预标注，这是刻意的；不要去别处找。
2. 表中**没有**智能体名称、路径名称、学期、学号。这是刻意遮蔽的（避免"探知侠/逆行侠"这类名字诱导判断）。
3. **两位标注者独立完成后才允许交流**。完成后不要修改自己已交的版本。
4. 不得用写作风格、文本长度、"像不像 AI"来判断来源。
5. `prior_ai_context` 只包含**本条之前**的 AI 内容，用于判断"学生是不是在搬运已有内容"。它是判断依据，**不是**学生证据。

---

## 三、每条怎么填（固定顺序，不要跳步）

| 步 | 做什么 | 填哪些列 |
|---|---|---|
| S1 | 确认发送角色 | `speaker_role_check`（预期多为 `student`；若不是，照实填） |
| S2 | 判断学生内容与前文 AI 的关系 | `content_relation` |
| S3 | 识别任务 + 谁执行 | `task_source`、`task_actor` |
| S4 | 判 Task 等级 | `task_bloom`、`task_confidence` |
| S5 | 定位学生证据片段 | `evidence_span`、`partial_rewrite`、`prompt_induced`、`scaffold_share` |
| S6 | 判 Student Evidence 等级 | `student_evidence_bloom`、`evidence_confidence` |
| S7 | 单独记正确性 | `correctness` |
| S8 | 记置信度与歧义 | `confidence`、`reason`、`ambiguity_type`、`needs_second_review` |

### 每行都必须填（9 列）

`speaker_role_check`、`task_bloom`、`task_confidence`、`student_evidence_bloom`、`evidence_confidence`、`confidence`、`reason`、`ambiguity_type`、`needs_second_review`

### 只在适用时填（条件字段）

| 字段 | 什么时候必填 |
|---|---|
| `task_source`、`task_actor` | `task_bloom` 是 L1–L6 时 |
| `evidence_span`、`content_relation`、`correctness`、`prompt_induced` | `student_evidence_bloom` 是 L1–L6 时 |
| `partial_rewrite` | `content_relation = reworked_with_addition` 时 |
| `speaker_unknown_reason` | `speaker_role_check = unknown` 时 |
| `source_unknown_reason` | `content_relation = not_comparable` 时 |
| `elapsed_sec` | 选填：本条大约花了多少秒 |

### 允许值

- `task_bloom`：`L1` `L2` `L3` `L4` `L5` `L6` `NOT_APPLICABLE` `UNDETERMINED`
- `student_evidence_bloom`：`L1` `L2` `L3` `L4` `L5` `L6` `NO_EVIDENCE` `NOT_APPLICABLE` `UNDETERMINED`
- 三个置信度列：`high` `medium` `low`
- `task_source`：`student_request` `ai_prompt` `embedded_question` `system` `mixed` `unknown`
- `task_actor`：`student` `ai` `both` `unknown`
- `content_relation`：`independent` `reworked_with_addition` `copied_verbatim` `reworked_without_addition` `not_comparable`
- `correctness`：`correct` `incorrect` `partially_correct` `not_assessable`
- `scaffold_share`：`high` `medium` `low` `none`
- `partial_rewrite` / `prompt_induced` / `needs_second_review`：`true` `false`
- `ambiguity_type`：`none`，或多个代码用 `;` 分隔（代码见表末）

---

## 四、最容易出错的 6 件事

1. **把任务要求当成学生证据。** Task=L5 而学生只说"好的" → `student_evidence_bloom = NO_EVIDENCE`。
2. **被动词骗了。** 出现"分析/评价/创新"不等于高阶；按 V0.1.1 第 8 节的完整性检验判。
3. **把"被提示"等同于"没证据"。** 强引导下完成的真实操作仍然赋级，同时填 `prompt_induced=true` 和 `scaffold_share`。
4. **把搬运当成学生证据。** 粘贴 AI 原文 → `copied_verbatim` → `NO_EVIDENCE`。只换标题/换顺序/同义改写 → `reworked_without_addition` → `NO_EVIDENCE`。
5. **因为算错就降级。** 错误的高阶操作仍是该高阶；正确性写进 `correctness`。
6. **用 `UNDETERMINED` 图省事。** 它是"规则下确实判不了"，必须能在 `reason` 里说清缺什么。反过来，证据不够时也不许硬凑一个等级。

---

## 五、置信度与二审

- `high`：角色与来源可判、证据位置完整、无会改变结论的竞争解释。
- `medium`：核心证据成立，但有轻微边界疑问 → **`needs_second_review` 必须 `true`**。
- `low`：缺关键语境或两个以上等级无法排除 → **受影响那轴必须 `UNDETERMINED`**，候选等级写在 `reason`（如 `candidates=L4|L5`），**`needs_second_review` 必须 `true`**。
- `NO_EVIDENCE` / `NOT_APPLICABLE` **可以**是 `high`。

**不得**把 `low` 改写成最小候选、最大候选、随机标签或 L1。

---

## 六、`ambiguity_type` 代码

`role_boundary`、`source_attribution`、`context_missing`、`task_unspecified`、`level_boundary`、`multi_operation`、`prompt_induced`、`copy_suspected`、`duplicate`、`link_only`、`correctness_uncertain`、`other`

`none` 不能与其他代码同时出现；`other` 必须在 `reason` 里解释。

---

## 七、交回方式

1. 只改自己那一份工作表，**另存为** `pilot_worksheet_<你的编号>_submitted.csv`。
2. **不要覆盖** `pilot_worksheet_A.csv` / `_B.csv` 原件。
3. 在交回时另外报告：总耗时（分钟）、你觉得最难的 3 条 `record_id`、以及任何你认为手册说不清的地方。
4. 规则说不清的地方**不要自己发明规则**，写进这条的 `reason` 并报告。

## 八、诚实要求

- 不得编造标签、不得参照别人的结果、不得为了让一致性好看而修改判断。
- 标注结果会用于计算一致性系数，并作为是否进入全量标注的判据。
- 你的**第一轮独立判断**本身就是数据；事后"修正"第一轮会破坏整个设计。