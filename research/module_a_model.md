# S3 模块 A：认知标注、校验抽样与误差传播候选

> **DECISION** 当前阶段不训练 LLM。先建立人工 codebook、抽样标注协议和统计可靠性/效度检查。AI 预标注只是待校验的编码建议，不是金标准。

## A1. Bloom 六级和三阶定义

设一条可判读文本单元 $i$ 的标签 $Y_i\in\{1,2,3,4,5,6\}$，分别是：

| 编码 | 名称 | 判定标准（基于认知活动，不仅按动词） |
|---|---|---|
| L1 | 记忆 Remember | 从记忆中提取、列出、识别、复述事实/规则。 |
| L2 | 理解 Understand | 用自己的话解释、归类、概括、推断意义或关系。 |
| L3 | 应用 Apply | 在给定问题/新情境中执行方法、程序或模型。 |
| L4 | 分析 Analyze | 将问题/论证拆解，比较组成部分、结构、因果/依赖关系。 |
| L5 | 评价 Evaluate | 按明确标准和证据检查、论证、批判或作判断。 |
| L6 | 创造 Create | 组合要素，提出连贯的新方案、模型、设计或实施计划。 |

另设 U=不可判读/没有足够可见学生证据。**U 不等于 L1 或 0 分**；它不纳入六级均值分母，但纳入 coverage 和缺失率。`task_bloom` 对任务要求编码，`student_evidence_bloom` 只对学生实际文本证据编码。

三阶映射为 $g(Y)$：低阶 L={L1,L2}；中阶 M={L3}；高阶 H={L4,L5,L6}。映射是赛题口径候选；它压缩序数信息，作为稳健性/教学粗分版本，不替代六级主标注。

### 关键标注规则

1. 任务或问题出现“分析/评价/设计”字词不能自动定高阶，须判断完成任务实际需要的认知操作。
2. 只问 AI “给我设计/评价”而无学生论证，task 可能高阶，但学生 evidence 可为 U/低层级。
3. AI 生成的步骤、证明和答案不记作学生证据；学生只复制内容也不能无证据升高层级。
4. 同一学生回答含多种证据，按预先规则拆成最小语义单元；无法稳定拆分时保留整体并记录多标签/歧义，不择最高层级制造 HOT。
5. 标注记录需包含：原始片段 ID、speaker、task/evidence 两个标签、置信/歧义原因、人工编码员和 adjudication 状态。

## A2. AI 预标注 + 分层人工校验

### 分层设计

1. 对所有可判读候选单位运行固定版本的预标注工具/人工辅助规则，记录版本、提示、输出概率向量 $\mathbf{q}_i$、主体置信度和原始文本哈希；本阶段不训练模型。
2. 定义 strata $h$ 为 `semester × agent_type/Unknown × predicted Bloom band × confidence band × text-type` 的可操作组合；稀疏 strata 合并前记录规则。
3. 在 strata 内按学生 cluster 抽取，再随机抽取 turns，降低同一学生重复记录造成的伪独立；另设每层最低随机抽样量和低置信/少数类过抽样。仅抽“模型不确定”的数据不能无偏评估总体一致性。
4. 每个抽样 turn 由两名编码员独立、盲于 AI 预测/对方标签标注；分歧交第三位 adjudicator 给最终审计标签。分别对 `task_bloom` 和 `student_evidence_bloom` 做校验。
5. 主估计用已知 inclusion probability $\pi_i$ 的设计权重 $w_i=1/\pi_i$；报告抽样流程、样本数、学生 cluster 数、各层支持量及加权/非加权结果。

### 抽样量和可靠性约束

设 $N_h$ 是 h 层可标注 turn 总数，$n_h$ 是人工双标数，$c_h$ 是每个 turn 的双标人工成本。总人工成本：

\[
\min_{n_1,...,n_H\in\mathbb Z_+}\quad C_{human}=\sum_{h=1}^H c_h n_h
\]

满足：

\[
\operatorname{LCB}_{1-\alpha}\{R_{ord}(n_1,...,n_H)\}\ge \tau,
\qquad n_h\ge n_{h,min},\qquad n_h\le N_h.
\]

