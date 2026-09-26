# 研究核心闭环验收（开发版）

本报告只使用 70 条 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 记录，不能替代人工 R1/R2、正式 Gate 或 Formal AIV。

## 当前模型

`w_i = I(observable_i) × c_i × (1 − λ_prompt prompt_i) × (1 − λ_context context_i)`。

`observable_i` 指 Student Evidence 为 L1–L6；NO_EVIDENCE 与 UNDETERMINED 权重为 0。置信度权重为 high=1.0、medium=0.75、low=0.5。权重和为 0 时返回 `NO_EFFECTIVE_EVIDENCE`，不填 0 分。

## 六个结论问题

1. **是否存在 measurement problem？** 是。70 条中只有 16 条可判读 Evidence，54 条为 NO_EVIDENCE/UNDETERMINED；且可判读集合全部 `prompt_induced=true`，说明可观察证据与引导路径完全分离。
2. **校正是否改变分数？** 在当前切片和公共缩放结构下，ABL=3.5625、HOT=0.3750、Gap=1.1250 保持不变；支持量从 16.0000 降为 6.0000。
3. **影响最大的风险因素是什么？** 当前可识别的主要风险是 prompt-induced evidence；context 风险在可判读 16 条中没有变异，因此只能作为压力情景，不能从本切片估计其独立影响。
4. **Score 与 Evidence Support 是否不同稳定？** 是。有效参数区间中分数稳定，但 effective coverage 从 0.228571 降至 0.085714；支持度比得分更敏感。
5. **模型发现了 Raw Score 无法表达的问题吗？** 是。Raw Score 会把 P108 的 L6 当成可直接解释的高证据，而校正模型同时报告其 prompt 风险和有限支持；P072/P035 则直接拒绝给出分数。
6. **是否支持 Formal AIV？** 否。缺少完成的人工 Gate、可比 AI/non-AI 条件、前后测与独立学习结果；Formal AIV 继续保持 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

## 消融结果

见 `ablation_results.csv`。M0–M3 都使用同一批 70 条记录；消融用于定位风险因素，不用于证明 M3 的预测准确率。

## 反例

见 `counterexamples.csv`。四条记录全部来自原始 development CSV，未人工编造；其中没有 `prompt_induced=false` 且 Evidence 可判读的记录，因此当前数据不能支持“独立 Evidence”案例。

## 冻结状态

Reliability Model、Raw/Adjusted、Sensitivity、Ablation、Counterexamples 和研究结论均已形成可复现产物，可标记为 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`。正式 Gate 与 AIV 扩展仍必须等待人工 R1/R2。
