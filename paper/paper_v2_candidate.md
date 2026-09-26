# 当观测不等于证据：面向教育 AI 增量价值评价的证据可靠性与拒判框架

**PAPER_V2_CANONICAL_DEVELOPMENT**（`EVIDENCE_DRIVEN_RESEARCH_PAPER`）

> **状态声明（贯穿全文，不可省略）**
> 本文全部结果来自 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 输入，`formal_gate_eligible = false`，`NOT_HUMAN_VALIDATED`。
> Human R1 = 0/70 VALID，R2 = 0/70，Formal Gate = `NOT_RUN`，`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。
> 本文不报告任何正式人工一致性系数、正式 AIV、学生排名或因果 AI 增量。
> 数字唯一源：`yu/paper/PAPER_NUMBER_LOCK.md` + `yu/outputs/final_results.json`；声明到证据的映射：`yu/paper/PAPER_EVIDENCE_TRACE.md`；文献映射与缺口：`yu/paper/LITERATURE_CITATION_MAP.md`。
> **晋升状态**：`PAPER_V2_CANONICAL_DEVELOPMENT`。因 Formal Human Gate 仍未完成，本文**不**标 `FORMAL_FINAL`。旧版 `paper/development_submission_candidate.md`（V1）保留不删除，可追溯。

---

## Abstract

评价 AI 辅助学习时，最常见的一步是把"观察到的表现"直接映射成分数并据此下结论：`Observed Result → Score / Decision`。这一步隐含了一个未经检验的假设——观测结果本身已经是可靠证据。学习科学与测量文献都指出这个假设可能不成立：即时表现与持久学习可以分离（Soderstrom & Bjork, 2015），AI 辅助练习的表现提升不必然带来撤去 AI 后的独立表现提升（Bastani et al., 2025），而学习分析日志指标必须经过效度论证才能进入解释与用途（Kane, 2013；Gašević et al., 2022）。

本文把这一问题明确定位为 **measurement / identifiability（测量与可识别性）问题**，而非预测问题或因果识别问题，并提出一个可审查的**证据感知评价框架**：把"表现有多高"（Raw Signal）与"这条表现有多少可审查支撑"（Evidence Reliability）分开建模，同时报告分数与有效证据支持（Support / Coverage），并在证据不足时输出 `ABSTAIN` 或 `NO_EFFECTIVE_EVIDENCE`，而不是填入一个看似有意义的分数。

真实数据表明这一关切确实存在。在 70 条开发记录中，仅 16 条具有可判读 Student Evidence，19 条为 `NO_EVIDENCE`、35 条为 `UNDETERMINED`，合计 54 条没有足够证据进入有效评价（`NO_EFFECTIVE_EVIDENCE`，分母始终为 N = 70）。更重要的是，这 16 条可判读记录全部满足 `prompt_induced = true`、`context_truncated = false`、`confidence = medium`、`task_actor = ai`——即当前切片高度同质，prompt / context / confidence / actor 的独立效应无法被充分识别。

在这一数据上，框架得到一条**描述性、结构性**结论：归一化分数（ABL / HOT / Gap = 3.5625 / 0.375 / 1.125）在引入可靠性权重前后保持不变，而有效证据权重从 16 降到 6、有效覆盖率从 0.228571 降到 0.085714。即：

> **Score Stability ≠ Evidence Support Stability（分数稳定，不等于证据支持稳定）。**

这一结论由五条互补验证路径共同攻击同一命题：基线对比（四种模型同分但支持记账不同）、消融（16→12→6→6）、局部参数敏感性（±10% / ±20% 扰动产生 0 个 decision-state 翻转；693 格声明网格中 660 defined / 33 undefined，分数不变而有效权重跨 0.4–16.0）、失败案例（P108 Raw = L6 但 R = 0.375、Adjusted = 2.25 → `LOW_SUPPORT / ABSTAIN`；P072 / P035 → `NO_EFFECTIVE_EVIDENCE`），以及外部结构迁移（BTC 历史纸面模拟 n = 1698：Gate1、Gate2 SUPPORTED，Gate3 NOT SUPPORTED）。两类对照——替代函数形式与机器学习挑战者——进一步表明 `NO_SINGLE_DOMINANT_MODEL` 与 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`：主模型被保留是 **problem-alignment decision**，不是 prediction-winner decision。

正式人工验证尚未完成，因此本文所有结论限于开发级证据边界，并在第 13 章给出可执行的 Formal Evidence Upgrade Protocol。

**Keywords**: evidence reliability；selective prediction / abstention；measurement validity；missing evidence；support and coverage；learning analytics；AI-assisted learning evaluation；sensitivity analysis

---

## 1. Introduction

### 1.1 从一个看似无害的链路说起

评价"AI 是否带来了增量价值"，一个自然的起点是把观察到的结果映射成分数：

```
Observed Result  →  Score / Decision
```

这条链路简短、可计算、易汇报。但它默认了一件事：**观测到的结果本身已经是可靠证据。**

在 AI 参与的学习记录里，这个默认常常不成立。一条学生发言可能同时包含：学生自己的思考、AI 提示的引导、被截断的上下文、不确定的来源归属，以及标注者对"这条到底算不算证据"的犹豫。这些因素不会让记录消失，它们会让记录**看起来仍然可用**——甚至看起来层级很高。

### 1.2 文献指出的关切

四类文献从不同方向指向同一个风险（详见第 2 章）：

- 即时表现与持久学习可分离，甚至方向相反（Soderstrom & Bjork, 2015）；
- 在高中数学的现场随机试验中，AI 辅助练习的表现提升不必然带来撤去 AI 后独立测试的提升（Bastani et al., 2025）；生成式 AI 改善产出也不等于改善知识与迁移（Fan et al., 2025）；
- 测量效度要求"观测 → 指标 → 解释 → 用途"每一跳都有可证伪的论证（Kane, 2013；Gašević et al., 2022；Gray & Bergner, 2022）；缺失不是零值，缺失机制决定可识别性（Little & Rubin, 2019；Rubin, 1976）；
- 允许拒判可以降低保留样本的风险，但代价是覆盖下降，二者必须同时报告（El-Yaniv & Wiener, 2010；Geifman & El-Yaniv, 2017）；置信度不等于校准概率（Guo et al., 2017）。

### 1.3 真实数据表明关切确实存在

本研究不停留在文献层面。在 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 开发记录上（正式 Pilot V1 全量 N = 140，秋 70 + 春 70；上游清洗主结果 `clean_interactions.csv` 含 7028 turns，student 3522 / AI 3506），证据可判读性分布如下：

| 类别 | 数量 | 占比（分母 70） |
|---|---:|---:|
| 可判读 Student Evidence（Bloom L2–L6） | 16 | 0.228571 |
| `NO_EVIDENCE`（无证据） | 19 | 0.271429 |
| `UNDETERMINED`（不可判定） | 35 | 0.500000 |
| 合计 | 70 | 1.000000 |

也就是说，**54 条记录没有足够证据进入有效评价**。如果沿用 `Observed Result → Score` 的单步链路，这 54 条要么被静默丢弃（分母悄悄变成 16），要么被填成 0 分（把"没有证据"伪装成"表现为零"）。两种处理都会让最终分数看起来比证据本身更确定。

同时，16 条可判读记录高度同质：全部 `prompt_induced = true`、`context_truncated = false`、`confidence = medium`、`task_actor = ai`。这意味着即使在这 16 条内部，我们也无法分离"prompt 风险"与"置信度"各自的贡献——这是一个**可识别性**限制，而不是一个可以通过更多计算解决的问题。

### 1.4 把现实翻译成一个数学问题

于是问题变成：能否构造一个评价结构，使得

1. "表现有多高"与"这条表现有多少可审查支撑"是两个**分开报告**的量；
2. 证据不足时，系统**允许不给出结论**，且这种"不给出"本身是一个有语义的输出，而不是失败；
3. 整个链路每一步都可审计、可复算、可被质疑。

### 1.5 Main Research Question（全文唯一正式研究问题）

> **当观测证据存在缺失、冲突或可信度差异时，如何避免直接把 Raw Signal 当成可信结论，并构建一个能够显式报告 Evidence Reliability 与 Support / Coverage，且在证据不足时允许 ABSTAIN 的可审查评价框架？**

**这是一个 measurement / identifiability 问题。**

它**不是**：

- AI 是否提高成绩；
- 学生真实能力预测；
- AI causal learning gain；
- AI vs baseline 的正式效果识别。

上述四个问题都需要当前项目不具备的条件（合法配对的 `Outcome_AI` / `Outcome_baseline`、独立学习 outcome、正式人工标注）。当前状态为 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`（`docs/metric_dictionary.md`）。

**全文只有一个正式 Main Research Question。** 后续所有实验都是对这一个问题的**验证路径**，记作 VQ1–VQ5（Validation Questions），不是五个并列的研究问题。

### 1.6 Contributions

1. 把 `Observed Result → Score` 的单步链路显式展开为可审查的六层结构：`Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support / Coverage → Decision`。
2. 明确区分"分数稳定"与"证据支持稳定"两个量，并在真实开发数据上展示二者可以分离（16→6；0.228571→0.085714，分数恒为 3.5625）。
3. 引入 fail-closed 的拒判语义：有效证据为零时返回 `NO_EFFECTIVE_EVIDENCE`，而不是填入 0 分；并明确 `NO_EFFECTIVE_EVIDENCE ≠ 0 分`、`Missing Evidence ≠ Zero Performance`。
4. 用五条互补验证路径 + 两类对照攻击同一核心命题，并对每条路径明确写出"支持什么、不支持什么"，包括必须保留的负结果（External Transfer Gate3 NOT SUPPORTED；`NO_SINGLE_DOMINANT_MODEL`；`INSUFFICIENT_FOR_STRONG_ML_CLAIM`）。
5. 诚实登记文献缺口（`CITATION_GAP`）与证据缺口，并给出可执行的 Formal Evidence Upgrade Protocol，而不是把待验证设计写成已完成验证。

---

## 2. Literature Review and Research Gap

本章不做文献罗列。四条 evidence line 各自回答一个问题：**它支持我们哪一个建模选择？**

### 2.1 Evidence Line A — Observed performance ≠ automatically true learning / true ability

| 文献 | 该文献在其设计下成立的结论 | 支持的建模选择 |
|---|---|---|
| Soderstrom & Bjork (2015), *Learning Versus Performance*, DOI 10.1177/1745691615569000 | 即时训练表现与较持久的学习可分离，甚至方向相反 | Raw Signal 只能命名为"可观察证据等级"，不能命名为 true learning / true ability → 支持第 5 章把 Raw 与 Reliability 分层 |
| Bastani et al. (2025), *Generative AI without guardrails can harm learning*, PNAS, DOI 10.1073/pnas.2422633122 | 现场随机试验中，AI 辅助练习的提升不必然带来撤去 AI 后独立测试的提升 | 不能把 AI 参与条件下的观测分数直接当作学习增益 → 支持 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED` 的边界声明 |
| Fan et al. (2025), *Beware of Metacognitive Laziness*, BJET, DOI 10.1111/BJET.13544 | 生成式 AI 改善产出可与知识增益 / 迁移不一致 | 过程指标不能替代结果效标 → 支持本文只报告描述性证据分数，不报告能力估计 |
| Krathwohl (2002), *A Revision of Bloom's Taxonomy*, DOI 10.1207/s15430421tip4104_2 | 六类认知过程是教学与评价的**分类语言**，不是能力真值 | Bloom L2–L6 是 Raw Signal 的编码词汇，不是稳定能力测量 → 支持第 5.1 节对 Raw Signal 的解释边界 |

**这条线支持的建模选择**：Raw 层必须是**描述性**的，且必须与"这条描述有多少支撑"分离。
**这条线不支持**：本文任何关于学生学习增益、能力水平或 AI 因果效果的陈述——本文也不做此类陈述。

### 2.2 Evidence Line B — Measurement reliability / measurement error / evidence quality / missing information

| 文献 | 该文献在其设计下成立的结论 | 支持的建模选择 |
|---|---|---|
| Kane (2013), *Validating the Interpretations and Uses of Test Scores*, DOI 10.1111/jedm.12000 | 支持"分数解释"不等于支持"把分数用于某个用途"；用途越强，证据要求越高 | 每一层（observation → scoring → generalization → extrapolation → decision）都需要单独的论证 → 支持第 4 章的六层展开与第 7 章的多路径验证设计 |
| Gašević, Greiff & Shaffer (2022), DOI 10.1016/j.chb.2022.107304 | 学习分析日志指标必须经过任务、构念、可信度、公平性与结果效度论证 | 把 coverage / missingness 当作**测量条件**而非 nuisance → 支持 Support / Coverage 与 Score 分开报告 |
| Gray & Bergner (2022), *A Practitioner's Guide to Measurement in Learning Analytics* | 先问数据测量什么、可推断什么，再定义指标与用途 | 支持第 3 章先做 Data and Evidence Audit、再定义模型（而不是先有分数再补解释） |
| Little & Rubin (2019), *Statistical Analysis with Missing Data*；Rubin (1976), DOI 10.1093/biomet/63.3.581 | 缺失机制决定可识别性；缺失不等于零值；MNAR 需敏感性分析 | 直接支持 `NO_EFFECTIVE_EVIDENCE` 语义：54 条不填 0，保留为独立状态；`I(observable_i)` 是显式 missingness indicator |
| Saisana, Saltelli & Tarantola (2005), DOI 10.1111/j.1467-985X.2005.00350.x；OECD/EU/EC-JRC (2008) | 综合指标的权重、补偿性与聚合方式都是**价值/模型选择**，必须公开并做多方案比较 | 支持把 `λ_prompt`、`λ_context`、`r_medium` 声明为 transparent / preregistered design assumptions，并用敏感性分析检验（第 6.3、8.3 节），而不是声称已校准 |
| Putnick & Bornstein (2016), DOI 10.1016/j.dr.2016.06.004 | 只有达到相应测量不变性层级，跨组均值比较才有解释基础 | 支持把跨学期 / 跨域比较降级为条件比较，并支持 External Transfer 只作结构迁移（第 10 章） |

**这条线支持的建模选择**：证据质量必须进入模型；缺失必须是状态而非数值；参数必须公开并接受敏感性检验。
**这条线不支持**：本文的具体权重取值（0.75 / 0.5 / 0.5）具有文献先例——见 §2.5 `CITATION_GAP`。

### 2.3 Evidence Line C — Selective prediction / abstention / reject option / risk–coverage