其中 $R_{ord}$ 是主序数可靠性指标（预先选加权 Cohen κ 或 ordinal Krippendorff α）；`LCB` 为 cluster/design-aware bootstrap 的单侧置信下界；(	au) 是项目预先决策的阈值，$\alpha$ 为置信错误水平。阈值和最少分层支持量当前是 **UNKNOWN/待人工决定**，不可伪装成标准答案。若六级难达阈值，可报告三阶可靠性作为另一种用途，不得用合并类别隐去六级失败。

可用 pilot 估每层类别率/混淆和编码成本，再枚举或模拟 $n_h$，选满足可靠性约束的最低成本配置。仅作初始分配参考的 Neyman 型分配为 $n_h\propto N_h S_h/\sqrt{c_h}$；它优化的是层比例估计的方差近似，**不保证**最小化 κ/α 约束成本，最终配置要以 pilot bootstrap 模拟验证。AI 预标成本若随样本固定，可加常数 $C_{pre}$，不影响最优 $n_h$。

**输入**：候选全量文本 ID、预标签、层属性、置信度、学生 ID、成本、阈值 (	au)。  
**输出**：按层/学生 cluster 的抽样清单、每条 $\pi_i$、双人标签、可靠性及区间、成本与可复现随机种子。

## A3. Cohen weighted kappa 与 Krippendorff alpha

### Cohen weighted κ

用于**恰好两位评定者**在同一批单位上的配对分类，适用于名义/序数标签；Bloom 六级有序时可用预先声明的线性或二次权重。

二次相似权重候选：

\[
w_{ab}=1-\left(\frac{a-b}{K-1}\right)^2,\quad K=6.
\]

若 $\hat p_{ab}$ 为评定者 1 给 a、评定者 2 给 b 的联合比例，边际比例为 $\hat p_{a+},\hat p_{+b}$：

\[
P_o^w=\sum_{a,b}\hat p_{ab}w_{ab},\quad
P_e^w=\sum_{a,b}\hat p_{a+}\hat p_{+b}w_{ab},\quad
\kappa_w=\frac{P_o^w-P_e^w}{1-P_e^w}.
\]

假设/限制：同一单位配对、评定者可视为独立、类别和权重预定；κ 受类别流行率/边际分布影响；不报告矩阵会掩盖特定类错分。置信区间需考虑按学生聚类和分层抽样权重。task 与 student evidence 不能混在同一个表算 κ。

### Krippendorff α

适合两名或多名编码员、不同尺度类型且存在部分缺失的内容标注。设观测分歧 $D_o$ 和依偶然一致预期分歧 $D_e$：

\[
\alpha=1-\frac{D_o}{D_e},\quad
D_o\propto\sum_{a,b}o_{ab}\delta_{ab},\quad
D_e\propto\sum_{a,b}e_{ab}\delta_{ab}.
\]

序数标签可用 δ_ab=(a-b)^2（常数归一不影响 α）；须声明距离函数、缺失规则、单位定义。若 $D_e=0$（无类别变化）则 α 不定义/无信息。信度仍不证明该分类代表能力。可同时给原始一致率、混淆矩阵、每类 precision/recall/F1、六级及三阶结果。

## A4. 标签误差混淆矩阵 → 概率标签

令人工裁决/审定标签 (Y_i=k) 为操作性 reference，预标注硬标签为 $\hat Y_i=a$，在分层 h 内估计：

\[
C^{(h)}_{ak}=P(Y=k\mid \hat Y=a,h),\qquad \sum_k C^{(h)}_{ak}=1.
\]

用抽样权重 $w_i=1/\pi_i$ 计算加权计数并作行归一；小样本层可合并或用 Dirichlet 平滑（先验参数作为敏感性输入），不能直接把稀疏行解释成精确概率。

若预标注输出 $\mathbf{q}_i=(q_{i1},...,q_{i6})$（概率分布），一个可运行的校正候选为：

\[
p_{ik}=\sum_{a=1}^6q_{ia}C^{(h_i)}_{ak}.
\]

