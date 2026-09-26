# 模型组件解释表

| Component | Mathematical meaning | Human meaning | Current status | Risk |
|---|---|---|---|---|
| Raw Signal | `y_i`，Student Evidence L1–L6 | 观察到的证据等级 | DEVELOPMENT_ONLY | 不是 AI 增量 |
| Reliability `R` | `w_i=I c_i(1−λ_p p_i)(1−λ_c t_i)` | 这条证据值得信多少 | DEVELOPMENT_ONLY | 非校准概率 |
| `c_i` | confidence 映射 high=1, medium=.75, low=.5 | 标注判断的确定程度 | WEAKLY_JUSTIFIED_COMPONENT | 待 Human Gate |
| `lambda_prompt` | 提示风险惩罚系数 | AI 引导可能削弱支持 | WEAKLY_JUSTIFIED_COMPONENT | 当前可判读记录均 prompt=true |
| `lambda_context` | 上下文截断惩罚系数 | 缺上下文削弱支持 | WEAKLY_JUSTIFIED_COMPONENT | 当前切片缺少变异 |
| Adjusted | `Raw_i×R_i`；汇总为加权分数 | 低支持贡献被降权 | DEVELOPMENT_ONLY | 不等于增量 |
| Support | `S=Σ_i w_i` | 有效证据总量 | DEVELOPMENT_ONLY | 不等于行覆盖 |
| Coverage | `C=n_observed/N` 或 `C_eff=Σw_i/N` | 覆盖全部输入记录的比例 | DEVELOPMENT_ONLY, `N=70` | 必须写清分子分母 |
| ACCEPT | 声明的分数和支持规则通过 | 可以按当前规则接受 | 未经 Formal Gate | 需同时报告错误/覆盖 |
| ABSTAIN | 证据不足、冲突或未过支持规则 | 暂缓判断 | DEVELOPMENT_ONLY | 不能宣传准确率提升 |
| NO_EFFECTIVE_EVIDENCE | `S=0` 或无可判读证据 | 有效证据缺失 | DEVELOPMENT_ONLY | 不等于 0 分 |
| Delta_raw | `Outcome_AI−Outcome_baseline` | 配对条件下的观察差 | NOT_SUPPORTED | 当前无合法 baseline |
| Delta_reliable | `Delta_raw×R` | 对已识别增量再加支持权重 | NOT_SUPPORTED | 不得用 Adjusted 替代 |
