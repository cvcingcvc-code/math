# LITERATURE CITATION MAP

> 状态：`PAPER_LITERATURE_LOCK`。只引用项目已真实收集的文献（见 `docs/literature/model_support_matrix.md`），不虚构作者、标题或 DOI。
> 无真实对应文献处标 `CITATION_GAP`，不得编造。

## 一、概念 → 文献匹配

| # | 论文观点 | 需要什么文献 | 项目已有真实文献（title / DOI / source） | 是否可正文引用 |
|---|---|---|---|---|
| 1 | measurement validity（观测指标不等于构念/用途） | 测量效度与 interpretation/use argument | Kane (2013), *Validating the Interpretations and Uses of Test Scores*, J. Educational Measurement, DOI 10.1111/jedm.12000；Gray & Bergner (2022), *A Practitioner's Guide to Measurement in Learning Analytics*；Gašević, Greiff & Shaffer (2022), *Towards Strengthening Links between Learning Analytics and Assessment*, Computers in Human Behavior, DOI 10.1016/j.chb.2022.107304 | 是（正文 Introduction / Problem Formulation） |
| 2 | missing data / evidence quality（缺失不是零值，缺失机制决定可识别性） | missing data 机制与状态建模 | Little & Rubin (2019), *Statistical Analysis with Missing Data*；Rubin (1976), *Inference and Missing Data*, Biometrika, DOI 10.1093/biomet/63.3.581 | 是（正文 NO_EFFECTIVE_EVIDENCE 语义） |
| 3 | selective prediction / abstention（拒判 + coverage–risk） | selective classification 基础 | El-Yaniv & Wiener (2010), *On the Foundations of Noise-Free Selective Classification*, JMLR 11:1605–1641；Geifman & El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS | 是（正文 ABSTAIN / coverage） |
| 4 | uncertainty / confidence（confidence ≠ 概率，需校准） | 校准与置信度 | Guo et al. (2017), *On Calibration of Modern Neural Networks*, ICML | 是（正文把 c_i 标为假设支持分，非概率） |
| 5 | human–AI learning evaluation（即时表现 ≠ 持久学习；AI 辅助表现与独立表现可分离） | 学习 vs 表现；AI 辅助 vs 独立 outcome | Soderstrom & Bjork (2015), *Learning Versus Performance*, Perspectives on Psychological Science, DOI 10.1177/1745691615569000；Bastani et al. (2025), *Generative AI without guardrails can harm learning*, PNAS, DOI 10.1073/pnas.2422633122；Fan et al. (2025), *Beware of Metacognitive Laziness*, BJET, DOI 10.1111/BJET.13544 | 是（正文 Introduction 背景 + 因果边界） |
| 6 | robustness / sensitivity analysis（综合指标不确定性传播） | 不确定性/敏感性分析方法 | Saisana, Saltelli & Tarantola (2005), *Uncertainty and Sensitivity Analysis Techniques for Composite Indicators*, JRSS-A, DOI 10.1111/j.1467-985X.2005.00350.x；OECD/EU/EC-JRC (2008), *Handbook on Constructing Composite Indicators* | 是（正文 Sensitivity/Robustness 方法依据） |
| 7 | external validation / transferability（跨域可比性、可迁移性） | 跨组测量不变性；观察数据因果边界 | Putnick & Bornstein (2016), *Measurement Invariance Conventions and Reporting*, Developmental Review, DOI 10.1016/j.dr.2016.06.004；Hernán & Robins (2022), *Using Big Data to Emulate a Target Trial*, Am J Epidemiology, DOI 10.1093/aje/kwab249 | 是（正文 External Transfer / 因果边界） |

## 二、支撑 abstention 的补充文献（可放正文/附录）

- **Angelopoulos et al. (2024)**, *Conformal Risk Control*, ICLR：在交换性等条件下把拒判升级为有限样本风险控制；当前无足够人工真值，仅作「后续方法储备」，不声称已有 conformal guarantee。
- **Cohen (1960)**, *A Coefficient of Agreement for Nominal Scales*, DOI 10.1177/001316446002000104；**Krippendorff (2018)**, *Content Analysis*：标注一致性统计；本项目冻结设计是同一标注者 test-retest，非 inter-rater。

## 三、supporting model 的文献（可放正文）

- **Krathwohl (2002)**, *A Revision of Bloom's Taxonomy*, DOI 10.1207/s15430421tip4104_2：Bloom 是认知过程分类语言，不是稳定能力测量——支撑「Task Bloom 与 Student Evidence 双轴，不直接解释为能力」。
- **Parasuraman & Riley (1997)**, *Humans and Automation*, DOI 10.1518/001872097778543886；**Skitka, Mosier & Burdick (2000)**, *Does Automation Bias Decision-Making?*, DOI 10.1006/ijhc.1999.0341；**Bansal et al. (2021)**, *Does the Whole Exceed its Parts?*, CHI, DOI 10.1145/3411764.3445717：支撑 prompt-induced / AI-origin / conflict evidence 标记的合理性。

## 四、最值得正文引用的 5–8 篇（优先）

1. Soderstrom & Bjork (2015) — observed performance ≠ durable learning。
2. Bastani et al. (2025) — AI 辅助表现与独立后测可分离（高质量随机证据）。
3. Kane (2013) — 分数解释与分数用途分开论证。
4. Gašević et al. (2022) — 学习分析日志放回测量效度框架。
5. Saisana et al. (2005) — 不确定性传播与敏感性分析。
6. El-Yaniv & Wiener (2010) — risk–coverage 与 selective prediction。
7. Guo et al. (2017) — confidence 不是概率，需校准。
8. Hernán & Robins (2022) — 约束 Observed AI Increment 不被误写为因果增量。

## 五、CITATION_GAP（项目当前无真实对应文献）

| 概念 | 缺口说明 | 处理 |
|---|---|---|
| 「AI 辅助学习交互日志中的 Evidence Reliability 加权」这一精确建模 | 项目文献矩阵中没有任何一篇直接提出「可观察证据的可靠性支持权重」这一具体构造；最近的 Gašević/Gray & Bergner 只是测量效度框架，非该权重公式 | `CITATION_GAP`：论文只声明为「本文提出的可审查支持权重」，不声称有直接文献先例 |
| 「Student Evidence Bloom L2–L6 作为可判读等级」的本地标注效度 | 只有 Krathwohl (2002) 支撑 Bloom 分类语言，无本地标注协议效度论文 | `CITATION_GAP`：标注效度留待 Human Gate / 本地验证 |
| 「同一标注者 test-retest（非 inter-rater）」的既定规范引用 | Cohen/Krippendorff 是 inter-rater 口径；项目当前无专门讨论 intra-rater test-retest 的收集文献 | `CITATION_GAP`：正文如实写明设计类型，不借用 inter-rater 文献冒充 |

## 六、引用纪律（写入论文）

- 只引用「该论文设计下成立的结论」，不把相关性写成因果、不把模型校准写成已校准、不把拒判风险覆盖写成 Gate 已通过。
- 跨领域方法论文用于公式/验证设计时标注「方法依据」，不冒充教育实证。
- 在 Human R1/R2 返回前，所有 Reliability 结论限于协议、开发数据与待验证设计。
