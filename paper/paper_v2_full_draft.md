# 当观测不等于证据：面向教育 AI 增量价值评价的证据可靠性与拒判框架

**PAPER_V2_CANONICAL_DEVELOPMENT**（完整论文正文 · Full Draft）

> **状态声明（贯穿全文，不可省略）**
> 本文全部结果来自 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 输入，`formal_gate_eligible = false`，`NOT_HUMAN_VALIDATED`。
> Human R1 = 0/70 VALID，R2 = 0/70，Formal Gate = `NOT_RUN`，`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。
> 本文不报告任何正式人工一致性系数、正式 AIV、学生排名或因果 AI 增量。
> 数字唯一源：`paper/PAPER_NUMBER_LOCK.md` + `outputs/final_results.json`；声明到证据的映射：`paper/PAPER_EVIDENCE_TRACE.md`；文献映射与缺口：`paper/LITERATURE_CITATION_MAP.md`。
> **晋升状态**：`PAPER_V2_CANONICAL_DEVELOPMENT`。因 Formal Human Gate 仍未完成，本文**不**标 `FORMAL_FINAL`。

---

## Abstract

评价 AI 辅助学习时，最常见的一步是把"观察到的表现"直接映射成一个分数并据此下结论：`Observed Result → Score / Decision`。这一步隐含了一个未经检验的假设——**观测到的结果本身已经是可靠证据**。学习科学与测量文献都指出这一假设可能不成立：即时表现与持久学习可以分离，AI 辅助练习的表现提升不必然带来撤去 AI 后的独立表现提升，而学习分析日志指标必须经过效度论证才能进入解释与用途。

本文把这一问题明确定位为一个 **measurement / identifiability（测量与可识别性）问题**，而非预测问题或因果识别问题，并提出一个可审查的**证据感知评价框架（Evidence-Aware Evaluation Framework）**：把"表现有多高"（Raw Signal）与"这条表现有多少可审查支撑"（Evidence Reliability）分开建模，同时报告分数与有效证据支持（Support / Coverage），并在证据不足时输出 `ABSTAIN` 或 `NO_EFFECTIVE_EVIDENCE`，而不是填入一个看似有意义的分数。

本文用五类互补验证共同攻击同一个结构性命题——基线对比、消融、局部参数敏感性、失败案例、外部结构迁移，并由机器学习挑战者与替代函数形式两类对照加固。在当前 70 条开发记录上，框架得到一条**描述性、结构性**结论：归一化分数在引入可靠性权重前后保持不变，而有效证据权重与覆盖率显著下降。即：

> **Score Stability ≠ Evidence Support Stability（分数稳定，不等于证据支持稳定）。**

这一结论受当前 development slice 的强边界约束：70 条记录中仅 16 条具有可判读证据，且这 16 条高度同质，prompt / context / confidence / actor 的独立效应无法被充分识别；正式人工验证（Human R1/R2）尚未完成，因果 AI 增量不可识别。本文结论限于开发级证据边界，并给出可执行的 Formal Evidence Upgrade Protocol。

**Keywords**: evidence reliability；selective prediction / abstention；measurement validity；missing evidence；support and coverage；learning analytics；AI-assisted learning evaluation；sensitivity analysis

---

## 1. Introduction

### 1.1 一个看似无害的链路

评价"AI 是否带来了增量价值"，最自然的起点是把观察到的结果映射成分数：

```
Observed Result  →  Score / Decision
```

这条链路简短、可计算、易汇报，但它默认了一件事：**观测到的结果本身已经是可靠证据。** 在 AI 参与的学习记录里，这个默认常常不成立。一条学生发言可能同时包含学生自己的思考、AI 提示的引导、被截断的上下文、不确定的来源归属，以及标注者对"这条到底算不算证据"的犹豫。这些因素不会让记录消失——它们会让记录**看起来仍然可用**，甚至看起来层级很高。

由此产生三类现实问题：

- **缺失证据（Missing Evidence）**：找不到可判读的学生证据，但记录本身存在；
- **冲突证据（Conflicting Evidence）**：任务层级看起来很高，但支撑它的学生证据层级很低；
- **低可信证据（Low-Trust Evidence）**：证据存在，但来源归属、上下文完整性或标注置信度不足。

这三类问题共享同一个后果：**Observed Result ≠ Reliable Evidence。** 把"观测到的表现"直接当作"可信结论"，存在系统性风险。学习科学指出即时表现与持久学习可分离（Soderstrom & Bjork, 2015）；现场随机试验表明 AI 辅助练习的表现提升不必然带来撤去 AI 后的独立测试提升（Bastani et al., 2025）；测量效度理论要求"观测 → 指标 → 解释 → 用途"每一跳都有可证伪的论证（Kane, 2013；Gašević et al., 2022）。

### 1.2 Main Research Question

本文的全文唯一正式研究问题为：

> **当观测证据存在缺失、冲突或可信度差异时，如何避免直接把 Raw Signal 当成可信结论，并构建一个能够显式报告 Evidence Reliability 与 Support / Coverage，且在证据不足时允许 ABSTAIN 的可审查评价框架？**

这是一个 **measurement / identifiability** 问题。它**不是**：AI 是否提高成绩；学生真实能力预测；AI causal learning gain；AI 与 baseline 的正式效果识别。上述问题都需要当前项目不具备的条件（合法配对的 `Outcome_AI` / `Outcome_baseline`、独立学习 outcome、正式人工标注），当前状态为 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。

### 1.3 Contributions

1. **Evidence-aware evaluation framework**：把 `Observed Result → Score` 的单步链路显式展开为可审查的六层结构——`Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support / Coverage → Decision`。
2. **Reliability 与 Score 显式分离**：明确区分"分数稳定"与"证据支持稳定"两个量，并在真实开发数据上展示二者可以分离。
3. **Support / Coverage 与 ABSTAIN 机制**：引入 fail-closed 的拒判语义——有效证据为零时返回 `NO_EFFECTIVE_EVIDENCE`，而不是填入 0 分；并明确 `NO_EFFECTIVE_EVIDENCE ≠ 0 分`、`Missing Evidence ≠ Zero Performance`。
4. **五类验证共同攻击同一命题**：基线对比、消融、敏感性、失败案例、外部结构迁移五条路径共同验证同一条结构性命题，并对每条路径明确写出"支持什么、不支持什么"，包括必须保留的负结果。
5. **External Structural Transfer**：把同一结构复用到性质完全不同的证据环境，检验框架是否能够跨场景迁移（仅结构迁移，不声称泛化或交易优势）。

本文**不声称**证明了 AI 提高学习效果，也不声称任何模型最优、任何预测准确率提升或任何因果增量。

---

## 2. Problem Formulation

### 2.1 传统形式及其语义承诺

传统评价把问题写成一个映射：

```
Score_i = f(x_i)
```

其中 `x_i` 是第 i 条记录的可观察特征。这个形式在数学上没有错误，问题在于它的**语义承诺**：它假设 `f` 的输出可以直接被解释为"该记录所代表表现的可信度量"。一旦证据质量存在差异，这一承诺就失效了。考虑两条 Raw Observation 完全相同（都是 Student Evidence L6）的记录：一条上下文完整、来源明确、非 AI 提示诱导、标注高置信；另一条 AI 提示诱导、标注中等置信（这正是本文失败案例 P108 的情形）。在 `Score_i = f(x_i)` 下，二者自动拥有相同的解释强度，但它们的可审查支撑显然不同。缺失的是一个**独立的维度**。

### 2.2 核心定义

本文对下列概念作出严格区分：

| 概念 | 含义 | 关键边界 |
|---|---|---|
| **Observation** | 系统实际观察到的交互记录 | 记录存在 ≠ 记录可判读 |
| **Raw Signal** | 可观察到的表现层级（Student Evidence 的 Bloom L2–L6） | 只回答"表现有多高"，不回答"是否可信" |
| **Evidence** | 可判读、可进入评价的学生证据 | 不可判读时**无定义**（null），不取 0 |
| **Reliability** | 该条证据的可审查支持权重 `w_i` | 声明性支持权重，**不是**校准概率、不是因果系数 |
| **Adjusted Score** | `Raw_i × w_i` | 证据加权的描述性分数，不是 AI 增量 |
| **Support** | `S = Σ w_i` | 有效证据权重之和，独立于分数报告 |
| **Coverage** | `C_eff = S / N` | 有效覆盖率，分母为全部 N 条记录 |
| **Decision** | `ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE` | 决策状态，不是预测结果 |
| **ABSTAIN** | 证据不足时暂缓判断 | 是模型的合理输出，不是模型失败 |
| **NO_EFFECTIVE_EVIDENCE** | 有效证据为零 | 是"无可评价证据"，**不是 0 分** |

### 2.3 为什么 Raw 与 Reliability 必须拆开

核心论证在于：**高 Raw 不代表高 Evidence Support。** 一条 Raw 层级很高但缺乏支撑的记录，不应被当成与"高 Raw 且高支撑"的记录等价。Raw Signal 回答"这条证据有多高"，Reliability 回答"这条证据有多少可审查支撑"——这是两个不同的量。若把二者混为一谈，系统会在弱证据、缺失证据或不同信息质量下给出过度确定的评价。

### 2.4 问题边界声明

本文解决的是 **measurement / evidence reliability / identifiability** 问题，**不是 causal inference**。要讨论 AI 因果增量，需要合法配对的 `Outcome_AI` 与 `Outcome_baseline`，当前项目不具备这一条件（Hernán & Robins, 2022 的 target-trial 逻辑：缺少 baseline pairing、独立 outcome 与分配机制时，只能保持描述性/条件关联）。因此本文的 `Adjusted Score` 是证据加权的描述性分数，不是 `Reliable AI Increment`，二者不可互换。

---

## 3. Evidence-Aware Evaluation Model

本章是全文数学核心。模型链固定为：

```
Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation
→ Support / Coverage → ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE
```

[FIGURE F1 HERE]

Figure 1. Overall evidence-aware evaluation framework: Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision. 不可判读 Evidence 直接返回 NO_EFFECTIVE_EVIDENCE；AI Increment 分支标为 NOT_SUPPORTED。Raw 与 Reliability 是两个独立层，这是全文结论的结构前提。

### 3.1 Raw Signal

Raw Signal 记录可观察到的证据等级，本文用 Student Evidence 的 Bloom 层级（冻结手册 L2–L6）表示。当前 16 条可判读记录的构成为 L2×5、L3×5、L4×1、L5×2、L6×3。

**语义边界**：Raw Signal 只回答"这条证据有多高"，不回答"这条证据是否可信"。它是描述性证据等级，**不是** AI 增量、不是可靠性、不是真实能力、不是校准概率。Bloom 是认知过程分类语言，不是稳定能力测量（Krathwohl, 2002）。当记录不可判读（`NO_EVIDENCE` / `UNDETERMINED`）时，**不强行为它编码一个分数**。

[FIGURE F2 HERE]

Figure 2. Raw vs Reliability / Adjusted：P108（L6，R = 0.375，贡献 2.25）与 P105（L2，R = 0.375，贡献 0.75）是逐记录贡献；面板保留 N = 70、16 条可判读、54 条 NO_EFFECTIVE_EVIDENCE；无定义记录不被画成零。分数与支持是两个轴；undefined ≠ 0。

### 3.2 Evidence Reliability

对每条可判读记录，定义其可靠性权重：

```
w_i = I(observable_i) · c_i · (1 − λ_prompt · p_i) · (1 − λ_context · t_i)
```

其中各项含义如下：

- `I(observable_i)`：仅当 Student Evidence 可判读时为 1，否则为 0（**fail-closed** 结构规则）；
- `c_i`：标注置信度映射（high = 1.0，medium = 0.75，low = 0.5）；
- `p_i`：AI 提示诱导标记（prompt-induced），`λ_prompt` 为其折减系数；
- `t_i`：上下文截断标记（context-truncated），`λ_context` 为其折减系数。

可靠性由 evidence attributes 进入模型：prompt 风险、context 截断、confidence 置信度，以及可判读性本身（actor / evidence type 的差异通过 `I(observable_i)` 与 `c_i` 间接进入）。这条公式回答了"这条信号有多少支撑依据"。

**语义边界（三条，必须同时成立）**：

1. **`w_i` 不是概率。** 它没有在独立校准集上验证过，不满足任何频率解释（Guo et al., 2017：confidence ≠ 校准概率）。当前 `c_i` 是**假设支持分**。
2. **`w_i` 不是因果系数。** 它不表示"prompt 导致表现下降多少"。
3. **参数不是通过样本学习得到的最优值。** `λ_prompt = 0.5`、`λ_context = 0.5`、`r_medium = 0.75` 是**冻结的声明参数**（transparent / preregistered design assumptions），其合理性通过敏感性分析检验，正式校准留待 Human Gate 与本地效度验证。`PAPER_EVIDENCE_TRACE.md` 将 `λ_prompt / λ_context / r_medium` 标为 **`WEAKLY_JUSTIFIED_COMPONENT`**——本文不假装这些系数已经完成正式人工校准。

### 3.3 Adjusted Evaluation

```
Adjusted_i = Raw_i × w_i        （仅在 I(observable_i) = 1 时有定义）
```

相同的 Raw Signal，在不同 Reliability 下，其可接受程度应当不同。一条高 Raw 但低支持的记录，不应被当成与高 Raw 且高支持的记录等价。乘法结构的设计动机是：**低 Evidence Quality 不应被高 Raw Signal 自动抵消**——当 `R → 0` 时 `Adjusted → 0`，无论 Raw 多高。**必须说明**：本文不声称乘法结构是唯一正确或最优结构（见第 7 章替代公式，审计结论 `NO_SINGLE_DOMINANT_MODEL`）。

聚合分数（当 `S > 0`）：

```
Score_adj = Σ_i w_i · Raw_i / Σ_i w_i
```

### 3.4 Support / Coverage

```
S     = Σ_i w_i                 （有效证据权重之和）
C_eff = Σ_i w_i / N             （有效覆盖率，分母 N = 70，含无证据与不可判读记录）
```

只报告一个 score 是不够的。Support 与 Coverage 是**独立于分数**的两个量，必须分开报告（`docs/metric_dictionary.md`）。二者也不同：support 是权重之和，coverage 是权重（或计数）除以全部输入记录。本文统一以 N = 70（全部开发记录）为分母，并在每次出现覆盖率时写明分母；把分母悄悄换成 16 是最常见的误导手法，本文禁止。

### 3.5 Decision Layer

模型输出三种状态：

| 状态 | 触发条件 | 语义 | 不是什么 |
|---|---|---|---|
| `ACCEPT` | 分数有定义且满足声明的支持规则 | 可作判断 | 不是"预测正确" |
| `ABSTAIN` / `LOW_SUPPORT` | 证据不足、冲突或支持较弱 | 暂缓判断 | 不是模型失败，不是准确率提升 |
| `NO_EFFECTIVE_EVIDENCE` | `Σw_i = 0` | 无可评价证据 | **不是 0 分**，不是"预测错误" |

**ABSTAIN 不是模型失败**，它是模型显式表达"不足以形成可靠判断"。当证据不足时，`ABSTAIN` / `NO_EFFECTIVE_EVIDENCE` 本身是合理的模型输出——它在防止过度结论（overclaim）。纪律要求（来自 El-Yaniv & Wiener, 2010 的 risk–coverage 框架）：拒判必须与 coverage 同时报告，不得宣传为"靠过滤提升准确率"。

---

## 4. Data and Development Slice

本章真实呈现当前数据状态，不模糊任何证据不足记录。

### 4.1 数据来源

| 层级 | 事实 | 来源 |
|---|---|---|
| 正式 Pilot V1 全量 | **N = 140**（秋 70 + 春 70） | `data/processed/pilot_sample.csv` |
| 上游清洗主结果 | **7028 turns**（student 3522 / AI 3506） | `data/processed/clean_interactions.csv` |
| 当前 development slice | **N = 70**，标注来源 `AI_PROVISIONAL`，状态 `DEVELOPMENT_ONLY` | `data/annotations/ai/pilot_ai_provisional.csv` |

这 70 条是正式 Pilot V1 中被冻结用于当前 Gate 的核心样本；其余 70 条不属于当前 Gate 范围，且未标注。本文**不**把 70 外推为 140，也不把 70 条描述为总体代表。

### 4.2 证据可判读性分布

独立复算（`reports/verification/independent_bounds_summary.json::raw_recount`，`independent_implementation = true`）给出：

**Table 1　证据可判读性分布（分母 N = 70）**

| 类别 | 数量 | 说明 |
|---|---:|---|
| 可判读 Student Evidence（Bloom L2–L6） | **16** | L2×5、L3×5、L4×1、L5×2、L6×3 |
| `NO_EVIDENCE` | **19** | 找不到可判读的学生证据 |
| `UNDETERMINED` | **35** | 存在材料但不可判定 |
| 合计 | **70** | — |
| ⇒ `NO_EFFECTIVE_EVIDENCE` | **54** | = 19 + 35，有效证据权重为零 |

### 4.3 「54」不等于「54 个零分」

这是本文最需要被听清的一点：54 条记录**不是** 54 个表现为零的学生，而是 54 条**没有足够证据进入有效评价**的记录。把它们编码为 0 分，等于用"没有证据"伪造"表现为零"。因此模型的 fail-closed 规则是：当 `Σw_i = 0` 时返回 `NO_EFFECTIVE_EVIDENCE`，**不填 0**（`outputs/final_results.json` 中 54 条的 `raw_score = null`、`adjusted_score = null`）。这一语义有明确的缺失数据文献依据（Little & Rubin, 2019；Rubin, 1976：缺失机制决定可识别性，缺失不等于零值）。

### 4.4 可识别性限制：16 条可判读记录高度同质

独立复算同时给出（`independent_bounds_summary.json::raw_recount`）：

**Table 2　全样本 vs 可判读子样本的因子分布**

| 因子 | 全部 70 条 | 16 条可判读 |
|---|---|---|
| `prompt_induced` | true 53 / false 17 | **true 16 / false 0** |
| `context_truncated` | true 28 / false 42 | **true 0 / false 16** |
| `confidence` | low 51 / medium 19 | **medium 16（无 high、无 low）** |
| `task_actor` | ai 53 / student 11 / unknown 6 | **ai 16** |

**这直接意味着**：`prompt`、`context`、`confidence`、`actor` 四个因子的**独立效应目前不能被充分识别**。所有可判读记录共享同一组因子取值，因此每条可判读记录的可靠性权重都等于同一个常数 `R = 0.75 × (1 − 0.5 × 1) × (1 − 0.5 × 0) = 0.375`；任何加权方案对每条被纳入的分数施加同一常数因子，归一化后相互抵消；`λ_context` 在当前切片上完全 inert。本文把这一现象称为**公共缩放退化（degenerate common-scaling slice）**——它是第 6 章多个"分数不变"结果的根本原因，也是本文最强的自我限制：当前切片只支持公共缩放行为层面的结构性结论。

---

## 5. Validation Framework

五类验证**不是五篇独立研究**，而是对同一个问题的五条攻击路径：

> 当 score 看似稳定时，evidence support 是否也同样稳定？

**Table 3　Main RQ 与五条 Validation Questions（VQ1–VQ5）**

| | 攻击的质疑 | 一句话问题 |
|---|---|---|
| **Main RQ** | — | 观测证据缺失/冲突/可信度不一时，如何避免把 Raw Signal 当可信结论，并显式报告 Reliability、Support/Coverage、允许 ABSTAIN？ |
| **VQ1** Baseline | "Reliability 层其实没必要" | 如果完全不建模 Reliability，会发生什么？ |
| **VQ2** Ablation | "公式里的组件只是装饰" | 模型组件是否真正改变证据支撑？ |
| **VQ3** Sensitivity / Robustness | "结果只是某个参数点碰巧调出来的" | 结论在参数局部变化下是否保持？ |
| **VQ4** Failure / Counterexample | "遇到最困难的记录时模型就没用了" | 高 Raw 是否仍被无条件接受？缺失证据是否被填成 0？ |
| **VQ5** Structural Portability | "模型只是为当前教育数据硬写的" | 同一结构能否在性质完全不同的 Raw Signal 上运行？ |

每条路径统一报告五段：**WHY → SETUP → RESULT → SUPPORTED → NOT SUPPORTED**。

---

## 6. Results

### 6.1 VQ1 — Baseline Validation

**WHY**：检验"如果完全不建模 Reliability，会发生什么"——如果 Raw-only 已经够用，整个框架就没有必要。

**SETUP**：四个候选在**完全相同的 70 条记录**上运行，无拟合模型参与：A Raw-only（M0，observable gate + 均值，不做校正）、B Simple Linear（三项加法折减 + 裁剪）、C Rule-based gated（observable gate + 固定规则）、Current Model（M3，三因子乘法 + 加权聚合 + 状态阈值）。

**RESULT**：

**Table 4　Baseline 对比（同 70 条记录）**

| Model | Aggregate Score (ABL) | Support Mass | Coverage (N=70) | 决策语义 SUPPORTED / LOW / NEE |
|---|---:|---:|---:|---:|
| A Raw-only | 3.5625 | 16.0 | 0.228571 | **16** / 0 / 54 |
| B Simple Linear | 3.5625 | 8.0 | 0.114286 | 0 / 16 / 54 |
| C Rule-based (gated) | 3.5625 | 16.0（raw mass） | 0.228571 | 0 / 16 / 54 |
| **Current Model (M3)** | 3.5625 | **6.0** | **0.085714** | 0 / 16 / 54 |

**SUPPORTED**：四种模型的归一化分数完全相同（3.5625），但 Raw-only 把 16 条可判读记录全部按满权重计入（support mass 16）并标为 `SUPPORTED`，它没有任何通道可以报告"证据等级"与"证据质量"的区别。Reliability 层带来 Raw-only 没有的东西：一个独立的、连续的支持量（16 → 6，coverage 0.228571 → 0.085714），以及"高 Raw 层级仍可能低支持"的解释能力。**所有 aggregate score 相同本身是研究结果，不能隐藏**——它来自公共缩放退化，既不是精度等价，也不是任何公式有效的证据。

**NOT SUPPORTED**：不得写成"主模型 accuracy 更高"（四者同分，且无 human truth）；不得写成"Raw-only 是错误的"（它是必要 baseline，只是不能完整回答 Main RQ）；不得声称乘法形式必需（B 得到相同分数与全部 70 条相同状态决策，support mass 为 8 而非 6，数据无法裁决 8 与 6）；不得把 missing-evidence 拒判单独记功于 Reliability 层（四个候选共享该规则）。

### 6.2 VQ2 — Ablation Validation

**WHY**：检验模型中哪些组成部分真正改变了支持记账与决策语义，回应"公式里的 Reliability / Gate 模块只是装饰"这一质疑。

**SETUP**：从 M0 到 M3 逐步加入组件（`reports/development/ablation_results.csv`；`outputs/final_results.json::ablation[]`）。

**Table 5　Ablation（M0 → M3）**

| Model | Components | Score (ABL / HOT / Gap) | Effective Weight | Coverage (N=70) |
|---|---|---:|---:|---:|
| M0 | 无校正 | 3.5625 / 0.375 / 1.125 | **16.0** | **0.228571** |
| M1 | + confidence | 3.5625 / 0.375 / 1.125 | **12.0** | **0.171429** |
| M2 | + confidence + prompt | 3.5625 / 0.375 / 1.125 | **6.0** | **0.085714** |
| M3 | + confidence + prompt + context | 3.5625 / 0.375 / 1.125 | **6.0** | **0.085714** |

**SUPPORTED**：有效权重 **16 → 12 → 6 → 6**；有效覆盖率 **0.228571 → 0.171429 → 0.085714 → 0.085714**；归一化分数始终保持 3.5625 / 0.375 / 1.125 不变。M0→M1 由 confidence 折减（16 × 0.75 = 12.0），M1→M2 由 prompt 折减（12.0 → 6.0，prompt 承担主要支持下降），M2→M3 因 context 在可判读记录中无变异而完全相同。这证明组件**确实改变 support accounting 与拒判边界**，而非只出现在公式里。**Score stability 不代表 Evidence support stability**——这是核心结论在同一份数据上的第二次独立显现。

[FIGURE F5 HERE]

Figure 5. Ablation / Refusal：M0→M1→M2→M3 有效权重 16→12→6→6；P105 / P108 为 low support，P072 / P035 为 refusal 状态。拒判边界由组件真实驱动，不是装饰；无 true outcome 时不声称准确率提升。

**NOT SUPPORTED**：不得把模块差异解释成独立因果效应；不得声称 context "已证明无作用"（M2 = M3 的原因是数据缺变异，`λ_context` 在当前切片不可识别）。

### 6.3 VQ3 — Sensitivity / Robustness

**WHY**：检验结论是否只是某个参数点碰巧产生的。

**SETUP**：两部分——(1) 在默认 `λ_prompt = 0.50`、`λ_context = 0.50`、`r_medium = 0.75` 上对三个参数分别做 ±10% / ±20% 的 one-at-a-time 扰动（共 15 个条件）；(2) 在 693 个声明参数网格（21 × 11 × 3）上复算边界。

**RESULT**：

**Table 6　693 格声明网格（`independent_bounds_summary.json`）**

| 量 | 结果 |
|---|---|
| 网格规模 | **693** = 21 × 11 × 3 |
| defined / undefined | **660 defined / 33 undefined** |
| ABL 范围 | 3.5625 – 3.5625（全部 defined 格恒定） |
| HOT / Gap | 0.375 / 1.125（同样恒定） |
| **effective weight 范围** | **0.4 – 16.0**（中位数 5.8） |
| **effective coverage 范围** | **0.005714 – 0.228571**（中位数 0.082857） |

15 个扰动条件产生 **0 个 decision-state 翻转**（`total_status_flips = 0`）；归一化分数保持 3.5625（±20% 处出现 1e−16 量级浮点残差）；学生级 ranking 为 `NOT_APPLICABLE`。

[FIGURE F3 HERE]

Figure 3. Evidence degradation / Support–Coverage：受控改变单个证据字段时模型如何响应（P108 假设移除 prompt 风险时 R 从 0.375 → 0.750、adjusted 从 2.25 → 4.50；P072 仅恢复 context 仍为 NO_EFFECTIVE_EVIDENCE）。这是对假设输入字段变化的机械响应，不是真实观测，也不是因果效应。

**SUPPORTED**：在整个 693 格声明网格内，归一化分数恒定，而有效支持跨 0.4 – 16.0（40 倍）、有效覆盖率跨 0.005714 – 0.228571（40 倍）。"分数稳定、支持变化"是局部结构现象，不是单点展示。支持为零时模型返回 `NO_EFFECTIVE_EVIDENCE` 而非伪造分数（33 个 undefined 格正是这一 fail-closed 行为的体现）。

**NOT SUPPORTED**：这是当前切片上的 local structural stability，**不是** global robustness、不是统计置信区间（693 是有限声明网格，不是抽样分布）、不是参数校准。0 个状态翻转的原因之一是所有可判读记录共享同一基线权重 0.375，局部扰动不足以跨越状态阈值——这**削弱**而非增强"状态稳定"的分量。本文**不使用** ranking stability 作为核心证据（ranking 为 `NOT_APPLICABLE`）。

[FIGURE F4 HERE]

Figure 4. Parameter perturbation: score remains effectively constant while support varies across the declared grid. 这是核心结论（Score Stability ≠ Evidence Support Stability）最直接的视觉证据；有限网格不是置信区间。

### 6.4 VQ4 — Counterexample / Failure Cases

**WHY**：检验模型在最困难记录上的行为，回答"高 Raw 是否仍被无条件接受""缺失证据是否被填成 0"。只使用真实存在的案例。

**SETUP**：从 70 条开发记录中选取边界案例（`outputs/final_results.json::counterexamples`）。

**Table 7　真实失败 / 边界案例**

| 记录 | Raw Evidence | Reliability `w_i` | Adjusted 贡献 | 决策状态 |
|---|---|---:|---:|---|
| **P108** | **L6（最高，raw = 6.0）** | **0.375** | **2.25** | **`LOW_SUPPORT` / `ABSTAIN`** |
| P105 | L2（raw = 2.0）；Task L5 而 Student Evidence L2 | 0.375 | 0.75 | `LOW_SUPPORT` |
| P072 | 不可判读（Evidence `UNDETERMINED`） | 0.0 | —（null，**不填 0**） | `NO_EFFECTIVE_EVIDENCE` |
| P035 | 不可判读（Evidence `UNDETERMINED`） | 0.0 | —（null，**不填 0**） | `NO_EFFECTIVE_EVIDENCE` |

**SUPPORTED**：P108 的 Raw 达到最高层级 L6，但因携带 prompt 诱导风险且置信度仅为 medium，可靠性只有 0.375，adjusted 贡献被降为 2.25，决策为 `LOW_SUPPORT` / `ABSTAIN` 而非满额接受。在 Raw-only 基线下，同一条记录会获得 `w = 1` 的满支持并被标为 `SUPPORTED`——这是两个框架最尖锐的分歧点。P072 / P035 因证据不可判读返回 `NO_EFFECTIVE_EVIDENCE`，模型拒绝为其编造分数。这一节直接展示两个语义：**High Raw ≠ High Evidence Support**，以及 **Missing Evidence ≠ Score 0**。

**NOT SUPPORTED**：这是结构性案例，不是准确率或真实错误率；没有独立 true outcome，无法检验 abstain 之后是否"正确"，不得写成"模型预测正确"；案例标签为 `AI_PROVISIONAL`，不是人工确认的典型错误。

### 6.5 VQ5 — External Structural Transfer

**WHY**：检验模型是否只是为当前教育数据硬写，回答"接口能否迁移到性质完全不同的 Raw Signal"。

**SETUP**：把 `Raw → Reliability → Adjusted → ACCEPT/ABSTAIN` 结构复用到一份 BTC-USD 历史纸面模拟（n = 1698，公开行情数据，`synthetic / controlled evidence; no live news feed`）上，做三个 information-missing Gate。

**Table 8　三个 information-missing Gate（`information_missing_validation.json::gates`）**

| Gate | 判据 | 关键数字 | 结果 |
|---|---|---|---|
| **Gate1** | 信息质量/完整性下降 → Reliability 下降 | full mean 0.6027 → missing mean 0.4077 | **SUPPORTED** |
| **Gate2** | 更低 Reliability → abstention 上升、coverage 下降 | coverage 0.3940 → 0.0012 | **SUPPORTED** |
| **Gate3** | 低 Reliability 决策应有更高 future error rate | low-R error 0.5248 vs high-R error 0.5277 | **NOT SUPPORTED** |

⇒ **`risk-coverage improvement = false`**。

**SUPPORTED**：同一接口能在性质完全不同的 Raw Signal 上运行，并在证据质量下降时降低 coverage、增加 abstention（Gate1、Gate2 SUPPORTED）。这说明框架不是只为当前教育数据硬写的。

**NOT SUPPORTED（负结果必须保留）**：Gate3 NOT SUPPORTED——低可靠性决策并**没有**带来更高的 future error rate（0.5248 vs 0.5277，实际上略低），因此"低 R ⇒ 高风险"这一 selective prediction 的核心预期在本数据上未成立。**Gate 3 的 NOT SUPPORTED 本身是重要结果**：它诚实地界定了"拒判能做什么、不能做什么"。不得写 prediction improvement、trading advantage、universal generalization 或教育泛化；不得把它发展成论文第二主线。

[FIGURE F6 HERE]

Figure 6. External Structural Transfer：A / B / C 三个策略的 low / medium / high reliability 分组；Strategy C 反转了排序。这是来自 BTC 历史纸面模拟的部分结构迁移证据，不是教育验证，不是交易主张。

---

## 7. ML Challenger

ML **不是 Main Model**，而是独立挑战者，用于检查"更灵活的数据驱动模型是否暴露主框架没有捕捉到的结构"。当前状态为 **`INSUFFICIENT_FOR_STRONG_ML_CLAIM`**、`NO_SINGLE_DOMINANT_MODEL`。

**SETUP**：以"是否获得可判读 Evidence"为代理目标（16 positives / 70 Gate records），测试逻辑回归、深度 2 决策树与探索性随机森林，重复 4 折交叉验证 × 25 次 = 100 折，并施加特征缺失与跨学期迁移压力测试。

**Table 9　重复交叉验证（mean，100 folds/model）**

| Model | Accuracy | Balanced acc. | F1 |
|---|---:|---:|---:|
| Logistic Regression | 0.875915 | 0.862541 | 0.757802 |
| Shallow Decision Tree | 0.919444 | 0.901195 | 0.814726 |
| Random Forest (exploratory) | 0.922190 | 0.894245 | 0.823291 |

**Table 10　测试时特征缺失压力测试与跨学期迁移**

| 条件 | Logistic acc. | Tree acc. | RF acc. |
|---|---:|---:|---:|
| Clean | 0.871429 | 0.900000 | 0.871429 |
| 20% missing | 0.785714 | 0.814286 | 0.800000 |
| 40% missing | 0.714286 | 0.714286 | 0.742857 |
| 2026春 → 2025秋 | 0.970588 | 0.941176 | **0.588235** |

**为什么没有把 ML 选成主模型**：表面 CV 判别指标不低（0.876 / 0.919 / 0.922），但——

1. **positive = 16**，且是 AI provisional 代理标签，**≠ human truth**；
2. 重复 CV 是对同一 70 条记录的重复重采样，**不是独立证据**，无 true holdout、无 external labeled transfer；
3. 特征缺失 20% / 40% 后降到约 0.71–0.81；RF 跨学期迁移不稳定（2026春→2025秋 仅 **0.588**）；
4. **interpretability**：ML 是 pre-label predictor（预测哪条记录会被标为可判读），主模型是 post-label support transformation（拿到 Evidence 标签后做支持变换 + fail-closed 拒判），二者不是同一件事，不构成直接替代；
5. **evidence semantics**：ML 无法显式表达缺失证据语义与拒判边界；
6. **missing-evidence handling**：主模型有显式 fail-closed `NO_EFFECTIVE_EVIDENCE`，ML 除非另加拒判策略否则仍输出概率；
7. **当前样本限制 + 无独立 holdout / Human Gate**。

因此正确表述是"challenge completed, winner unselected"——**不得**写"手工模型优于机器学习"，也不得写"ML 被击败"；主模型的经验优越性同样未被证明。

---

## 8. Alternative Formulations

替代函数形式的作用是检查：**核心结论是否依赖单一公式形式**，而不是举办模型排行榜。结论继续保持 **`NO_SINGLE_DOMINANT_MODEL`**。

**SETUP**：比较四种函数形式（乘法 A / 加法 B / 门控 C / 非线性 D），协议在查看候选结果前冻结（`tuning: none`），输入为同一份 70 行 `AI_PROVISIONAL` 文件。

**Table 11　四种函数形式（sample-in，n = 70）**

| Model | Formula | `R → 0` 行为 | defined_n | abstain_n | RMSE vs Raw |
|---|---|---|---|---:|---:|---:|
| A 乘法 | `S_raw × R` | `S_adj → 0` | 16 | 0 | 2.4156 |
| B 加法 | `S_raw − λ(1−R)` | 保留 `S_raw − λ` | 16 | 0 | **0.3125**（λ=.5，最小） |
| C 门控 | `R < τ ⇒ ABSTAIN` | `ABSTAIN` | **0** | **16** | null |
| D 非线性 | `S_raw × R^γ` | `S_adj → 0` | 16 | 0 | 1.4981 / 2.4156 / 3.3214 |

**关键分歧案例 P108（Raw = L6 = 6.0，R = 0.375）**：乘法 A 输出 2.25；加法 B（λ=.5）输出 5.6875；门控 C 直接 ABSTAIN；非线性 D 随 γ 从 3.6742 变到 0.84375。

**SUPPORTED**：主现象（分数稳定而支持下降、缺失证据不填 0）在多种函数形式下都存在，因此不是乘法公式的产物。不同形式在弱证据下的行为实质不同，"选择哪种形式"是一个必须公开的建模决定。

**NOT SUPPORTED**：`NO_SINGLE_DOMINANT_MODEL`——不得选出"最佳"公式或阈值。安全导向的拒判偏好 gated rule；接近 Raw 偏好 additive λ=0.5；透明的可靠性衰减与显式缺失状态偏好当前乘法结构。这是 operating-condition choice，不是 universal champion。主模型被保留的理由是研究问题对齐 + 透明性 + 显式缺失证据语义 + 拒判结构，不是"已证明最优"。

---

## 9. Discussion

### 9.1 为什么 Score Stability 不等于 Evidence Support Stability

这是全文中心机制，需要解释清楚，而不是掩饰。

在当前切片上，16 条可判读记录共享同一组因子取值（`prompt = true`、`context = false`、`confidence = medium`），因此任何可靠性加权方案都对每条被纳入的分数施加同一个常数因子 `k`：

```
Score_adj = Σ(k · Raw_i) / Σ(k · w_i⁰) = k · ΣRaw_i / (k · Σw_i⁰) = ΣRaw_i / Σw_i⁰
```

常数因子在归一化中抵消，所以 ABL / HOT / Gap 恒为 3.5625 / 0.375 / 1.125。但支持量 `S = Σw_i` **不做归一化**，它直接随 `k` 缩放：16 → 12 → 6 → 6；693 格网格上跨 0.4 – 16.0。

**这不是 bug，这正是本文的论点。** 一个只看归一化分数的评价体系，在当前数据上**完全无法察觉**支撑它的证据已经从 16 个单位收缩到 6 个单位（覆盖率从 0.228571 收缩到 0.085714，分母 70）。分数看起来一样确定，证据的确定性已经下降了 62.5%。这一现象在三条独立路径上反复出现（Baseline 四模型同分不同支持、Ablation 16→12→6→6、Sensitivity 693 格分数不变而支持 0.4–16.0），是"同一条可复算链上的相互吻合"，而非实验数量堆砌。

### 9.2 为什么 ABSTAIN 是一个有效输出

当 evidence 不足时，拒绝形成强判断，比输出一个貌似精确的数字更合理。ABSTAIN 不是模型的失败，而是模型显式表达"不足以形成可靠判断"。

当前切片下 **0 条 ACCEPT**——这一事实本身是有信息量的：它说明在 AI 提示诱导普遍存在、置信度普遍为 medium 的开发数据上，一个诚实的框架**不应该**给出确定性结论。把这个结果写成"模型没有用"是误读；把它写成"模型成功地拒绝了过度确定的判断"更接近事实，但同样必须与 coverage 一起报告，且不能声称它提高了准确率（无 true outcome）。

### 9.3 为什么当前结果不能升级成因果结论

当前**没有**合法配对的 `Outcome_AI` 与 `Outcome_baseline`，因此 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。本文的 Adjusted Score 是证据加权的描述性分数，不是因果增量。**不得声称 AI 导致学习效果提升。** 任何因果声明都需要合法配对 outcome、独立学习 outcome 与相应识别设计（Hernán & Robins, 2022 的 target-trial 要素），当前项目均不具备。

---

## 10. Limitations

以下限制是当前证据边界的组成部分，**不压缩、不删除**：

### GAP-1 — Human Gate 尚未完成

- Human R1 = **0/70 VALID**，R2 = **0/70**，Formal Gate = **`NOT_RUN`**，`formal_gate_eligible = false`。
- 近期收到的一份标注文件已核验为同一 B 标签的派生副本（`filled_from_B`），**不是**独立 R1/R2，不能作为 test-retest 或 inter-rater 证据。
- 冻结设计是 `single_annotator_test_retest`（非 inter-rater），正式一致性系数尚未产生。

### GAP-2 — Reliability 参数正式校准不足

- `c_i`、`λ_prompt`、`λ_context`、`r_medium` 是假设/敏感性参数，**不是**校准概率，标为 `WEAKLY_JUSTIFIED_COMPONENT`。
- 16 条可判读记录高度同质，prompt / context / confidence / actor 的独立效应不可识别。

### GAP-3 — AI Increment / causal learning gain 无法识别

- 无 `Outcome_AI` / `Outcome_baseline`，`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，不支持 causal learning gain。

