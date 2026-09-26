# 提交包验收报告（2026-09-26）

## 结论

当前可以提交“开发版材料供内部审查/演示”，不能声称已完成正式比赛最终提交包，也不能声称正式 R1/R2 Gate、正式 AIV 或学生排名已完成。

状态：

- READABLE_ARTIFACTS_PRESENT
- DEVELOPMENT_NUMBERS_REPRODUCED
- DEMO_PAPER_NUMERICALLY_CONSISTENT
- FORMAL_R1_NOT_COMPLETE
- FORMAL_R2_NOT_COMPLETE
- FORMAL_GATE_NOT_GENERATED
- GATE_PASS_NOT_ESTABLISHED
- FORMAL_AIV_NOT_AVAILABLE
- FINAL_SUBMISSION_PACKAGE_NOT_READY
- WORKTREE_DIRTY

## 已核验文件

- `reports/paper/competition_paper_narrative_draft.md`
- `reports/paper/paper_ready_development_draft.md`
- `reports/paper/method_results_skeleton.md`
- `reports/paper/judge_story_3min.md`
- `reports/paper/elevator_pitch_30s.md`
- `reports/paper/core_figures_interpretation.md`
- `reports/development/core_figure_4_bounds_support.svg`
- `reports/demo/index.html`
- `reports/demo/demo_payload.json`
- `reports/verification/core_numbers_source_of_truth.json`
- `reports/verification/demo_payload_consistency.json`
- `reports/verification/reproduction_review.md`
- `reports/annotation_gate_report.md`
- `reports/annotation_gate_report.json`

上述文件均可读取；Demo 已实际预览，Figure 4 SVG 已实际读取。

## 数字与状态口径

开发版 source of truth 与 Demo/论文一致：

- 70 development records
- 16 interpretable Evidence
- NO_EVIDENCE = 19
- UNDETERMINED = 35
- parameter grid = 693
- defined = 660
- undefined = 33
- ABL = 3.5625
- HOT = 0.375
- Gap = 1.125
- effective weight = 0.4–16.0
- effective coverage = 0.005714–0.228571
- coverage 分母 = 全部 70 条 development records

统一状态：

- `AI_PROVISIONAL`
- `DEVELOPMENT_ONLY`
- `formal_gate_eligible=false`
- 零有效权重返回 `NO_EFFECTIVE_EVIDENCE`，不填 0

Figure 4 当前直接展示 Score 稳定红线和 Evidence Support 下降蓝线，横轴为 `lambda_prompt`，固定 `lambda_context=0.00`、`r_medium=0.75`，并注明公共缩放结构不是因果效应。

## 正式 Gate

正式 R1、R2 均未完成，人工标签列仍为空。当前没有：

- test-retest reliability
- 正式 Kappa / Alpha
- Gate Report 结果
- Gate PASS
- formal AIV
- 学生级 AIV 排名

`reports/annotation_gate_report.md/.json` 仍是 PENDING 占位；`validation/gate_thresholds.json` 已确认为 `preregistered=true`，二者含义已区分。

## 比赛要求与实际齐备情况

赛题终版文件为：
`work/extracted/黑客松赛题-关老师/新时代教育AI增量价值评价建模方法-赛题终版（最终交付版）.md`

| 要求 | 格式 | 当前实际情况 |
|---|---|---|
| 建模论文 | PDF，正文不超过 30 页 | 当前只有 Markdown 草稿；最终 PDF 未发现，待生成/核对 |
| 复现包 | ZIP，含代码、环境、数据字典、`run_all` | 最终 ZIP、根 README、环境说明和 `run_all` 未发现；待整理 |
| 结果数据表 | CSV，学生级指标、AIV 分值与排名 | 未发现正式学生级 AIV/排名 CSV；正式 Gate 未完成，不能伪造 |
| 路演材料 | PDF/PPT，不超过 20 页 | 最终 PDF/PPT 未发现，待制作/核对 |
| 命名规范 | `队号_模块_文件名` | 队号未知，待负责人提供/核对 |

规则文件已在仓库中发现，因此不再标记为“未获规则”；但具体队号、最终提交渠道、截止时间和是否允许开发版替代正式结果，当前仍未在本地材料中确认，标记为待核对。

## 检查证据

已成功：

- 独立 Bounds 复算：70 / 16 / 693 / 660 / 33 及核心指标全部复现；
- Demo payload consistency 报告为匹配；
- Figure 4 文件读取与关键文案检查；
- Demo HTML 实际打开预览；
- Git diff check 无格式错误；
- 赛题终版提交规范读取成功；
- `reports/annotation_gate_report` 明确为 PENDING。

明确未运行：

- `src/run_development_experiment.py`：`NOT RUN / BLOCKED_BY_PANDAS_ENVIRONMENT`；
- `src/run_reliability_sensitivity.py`：`NOT RUN / BLOCKED_BY_PANDAS_ENVIRONMENT`。

pandas 安装失败于 pandas 源码构建的 `vswhere.exe` 解析阶段，不能将这两个脚本写成测试通过。

## 本轮只修复的提交阻断问题

- 更新 `handoff/CURRENT_HANDOFF.md` 的实际 HEAD SHA 为 `f0c115f`；
- 修正 Gate PENDING 占位报告中的 `preregistered` 过期文本，使其与冻结阈值文件一致；
- 更新复算审查中 Figure 4 的历史 P1 状态为已修复；
- 记录两个 pandas 脚本为 NOT RUN；
- 未开发新模型，未改变数据、标注、公式、阈值或 R1/R2。

本轮状态修正尚未单独提交时，当前 HEAD 为：

```text
f0c115f
```
