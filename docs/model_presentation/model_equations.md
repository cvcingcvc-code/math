# 核心公式（展示版）

## 1. 可观察证据

`I(observable_i)=1` 当 `Student Evidence ∈ {L1,…,L6}`，否则为 0。它防止 `NO_EVIDENCE/UNDETERMINED` 被误当作低分。

## 2. 证据可靠性权重

`w_i = I(observable_i) × c_i × (1−λ_prompt p_i) × (1−λ_context t_i)`

`c_i`: high=1、medium=0.75、low=0.5；`p_i,t_i` 是风险标记；`λ` 是开发版敏感性参数。它表示支持度，不是概率，也不是因果系数。

## 3. 调整后分数与覆盖率

`Score_adj = Σ(w_i y_i)/Σw_i`（`Σw_i>0`）；`C_eff=Σw_i/N`，`N` 包含全部分析记录。无有效支持时返回 `NO_EFFECTIVE_EVIDENCE`。

`Adjusted Score` 不等于 `Reliable AI Increment`；后者需要当前项目尚未具备的 `Outcome_AI−Outcome_baseline`。
