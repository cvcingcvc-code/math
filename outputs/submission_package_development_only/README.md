# 赛道一：教育 AI 增量价值评价

当前项目处于 S4 Pilot Annotation Gate。正式人工 R1/R2 由负责人亲自完成，本窗口不读取、不推断、不建议任何 R1 标签判断。

## 当前可交付状态

研究核心已冻结为 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`。开发版闭环可复现，正式 AIV 仍为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

核心开发数字：70 条 development records 中 16 条可判读 Evidence；Raw/Adjusted ABL、HOT、Gap 均为 `3.5625 / 0.375 / 1.125`；effective weight `16 → 6`；coverage `0.228571 → 0.085714`，分母为 70。

核心表达：**Score stability does not imply Evidence Support stability.**

## 入口

- 开发版复现：`python run_all.py`，脚本保留完整链路说明；当前包按交付清单提供结果与审计产物，正式 Gate 仍 fail-closed。
- Formal 模式：`python run_all.py --mode formal`，在 Gate PASS 前保持 fail-closed。
- Demo：`demo/index.html`，顶部明确 `DEVELOPMENT_ONLY · AI_PROVISIONAL`。
- 路演 PPT：`slides/final_roadshow.pptx`（10 页最终版）。
- 最终论文：`paper/final_paper.pdf`、`paper/final_paper.md`、`paper/final_paper_editable.docx`。
- 最终图件：`development/F1_model_flow.svg` 至 `development/F6_external_structural_transfer.svg`。
- 包完整性：`MANIFEST.sha256.json`，共 41 项，逐项校验 PASS。

## 目录

`data/` 数据与标注；`docs_data_dictionary.md` 数据字典；`src/` 开发版复现代码；`reports/` 审计、开发结果与复现记录；`reproduction/` 运行说明；`demo/` 离线演示；`paper/` 论文交付物；`slides/` 路演 PPT。

## 边界

当前不声称正式 Gate 通过、Formal AIV、学生排名、学生真实能力或 prompt/agent 因果效应。不要把 development 结果包装为 Formal AIV，也不要把 16 条 Evidence 外推到 140 条正式样本或总体。

恢复工作前先读 `AGENTS.md` 与 `handoff/PROJECT_STATE.md`、`DECISIONS.md`、`NEXT_TASK.md`、`ARTIFACT_INDEX.md`、`BLOCKERS.md`。