| 文献 | 该文献在其设计下成立的结论 | 支持的建模选择 |
|---|---|---|
| El-Yaniv & Wiener (2010), JMLR 11:1605–1641 | 允许 abstain 可降低保留样本风险，但代价是 coverage 下降；`coverage = P(g(X)=1)`、`R_sel = E[L(f(X),Y) | g(X)=1]`，二者必须同时报告 | 直接支持 `ACCEPT / ABSTAIN` 决策层，以及"拒判必须与 coverage 同时报告、不得宣传为靠过滤提升准确率"的纪律 |
| Geifman & El-Yaniv (2017), NeurIPS | 置信度阈值可形成经验 risk–coverage trade-off，但必须在独立校准集选择、在测试集评估 | 支持本文**不**声称已优化阈值，并把阈值校准列为 pending（第 13 章）；也支持 Gate3 负结果的诚实保留（无外部 outcome 时无法验证拒判是否"正确"） |
| Guo et al. (2017), *On Calibration of Modern Neural Networks*, ICML | 现代模型可严重过度自信；confidence ≠ 校准概率 | 支持把 `c_i`（high = 1 / medium = 0.75 / low = 0.5）明确标为**假设支持分**，`w_i` 不是概率 |
| Angelopoulos et al. (2024), *Conformal Risk Control*, ICLR | 在交换性等条件下可把拒判升级为有限样本风险控制 | **仅作后续方法储备**：当前无足够人工真值，本文不声称已有 conformal guarantee |

**这条线支持的建模选择**：ABSTAIN 是合理的模型输出，不是模型失败；拒判语义必须与 coverage 绑定报告。
**这条线与本项目的关键差异**（必须写明，否则会被答辩追问）：selective classification 通常假设**可观测的风险标签**；本文面对的是**证据支持不足 / 冲突 / 不可判读**，没有独立 true outcome。因此本文不能报告 selective risk，只能报告 support / coverage 与决策状态分布。

### 2.4 Evidence Line D — AI assistance / prompt dependence / automation bias / external assistance

| 文献 | 该文献在其设计下成立的结论 | 支持的建模选择 |
|---|---|---|
| Parasuraman & Riley (1997), DOI 10.1518/001872097778543886 | 自动化错误会引发 misuse，不信任或忽略会引发 disuse；界面与情境影响依赖 | 支持把 `AI_suggestion` 与 `student_evidence` 分列记录 → 支持 Raw Signal 只编码 Student Evidence 轴 |
| Skitka, Mosier & Burdick (2000), DOI 10.1006/ijhc.1999.0341 | 人可能把自动化建议当作默认答案，增加遗漏与盲目采纳 | 支持 `prompt_induced` 标记与 `λ_prompt` 折减项的**存在性**（不是其具体取值） |
| Bansal et al. (2021), CHI, DOI 10.1145/3411764.3445717 | AI 解释不必然改善互补表现；主观信任与实际可靠性可能错配 | 支持把 confidence / acceptance 与 correctness 分开核验 → 支持"无 true outcome 时不报告准确率"的边界 |
| Hernán & Robins (2022), DOI 10.1093/aje/kwab249 | 观察数据要先写清理想试验（人群、处理、时间零点、结局、随访、estimand），缺一项就降为描述性/条件关联 | 支持本文把 `Delta_raw = Outcome_AI − Outcome_baseline` 分支显式标为 `NOT_SUPPORTED`，不进入开发版 Adjusted Score |
| Cohen (1960), DOI 10.1177/001316446002000104；Krippendorff (2018) | 标注一致性统计（κ、α）及其对类别盛行率、距离函数的敏感性 | 支持第 13 章的一致性报告设计（保留混淆矩阵、每类支持量，不只报一个系数）。**注意**：二者是 inter-rater 口径，本项目冻结设计是同一标注者 test-retest，见 §2.5 |

**这条线支持的建模选择**：AI 提示诱导风险与来源归属必须进入可靠性计算，不能假设观测到的学生表现是"纯学生"的。
**这条线不支持**：本项目中确实存在自动化偏差的实证结论——上述文献是概念与实验框架，其偏差率不能外推到本项目的学生群体。

### 2.5 Research Gap 与 CITATION_GAP（诚实登记）

**Research Gap（本文填补的位置）**：
现有学习分析测量框架（Kane, 2013；Gašević et al., 2022；Gray & Bergner, 2022）强调每一跳都要有可证伪论证，但**缺少一个把"证据支持"显式纳入评分、并允许在证据不足时拒判的具体评价结构**；选择性分类文献（El-Yaniv & Wiener, 2010；Geifman & El-Yaniv, 2017）为"拒判 + coverage"提供了形式基础，但**通常假设可观测的风险标签**，而教育 AI 交互日志面对的是证据支持不足 / 冲突 / 不可判读。本文的位置是这两者之间的具体构造。

**CITATION_GAP（保留 `yu/paper/LITERATURE_CITATION_MAP.md` §5 全部三项，不虚构文献）**：

| # | 缺口 | 本文处理方式 |
|---|---|---|
| GAP-1 | 「AI 辅助学习交互日志中的 Evidence Reliability 加权」这一**精确建模构造**在项目文献矩阵中没有任何一篇直接提出；最近的 Gašević / Gray & Bergner 只是测量效度框架，不是该权重公式 | 只声明为「本文提出的可审查支持权重」，**不声称有直接文献先例**，不声称乘法形式最优 |
| GAP-2 | 「Student Evidence Bloom L2–L6 作为可判读等级」的**本地标注效度**无对应文献；只有 Krathwohl (2002) 支撑 Bloom 作为分类语言 | 标注效度留待 Human Gate / 本地验证（第 13 章），正文不写成已验证 |
| GAP-3 | 「同一标注者 test-retest（非 inter-rater）」的**既定规范引用**缺失；Cohen / Krippendorff 是 inter-rater 口径 | 正文如实写明设计类型为 `single_annotator_test_retest`、`inter_rater = false`（`reports/annotation_gate_report.json`），**不借用 inter-rater 文献冒充** |

**引用纪律（本文遵守）**：只引用"该论文设计下成立的结论"；不把相关性写成因果；不把模型参数写成已校准；不把拒判 risk–coverage 写成 Gate 已通过；跨领域方法论文用于公式/验证设计时标注"方法依据"，不冒充教育实证。

**本文不声称**：任何文献证明了当前具体乘法公式 `w_i = I_i · c_i · (1 − λ_prompt p_i)(1 − λ_context t_i)` 是最优的。文献支持的是**建模方向**（可靠性应被建模、缺失应是状态、拒判应被允许、AI 来源应被标记），不是**具体函数形式与参数取值**。

---

## 3. Data and Evidence Audit

本章先讲数据的故事，再报数字。顺序是刻意的：**先审计证据可用性，再定义模型**——因为模型能说什么，取决于证据允许说什么。

### 3.1 数据从哪里来

| 层级 | 事实 | 来源 |
|---|---|---|
| 正式 Pilot V1 全量 | **N = 140**（秋 70 + 春 70） | `data/processed/pilot_sample.csv`（140 行）；`docs/DATA_STRUCTURE.md` §2 |
| 上游清洗主结果 | **7028 turns**，其中 student = **3522**、AI = **3506** | `data/processed/clean_interactions.csv`；`docs/DATA_STRUCTURE.md` §2 |
| 当前 development slice | **N = 70**，标注来源 `AI_PROVISIONAL`，状态 `DEVELOPMENT_ONLY` | `data/annotations/ai/pilot_ai_provisional.csv`（70 行）；`outputs/final_results.json::data_identity.sample_count` |

这 70 条是正式 Pilot V1 中被冻结用于当前 Gate 的核心样本；其余 70 条不属于当前 Gate 范围，且**未标注**。因此本文**不得**把 70 外推为 140，也不得把 70 条描述为总体代表。

输入可复现性回执（`outputs/final_results.json::reproducibility`）：输入文件 sha256 `1f09059c56e8ba55a9467db93d526d146d505d8159498dd7e7dc3171d3d33b25`、70 行；Git HEAD `667ecf7e25226366014687aa0ff77cbd80d8df34`（branch `master`）；运行时 Python 3.14.2 / pandas 3.0.1 / numpy 2.4.1 / Windows-11。

### 3.2 证据可判读性：本文最核心的数据事实

独立复算（`reports/verification/independent_bounds_summary.json::raw_recount`，`independent_implementation = true`）给出：

**Table 3-1　证据可判读性分布（分母 N = 70）**

| 类别 | 数量 | 说明 |
|---|---:|---|
| 可判读 Student Evidence（Bloom L2–L6） | **16** | L2×5、L3×5、L4×1、L5×2、L6×3 |
| `NO_EVIDENCE` | **19** | 找不到可判读的学生证据 |
| `UNDETERMINED` | **35** | 存在材料但不可判定 |
| **合计** | **70** | — |
| ⇒ `NO_EFFECTIVE_EVIDENCE` | **54** | = 19 + 35，有效证据权重为零 |

### 3.3 「54」不等于「54 个零分」

这是本文最需要被听清的一句话。

54 条记录**不是**54 个表现为零的学生。它们是 54 条**没有足够证据进入有效评价**的记录：19 条找不到可判读的学生证据，35 条材料存在但不可判定。把它们编码为 0 分，等于用"没有证据"伪造"表现为零"——这正是本文要防止的过度确定。

因此模型的 fail-closed 规则是：当 `Σw_i = 0` 时返回 `NO_EFFECTIVE_EVIDENCE`，**不填 0**（`outputs/final_results.json::development_results.explain_records` 中 54 条的 `raw_score = null`、`adjusted_score = null`）。这一语义有明确的缺失数据文献依据（Little & Rubin, 2019；Rubin, 1976：缺失机制决定可识别性，缺失不等于零值）。

相应地，**Coverage 的分母始终为 70**，包含无证据与不可判读记录。本文每次出现 coverage 都写明分母；把分母悄悄换成 16 是最常见的误导手法，本文禁止（`docs/metric_dictionary.md`："The denominator must be reported with every coverage value"）。

### 3.4 16 条可判读证据高度同质：一个必须前置的可识别性限制

独立复算同时给出（`independent_bounds_summary.json::raw_recount`）：

**Table 3-2　全样本 vs 可判读子样本的因子分布**

| 因子 | 全部 70 条 | 16 条可判读 |
|---|---|---|
| `prompt_induced` | true 53 / false 17 | **true 16 / false 0** |
| `context_truncated` | true 28 / false 42 | **true 0 / false 16** |
| `confidence` | low 51 / medium 19 | **medium 16（无 high、无 low）** |
| `task_actor` | ai 53 / student 11 / unknown 6 | **ai 16** |
| `task_source` | ai_prompt 53 / student_request 11 / unknown 6 | **ai_prompt 16** |

**这直接意味着**：`prompt`、`context`、`confidence`、`actor` 四个因子的**独立效应目前不能被充分识别**。所有可判读记录共享同一组因子取值，因此：

- 每条可判读记录的可靠性权重都等于同一个常数 `R = 0.75 × (1 − 0.5×1) × (1 − 0.5×0) = 0.375`；
- 任何加权方案对每条被纳入的分数施加**同一常数因子**，归一化后相互抵消；
- `λ_context` 在当前切片上**完全 inert**（无可判读记录带 context 截断），其作用只能作 sensitivity-only 情景，不能被解释为"已证明 context 无作用"。

`independent_bounds_summary.json::stability` 对此的机器判定是：`all_readable_prompt_induced = true`、`all_readable_context_not_truncated = true`、`all_readable_confidence_medium = true`，reason = "Every readable row has the same prompt/context/confidence factors, so parameter-dependent factors are a common multiplier and cancel in normalized metrics."

本文把这称为**公共缩放退化（degenerate common-scaling slice）**。它是第 8 章多个"分数不变"结果的根本原因，也是本文最强的自我限制：**当前切片只支持公共缩放行为层面的结构性结论。**

### 3.5 证据审计的另一面：数据完整性与已知缺陷

- `src/verify_pilot_integrity.py`：21/21 冻结不变量通过，另有 **2 个 open defects**：`S4-F01`（未来内容泄漏）、`S4-F02`（非盲标队列）。二者均已从标注路径隔离，但缺陷状态如实保留（`reports/annotation_gate_report.json::completed_checks`）。
- `run_all.py`：**32/32 PASS**（六步，exit-code 0）。但其 scope 只覆盖**开发版核心链路**，不覆盖 final artifact / figure / Paper / Demo 的全链路生成。本文按此如实描述，不声称全链路可复现（`PAPER_NUMBER_LOCK.md` CONFLICT 4）。
- 一份近期收到的标注文件已核验为**同一 B 标签的派生副本**（`filled_from_B`），它**不是**独立 R1/R2，不能作为 test-retest 或 inter-rater 证据。

### 3.6 数字口径与冲突处理（不静默选择）

`PAPER_NUMBER_LOCK.md` §2 登记了 4 处冲突，本文的处理如下——全部公开，不做静默选择：

| # | 冲突 | 本文采用 | 本文拒绝 | 理由 |
|---|---|---|---|---|
| C1 | Demo 的 `raw_metrics` = 12.0 / 0.171429，与 M0 Raw = 16.0 / 0.228571 不一致 | `outputs/final_results.json`（M0 Raw = 16 / 0.228571） | `reports/demo/demo_payload.json` 的 raw_metrics | Demo 的"raw"是 confidence-only theta0/M1（λ_prompt = 0、λ_context = 0、r_medium = .75），不是无校正的 M0 Raw |
| C2 | `reports/failure_cases/development_candidates.json` 把 P105/P108 的 raw/adjusted 全写 null | `outputs/final_results.json::counterexamples`（P105 = 2.0/0.75，P108 = 6.0/2.25；P072/P035 = null） | 上述文件对 P105/P108 的 null | `final_results.json` 是统一事实源；P105/P108 可判读，其 raw/adjusted 有定义；P072/P035 不可判读，null 正确保留为 `NO_EFFECTIVE_EVIDENCE` |
| C3 | Demo 默认 λ = 0/0，adjusted artifact 用 λ = 0.5/0.5 | `model_parameters.adjusted_default`（λ = 0.5/0.5，M3） | Demo 默认 λ = 0/0（theta0/M1） | 论文 Adjusted 口径是 M3（confidence + prompt + context） |
| C4 | `run_all.py` 32/32 的覆盖范围 | 描述为"开发版核心链路可复现" | 全链路可复现的说法 | 数字真实，scope 必须如实标注 |

