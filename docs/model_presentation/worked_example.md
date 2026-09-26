# Worked example — P033

> **DEVELOPMENT EXAMPLE / AI_PROVISIONAL；不是正式人工结果。**

1. 输入：`Student Evidence=L6`，`confidence=medium`，`prompt_induced=true`，`context_truncated=false`。
2. Raw Score：`y=6`。
3. 组件：`I=1`，`c=.75`，prompt 因子 `1−.5×1=.5`，context 因子 `1−.5×0=1`。
4. Reliability：`w=1×.75×.5×1=.375`。
5. Adjusted contribution：`w×y=.375×6=2.25`。
6. 状态：`0<w<.75`，所以是 `LOW_SUPPORT`；展示层将其解释为“保留 L6 信号，但不把它当作高支持证据”。

这条记录不产生 AI increment，也不代表真实学习效果。
