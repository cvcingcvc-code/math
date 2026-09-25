# 评委版 3 分钟研究故事

> **使用场景**：第一次向不了解项目的评委介绍。建议语速正常，约 3 分钟。当前所有数值都必须带有 DEVELOPMENT_ONLY / AI_PROVISIONAL 说明。

## 口头稿

我们的项目关注一个很容易被忽略的问题：AI 已经参与学习过程以后，学生提交的结果还能够被直接当成学生能力的证据吗？

学生文本可能同时受到自己的思考、AI 的提问和提示、AI 内容重组、上下文缺失以及来源不确定性的影响。所以，评价者看到“学生交了什么”，不一定等于观察到了“学生真正提供了多少可解释证据”。这使问题首先成为一个 measurement 和 identifiability problem，而不是单纯的预测问题。

传统做法往往直接给出一个分数，或者在看到数据不完整时估计一个修正系数。但在当前数据里，我们发现，16 条可判读 Evidence 全部来自 prompt 引导的 AI 路径，没有可用于对照的 prompt 非引导 Evidence；上下文、置信度和行为主体也缺少充分交叉支持。因此，prompt penalty、context penalty 和可靠性参数不能从数据中被唯一估计。

我们的选择是 Partial Identification，也就是不假装知道一个精确修正系数，而是在一组透明的假设范围内计算结果。核心权重可以用一条公式表示：

```text
w_i = Evidence indicator × confidence weight
      × prompt factor × context factor
```

然后我们同时报告两类东西：第一类是分数，例如 ABL、HOT 和 Task/Evidence Gap；第二类是支撑这些分数的 effective evidence weight 和 effective coverage。

开发结果非常关键。基线下，ABL 是 3.5625，HOT 是 0.375，Gap 是 1.125。在有效参数范围内，这三个分数基本不变，看起来非常稳定。但是有效 Evidence weight 可以从 16.0 降到 0.4，有效 coverage 可以从 0.2286 降到 0.0057。也就是说，分数可以稳定，但支撑分数的证据正在快速减少。

因此，我们提出这句话作为项目的核心：**Score Stability 不等于 Evidence Support Stability。** 传统评价可能只问分数是否稳定；AI 参与以后，还必须问：这个分数背后是否仍然存在足够可信的学生证据？

我们还保留了一个重要的极端边界。当 `lambda_prompt=1`，而当前所有可判读 Evidence 都是 prompt-induced 时，有效证据权重会变成 0。此时模型返回 `NO_EFFECTIVE_EVIDENCE`，ABL、HOT 和 Gap 是 undefined，而不是 0。这个结果说明，评价可能不是“分数变差”，而是已经失去定义。

当然，当前结果不能被过度解释。它们来自 AI provisional labels，属于 development-only；正式人工 R1/R2 尚未完成，Gate 尚未通过。因此我们不能宣称学生真实能力、prompt 因果效应、AI 正式增量价值或学生排名。当前完全分离结构只能描述为数据选择、标注规则、临时标签和字段映射的混合结果。

正式闭环是：Human R1，间隔至少 24 小时后完成同一标注者 R2，计算 test-retest reliability，完成 Gate，再进行正式 Support Audit 和 Bounds。我们的 Demo 也不只展示一个分数，而是让评委看到：当假设变化时，Score 可能不动，但 Support 会下降；当支持归零时，系统会拒绝伪装成一个 0 分。

所以，这个项目的价值不是声称已经得到一个精确的 AI 增量价值，而是建立一个诚实的前置评价框架：在 AI 参与的学习环境中，先确认分数由什么证据支撑，再讨论是否可以进入正式 AIV 评价。