---

## 4. Problem Formulation

### 4.1 传统形式，以及它的问题

传统评价把问题写成一个映射：

```
Score_i = f(x_i)
```

其中 `x_i` 是第 i 条记录的可观察特征。这个形式在数学上没有问题，问题在于它的**语义承诺**：它假设 `f` 的输出可以直接被解释为"该记录所代表表现的可信度量"。

一旦证据质量存在差异，这个承诺就失效了。考虑两条记录，它们的 Raw Observation 完全相同（都是 Student Evidence L6）：

- 记录甲：上下文完整、来源明确、非 AI 提示诱导、标注高置信；
- 记录乙：AI 提示诱导、标注中等置信（这正是本项目 P108 的情形）。

在 `Score_i = f(x_i)` 下，甲和乙**自动拥有相同的解释强度**。但它们的可审查支撑显然不同。这不是 `f` 选得不够好——任何只以 Raw 层级为输入的 `f` 都会给出相同结果。缺失的是一个**独立的维度**。

### 4.2 把现实翻译成数学问题

于是本文把单步链路展开为六层，每层回答一个不同的问题：

```
Observed Evidence      ── 实际看到了什么？（可判读 / 无证据 / 不可判定）
      ↓
Raw Signal             ── 原始表现信号有多高？（Student Evidence Bloom L2–L6）
      ↓
Evidence Reliability   ── 这条信号有多少支持依据？（w_i，有界支持权重）
      ↓
Adjusted Evaluation    ── 弱支持如何影响评价？（Raw_i × w_i）
      ↓
Support / Coverage     ── 还有多少有效支撑？（S = Σw_i；C_eff = Σw_i / N，N = 70）
      ↓
Decision               ── 是否应作判断？（ACCEPT / ABSTAIN / LOW_SUPPORT / NO_EFFECTIVE_EVIDENCE）
```

**Figure 1（F1 Model Flow）** 给出这一链路的可视化。
- **Question**：模型各层如何衔接，"不可判读"走哪条路？
- **Result**：链路为 `Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision`；不可判读 Evidence 直接返回 `NO_EFFECTIVE_EVIDENCE`；AI Increment 分支标为 `NOT_SUPPORTED`。
- **Meaning**：Raw 与 Reliability 是**两个独立层**，这是本文全部结论的结构前提（对应 Claim C1）。
- 路径：`yu/reports/visual_evidence/final/F1_model_flow.svg`。

### 4.3 形式化定义

设分析输入为 N = 70 条开发记录，第 i 条记录：

- `I(observable_i) ∈ {0, 1}`：Student Evidence 可判读（Bloom L2–L6）时为 1，`NO_EVIDENCE` / `UNDETERMINED` 时为 0（**fail-closed**）；
- `Raw_i`：可判读时的 Bloom 层级数值；不可判读时**无定义**（`null`，不取 0）；
- `c_i`：标注置信度映射；`p_i`：AI 提示诱导标记；`t_i`：上下文截断标记。

**Evidence Reliability（证据可靠性权重）**：

```
w_i = I(observable_i) · c_i · (1 − λ_prompt · p_i) · (1 − λ_context · t_i)
```

**Adjusted Evaluation（校正评价）**：

```
Adjusted_i = Raw_i × w_i        （仅在 I(observable_i) = 1 时有定义）
```

**Support 与 Coverage**：

```
S     = Σ_i w_i                 （有效证据权重之和）
C_eff = Σ_i w_i / N             （有效覆盖率，分母 N = 70，含无证据与不可判读记录）
```

**聚合分数**（当 `S > 0`）：

```
Score_adj = Σ_i w_i · Raw_i / Σ_i w_i
```

**Decision（决策状态）**：

| 状态 | 触发条件 | 语义 | 不是什么 |
|---|---|---|---|
| `ACCEPT` | 分数有定义且满足声明的支持规则 | 可作判断 | 不是"预测正确" |
| `ABSTAIN` / `LOW_SUPPORT` | 证据不足、冲突或支持较弱 | 暂缓判断 | 不是模型失败，不是准确率提升 |
| `NO_EFFECTIVE_EVIDENCE` | `Σw_i = 0` | 无可评价证据 | **不是 0 分**，不是"预测错误" |

### 4.4 一个必须保留的未支持分支

理论上，若要讨论 AI 增量，需要：

```
Delta_raw      = Outcome_AI − Outcome_baseline
Delta_reliable = Delta_raw × R
```

当前项目**不存在**合法配对的 `Outcome_AI` 与 `Outcome_baseline`，因此这条分支状态为 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，**不进入**开发版 Adjusted Score（`docs/metric_dictionary.md`）。本文的 `Adjusted Score` 是**证据加权的描述性分数**，不是 `Reliable AI Increment`。二者不可互换。Hernán & Robins (2022) 的 target-trial 逻辑正是这一降级的方法依据：缺少 baseline pairing、独立 outcome 与分配机制时，只能保持描述性/条件关联。

---

## 5. Evidence-Aware Evaluation Model

本章逐层给出定义、当前取值与其语义边界。

### 5.1 Raw Signal（原始信号）

**回答的问题**：我们观察到了什么？

Raw Signal 记录可观察到的证据等级——本文用 Student Evidence 的 Bloom 层级（冻结手册 L2–L6）表示。当前 16 条可判读记录的构成为 L2×5、L3×5、L4×1、L5×2、L6×3。

**语义边界**：Raw Signal 只回答"这条证据有多高"，不回答"这条证据是否可信"。它是描述性证据等级，**不是** AI 增量、不是可靠性、不是真实能力、不是校准概率。Bloom 是认知过程分类语言，不是稳定能力测量（Krathwohl, 2002）。当记录不可判读（`NO_EVIDENCE` / `UNDETERMINED`）时，**不强行为它编码一个分数**。

### 5.2 Evidence Reliability（证据可靠性）

**回答的问题**：这条证据有多少支撑依据？

```
w_i = I(observable_i) · c_i · (1 − λ_prompt · p_i) · (1 − λ_context · t_i)
```

**参数当前取值（冻结）**：

| 参数 | 取值 | 性质 |
|---|---|---|
| `c_i`（confidence 映射） | high = **1.0**，medium = **0.75**，low = **0.5** | transparent / preregistered design assumption |
| `λ_prompt` | **0.5** | transparent / preregistered design assumption |
| `λ_context` | **0.5** | transparent / preregistered design assumption |
| `I(observable_i)` | 可判读 = 1，否则 = 0 | fail-closed 结构规则 |

**当前切片上的实际结果**：16 条可判读记录全部 `prompt = true / context = false / confidence = medium`，因此每条的可靠性权重都是

```
w_i = 1 × 0.75 × (1 − 0.5 × 1) × (1 − 0.5 × 0) = 0.75 × 0.5 × 1 = 0.375
```

于是 `S = 16 × 0.375 = 6.0`，`C_eff = 6.0 / 70 = 0.085714`。

**语义边界（三条，全部必须写明）**：

1. **`w_i` 不是概率。** 它没有在独立校准集上验证过，不满足任何频率解释。若未来要把 reliability 解释为概率，必须使用 ECE / reliability diagram 并分离校准集与测试集（Guo et al., 2017）。当前 `c_i` 是**假设支持分**。
2. **`w_i` 不是因果系数。** 它不表示"prompt 导致表现下降多少"。
3. **参数不是通过当前样本学习得到的最优值。** 它们属于 transparent / preregistered design assumptions，其合理性通过 sensitivity analysis 检验（§8.3），正式校准留待 Human Gate 与本地效度验证（第 13 章）。`PAPER_EVIDENCE_TRACE.md` C2 将 `λ_prompt / λ_context / r_medium` 标为 `WEAKLY_JUSTIFIED_COMPONENT`。

**Figure 2（F2 Raw vs Adjusted）**：
- **Question**：Raw 与 Adjusted 在记录级别如何分离？
- **Result**：P108（L6，R = .375，贡献 2.25）与 P105（L2，R = .375，贡献 0.75）是逐记录贡献；面板保留 N = 70、16 条可判读、54 条 `NO_EFFECTIVE_EVIDENCE`；无定义记录**不被画成零**。
- **Meaning**：分数与支持是两个轴；undefined ≠ 0（对应 Claim C2、C9）。
- 路径：`yu/reports/visual_evidence/final/F2_raw_vs_adjusted.svg`。

### 5.3 Adjusted Evaluation（校正评价）

**回答的问题**：弱支持如何影响评价？

```
Adjusted_i = Raw_i × w_i
```

相同的 Raw Signal，在不同 Reliability 下，其可接受程度应当不同。一条高 Raw 但低支持的记录，不应被当成与高 Raw 且高支持的记录等价。

**语义边界**：`Adjusted Score ≠ Reliable AI Increment`。后者需要当前项目尚未具备的 `Outcome_AI − Outcome_baseline` 配对（§4.4）。

### 5.4 Support / Coverage（支持度与覆盖率）

**回答的问题**：还有多少有效支撑？

```
S = Σ_i w_i           C_eff = S / N，N = 70
```

Support 与 Coverage 是**独立于分数**的两个量，必须分开报告。二者也不同：support 是权重之和，coverage 是权重（或计数）除以全部输入记录（`docs/metric_dictionary.md` Non-equivalences）。

当前两个口径：

| 口径 | Score（ABL / HOT / Gap） | Effective Weight | Effective Coverage（分母 70） |
|---|---|---:|---:|
| Raw（M0，无校正） | 3.5625 / 0.375 / 1.125 | 16.0 | 0.228571 |
| Adjusted（M3，confidence + prompt + context） | 3.5625 / 0.375 / 1.125 | 6.0 | 0.085714 |

**Raw 与 Adjusted 分数相同，这不是 improvement，也不是任何公式有效的证据。** 它是 §3.4 所述公共缩放退化的直接后果：16 条可判读记录共享同一组因子，各加权方案施加同一常数因子，归一化后抵消。`independent_bounds_summary.json::bounds` 给出 693 格网格上 `ABL_min = 3.56250`、`ABL_max = 3.56250`（浮点误差量级 1e-16），`HOT` 与 `Gap` 同样恒定。

### 5.5 Decision and Abstention（决策与拒判）

模型输出三种状态（`model_parameters.evaluation_statuses`：`DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`、`LOW_SUPPORT`、`NO_EFFECTIVE_EVIDENCE`）。当前 70 条的状态分布为：

| 状态 | 数量 |
|---|---:|
| `SUPPORTED` / `ACCEPT` | **0** |
| `LOW_SUPPORT`（16 条可判读） | **16** |
| `NO_EFFECTIVE_EVIDENCE`（19 + 35） | **54** |

**注意：当前切片下没有任何一条记录被 ACCEPT。** 这不是模型"失败"，而是证据状态的如实反映：全部 16 条可判读记录都带 prompt 诱导风险且置信度仅为 medium。

当证据不足时，`ABSTAIN` / `NO_EFFECTIVE_EVIDENCE` 本身是合理的模型输出——它在防止过度结论（overclaim）。纪律要求（来自 El-Yaniv & Wiener, 2010 的 risk–coverage 框架，以及 `docs/metric_dictionary.md`）：

- 拒判**必须与 coverage 同时报告**；
- **不得**宣传为"靠过滤提升准确率"（`accuracy_coverage_audit = NOT_RUN`，无 true outcome）；
- **不得**把 `NO_EFFECTIVE_EVIDENCE` 写成 0 分，也不得写成"预测错误"。

**Figure 5（F5 Ablation / Refusal）**：
- **Question**：逐层加入可靠性组件时，拒判语义如何变化？
- **Result**：M0→M1→M2→M3 有效权重 `16→12→6→6`；P105 / P108 为 low support，P072 / P035 为 refusal 状态。
- **Meaning**：拒判边界由组件真实驱动，不是装饰；无 true outcome 时不声称准确率提升（对应 Claim C4、C7）。
- 路径：`yu/reports/visual_evidence/final/F5_ablation_refusal.svg`。

---

## 6. Model Design Rationale

第 5 章说明模型**是什么**；本章说明它**为什么这样设计**，以及设计中哪些部分是选择、哪些部分是被数据强制的。

### 6.1 为什么需要独立的 Reliability 层

§4.1 已给出核心论证：在 `Score_i = f(x_i)` 下，两条 Raw 相同但证据质量不同的记录自动获得相同解释强度。这不是 `f` 的形式问题，而是**维度缺失**问题。Reliability 层的作用是补上这个维度，使"表现有多高"与"这条表现有多少可审查支撑"成为两个可分别报告的量。

文献依据：Kane (2013) 的 interpretation/use argument 要求每一跳单独论证；Gašević et al. (2022) 要求把 coverage / missingness 当作测量条件；Little & Rubin (2019) 要求缺失保留为状态。

### 6.2 为什么是乘法结构（以及它没有被证明最优）

**Multiplicative formulation 是一个建模设计选择。** 设计理由有四条：

1. **低 Evidence Quality 不应被高 Raw Signal 自动抵消。** 乘法结构下，`R → 0` 时 `Adjusted → 0`，无论 Raw 多高。加法结构做不到这一点：在 `S_raw − λ(1−R)` 下，Raw = 6、R = 0 时输出仍为 `6 − λ`（λ = 0.5 时为 5.5）。本文的替代公式实验（§9.1）直接量化了这一差异：P108（Raw = L6，R = 0.375）在乘法下输出 2.25，在加法 λ = 0.5 下输出 **5.6875**、λ = 1.0 下输出 **5.375**。
2. **`R → 0` 时自然收缩**，与"证据消失则结论消失"的直觉一致，无需额外裁剪规则。
3. **缺失证据语义明确**：`I(observable_i) = 0` 使 `w_i = 0`，`Σw_i = 0` 直接触发 `NO_EFFECTIVE_EVIDENCE`，而不是产生一个数值。
4. **便于审计**：每个最终决策都能追溯到 `c_i`、`p_i`、`t_i` 三个可读组件，评委可以逐项质疑。

**但是——这是本章最重要的一句——当前数据没有证明 multiplicative 是唯一正确或最优结构。**

`experiments/model_tournament/final/model_selection_evidence.md` 的审计结论是 **`NO_SINGLE_DOMINANT_MODEL`**：

> "Safety-oriented abstention favors the gated rule; raw-score closeness favors additive lambda=0.5; transparent reliability attenuation and explicit missing-evidence status favor the current multiplicative structure. A formal selection claim must wait for common human labels, an outcome holdout, common perturbation/missingness masks, and completed pending challengers."

