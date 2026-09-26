# 评委 3 分钟模型故事

## 1. 现实问题

AI 辅助学习里，学生的答案、操作和行为并不都同样可信。有的记录信息完整、学生自己完成、上下文充分；有的记录带有明显 AI 引导、上下文被截断、来源冲突或标注不确定。看见一个高分，不等于这条分数有同样高的证据支持。

## 2. 数学思想

传统评价只问“表现有多高”。本模型同时问“表现有多高”和“这条表现证据有多可信”。因此每条观察拆成 `Raw Signal` 与 `Evidence Reliability`。

## 3. 核心公式

`w_i = I(observable_i)c_i(1−λ_prompt p_i)(1−λ_context t_i)`  
人话：先确认有可判读证据，再按置信度、提示风险和上下文风险给支持权重；`w_i` 是支持度，不是概率。

`Adjusted_i = Raw_i × w_i`  
人话：同样是 6 分，若支持度只有 0.375，它的有效贡献就是 2.25；低支持不会被放大。

`C_eff = Σ_i w_i / N`，本开发切片 `N=70`。  
人话：覆盖率的分母是全部 70 条记录，不是 16 条可判读记录。

当 `Σw_i>0`，用加权结果汇总；支持规则通过时为 `ACCEPT`，证据不足时为 `ABSTAIN`，权重为零或没有可判读证据时为 `NO_EFFECTIVE_EVIDENCE`。`LOW_SUPPORT` 是支持等级标签，不是把它包装成准确率。

## 4. 为什么乘 Reliability

乘法是透明、单调、可审计的 evidence-weighted 结构：可靠性越低，贡献不会被放大；可靠性为 0 时不产生有效贡献。它不是理论上唯一正确的形式，稳健性由 sensitivity、ablation 和 Human Gate 检查。当前 `c_i`、`λ_prompt`、`λ_context` 含 `WEAKLY_JUSTIFIED_COMPONENT`，尚未校准为概率。

## 5. 一个真实开发案例

`P108`（`DEVELOPMENT EXAMPLE / AI_PROVISIONAL`）：`Raw=6`，`Reliability=0.375`，`Adjusted contribution=2.25`，状态 `LOW_SUPPORT`，答辩动作是 `ABSTAIN`。它说明高 Raw 也可能只有低支持。`P072` 的证据不可判读且上下文截断，`Reliability=0`，直接 `NO_EFFECTIVE_EVIDENCE`，不填成 0 分。

## 6. 能说什么、不能说什么

模型最重要的能力是在证据不足时拒绝装作确定：证据强就评估，证据弱就降低贡献或暂缓，证据缺失就报告 `NO_EFFECTIVE_EVIDENCE`。当前它评价的是 AI 辅助环境下的可观察表现与证据支持程度，不能证明学生真实能力提升、长期学习增益、AI 因果效果、正式 AI Increment 或能力排名。Formal HUMAN R1/R2 尚未完成，所有案例仍是 `DEVELOPMENT_ONLY`。

理论分支单独保留：`Delta_raw = Outcome_AI − Outcome_baseline`，`Delta_reliable = Delta_raw × R`。当前没有合法配对的两个 outcome，因此二者均为 `NOT_SUPPORTED`。
