# 赛道一 S2：文献与信息检索证据矩阵

> **研究对象冻结**：学生在 AI 辅助学习中的“可观察交互与学习表现证据”，而不是 AI 回答本身的质量。  
> **核心目标**：构建能区分学生真实学习表现、智能体引导路径及数据/标注偏差的可信 AIV 评价体系，并限定结论适用边界。  
> **原则**：先论证观测代表什么，再讨论数学模型。本文件是文献证据整理，不是最终建模、模型训练或 AIV 公式。

## 0. 研究边界与现有数据能回答的问题

### 0.1 变量概念图

| 概念 | 本项目可观察或潜在变量 | 解释边界 |
|---|---|---|
| 学生真实学习表现（目标构念） | 学生自己提出的问题、解释、推理、应用、检验/纠错、迁移等内容证据；若有独立测验则包括无 AI 条件下的正确率、保持与迁移 | 仅有交互文本时，最多测到“交互中可见的表现证据”，不能直接等同于稳定能力或长期学习。无 AI 后测、延迟测验、独立评分时，不能声称已验证学习增量。 |
| AI/智能体影响 | 智能体类型、提示顺序与脚手架、反向/正向路径、问题提示、AI 回答、学生对回答的采纳/质疑/改写、使用频次 | 目前日志能够反映部分工具暴露与互动，但不能自动识别哪些推理来自学生、哪些由 AI 供给；工具暴露也可能受先前能力和动机影响。 |
| 数据偏差/选择 | 学期/课程/班级构成、是否进入导出名单、是否有日志、使用工具的自选择、记录窗口差异、链接缺文、学号匹配失败 | 只分析有日志者会引入选择；缺失不等于未使用。秋春构成/窗口/工具不齐时，群体均值差不是处理效应。 |
| 测量/标注误差 | 学生/AI 语句边界、Q/A 混合、Bloom 六级歧义、AI 预标注置信度、人工分歧、智能体身份解析错误 | Bloom 级别是对可见语句/任务的编码，不是学生能力的直接观测。应报告类别混淆与不确定度，而非只报总体准确率。 |
| 主观反馈 | 学生自评、满意度、感知帮助、赞踩与评论 | 是感受/感知效用，不是客观掌握的替代测量；应作为不同结果维度单列，并检验与表现证据的关联。 |

### 0.2 赛题附件审计带来的证据边界

此前对 RAR 附件的结构核验发现：2025 秋问答表为 845 条、297 个学号；该表没有认知层级字段，尽管文件名带“已标注”。另一个被用作春季问答来源的表有 1,925 条、528 个学号，时间覆盖 2024-11-21 至 2026-09-19，来源字段混合多个 AI 渠道；春季四份参与名单并集 133 个学号，其中 109 人可匹配到 482 条记录（匹配记录时间 2026-03-19 至 2026-07-27）。秋季有 21 条、该大表有 123 条链接型记录而非完整正文。以上只是数据结构核验，不是清洗完成后的分析样本。需再次核对原表、时间窗、表格版本、纳入名单和去重口径后方可用于正式分析。

因此，现有日志可直接描述被记录到的互动行为、文本类别（经可信标注后）、工具/来源构成、频次、时间分布和反馈；可以估计标注一致性、日志覆盖、记录缺失、工具路径与交互特征的条件关联。**当前附件不足以直接回答**学生长期能力是否提高、撤去 AI 后是否能独立完成任务、AI 相对无 AI 的平均因果效应、秋春变化由 AI 导致的比例。需确认是否另有成绩/前测/后测、分配机制、课程教学计划及稳定的班级/工具字段。

## 1. Search Strategy

### 来源

- 出版方/原始论文页：AAAI OJS、PNAS、Nature Scientific Reports、Elsevier/ScienceDirect、Wiley、SAGE、Springer、BMJ、JAMA、OECD/JRC。
- 学术索引与全文仓储：PubMed/PMC、arXiv（仅作为预印本版本核对，不与最终同行评审版本混淆）、SoLAR/Handbook of Learning Analytics、机构仓储和 Crossref DOI 落地页。
- 赛题指定网站 `wytsg.com/e/action/ListInfo/?classid=62`：本次 Web 检索无法读取（页面抓取返回错误）；桌面浏览器自动化也未能判定当前页面 URL，故不声称检索过站内资料。检索结果以可公开核验来源为准。

### 关键词与组合

- 中文：布鲁姆认知层次；开放文本/学生提问自动分类；教育文本标注一致性；智能体脚手架；认知卸载；独立测验/延迟保持/迁移；学习分析测量效度；测量不变性/差异题项功能；目标试验/教育因果推断；倾向评分/双重差分/平行趋势；复合指标/权重/排名稳健性；Goodhart/指标博弈；标注误差传播/概率标签/不确定性分析；自评与客观成绩一致性。
- 英文：`Bloom taxonomy student-generated questions classification reliability`; `student dialogue cognitive level annotation LLM human agreement`; `AI tutoring scaffolding unassisted posttest retention transfer randomized trial`; `generative AI cognitive offloading learning performance`; `learning analytics measurement validity construct`; `target trial education AI observational treatment outcome estimand`; `difference-in-differences parallel trends education cohort`; `measurement invariance cross-cohort assessment`; `composite indicator uncertainty sensitivity ranking robustness`; `metric gaming reactivity education`; `classification error uncertainty propagation composite score`。
- 组合示例：`(Bloom OR cognitive taxonomy) AND (student questions OR dialogue) AND (annotation OR inter-rater)`；`(generative AI OR intelligent tutor) AND (unassisted test OR transfer OR retention) AND (randomized OR experiment)`；`(learning analytics) AND (measurement validity OR construct validity)`；`(composite indicator) AND (weight OR uncertainty OR sensitivity OR ranking)`；`education AND (target trial OR DID OR matching) AND (identification OR assumptions)`。

### 时间范围、筛选与状态约定

优先覆盖 2021—2026（近五年），并保留构念效度、学习/表现区分、Bloom 理论、测量一致性、因果推断和综合指标的经典依据。纳入同行评议实验/系统综述/元分析/方法论文、权威手册及能直接对应本题的理论论文；排除仅泛谈 AI 教育、只评 AI 输出质量而无学生测量含义的论文、无法核验的引用、与学习证据无关的工程模型。文献的证据强度针对“对本题具体主张的支撑力”，不是对期刊声誉的评价。

- `FULL_TEXT_READ`：检索到并读取论文全文或可访问全文页面/章节。
- `ABSTRACT_ONLY`：只核对元数据、摘要或摘要级索引，不据此补写全文方法细节。
- `UNVERIFIED`：关键元数据/原文结论尚未找到权威来源核实；本表不把这类文献作为支持性证据。
- **下载状态**：当前网络/浏览器工具可打开部分开放全文，但无法将 PDF 稳妥落盘到工作区；本次未保存论文 PDF 至 `references/papers/`。保留可访问的出版方或仓储原链接，不能把“网页可读”表述成“本地已下载”。

## 2. Evidence Matrix

下列每条均按统一字段记录。`Cannot support` 是使用该文献时必须保留的边界。证据强度：高=与论断直接匹配且设计强/综合证据；中=方法/机制强但场景有差异；低=概念或间接迁移。

