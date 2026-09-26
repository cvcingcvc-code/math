# Model pipeline

| 层 | 数学符号 | 输入 | 输出 | 一句话 |
|---|---|---|---|---|
| Data | `x_i` | 交互记录与标注字段 | 可观察字段 | 先说明我们实际看到了什么 |
| Raw Signal | `y_i` | Student Evidence Bloom | L1–L6 或不可判读 | 观察到的证据落在哪一级 |
| Reliability | `w_i` | 可观察性、confidence、prompt/context 风险 | `[0,1]` 权重 | 这条证据值得信多少 |
| Adjusted | `S_adj` | `y_i,w_i` | 加权分数 | 让支持度进入评价 |
| Decision | `status` | 分数与权重 | SUPPORTED / LOW_SUPPORT / NO_EFFECTIVE_EVIDENCE | 证据不足时停下来 |

当前不存在合法的 `Outcome_AI` 与 `Outcome_baseline` 配对，因此不写 `Observed AI Increment` 或 `Reliable AI Increment`。
