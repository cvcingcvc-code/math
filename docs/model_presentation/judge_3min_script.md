# 3 分钟答辩稿

在 AI 辅助学习里，学生的答案不一定都代表同等可信的学生证据。信息完整、学生自己完成、上下文充分的记录，和受 AI 引导、上下文截断、来源冲突的记录，不能只看表面分数来等价处理。我们的模型不是证明 AI 提升了学习，而是在 AI 辅助环境下判断一条表现证据到底值得相信多少。

模型先从 Student Evidence 得到 Raw Signal，再计算 Evidence Reliability：`w_i=I(observable_i)c_i(1−λ_prompt p_i)(1−λ_context t_i)`。然后把每条证据的有效贡献写成 `Adjusted_i=Raw_i×w_i`，汇总支持度 `S=Σw_i`，有效覆盖率为 `C_eff=Σw_i/N`。这里的分母是全部 70 条开发记录。乘法结构让低可靠证据不被放大，权重为零时输出 `NO_EFFECTIVE_EVIDENCE`；证据不足或冲突时 `ABSTAIN`，只有支持规则通过才 `ACCEPT`。

看一个真实开发例子：P108 的 Raw Evidence 是 L6，看起来很高，但存在 prompt 风险，Reliability 只有 0.375，Adjusted contribution 是 2.25，因此标记为 LOW_SUPPORT，并采取 ABSTAIN。P072 的证据不可判读且上下文截断，权重为零，输出 NO_EFFECTIVE_EVIDENCE，而不是填成 0 分。70 条中只有 16 条可判读，Raw ABL 为 3.5625，归一化分数保持稳定，但有效权重从 16 降到 6，说明 Score Stability 不等于 Evidence Support Stability。

敏感性分析在声明的参数网格内得到相同的分数和状态，支持度更敏感；消融显示 confidence 和 prompt 组件会减少不受支持的贡献。它们验证的是结构行为，不是准确率。当前 HUMAN R1/R2 尚未完成，Formal Gate 仍未运行；`c_i` 与两个 lambda 也是弱依据组件。由于没有合法配对的 Outcome_AI 和 Outcome_baseline，AI Increment 仍为 NOT_SUPPORTED。因此本模型当前评价的是可观察表现的证据支持程度，不能推出真实能力、长期学习增益或 AI 因果效果。