`experiments/model_tournament/baselines/baseline_comparison.md` 进一步指出一个**直接的模型必要性限制**：

> "the currently readable development evidence has no factor heterogeneity, so the main candidate's extra multiplicative complexity cannot be validated against a simpler additive or rule model using current observed outcomes."

同一文件对"简单线性模型能否达到类似效果"的回答是：**Yes in this slice**——Baseline B 在当前切片上得到与主模型相同的分数与全部 70 条状态决策，只是 support mass 为 8 而非 6；"The data do not adjudicate 8 versus 6; claiming the main product form is necessary would overstate the evidence."

因此本文的立场是：**乘法结构因研究问题对齐、透明性、显式缺失证据语义与可审计性而被保留，不因经验优越性而被保留。** §9.1 的 Alternative Formulations 是对这一选择的结构性检验，不是模型冠军赛。

### 6.3 为什么参数是"声明的假设"而不是"学到的最优值"

`λ_prompt = 0.5`、`λ_context = 0.5`、`r_medium = 0.75` 是**冻结的声明参数**，不是拟合结果。理由：

- 当前只有 16 条可判读记录，且全部同质（§3.4），任何"学习"出的参数都只是对同一常数因子的重述，不具备识别力；
- 无独立 holdout、无 human truth，无法定义损失函数进行有意义的优化；
- OECD/EU/EC-JRC (2008) 与 Saisana et al. (2005) 的复合指标方法论明确要求：权重、补偿性与聚合方式是价值/模型选择，必须公开并做多方案比较，而不是伪装成数据驱动结果。

因此本文采取的替代方案是：**公开参数 + 敏感性检验**。§8.3 报告 ±10% / ±20% 单变量扰动与 693 格声明网格的结果；§9.1 报告替代函数形式的行为差异。这是"我们无法证明参数正确，但我们可以证明结论不是某个参数点碰巧产生的"。

### 6.4 fail-closed 而不是 fail-open

`I(observable_i)` 的设计是 fail-closed：不可判读 ⇒ 权重为 0 ⇒ 不产生分数。反过来的选择（fail-open：不可判读时给一个保守的低分）会把"没有证据"与"证据表明表现低"混为一谈，这正是 §3.3 要防止的。

`robustness_validation_summary.md` §5 把这条边界称为"the clearest refusal boundary"：54/70 记录没有有效证据。§8.4 的 P072 案例进一步显示 fail-closed 的一个非平凡性质：**仅恢复上下文不会制造证据**——P072 在只恢复 context 的受控变体下仍然是 `NO_EFFECTIVE_EVIDENCE`，因为 Student Evidence 仍是 `UNDETERMINED`，observable gate 仍然关闭。

### 6.5 保留主模型的六条理由（problem-alignment decision）

1. **transparency（透明性）**：评委能看到 `Raw → Reliability → Adjusted → Support → Decision` 每一步为什么发生，而不是一个黑盒分数。
2. **auditability（可审计性）**：每个最终决策都能追溯到输入证据与可靠性权重。
3. **explicit evidence support**：显式记账"这条证据有多少支撑"，而不是把所有 observation 当成等价信息。
4. **missing-evidence semantics**：明确区分"没有证据"（`NO_EFFECTIVE_EVIDENCE`）与"有证据但支持较弱"（`LOW_SUPPORT`）。
5. **abstention semantics**：允许模型在证据不够时拒绝过度判断。
6. **research-question alignment**：Main RQ 问的是"如何避免把 Raw 当结论"，主模型的结构直接回答这个问题。

这六条**没有一条**是"它的观测指标更高"。`baseline_comparison.md` 明确写：主模型的 "empirical superiority is **not demonstrated**"，保留它的理由是 "transparency of support decomposition and future testability, not a higher observed metric"。

---

## 7. Validation Design

### 7.1 一个 Main RQ，五条 Validation Questions

本文不建立五个并列研究问题。全部实验都是对 §1.5 那**一个** Main RQ 的验证路径。统一命题是：

> 如果 Raw Signal 与证据支持被混为一谈，系统会在弱证据、缺失证据或不同信息质量下给出过度确定的评价；可靠性层能把这条差异显式化，并允许拒判。

**Table 7-1　Main RQ 与五条 Validation Questions**

| | 攻击的质疑 | 一句话问题 | 证据来源 |
|---|---|---|---|
| **Main RQ** | — | 当观测证据缺失/冲突/可信度不一时，如何避免把 Raw Signal 当可信结论，并显式报告 Reliability、Support/Coverage，且允许 ABSTAIN？ | 全文 |
| **VQ1** Baseline | "Reliability 层其实没必要" | 如果完全不建模 Reliability，会发生什么？ | `experiments/model_tournament/baselines/baseline_comparison.md` |
| **VQ2** Ablation | "公式里的组件只是装饰" | 模型组件是否真正改变证据支撑？ | `reports/development/ablation_results.csv` |
| **VQ3** Sensitivity / Robustness | "结果只是某个参数点碰巧调出来的" | 结论在参数局部变化下是否保持？ | `reports/robustness/parameter_perturbation_summary.json`；`reports/verification/independent_bounds_summary.json` |
| **VQ4** Failure / Counterexample | "遇到最困难的记录时模型就没用了" | 高 Raw 是否仍被无条件接受？缺失证据是否被填成 0？ | `outputs/final_results.json::counterexamples`；`reports/development/counterexamples.csv` |
| **VQ5** Structural Portability | "模型只是为当前教育数据硬写的" | 同一结构能否在性质完全不同的 Raw Signal 上运行？ | `experiments/transfer_finance/transfer_validation.json`；`information_missing_validation.json` |

此外，两类对照（**不是** VQ，是 challenger）回答"为什么主模型被保留"：

| 对照 | 攻击的质疑 | 证据来源 |
|---|---|---|
| Alternative Formulations | "主结论只依赖你这一个公式" | `experiments/model_tournament/formulations/formulation_results.json`；`final/model_selection_evidence.md` |
| ML Challenger | "更灵活的数据驱动模型足以替代你的可解释框架" | `experiments/model_tournament/ML_CHALLENGER_HANDOFF.md`；`ml_results.json` / `.csv` |

### 7.2 每条路径的报告格式

本文对每条验证路径统一报告五段，便于答辩追问：

> **WHY**（为什么做这个检验，它回应哪个质疑） → **SETUP**（真实设置与参数） → **RESULT**（如实数字，含负结果） → **SUPPORTED**（这个结果支持什么） → **NOT SUPPORTED**（这个结果**不能**支持什么）。

### 7.3 验证设计的两条纪律

