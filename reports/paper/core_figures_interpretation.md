# 核心图论文级解读

> 所有图均来自 `reports/development/`，当前只支持 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 解释。图中为开发版参数敏感性或结构审计，不是正式人工标注结果，也不是统计置信区间。

## Figure 2. Evidence support and identifiability heatmap

### 图名
**Figure 2. 可判读 Evidence 与关键来源变量的联合支持结构**

### 论文 caption
**图 2｜可判读 Student Evidence 与 prompt 引导、上下文截断及标注置信度的联合支持结构。** 每个单元格报告当前开发样本中对应组合的记录数；红色空单元格表示在 AI provisional 数据中没有可判读 Evidence 支持，蓝色单元格表示存在可判读记录。可判读 Evidence 全部落在 `prompt_induced=true`、`context_truncated=false`、`confidence=medium` 的组合中，显示 correction / reliability 对比所需的交叉支持不足。图中结果用于诊断识别边界，不代表这些变量之间已被证明存在因果关系。

### 图告诉评委什么
- 当前可判读 Evidence 的联合支持高度集中，而不是均匀覆盖参数条件。
- `prompt_induced=false`、`context_truncated=true`、low confidence 等关键对照格为空。
- 因此，唯一 prompt/context/reliability correction coefficient 不能从当前开发数据直接识别。
- 这为采用 bounds 而不是点估计提供了数据层面的理由。

### 不能从图推出什么
- 不能推出 prompt 一定造成了 Evidence，也不能推出 AI 一定导致了分数变化。
- 不能把空单元格解释为现实中不存在该类记录；它只表示当前开发样本中没有可判读 Evidence 支持。
- 不能推出 AI actor 的因果效应、学生能力或正式 AIV。
- 不能把 AI provisional 标签当作人工标签真值。

## Figure 3. Prompt assumption versus effective evidence

### 图名
**Figure 3. Prompt 惩罚假设与有效证据覆盖度**

### 论文 caption
**图 3｜在当前开发样本完全分离结构下，`lambda_prompt` 对 effective coverage 的敏感性。** 横轴为 prompt 惩罚假设，纵轴为按权重计算的有效证据覆盖度。随着 `lambda_prompt` 从 0 增至 1，当前 16 条可判读 Evidence 的有效支持单调下降；由于这些记录均具有 `prompt_induced=true`，在极端假设 `lambda_prompt=1` 时有效支持归零并触发 `NO_EFFECTIVE_EVIDENCE`。该曲线描述假设下的权重变化，不是 prompt 的估计因果效应。

### 图告诉评委什么
- prompt penalty 主要改变支持量，而不是在当前结构下改变归一化后的分数。
- 权重从 1 到 0 的透明变化可以直观看到 evidence support collapse。
- 当支持为 0 时，系统会返回不可定义状态，而不是填 0。

### 不能从图推出什么
- 不能把横轴当作从数据估计出的真实 prompt effect。
- 不能说真实世界中的 prompt 引导强度必然位于 0–1 的某个特定值。
- 不能据此宣称 AI 造成了学习损失或收益。
- 不能忽略正式人工标签和对照支持仍然缺失。

## Figure 4. Bounds: score stable, support collapses

### 图名
**Figure 4. 分数稳定与证据支持退化的分离**

### 论文 caption
**图 4｜Partial Identification 视角下的 Evidence Support 退化（须结合表中 Score bounds 阅读）。** 当前 SVG 实际只绘制 effective coverage 对 prompt 惩罚假设的曲线，并未绘制 ABL、HOT、Gap 曲线或区间；这些分数近似不变的结论来自配套的 `partial_identification_summary.json`。该配套分析说明分数稳定不能替代证据支持审计；当分母为零时，评价状态应记为 `NO_EFFECTIVE_EVIDENCE`，指标为 undefined under assumption。图示是 assumption-based sensitivity behavior，不是统计置信区间。

### 图告诉评委什么
- 配套 bounds 结果至少有两个维度：归一化 Score 与 support 规模。
- 只看 Score 会遗漏有效证据快速减少的情况。
- Bounds 的价值不仅是给出上下界，也是把“何时失去定义”明确显示出来。
- 评委阅读本图时应同时查看 `partial_identification_summary.json`，不要把 SVG 单独解读为同时绘制了 Score 和 Support。

### 不能从图推出什么
- 不能推出 ABL/HOT/Gap 已经是正式有效的学生能力估计。
- 不能把 support collapse 解释成已识别的 prompt causal effect。
- 不能以图中稳定分数证明模型具有外部有效性或跨人群稳健性。
- 不能把假设区间当成测量误差的概率区间。

## Figure 5. Measurement-to-AIV decision flow

### 图名
**Figure 5. 从观察日志到正式 AIV 的证据门控流程**

### 论文 caption
**图 5｜从观察日志、Evidence 筛选、Support 检查到 Bounds 分析的分阶段评价流程。** 只有在证据支持、标注可靠性、Gate 状态和识别条件满足后，结果才可能进入正式 AIV 解释；开发版数据当前在 formal AIV 之前停止。该流程强调 AIV 不是对原始日志的直接打分，而是经过证据筛选与可识别性门控的条件性产物。

### 图告诉评委什么
- 研究不是从原始日志直接跳到 AIV，而是逐级检查 measurement、support 和 identification。
- 当前开发结果的正确终点是 bounds / sensitivity，而不是 formal AIV。
- 该流程与项目的 fail-closed 原则一致：条件不足时拒绝推进。

### 不能从图推出什么
- 不能推出当前项目已经通过 Gate 或已经拥有正式 AIV。
- 不能把流程图中的最后一个框理解为当前结果。
- 不能把“可进入正式 AIV”解释成“已经识别了 AI 因果增量”。
- 不能替代正式人工 R1/R2、可靠性检验和预注册阈值。

## 统一图注尾注建议

建议四张图在论文中统一附注：

> Results shown are `AI_PROVISIONAL` and `DEVELOPMENT_ONLY`; `formal_gate_eligible=false`. The displayed ranges are assumption-based identification/sensitivity results, not statistical confidence intervals, causal effects, formal AIV estimates, or student rankings.
