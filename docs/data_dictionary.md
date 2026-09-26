# 数据字典（完整版）

> 覆盖项目**实际使用**的全部数据文件的字段级定义。全部内容默认 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `formal_gate_eligible=false`。
> 分类索引与文件用途见 `docs/DATA_STRUCTURE.md`；变量概念定义见 `variable/variable_map.md`；运行方法见 `docs/RUN_GUIDE.md`。
> 只描述现状，不改变任何数据。未核验字段标注「待核验」。

---

## 0. 原始数据来源

- 原始 Q&A 工作表 Excel 导出**未入库**（`data/raw/` 为空）。字段结构以清洗后 `clean_interactions.csv` 的 `raw_segment_text`、`source_row_id`、`raw_excel_row` 等保留列间接体现。
- 两学期来源与纳入/排除计数固化于 `data/processed/cohort_flow.csv`、`exclusion_log.csv`。

---

## 1. 处理中间数据

### 1.1 `data/processed/clean_interactions.csv`（7028 turns，UTF-8 BOM）

主清洗结果，一条 = 一个解析后的发言（turn）。

| 字段 | 类型 | 含义 / 取值 |
|---|---|---|
| student_id | str | 学生标识（去标识） |
| semester | enum | `2025秋` / `2026春` |
| session_id | str | 会话标识（项目内；原始数据无原生 session_id，见 BLOCKERS B003） |
| turn_id | str | 轮次标识（`pilot_sample.csv` 用其定位） |
| speaker_role | enum | `student` / `ai`（学生 3522 / AI 3506） |
| student_text / ai_text / system_text | str | 学生 / AI / 系统文本 |
| raw_segment_text | str | 原始分段文本 |
| agent_type | enum | AI 路径类型（含 `unknown`，约 10.5% turn；D011 保留并报告） |
| agent_confidence / speaker_confidence | float/str | 解析置信度 |
| agent_basis | str | agent 判定依据 |
| timestamp | datetime | 发言时间（观察期 2025-10-09 起 / 2026-03-19 起） |
| source_row_id | str | 来源 Excel 行号（session_proxy 重建依据） |
| source_file / source | str | 来源文件 / 来源类型 |
| course / class | str | 课程 / 班级 |
| turn_index_in_session | int | 会话内轮次序号 |
| raw_excel_row | int | 原始 Excel 行号 |
| session_parse_status | str | 会话解析状态 |

### 1.2 `data/processed/pilot_sample.csv`（N=140，UTF-8 BOM）— 正式 Pilot V1

主键：`pilot_id`（P001–P140 唯一）。分析单位 = 学生轮（140/140 均 student）。

| 字段 | 类型 | 含义 |
|---|---|---|
| pilot_id | str（主键） | P001–P140 |
| student_id / semester / session_id / turn_id | str | 与 clean_interactions 对应 |
| speaker_role | enum | 恒 `student` |
| student_text | str | 学生发言原文 |
| ai_context_text | str | **已弃用字段（S4-F01 HIGH）**：实为该轮**之后**的 AI 内容，非前文；标注路径已隔离，任何下游使用前须先修复/弃用 |
| agent_type / agent_confidence | str | AI 路径类型 / 置信度 |
| timestamp / speaker_confidence | — | 时间 / 置信度 |
| source_row_id / source_file | str | 来源定位 |
| text_length_chars / length_stratum | int/str | 文本长度 / 长度分层 |
| question_form_stratum / possible_bloom_surface_signal / surface_signal_terms | str | 表层信号（仅探索，非标签） |
| path_case | str | 路径案例（盲标表遮蔽此列） |
| annotation_status / annotation_note | str | 标注状态 / 备注 |

### 1.3 `data/processed/cohort_flow.csv`（8 行，UTF-8 BOM）

