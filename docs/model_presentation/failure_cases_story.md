# Failure and counterexample story

| 案例 | 现象 | 模型处理 | 边界 |
|---|---|---|---|
| P105 | Task L5，但 Evidence L2 且有 prompt 风险 | L2 保留，降低权重 `.375` | 仅开发标注 |
| P108 | Raw Evidence L6，但所有可判读证据均有 prompt 风险 | 保留 L6，报告低支持 | 不能解释成真实高能力 |
| P072 | 上下文截断，Evidence 不可判读 | `NO_EFFECTIVE_EVIDENCE`，不填 0 | 不是“错误预测” |
| P035 | Evidence 不可判读、低置信、上下文截断 | `NO_EFFECTIVE_EVIDENCE` | 不是“模型正确” |

当前没有正式 outcome，因此“Reliability 高但后来错误”“ABSTAIN 后实际正确”均为 `OUTCOME NOT AVAILABLE`，不得补写。
