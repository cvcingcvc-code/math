# 30 秒版

AI 辅助学习的文本不一定都是学生自己的可观察证据。我们先把 Student Evidence 变成 Raw Score，再用可观察性、标注置信度、提示诱发和上下文完整性计算 Evidence Reliability，最后得到 Adjusted Evaluation。证据不足时输出 `NO_EFFECTIVE_EVIDENCE`，而不是硬给一个分数。当前结果是开发版证据评价，不是已识别的 AI 增量。
