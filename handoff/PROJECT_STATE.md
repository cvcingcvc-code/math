# PROJECT STATE

## Competition

中国第一届数学建模黑客松 · 赛道一

题目：《新时代教育中 AI 增量价值评价的建模方法》

研究方向：《考虑智能体引导偏差与标注不确定性的教育 AI 增量价值评价》

## Research object

学生在 AI 辅助学习中的可观察交互与学习表现证据。

不直接等同于长期稳定能力、独立学习增益或 AI 因果效应。

## Current stage

S4 Pilot Annotation Gate

当前状态：**BLOCKED_BY_HUMAN_ANNOTATION**（S4 协议冻结，2026-09-25 19:40）

冻结决定：Gate 使用 70 条核心样本；B010 采用同一标注者两轮、间隔至少 24 小时的 test-retest。当前 R1/R2 均为空，尚未产生任何真实人工标签、一致性结果或 Gate 通过结论。

前状态为 `BLOCKED_BY_ANNOTATION`。协议侧阻塞（B002）已产出澄清件，标注包与 Gate 分析器已交付；**剩余阻塞是真实人工标签尚未返回**，该项无法由 AI 窗口推进，也不得虚构。

尚未进入：
- 全量 Bloom 标注
- 正式一致性实验
- 最终 CTQ/DHI/AIV
- PSM
- DID
- 正式因果模型

## Canonical dataset

2025 秋：
- 原始问答 845 rows
- URL-only 排除 21
- 纳入 824 rows
- 295 students
- 5019 turns
- 观察期 2025-10-09 至 2026-02-05

2026 春：
- 聚合原表 1925 rows / 528 ids
- 明确参与名单并集 131 students
- 日志匹配 109 students / 482 rows
- 排除空文本 13
- 排除 URL-only 68
- 最终 401 rows
- 106 students
- 2009 turns
- 观察期 2026-03-19 至 2026-07-27

总有效 turns：7028。

## Important data limitations

1. 2026 春原始导出不是天然春季队列；
2. 约 22 名明确参与学生没有匹配日志；
3. 缺日志不能解释为未使用 AI；
4. 秋季班级无法逐人完整映射；
5. 原始数据没有真实 session_id；
6. 当前使用原始记录行为 session_proxy；
7. CTQ 等序列指标不得跨 session_proxy 计算；
8. speaker parser 当前是全覆盖，不代表 100% accuracy；
9. 4 条连续学生标记异常已进入低置信审计；
10. agent_type unknown：740 / 7028 turns ≈ 10.5%；167 / 1225 session_proxy ≈ 13.6%；
11. Unknown agent 不得直接删除。

## Canonical Pilot

正式 Pilot V1：`data/processed/pilot_sample.csv`，N = 140（完整性已核验，见下）。

构成：
- 秋 70
- 春 70
- 探知侠 65
- 逆行侠 18
- 数模全才 23
- 数模匹配 5
- AI 学伴 6
- unknown agent 23

56 条旧 Pilot 不是正式 Pilot，不得混入 Kappa / Alpha / AIV 正式实验。

## Integrity verification (2026-09-25)

`src/verify_pilot_integrity.py`：21/21 冻结不变量通过。

- N=140、pilot_id 唯一且为 P001–P140、无旧 56 条 ID 体系混入；
- 140/140 均为 student turn（分析单位为"学生轮"）；
- AI 预标注 140 行、`annotator_type=LLM_EXPLORATORY_NOT_HUMAN`（D007 合规）；
- 复核队列 70 = 50 疑难 + 20 随机审计，manual_version=V0.1；
- `annotation_manual_v0.1.md` SHA-256 = CHANGELOG 记录值（未改动）；
- `prior_ai_context` 可被独立重建复现：prelabel 140/140、queue 70/70。

## Defect register（未解决）

**S4-F01（HIGH）** `pilot_sample.csv::ai_context_text` 是**未来** AI 内容，不是前文。

- 48/140 条在该 source_row 内**根本没有**更早的 AI 轮，但该列仍非空；
- 其中 45 条与**其后**的 AI 轮匹配；26 条完全相同、63 条为其前缀。
- 结论：该列**不是良定义的前文语境字段**，用于标注会把 AI 回答泄漏进 Task/Evidence 判断（相似性、搬运判定、任务复述）。
- 处置：`src/build_annotation_worksheets.py` 一律不使用它，前文由 `clean_interactions.csv` 的轮次顺序严格重建。

**S4-F02（HIGH）** `pilot_human_review_queue.csv` 不是盲标表。

- `task_bloom`、`student_evidence_bloom`、`confidence`、`reason`、`content_source_attribution` 已填入 AI 预标注，且含 `agent_type`、`path_case`。
- 直接下发会让标注者锚定自动标签，违反 manual V0.1 第 七.3 条（第一轮不看自动标签、遮蔽路径名称）。
- 处置：改发 `data/annotations/human/pilot_worksheet_A|B.csv`（已核验零泄漏列），映射另存 `data/annotations/_keys/pilot_worksheet_key.csv`。

## Current annotation status

140 条已有 AI 探索性预标注。人工复核计划：50 条疑难样本 + 20 条固定随机正常样本。

**已交付并可直接执行**：
- 澄清件 `docs/annotation/annotation_clarification_v0.1.1.md`（待负责人签署）
- 盲标表 A/B：`data/annotations/human/pilot_worksheet_A.csv`、`_B.csv`（70 行，无泄漏列）
- 标注者说明：`data/annotations/human/README_ANNOTATOR.md`
- B010 R1/R2：`pilot_worksheet_A.csv` →（至少 24 小时）→ `pilot_worksheet_A_retest.csv`；这是同一标注者的 test-retest reliability，不是 inter-rater reliability。
- Gate 分析器：`src/annotation_gate_report.py`（标签返回后一条命令出 Gate Report）
- 一键入口：`src/run_s4_gate.py`

**仍缺**：真实人工双标结果。当前 `pilot_worksheet_A|B.csv` 标注列全为空。

禁止在人工标注完成前报告正式 Cohen Kappa、weighted Kappa、Krippendorff Alpha。

## Pending sign-off（不得由 AI 窗口自行决定）

1. `annotation_clarification_v0.1.1.md` 已于 2026-09-25 19:40 在真实人工标签产生前冻结并采纳为 Pilot 执行规则；冻结后不得根据 R1 结果临时修改。
2. `validation/gate_thresholds.json` 已于 2026-09-25 19:40 在查看任何真实标签前确认为 `preregistered: true`；不得根据结果回改。
3. B008 已冻结为当前 Gate 使用 70 条核心样本；原始 140 条 Pilot 保留，其余 70 条不属于当前 Gate 必须完成人工标签。

## Indicator feasibility (2026-09-25 晚, label-free)

见 `reports/indicator_feasibility_audit.md`。结构事实：session_proxy 学生轮中位数 2；每生学生轮中位数 8/9；春季 unknown agent 占 36.8%。
按 AI 预标注情景推算，学生级独立比例指标精度不足以做个体排名 → B009（模型结构待决）。单人参赛与双人标注设计冲突 → B010。
Gate 状态不变：仍无人工标签。

## Module B evidence level

当前最高：Level 1 — 描述性差异。

在处理、对照、基线、结果、共同支持等条件确认之前，不得宣称 AI 因果增量。
