# 评委 10 秒解释：Score 稳定，但 Evidence Support 崩塌

## 一句话研究问题

AI 参与学习过程后，一个看似稳定的评价分数，是否仍然有足够可信的学生证据支撑？

## 一句话核心发现

在当前 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 数据中，ABL、HOT 和 Gap 可以保持数值稳定，但 effective evidence weight 从 `16.0` 降到 `0.4`，effective coverage 从 `0.2286` 降到 `0.0057`，极端时返回 `NO_EFFECTIVE_EVIDENCE`。

## 为什么传统 Score-only 评价可能误导

因为归一化分数会把当前 16 条可判读 Evidence 的共同缩放因子约掉：分数看起来没变，但支撑它的有效证据正在减少。于是“分数稳定”不等于“证据支持稳定”。

## 我们的方法增加了什么

我们用 Partial Identification / Bounds 把 `Score` 与 `Evidence Support` 分开报告：在透明的 `lambda_prompt`、`lambda_context` 和 `r_medium` 敏感性假设下，同时检查分数、有效证据权重、effective coverage，以及证据归零时的 `NO_EFFECTIVE_EVIDENCE` 状态。这里的 effective coverage 定义为：

`effective coverage = effective evidence weight / 70 development records`

## 当前 development-only 结果不能证明什么

它不能证明 prompt 或 agent 的因果效应、学生真实能力、正式 AI 增量价值、正式 AIV 或学生排名。当前结果只说明：在现有 provisional 数据结构和透明假设下，数值 Score 与 Evidence Support 可能出现明显分离；正式结论仍需 Human R1 → 至少 24 小时 → Human R2 → test-retest reliability → Gate 后再验证。