1. **不依赖任何单一实验。** 五条路径从不同方向攻击同一命题；任何一条被推翻，其余仍能界定结论边界。
2. **负结果必须保留。** External Transfer 的 Gate3（NOT SUPPORTED）、Alternative Formulations 的 `NO_SINGLE_DOMINANT_MODEL`、ML Challenger 的 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`、以及"当前 0 条 ACCEPT"全部如实进入正文，不移入附录、不淡化。

---

## 8. Results

本章围绕 Main RQ 组织，**不按实验时间顺序**。每节回答一个 VQ。

### 8.1 Evidence availability reveals why Raw-only evaluation is risky（VQ1 — Baseline）

**WHY**：检验"如果完全不建模 Reliability，会发生什么"。这是对 Main RQ 最直接的攻击——如果 Raw-only 已经够用，本文的整个框架就没有必要。

**SETUP**：四个候选在**完全相同的 70 条记录**上运行，无拟合模型参与：

- **A Raw-only（M0）**：一个 observable gate + 均值，不做任何校正；
- **B Simple Linear**：三项加法折减 + 裁剪，每条可判读记录权重 0.5；
- **C Rule-based (gated)**：一个 observable gate + 固定的 L4/confidence/risk 决策规则，无 graded support measure；
- **Current Model（M3）**：三因子乘法 + 加权聚合 + 状态阈值。

**RESULT**：

**Table 8-1　Baseline 对比（同 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录）**

| Model | Aggregate Score (ABL) | HOT / Gap | Support Mass | Coverage（分母 N = 70） | 决策语义 `SUPPORTED / LOW / NEE` | Role |
|---|---:|---:|---:|---:|---:|---|
| A Raw-only | 3.5625 | .375 / 1.125 | 16.0 | 0.228571 | **16** / 0 / 54 | 必要 baseline |
| B Simple Linear | 3.5625 | .375 / 1.125 | 8.0 | 0.114286 | 0 / 16 / 54 | 更简单的加法对照 |
| C Rule-based (gated) | 3.5625 | .375 / 1.125 | 16.0（raw mass） | 0.228571 | 0 / 16 / 54 | 拒判安全对照 |
| **Current Model (M3)** | 3.5625 | .375 / 1.125 | **6.0** | **0.085714** | 0 / 16 / 54 | 主模型 |

补充的压力测试（同一 canonical 文件 `baseline_comparison.md`，如实呈现，包括对主模型不利的部分）：

| 维度 | 结果 |
|---|---|
| Main metric | 四者全部 3.5625；**主模型在观测分数上没有任何优势** |
| 七条记录 prompt-flag flip 响应性 | 主模型 score +0.133152、coverage +0.0375，翻转 7 个状态；B +0.078526、+0.025，翻转 7 个；A 与 C 的 score/coverage 不变，C 翻转 4 个，A 翻转 0 个。原文标注：这测量的是 **responsiveness, not correctness** |
| Evidence 层级 ±1 噪声扰动 | 四者 score 均为 3.5，状态翻转 0；flag-flip 贡献序稳定性（Kendall-like sign concordance）：主模型 **0.7474**、A **1.0**、B **0.9540**、C **1.0** |
| Missing evidence | 四者对 54/70 行都返回 `NO_EFFECTIVE_EVIDENCE`——这是**共享**的 observability 规则，不能单独记功于 Reliability 层 |
| Accuracy / classification sensitivity | `NOT_COMPUTABLE_NO_HUMAN_TRUTH`（对每个候选都是）；accepted error 与 risk–coverage improvement 同样未测 |
| External transfer 用于比较 | `NOT_SUPPORTED_FOR_COMPARISON`：金融研究改变了 signal、reliability 与 target，无匹配的教育 baseline 或 human truth，不能在此选出 winner |

**SUPPORTED**：

- Raw-only **缺少 graded support semantics**：它把 16 条可判读记录全部按满权重（`w = 1`）计入，并把它们标为 `SUPPORTED`。P108（Evidence L6、prompt-induced、medium confidence）在 Raw-only 下获得满支持——它没有任何通道可以报告"证据等级"与"证据质量"的区别。这是**结构性限制**，不是测得的准确率失败。
- Reliability 层带来 Raw-only 没有的东西：一个**独立的、连续的支持量**（`16 → 6`，coverage `0.228571 → 0.085714`，分母 70），以及"高 Raw 层级仍可能低支持"的解释能力。
- **所有 aggregate score 相同本身是研究结果**，不能隐藏。它来自 §3.4 的公共缩放退化，既不是精度等价，也不是任何公式有效的证据。

**NOT SUPPORTED**：

- **不得**写成"主模型 accuracy 更高"或"主模型精度优越"——四者同分，且无 human truth，`NOT_COMPUTABLE_NO_HUMAN_TRUTH`。
- **不得**写成"Raw-only 是错误的"。它是**必要 baseline**，只是不能完整回答 Main RQ。
- **不得**声称乘法形式是必需的。B（简单线性）在当前切片上得到相同分数与**全部 70 条相同的状态决策**，support mass 为 8 而非 6；"The data do not adjudicate 8 versus 6"。
- **不得**把 missing-evidence 拒判单独记功于 Reliability 层——四个候选共享该规则。
- 主模型对 flag 扰动的更高响应性"could be desirable caution or unwanted instability"，需要独立人工验证与异质案例才能判定。

### 8.2 Reliability changes support accounting even when normalized score remains unchanged（VQ2 — Ablation）

**WHY**：检验模型中哪些组成部分真正改变了支持记账与决策语义，回应"公式里的 Reliability / Gate 模块只是装饰"这一质疑。

**SETUP**：从 M0 到 M3 逐步加入组件，同一确定性模型、同一 70 条记录（`reports/development/ablation_results.csv`；`outputs/final_results.json::ablation[]`）。

**Table 8-2　Ablation（M0 → M3）**

| Model | Components | λ_prompt | λ_context | conf. weighting | Score (ABL / HOT / Gap) | Effective Weight | Coverage（分母 N = 70） | included |
|---|---|---:|---:|---|---:|---:|---:|---:|
| M0 | 无校正 | 0.0 | 0.0 | False | 3.5625 / 0.375 / 1.125 | **16.0** | **0.228571** | 16 |
| M1 | + confidence | 0.0 | 0.0 | True | 3.5625 / 0.375 / 1.125 | **12.0** | **0.171429** | 16 |
| M2 | + confidence + prompt | 0.5 | 0.0 | True | 3.5625 / 0.375 / 1.125 | **6.0** | **0.085714** | 16 |
| M3 | + confidence + prompt + context | 0.5 | 0.5 | True | 3.5625 / 0.375 / 1.125 | **6.0** | **0.085714** | 16 |

**RESULT**：有效权重 **16 → 12 → 6 → 6**；有效覆盖率 **0.228571 → 0.171429 → 0.085714 → 0.085714**；归一化分数**始终保持 3.5625 / 0.375 / 1.125 不变**；`included_evidence_count` 恒为 16；四者 status 均为 `DEFINED`。

- M0→M1：confidence 折减（0.75）使 16 × 0.75 = 12.0；
- M1→M2：prompt 折减使 12.0 → 6.0，**prompt 模块承担当前切片的主要支持下降**；
- M2→M3：**context 模块在可判读记录中没有变异**（16 条全部 `context_truncated = false`），因此 M3 与 M2 完全相同。

**SUPPORTED**：

- 组件**确实改变 support accounting 与拒判边界**，而不是只出现在公式里。重点应放在 **16→12→6→6**，而不是只看 3.5625 恒等。
- **Score stability 不代表 Evidence support stability。** 这正是本文的核心结论在同一份数据上的第二次独立显现（第一次是 §8.1 的四模型同分不同支持）。
- 因此**不能把 score 不变写成"性能稳健"**。分数不变是公共缩放的算术后果；支持量变化才是模型在做的事。

**NOT SUPPORTED**：

- **不得**把模块差异解释成**独立因果效应**。
- **不得**声称 context "已证明无作用"。M2 = M3 的原因是**数据缺变异**，`λ_context` 的作用在当前切片**不可识别**（`NOT_IDENTIFIED`），只能作 sensitivity-only 情景。
- **不得**由 included 恒为 16 推断"纳入的记录集合稳健"——纳入集合由 observable gate 决定，与可靠性参数无关。

### 8.3 The finding persists under local parameter variation（VQ3 — Sensitivity / Robustness）

**WHY**：检验结论是否只是某个参数点碰巧产生的，回应"结果只是调参调出来的"这一质疑。

**SETUP**：两部分。

1. **单变量扰动**：在默认 `λ_prompt = 0.50`、`λ_context = 0.50`、`r_medium = 0.75` 上，对三个参数分别做 ±10%、±20% 的 one-at-a-time 扰动，共 **15 个条件**（`outputs/final_results.json::sensitivity.rows`，15 行；`reports/robustness/parameter_perturbation_summary.json`）。
2. **声明参数网格**：`λ_prompt ∈ [0, 1] step 0.05`（21 值）× `λ_context ∈ [0, 1] step 0.1`（11 值）× `r_medium ∈ {0.5, 0.75, 1.0}`（3 值）= **693 格**（`independent_bounds_summary.json::parameter_space`）。

**RESULT**：

**Table 8-3　单变量扰动（15 条件）**

| 参数 | 变化 | 取值 | Δ mean reliability | Δ adjusted score | 状态翻转 | 核心结论翻转 |
|---|---|---:|---:|---:|---|---|
| λ_prompt | −20% / −10% | 0.40 / 0.45 | +0.017143 / +0.008571 | 0.0 / 0.0 | 否 | 否 |
| λ_prompt | baseline | 0.50 | 0.0 | 0.0 | 否 | 否 |
| λ_prompt | +10% / +20% | 0.55 / 0.60 | −0.008571 / −0.017143 | 0.0 / ≈0（−4.4e−16） | 否 | 否 |
| λ_context | −20% … +20% | 0.40 – 0.60 | **全部 0.0** | 全部 0.0 | 否 | 否 |
| r_medium | −20% / −10% | 0.60 / 0.675 | −0.017143 / −0.008571 | ≈0（−4.4e−16）/ 0.0 | 否 | 否 |
| r_medium | baseline | 0.75 | 0.0 | 0.0 | 否 | 否 |
| r_medium | +10% / +20% | 0.825 / 0.90 | +0.008571 / +0.017143 | 0.0 / 0.0 | 否 | 否 |

- **15 个扰动条件产生 0 个 decision-state 翻转**（`total_status_flips = 0`；`evaluation_status_changed = false`、`core_conclusion_changed = false` 全部为 false）；
- 归一化分数保持 **3.5625**（±20% 处出现 1e−16 量级浮点残差）；
- 基线状态分布保持 **16 `LOW_SUPPORT` + 54 `NO_EFFECTIVE_EVIDENCE`**；
- 最大平均绝对可靠性变化 **0.017143**，最大记录级变化 **0.075**；
- 学生级 ranking：**`NOT_APPLICABLE`**（`total_ranking_changes = "NOT_APPLICABLE"`）；`structural_collapse = false`；
- **λ_context 的扰动完全 inert**（Δ reliability = 0），原因见 §3.4：可判读记录没有 context 变异。

**Table 8-4　693 格声明网格（`independent_bounds_summary.json`；`core_numbers_source_of_truth.json`）**

| 量 | 结果 |
|---|---|
| 网格规模 | **693** = 21 × 11 × 3 |
| defined / undefined | **660 defined / 33 undefined** |
| undefined 原因 | `NO_EFFECTIVE_EVIDENCE`（例如 λ_prompt = 1.0 时全部可判读记录权重归零，ABL/HOT/Gap = null） |
| ABL 范围 | 3.5625 – 3.5625（`ABL_all_defined_equal = true`） |
| HOT / Gap | 同样恒定（0.375 / 1.125） |
| **effective weight 范围** | **0.4 – 16.0**（中位数 5.8；q25 3.15；q75 8.85） |
| **effective coverage 范围** | **0.005714 – 0.228571**（中位数 0.082857；q25 0.045；q75 0.126429） |

**SUPPORTED**：

- **主现象不是单一参数点碰巧产生的。** 在整个 693 格声明网格内，归一化分数恒定，而有效支持跨 **0.4 – 16.0**（40 倍）、有效覆盖率跨 **0.005714 – 0.228571**（40 倍）。"分数稳定、支持变化"是**局部结构现象**，不是单点展示。
- 在 ±10% / ±20% 范围内，决策状态语义稳定（0 flips）。
- 支持为零时，模型返回 `NO_EFFECTIVE_EVIDENCE` 而非伪造分数——33 个 undefined 格正是这一 fail-closed 行为的体现。

**NOT SUPPORTED**：

- 这是**当前切片上的 local structural stability**，**不是**：
  - global robustness；
  - statistical confidence interval（693 是**有限声明网格**，不是抽样分布）；
  - universal stability；
  - parameter calibration（参数仍未被校准）。
- context 方向的平坦是**数据缺变异**，不是已证明"λ_context 无作用"。
- 0 个状态翻转的原因之一是：所有可判读记录共享同一基线权重 0.375，局部扰动不足以跨越状态阈值（`robustness_validation_summary.md` §5）。这**削弱**而非增强"状态稳定"的分量，必须写明。
- 学生级 ranking 为 `NOT_APPLICABLE`：本文**不产生任何学生排名**。

**Figure 3（F3 Evidence Degradation）**：
- **Question**：受控地改变单个证据字段，模型如何响应？
- **Result**：P108（L6、prompt-induced、medium）在**假设**移除 prompt 风险时，R 从 0.375 → 0.750、adjusted 从 2.25 → 4.50、状态从 `LOW_SUPPORT` → `DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`；把 confidence 降到 low 时，R → 0.250、adjusted → 1.50，保持 `LOW_SUPPORT`；P072 在**仅恢复 context** 时仍为 `NO_EFFECTIVE_EVIDENCE`（Student Evidence 仍 `UNDETERMINED`）。
- **Meaning**：模型对证据质量的变化有方向性响应；但"恢复上下文不会制造证据"——observable gate 是硬约束。**这是对假设输入字段变化的机械响应，不是真实观测，也不是因果效应。**
- 路径：`yu/reports/visual_evidence/final/F3_evidence_degradation.svg`。

**Figure 4（F4 Parameter Perturbation）**：
- **Question**：Score 稳定 vs Support 变化，能否在同一张图上被看见？
- **Result**：局部 ±20% 扰动下 support 移动而记录到 0 次状态翻转；ranking `NOT_APPLICABLE`；有限网格**不是**置信区间；context 平坦在此切片为 `NOT_IDENTIFIED`。
- **Meaning**：这是核心结论（Score Stability ≠ Evidence Support Stability）最直接的视觉证据（对应 Claim C3、C5、C8）。
- 路径：`yu/reports/visual_evidence/final/F4_parameter_perturbation.svg`。

### 8.4 Failure cases show when the framework should abstain（VQ4 — Failure / Counterexample）

**WHY**：检验模型在最困难记录上的行为，回答"高 Raw 是否仍被无条件接受""缺失证据是否被填成 0"。只使用真实存在的案例。

**SETUP**：从 70 条开发记录中选取四类边界案例（`outputs/final_results.json::counterexamples`、`::development_results.explain_records`；`reports/development/counterexamples.csv`）。

**Table 8-5　真实失败 / 边界案例**

| 记录 | Case type | Raw Evidence | Risk factor | Reliability `w_i` | Adjusted 贡献 | 决策状态 |
|---|---|---|---|---:|---:|---|
| **P108** | Case_B_raw_score_low_support | **L6（最高，raw = 6.0）** | `prompt_induced` | **0.375** | **2.25** | **`LOW_SUPPORT` / `ABSTAIN`** |
| **P105** | Case_A_high_task_prompt_risk | L2（raw = 2.0）；Task 层级 L5 看起来高而 Student Evidence 为 L2 | `prompt_induced` | 0.375 | **0.75** | `LOW_SUPPORT` |
| **P072** | Case_C_context_truncated | 不可判读（Task L4，Evidence `UNDETERMINED`，context 截断） | `prompt_induced; context_truncated; low_confidence` | **0.0** | —（null，**不填 0**） | **`NO_EFFECTIVE_EVIDENCE`** |
| **P035** | Case_D_low_confidence_context_risk | 不可判读（Task L6，Evidence `UNDETERMINED`，low confidence，context 截断） | `prompt_induced; context_truncated; low_confidence` | **0.0** | —（null，**不填 0**） | **`NO_EFFECTIVE_EVIDENCE`** |

（`decision_reason`：P108/P105 = "confidence/prompt/context correction lowers contribution"；P072/P035 = "student_evidence_bloom is not L1-L6"。）

**RESULT**：

- **P108** 的 Raw 达到最高层级 L6，但因为携带 prompt 诱导风险且置信度仅为 medium，可靠性只有 0.375，adjusted 贡献被降为 2.25，决策为 `LOW_SUPPORT` / `ABSTAIN`，**而非满额接受**。在 Raw-only 基线下，同一条记录会获得 `w = 1` 的满支持并被标为 `SUPPORTED`（§8.1）——这是两个框架最尖锐的分歧点。
- **P105** 展示了另一种冲突：任务层级看起来是 L5，但支撑它的学生证据只有 L2。框架保留 Evidence L2 并降权（0.75），而不是让任务层级"抬升"证据层级。
- **P072 / P035** 因证据不可判读返回 `NO_EFFECTIVE_EVIDENCE`，模型**拒绝为其编造分数**（`adjusted_score = null`，不是 0）。

**SUPPORTED**：

- **High Raw ≠ High Evidence Support.** P108 是这一命题的具体实例。
- **Missing Evidence ≠ Zero Performance.** P072 / P035 是这一命题的具体实例。
- 框架在"高 Raw + 弱支持"与"任务层级高 + 学生证据低"两种冲突下都给出可审计的降级理由，而不是静默接受。

**NOT SUPPORTED**：

- 这是**结构性案例**，不是准确率或真实错误率。
- **没有独立 true outcome**，因此无法检验 abstain 之后是否"正确"。**不得**写成"模型预测正确"或"ABSTAIN 后实际正确"（`OUTCOME NOT AVAILABLE`）。
- **不得**由此推断总体错误率、误判率或任何频率量。
- 案例是 development example，标签为 `AI_PROVISIONAL`；它们不是人工确认的典型错误。

**Figure 2 / Figure 5** 承载本节的可视化（见 §5.2、§5.5）。

### 8.5 Alternative and ML challengers do not establish a single dominant model

**WHY**：在给出核心结论前，先回答两个"你的结论是不是只是因为你选了对自己有利的方法"的质疑。详细设计见第 9 章，本节只陈述结果对 Main RQ 的意义。

**RESULT（摘要）**：

- **Alternative Formulations**（乘法 A / 加法 B / 门控 C / 非线性 D）：审计结论为 **`NO_SINGLE_DOMINANT_MODEL`**。B（λ = 0.5）最接近 Raw（RMSE vs Raw = **0.3125**，为四者最小）；C（τ = 0.5）拒判最激进（16 条可判读记录**全部 ABSTAIN**，`defined_n = 0`）；D 引入额外 nonlinear sensitivity（γ = 0.5/1.0/2.0 时 mean output 分别为 2.1816 / 1.3359 / 0.5010）。**没有任何一个公式在拟合、安全、覆盖、可解释、迁移、复杂度上全面胜出。**
- **ML Challenger**（LogReg / depth-2 Tree / exploratory RF）：重复 4 折 CV × 25 = 100 折下 accuracy 分别约 **0.876 / 0.919 / 0.922**，但特征缺失 20%/40% 后降到约 **0.71–0.81**，RF 跨学期（2026春→2025秋）仅 **0.588**。结论为 **`INSUFFICIENT_FOR_STRONG_ML_CLAIM`**。

**SUPPORTED**：核心结论（Score Stability ≠ Evidence Support Stability）**不依赖单一公式**，也不依赖"手工模型打败了 ML"这一类叙事。它是一个在多种规范下都能被观察到的结构现象。

**NOT SUPPORTED**：

- **不得**写 "ML failed"，也**不得**写 "Current Model defeated ML"——二者都没有被证明更优（`winner unselected`）。
- **不得**选出"最佳"公式或"最佳"阈值 τ / γ / λ。
- **不得**把 CV 指标当作正式验证或泛化证据。

---

## 9. Challenger Models and Alternative Specifications

本章展开 §8.5 的两类对照。它们的共同作用是**挑战主结论是否依赖单一方法选择**，不是 Model Winner Tournament。

### 9.1 Alternative Formulations（替代函数形式）

**WHY**：检验当前结论是否只依赖某一个具体公式。如果换掉函数形式后主现象消失，那么结论就是公式的产物而非证据结构的产物。

**SETUP**：协议在查看候选结果**前**冻结（`formulation_results.json::preregistration`："A fixed; B lambda in [0.5,1.0]; C threshold=0.5; D gamma in [0.5,1.0,2.0]"，`tuning: none`），R 扰动固定为 {0.0, 0.5, 0.8, 1.0, 1.2}，输入为同一份 70 行 `AI_PROVISIONAL` 文件。

**Table 9-1　四种函数形式（sample-in，n = 70，raw_observed = 16，missing_evidence_n = 54）**

| Model | Formula | 新增参数 | `R → 0` 行为 | defined_n | abstain_n | mean output | RMSE vs Raw | rank stability vs Raw |
|---|---|---|---|---:|---:|---:|---:|---:|
| **A 乘法** | `S_raw × R` | 无 | `S_adj → 0` | 16 | 0 | **1.3359375** | 2.4156 | **1.0** |
| **B 加法** | `S_raw − λ(1−R)` | λ ∈ {0.5, 1.0} | 保留 `S_raw − λ` | 16 | 0 | 3.25（λ=.5）/ 2.9375（λ=1） | **0.3125**（λ=.5，最小）/ 0.625（λ=1） | 1.0 |
| **C 门控** | `R < τ ⇒ ABSTAIN` | τ = 0.5 | `ABSTAIN` | **0** | **16** | null | null | null |
| **D 非线性** | `S_raw × R^γ` | γ ∈ {0.5, 1.0, 2.0} | `S_adj → 0` | 16 | 0 | 2.1816 / 1.3359 / 0.5010 | 1.4981 / 2.4156 / 3.3214 | 1.0 |

**关键分歧案例：P108（Raw = L6 = 6.0，R = 0.375）**

| Model | P108 输出 | 状态 |
|---|---:|---|
| A 乘法 | **2.25** | `DEFINED` |
| B 加法 λ=0.5 | **5.6875** | `DEFINED` |
| B 加法 λ=1.0 | **5.375** | `DEFINED` |
| C 门控 τ=0.5 | null | **`ABSTAIN`** |
| D 非线性 γ=0.5 | 3.6742 | `DEFINED` |
| D 非线性 γ=1.0 | 2.25 | `DEFINED` |
| D 非线性 γ=2.0 | 0.84375 | `DEFINED` |

P072 / P035 在**全部四种形式**下都是 `NO_EFFECTIVE_EVIDENCE`（缺失证据语义是共享的，不是乘法的独有优点）。

**RESULT**：

- **B 可以更接近 Raw**（RMSE 最小 0.3125），但在高 Raw + 低 R 时仍保留很高输出（P108 → 5.6875）：加法惩罚是 **score-scale dependent** 的，这正是它的失败模式。
- **C 拒判更激进**：16 条可判读记录全部 ABSTAIN（`defined_n = 0`，`coverage_observed = 0.0`）。安全性最高，但当前切片下不提供任何连续 Adjusted Score。
- **D 引入额外 nonlinear sensitivity**：γ 从 0.5 到 2.0，P108 输出从 3.6742 变到 0.84375，而 γ 在当前数据上**不可识别**。
- **A 的优势主要是**：解释简单、`R → 0` 行为清晰、missing-evidence 语义清楚、容易审计、**无额外参数**。

**SUPPORTED**：

- 主现象（分数稳定而支持下降、缺失证据不填 0）在**多种函数形式下都存在**，因此不是乘法公式的产物。
- 不同形式在弱证据下的行为**实质不同**（`formulation_results.json` 的分析结论），因此"选择哪种形式"是一个必须公开的建模决定，而不是无关紧要的技术细节。

**NOT SUPPORTED**：

- **`NO_SINGLE_DOMINANT_MODEL`**——不得选出"最佳"公式或阈值。`model_selection_evidence.md` 明确写：安全导向的拒判偏好 gated rule；接近 Raw 偏好 additive λ=0.5；透明的可靠性衰减与显式缺失状态偏好当前乘法结构。这是 **operating-condition choice，不是 universal champion**。
- 不得声称某公式在预测或因果上更优。
- 审计同时指出比较是**不完整的**：没有 formal holdout label、没有 Human Gate PASS、没有共同 outcome target、没有 parameter-resampling report。因此任何"正式选择声明"都必须等待共同人工标签、outcome holdout、共同的扰动/缺失掩码与已完成的 pending challengers。

### 9.2 ML Challenger（机器学习挑战者）

**WHY**：回答"更灵活的数据驱动模型是否足以替代当前可解释框架"。**目标不是找冠军。**

**SETUP**（`ML_CHALLENGER_HANDOFF.md`；`ml_protocol.md`）：

- **代理目标**：一条 `AI_PROVISIONAL` 记录**是否获得可判读 Student Evidence**（16 positives / 70 Gate records）。这**不是** learning gain、不是 AIV、不是 causal AI effect、不是 human truth。
- **模型**：Logistic Regression（class-balanced，C = 1，max 2000 iter）；Shallow Decision Tree（class-balanced，max_depth = 2，min_samples_leaf = 5）；Random Forest **exploratory**（100 trees，max_depth = 3，min_samples_leaf = 4；exploratory 因为正例只有 16 条）。
- **未运行**：其他模型、超参搜索、AutoML、神经网络、XGBoost 搜索或任何优化。
- **特征**：pre-label 特征为文本长度、agent/speaker confidence、context truncation、semester、length stratum、question form、surface Bloom cue、path case；**label-derived 字段被排除**。
- **协议**：重复分层 4 折 CV × 25 repeats = 100 folds/model；固定 4 折缺失压力测试（20% / 40% feature mask，非额外训练或调参）；内部跨学期迁移（同一 70 条来源内的 cohort transfer，**不是**外部验证）。

**Table 9-2　重复交叉验证（mean ± fold SD，100 folds/model）**

| Model | Accuracy | Balanced acc. | F1 | ROC-AUC | Brier | Log loss |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | **0.875915** ± 0.072783 | 0.862541 ± 0.092290 | 0.757802 ± 0.130937 | 0.953915 ± 0.044753 | 0.090794 ± 0.035439 | 0.317908 ± 0.108382 |
| Shallow Decision Tree | **0.919444** ± 0.058611 | 0.901195 ± 0.114824 | 0.814726 ± 0.176275 | 0.913942 ± 0.106858 | 0.073493 ± 0.055742 | 1.075900 ± 1.895063 |
| Random Forest (exploratory) | **0.922190** ± 0.066379 | 0.894245 ± 0.113757 | 0.823291 ± 0.168200 | 0.928352 ± 0.085920 | 0.123528 ± 0.023253 | 0.416854 ± 0.050383 |

**Table 9-3　测试时特征缺失压力测试（固定 4 折）**

| 条件 | Logistic acc. | Tree acc. | RF acc. |
|---|---:|---:|---:|
| Clean | 0.871429 | 0.900000 | 0.871429 |
| 20% missing | 0.785714 | 0.814286 | 0.800000 |
| 40% missing | 0.714286 | 0.714286 | 0.742857 |

⇒ 缺失后准确率降到约 **0.71 – 0.81**。

**Table 9-4　内部跨学期迁移（同一 70 条开发来源，非外部验证）**

| Train → Test | Logistic | Tree | RF |
|---|---:|---:|---:|
| 2025秋 → 2026春 | 0.833333 | 0.888889 | 0.916667 |
| 2026春 → 2025秋 | 0.970588 | 0.941176 | **0.588235** |

⇒ **RF cross-semester = 0.588**（2026春→2025秋），迁移不稳定。

**RESULT**：表面 CV 判别指标不低（0.876 / 0.919 / 0.922），但：

1. **positive = 16**，且是 AI provisional **代理标签 ≠ human truth**；
2. 重复 CV 是对**同一 70 条记录**的重复重采样，**不是独立证据**；
3. 无 true validation / holdout；无 external labeled transfer（其余 70 条 Pilot 记录**未标注**）；
4. 特征缺失 20%/40% 后降到约 **0.71–0.81**；
5. RF 跨学期 **0.588**，不稳定；
6. 可解释性证据（logistic 系数、tree 规则、RF importance）是**关联，不是因果**；shallow tree 的主导规则使用标准化文本长度与 context truncation；RF 最大 importance 为文本长度与 context truncation；
7. 高置信分歧案例（P051 预测可判读而 provisional target 不可判读；P024 相反）**不是 human-label errors**。

**结论：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`、`NO_SINGLE_DOMINANT_MODEL`。**

