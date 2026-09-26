# 数据字典（开发版复现链路）

> 覆盖 `run_all.py` 读取和写出的核心文件。全部内容为 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `formal_gate_eligible=false`。
> 设计阶段的变量概念定义见 `variable/variable_map.md`；本文件是列级字典。

## 1. 输入：`data/annotations/ai/pilot_ai_provisional.csv`（70 行，UTF-8 BOM）

| 字段 | 类型 | 取值 / 含义 |
|---|---|---|
| case_order | int | 工作表中的呈现顺序 |
| record_id | str | 记录 ID（P001…），对应 `data/processed/pilot_sample.csv` 的 `pilot_id` |
| student_text | str | 学生发言原文 |
| prior_ai_context | str | 该发言前可见的 AI 上文（可为空） |
| context_truncated | bool | `true`/`false`，上文是否被截断 |
| speaker_role_check | str | 恒为 `student` |
| task_bloom | enum | 任务要求的 Bloom 层级：`L2`–`L6`、`UNDETERMINED` |
| task_confidence | enum | `low` / `medium` |
| student_evidence_bloom | enum | 学生可观察证据层级：`L2`–`L6`、`NO_EVIDENCE`、`UNDETERMINED` |
| evidence_confidence | enum | `low` / `medium` / `high` |
| confidence | enum | 综合置信度：`low` / `medium`（进入权重 `r_*`） |
| reason | str | 标注理由 |
| ambiguity_type | str | 分号分隔：`context_missing`、`prompt_induced`、`copy_suspected`、`task_unspecified` |
| needs_second_review | bool | 当前恒为 `true` |
| task_source | enum | `ai_prompt` / `student_request` / `unknown` |
| task_actor | enum | `ai` / `student` / `unknown` |
| evidence_span | str | 证据原文片段 |
| content_relation | enum | `copied_verbatim` / `reworked_with_addition` / `not_comparable` |
| partial_rewrite | bool | 是否部分改写 |
| prompt_induced | bool | 是否由 AI 提示诱发（进入 `lambda_prompt` 折减） |
| scaffold_share | enum | `none` / `medium` / `high` |
| correctness | enum | 恒为 `not_assessable` |
| speaker_unknown_reason / source_unknown_reason | str | 不可判定原因说明 |
| elapsed_sec | int | AI 标注无人工耗时，恒为 `0` |
| annotation_source | enum | 恒为 `AI_PROVISIONAL` |
| annotation_status | enum | 恒为 `DEVELOPMENT_ONLY` |
| annotation_disclaimer | str | 禁止作为人工标注 / 信度 / Gate 证据的声明 |
| manual_version | str | `V0.1+V0.1.1` |

计数：可判读 Evidence（`L2`–`L6`）16，`NO_EVIDENCE` 19，`UNDETERMINED` 35。

## 2. 参数网格：`reports/development/partial_identification_grid.csv`（693 行）

| 字段 | 含义 |
|---|---|
| lambda_prompt | 提示诱发证据的折减，0.00–1.00 步长 0.05（21 档） |
| lambda_context | 截断上下文证据的折减，0.0–1.0 步长 0.1（11 档） |
| r_medium | medium 置信度权重：0.5 / 0.75 / 1.0 |
| effective_weight | 有效证据权重之和 |
| effective_coverage | `effective_weight / 70`（**分母为全部 70 条记录**） |
| valid_or_undefined | `True` = 有定义；`False` = 有效权重为 0 |
| adjusted_ABL / adjusted_HOT / adjusted_gap | 加权 Score；未定义格为空 |
| undefined_reason | 未定义格填 `NO_EFFECTIVE_EVIDENCE`（**未定义，不是 0**） |

有定义 660 格，未定义 33 格（全部位于 `lambda_prompt=1.0`）。

## 3. 结果表：`reports/submission/development_results_record_level.csv`（70 行）

| 字段 | 含义 |
|---|---|
| record_id | 记录 ID |
| evidence_class | `READABLE_EVIDENCE`（16）/ `NO_EVIDENCE`（19）/ `UNDETERMINED`（35） |
| student_evidence_bloom / task_bloom | 同输入 |
| evidence_level_numeric | L2–L6 → 2–6；不可判读为空 |
| confidence / prompt_induced / context_truncated | 同输入 |
| baseline_weight | 基线参数（`lambda_prompt=0, lambda_context=0, r_medium=0.75`）下的记录权重 |
| enters_score | 是否进入 Score 分母（16 条为 `true`） |
| record_score_status | `IN_SCORE_DENOMINATOR` / `NOT_SCORED_NO_EVIDENCE` / `NOT_SCORED_UNDETERMINED` / `NOT_SCORED_ZERO_WEIGHT` |
| AIV / ranking | 恒为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`（不估算、不插值） |
| annotation_source / development_status / formal_gate_eligible | `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `false` |
| claim_boundary | `NOT A FORMAL COMPETITION RESULT OR RANKING` |

说明：开发数据未经验证的学生级聚合，因此结果表为**记录级**；学生级 AIV 与排名只能在 Gate PASS 后产生（见 `FORMAL_GATE_SWITCH.md`）。

## 4. 汇总表：`reports/submission/development_results_summary.csv`

列：`quantity, scope, value, value_max, annotation_source, development_status, formal_gate_eligible, claim_boundary`。
包含计数（70/16/19/35）、网格（693/660/33）、基线 Score（ABL 3.5625、HOT 0.375、Gap 1.125）、基线 Support（权重 12.0，覆盖率 12/70 = 0.1714）、有定义格上的范围，以及 `AIV`、`ranking` = `NOT_AVAILABLE_PENDING_FORMAL_GATE`。范围值中的 `3.5624999999999996` 等为浮点舍入，数学上恒等于 3.5625。

## 5. 其他输出

| 文件 | 内容 |
|---|---|
| `reports/development/development_metrics.csv` | 记录级开发指标（task/evidence level、gap、development_score 等） |
| `reports/development/reliability_sensitivity.csv` | 信度敏感性分析 |
| `reports/verification/core_numbers_source_of_truth.json` | 独立复算得到的核心数字，`run_all.py` 以它为检查基准 |
| `reports/demo/demo_payload.json` | Demo 数据（带状态标记） |
| `reports/development/core_figure_4_bounds_support.svg` | Figure 4：Score 与 Support 随 `lambda_prompt` 变化 |
| `reports/submission/run_all_report.json` | 每步退出码与 32 项检查结果 |

