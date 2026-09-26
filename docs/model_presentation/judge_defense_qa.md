# Judge Defense QA

1. **为什么乘 Reliability？** 这是透明、单调、可审计的 evidence-weighted 结构；低可靠性不会放大贡献，权重为零就没有有效贡献。它不是唯一正确形式。
2. **权重怎么来？** 来自可观察性、confidence、prompt/context 风险的冻结规则；`c_i`、两个 lambda 仍是 `WEAKLY_JUSTIFIED_COMPONENT`，不是校准概率。
3. **为什么不直接丢掉低质量数据？** 保留 Raw 与降权后的支持度，便于审计；只有有效证据为零才 `NO_EFFECTIVE_EVIDENCE`。
4. **Adjusted Score 是 AI Increment 吗？** 不是。Adjusted 是证据加权结果；AI Increment 需要 `Outcome_AI−Outcome_baseline`。
5. **证明 AI 提升学习了吗？** 没有。当前没有合法配对 outcome。
6. **为什么 AI Increment 是 NOT_SUPPORTED？** 当前没有可比的 AI 与 baseline 配对观测。
7. **没有 baseline 项目还有什么价值？** 它仍能识别可观察表现的证据支持程度，并在证据不足时 abstain。
8. **Reliability 是概率吗？** 不是；它是有界支持权重，尚未外部校准。
9. **lambda_prompt 为什么这样取？** 是冻结的开发敏感性参数；敏感性分析检验结构稳健性，不把它包装成估计量。
10. **参数是不是人为调出来的？** 有人为设定成分，因此明确标弱依据，并用预先声明的网格报告敏感性。
11. **Sensitivity 证明什么？** 在当前 ±20% 网格内分数与决策不变、支持度变化；不证明普适稳定。
12. **Ablation 证明什么？** 证明组件改变有效支持贡献；不证明准确率。
13. **为什么要 ABSTAIN？** 让证据不足时不输出过度确定的评价。
14. **NO_EFFECTIVE_EVIDENCE 和 0 分区别？** 前者表示没有有效证据，后者是有证据但数值为零；本模型不把前者填成 0。
15. **Accuracy 有没有提高？** `NOT_SUPPORTED`；缺少合法 truth/prediction 配对。
16. **HUMAN R1/R2 验证什么？** 同一标注者两轮的 test-retest；目前尚未完成。
17. **Formal Gate 为什么未 PASS？** R1/R2 尚未返回，Formal Gate `NOT_RUN`。
18. **当前数据最大弱点？** 16 条可判读证据都带 prompt 风险，且缺少 baseline。
19. **能迁移到别的教育场景吗？** 结构可作为候选框架，但需要该场景重新定义证据字段并通过人工 Gate。
20. **更多数据下一步验证什么？** 完成人工 R1/R2、配对 baseline 与独立 outcome，再检验校准和选择性评价。
21. **为什么不是加法？** 乘法直接保证低支持不放大贡献，且易审计；替代函数需要单独比较，当前没有做出优越性声明。
22. **Coverage 覆盖什么？** `C=n_observed/N` 或 `C_eff=Σw_i/N`；当前开发分母是全部 70 条记录，必须随数值报告。