**SUPPORTED**：

- ML 是**有价值的 robustness challenger**：它证明"是否存在可判别模式"这一问题上，简单模型在代理目标上能取得不低的 CV 指标，因此本文不能声称"只有我们的框架能处理这批数据"。
- 手工模型与 ML 在**问题类型上不同**：ML challenger 是 **pre-label predictor**（预测哪条记录会被标为可判读），主模型是 **post-label support transformation**（拿到 Evidence 标签后做支持变换 + fail-closed 拒判）。二者不是同一件事，因此不构成直接替代关系。
- 主模型当前证据的不同之处：显式 support decomposition、effective coverage、fail-closed `NO_EFFECTIVE_EVIDENCE`。

**NOT SUPPORTED**：

- **不得**写 "ML failed" 或 "ML 被击败"；
- **不得**写 "Current Model defeated ML" 或 "handcrafted 模型优于 ML"——主模型的经验优越性**同样未被证明**；
- 不得把 CV 值转换为正式验证、formal predictive accuracy、对全部 140 条 Pilot 记录的泛化、校准的可靠性概率、Formal AIV、learning gain 或 causal AI effect；
- 不得声称 ML 可替代 Evidence Reliability Model；正式主模型**不变**。
- 正确的 study-level 状态是：**challenge completed, winner unselected**。

---

## 10. External Structural Validation（VQ5 — Structural Portability）

**WHY**：检验模型是否只是为当前教育数据硬写，回答"接口能否迁移到性质完全不同的 Raw Signal"。

**SETUP**：把 `Raw → Reliability → Adjusted → ACCEPT/ABSTAIN` 结构复用到一份 **BTC-USD 历史纸面模拟**上：

- 样本 **n = 1698**（日期范围 2021-01-30 至 2025-09-23，公开行情数据）；
- Raw Signal：`tanh(7-day close return / 0.05)`；
- Reliability：`0.30·completeness_30d + 0.30·agreement(3/7/14d) + 0.20·stability(rolling volatility) + 0.20·calibration(90d past hit rate)`；
- Adjusted：`raw_signal × R_market`，`abstain if R_market < 0.65`（**threshold = 0.65**，冻结）；
- 三个固定策略信号：**A 7-day momentum**、**B RSI14 mean reversion**、**C MA20/50 trend**；
- 证据身份：**`synthetic / controlled evidence; no live news feed`**，`DEVELOPMENT_ONLY`；
- information-missing 实验：在 fixed 条件外，分别施加 missing / delayed / conflicting / low-trust 四种证据降级。

**Table 10-1　三个 information-missing Gate（`information_missing_validation.json::gates`）**

| Gate | 判据 | 关键数字 | 结果 |
|---|---|---|---|
| **Gate1** | 信息质量/完整性下降 → Reliability 下降 | full mean **0.6027** → missing mean **0.4077**；median 0.600 → 0.405；paired n = 1698 | **SUPPORTED** |
| **Gate2** | 更低 Reliability → abstention 上升、coverage 下降 | coverage **0.3940 → 0.0012**；accept_n 669 → 2；abstain_rate 0.606 → 0.999 | **SUPPORTED** |
| **Gate3** | 低 Reliability 决策应有**更高** future error rate | low-R error **0.5248** vs high-R error **0.5277** | **NOT SUPPORTED** |

⇒ **`risk-coverage improvement = false`**（`outputs/final_results.json::transfer_validation.risk_coverage_improvement = "NOT_SUPPORTED"`；`transfer_validation.json::risk_coverage.supported = false`）。

**补充的 reliability separation（`transfer_validation.json::reliability_separation`，`supported = true`）**：按支持度三分组，各 n = 566，raw hit rate 分别为 low **0.4647** / medium **0.4735** / high **0.4841**，mean reliability 分别为 0.6202 / 0.7178 / 0.7920。

**三种策略的差异**：A / B 表现出有限的可靠性分离（high-R 组质量高于 low-R 组），**C 不表现出该排序**（`robustness_validation_summary.md` §4："A/B show high-R quality above low-R; C does not"；F6 图注："Strategy C reverses the ordering"）。selective decision gain 记为 **`PARTIAL`**。

**权重敏感性（`transfer_validation.json::sensitivity`，`supported = true`）**：completeness 权重 ±10% / ±20% 并重归一化后，Spearman reliability 相关 ≈ **1.0**（最低 0.9999999981616376），0.65 阈值下 accepted 数从 1241 到 1394。

**Figure 6（F6 External Structural Transfer）**：
- **Question**：教育结构能否迁移到性质不同的 Raw Signal？
- **Result**：A / B / C 三个策略的 low / medium / high reliability 分组；**Strategy C 反转了排序**。
- **Meaning**：这是来自 BTC 历史纸面模拟的**部分**结构迁移证据，**不是**教育验证，**不是**交易主张。
- 路径：`yu/reports/visual_evidence/final/F6_external_structural_transfer.svg`。

**SUPPORTED**：

- **External Structural Transfer（结构可迁移）**：同一接口能在性质完全不同的 Raw Signal 上运行，并在证据质量下降时降低 coverage、增加 abstention（Gate1、Gate2 SUPPORTED）。
- 说明本文的框架**不是只为当前教育数据硬写的**——这直接回应 VQ5 的质疑。
- 状态标签：`EXTERNAL_TRANSFER / DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`；`reliability_separation = PARTIAL`。

**NOT SUPPORTED（Gate3 的失败必须保留）**：

- **Gate3 NOT SUPPORTED**：低可靠性决策并**没有**带来更高的 future error rate（0.5248 vs 0.5277，实际上略低），因此"低 R ⇒ 高风险"这一 selective prediction 的核心预期在本数据上**未成立**，`risk-coverage improvement = false`。
- **不得**写 prediction improvement、prediction superiority；
- **不得**写 trading advantage 或 "trading strategy is profitable"（`trading_advantage = "NOT_SUPPORTED_CLAIM"`；`paper_use = "small external validation only; not a trading strategy"`）；
- **不得**写 universal generalization 或教育泛化；
- **不得**把它发展成论文第二主线——它是 synthetic/controlled 的**结构演示**，`overall_status = PASS` 仅指该结构演示按协议完成；
- baseline comparison 已判定 external transfer 为 `NOT_SUPPORTED_FOR_COMPARISON`：它改变了 signal、reliability 与 target，且无匹配的教育 baseline 或 human truth，**不能用来在候选模型间选出 winner**。
- 另有 Binance shadow 记录（`outputs/final_results.json::transfer_validation.binance_shadow`，其 source_artifact 指向 `experiments/transfer_finance/live_shadow/live_shadow_summary.json`，sample_size = 10）：`INDEPENDENT_PUBLIC_DATA_ONLY`、`private_api_required = false`、`trading_performed = false`、`main_model_parameters_modified = false`、`short_term_returns_in_main_conclusion = false`。本文**不**使用任何短期收益作为结论。

---

## 11. Discussion

### 11.1 为什么分数可以稳定而支持下降

这是全文需要解释清楚的核心机制，而不是需要掩饰的尴尬结果。

在当前切片上，16 条可判读记录**共享同一组因子取值**（`prompt = true`、`context = false`、`confidence = medium`）。因此任何可靠性加权方案都对每条被纳入的分数施加**同一个常数因子** `k`：

```
Score_adj = Σ (k · Raw_i) / Σ (k · w_i^0) = k · Σ Raw_i / (k · Σ w_i^0) = Σ Raw_i / Σ w_i^0
```

