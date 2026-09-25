# Red Team Review

> 审稿窗口：独立验证 / 红队。审稿日期：2026-09-25。只读审查，未修改任何主线文件。
> 依据：AGENTS.md、README.md、handoff/*、research/*、variable/、validation/*、reports/*、docs/annotation/*、data/processed/*、data/annotations/*、赛题原文（work/extracted/.../赛题终版.md），以及只读统计脚本（未落盘）。
> 标记约定：**[FACT]** = 本窗口从文件/数据中直接复算得到；**[LLM-EXPL]** = 来自 `pilot_ai_prelabel.csv`（annotator_type=LLM_EXPLORATORY_NOT_HUMAN，annotator_id=Codex-AI-1），只能作风险信号，不是人工结论；**[证据不足]** = 现有文件无法判定。
> 本文没有产生任何新的实验结果，也没有使用任何人工标注（目前人工标注为 0 条）。

## 1. 当前研究链条

1. **数据**：2 学期问答日志 → 7028 个 turn（学生 3522 / AI 3506），401 名学生，1225 个 session_proxy（= 原始记录行）；无前后测、无无 AI 对照组、无成绩数据。
2. **证据**：只使用学生 turn 文本（AI 文本仅作为语境）；Task Bloom 与 Student Evidence 分两个轴标注。
3. **标注**：仅有 140 条 LLM 探索性预标注；70 条双盲人工表已下发，**人工标签 0 条**；Gate