### A. 构念、Bloom 标注与学习分析测量

#### A1. Krathwohl (2002), “A Revision of Bloom’s Taxonomy: An Overview”

- **来源/DOI**：*Theory Into Practice*, 41(4), 212–218. [原文 DOI](https://doi.org/10.1207/s15430421tip4104_2)。全文状态：`ABSTRACT_ONLY`（本轮核对出版信息与摘要级资料）。
- **研究对象/问题**：修订版教育目标分类框架；阐明认知过程与知识维度的二维分类。
- **数据/变量**：理论综述，无学生样本数据；变量为六类认知过程及知识类型。
- **方法/指标/发现**：概念分析；Remember、Understand、Apply、Analyze、Evaluate、Create 描述认知活动分类。分类服务于目标、教学和评价对齐。
- **假设/局限/证据强度**：分类需结合学科内容、任务情境与可观察证据解释。理论框架不是经验证的能力测试。证据强度：中（分类语言的理论依据）。
- **可用于/不能支持**：用于制定代码本、说明分类语义；不能支持“某次高阶提问=学生高阶能力/学习增长”，也不给出适用于本数据的标注效度或可靠性。

#### A2. Chan, Tsui, Chan & Hong (2002), “Applying the Structure of the Observed Learning Outcomes (SOLO) Taxonomy on Student's Learning Outcomes: An empirical study”

- **来源/DOI**：*Assessment & Evaluation in Higher Education*, 27(6), 511–527. [原文 DOI](https://doi.org/10.1080/0260293022000020282)。全文状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：学生长篇试卷与短课堂讨论文本；比较 Bloom、SOLO 与反思思维分类对学习结果测量的适用性。
- **数据/变量**：学生 essay 和课堂讨论回应；不同分类下的认知/结果层次。
- **方法/指标/发现**：概念比较并对学生文本进行分类。摘要指出 SOLO 可用于多种学习结果，但层级细分未消除概念歧义；建议用专家评审判断分类法、结果构念与情境的匹配。
- **假设/局限/证据强度**：摘要未报告完整样本量、编码协议及一致性数值。证据强度：中。
- **可用于/不能支持**：支持先界定“要测什么”再选分类框架，提示细分等级可能不自动消除歧义；不能直接给出本题六级与三阶可靠性的差异。

#### A3. Elkins, Kochmar, Cheung & Serban (2024), “How Teachers Can Use Large Language Models and Bloom’s Taxonomy to Create Educational Quizzes”

- **来源/DOI**：*Proceedings of AAAI*, 38(21), 23084–23091. [AAAI 论文页与 PDF](https://ojs.aaai.org/index.php/AAAI/article/view/30353)，[DOI](https://doi.org/10.1609/aaai.v38i21.30353)。全文状态：`FULL_TEXT_READ`。
- **研究对象/问题**：LLM 按 Bloom 学习目标生成测验题，评估教师是否使用、题目/测验质量如何。
- **数据/变量**：论文报告教师参与的多项实验；评价对象是 AI 辅助生成的题目和教师制作的 quiz，不是学生独立能力。
- **方法/指标/发现**：受控提示生成六级题目；教师偏好、质量判断及 quiz 指标显示 AI 题目可作为教师编题支架，整体质量不低于手写版本，部分指标更好。
- **假设/局限/证据强度**：Bloom 标签用于控制生成目标，不代表验证学生能力；需教师审查内容与教学适切性。证据强度：中（证明路径/提示可塑造题目层级）。
- **可用于/不能支持**：直接支持“智能体路径会塑造可见问题/任务层级”，提示路径效应要独立建模；不能支持学生提问的自动 Bloom 分类准确率或学习增益。

#### A4. Gašević, Greiff & Shaffer (2022), “Towards Strengthening Links between Learning Analytics and Assessment: Challenges and Potentials of a Promising New Bond”

- **来源/DOI**：*Computers in Human Behavior*, 134, 107304. [出版方页](https://doi.org/10.1016/j.chb.2022.107304)，[可读全文 PDF](https://www.epistemicanalytics.org/images/pdf/SI_introduction%2022Mar2022_track_clean%5B31%5D.pdf)。全文状态：`FULL_TEXT_READ`。
- **研究对象/问题**：学习分析日志与正式教育测量/评价之间的关系。
- **数据/变量**：特别专刊的 11 项研究及概念综合；交互数据、学习分析指标、正式/形成性评价和测量效度。
- **方法/发现**：综述性框架将研究分为 analytics for assessment、analytics of assessment、validity of measurement；指出任务设计、学习进阶、可信度和公平是连接关键。
- **假设/局限/证据强度**：社论/专刊导言，不能替代单一效应评估。证据强度：中高（学习分析测量有效性框架）。
- **可用于/不能支持**：支持把学习日志视为待验证的测量证据，而非天然有效的能力指标；不能给出本题某个指标的效度系数。

#### A5. Gray & Bergner (2022), “A Practitioner’s Guide to Measurement in Learning Analytics: Decisions, Opportunities, and Challenges”

- **来源**：*Handbook of Learning Analytics*, 2nd ed., Chapter 2, pp. 20–28. [SoLAR 章节页](https://www.solaresearch.org/publications/hla-22/hla22-chapter2/)，[手册 PDF](https://solaresearch.org/wp-content/uploads/hla22/HLA22.pdf)。全文状态：`FULL_TEXT_READ`。
- **研究对象/问题**：如何从多源学习数据建立有意义、有效、可靠的学习测量。
- **数据/变量**：方法指南并以学习分析实例说明；潜在学习构念、交互日志、测量工具及误差。
- **方法/主要结论**：从“数据测量什么、为何测量、可推断什么”出发，将可观察数据联系到潜在构念；讨论数据收集误差与有效可靠测量。
- **假设/局限/证据强度**：方法章节，不是随机试验；需要为不同数据源分别建立效度论证。证据强度：高（本项目测量论主依据）。
- **可用于/不能支持**：用于学生行为日志→指标→教育解释的测量论证；不能证明某个行为变量已经代表能力。

#### A6. Kane (2013), “Validating the Interpretations and Uses of Test Scores”

- **来源/DOI**：*Journal of Educational Measurement*, 50(1), 1–73. [原文 DOI](https://doi.org/10.1111/jedm.12000)。全文状态：`ABSTRACT_ONLY`（可核对摘要与期刊元数据）。
- **研究对象/问题**：测试分数解释与用途如何验证。
- **数据/变量**：论证型效度理论，无单一数据集；从作答到评分、构念解释及决策用途的推论链和假设。
- **方法/发现**：构造解释/使用论证，逐项检查推论与假设证据；分数解释被支持不自动意味着对应使用也有效，越强的主张需越强证据。
- **局限/证据强度**：理论/方法论文，不提供本项目实证效度结果。证据强度：高（论证框架）。
- **可用于/不能支持**：为 AIV 每一层解释链（文本→编码→指标→评价）建立可证伪主张；不能替代校验样本或结果效度。

#### A7. Soderstrom & Bjork (2015), “Learning Versus Performance: An Integrative Review”

- **来源/DOI**：*Perspectives on Psychological Science*, 10(2), 176–199. [DOI](https://doi.org/10.1177/1745691615569000)，[作者公开 PDF](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/11/soderstorm_ra_learningvsperformance.pdf)。全文状态：`FULL_TEXT_READ`。
- **研究对象/问题**：即时训练表现是否能代表较持久的学习。
- **数据/变量**：跨言语与动作学习研究的整合综述；学习以延迟保持/迁移表征，表现为训练或即时作答表现。
- **方法/主要发现**：综述表明即时表现与相对持久的知识/技能变化可能分离，甚至某些条件下方向相反。
- **假设/局限/证据强度**：不是 GenAI 特定研究；经典基础证据。证据强度：高（构念区分理论）。
- **可用于/不能支持**：支持区分 AI 辅助完成任务与撤去 AI 后独立表现/保持；不能直接量化本题学生的学习效果。

### B. AI 脚手架、认知卸载、表现与自评

#### B1. Faber et al. (2024), “Effects of adaptive scaffolding on performance, cognitive load and engagement in game-based learning: a randomized controlled trial”

- **来源/DOI**：*BMC Medical Education*, 24, 943. [PubMed 原始记录](https://pubmed.ncbi.nlm.nih.gov/39210381/)，[DOI](https://doi.org/10.1186/s12909-024-05698-3)。全文状态：`ABSTRACT_ONLY`（本轮仅核实摘要/元数据）。
- **研究对象/问题**：自适应脚手架对游戏化学习中的表现、认知负荷和参与的影响。
- **数据/变量**：随机对照设计；脚手架条件、测验表现、认知负荷与参与度。
- **方法/结论**：实验比较不同脚手架条件，重点是同时测多种结果，而非只看行为量。需按全文核对具体样本、效应和测量时点后再引用数值。
- **假设/局限/证据强度**：领域/游戏任务与本题智能体对话不同；证据强度：中（干预设计与多结果测量）。
- **可用于/不能支持**：说明脚手架是影响学习过程和结果的处理组成，可做路径/条件分层；不能外推为探知侠/逆行侠效果。

#### B2. Bastani et al. (2025), “Generative AI without guardrails can harm learning: Evidence from high school mathematics”

- **来源/DOI**：*PNAS*, 122(26), e2422633122. [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635/)，[DOI](https://doi.org/10.1073/pnas.2422633122)。全文状态：`FULL_TEXT_READ`。
- **研究对象/问题**：近千名高中数学学生使用 GPT-4 时，AI 帮助方式如何影响辅助练习表现和撤去 AI 后测验。
- **数据/核心变量**：课堂随机分配 control、GPT Base、GPT Tutor；练习成绩、无资源独立考试、对话记录、学生自我感知。
- **方法/指标/发现**：随机现场实验；AI 辅助练习相对控制组分数提高（Base 48%、Tutor 127%），但撤去 AI 的考试中 Base 组低 17%，Tutor 组与控制组无显著差异；学生感知与实际成绩不一致。评分使用盲化/平衡分配的独立阅卷者和教师 rubric。
- **假设/局限/证据强度**：单校、高中数学、短期/特定模型与工具设计；随机分配使内部因果识别强，外部可迁移性有限。证据强度：高（即时表现 vs 独立表现）。
- **可用于/不能支持**：强力支持本项目分开记录辅助表现与独立学习证据、学生自评与客观结果；不能证明本项目日志里的学生发生了同类负效应。

#### B3. Kestin et al. (2025), “AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting”

- **来源/DOI**：*Scientific Reports*, 15, 17458. [出版方全文](https://www.nature.com/articles/s41598-025-97652-6)，[PubMed](https://pubmed.ncbi.nlm.nih.gov/40537565/)，[DOI](https://doi.org/10.1038/s41598-025-97652-6)。全文状态：`FULL_TEXT_READ`（公开论文页/摘要和方法信息）。
- **研究对象/问题**：大学物理课堂中，基于研究型教学设计的 AI tutor 与主动学习课堂对比。
- **数据/变量**：大学生随机对照试验；学习测验表现、学习时间、参与/动机感知。
- **方法/发现**：随机比较 AI tutor 与面对面主动学习；作者报告 AI tutor 组学习更多且耗时更短。
- **假设/局限/证据强度**：特定结构化 tutor、内容和短期测试；作者也提醒复杂综合/高阶批判任务未必同样适用。证据强度：高（该情境内干预效果）。
- **可用于/不能支持**：证明 AI 效果取决于设计和比较条件；支持把“AI 处理”具体定义为某种脚手架，而非笼统 AI 使用。不能与 Bastani 的结果简单平均，也不说明自然交互的长期效果。

#### B4. Fan et al. (2025), “Beware of Metacognitive Laziness: Effects of Generative Artificial Intelligence on Learning Motivation, Processes, and Performance”

- **来源/DOI**：*British Journal of Educational Technology*. [DOI](https://doi.org/10.1111/BJET.13544)，[开放作者版 PDF](https://iagen.unam.mx/recursos/Beware%20of%20Metacognitive%20Laziness-%20Effects%20of%20Generative%20Artificial%20Intelligence%20on%20Learning%20Motivation%2C%20Processes%2C%20and%20Performance.pdf)。全文状态：`FULL_TEXT_READ`（作者版全文可读）。
- **研究对象/问题**：117 名大学生完成写作任务，比较 ChatGPT、人类专家、写作分析工具与无额外工具对动机、自我调节过程、表现的影响。
- **数据/变量**：随机实验；多通道学习过程/表现/动机数据，作文改进、知识增益与迁移、自我调节过程序列。
- **方法/发现**：组间实验与过程序列分析；不同支持组的自我调节过程频率/顺序有差异；ChatGPT 组作文分数改善，但知识增益和迁移未显著不同。
- **假设/局限/证据强度**：写作任务、样本 117、特定工具条件。证据强度：中高。
- **可用于/不能支持**：支持“产出改善≠知识/迁移提升”，以及分析互动过程/脚手架路径；不能把写作实验的效应量外推到数模课程。

#### B5. Deng et al. (2025), “Does ChatGPT enhance student learning? A systematic review and meta-analysis of experimental studies”

- **来源/DOI**：*Computers & Education*, 227, 105224. [出版方页](https://www.sciencedirect.com/science/article/pii/S0360131524002380)，[DOI](https://doi.org/10.1016/j.compedu.2024.105224)。全文状态：`ABSTRACT_ONLY`（核对摘要与出版页）。
- **研究对象/问题**：ChatGPT 对学生学习表现、动机/情感、高阶思维等影响的实验研究综合。
- **数据/变量**：系统综述与实验研究元分析；干预组、学业表现及其他学习维度；摘要称研究主要在大学、语言课程。
- **方法/发现**：实验研究系统综述/元分析；作者强调测验需区分 AI 输出质量与干预对学业表现的影响，鼓励复杂项目/监考测量、客观高阶指标、长程跟踪和充分样本量。
- **假设/局限/证据强度**：异质干预和结果使平均效应依赖研究纳入与模型；此处不引用未核实效应数值。证据强度：高（实验综述，摘要级核实）。
- **可用于/不能支持**：支撑 B 的证据设计要求；不能给本项目的因果效应或分层参数。

#### B6. Yan et al. (2022), “Effects of self-assessment and peer-assessment interventions on academic performance: A meta-analysis”

- **来源/DOI**：*Educational Research Review*, 37, 100484. [出版方开放页](https://www.sciencedirect.com/science/article/pii/S1747938X22000537)，[DOI](https://doi.org/10.1016/j.edurev.2022.100484)。全文状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：学生自评、同伴评价及二者结合对学业表现的影响。
- **数据/变量**：175 项独立研究、19,383 名参与者、626 个效应量；评估干预与学业表现。
- **方法/发现**：元分析；自评、同伴评、混合干预与表现均有正向总体效果；有对照组研究的效应量低于无对照组研究，在线技术调节同伴评价效果。
- **假设/局限/证据强度**：这是“自评干预是否促进表现”，不是自评分数和客观能力的一致性元分析。证据强度：高（广泛综合）。
- **可用于/不能支持**：提醒设计中区分自评作为干预/感受和自评作为能力测量；不能将自评指标当成客观学习结果。

#### B7. Wang & Fan (2025), “The effect of ChatGPT on students’ learning performance, learning perception, and higher-order thinking: insights from a meta-analysis”

- **来源/DOI**：*Humanities and Social Sciences Communications*, 12, 621. [原文 DOI](https://doi.org/10.1057/s41599-025-04787-y)。**排除：该期刊页面当前明确标注 RETRACTED ARTICLE**，不纳入支持性证据、不引用其效应量。状态：`FULL_TEXT/RETRACTION_STATUS_VERIFIED`。
- **研究对象/方法**：原文为 2022–2025 ChatGPT 效果元分析，但撤稿信息已使其结论不可作为可靠支持。
- **对本项目价值**：只作为检索/引用风险实例：必须查撤稿状态，不能因摘要效果“好看”就引用。不能支持任何 AIV 权重或 AI 正效应。

#### B8. Krathwohl / student self-assessment additional evidence: Eva & Regehr (2005), “Self-assessment in the health professions: a reformulation and research agenda”

- **来源/DOI**：*Academic Medicine*, 80(10 Suppl), S46–S54. [DOI](https://doi.org/10.1097/00001888-200510001-00015)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：专业教育中的自我评估研究与自我监控概念。
- **数据/变量/方法/发现**：概念/研究综述，区分自我评分与自我监控/调节；不同操作定义对应不同效度问题。
- **局限/强度**：医学/专业教育且较早；中等理论依据。
- **可用于/不能支持**：支持主观反馈单列、用独立证据检验；不能给出本项目学生反馈-客观分数相关系数。

### C. B 模块：因果效应、处理定义与观察数据边界

#### C1. Hernán & Robins (2022), “Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available”

- **来源**：*American Journal of Epidemiology*, 191(4), 541–552. [出版方 DOI 入口](https://doi.org/10.1093/aje/kwab249)。状态：`ABSTRACT_ONLY`（方法文献，跨领域迁移）。
- **研究对象/问题**：如何用观察数据明确模拟理想随机试验，减少观察研究的设计偏差。
- **数据/变量**：方法学论文；目标人群、处理策略、分配/时间零点、结局、随访、因果对比、分析计划。
- **方法/发现**：先指定 target trial，再映射现有数据；透明化处理定义与时间对齐，仍需混杂控制和完整数据。
- **假设/局限/证据强度**：target-trial 框架不能弥补未测量混杂、没有合适对照或结局缺失。证据强度：高（设计原则）。
- **可用于/不能支持**：要求先定义学生的处理（AI 暴露/路径）、时点和学习结果；不能将其作为存在因果识别的证明。

#### C2. Callaway & Sant’Anna (2021), “Difference-in-Differences with Multiple Time Periods”

- **来源/DOI**：*Journal of Econometrics*, 225(2), 200–230. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：多期、分批处理时 DID 的识别、估计和推断。
- **数据/变量**：多期处理组/对照组面板或重复截面；组别-时间处理效应与结果。
- **方法/发现**：在条件平行趋势等假设下定义 group-time ATT，适用于处理时间差异；不能把传统双向固定效应一概视为可解释平均效应。
- **假设/局限/证据强度**：要求可信处理/对照、前后结果、处理时间与平行趋势；估计器不会创造这些数据。证据强度：高（方法）。
- **可用于/不能支持**：作为未来若有可比控制组和多个时期时的候选方法；当前两个学期日志本身不能满足其前提。

#### C3. Roth, Sant’Anna, Bilinski & Poe (2023), “What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature”

- **来源/DOI**：*Journal of Econometrics*, 235(2), 2218–2244. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：DID 近期方法问题综述，聚焦平行趋势、事件研究、估计量与推断。
- **数据/变量**：计量方法综述，无单个教育数据集。
- **方法/主要结论**：综合 DID 的识别假设和常见误用，强调平行趋势不能由“不显著的前趋势检验”证明，有限样本下检验能力/置信区间需报告。
- **局限/证据强度**：不是教育 AI 应用。证据强度：高（方法假设）。
- **可用于/不能支持**：约束模块 B 的 DID 声称和安慰剂解释；不能以跨秋春一前一后均值制造 DID。

#### C4. Stuart (2010), “Matching Methods for Causal Inference: A Review and a Look Forward”

- **来源/DOI**：*Statistical Science*, 25(1), 1–21. [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC2943670/)，[DOI](https://doi.org/10.1214/09-STS313)。全文状态：`FULL_TEXT_READ`。
- **研究对象/问题**：观察性研究匹配方法如何构造可比较处理/对照样本。
- **数据/变量**：方法综述；处理状态、协变量、结果，强调处理前混杂变量。
- **方法/发现**：倾向评分、精确/近邻/全匹配等；先检查共同支持与协变量平衡，匹配是分析前设计，不应只报告倾向评分模型。
- **假设/局限/证据强度**：仅控制已测混杂；未测混杂仍然存在；缺乏重叠不能靠模型修复。证据强度：高（方法综述）。
- **可用于/不能支持**：给未来学生使用差异比较时的诊断清单；如果无基线能力、动机等混杂变量，PSM 不会自动变成因果证据。

#### C5. Lipsitch, Tchetgen Tchetgen & Cohen (2010), “Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies”

- **来源/DOI**：*Epidemiology*, 21(3), 383–388. [DOI](https://doi.org/10.1097/EDE.0b013e3181d61eeb)，[作者/机构全文记录](https://dash.harvard.edu/entities/publication/73120379-21f6-6bd4-e053-0100007fdf3b)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：观察研究中的非因果关联和偏差诊断。
- **数据/变量**：方法论文；暴露、结局、负对照暴露/结局。
- **方法/发现**：构造理论上不受因果处理影响、但可暴露混杂/偏差的对照，作为敏感性/偏差探测工具。
- **假设/局限/证据强度**：负对照要有领域知识保证“不应存在该因果路径”；异常可提示偏差，正常不证明无偏。证据强度：中高。
- **可用于/不能支持**：启发模块 D 设计日志窗口、与 AI 无关的负对照结果（需数据可用）；不能凭空选对照变量。

### D. 跨学期/跨工具的测量可比性

#### D1. Putnick & Bornstein (2016), “Measurement Invariance Conventions and Reporting: The State of the Art and Future Directions for Psychological Research”

- **来源/DOI**：*Developmental Review*, 41, 71–90. [DOI](https://doi.org/10.1016/j.dr.2016.06.004)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：跨组/跨时间比较潜变量时，测量不变性检验和报告规范。
- **数据/变量**：文献方法综述；构型、因子负荷、截距/阈值等参数跨群组稳定性。
- **方法/发现**：多组 CFA/测量不变性逐级检验；不同不变性层级允许的均值比较不同。
- **假设/局限/证据强度**：针对量表/潜变量，不是任何行为指数都适用 CFA；只有共同题项/共同测量才可检验等值。证据强度：高（方法规范）。
- **可用于/不能支持**：秋春或工具组间比较前先检查同一构念、同一编码规则和共同支持；不能在任务/工具/样本完全改变时用一个标准化就宣称可比。

#### D2. Berrío, Gómez-Benito & Arias-Patiño (2020), “Developments and Trends in Research on Methods of Detecting Differential Item Functioning”

- **来源/DOI**：*Educational Research Review*, 31, 100340. [DOI](https://doi.org/10.1016/j.edurev.2020.100340)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：教育测量 DIF 检测方法及发展趋势。
- **数据/变量**：DIF 模拟研究领域综述；题项反应、潜在能力与群体身份。
- **方法/发现**：审阅约百种 DIF 方法/统计量及其应用主题，指出比较群体时需考察相同能力条件下题项是否仍有群体差异。
- **假设/局限/证据强度**：经典测试题项语境；学生自由交互的 ABL/HOT 不是现成题项反应。证据强度：中高。
- **可用于/不能支持**：作为“同等水平的学生是否因工具/学期而获得不同分数”这一差异功能问题的类比框架；不能直接跑 DIF 而无统一任务锚点。

#### D3. Gašević et al. (2023), “Towards a partnership of teachers and intelligent learning technology: A systematic literature review of model-based learning analytics”

- **来源/DOI**：*Journal of Computer Assisted Learning*, 39(5), 1397–1417. [DOI](https://doi.org/10.1111/jcal.12844)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：透明的学生学习模型如何与教师知识及课堂决策结合。
- **数据/变量**：系统综述纳入 42 篇 ITS/学习分析仪表盘研究；学生模型、教学模型、教师使用/解释。
- **方法/发现**：系统综述，关注模型假设如何与教师理解连接。
- **局限/证据强度**：主要是技术/教师决策，不是跨学期校准实验。证据强度：中。
- **可用于/不能支持**：支持报告须能解释到教学诊断并允许教师复核；不能证明秋春成绩可比。

### E. C 模块：复合指标、权重、稳健性与抗操纵

#### E1. OECD / EU / EC-JRC (2008), “Handbook on Constructing Composite Indicators: Methodology and User Guide”

- **来源/DOI**：[OECD 原始手册页](https://doi.org/10.1787/9789264043466-en)，162 页。全文状态：`FULL_TEXT_READ`（权威公开手册）。
- **研究对象/问题**：复合指标的理论框架、指标选择、归一化、权重、聚合与验证。
- **数据/变量**：方法手册，案例为国家/政策领域指标，不是学生数据。
- **方法/主要结论**：要求理论框架先行，透明说明归一化/权重/聚合和补偿性；用多模型、敏感性与不确定性分析检查排名和政策结论。输入数据、指标选取、权重和聚合都应进入不确定性讨论。
- **假设/局限/证据强度**：国家级指数经验不能直接定出学生 AIV 的权重；高质量方法参考。证据强度：高（合成流程）。
- **可用于/不能支持**：作为 C/D 报告框架；不能因为手册列出 AHP/熵权就选其一或证明客观权重。

#### E2. Saisana, Saltelli & Tarantola (2005), “Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators”

- **来源/DOI**：*Journal of the Royal Statistical Society: Series A*, 168(2), 307–323. [DOI](https://doi.org/10.1111/j.1467-985X.2005.00350.x)。状态：`ABSTRACT_ONLY`（摘要与引用信息核验）。
- **研究对象/问题**：综合指标排名对建模选择的稳健程度如何评估。
- **数据/变量**：联合国技术成就指数案例；权重、标准化和聚合选择、排名。
- **方法/发现**：把不确定性分析（输入/假设如何传播到输出）与敏感性分析（各来源贡献）结合，检查结论和排名稳定性。
- **假设/局限/证据强度**：指标的结果取决于不确定性范围设定；跨领域适用流程而非参数。证据强度：高（方法）。
- **可用于/不能支持**：直接支持对 Bloom 标签、工具归类、缺失、权重和聚合方案传播不确定性；不能指定哪种 AIV 公式正确。

#### E3. Cinelli et al. (2021), “A Framework Based on Statistical Analysis and Stakeholders’ Preferences to Inform Weighting in Composite Indicators”

- **来源/DOI**：*Environmental Modelling & Software*, 145, 105208. [DOI/出版方页](https://doi.org/10.1016/j.envsoft.2021.105208)。状态：`ABSTRACT_ONLY`（本轮核对出版方页摘要）。
- **研究对象/问题**：复合指标权重如何兼顾数据结构与利益相关者偏好。
- **数据/变量**：电力供应韧性案例；分指标信息、相关性/信息转移与偏好。
- **方法/发现**：提出衡量各指标向综合指数转移信息的指标及优化权重方案，以目标或最大化信息传递。
- **假设/局限/证据强度**：案例权重不是客观真值；特定利益相关者偏好需要明确。证据强度：中高。
- **可用于/不能支持**：说明纯数据权重与目标价值权重表达的是不同问题；本题可比较方案但须先定教育目标；不能以“熵高”直接等价“教育重要”。

#### E4. Becker, Saisana, Paruolo & Vandecasteele (2017), “Weights and Importance in Composite Indicators: Closing the Gap”

- **来源/DOI**：*Ecological Indicators*, 80, 12–22. [DOI](https://doi.org/10.1016/j.ecolind.2017.03.056)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：名义权重与指标对综合指标实际重要性之间的差异。
- **数据/变量/方法**：复合指标方法论文，借助回归/方差分解及相关结构讨论重要性。
- **主要结论**：权重系数本身不等于最终影响力；指标相关性和聚合函数会改变贡献解释。
- **局限/强度**：方法结论；非教育场景。证据强度：中高。
- **可用于/不能支持**：要求展示权重来源并补充实际贡献/敏感性；不能把熵权结果解释成教育价值重要性。

#### E5. Saltelli & Tarantola / Saisana framework; ranking robustness

- **Citation**：Seth & McGillivray (2018), “Rank Robustness of Composite Indices”. [Oxford Research Archive](https://ora.ox.ac.uk/objects/uuid%3Ac55332d1-a2aa-45e0-ab6f-a22d955c42e4)。状态：`ABSTRACT_ONLY`。
- **研究内容**：定义权重集合下排名不发生逆转的稳健比较关系，以 HDI 说明有些排序稳健、有些排序脆弱。
- **方法/指标**：对权重扰动集合进行比较，而不只报告一个排名。
- **假设/限制**：结果取决于允许的权重范围和指数结构；国家发展指数不能提供学生权重。
- **用途/不能支持**：建议报告名次分布/两两胜率或排名区间；不能把某一精确 AIV 排名当成无不确定性事实。

#### E6. Campbell (1976), “Assessing the Impact of Planned Social Change”

- **来源/DOI**：*Social Indicators Research*, 3, 237–256. [DOI](https://doi.org/10.1007/BF00286305)；重刊版本 [JMDE](https://doi.org/10.56645/jmde.v7i15.297)。状态：`ABSTRACT_ONLY`/经典理论。
- **研究对象/问题**：社会干预评价及指标在决策中被使用后的行为反应。
- **变量/方法**：社会指标与被评价行为；理论讨论指标用途及其可被目标化。
- **结论/边界**：作为 Goodhart/Campbell 思路的理论依据，指标承担高风险目标后可能诱发适应性行为；并非教育 AI 交互的直接实证。
- **用途/不能支持**：用于提出重复刷问、关键词堆砌、堆智能体等红队假设；不能证明本数据已发生操纵。

#### E7. Espeland & Sauder (2007), “Rankings and Reactivity: How Public Measures Recreate Social Worlds”

- **来源/DOI**：*American Journal of Sociology*, 113(1), 1–40. [DOI](https://doi.org/10.1086/517897)，[作者公开 PDF](https://sociology.northwestern.edu/documents/faculty-docs/faculty-research-article/rankings-and-reactivity-2007.pdf)。状态：`FULL_TEXT_READ`。
- **研究对象/问题**：法学院公开排名如何改变被评价对象行为与组织过程。
- **数据/变量/方法**：法学院排名的案例/访谈/历史资料；排名、机构响应和行为调整。
- **主要发现**：公共评价指标会引发 reactivity，被评价者会依据排名调整行为，改变测量对象本身。
- **假设/局限/强度**：组织排名情境，不能直接量化学生刷分。证据强度：中（机制证据）。
- **可用于/不能支持**：论证高风险公布 AIV 可能诱发策略性互动；支持低风险诊断和反操纵测试；不能说学生已经操纵。

### F. 标注一致性与学生主观评价

#### F1. Cohen (1960), “A Coefficient of Agreement for Nominal Scales”

- **来源/DOI**：*Educational and Psychological Measurement*, 20(1), 37–46. [DOI](https://doi.org/10.1177/001316446002000104)。状态：`ABSTRACT_ONLY`。
- **研究对象/问题**：两位评定者对名义分类的一致性，校正偶然一致。
- **数据/方法/指标**：统计方法论文；观测一致率与偶然一致率，Cohen’s κ。
- **主要结论/边界**：适用于两名评定者、名义类别；Bloom 六级有序，未经加权 κ 不利用相邻等级信息，且 κ 会受类别盛行率影响。
- **用途/不能支持**：作为报告协议之一，需同时给混淆矩阵/各类 F1/原始一致率；κ 单值不能代表标注全貌。

#### F2. Krippendorff (2018 ed.), *Content Analysis: An Introduction to Its Methodology* (reliability chapters)

- **来源**：[SAGE 书籍页面](https://us.sagepub.com/en-us/nam/content-analysis/book258450)。状态：`ABSTRACT_ONLY`（本轮未读取完整专著）。
- **研究对象/问题**：内容编码中多评定者可靠性，适用不同测量尺度和缺失编码。
- **方法/指标**：Krippendorff’s α，可用距离函数处理有序标签，也可处理多名编码员和缺失。
- **局限/强度**：具体 α 需要预先定义距离、单位与缺失规则；可靠性不等于效度。证据强度：高（方法教科书）。
- **用途/不能支持**：适用于多标注者/有序 Bloom 的候选一致性指标；不能证明 Bloom 构念本身测量了能力。

### G. 学习反馈、自评与外部效标

#### G1. Wang et al. (2022), “The Effect of Self-Assessment on Academic Performance and the Role of Explicitness: A Meta-Analysis”

- **来源/DOI**：*Assessment & Evaluation in Higher Education*. [DOI](https://doi.org/10.1080/02602938.2021.2012644)。状态：`ABSTRACT_ONLY`。
- **对象/数据**：高等教育自评干预；26 项研究、98 个效应量。
- **方法/发现**：元分析；自评干预总体正向，带有他人明确反馈的研究效果高于未提供显性反馈的研究。
- **边界**：研究的是自评实践干预对学业表现的效果，不是学生主观“感觉学得好”与客观成绩的相关性。
- **用途/不能支持**：支持反馈/反思可能是学习过程机制；不应把问卷感知直接当成学习成效。

## 3. Literature Synthesis

### A：认知标注

Bloom 分类适合描述目标和可见认知过程，但它不是能力测试。修订版分类提供共同语言（A1），课堂文本分类研究表明可对文本进行自动分类（赛题也提及相关研究），但教师提问、学生自由提问、AI 提示和学生回答不是同一种分析单位。Chan 等的比较研究提示层级细分不必然消除歧义（A2）。所以本项目应把“任务需要何种认知过程”和“学生输出展示了什么证据”作为两个可分别编码的问题，不能将任务要求层次直接替代学生能力。

AI/Bloom 文献中较直接的研究（A3）多用 Bloom 控制系统生成题目，再评估教师接受度/题目质量；这证明脚手架能重塑题目，但并不验证学生对话标注。当前检索未找到足够强的近期研究，能证明 LLM 对本题这种“学生与 AI 多轮混合对话”六级标签已经达到可替代人工的可靠性。故需本地小样本双人盲标，报告六级混淆矩阵、加权/非加权一致性、低/中/高折叠结果，并对学生发言/AI 发言边界分别校验。三阶折叠一般会降低标签细节和可能的分歧，但是否显著改善一致性必须由本语料实测，不能先验保证。

可靠性回答“评定者是否一致”；效度回答“标签是否支持我们声称的解释”。A4–A6 要求把整条解释链逐步论证。自动标签即使与人工高度一致，最多说明复制了人工代码本判断，不能单独证明标签代表独立能力。

### AI 脚手架与认知卸载

实验结果显示 AI 产生的帮助可提高即时完成表现，但独立考试结果可能不同（B2）；另一项结构化 AI tutor RCT 在特定物理任务中优于主动学习（B3）。这不是矛盾，而是处理设计、对照条件、任务和结局不同。写作 RCT 也发现作文输出改善不必然伴随知识获得/迁移改善（B4）。实验元分析（B5）明确建议使用客观、复杂任务与长程结果，分开评 AI 产出和学习效果。

A3 直接表明 Bloom 目标可写进提示控制生成问题。对本赛题而言，探知侠按六级递进、逆行侠由创造目标向下回溯，本身就可能改变对话顺序、动词和认知层级频率。因此“高层级占比变化”至少同时受学生状态、任务、脚手架路径、AI 回应与记录机制影响。交互量可作为过程证据或可能机制，除非独立验证，不能等同学习结果。

### B：因果/增量识别

B2/B3 的高强度证据来自明确对照和随机分配；而附件主要是已发生的交互记录。观察性因果研究先指定处理策略、时间零点、结果、随访和估计目标，再检查现有数据是否能映射（C1）。PSM 只在有足够的处理前混杂变量和共同支持时，可帮助构造可比组；诊断平衡是关键，未观测混杂仍无法消除（C4）。DID 需要可比组的前后变化和可信平行趋势；在多期/异质处理效应下需选择匹配 estimand 的估计器（C2–C3）。

当前附件没有明确的无 AI 组、课程共同的前测和独立后测信息。即使学生自选择使用不同智能体，也可能由基础、动机、任务需求共同决定。仅以当前表格，模块 B 最稳妥的结论等级为**条件关联/描述性过程差异**；只有补齐合适的前置协变量、时间排序、可比结局和对照设计后，才可能把结论提升到准因果。不能把秋春平均值差称为 AI 增量。负对照/安慰剂测试可探测某些偏差，但不能证明完全无混杂（C5）。

### 跨学期可比性

秋春数据在学生名单、记录字段、时间窗、AI 工具组合、课程/任务构成方面都可能改变。测量不变性文献指出，均值比较前要确认测量结构与尺度等值；DIF 可帮助思考相同潜在水平学生在不同组是否有差异性测量（D1–D2）。但 ABL/HOT 是行为构造指标，不是成熟量表或共同试题，传统多组 CFA/IRT 并非可直接套用。至少需要相同任务/共同锚点、同一编码协议、共同支持及对班级/课程/工具差异的分层说明；若这些条件不满足，应限制比较人群和结论，而不是只做 z 标准化。

### C：综合指标

复合指标的首要选择不是权重算法，而是概念框架、指标定义、方向/量纲、归一化、补偿性和目标用途。OECD/JRC 手册（E1）要求披露每项判断，多模型比较，并用敏感性/不确定性分析检验排名与政策结论。Saisana 等（E2）把不确定性传播与敏感性贡献分开；权重名义值也不等同变量实际重要性（E4）。排名可能对合理权重范围敏感（E5）。

这支持并行比较等权、理论/利益相关者设定、数据驱动权重等候选，而不支持预先认定 AHP、熵权、TOPSIS 中任一为真值。若一项分数更高可以完全补偿另一项极低表现，需论证这种补偿是否合乎教育目标。区间/分布和排名稳定性比伪精确单点排序更诚实。当前不定义 AIV 公式。

### 抗操纵

Campbell 与 Espeland/Sauder 的理论/案例表明，指标成为评价目标后会影响行为与组织策略。对 AIV 的合理红队假设包括重复提交相似提问、关键词堆砌、诱发 AI 输出高阶任务、把 AI 回答错计为学生证据、堆叠更多智能体以抬高广度。它们目前是待测风险，不是本数据已存在操纵的证据。可测试重复/去重、关键词删改、剥离 AI 回答、限制同一任务对计数、广度饱和和标签置信度变化下的排名稳定性。规则须在结果计算前固定并做对抗样本测试。

### 不确定性传播

复合指标手册与 Saisana 等提供直接理论基础：对输入数据、缺失、归一化、权重、聚合的合理不确定范围重复计算，并把它传播到指数和排名。映射到本题，可用人工双标差异形成 Bloom 混淆/概率标签，对学生语句和智能体类型的低置信识别设置类别概率或多重抽样，再重算 ABL/HOT、CTQ/DHI/MAB/AIV 候选及排名分布。需要区分标注者一致性、标签概率校准与学习结果因果不确定性，它们不是同一种误差。当前论文证据支持这套评估思路，但尚未找到完全相同的“Bloom 多轮对话标签→AIV 排名”现成算法；这是潜在方法贡献，而非已经有现成公式。

## 4. Research Gaps

1. **分析单位未统一**：不少 Bloom 自动分类研究针对教师编写题目或系统生成题目，本赛题则有多轮对话、学生输入与 AI 回答混合、部分纯链接记录。
2. **构念效度缺口**：高阶任务/问题与学生实际展示的高阶能力不是同一构念；独立思考和 AI 供给内容之间缺少来源归因证据。
3. **六级到三阶的实证缺口**：分类合并是否提高本数据的一致性、保留多少诊断信息，需要分层人工校验，不能照搬外部结论。
4. **AI 路径混淆缺口**：脚手架能机械改变问题顺序和层次；现有一般 AI tutoring 研究没有直接校正探知侠/逆行侠的提示设计。
5. **结果效标缺口**：日志缺少统一前测、无 AI 后测、延迟保持/迁移证据时，不能估计长期学习增量。
6. **跨期可比性缺口**：秋春名单、课程、记录工具和测量窗口需重建；缺共同任务锚点时，“校准”无法凭公式保证等值。
7. **综合指标验证缺口**：AIV 各留白指标的理想分布、边界和教育解释需项目自身论证；文献提供设计原则，不给现成权重。
8. **排名抗操纵缺口**：需要用重复/关键词/AI 代答/工具堆叠等可复现红队样本直接测量脆弱性。
9. **误差联合传播缺口**：现成不确定性方法可迁移，但 Bloom 误标、学生/AI 话语分离、智能体识别和抽样误差需在本语料中量化。
10. **文献精读缺口**：部分方法文献本轮仅核摘要；正式论文引用数值前需精读全文，尤其 Faber 具体样本与效果、Deng 元分析纳入数/异质性、各本地课程评价字段说明。

## 5. Implications for This Competition

### A 模块

- 把编码单位和发言主体写进代码本：学生问题/回答、AI 追问、AI 解释分别标记；学生文本被 AI 改写时标注归属不确定。
- 分开定义“任务认知要求”和“学生可见表现证据”；高 Bloom 问题只可解释为任务/交互特征，除非有独立效标验证。
- 抽样兼顾学期、智能体、六级类别、文本长度和模型置信度；低置信/分歧/稀有类别过抽样，最终用抽样权重校正一致性/总体比例。
- 一致性报告至少包括六级混淆矩阵、每类支持量、原始一致率、适合序数类别的 α 或加权 κ，以及低/中/高三阶重算结果。人工一致性是标签可信度，不是构念效度。

### B 模块

- 先以 target trial 表述理想问题（对象、AI 策略、对照、时间零点、独立结局、随访和 estimand），再逐项标出现有数据对应或缺失。
- 当前可报告工具使用、互动深度、文本认知特征和反馈的关联；将独立学习增益/因果效应标为当前不可识别，除非找到外部前后测/合理对照。
- 不用两学期均值差直接称 AI 效应。PSM 要有处理前混杂和重叠；DID 要有处理组/对照组、多个时点与可信趋势。
- 若要做未来研究，优先补共同的基线能力测量、标准化独立后测/延迟迁移测验、明确工具暴露和班级/课程/教师信息，必要时随机或分阶段实施。

### C 模块

- 先论证 ABL/HOT/CTQ/DHI/MAB 各自测量含义、方向、有界性和可比条件；权重与聚合方案随后才是比较对象。
- 比较多套透明基线方案；报告指标间相关、重复计数/补偿性、单项扰动、权重扰动以及排名变化。
- 将标签/主体识别/缺失的不确定性传到学生分值与排名；同时单列数据覆盖与置信度，不把低置信结果强行压成精确分数。
- 不预选 AHP、熵权、TOPSIS；权重反映的目标不同，需说明目标、可解释性和敏感性后再选。

### D 模块：红队与复现

- 对每条结论给出数据筛选规则、字段字典、脚本和随机种子；检查重复记录、链接缺文、名单匹配以及日期范围。
- 对关键词堆砌、重复高阶问题、复制 AI 回答、改变对话长度、虚增智能体类型数做攻击样本；观察指标与排名是否超比例变化。
- 报告分类错误传播和排名稳定性。每个显著结论都应能在干净分析队列上独立重算。
- 在报告学生级结果时使用脱敏标识并控制小群体披露；分数作为教师诊断线索，不作高风险个体决策。

## 6. Method Candidate Table（仅候选，不做最终选择）

| 候选方法 | 要解决的问题 | 数据要求 | 关键假设 | 优点 | 风险 | 当前数据可能支持？ |
|---|---|---|---|---|---|---|
| 分层人工双标 + Cohen κ / 加权 κ / Krippendorff α | Bloom 编码可靠性 | 原始学生/AI语句、代码本、独立标注、抽样层信息 | 分析单位一致；标注独立；序数距离预先定义 | 可审计，揭示类别混淆 | 一致不等于有效；稀有类/偏斜会影响 κ | 可支持；需重抽样标注 |
| 低置信/分歧优先复核、序贯抽样 | 控制人工成本又保证类别质量 | 预标置信度、层/时间/工具分组及人工复核标签 | 抽样概率可记录；停止规则预先设定 | 将人工用在最不确定部分 | 若只抽低置信，不能无权估总体一致性 | 可支持，须加随机审计样本 |
| 多标签/概率标签传播（Monte Carlo 或 bootstrap） | 上游误差如何改变 AIV 与排名 | 双标混淆矩阵、主体识别置信度、学生聚合记录 | 误差机制可从校验样本估计；抽样代表目标层 | 结果是区间/排名分布，透明 | 若混淆矩阵小样本不稳，概率会失真 | 可支持，校验数据为先决条件 |
| 独立结果效度/相关验证 | Bloom 交互指标是否对应学习表现 | 无 AI 后测、前测、延迟保持/迁移、文本 | 效标可靠且时间关系明确 | 直接连接交互指标与目标构念 | 本附件未见相应成绩 | 当前不支持（需确认其他数据） |
| 分层描述/多层回归 | 描述工具/班级/基础分层关联 | 学生级结果、班级/学期/工具字段、协变量 | 模型规格合理；时间顺序清楚 | 估关联、异质性与聚类结构 | 混杂未控不可因果解释 | 部分可能；需清洗出队列/工具 |
| 倾向评分匹配/加权 | 可观测混杂条件下处理组比较 | AI策略组/对照组、处理前协变量、结果、共同支持 | 一致性、可交换性、正值性、无未测混杂 | 可检查协变量平衡，设计透明 | 无未测混杂无法检验；无对照/基线时失效 | 目前证据不足，不能承诺因果 |
| DID / group-time ATT / 事件研究 | 政策/工具变化前后的差分 | 多时期处理组与对照组结果、处理时间、前趋势 | 平行趋势、无预期/溢出等 | 可扣除共同时间变化 | 两学期不同学生且只有前后标签不等于 DID；前趋势无力证明假设 | 目前不支持，除非找到额外时期/对照 |
| 测量不变性 / DIF / 共同锚点校准 | 判断秋春/工具指标可比性 | 共同测验/共同任务或稳定测量模型、组别和样本 | 构念结构/锚点一致 | 明确哪些比较可做 | 缺锚点时模型不识别或只是强假设 | 当前仅可检查文本规范/分布，不足完整检验 |
| 透明规则权重、等权基线、多方案对照 | 权重与聚合选择 | 标准化后有效指标、教育目标说明 | 正向方向、尺度可比、权重有解释 | 简单可复算，可与复杂法对照 | 等权也含价值判断；线性可补偿 | 可在指标定义后进行方案比较 |
| 经验/数据驱动权重（回归、熵、偏好结合） | 探索指标信息或预测关联 | 足量且外部效标可靠数据，偏好样本 | 训练/验证分离；目标函数对应教育目标 | 可估信息量/预测关联 | 熵≠重要性，回归权重依赖效标，可能过拟合 | 不建议当前直接据此定权 |
| 权重/标准化/聚合敏感性与排名稳健性 | 单点排名是否脆弱 | 候选模型、权重/参数可接受域、学生指标 | 可接受域有实质依据 | 直接呈现结论稳定区间 | 域任意会决定结果 | 可支持，适合 C/D |
| 抗操纵对抗测试 / 去重 / 饱和诊断 | 指标是否被低成本游戏化 | 原始交互文本、重复相似度、工具身份、测试样例 | 攻击覆盖主要可操纵路径 | 对红队问题直接 | 攻击样本不等于真实行为发生率 | 可支持测试，不能推断现实作弊率 |
| 负对照 / placebo / 定量敏感性 | 检查某些未测混杂/伪效应 | 明确无因果路径的对照变量、时间信息 | 负对照确实满足理论条件 | 可发现模型或时间偏差 | 阴性结果不能证明无混杂 | 需先看字段；目前待核 |

## 7. 建模前研究决策：下一阶段必须回答

1. **目标效标是什么？** 是否有学生使用 AI 前的基线、无 AI 独立后测、延迟保持或迁移任务？若都没有，AIV 的“学习增量”应如何限定为交互证据而非真实增益？
2. **分析单位和话语归属如何定？** 一行是一轮、一条问题还是整段对话？如何分离学生/AI 文本、学生复述 AI、链接型和重复型记录？
3. **春秋分析队列与可比对象如何确定？** 2026 春 1,925 行的完整筛选规则、四份名单 133 人并集与 109 人日志匹配差异、课程/班级/教师/任务/日期是否可追溯？
4. **AI 处理/路径的精确定义是什么？** 工具使用、某智能体路径、提示强度、互动轮数和采纳程度分别是什么处理；能否与学生先前基础/自选择区分？
5. **AIV 计划服务何种用途与谁？** 是形成性教师诊断还是学生排名/管理问责？是否允许维度补偿、跨组比较和个体决策？用途决定所需效度证据及抗操纵强度。

## 8. S2 交付结论

现有文献支持把学生可观察交互看作“需要效度论证的学习过程证据”，把 AI 辅助任务表现与独立学习结果分开，把脚手架路径视作重要解释因素，并对因果估计、跨学期比较和复合排名设置数据条件。现有附件当前最强支持是描述性/条件关联与测量可靠性分析；未发现足够证据支持直接宣称 AI 因果增量。S3 前优先确定独立学习效标是否存在、分析队列与分析单位、学生/AI 话语分离规则和评价用途。**本文件不包含最终 AIV 公式、模型训练或最终模型选择。**