| 字段 | 含义 |
|---|---|
| semester | `2025秋` / `2026春` |
| stage | 流程阶段（raw / included / excluded / clean_turns） |
| n | 该阶段记录数 |
| student_count | 该阶段学生数 |
| date_min / date_max | 观察期 |
| note | 阶段说明（含排除构成 JSON） |

### 1.4 `data/processed/exclusion_log.csv`（2770 行，UTF-8 BOM）

| 字段 | 含义 |
|---|---|
| semester / source_file / source_sheet / source_row_id / student_id / timestamp / source | 被排除记录的定位 |
| disposition | 处置（如 `excluded`） |
| reason | 排除原因（`url_only_unretrieved_content` / `empty_interaction_text` / `outside_affirmative_spring_rosters`） |

### 1.5 `data/processed/speaker_audit.csv`（120 行，UTF-8 BOM）

| 字段 | 含义 |
|---|---|
| audit_id（主键） | 审计样本 ID |
| speaker_role_auto / agent_type_auto / *_confidence_auto | 自动解析结果 |
| audited_speaker_role / audited_agent_type | 人工审计结果 |
| speaker_correct / agent_correct | 自动 vs 人工 是否一致 |
| auditor_notes | 审计备注 |

### 1.6 `data/processed/pilot_ai_prelabel.csv`（140 行，UTF-8 BOM）

AI 探索性预标注（`annotator_type=LLM_EXPLORATORY_NOT_HUMAN`，D007 合规，非人工标签）。

| 字段 | 含义 |
|---|---|
| record_id | = pilot_id |
| task_bloom / student_evidence_bloom | AI 预标注（L2–L6 / NO_EVIDENCE / UNDETERMINED） |
| task_confidence / evidence_confidence / confidence | 置信度 |
| reason / ambiguity_type / needs_human_review | 理由 / 歧义 / 是否需人工 |
| content_source_attribution | 内容来源归属 |
| prior_ai_context / prior_ai_source_row_id | 该发言前可见 AI 上文（可独立重建复现） |
| task_evidence_numeric_gap / pilot_sampling_strata | 双轴数值差 / 抽样分层 |
| manual_version / annotator_id / annotator_type / annotation_status | V0.1 / Codex-AI-1 / LLM_EXPLORATORY_NOT_HUMAN / … |

### 1.7 `data/processed/pilot_human_review_queue.csv`（70 行，UTF-8 BOM）

在 prelabel 基础上追加：`review_priority_score`、`review_sample_type`（`HARD_CASE` 50 / `RANDOM_NORMAL_AUDIT` 20）、`human_review_reason`。
**注意（S4-F02 HIGH）：非盲表**，含 AI 预标注与 agent/path，仅分析侧，禁止下发。

---

## 2. 人工标注（盲标表，25 列，统一结构）

`pilot_worksheet_A.csv`（R1，GB18030）、`pilot_worksheet_A_retest.csv`（R2，UTF-8 BOM）、`pilot_worksheet_B.csv`（遗留空白，UTF-8 BOM）结构相同：

| 字段 | 类型 | 含义 / 取值 |
|---|---|---|
| case_order | int | 呈现顺序 |
| record_id | str | 对应 pilot_id（映射见 `_keys/pilot_worksheet_key.csv`） |
| student_text / prior_ai_context / context_truncated | str/str/bool | 盲标可见输入 |
| speaker_role_check | str | 恒 `student` |
| task_bloom | enum | 任务 Bloom 层级（冻结手册：L2–L6 / UNDETERMINED） |
| task_confidence | enum | `low` / `medium` / `high` |
| student_evidence_bloom | enum | 学生证据层级（L2–L6 / NO_EVIDENCE / UNDETERMINED） |
| evidence_confidence | enum | `low` / `medium` / `high` |
| confidence | enum | 综合置信度 |
| reason | str | 标注理由 |
| ambiguity_type | str | 分号分隔（`context_missing` / `prompt_induced` / `copy_suspected` / `task_unspecified` …） |
| needs_second_review | bool | 是否需二审 |
| task_source | enum | `ai_prompt` / `student_request` / `unknown` |
| task_actor | enum | `ai` / `student` / `unknown` |
| evidence_span | str | 证据原文片段 |
| content_relation | enum | `copied_verbatim` / `reworked_with_addition` / `not_comparable` |
| partial_rewrite | bool | 是否部分改写 |
| prompt_induced | bool | 是否提示诱发 |
| scaffold_share | enum | `none` / `medium` / `high` |
| correctness | enum | 恒 `not_assessable`（教育场景不评对错） |
| speaker_unknown_reason / source_unknown_reason | str | 不可判定原因 |
| elapsed_sec | int | 人工耗时（供成本阈值判断） |

