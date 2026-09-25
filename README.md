# 赛道一：教育 AI 增量价值评价

比赛题目：《新时代教育中 AI 增量价值评价的建模方法》

研究方向：《考虑智能体引导偏差与标注不确定性的教育 AI 增量价值评价》

当前阶段：S4 Pilot Annotation Gate，等待正式人工/WorkBuddy 复核；不进行全量标注、最终 AIV 或因果模型。

恢复工作：先按 [AGENTS.md](AGENTS.md) 读取 `handoff/PROJECT_STATE.md`、`DECISIONS.md`、`NEXT_TASK.md`、`ARTIFACT_INDEX.md` 和未解决的 `BLOCKERS.md`，再按任务需要读取研究文件。

Canonical Pilot：[`data/processed/pilot_sample.csv`](data/processed/pilot_sample.csv)，140 条。旧 56 条 Pilot / ID 不匹配版本不属于正式实验。

主要目录：`data/` 数据与标注；`docs/` 文献及标注规则；`research/` 研究设计；`src/` 代码；`validation/` 验证方案；`reports/` 审计与复核报告；`handoff/` 持久项目状态。

当前 blocker：正式人工 Pilot 标注、标注协议边界统一、原生 session_id 缺失、独立无 AI 学习结果缺失，以及部分 agent 身份未知。详见 [`handoff/BLOCKERS.md`](handoff/BLOCKERS.md)。
