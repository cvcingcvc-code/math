# 30 秒版本

AI 参与学习后，学生提交的文本可能混合了自己的思考和 AI 的引导，因此“分数稳定”不一定代表“学生证据充分”。我们没有把不可识别的 prompt、context 和 reliability 修正项硬估成一个精确参数，而是用 Partial Identification / Bounds 在透明假设下同时报告 Score 和 Evidence Support。开发结果显示：ABL、HOT、Gap 几乎不变，但 effective evidence weight 可从 16.0 降到 0.4，极端时返回 `NO_EFFECTIVE_EVIDENCE`。因此项目的核心发现是：**Score Stability ≠ Evidence Support Stability**；可信的 AI 教育评价必须先证明分数有足够可解释的证据支撑，再讨论正式 AIV，而不是把 provisional 结果伪装成因果结论。