当前填写状态：R1 = **0/70 有效**（原 1 条非法行已清空），R2 = **0/70**，B = 0/70（遗留空白）。

### `data/annotations/_keys/pilot_worksheet_key.csv`（70 行，仅分析侧）

盲标映射：`case_order, record_id, semester, student_id, turn_id, source_row_id, agent_type, agent_confidence, text_length_chars, path_case, pilot_sampling_strata, task_bloom_ai, student_evidence_bloom_ai, in_review_queue, review_sample_type, review_priority_score, human_review_reason, manual_version`。

### `data/annotations/workbuddy/pilot_worksheet_B_submitted.csv`（70 行，UTF-8 BOM，只读）

队友 B 交回件，列结构与盲标表相同。**取值尺度为 L1–L6 + NOT_APPLICABLE，与冻结手册 L2–L6 不一致**；`content_relation` 含 `independent` / `reworked_without_addition`，`correctness` 含 `correct` / `partially_correct` / `incorrect`（非手册 `not_assessable`）。
边界：不作冻结 B010 的 R1/R2，不计算一致性；详见 `reports/workbuddy_annotation_audit.md`。

---

## 3. 模型输入

### 3.1 `data/annotations/ai/pilot_ai_provisional.csv`（70 行，UTF-8 BOM，29 列）— 开发版模型唯一输入

字段（盲标表字段基础上增补）：

| 字段 | 含义 |
|---|---|
| case_order, record_id, student_text, prior_ai_context, context_truncated, speaker_role_check | 同盲标表 |
| task_bloom | L2–L6 / UNDETERMINED |
| task_confidence | low / medium |
| student_evidence_bloom | L2–L6 / NO_EVIDENCE / UNDETERMINED |
| evidence_confidence | low / medium / high |
| confidence | low / medium |
| reason, ambiguity_type, needs_second_review | 同盲标表 |
| task_source, task_actor, evidence_span, content_relation, partial_rewrite, prompt_induced, scaffold_share, correctness | 同盲标表 |
| speaker_unknown_reason, source_unknown_reason | 同盲标表 |
| elapsed_sec | 恒 0 |
| annotation_source | 恒 `AI_PROVISIONAL` |
| annotation_status | 恒 `DEVELOPMENT_ONLY` |
| annotation_disclaimer | 禁止作为人工标注/信度/Gate 证据的声明 |
| manual_version | `V0.1+V0.1.1` |

计数：可判读 Evidence（L2–L6）= 16（L2=5 / L3=5 / L4=1 / L5=2 / L6=3），NO_EVIDENCE = 19，UNDETERMINED = 35。

### 3.2 `data/annotations/ai/pilot_ai_assisted_full.csv`（70 行，UTF-8 BOM，28 列）

AI 辅助标注（deepseek-flash），列与 3.1 相同但以 `formal_gate_eligible`（恒 false）取代 `manual_version`。**取值尺度 L1–L6 + NOT_APPLICABLE，与冻结手册不一致**，仅开发记录，不得混入正式输入。

---

## 4. 参数网格与开发结果

### 4.1 `reports/development/partial_identification_grid.csv`（693 行）

