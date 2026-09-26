# 逐页口播稿

## 开场（约 25 秒）
我们一开始以为，这个问题的核心是怎么计算一个更好的学生表现分数。但整理数据后发现，真正的问题其实更早：当证据本身并不完整的时候，我们有没有资格直接相信这个分数？所以全场只回答一句话：**我们不是重新给学生打分，而是在回答：这个分数，到底有多少证据值得相信？** 另一句等价的话是：**一个结果有多高，和我们有多大把握解释这个结果，不是一回事。**

## 30 秒核心发现讲法（随时备用）
我们的核心结果其实很反直觉。加入 Reliability 以后，归一化 Score 仍然是 3.5625。如果只看分数，看起来什么都没有改变。但是有效 Support 从 16 降到 6，Coverage 从 22.86% 降到 8.57%。所以真正变化的不是表面的 Score，而是：我们到底有多少证据支撑这个 Score。这就是 Score Stability 不等于 Evidence Support Stability。

## 1｜观察到的结果，不等于可靠证据（约 35 秒）
我们研究的不是“AI 是否提高成绩”，而是一个更基础的测量问题：当观测证据缺失、冲突或者可信度不同的时候，能不能避免把 Raw Signal 直接当成可信结论。开场的现实入口是：**我们不是重新给学生打分，而是问这个分数有多少证据值得相信。** 我们的核心判断是，分数稳定不等于证据支撑稳定。也就是说，系统不仅要给出一个表现水平，还要把证据可靠性、支持范围以及暂缓判断的情况一起报告出来。

## 2｜为什么 Raw Signal 不够（约 45 秒）
Raw Signal 只告诉我们观察到了什么，不告诉我们这些观察是否足以支撑结论。这里把 Raw 和 Evidence Reliability 明确拆成两层。即使最终归一化后的数值看起来没有变化，也不能由此推断证据支持没有变化。真正需要追踪的是有效证据有多少、覆盖了多少记录，以及哪些记录应该暂缓判断。

## 3｜Reliability-aware evaluation（约 55 秒）
我们的固定链路从 Observed Evidence 开始，先得到 Raw Signal，再计算 Evidence Reliability，接着得到 Adjusted Evaluation，最后同时输出 Support、Coverage 和决策状态。权重由可观测性、置信度、prompt 和 context 因子共同决定。这里的 R 是确定性的支持权重，不是校准概率。若没有有效证据，系统返回 NO_EFFECTIVE_EVIDENCE，而不是把缺失伪装成 0 分；如果支持不足，则允许 ABSTAIN。

## 4｜Development slice（约 45 秒）
当前 development slice 是 70 条 AI provisional records，其中只有 16 条可判读。另有 19 条 NO_EVIDENCE、35 条 UNDETERMINED，所以 54 条进入 NO_EFFECTIVE_EVIDENCE。这个 54 不是 54 个零分，而是没有足够证据去定义一个可评价的数值。这个区分是后续所有 coverage 和拒答结论的基础。

## 5｜公共缩放退化（约 60 秒）
16 条可判读记录共享同一组因素：prompt=true、context=false、confidence=medium，因此每条 Reliability 都是 0.375。公共缩放会在归一化的平均分里被抵消，所以 ABL、HOT、Gap 仍然是 3.5625、0.375、1.125，看起来像稳定。但有效权重从 16 下降到 12、再到 6，coverage 从 0.228571 下降到 0.085714。这说明稳定的 score 不能替代稳定的 evidence support。

## 6｜五条验证路径（约 55 秒）
这里的五条路径不是五个彼此独立的新主张，而是共同回答同一个问题：当 score 看似稳定时，evidence support 是否也稳定。鲁棒性网格一共有 693 个组合，其中 660 个有定义、33 个无定义；参数扰动 ±10% 和 ±20% 都没有造成 decision-state flip。消融、失败案例、ML challenger 和外部迁移分别约束支持范围、拒答语义和外推边界。

## 7｜失败不是 0 分（约 55 秒）
P108 的 Raw 是 L6，但 Reliability 只有 0.375，Adjusted contribution 是 2.25，因此状态是 LOW_SUPPORT / ABSTAIN。P105 的 Adjusted 是 0.75，同样是低支持。P072 和 P035 没有可判读证据，Adjusted 为 null，返回 NO_EFFECTIVE_EVIDENCE。ABSTAIN 是合理输出，不是模型失败；把无证据写成 0 分，反而会制造虚假的确定性。

## 8｜Challenger 与外部迁移（约 65 秒）
ML challenger 的单次结果是 LogReg 约 0.876、Tree 约 0.919、RF 约 0.922，但 RF 跨学期只有 0.588，所以不能声称存在 ML winner，也不能声称手工框架优于 ML。BTC 外部迁移中，Gate1 和 Gate2 supported，Gate3 not supported，risk-coverage improvement 为 false。因此外部结果只支持 structural only：它说明结构可以被检查，不支持交易优势、预测优势或通用泛化。

## 9｜研究边界（约 45 秒）
当前状态是 AI_PROVISIONAL、DEVELOPMENT_ONLY、NOT_HUMAN_VALIDATED。Human R1 和 R2 都是 0/70，Formal Gate 是 NOT_RUN，AI increment identification 是 NOT_SUPPORTED。我们没有合法配对的 Outcome_AI 和 Outcome_baseline，因此不能声称 AI 提高学习效果、因果增量、准确率提升或普适泛化。把边界说清楚，是结果可信度的一部分。

## 10｜结论与 Demo（约 35 秒）
最后只保留一个结论：Score Stability 不等于 Evidence Support Stability。现场 Demo 只走四个锚点：研究问题、模型链路、主结果和 P108 失败案例。如果交互展示不稳定，直接切换到离线静态 Demo 和六张冻结图，主线不改变。