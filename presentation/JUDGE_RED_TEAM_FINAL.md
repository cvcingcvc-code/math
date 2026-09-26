# JUDGE RED TEAM FINAL

> 最危险的 10 个评委追问 + 严格基于现有 artifact 的答案。
> 生成日期：2026-09-27。**答案不得超越现有证据边界。**

---

## 1. Reliability 为什么这么定义？

不是「拍脑袋」：它由三个可审计的证据属性显式进入——可判读性（`I(observable_i)`）、标注置信度（`c_i`）、prompt/context 风险折减。它明确**不是**概率、**不是**因果系数，而是「这条信号有多少可审查支撑」的声明性权重。合理性通过 693 格参数网格敏感性检验来兜底，正式校准留待 Human Gate。

## 2. 参数为什么是 0.5 / 0.75？

`λ_prompt=0.5`、`λ_context=0.5`、`r_medium=0.75` 是**冻结的透明声明假设**（preregistered design assumptions），不是从样本学习得到的最优值。论文已把它们标为 `WEAKLY_JUSTIFIED_COMPONENT`，并明确不声称已完成正式校准。我们做 ±10%/±20% 扰动和 693 格网格，正是为了检验「结论是否依赖这些具体取值」——结果显示归一化分数稳定、支持度跨 40 倍变化，说明核心机制不依赖单点取值。

## 3. 为什么只有 16 条可判读？

因为 70 条里 19 条 NO_EVIDENCE、35 条 UNDETERMINED，合计 54 条没有可判读的学生证据。模型不把不可判读记录强行转成数值，而是 fail-closed 返回 `NO_EFFECTIVE_EVIDENCE`。这不是数据丢失，而是诚实的数据审计结果。

## 4. 54 条没有 Evidence，模型是不是没意义？

不是。54 条**不是** 54 个零分，而是「没有足够证据进入有效评价」的记录。把它们编码成 0 分，等于用「没有证据」伪造「表现为零」。模型的 fail-closed 规则（`Σw_i=0 → NO_EFFECTIVE_EVIDENCE`）正是为了不制造这种伪结果。Missing Evidence ≠ Zero Performance。

## 5. Score 都没变，模型到底改变了什么？

分数（ABL/HOT/Gap）恒为 3.5625/0.375/1.125，是因为 16 条可判读记录共享同一组因子，公共缩放因子在归一化中抵消——这**本身就是研究结果**。真正改变的是：Raw-only 无法报告的「证据支持」从 16 个单位降到 6 个单位、覆盖率从 0.228571 降到 0.085714。分数看起来一样确定，证据的确定性已经下降 62.5%。所以结论是「Score Stability ≠ Evidence Support Stability」，不是「模型提升了分数」。

## 6. 乘法为什么不是人为设计？

论文明确不声称乘法结构是唯一正确或最优结构——第 7 章用四种替代形式（加法/门控/非线性）做对照，结论是 `NO_SINGLE_DOMINANT_MODEL`。保留乘法是因为「研究问题对齐 + 透明 + 显式缺失语义 + 拒判结构」，不是「已证明最优」。核心现象（分数稳定而支持下降、缺失不填 0）在多种形式下都存在，说明结论不依赖乘法形式。

## 7. 为什么需要 ABSTAIN？

当证据不足时，拒绝形成强判断，比输出一个貌似精确的数字更合理。ABSTAIN 是模型的**合理输出**，不是失败——它显式表达「不足以形成可靠判断」，防止过度结论（overclaim）。当前切片下 0 条 ACCEPT，正说明在 AI 提示诱导普遍、置信度普遍 medium 的数据上，诚实的框架不应该给出确定性结论。

## 8. ML 指标比你的模型看起来高，为什么不用 ML？

ML 表面 CV 判别不低（0.876/0.919/0.922），但：① positive 只有 16 且是 AI provisional 代理标签，≠ human truth；② 重复 CV 是对同一 70 条记录的重采样，无独立 holdout；③ 特征缺失 20%/40% 后降到 0.71–0.81，RF 跨学期仅 0.588；④ 更根本地，ML 是「pre-label predictor」（预测哪条会被标可判读），主模型是「post-label support transformation」（拿到证据标签后做支持变换 + fail-closed 拒判），二者不是同一件事，不构成替代。因此正确表述是 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`，不是「手工模型更准」。

## 9. 为什么拿 BTC 来验证？

不是要做金融预测，而是**刻意**选一个性质完全不同的 noisy-signal domain 做 stress test，检验同一个 `Raw → Reliability → Adjusted → Coverage → Decision` 结构是不是只为教育数据量身定做。教育场景和金融场景的 Raw Signal 同样面临 noisy / missing / conflicting information。结果 Gate1、Gate2 SUPPORTED（结构可迁移），Gate3 NOT SUPPORTED（低 Reliability 并不带来更高 future error rate）——这个失败我们**主动保留**，因为它诚实界定了「Reliability 尚未被证明是未来正确性的 calibrated predictor」。

## 10. Human Gate 没做，你这个结论还能信到什么程度？

结论只能信到它的**声明的级别**：`descriptive / structural`（Evidence Level 1）、`DEVELOPMENT_ONLY`、`NOT_HUMAN_VALIDATED`。我们明确 Human R1=0/70、R2=0/70、Formal Gate=NOT_RUN，且不声称 AI 提高学习、不声称因果增量、不声称任何准确率提升或通用泛化。正式结论须等待 Human Gate 完成（PENDING HUMAN-ANNOTATION INTAKE VERIFICATION）。把结论边界说清楚，恰恰是这项工作的诚实性所在。