| 字段 | 含义 |
|---|---|
| lambda_prompt | 提示诱发折减，0.00–1.00 步长 0.05（21 档） |
| lambda_context | 截断上下文折减，0.0–1.0 步长 0.1（11 档） |
| r_medium | medium 置信度权重 0.5 / 0.75 / 1.0 |
| effective_weight | 有效证据权重之和 |
| effective_coverage | `effective_weight / 70`（分母 = 全部 70 条记录） |
| valid_or_undefined | True = 有定义；False = 有效权重 0 |
| adjusted_ABL / adjusted_HOT / adjusted_gap | 加权 Score；未定义格为空 |
| undefined_reason | 未定义格填 `NO_EFFECTIVE_EVIDENCE`（未定义 ≠ 0） |

有定义 660 格，未定义 33 格（全部位于 `lambda_prompt=1.0`）。

### 4.2 `reports/submission/development_results_record_level.csv`（70 行）

| 字段 | 含义 |
|---|---|
| record_id | 记录 ID |
| evidence_class | READABLE_EVIDENCE(16) / NO_EVIDENCE(19) / UNDETERMINED(35) |
| student_evidence_bloom / task_bloom | 同输入 |
| evidence_level_numeric | L2–L6 → 2–6；不可判读为空 |
| confidence / prompt_induced / context_truncated | 同输入 |
| baseline_weight | M1 confidence-only 权重（λ_prompt=0、λ_context=0、r_medium=0.75）；**注意这是 confidence-only 基线，不是 M0 Raw-only**（M0 无任何校正，权重恒为 1.0） |
| enters_score | 是否进入 Score 分母（16 条 true） |
| record_score_status | IN_SCORE_DENOMINATOR / NOT_SCORED_* |
| AIV / ranking | 恒 `NOT_AVAILABLE_PENDING_FORMAL_GATE` |
| annotation_source / development_status / formal_gate_eligible | AI_PROVISIONAL / DEVELOPMENT_ONLY / false |
| claim_boundary | NOT A FORMAL COMPETITION RESULT OR RANKING |

### 4.3 `reports/submission/development_results_summary.csv`

列：`quantity, scope, value, value_max, annotation_source, development_status, formal_gate_eligible, claim_boundary`。含 70/16/19/35、693/660/33、Score（ABL 3.5625 / HOT 0.375 / Gap 1.125）、以及 Support 消融序列 —— **M0 Raw-only = 16（coverage 0.228571）；M1 confidence-only = 12（0.171429）；M2/M3 当前模型 = 6（0.085714）**；AIV/ranking=NOT_AVAILABLE…。浮点 `3.5624999999999996` 为舍入，恒等于 3.5625。

### 4.4 其他开发输出

| 文件 | 内容 |
|---|---|
| `reports/development/development_metrics.csv` | 记录级开发指标 |
| `reports/development/reliability_sensitivity.csv` | 信度敏感性（15 条件） |
| `reports/verification/core_numbers_source_of_truth.json` | 独立复算核心数字（run_all.py 检查基准） |
| `reports/demo/demo_payload.json` | Demo 数据接口 |
| `reports/development/core_figure_4_bounds_support.svg` | Figure 4 |
| `reports/submission/run_all_report.json` | 每步退出码 + 32 项检查 |
| `outputs/final_results.json` | 统一事实源（paper/demo/PPT/figures 共同读取） |

---

## 5. 表间关联

- `pilot_sample.pilot_id` ↔ `pilot_ai_prelabel.record_id` ↔ 盲标表/`_keys`.record_id ↔ `pilot_ai_provisional.record_id`（P001–P140 子集 P001–P070 用于 70 条核心 Gate）。
- `pilot_sample.turn_id` ↔ `clean_interactions.turn_id`（140/140 定位成功）。
- `clean_interactions.source_row_id + turn_index_in_session` → 重建 `prior_ai_context`（标注路径用此，不用 `ai_context_text`）。
- `exclusion_log.source_row_id` ↔ `clean_interactions.raw_excel_row`（排除轨迹可追溯）。