### 其他必须保留的限制

- **无 true outcome**：无法验证 abstain 后是否正确，`accuracy_coverage_audit = NOT_RUN`，不能报告准确率提升。
- **finance 仅 structural transfer**：synthetic/controlled 结构演示，Gate3 NOT SUPPORTED，`risk-coverage improvement = false`，no trading advantage claim。
- **ML strong claim unsupported**：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`（16 positives、代理标签、无 holdout、缺失降级、跨学期不稳）。
- **no single dominant formulation**：`NO_SINGLE_DOMINANT_MODEL`。
- **复现边界**：`run_all.py` 32/32 只覆盖开发版核心链路，不覆盖 final artifact / figure / Paper / Demo 全链路。
- **数据完整性 open defects**：21/21 冻结不变量通过，但 `S4-F01`（未来内容泄漏）、`S4-F02`（非盲标队列）仍为 open，已从标注路径隔离。

---

## 11. Conclusion

本研究的主要发现**不是某个 score 更高**，而是：当观测结果的证据完整性和可信度存在差异时，仅报告 Raw Score 可能隐藏重要的不确定性。显式建模 Evidence Reliability、Support / Coverage，并允许 ABSTAIN，可以使评价结果更透明地表达"我们知道什么"以及"我们不知道什么"。

在当前 development slice 中，结果支持：

> **Score Stability ≠ Evidence Support Stability.**
> 分数稳定，不等于证据支持稳定——稳定的评分不意味着支撑该评分的证据同样稳定、充分或可信。

这是一条 **descriptive / structural** 结论（Evidence Level 1），标记为 `DEVELOPMENT_ONLY`，**不**升级为 universal theorem，**不**声称任何模型最优、任何预测准确率提升、任何因果 AI 增量或跨域普适性。五条验证路径与两类对照共同界定了这条结论的边界，其中三条负结果被完整保留：External Transfer Gate3 `NOT SUPPORTED`、`NO_SINGLE_DOMINANT_MODEL`、`INSUFFICIENT_FOR_STRONG_ML_CLAIM`。正式结论须等待 Human Gate 完成（`PENDING HUMAN-ANNOTATION INTAKE VERIFICATION`）。

---

## References

**Evidence Line A — observed performance ≠ true learning**
- Soderstrom, R. A., & Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*, 10(2). DOI 10.1177/1745691615569000.
- Bastani, H., et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*. DOI 10.1073/pnas.2422633122.
- Fan, Y., et al. (2025). Beware of metacognitive laziness. *British Journal of Educational Technology*. DOI 10.1111/BJET.13544.
- Krathwohl, D. R. (2002). A revision of Bloom's taxonomy: An overview. *Theory Into Practice*, 41(4). DOI 10.1207/s15430421tip4104_2.

**Evidence Line B — measurement reliability / evidence quality / missing information**
- Kane, M. T. (2013). Validating the interpretations and uses of test scores. *Journal of Educational Measurement*, 50(1). DOI 10.1111/jedm.12000.
- Gašević, D., Greiff, S., & Shaffer, D. W. (2022). Towards strengthening links between learning analytics and assessment. *Computers in Human Behavior*, 134. DOI 10.1016/j.chb.2022.107304.
- Gray, G., & Bergner, Y. (2022). A practitioner's guide to measurement in learning analytics. *Handbook of Learning Analytics*.
- Little, R. J. A., & Rubin, D. B. (2019). *Statistical Analysis with Missing Data* (3rd ed.). Wiley.
- Rubin, D. B. (1976). Inference and missing data. *Biometrika*, 63(3). DOI 10.1093/biomet/63.3.581.
- Saisana, M., Saltelli, A., & Tarantola, S. (2005). Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators. *Journal of the Royal Statistical Society: Series A*, 168(2). DOI 10.1111/j.1467-985X.2005.00350.x.
- OECD/EU/EC-JRC. (2008). *Handbook on Constructing Composite Indicators*.
- Putnick, D. L., & Bornstein, M. H. (2016). Measurement invariance conventions and reporting. *Developmental Review*, 41. DOI 10.1016/j.dr.2016.06.004.

**Evidence Line C — selective prediction / abstention / risk–coverage**
- El-Yaniv, R., & Wiener, Y. (2010). On the foundations of noise-free selective classification. *Journal of Machine Learning Research*, 11, 1605–1641.
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. *Advances in Neural Information Processing Systems (NeurIPS)*.
- Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *International Conference on Machine Learning (ICML)*.
- Angelopoulos, A. N., et al. (2024). Conformal risk control. *International Conference on Learning Representations (ICLR)*.（仅方法储备）

**Evidence Line D — AI assistance / prompt dependence / automation bias**
- Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors*, 39(2). DOI 10.1518/001872097778543886.
- Skitka, L. J., Mosier, K. L., & Burdick, M. (2000). Does automation bias decision-making? *International Journal of Human-Computer Studies*, 51(5). DOI 10.1006/ijhc.1999.0341.
- Bansal, G., et al. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *Proceedings of CHI*. DOI 10.1145/3411764.3445717.
- Hernán, M. A., & Robins, J. M. (2022). Using big data to emulate a target trial when a randomized trial is not available. *American Journal of Epidemiology*. DOI 10.1093/aje/kwab249.
- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1). DOI 10.1177/001316446002000104.（inter-rater 口径，见 GAP-3）
- Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology* (4th ed.). SAGE.（inter-rater 口径，见 GAP-3）

---

## Appendix — 图表清单与证据索引

**Figure 占位清单（正文已预留，图后补）**

| 图 | 位置 | Caption 摘要 | 源 artifact |
|---|---|---|---|
| F1 | §3 开头 | 整体框架六层链路 | `reports/visual_evidence/final/F1_model_flow.svg` |
| F2 | §3.2 / §6.4 | Raw vs Adjusted 逐记录分离（P108/P105） | `F2_raw_vs_adjusted.svg` |
| F3 | §6.3 | Evidence degradation 响应 | `F3_evidence_degradation.svg` |
| F4 | §6.3 | Score 稳定 vs Support 变化 | `F4_parameter_perturbation.svg` |
| F5 | §6.2 | Ablation 拒判语义 | `F5_ablation_refusal.svg` |
| F6 | §6.5 | External structural transfer | `F6_external_structural_transfer.svg` |

**锁定文件索引**

| 用途 | 路径 |
|---|---|
| 唯一数字源与冲突处理 | `paper/PAPER_NUMBER_LOCK.md` |
| 声明 → 证据 → 数字 → 表/图映射（C1–C13） | `paper/PAPER_EVIDENCE_TRACE.md` |
| 文献引用映射与 CITATION_GAP | `paper/LITERATURE_CITATION_MAP.md` |
| 冻结词汇与非等价关系 | `docs/metric_dictionary.md` |
| 统一事实源 | `outputs/final_results.json` |
| 旧版 V1 论文（保留可追溯，本文不覆盖） | `paper/development_submission_candidate.md` |
| 结构重写 canonical 稿（本文的原型） | `paper/paper_v2_candidate.md` |

---

**PAPER_V2_STATUS = PAPER_V2_CANONICAL_DEVELOPMENT**

_Formal Human Gate 仍未完成，不标 FORMAL_FINAL。所有 Human Gate 依赖结论保持 PENDING / NOT_RUN，所有 AI increment 结论保持 NOT_SUPPORTED。_