常数因子在归一化中**抵消**，所以 ABL / HOT / Gap 恒为 3.5625 / 0.375 / 1.125。但支持量 `S = Σ w_i` **不做归一化**，因此它直接随 `k` 缩放：16 → 12 → 6 → 6；693 格网格上跨 0.4 – 16.0。

**这不是 bug，这正是本文的论点。** 一个只看归一化分数的评价体系，在当前数据上**完全无法察觉**支撑它的证据已经从 16 个单位收缩到 6 个单位（覆盖率从 0.228571 收缩到 0.085714，分母 70）。分数看起来一样确定，证据的确定性已经下降了 62.5%。

`baseline_comparison.md` 对此的表述是："Score stability conceals the change from 16 raw contributions to 6 effective units under the main assumptions."

### 11.2 三条路径上的同一现象

核心现象在三条独立路径上反复出现，这是本文最强的证据形态——不是"实验数量多"，而是**同一条可复算链上的相互吻合**：

| 路径 | 分数 | 支持 | 现象 |
|---|---|---|---|
| Baseline（§8.1） | 四模型全部 3.5625 | 16 / 8 / 16(raw mass) / **6** | 同分，不同支持记账 |
| Ablation（§8.2） | 恒 3.5625 / 0.375 / 1.125 | **16 → 12 → 6 → 6** | 组件改变支持，不改变分数 |
| Sensitivity（§8.3） | 693 格全部 3.5625 | **0.4 – 16.0** | 分数恒定，支持大幅变化 |

独立复算（`independent_implementation = true`）与统一 source of truth 复现了 `70 / 16 / 19 / 35`、`693 / 660 / 33`、ABL/HOT/Gap 与 weight/coverage bounds；`run_all.py` 开发检查 32/32 PASS。

### 11.3 何时 ACCEPT、何时 ABSTAIN、何时 NO_EFFECTIVE_EVIDENCE

| 情形 | 输出 | 依据 |
|---|---|---|
| 证据可判读且支持充分 | `ACCEPT` | 分数有定义且满足声明的支持规则 |
| 证据可判读但支持弱/冲突（当前 16 条全部如此） | `LOW_SUPPORT` / `ABSTAIN` | 存在证据，但其支撑不足以支持确定性结论 |
| 证据不可判读或不存在（当前 54 条） | `NO_EFFECTIVE_EVIDENCE` | `Σw_i = 0`，不填 0 分 |

**当前切片下 0 条 ACCEPT。** 这一事实本身是有信息量的：它说明在 AI 提示诱导普遍存在、置信度普遍为 medium 的开发数据上，一个诚实的框架**不应该**给出确定性结论。把这个结果写成"模型没有用"是误读；把它写成"模型成功地拒绝了过度确定的判断"更接近事实，但同样必须与 coverage 一起报告，且不能声称它提高了准确率（无 true outcome）。

### 11.4 为什么保留当前主模型（重申，且限定）

主模型被保留是 **problem-alignment decision**，不是 **prediction-winner decision**（§6.5 的六条理由）。这里的限定必须重复一次，因为它是答辩最可能被追问的点：

- `baseline_comparison.md`：主模型的 empirical superiority is **not demonstrated**；在当前切片上 **B（简单线性）是一个 serious simpler challenger**，C 复现了全部 categorical decisions；保留主模型的理由是 "transparency of support decomposition and future testability, not a higher observed metric"。
- `model_selection_evidence.md`：**`NO_SINGLE_DOMINANT_MODEL`**，这是 operating-condition choice，不是 universal champion。
- `ML_CHALLENGER_HANDOFF.md`：challenge completed, **winner unselected**。

因此本文的模型选择声明只能是：**在当前研究问题与证据边界下，乘法结构因其透明性、显式缺失证据语义与可审计性而被保留；它没有被证明是最优的，也没有被证明优于更简单的替代方案。**

### 11.5 两个必须保留的削弱项

`research_story_summary.md` §7 明确列出两个削弱项，本文如实保留：

1. **16 条 readable 记录是同质幸存者**（homogeneous survivors）：它们之所以可判读，可能与其因子取值本身相关，这构成一种选择效应，当前无法量化。
2. **provisional 标签的生成脚本 / 逐行日志尚未完全闭合**：`AI_PROVISIONAL` 标签的可追溯性仍有缺口。

这两项都进一步限制了本文结论的强度，也是第 13 章 Formal Evidence Upgrade Protocol 要解决的对象。

---

## 12. Limitations and Claim Boundary

### 12.1 Limitations（当前证据边界的组成部分，不压缩）

| # | 限制 | 具体状态 |
|---|---|---|
| L1 | **输入是 AI provisional 标签** | 所有结果来自 `AI_PROVISIONAL / DEVELOPMENT_ONLY`，不能替代人工验证 |
| L2 | **Human R1/R2 未完成** | R1 = 0/70 VALID、R2 = 0/70，Formal Gate `NOT_RUN`。近期收到的一份标注文件已核验为同一 B 标签的派生副本（`filled_from_B`），**不是**独立 R1/R2，不能作为 test-retest 或 inter-rater 证据 |
| L3 | **Formal Gate NOT_RUN** | 正式可靠性系数、正式支持指标、Formal AIV 均未产生；`formal_gate_eligible = false` |
| L4 | **无 Outcome_AI / Outcome_baseline** | `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，不支持 causal learning gain |
| L5 | **可判读切片高度同质** | 16 条全部 `prompt=true / context=false / confidence=medium / task_actor=ai`；prompt、context、confidence、actor 的独立效应**不可识别** |
| L6 | **context 无变异** | `λ_context` 的作用在当前切片不可识别，扰动完全 inert，只能作 sensitivity-only 情景；**不得**写成"已证明 context 无作用" |
| L7 | **reliability 参数未被正式校准** | `c_i`、`λ_prompt`、`λ_context`、`r_medium` 是假设/敏感性参数，**不是**校准概率，`WEAKLY_JUSTIFIED_COMPONENT` |
| L8 | **无 true outcome** | 无法验证 abstain 之后是否"正确"；`accuracy_coverage_audit = NOT_RUN`，不能报告准确率提升 |
| L9 | **finance 仅 structural transfer** | synthetic/controlled 结构演示；**Gate3 NOT SUPPORTED**，`risk-coverage improvement = false`，no trading advantage claim |
| L10 | **ML strong claim unsupported** | `INSUFFICIENT_FOR_STRONG_ML_CLAIM`；16 positives、代理标签、无 holdout、缺失降级、跨学期不稳 |
| L11 | **no single dominant formulation** | `NO_SINGLE_DOMINANT_MODEL`，不能选出"最佳"公式；主模型的经验优越性未被证明，简单线性是 serious challenger |
| L12 | **复现边界** | `run_all.py` 32/32 只覆盖**开发版核心链路**，不覆盖 final artifact / figure / Paper / Demo 全链路 |
| L13 | **数据完整性 open defects** | 21/21 冻结不变量通过，但 `S4-F01`（未来内容泄漏）、`S4-F02`（非盲标队列）仍为 open，已从标注路径隔离 |
| L14 | **同质幸存者与标签可追溯性** | 16 条 readable 记录是同质幸存者；provisional 标签的生成脚本/逐行日志尚未完全闭合 |
| L15 | **样本范围** | 70 条是 Gate 核心样本，**不代表** Pilot V1 全量 140 条，更不代表总体；其余 70 条未标注；**不产生学生排名**（ranking `NOT_APPLICABLE`） |

### 12.2 Claim Boundary

**Table 12-1　可以说 / 不可以说**

| ✅ 本文可以说 | ❌ 本文不可以说 |
|---|---|
| Raw Signal 与 Evidence Support 是不同的量，应同时报告 | Adjusted Score / Support / Coverage 是 AI Increment、正式 AIV、真实学习增益或因果效果 |
| 在声明参数网格内，归一化 ABL/HOT/Gap 保持 3.5625 / 0.375 / 1.125，而有效权重 16→6、覆盖率 0.228571→0.085714 | 分数相同说明任何公式有效/等价/winner，或说明 accuracy parity / predictive superiority |
| Reliability 层能在开发版规则下降低弱证据的有效贡献，并保留 `NO_EFFECTIVE_EVIDENCE` / `ABSTAIN` 语义 | `R` 是校准概率、真实可靠度或能力估计 |
| 54 条返回 `NO_EFFECTIVE_EVIDENCE`，不填 0 | 54 条是 54 个 0 分；54 条是"预测错误" |
| ±10%/±20% 扰动产生 0 decision-state flips；693 格中 660 defined / 33 undefined | 这是统计置信区间、全局稳健性或参数已校准 |
| 当前模型的行为、消融路径、局部参数敏感性、困难案例与有限结构迁移均可复算 | 这些结果证明了形式有效性、因果效果或普适性 |
| External Transfer 显示 structural portability（Gate1/Gate2 SUPPORTED） | 教育泛化、交易优势、预测优越、universal generalization；Gate3 成立 |
| ML challenger 是有价值的 robustness challenge，结论 `INSUFFICIENT_FOR_STRONG_ML_CLAIM` | ML failed；ML 被击败；handcrafted 模型优于 ML；ML winner |
| Human Gate 尚未完成，正式验证 pending | Kappa / Alpha 已有正式结果；Formal Gate 已 PASS；AI provisional 标签可当人工标签 |
| 乘法结构因研究问题对齐、透明性与缺失语义被保留 | multiplicative model is best / 唯一正确 / 已被证明必需 |

**本文严格禁止出现的陈述**（逐条对应任务边界）：

- ❌ AI improves learning
- ❌ model improves accuracy
- ❌ multiplicative model is best
- ❌ Reliability is calibrated probability
- ❌ abstention improves correctness
- ❌ financial prediction improves / trading strategy is profitable
- ❌ 70 records represent the full population
- ❌ Human Gate passed

### 12.3 无法进入本文的 Claim（无 canonical source）

以下声明在 `PAPER_EVIDENCE_TRACE.md` 中被明确列为"无法进入论文"，本文全部不出现：

1. 任何「AI 增量 / 学习增益 / 因果效果」——`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，无合法 paired outcome；
2. 任何「准确率提升 / abstain 提高精度」——`accuracy_coverage_audit = NOT_RUN`，无 true outcome；
3. 任何「R 是校准概率」——`c_i / λ` 是假设参数，未外部校准；
4. 任何「主模型最优 / 胜出」——`NO_SINGLE_DOMINANT_MODEL`；
5. 任何「Kappa / Alpha 正式一致性」——Human Gate 未运行，test-retest（非 inter-rater）尚无结果。

---

## 13. Formal Human Validation Protocol (PENDING)

> **本章不是一个 Completed Validation Result，而是一个 Formal Evidence Upgrade Protocol。**
> 当前状态：`PENDING_REAL_HUMAN_R1_R2`；Formal Gate = `NOT_RUN`；`formal_gate_eligible = false`。

### 13.1 当前 Human Gate 状态（如实）

| 项 | 状态 |
|---|---|
| Human R1 | **0/70 VALID** |
| Human R2 | **0/70** |
| Formal Gate | **`NOT_RUN`** |
| `formal_gate_eligible` | **false** |
| `gate_report_generated` | false |
| reason | "No real human annotations have been returned yet. No reliability coefficient is computed (D008)." |
| AI_ASSISTED | 70/70（`DEVELOPMENT_ONLY`，**非**正式替代） |
| `human_validation_status` | `PENDING_REAL_HUMAN_R1_R2` |

### 13.2 设计类型必须写清楚

冻结设计是 **`single_annotator_test_retest`**，`inter_rater = false`。

**R2 是同一 annotator、间隔 ≥ 24h 的 test-retest 重测，不是 second independent annotator。** 因此：

- 它产生的是 **intra-rater test-retest reliability**，不是 inter-rater agreement；
- **不得**借用 Cohen (1960) / Krippendorff (2018) 的 inter-rater 口径来描述它（`CITATION_GAP` GAP-3）；
- 本文**不报告**任何 Kappa / Alpha 数值，因为尚无数据。

### 13.3 已就绪的部分（preregistered = true）

| 组件 | 路径 / 状态 |
|---|---|
| 标注澄清手册 | `docs/annotation/annotation_clarification_v0.1.1.md` |
| R1 工作表 | `data/annotations/human/pilot_worksheet_A.csv` |
| R2 重测工作表（≥24h 后） | `data/annotations/human/pilot_worksheet_A_retest.csv` |
| 答案键 | `data/annotations/_keys/pilot_worksheet_key.csv` |
| Gate 阈值 | `validation/gate_thresholds.json`（**preregistered**） |
| 生成命令 | `python src/run_s4_gate.py` |
| 已完成检查 | 21/21 完整性不变量通过；9 项 reliability self-tests 通过；2 个 open defects（S4-F01、S4-F02） |

### 13.4 边界纪律

- **Thresholds must be confirmed before viewing results**（阈值必须在查看结果前确认）；
- **AI prelabels must never be reported as human labels**（D007/D008）；
- 派生副本（`filled_from_B`）不得充当 R1/R2。

### 13.5 Gate 通过后能升级什么、不能升级什么

**能升级**：若同一标注者按冻结协议完成 R1、间隔 ≥24h 完成独立 R2，且 Formal Gate 通过，则可以把**标注 test-retest reliability** 及由此产生的**支持审计**升级为正式验证输入；本文当前所有 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 标签可以被替换为正式结果。

**不能升级**：**Gate PASS 不会自动识别 AI 因果增量。** 要讨论 `Delta_raw` 或正式 AIV，还需要：

1. 合法配对的 `Outcome_AI` / `Outcome_baseline`；
2. 独立 learning outcome（撤去 AI 后的后测、保持或迁移测验）；
3. 相应的识别设计（target trial 各要素：人群、处理、时间零点、结局、随访、estimand；Hernán & Robins, 2022）；
4. 充分的因子交叉支持（`prompt = false`、`context_truncated = true`、high/low confidence、非 AI actor），以识别 `λ_prompt`、`λ_context`、`r_medium` 的独立效应。

**方法储备（不声称已具备）**：若未来获得足够人工真值与可交换样本，Angelopoulos et al. (2024) 的 Conformal Risk Control 可把当前的启发式拒判阈值升级为有限样本风险控制；Guo et al. (2017) 的 ECE / reliability diagram 可检验 `c_i` 是否具备概率解释；Geifman & El-Yaniv (2017) 的独立校准集/测试集分离可为 τ 的选择提供依据。本文**不声称**已有 conformal guarantee、已校准概率或已优化阈值。

---

## 14. Conclusion

