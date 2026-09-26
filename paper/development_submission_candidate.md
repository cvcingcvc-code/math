# 当观测不等于证据：教育 AI 增量价值评价中的证据可靠性与拒判建模

**Development Submission Candidate**（`PAPER_FINAL_DRAFT`）

> **状态声明（贯穿全文）**：本文所有结果来自 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 输入，`formal_gate_eligible=false`，`NOT_HUMAN_VALIDATED`。Human R1/R2 尚未产生（0/70、0/70），Formal Gate `NOT_RUN`，`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。本文不报告任何正式人工一致性、正式 AIV、学生排名或因果 AI 增量。数字唯一源见 `paper/PAPER_NUMBER_LOCK.md`，声明到证据的映射见 `paper/PAPER_EVIDENCE_TRACE.md`。

---

## 1. 摘要

在教育 AI 辅助学习中，一条被观察到的学习表现（Raw Signal）并不自动等同于一条可靠证据。AI 提示引导、上下文缺失、来源冲突和标注不确定，都会让"看起来很高"的原始信号背后缺乏足够的支撑。本文提出一个显式的**证据支持评价框架**：先把"表现有多高"（Raw Signal）与"这条表现有多少可审查支撑"（Evidence Reliability）分开建模，再同时报告分数与有效证据支持（Support / Coverage），并在证据不足时**拒绝给出过度确定的结论**（`ABSTAIN` / `NO_EFFECTIVE_EVIDENCE`），而不是填入一个看似有意义的分数。

在 70 条开发记录上，框架得到一条结构性结论：归一化分数（ABL/HOT/Gap = 3.5625 / 0.375 / 1.125）在加入可靠性权重前后保持不变，而有效证据权重从 16 降到 6、有效覆盖率从 0.228571 降到 0.085714（分母为全部 70 条记录）。即：**分数稳定，不等于证据支持稳定（Score Stability ≠ Evidence Support Stability）。** 这一结论由五条相互补充的验证路径（Baseline、Ablation、Sensitivity/Robustness、Failure Case、External Transfer）共同支撑，并由 ML Challenger 与 Alternative Formulations 两个对照加固。全部结果为开发级描述性/结构性证据，不等价于因果增量或普适性结论。

---

## 2. 引言

### 2.1 Background

评价 AI 增量价值时，一个自然的起点是把观察到的结果直接映射成分数，再据此下结论。这条链路写作：

```
Observed Result  →  Score / Decision
```

它隐含了一个未经检验的假设：**观测到的结果本身已经是可靠证据。**

但在 AI 参与的学习记录里，这个假设常常不成立。一条学生发言可能同时包含学生自己的思考、AI 提示的引导、被截断的上下文、不确定的来源归属，以及标注者对"这条到底算不算证据"的犹豫。学习科学中的经典结论是即时表现与持久学习可分离（Soderstrom & Bjork, 2015），随机试验也表明 AI 辅助练习的表现提升不必然带来撤去 AI 后的独立表现提升（Bastani et al., 2025）。因此，把"观测到的表现"直接当作"可信结论"存在系统性风险。

### 2.2 Research Gap

这些因素叠加后会产生四种典型情况：

- **缺失（missing）**：找不到可判读的学生证据；
- **冲突（conflicting）**：任务层级看起来很高，但支撑它的学生证据层级很低；
- **低可信（low-trust）**：证据存在，但来源或标注置信度不足；
- **支持不完整（incomplete support）**：少数记录贡献了分数，大量记录没有有效证据。

现有学习分析测量框架（Gašević et al., 2022；Kane, 2013）强调"观测→指标→解释→用途"每一跳都要有可证伪的论证，但缺少一个把"证据支持"显式纳入评分、并允许在证据不足时拒判（abstain）的具体评价结构。选择性分类文献（El-Yaniv & Wiener, 2010）为"拒判 + coverage"提供了形式基础，但通常假设可观测的风险标签；本项目面对的是证据支持不足/冲突，而非单纯分类置信度。

### 2.3 Research Question

> 当观测证据存在缺失、冲突或可信度差异时，如何避免把 Raw Signal 直接当成可信结论，并通过 Evidence Reliability、Support/Coverage 以及 ABSTAIN 机制避免过度确定的判断？

这是一个 **measurement / identifiability（测量与可识别性）** 问题，不是预测问题，也不是因果识别问题。研究对象是 AI 辅助学习中的可观察交互与学生表现证据，而非已识别的真实能力、长期学习增益或 AI 因果效果。

### 2.4 Contributions

1. 把"观测结果 → 结论"的单步链路，显式展开为可审查的六层结构：Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision。
2. 明确区分"分数稳定"与"证据支持稳定"两个量，并在开发数据上展示二者可以分离。
3. 引入 fail-closed 的拒判语义：有效证据为零时返回 `NO_EFFECTIVE_EVIDENCE`，而不是填入 0 分。
4. 用五条互补验证路径（而非单一实验）攻击同一核心命题，并明确每条路径"证明了什么、不能证明什么"。

---

## 3. 数据与证据结构

**数据身份**：70 条开发记录，来自 `data/annotations/ai/pilot_ai_provisional.csv`，标注来源为 `AI_PROVISIONAL`、状态为 `DEVELOPMENT_ONLY`。这 70 条是正式 Pilot V1（N=140，秋 70 + 春 70）中被冻结用于当前 Gate 的核心样本；其余 70 条不属于当前 Gate 范围。上游清洗主结果 `clean_interactions.csv` 含 7028 turns（student 3522 / ai 3506）。

**证据可判读性分布**（Table 1）：

| 类别 | 数量 |
|---|---:|
| 可判读 Student Evidence（Bloom L2–L6） | 16 |
| NO_EVIDENCE（无证据） | 19 |
| UNDETERMINED（不可判定） | 35 |
| 合计 | 70 |

16 条可判读记录的构成：L2×5、L3×5、L4×1、L5×2、L6×3。19 条 NO_EVIDENCE 与 35 条 UNDETERMINED 共 54 条，其有效证据权重为零，统一返回 `NO_EFFECTIVE_EVIDENCE`。

**关键结构性事实（限制项）**：这 16 条可判读记录全部满足 `prompt_induced=true`、`context_truncated=false`、`confidence=medium`、`task_actor=ai`。也就是说，当前开发切片是**高度同质**的——所有可判读记录都携带 AI 提示诱导风险，且上下文截断与置信度维度没有变异。这一事实直接决定了：本文只能支持"公共缩放行为"层面的结构性结论，不能单独识别 prompt、context、confidence 或 actor 的独立效应（Table 1 对应 `reports/verification/independent_bounds_summary.json`）。

---

## 4. 模型

核心模型链固定为（Figure 1）：

```
Observed Evidence
  → Raw Signal
  → Evidence Reliability
  → Adjusted Evaluation
  → Support / Coverage
  → ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE
