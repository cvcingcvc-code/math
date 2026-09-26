# TOMORROW_RUN_CARD

## 开场一句
我们研究的不是“AI 是否提高了学习效果”，而是：当观测证据存在缺失、冲突或可信度差异时，如何避免把 Raw Signal 直接解释为可靠结论？

## 核心 Research Question
如何把表现水平与证据支持度分开，并在证据不足时允许模型拒判？

## 核心流程
`Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support / Coverage → ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE`

## 最重要三个数字
- `70 / 16 / 54`：70 条开发记录，16 条可判读，54 条返回 `NO_EFFECTIVE_EVIDENCE`。
- `3.5625 / 0.375 / 1.125`：ABL / HOT / aggregate Gap。
- `P108: L6 / R=0.375 / Adjusted=2.25 / LOW_SUPPORT → ABSTAIN`。

## 唯一 Main Conclusion
**Score Stability ≠ Evidence Support Stability.**

## Demo 固定路线
1. `#rq`：说明问题是 measurement / identifiability，不是 AI 增量证明。
2. `#model`：展示六层流程与公式。
3. `#result`：展示 70 / 16 / 54、16→12→6→6 和 coverage 下降。
4. `#failure`：展示 P108、P072/P035 的拒判语义。

## 三个最危险问题
- “54 条是不是 54 个零分？”答：不是，`NO_EFFECTIVE_EVIDENCE` 的 Adjusted 为 null。
- “Reliability 是概率吗？”答：不是，是未正式校准的声明性支持权重。
- “你们证明 AI 提高学习了吗？”答：没有，AI Increment 为 `NOT_SUPPORTED`，Human Gate `NOT_RUN`。

## Claim Boundary
- ML 仅为 challenger：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`。
- BTC 仅为 `STRUCTURAL ONLY`，Gate3 `NOT SUPPORTED`。
- 不声称准确率提升、因果学习增益、交易优势、教育泛化或正式验证。

## 结束一句
所以我们报告的不只是“分数是多少”，还报告“这个分数有多少证据支持，以及什么时候应该拒绝装作确定”。
