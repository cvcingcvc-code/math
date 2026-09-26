# 高概率评委问答（20 题）

## 1. 你们研究的是 AI 增量吗？
不是。当前研究问题是 measurement / identifiability：如何把观测结果、证据可靠性和支持范围分开。AI increment identification 为 `NOT_SUPPORTED`。

## 2. 为什么不能直接用 Raw Signal？
因为 Raw Signal 只描述观察到的表现，不表达证据是否可判读、是否缺失或是否受到 prompt/context 影响。直接使用会把弱证据包装成确定结论。

## 3. 你们的 Reliability 是概率吗？
不是。R 是确定性的支持权重，用于调整贡献和计算 Support/Coverage，不是校准概率。

## 4. 公式中的参数是怎么来的？
当前使用冻结默认值：`lambda_prompt=0.5`、`lambda_context=0.5`、`confidence medium=0.75`。它们是 development-only 的弱合理化组件，不被升级成普适参数。

## 5. 为什么 Adjusted 和 Raw 的平均分相同？
因为当前 16 条可判读记录共享同一组因素，Reliability 形成公共缩放；归一化后平均分里的常数因子抵消。这是公共缩放退化，不是效果提升。

## 6. 既然分数没变，方法增加了什么？
增加了对 Evidence Reliability、effective weight、coverage 和拒答状态的显式报告，使“分数稳定但支持下降”可被观察和审查。

## 7. 70 条里为什么只有 16 条可判读？
因为 19 条是 NO_EVIDENCE，35 条是 UNDETERMINED。系统不把不可判读记录强行转成数值，因此 54 条返回 NO_EFFECTIVE_EVIDENCE。

## 8. 54 条是不是 54 个零分？
不是。它们没有有效证据，Adjusted 为 null；填 0 会把“无证据”错误解释成“表现为零”。

## 9. ABSTAIN 是不是模型失败？
不是。ABSTAIN 是在支持不足时避免错误确定性的合理决策状态；它是 fail-closed 设计的一部分。

## 10. P108 的含义是什么？
P108 的 Raw=L6，但 R=0.375，Adjusted=2.25，最终是 LOW_SUPPORT/ABSTAIN。它展示了高表现信号不一定有足够支持。

## 11. 你们的模型是否比 ML 更好？
不能这样说。ML challenger 只是参照：LogReg≈0.876、Tree≈0.919、RF≈0.922，但跨学期 RF=0.588，因此结论是 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`，不存在单一 winner。

## 12. 为什么不追求更高准确率？
因为本项目当前的核心问题不是预测竞赛，而是证据是否可识别、是否支持结论。把任务改成准确率优化会偏离研究问题。

## 13. 693 个 robustness grid 足够吗？
它覆盖了冻结参数空间中的 693 个组合，其中 660 defined、33 undefined。它支持当前 development slice 的结构性观察，不构成普适定理。

## 14. 参数扰动结果是什么？
在 ±10% 和 ±20% 扰动下，decision-state flips 为 0；ranking 为 NOT_APPLICABLE。这个结果说明当前状态判断在该扰动范围内稳定，但不等于参数已经正式校准。

## 15. BTC 外部迁移证明了什么？
只证明了结构性检查可以迁移到另一个数据场景：Gate1、Gate2 supported，Gate3 not supported。结果标记为 `STRUCTURAL ONLY`。

## 16. BTC 是否证明了交易优势？
没有。risk-coverage improvement=false，不能声称交易优势、预测优势或通用泛化。

## 17. 为什么 Human Gate 没有运行？
当前 R1=0/70、R2=0/70，Formal Gate=NOT_RUN。材料状态是 AI_PROVISIONAL、DEVELOPMENT_ONLY、NOT_HUMAN_VALIDATED。

## 18. 这能否说明 AI 提高了学习效果？
不能。缺少合法配对的 Outcome_AI、Outcome_baseline 和独立学习 outcome，因此 AI causal learning gain 不受支持。

## 19. 当前最重要的负结果是什么？
三条：External Transfer Gate3 NOT SUPPORTED；不存在单一主导模型；ML challenger 不足以支持 strong ML claim。

## 20. 下一步是什么？
先完成正式人工标注和 Human Gate，再讨论更强的效果识别；在此之前，结论保持 descriptive / structural、development-only，不扩张 Claim。