```

### 4.1 Raw Signal（原始信号）

**回答的问题**：我们观察到了什么？

Raw Signal 记录可观察到的证据等级——本文用 Student Evidence 的 Bloom 层级（冻结手册 L2–L6）表示。它只回答"这条证据有多高"，不回答"这条证据是否可信"。当记录不可判读（NO_EVIDENCE / UNDETERMINED）时，不强行为它编码一个分数。Bloom 是认知过程分类语言，不是稳定能力测量（Krathwohl, 2002）。

### 4.2 Evidence Reliability（证据可靠性）

**回答的问题**：这条证据有多少支撑依据？

对每条可判读记录，定义其可靠性权重：

```
w_i = I(observable_i) · c_i · (1 − λ_prompt · p_i) · (1 − λ_context · t_i)
```

其中：

- `I(observable_i)`：仅当 Student Evidence 可判读时为 1，否则为 0（fail-closed）；
- `c_i`：标注置信度映射（high=1.0，medium=0.75，low=0.5）；
- `p_i`：AI 提示诱导标记（prompt-induced），`λ_prompt` 为其折减系数；
- `t_i`：上下文截断标记（context-truncated），`λ_context` 为其折减系数。

`w_i` 是**声明性的支持权重**，不是校准过的概率，也不是因果系数。置信度权重（`c_i`）在当前数据上也不具备概率含义（cf. Guo et al., 2017：confidence ≠ 校准概率）。这些系数是当前开发假设下的可审查参数，其合理性待 Human Gate 与后续本地效度验证。

### 4.3 Adjusted Evaluation（校正评价）

**回答的问题**：弱支持如何影响评价？

```
Adjusted_i = Raw_i × w_i
```

相同的 Raw Signal，在不同 Reliability 下，其可接受程度应当不同。一条高 Raw 但低支持的记录，不应被当成与高 Raw 且高支持的记录等价。注意：`Adjusted Score` 不等于 `Reliable AI Increment`——后者需要当前项目尚未具备的 `Outcome_AI − Outcome_baseline` 配对。

### 4.4 Support / Coverage（支持度与覆盖率）

**回答的问题**：还有多少有效支撑？

```
S = Σ_i w_i           （有效证据权重之和）
C_eff = S / N         （有效覆盖率，分母为全部 N 条记录）
```

本文统一以 N=70（全部开发记录，含无证据与不可判读记录）为分母，并在每次出现覆盖率时写明分母。Support 与 Coverage 是独立于分数的两个量，必须分开报告（`docs/metric_dictionary.md`）。

### 4.5 Decision and Abstention（决策与拒判）

模型输出三种状态：

- `ACCEPT`：分数有定义且满足支持规则；
- `ABSTAIN` / `LOW_SUPPORT`：证据不足、冲突或支持较弱，暂缓判断；
- `NO_EFFECTIVE_EVIDENCE`：有效证据为零，不填 0 分，而是明确报告"无可评价证据"。

当证据不足时，`ABSTAIN` 或 `NO_EFFECTIVE_EVIDENCE` 本身是合理的模型输出——它不是"模型失败"，而是在防止过度结论（overclaim）。拒判必须与 coverage 同时报告，不能宣传为"靠过滤提升准确率"。

---

## 5. 验证设计

本文不依赖任何单一实验结果，而是用五条路径从不同方向攻击同一个核心命题（Table 2）：

> 如果 Raw Signal 与证据支持被混为一谈，系统会在弱证据、缺失证据或不同信息质量下给出过度确定的评价；可靠性层能把这条差异显式化，并允许拒判。

| Validation | Question | Setup | Main Result | Supported Claim | Not Supported |
|---|---|---|---|---|---|
| Baseline Comparison | 可靠性层是否必要 | Raw-only / 线性 / 规则 vs 主模型，同 70 条 | 四模型 ABL 均 3.5625；Raw-only support=16，主模型=6 | 可靠性层带来 Raw-only 没有的 graded support | 乘法形式必需；精度/预测优越 |
| Ablation | 组件是否只是装饰 | M0→M3 逐项加 confidence/prompt/context | 有效权重 16→12→6→6，分数恒 3.5625 | 组件改变 support accounting | 模块差异=独立因果效应；context 已证无作用 |
| Sensitivity/Robustness | 是否单点偶然 | λ_prompt/λ_context/r_medium ±10%/±20% | 0 decision-state flips；分数稳定，support 变化 | 局部结构稳定性 | 统计置信区间；全局稳健性 |
| Failure Case | 高 Raw 是否仍被接受 | P108/P105/P072/P035 | P108 L6→R=0.375→LOW_SUPPORT；P072/P035 NEE | High Raw ≠ High Support | 准确率/真实错误率 |
| External Transfer | 是否只为教育数据硬写 | BTC n=1698 复用同一结构 | Gate1/Gate2 SUPPORTED，Gate3 NOT SUPPORTED | 结构可迁移 | 教育泛化 / 交易优势 |

此外，ML Challenger 与 Alternative Formulations 作为**补充对照**（第 7 节），回答"为什么主模型被保留"。

---

## 6. 结果

### 6.1 Baseline Comparison（基线对比）

**WHY**：检验"如果完全忽略 Reliability，会发生什么"。

**SETUP**：Raw-only 基线（M0，不做任何校正）、Simple Linear、Rule-based 与主模型（M3）在相同的 70 条记录上运行，比较归一化分数与证据支持（Table 3）。

| Model | Aggregate Score | Support Mass | Coverage (N=70) | Decision Semantics | Role |
|---|---:|---:|---:|---|---|
| Raw-only | 3.5625 | 16.0 | 0.228571 | 16 SUPPORTED / 0 LOW / 54 NEE | 必要 baseline |
| Simple Linear | 3.5625 | 8.0 | 0.114286 | 0 SUPPORTED / 16 LOW / 54 NEE | 更简单加法对照 |
| Rule-based (gated) | 3.5625 | 16.0（raw mass） | 0.228571 | 0 SUPPORTED / 16 LOW / 54 NEE | 拒判安全对照 |
| **Current Model** | 3.5625 | 6.0 | 0.085714 | 0 SUPPORTED / 16 LOW / 54 NEE | 主模型 |

**RESULT**：四种模型的归一化分数完全相同（3.5625），但 Raw-only 把 16 条可判读记录全部按满权重计入（support mass 16），主模型把它们标为 `LOW_SUPPORT` 并把有效权重记为 6，线性为 8。

**INTERPRETATION**：**所有 aggregate score 相同本身是研究结果**，不能隐藏。分数相同来自当前可判读记录的高度同质公共缩放结构——16 条记录共享 prompt=true、context=false、medium，各加权方案对每条被纳入的分数施加同一常数因子，归一化后抵消。这既不是精度等价，也不是任何公式有效的证据。Raw-only 缺少区分"证据等级"与"证据质量"的通道（graded support semantics），因此它是必要 baseline，而非完整模型。**不要把 Raw-only 写成"错误"。**

### 6.2 Ablation（消融）

**WHY**：检验模型中哪些组成部分真正改变了支持记账与决策语义。

**SETUP**：从 M0 到 M3 逐步加入组件（Table 4）：

| Model | Components | Score (ABL/HOT/Gap) | Effective Weight | Coverage (N=70) | Interpretation |
|---|---|---|---:|---:|---:|---|
| M0 | 无校正 | 3.5625 / 0.375 / 1.125 | 16.0 | 0.228571 | 全权重 |
| M1 | + confidence | 3.5625 / 0.375 / 1.125 | 12.0 | 0.171429 | 置信度折减 |
| M2 | + confidence + prompt | 3.5625 / 0.375 / 1.125 | 6.0 | 0.085714 | prompt 主导下降 |
| M3 | + confidence + prompt + context | 3.5625 / 0.375 / 1.125 | 6.0 | 0.085714 | context 无变异 |

**RESULT**：有效权重 16→12→6→6；归一化分数始终保持 3.5625 / 0.375 / 1.125 不变。prompt 模块承担了当前切片的主要支持下降（M1→M2）；context 模块在当前可判读记录中没有变异，因此 M2 与 M3 相同。

**INTERPRETATION**：重点应放在 **16→12→6→6**，而不是只看 3.5625 恒等。消融证明这些组件确实改变 support accounting 与拒判边界，而不是只出现在公式里。

**LIMIT**：不能把模块差异解释成独立因果效应；context 的作用在当前切片不可识别（数据缺变异）。

### 6.3 Sensitivity / Robustness（敏感性/稳健性）

**WHY**：检验结论是否只是某个参数点的偶然结果。

**SETUP**：在默认参数 `λ_prompt=0.50、λ_context=0.50、r_medium=0.75` 上，对三个参数分别做 ±10%、±20% 的单变量扰动（共 15 个条件），并在 693 个参数网格（21×11×3）上复算边界。

**RESULT**：15 个扰动条件产生 **0 个 decision-state 翻转**；归一化分数保持 3.5625，而 support 随参数变化。693 个网格中 660 个 defined、33 个 undefined；有效权重跨 0.4–16.0，有效覆盖率跨 0.005714–0.228571。学生级 ranking 为 `NOT_APPLICABLE`。

**INTERPRETATION**：Figure 4 直接展示这一对比——Score 在网格内几乎不变，而 Effective Support / Coverage 明显变化。这回答了一个关键质疑：主现象不是单一参数点碰巧产生的。分数稳定、支持变化是局部结构现象。

**LIMIT**：这是有限声明网格，不是统计置信区间，也不是全局稳健性；context 平坦是数据缺变异，不是已证明"无作用"。

### 6.4 Counterexamples / Failure Cases（反例/失败案例）

**WHY**：检验模型在最困难记录上的行为，回答"高 Raw 是否仍应被接受"。

**SETUP**：选取具有代表性的边界案例（Table 5，Figure 2 / Figure 5）：

| 记录 | Raw Evidence | Reliability | Adjusted 贡献 | 决策 |
|---|---|---:|---:|---|
| P108 | L6（最高） | 0.375 | 2.25 | LOW_SUPPORT / ABSTAIN |
| P105 | L2 | 0.375 | 0.75 | LOW_SUPPORT |
| P072 | 不可判读 | 0 | — | NO_EFFECTIVE_EVIDENCE |
| P035 | 不可判读 | 0 | — | NO_EFFECTIVE_EVIDENCE |

**RESULT**：P108 的 Raw 达到最高层级 L6，但因为携带 prompt 诱导风险，可靠性只有 0.375，被降为 `LOW_SUPPORT` 而非满额接受；P072、P035 因证据不可判读而返回 `NO_EFFECTIVE_EVIDENCE`，模型拒绝为其编造分数。

**INTERPRETATION**：这组案例直接展示两个语义：**High Raw ≠ High Evidence Support**，以及 **Missing Evidence ≠ Score 0**。

**LIMIT**：这是结构性案例，不是准确率或真实错误率；没有独立 true outcome，无法检验 abstain 之后是否"正确"，不能写成"模型预测正确"。

### 6.5 External Transfer Validation（外部迁移验证）

**WHY**：检验模型是否只是为当前教育数据硬写，回答接口能否迁移到不同性质的 Raw Signal。

**SETUP**：把 `Raw → Reliability → Adjusted → ACCEPT/ABSTAIN` 结构复用到一份 BTC 历史纸面模拟（1698 条样本）的三个固定策略信号（动量、RSI 均值回归、MA20/50 趋势）上，并做三个 information-missing Gate（Table 6，Figure 6）。

| Gate | 判据 | 结果 |
|---|---|---|
| Gate1 | 信息质量下降 → Reliability 下降 | SUPPORTED（0.603 → 0.408） |
| Gate2 | 低 Reliability → coverage 下降 / abstention 上升 | SUPPORTED（coverage 0.394 → 0.001） |
| Gate3 | 低 Reliability → 更低 future error | NOT SUPPORTED（0.525 vs 0.528，无改善） |

**RESULT**：三个策略中前两个（A/B）表现出有限的可靠性分离，第三个（C）是失败边界；缺失、延迟、冲突和低可信条件会降低 coverage 并增加 abstention。**Gate3 的负结果必须保留**：低可靠性并没有带来更低的未来错误率，risk-coverage improvement = false。

**INTERPRETATION**：同一接口能在性质不同的 Raw Signal 上运行，说明 **structural portability（结构可迁移）**，但这**不是** profitable trading、prediction superiority 或 universal generalization 的证据（no trading advantage claim）。

**LIMIT**：这是 `DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`，synthetic/controlled 性质。它不能成为论文第二主线，只能作为结构迁移演示。

---

## 7. Challenger Analysis

### 7.1 ML Challenger（机器学习挑战者）

**WHY**：回答"更灵活的数据驱动模型是否足以替代当前可解释框架"——目标不是找冠军。

**SETUP**：以"是否获得可判读 Evidence"为代理目标，测试逻辑回归、深度 2 决策树与探索性随机森林（正样本仅 16 条，重复 4 折交叉验证 × 25 次 = 100 折），并施加特征缺失与跨学期迁移压力测试（Table 8）。

| Model | Accuracy | Balanced Accuracy | F1 |
|---|---:|---:|---:|
| Logistic Regression | 0.876 | 0.863 | 0.758 |
| Shallow Decision Tree | 0.919 | 0.901 | 0.815 |
| Random Forest (exploratory) | 0.922 | 0.894 | 0.823 |

**RESULT**：表面 CV 判别指标不低，但：特征缺失 20%/40% 后准确率降到约 0.71–0.81；随机森林跨学期迁移不稳定（2026春→2025秋 准确率 0.588）。

**INTERPRETATION**：ML 是有价值的 Challenger，但结论为 **`INSUFFICIENT_FOR_STRONG_ML_CLAIM`**、`NO_SINGLE_DOMINANT_MODEL`。原因不是"ML 不好"，而是当前证据边界下：positive = 16（AI provisional 代理标签）、无独立 holdout、缺失降级、跨学期不稳，且 ML 的预测目标（Evidence 可读性）与主模型的证据变换问题（拿到标签后的支持变换 + fail-closed 拒判）不是同一件事。

**LIMIT**：交叉验证不是独立证据；本文**不声称** handcrafted 模型优于 ML，也**不声称** ML 胜出——二者都没有被证明"更优"。

### 7.2 Alternative Formulations（替代公式）

**WHY**：检验当前结论是否只依赖某一个具体公式，回答"换个函数形式，主现象是否仍在"。

**SETUP**：比较四种函数形式的支持衰减行为（Table 7）：

| Model | Formula | 新增参数 | R→0 行为 | Sample-in 观察 |
|---|---|---|---|---|
| A 乘法 | `S_raw × R` | 无 | `S_adj→0` | mean 1.336；rank stability 1.0 |
| B 加法 | `S_raw − λ(1−R)` | λ∈{0.5,1.0} | 保留 `S_raw−λ` | RMSE vs Raw = 0.3125（λ=0.5，最小） |
| C 门控 | `R<τ ⇒ ABSTAIN` | τ=0.5 | ABSTAIN | 16 条全部 ABSTAIN（defined_n=0） |
| D 非线性 | `S_raw × R^γ` | γ∈{0.5,1.0,2.0} | `S_adj→0` | 衰减曲率随 γ 变化 |

**RESULT**：B 可以更接近 Raw（RMSE 最小 0.3125）；C 拒判更激进（16 条全部 ABSTAIN）；D 引入额外 nonlinear sensitivity。A（乘法）的优势主要是：解释简单、R→0 行为清晰、missing-evidence 语义清楚、容易审计。

**INTERPRETATION**：**不要选冠军。** 结论是 `NO_SINGLE_DOMINANT_MODEL`——没有任何公式在拟合、安全、覆盖、可解释、迁移、复杂度上全面胜出。因此 Alternative Formulations 作为 **structural robustness check**，检验主结论不依赖单一公式。主模型被保留的理由是研究问题对齐 + 透明性 + 显式缺失证据语义 + 拒判结构，不是"已证明最优"。

---

## 8. 讨论：为什么保留当前主模型

主模型被保留，**不是因为"它最好"**，而是因为它是 **problem-alignment decision**，不是 **prediction-winner decision**。具体理由（每一条对应上述真实结构与实验）：

1. **transparency（透明性）**：评委能看到 Raw → Reliability → Adjusted → Support → Decision 每一步为什么发生，而不是一个黑盒分数。
2. **auditability（可审计性）**：每个最终决策都能追溯到输入证据与可靠性权重。
3. **explicit evidence support**：显式记账"这条证据有多少支撑"，而不是把所有 observation 当成等价信息。
4. **missing-evidence semantics**：明确区分"没有证据"（`NO_EFFECTIVE_EVIDENCE`）与"有证据但结果较弱"（`LOW_SUPPORT`）。
5. **abstention semantics**：允许模型在证据不够时拒绝过度判断。
6. **research-question alignment**：研究问题问的是"如何避免把 Raw 当结论"，主模型的结构直接回答这个问题。

Raw-only 结构简单，但不能显式表达 evidence quality、conflict、support、abstention，因此它是必要 baseline，而非完整模型。ML challenger 与替代公式分别回答"数据驱动模型是否更有说服力"与"结论是否依赖单一公式"，它们被保留为对照，而不是替代。

**核心发现**：分数稳定，不等于支撑该分数的证据同样稳定、充分或可信。这一现象在 Baseline（四模型同分但支持不同）、Ablation（16→12→6→6）、Sensitivity（693 网格分数不变而支持 0.4–16）三条路径上都被反复观察到。

---

## 9. 局限性

以下限制是当前证据边界的组成部分，不能压缩成一句话：

1. **输入是 AI provisional 标签**：所有结果来自 `AI_PROVISIONAL / DEVELOPMENT_ONLY`，不能替代人工验证。
2. **Human R1/R2 未完成**：R1=0/70、R2=0/70，Formal Gate `NOT_RUN`。最近收到的一份标注文件已核验为同一 B 标签的派生副本（filled_from_B），它**不是**独立 R1/R2，不能作为 test-retest 或 inter-rater 证据。
3. **Formal Gate NOT_RUN**：正式可靠性系数、正式支持指标、Formal AIV 均未产生。
4. **无 Outcome_AI / Outcome_baseline**：`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，不支持 causal learning gain。
5. **可判读切片高度同质**：16 条可判读记录全部 `prompt=true、context=false、confidence=medium、task_actor=ai`，prompt/context/confidence/actor 的独立效应不可识别。
6. **context 无变异**：`λ_context` 的作用在当前切片不可识别，只能作 sensitivity-only 情景。
7. **reliability 参数未被正式校准**：`c_i`、`λ_prompt`、`λ_context`、`r_medium` 是假设/敏感性参数，不是校准概率。
8. **无 true outcome**：无法验证 abstain 后是否正确，不能报告准确率提升。
9. **finance 仅 structural transfer**：金融案例是 synthetic/controlled 结构演示，不是教育泛化或交易优势证据（no trading advantage claim）。
10. **ML strong claim unsupported**：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`。
11. **no single dominant formulation**：`NO_SINGLE_DOMINANT_MODEL`，不能选出"最佳"公式。
12. **复现边界**：`run_all.py` 32/32 覆盖开发版核心链路，不覆盖 final artifact / figure / Paper / Demo 的全链路生成。

---

## 10. 结论

在存在缺失、冲突或低可信证据的系统中，应当把 observed score 与 evidence reliability/support **分开建模**，并在证据不足时允许 abstention。

在当前 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录和声明的参数范围内，Evidence Reliability 框架能够显式区分 Raw Performance 与 Evidence Support：归一化分数（ABL/HOT/Gap = 3.5625 / 0.375 / 1.125）保持稳定，而有效证据权重从 16 降到 6、有效覆盖率从 0.228571 降到 0.085714；当 support = 0 时返回 `NO_EFFECTIVE_EVIDENCE`，而不是伪造零分。

因此，核心结论可以表述为：**Score Stability ≠ Evidence Support Stability**——分数稳定，不等于证据支持稳定。用自然语言说：**稳定的评分不意味着支撑该评分的证据同样稳定、充分或可信。** 在缺失、冲突或低可信证据环境下，score 和 evidence support 应分开报告，证据不足时系统应允许 abstention。

这是当前 development slice 的描述性、结构性结论。它不升级为 universal theorem，不声称任何模型最优、任何预测准确率提升、任何因果 AI 增量或跨域普适性。正式结论须等待 Human Gate 完成（`PENDING HUMAN-ANNOTATION INTAKE VERIFICATION`）。

---

## 附录 A：图表清单

| 图 | QUESTION ANSWERED | DATA SOURCE | CLAIM SUPPORTED |
|---|---|---|---|
| Figure 1 | 模型各层如何衔接 | `final_model_overview.md` | C1（Raw 与 Reliability 分层） |
| Figure 2 | Raw 与 Adjusted 如何分离 | `raw_adjusted_metrics.csv` | C2、C9 |
| Figure 3 | 证据降级如何影响 | `evidence_perturbation_cases.csv` | C5 |
| Figure 4 | Score 稳定 vs Support 变化 | `parameter_perturbation.csv`、693 网格 | C3、C5、C8 |
| Figure 5 | Ablation 拒判语义 | `ablation_results.csv` | C4、C7 |
| Figure 6 | 教育结构 → 金融结构迁移 | `transfer_validation.json` | C10 |

## 附录 B：锁定文件索引

- 声明→证据→数字→表/图映射：`paper/PAPER_EVIDENCE_TRACE.md`
- 唯一数字源与冲突处理：`paper/PAPER_NUMBER_LOCK.md`
- 文献引用映射：`paper/LITERATURE_CITATION_MAP.md`