在存在缺失、冲突或低可信证据的系统中，应当把 observed score 与 evidence reliability / support **分开建模**，并在证据不足时允许 abstention。

在当前 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录和声明的参数范围内，Evidence Reliability 框架能够显式区分 Raw Performance 与 Evidence Support：

- 归一化分数（ABL / HOT / Gap = **3.5625 / 0.375 / 1.125**）保持稳定；
- 有效证据权重从 **16 降到 6**；
- 有效覆盖率从 **0.228571 降到 0.085714**（分母 N = 70）；
- 当 `Σw_i = 0` 时返回 **`NO_EFFECTIVE_EVIDENCE`**，而不是人为补成 0 分（54 条：19 `NO_EVIDENCE` + 35 `UNDETERMINED`）。

因此，本文的最强结论只能表述为：

> ## **Score Stability ≠ Evidence Support Stability**
>
> **分数稳定，不等于证据支持稳定。** 稳定的评分不意味着支撑该评分的证据同样稳定、充分或可信。

这是一条 **descriptive / structural conclusion**（Evidence Level 1）。它说明框架在当前开发切片上的行为与审计语义。

它**不**升级为 universal theorem，**不**声称任何模型最优、任何预测准确率提升、任何因果 AI 增量或跨域普适性。五条验证路径与两类对照共同界定了这条结论的边界，其中三条负结果被完整保留：External Transfer Gate3 `NOT SUPPORTED`、`NO_SINGLE_DOMINANT_MODEL`、`INSUFFICIENT_FOR_STRONG_ML_CLAIM`。

正式结论须等待 Human Gate 完成（`PENDING HUMAN-ANNOTATION INTAKE VERIFICATION`）。

---

## Appendix

### A. 图表清单（复用现有真实 F1–F6，不为 V2 重新生成实验图）

| 图 | QUESTION | RESULT | MEANING | 源 artifact | Claim |
|---|---|---|---|---|---|
| **Figure 1** F1 Model Flow | 模型各层如何衔接，不可判读走哪条路 | 六层链路；不可判读 → `NO_EFFECTIVE_EVIDENCE`；AI Increment `NOT_SUPPORTED` | Raw 与 Reliability 是两个独立层 | `reports/visual_evidence/final/F1_model_flow.svg`（源 `final_model_overview.md`） | C1 |
| **Figure 2** F2 Raw vs Adjusted | Raw 与 Adjusted 如何在记录级分离 | P108（L6，R=.375，贡献 2.25）、P105（L2，贡献 0.75）；保留 N=70 / 16 readable / 54 NEE；undefined 不画成零 | 分数与支持是两个轴；undefined ≠ 0 | `F2_raw_vs_adjusted.svg`（源 `raw_adjusted_metrics.csv`） | C2、C9 |
| **Figure 3** F3 Evidence Degradation | 受控改变单个证据字段，模型如何响应 | P108 假设移除 prompt 风险：R .375→.750、adj 2.25→4.50；降 confidence 到 low：R→.250、adj→1.50；P072 仅恢复 context 仍 NEE | 模型对证据质量有方向性响应；恢复上下文不制造证据。**非因果实验** | `F3_evidence_degradation.svg`（源 `evidence_perturbation_cases.csv`） | C5 |
| **Figure 4** F4 Parameter Perturbation | Score 稳定 vs Support 变化能否同图可见 | 局部 ±20% 扰动下 support 移动、0 次状态翻转；ranking `NOT_APPLICABLE`；有限网格非置信区间；context 平坦 `NOT_IDENTIFIED` | 核心结论最直接的视觉证据 | `F4_parameter_perturbation.svg`（源 `parameter_perturbation.csv` + 693 网格） | C3、C5、C8 |
| **Figure 5** F5 Ablation / Refusal | 逐层加组件时拒判语义如何变化 | M0→M3 有效权重 16→12→6→6；P105/P108 low support；P072/P035 refusal | 拒判边界由组件真实驱动；无 true outcome 时不声称准确率提升 | `F5_ablation_refusal.svg`（源 `ablation_results.csv`） | C4、C7 |
| **Figure 6** F6 External Structural Transfer | 教育结构能否迁移到不同性质的 Raw Signal | A/B/C 三策略的 low/medium/high reliability 分组；**Strategy C 反转排序** | 部分结构迁移证据；非教育验证、非交易主张 | `F6_external_structural_transfer.svg`（源 `transfer_validation.json`） | C10 |

**Table 优先展示顺序**（本文已按此组织）：Data audit（Table 3-1、3-2）→ Model definition（§4.3、§5.2）→ Ablation（Table 8-2）→ Validation matrix（Table 7-1）→ Challenger comparison（Table 9-1、9-2、9-3、9-4）→ Claim boundary（Table 12-1）。

### B. 锁定数字索引（18 组，全部来自 `PAPER_NUMBER_LOCK.md`，本文未新增任何数字）

| # | 量 | 值 | canonical source |
|---|---|---|---|
| 1 | Pilot V1 样本 | N = 140（秋 70 + 春 70） | `data/processed/pilot_sample.csv`；`docs/DATA_STRUCTURE.md` §2 |
| 2 | clean interactions | 7028 turns（student 3522 / AI 3506） | `data/processed/clean_interactions.csv` |
| 3 | Development sample | N = 70，`AI_PROVISIONAL` | `data/annotations/ai/pilot_ai_provisional.csv`；`final_results.json::data_identity` |
| 4 | Readable Evidence | 16（L2×5、L3×5、L4×1、L5×2、L6×3） | `independent_bounds_summary.json::raw_recount` |
| 5 | NO_EVIDENCE | 19 | 同上 |
| 6 | UNDETERMINED | 35 | 同上 |
| 7 | NO_EFFECTIVE_EVIDENCE | 54（= 19 + 35） | `final_results.json`（54 条 raw_score = null）；`research_core_closure.md` |
| 8 | Raw / Adjusted 分数 | ABL 3.5625；HOT 0.375；Gap 1.125（Raw 与 Adjusted 相同） | `final_results.json::raw_summary` / `::adjusted_summary` |
| 9 | Ablation effective weight | 16 → 12 → 6 → 6 | `ablation_results.csv`；`final_results.json::ablation[]` |
| 10 | Ablation effective coverage | 0.228571 → 0.171429 → 0.085714 → 0.085714（分母 N = 70） | `ablation_results.csv` |
| 11 | Robustness grid | 693 = 21 × 11 × 3；660 defined；33 undefined | `core_numbers_source_of_truth.json`；`independent_bounds_summary.json::parameter_space` |
| 12 | effective weight range | 0.4 → 16.0（中位数 5.8） | `independent_bounds_summary.json::bounds.effective_weight` |
| 13 | effective coverage range | 0.005714 → 0.228571（中位数 0.082857） | `independent_bounds_summary.json::bounds.effective_coverage` |
| 14 | parameter perturbation | ±10% / ±20% → 0 decision-state flips；ranking `NOT_APPLICABLE` | `parameter_perturbation_summary.json`；`final_results.json::sensitivity.rows`（15 行） |
| 15 | Counterexample | P108 Raw L6 / R 0.375 / adj 2.25 / `LOW_SUPPORT`+`ABSTAIN`；P105 Raw L2 / adj 0.75；P072、P035 `NO_EFFECTIVE_EVIDENCE` | `final_results.json::counterexamples`、`::development_results.explain_records`；`counterexamples.csv` |
| 16 | ML Challenger | LogReg ≈ 0.876（balanced ≈ 0.863）；Tree ≈ 0.919（balanced ≈ 0.901）；RF ≈ 0.922（balanced ≈ 0.894）；missing 0.71–0.81；RF cross-semester 0.588；`INSUFFICIENT_FOR_STRONG_ML_CLAIM` | `experiments/model_tournament/ml_results.json` / `.csv`；`ML_CHALLENGER_HANDOFF.md` |
| 17 | External Transfer | BTC n = 1698；threshold 0.65；Gate1 SUPPORTED（0.603→0.408）；Gate2 SUPPORTED（coverage 0.394→0.001）；Gate3 NOT SUPPORTED（≈0.525 vs ≈0.528）；`risk-coverage improvement = false` | `transfer_validation.json`；`information_missing_validation.json` |
| 18 | Human Gate | R1 = 0/70；R2 = 0/70；Formal Gate = `NOT_RUN` | `annotation_gate_report.json`；`final_results.json::reproducibility.formal_boundary` |

**一致性基线**：`run_all.py` 开发检查 32/32 PASS（六步，exit-code 0）；`src/verify_pilot_integrity.py` 21/21 冻结不变量 + 2 open defects（S4-F01、S4-F02，已从标注路径隔离）；独立复算复现 70/16/19/35、693/660/33、ABL/HOT/Gap 与 weight/coverage bounds。

### C. 引用文献（全部来自 `LITERATURE_CITATION_MAP.md` / `docs/literature/model_support_matrix.md`，无虚构 DOI、无虚构作者）

**Evidence Line A（observed performance ≠ true learning）**
- Soderstrom & Bjork (2015). *Learning Versus Performance: An Integrative Review*. Perspectives on Psychological Science. DOI 10.1177/1745691615569000
- Bastani et al. (2025). *Generative AI without guardrails can harm learning: Evidence from high school mathematics*. PNAS. DOI 10.1073/pnas.2422633122
- Fan et al. (2025). *Beware of Metacognitive Laziness*. British Journal of Educational Technology. DOI 10.1111/BJET.13544
- Krathwohl (2002). *A Revision of Bloom's Taxonomy*. Theory Into Practice. DOI 10.1207/s15430421tip4104_2

**Evidence Line B（measurement reliability / evidence quality / missing information）**
- Kane (2013). *Validating the Interpretations and Uses of Test Scores*. Journal of Educational Measurement. DOI 10.1111/jedm.12000
- Gašević, Greiff & Shaffer (2022). *Towards Strengthening Links between Learning Analytics and Assessment*. Computers in Human Behavior. DOI 10.1016/j.chb.2022.107304
- Gray & Bergner (2022). *A Practitioner's Guide to Measurement in Learning Analytics*. Handbook of Learning Analytics.
- Little & Rubin (2019). *Statistical Analysis with Missing Data* (3rd ed.).
- Rubin (1976). *Inference and Missing Data*. Biometrika. DOI 10.1093/biomet/63.3.581
- Saisana, Saltelli & Tarantola (2005). *Uncertainty and Sensitivity Analysis Techniques for Composite Indicators*. JRSS-A. DOI 10.1111/j.1467-985X.2005.00350.x
- OECD/EU/EC-JRC (2008). *Handbook on Constructing Composite Indicators*.
- Putnick & Bornstein (2016). *Measurement Invariance Conventions and Reporting*. Developmental Review. DOI 10.1016/j.dr.2016.06.004

**Evidence Line C（selective prediction / abstention / risk–coverage）**
- El-Yaniv & Wiener (2010). *On the Foundations of Noise-Free Selective Classification*. JMLR 11:1605–1641.
- Geifman & El-Yaniv (2017). *Selective Classification for Deep Neural Networks*. NeurIPS.
- Guo et al. (2017). *On Calibration of Modern Neural Networks*. ICML.
- Angelopoulos et al. (2024). *Conformal Risk Control*. ICLR.（仅方法储备）

**Evidence Line D（AI assistance / prompt dependence / automation bias）**
- Parasuraman & Riley (1997). *Humans and Automation: Use, Misuse, Disuse, Abuse*. Human Factors. DOI 10.1518/001872097778543886
- Skitka, Mosier & Burdick (2000). *Does Automation Bias Decision-Making?* International Journal of Human-Computer Studies. DOI 10.1006/ijhc.1999.0341
- Bansal et al. (2021). *Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance*. CHI. DOI 10.1145/3411764.3445717
- Hernán & Robins (2022). *Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available*. American Journal of Epidemiology. DOI 10.1093/aje/kwab249
- Cohen (1960). *A Coefficient of Agreement for Nominal Scales*. Educational and Psychological Measurement. DOI 10.1177/001316446002000104（inter-rater 口径，见 GAP-3）
- Krippendorff (2018). *Content Analysis: An Introduction to Its Methodology*. SAGE.（inter-rater 口径，见 GAP-3）

**CITATION_GAP（无真实对应文献，不虚构）**：GAP-1 Evidence Reliability 加权的精确建模构造；GAP-2 Bloom L2–L6 本地标注效度；GAP-3 同一标注者 intra-rater test-retest 的规范引用。详见 `paper_v2_citation_gap_report.md`。

### D. 锁定文件索引

| 用途 | 路径 |
|---|---|
| 唯一数字源与冲突处理 | `yu/paper/PAPER_NUMBER_LOCK.md` |
| 声明 → 证据 → 数字 → 表/图映射（C1–C13） | `yu/paper/PAPER_EVIDENCE_TRACE.md` |
| 文献引用映射与 CITATION_GAP | `yu/paper/LITERATURE_CITATION_MAP.md` |
| 冻结词汇与非等价关系 | `yu/docs/metric_dictionary.md` |
| 研究故事与五重验证 | `yu/docs/research_story/research_story_summary.md` |
| 统一事实源 | `yu/outputs/final_results.json` |
| 独立复算 | `yu/reports/verification/independent_bounds_summary.json`、`core_numbers_source_of_truth.json` |
| 稳健性/失败边界小结 | `yu/reports/development/robustness_validation_summary.md` |
| Binance 公开数据 shadow | `yu/experiments/transfer_finance/live_shadow/live_shadow_summary.json` |
| 旧版 V1 论文（保留可追溯，本文不覆盖） | `yu/paper/development_submission_candidate.md` |

### E. V2 与 canonical paper 的关系声明

本文件是**结构重写后的 canonical development 论文**，不是新研究。它：

- **不新增**模型、数据、实验、参数、结果、Human Label 或 Formal Gate；
- **不改变**任何 canonical 数字（全部 18 组锁定数字逐一沿用，见 Appendix B）；
- **不覆盖** V1 `paper/development_submission_candidate.md`（保留不删除，可追溯）；
- 相对 V1 的改动仅限于：结构重写、验证路径统一到单一 Main RQ + VQ1–VQ5、文献按 evidence line 组织并保留 CITATION_GAP、以及 claim boundary 显式化；未新增任何经验结果；
- 本轮已 commit（未 push）、未生成最终 PDF。

---

**PAPER_V2_STATUS = PAPER_V2_CANONICAL_DEVELOPMENT**

_Formal Human Gate 仍未完成，不标 `FORMAL_FINAL`。_
