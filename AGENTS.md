# AGENTS.md

## Project

中国第一届数学建模黑客松 · 赛道一

题目：
《新时代教育中 AI 增量价值评价的建模方法》

唯一项目根目录：
`C:\Users\lin\Documents\Codex\2026-09-25\yu`

## Mandatory startup procedure

每次进入本项目的新 Codex 对话，在执行任何实质任务前必须依次读取：

1. `handoff/PROJECT_STATE.md`
2. `handoff/DECISIONS.md`
3. `handoff/NEXT_TASK.md`
4. `handoff/ARTIFACT_INDEX.md`
5. 如存在 `handoff/BLOCKERS.md`，读取其中未解决 blocker

然后再读取当前任务直接相关的 research / docs / data / validation 文件。
不要依赖旧聊天上下文作为唯一依据；文件中的当前状态优先于旧对话记忆。

## Core research direction

研究对象：学生在 AI 辅助学习中的“可观察交互与学习表现证据”。

当前主方向：构建能区分学生可观察表现、智能体引导路径以及数据/标注偏差的可信 AIV 评价体系。

AIV 当前用途为形成性教学诊断。不得将 AIV 直接解释为学生长期稳定能力、AI 相对于无 AI 的已识别因果效果或高风险学生奖惩排名。

## Research principle

顺序固定为：数据事实 → 标注可信性 → 数学模型 → 验证/证伪 → AIV → 稳定性与红队 → 复现 → 论文/路演。

禁止先选高级算法再强行套问题。任何新方法必须回答：解决什么真实问题、需要什么数据、假设是什么、如何验证、失败时如何解释。

## Canonical data

正式 Pilot V1：`data/processed/pilot_sample.csv`，N = 140。

56 条旧 Pilot / ID 不匹配版本仅属于探索性结果，不进入正式一致性实验。不得把两个 AI 输出冒充两名独立人工标注者。

## Roles

Builder：负责数据、Python、实验、可视化、复现。

Critic / Writer：负责规则、方法审查、文献、反例、论文表述和结论边界。

若当前任务角色未说明，优先根据 `handoff/NEXT_TASK.md` 执行。

## Gate discipline

不得自行跳过 Gate。若发现新事实与 `DECISIONS.md` 冲突，停止相关后续实验，把事实写入 `handoff/BLOCKERS.md`，向用户报告；不得自行悄悄改变研究方向。

## Handoff discipline

完成每个阶段后必须更新 `handoff/PROJECT_STATE.md`、`handoff/NEXT_TASK.md`、`handoff/ARTIFACT_INDEX.md`、`handoff/CHANGELOG.md`。重大冻结决策才写入 `DECISIONS.md`。

AGENTS.md 保持精简；详细研究内容放在 research / docs / handoff 中。
