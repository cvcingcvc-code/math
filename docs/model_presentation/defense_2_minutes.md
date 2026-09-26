# 2 分钟版

先讲三层：Raw Score 说明观察到什么，Reliability 说明支持度，Adjusted Score 说明降权后剩什么。可靠性由 `I(observable)c(1−λ_prompt p)(1−λ_context t)` 分解。当前 70 条开发记录只有 16 条可判读证据；Raw ABL=3.5625，Adjusted ABL 仍为 3.5625，但有效覆盖率从 0.228571 降到 0.085714。这个差异说明“分数稳定”不等于“证据支持稳定”。当权重为零时模型 abstain。所有数值来自 AI_PROVISIONAL，Formal Gate 尚未运行。
