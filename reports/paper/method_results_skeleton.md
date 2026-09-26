# 教育 AI 交互证据评价：方法与结果骨架（开发版）

> 本文骨架只承载 DEVELOPMENT_ONLY / AI_PROVISIONAL 结果，不替代正式人工标注、Gate 或 AIV。

## 1 Introduction
AI 介入后，观察到的学生文本不自动等于学生能力。

## 2 Problem Definition
定义 observed evidence、student evidence、prompt-induced evidence、measurement uncertainty、support 与 identifiability。

## 3 Data and Measurement
说明 70 条开发样本、L1-L6 可判读 Evidence、NO_EVIDENCE/UNDETERMINED 拒判状态，以及 AI provisional 与 human R1/R2 的边界。

## 4 Identifiability Diagnosis
报告 16 条可判读 Evidence 的完全分离：prompt=true、actor=ai、confidence=medium、context_truncated=false，并区分数据生成、规则、provisional 标签和字段映射来源。

## 5 Model
使用 assumption-based identification interval，而不是唯一惩罚系数：

`w_i(theta)=I(E_i=L1..L6) * c_i * (1-lambda_prompt*p_i) * (1-lambda_context*t_i)`

对参数集合 Θ 计算 ABL/HOT/Gap/有效证据权重的可行范围；分母为零时记为 undefined。该区间不是统计置信区间。

## 6 Experiments
开发版包括参数网格、压力测试和组件状态审计；不比较 accuracy，不拟合复杂模型。

## 7 Results
当前最重要结果是：有效区间内 ABL/HOT/Gap 基本稳定，但有效 Evidence weight 随 prompt penalty 下降并可退化为零；不确定性主要来自 evidence availability。

## 8 Limitations
缺少真实 R1/R2、独立无 AI outcome、可靠 session_id、可比 prompt 对照和充分 actor/confidence 支持；不能宣称因果增量、正式 AIV 或学生排名。

## 9 Discussion
“先证明 Evidence 可解释”是教育 AI 增量价值评价的必要前置条件之一；这里是方法论命题，不是已验证因果结论。

## 10 Formal replacement plan
人工标签返回后，以统一输入接口替换 source_type/mode，重跑 Gate、可靠性、support audit、bounds、stress tests 和最终图表；不得把开发结果覆盖为正式结果。
