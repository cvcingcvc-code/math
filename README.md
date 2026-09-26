# 赛道一：教育 AI 增量价值评价

当前项目处于 S4 Pilot Annotation Gate。正式人工 R1/R2 由负责人亲自完成，本窗口不读取、不推断、不建议任何 R1 标签判断。

## 当前可交付状态

研究核心已冻结为 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`。开发版闭环可复现，正式 AIV 仍为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

核心开发数字：70 条 development records 中 16 条可判读 Evidence；Raw/Adjusted ABL、HOT、Gap 均为 `3.5625 / 0.375 / 1.125`；effective weight `16 → 6`；coverage `0.228571 → 0.085714`，分母为 70。

核心表达：**Score stability does not imply Evidence Support stability.**

## 入口

- 开发版复现：`python run_all.py`，预期 6 步、32 项一致性检查通过。
- Formal 模式：`python run_all.py --mode formal`，在 Gate PASS 前保持 fail-closed。
- Demo：`reports/demo/index.html`，顶部明确 `DEVELOPMENT_ONLY · AI_PROVISIONAL`。
- 路演 PPT：`outputs/education_ai_evidence_roadshow_v1_final.pptx`。
- 内部提交包：`outputs/submission_package_development_only/`，含 MANIFEST 与复现说明。

## 目录

`data/` 数据与标注；`docs/` 标注规则与数据字典；`research/` 研究设计；`src/` 代码；`validation/` Gate 阈值；`reports/` 审计、开发结果与复现记录；`slides/` 路演大纲；`outputs/` 用户可交付材料；`handoff/` 持久项目状态。

## 边界

当前不声称正式 Gate 通过、Formal AIV、学生排名、学生真实能力或 prompt/agent 因果效应。不要把 development 结果包装为 Formal AIV，也不要把 16 条 Evidence 外推到 140 条正式样本或总体。

恢复工作前先读 `AGENTS.md` 与 `handoff/PROJECT_STATE.md`、`DECISIONS.md`、`NEXT_TASK.md`、`ARTIFACT_INDEX.md`、`BLOCKERS.md`。