硬标签时 $\mathbf{q}_i$ 为 one-hot，$\mathbf{p}_i$ 是该预测类和校验层的经验真类比例。若工具不给经过校准的 q，只用 one-hot 经验行；不要把 LLM 自报 confidence 当校准概率。校验集另用 Brier score/对数损失检查概率校准。

**假设**：校验抽样在 h 内可代表待校正数据；reference 标注经盲标/裁决且自身误差可接受；混淆关系在 h 内足够稳定。若这些假设不成立，矩阵误差也要纳入 bootstrap，且结果标为探索性概率。

## A5. 概率标签下 ABL / HOT

期望层级标签：

\[
E[z_i\mid data]=\sum_{k=1}^6 k p_{ik}.
\]

学生 s 的概率 ABL：

\[
ABL_s=\frac{\sum_{i\in s}r_i\sum_{k=1}^6 k p_{ik}}
{\sum_{i\in s}r_i},\qquad r_i=1\text{ for eligible evidence turns}.
\]

HOT 概率：

\[
HOT_s=\frac{\sum_{i\in s}r_i(p_{i4}+p_{i5}+p_{i6})}{\sum_{i\in s}r_i}.
\]

分母只含可判读学生证据 turns；U turns 计入另报的判读覆盖率，不能悄悄当低阶。若需要限制长 session 的支配，应另做 session 等权敏感性分析，而非将两种分母混淆。

## A6. 标签误差传播至 CTQ

候选 session 路径使用连续可判读学生 evidence labels，编码 $z_t\in\{1,...,6\}$，相邻差 (d_t=z_{t+1}-z_t)。候选 CTQ（细节见 C 指标文件）：

\[
CTQ=\begin{cases}
0.5,&\sum_t|d_t|=0,\\
0.5\left(1+\frac{\sum_t d_t}{\sum_t|d_t|}\right),&\sum_t|d_t|>0.
\end{cases}
\]

范围 [0,1]；无迁移=.5；纯下降=0；纯上升=1。为传播误差，不将 $E[z_t]$ 代入非线性 ratio 后只算一次（一般 $E[f(Z)]\ne f(E[Z])$）。而是重复：

1. 从每个 $p_t$ 抽一条 $z_t^{(b)}\sim Categorical(p_t)$，或从校验集中按学生 cluster 重抽标签误差；
2. 按每个抽样路径重算 ABL/HOT/CTQ；
3. 抽样学生/会话再聚合，报告中位数、区间与标签/抽样误差贡献。

若相邻 turn 标签误差相关（同一学生/编码员/智能体路径），独立逐 turn 抽样的 ASSUMPTION 不可靠；应对整名学生/session cluster 重抽或用校验样本估计相邻联合分布 (P(z_t=a,z_{t+1}=b))。CTQ 至少报告 transition 数；路径只有一个有效 transition 时结果高度离散，不能与长路径等精度处理。

## A 验证协议

- 先冻结 codebook 并用不进入正式抽样的 pilot 讨论歧义，再由双编码员独立标记正式概率样本。
- 可靠性分别按六级、三阶、task、student evidence、speaker 计算；报告加权设计估计和学生 cluster bootstrap CI。
- 检查六級相邻/远距错误、低置信层与每个 agent/semester 的分层误差；折叠三阶之后若提高一致性同时掩盖 L4/L5/L6 混淆，需保留六级作为解释限制。
- 把概率标签推到 ABL/HOT/CTQ，检查学生分布、置信区间和名次变动；“标注一致性通过”不等于“认知构念效度通过”。
- 外部效度需另用无 AI 标准化任务、盲评成绩/迁移任务核验；当前问答日志不能替代此项。

## 运行输入与输出清单

**输入**：选定队列的 Turn 文本与 ID、speaker/agent 初始解析、学生/Session ID、时间、AI 预标标签/概率、分层变量、抽样概率、人工双标/裁决结果、预先确定的 τ 与错误率 α。  
**输出**：可追溯的标签表（含 p 向量和状态）、抽样/成本报告、混淆矩阵、Kappa/Alpha 及区间、概率 ABL/HOT、误差传播的 CTQ/学生指标分布，以及失败/稀疏标签说明。
