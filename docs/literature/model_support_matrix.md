# 文献增强：Observed AI Increment → Evidence Reliability → Reliable AI Increment → ACCEPT / ABSTAIN

## 使用说明

本表服务于已经冻结的研究主线，不改变研究问题、变量定义、权重、阈值或 R1/R2 协议。文献被分成四类支持：**理论依据**（为什么要区分观察表现、证据和真实学习）、**数学方法**（可直接借鉴的统计量/决策规则）、**变量选择**（应记录哪些证据与缺失状态）、**验证方法**（如何检验可靠性、校准、覆盖率和边界）。

当前项目的 `Evidence Reliability` 是有界的支持权重，不是未经外部校准的概率；`Reliable AI Increment` 只有在存在合法的 baseline-paired `Delta_raw` 时才有定义；`ABSTAIN` 必须和 coverage 一起报告。以下论文不能替代正式人工 R1/R2，也不能把日志观察差异变成 AI 的因果学习增益。

## 支持矩阵

| 论文 | 研究问题 | 核心方法 | 关键结论 | 可以支持当前模型哪一部分 | 可直接借鉴的公式/验证设计 | 与当前项目的差异 | 是否建议引用正文 | 是否建议只放附录 | 风险/限制 |
|---|---|---|---|---|---|---|---|---|---|
| Soderstrom & Bjork (2015), *Learning Versus Performance: An Integrative Review*, Perspectives on Psychological Science, DOI [10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000) | 即时训练表现能否代表持久学习？ | 整合学习心理学中表现、保持、迁移的证据 | 即时表现和较持久的学习可分离，甚至方向相反 | **理论依据；变量选择**：Observed performance 不能直接命名为 true learning | 将独立后测、延迟保持、迁移作为外部效标；报告 `observed performance` 与 `independent outcome` 的相关/差异，而非替代 | 非 GenAI 专门研究；不提供本项目权重 | **是** | 否 | 不能量化本项目学生的学习增益 |
| Bastani et al. (2025), *Generative AI without guardrails can harm learning: Evidence from high school mathematics*, PNAS, DOI [10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122) | AI 辅助练习表现与撤去 AI 后的独立表现是否一致？ | 现场随机试验；GPT Base、GPT Tutor、控制组；辅助练习与无资源测试分离 | 辅助练习提高不必然带来独立测试提高；学生感知与实际结果也可不一致 | **理论依据；变量选择；验证方法**：要求分开记录 AI-assisted outcome、独立 outcome、感知 | 预注册 `Y_assisted`、`Y_unassisted`、保持/迁移；用组间差和置信区间，禁止把日志分数直接叫 learning gain | 高中数学、特定 GPT tutor 和短期试验；不能外推本项目效应 | **是** | 否 | 这是因果证据，但只对其随机分配场景成立，不能证明本项目日志有同样效应 |
| Fan et al. (2025), *Beware of Metacognitive Laziness*, British Journal of Educational Technology, DOI [10.1111/BJET.13544](https://doi.org/10.1111/BJET.13544) | 生成式 AI 改善产出是否也改善知识、迁移和自我调节？ | 随机实验与过程序列分析，多维结果测量 | 作文产出改善可与知识增益/迁移不一致；过程路径是重要解释变量 | **理论依据；变量选择**：AI path、学生自我调节和独立结果应分列 | 同时报告过程指标、即时产出、知识后测和迁移；不要用过程分数替代结果效标 | 写作任务、117 名大学生、特定工具；不直接验证数模对话 | **是** | 否 | 不能将其效应量迁移到本项目 |
| Gašević, Greiff & Shaffer (2022), *Towards Strengthening Links between Learning Analytics and Assessment*, Computers in Human Behavior, DOI [10.1016/j.chb.2022.107304](https://doi.org/10.1016/j.chb.2022.107304) | 学习分析日志如何与正式测量和评价连接？ | 学习分析与 assessment 的效度框架 | 日志指标必须经过任务、构念、可信度、公平性和结果效度论证 | **理论依据；验证方法**：把文本→标签→指标→解释写成可审计推论链 | 对每一层写 claim、warrant、反例和验证数据；把 coverage/missingness 作为测量条件 | 专刊导言/框架，不给本项目指标效度系数 | **是** | 否 | 不能代替本地验证数据 |
| Gray & Bergner (2022), *A Practitioner’s Guide to Measurement in Learning Analytics*, Handbook of Learning Analytics | 学习分析数据怎样成为可靠、有效的测量？ | 测量论实践指南：观测数据、潜在构念、误差与使用 | 先问数据测量什么、可推断什么，再定义指标和用途 | **理论依据；变量选择**：将 evidence、target construct、intended use 分离 | 建立 measurement argument；分别审计 construct validity、reliability、fairness 和 use validity | 手册章节，不是本项目实证 | **是** | 否 | 不能证明某个 Bloom 证据已经代表稳定能力 |
| Kane (2013), *Validating the Interpretations and Uses of Test Scores*, Journal of Educational Measurement, DOI [10.1111/jedm.12000](https://doi.org/10.1111/jedm.12000) | 分数解释和使用的推论如何验证？ | Interpretation/use argument；逐项检查推论与假设 | 支持“分数解释”不等于支持“把分数用于决策”；用途越强，证据要求越高 | **理论依据；验证方法**：形成性诊断用途需和排名/奖惩用途分开 | 对 `ACCEPT` 记录列出 observation→scoring→generalization→extrapolation→decision 假设；任何关键假设失败则拒判 | 测验分数语境；不提供本项目阈值 | **是** | 否 | 是论证框架，不是统计检验本身 |
| Krathwohl (2002), *A Revision of Bloom’s Taxonomy*, Theory Into Practice, DOI [10.1207/s15430421tip4104_2](https://doi.org/10.1207/s15430421tip4104_2) | 如何描述认知过程和知识维度？ | 修订 Bloom 二维分类 | 六类认知过程是教学目标/评价语言，不是能力真值 | **变量选择**：支持 Task Bloom 与 Student Evidence 双轴，但不支持直接能力解释 | 保留任务要求与学生可见证据两列；检验两轴信息量和混淆矩阵 | 理论分类，没有本地标注效度 | **是** | 否 | 高等级问题不自动表示高等级学习 |
| Cohen (1960), *A Coefficient of Agreement for Nominal Scales*, Educational and Psychological Measurement, DOI [10.1177/001316446002000104](https://doi.org/10.1177/001316446002000104) | 两名评定者的名义分类一致性如何扣除偶然一致？ | Cohen's kappa：`kappa=(p_o-p_e)/(1-p_e)` | κ 受类别盛行率影响；单一 κ 不能替代混淆矩阵和类别支持量 | **验证方法**：支持人工标注一致性报告 | 输出原始一致率、混淆矩阵、每类支持量和 κ；不要只报一个系数 | 本项目冻结的是同一标注者 test-retest，不是两名标注者 | **是** | 否 | 六级是有序标签，未加权 κ 丢失相邻等级信息；不能证明构念效度 |
| Krippendorff (2018), *Content Analysis: An Introduction to Its Methodology*, SAGE | 多评定者、缺失和有序内容编码如何评估可靠性？ | Krippendorff's alpha，按测量尺度定义距离函数，可处理缺失 | α 可按名义/序数距离扩展；可靠性仍不等于效度 | **数学方法；验证方法**：支持序数标签和缺失状态的 reliability 审计 | `alpha=1-D_o/D_e`；预先冻结 ordinal distance、缺失规则、分析单位，并报告 bootstrap CI | 专著方法；项目当前单人重测设计需明确是 intra-rater 结果 | **是** | 否 | 小样本/稀有类时 CI 很宽；不同距离函数会改变结果 |
| Putnick & Bornstein (2016), *Measurement Invariance Conventions and Reporting*, Developmental Review, DOI [10.1016/j.dr.2016.06.004](https://doi.org/10.1016/j.dr.2016.06.004) | 跨学期/工具比较前，测量尺度是否相同？ | 多组测量不变性：构型、负荷、截距/阈值 | 只有达到相应不变性层级，跨组均值比较才有解释基础 | **验证方法；变量选择**：支持秋春/agent 组比较前的可比性检查 | 若有共同任务/锚点，逐级比较模型；没有共同测量则标记不可比/条件比较 | ABL/HOT 不是现成量表，不能机械套 CFA | **是** | 否 | 需要共同题项/锚点；标准化不能创造不变性 |
| Saisana, Saltelli & Tarantola (2005), *Uncertainty and Sensitivity Analysis Techniques for Composite Indicators*, JRSS-A, DOI [10.1111/j.1467-985X.2005.00350.x](https://doi.org/10.1111/j.1467-985X.2005.00350.x) | 综合指标结果对输入和建模选择有多敏感？ | 不确定性传播 + 全局敏感性分析 | 应区分不确定性来源及其对指数/排名的贡献 | **数学方法；验证方法**：支持 Reliability 参数、标签不确定性和缺失状态的压力测试 | 对标签/主体识别/缺失/权重采样，重算 `Score_adj`、support、coverage 和排名；报告区间而非单点 | 国家综合指数案例；不提供教育权重 | **是** | 否 | 结果依赖可接受参数域；不能产生“真权重” |
| OECD/EU/EC-JRC (2008), *Handbook on Constructing Composite Indicators* | 复合指标如何透明构建和验证？ | 理论框架、归一化、权重、聚合、敏感性和不确定性流程 | 权重、补偿性和聚合方式都是价值/模型选择，必须公开并做多方案比较 | **数学方法；验证方法**：支持当前 Raw/Adjusted 分开、消融和敏感性 | 预先说明方向、边界、补偿性；比较等权/冻结权重/区间权重；报告 rank robustness | 政策指标手册，不指定本项目公式 | **是** | 否 | 不能把手册示例当成 AIV 的实证支持 |
| El-Yaniv & Wiener (2010), *On the Foundations of Noise-Free Selective Classification*, JMLR, 11, 1605–1641 | 分类器何时应拒绝预测？拒判如何与风险/覆盖权衡？ | Selective classification；选择函数 `g(x)`，预测器 `f(x)`，coverage 与 selective risk | 允许 abstain 可降低保留样本风险，但代价是覆盖下降；需同时报告 risk-coverage 曲线 | **数学方法；验证方法**：直接支持 `ACCEPT / ABSTAIN` 和 coverage | `coverage=P(g(X)=1)`；`R_sel=E[L(f(X),Y)|g(X)=1]`；报告 coverage、selective risk、曲线和阈值敏感性 | 传统分类标签、风险通常可观测；本项目是证据支持不足/冲突，不是单纯分类置信度 | **是** | 否 | 不能把低 coverage 自动说成模型更好；需要外部 outcome 或人工审计标签 |
| Geifman & El-Yaniv (2017), *Selective Classification for Deep Neural Networks*, NeurIPS | 深度模型怎样用置信度进行选择性预测？ | 以 softmax/风险阈值建立 selective prediction；比较 coverage-risk | 置信度阈值可形成经验 risk-coverage trade-off，但必须在独立校准/测试数据评估 | **数学方法；验证方法**：为拒判门槛提供实验设计 | 在校准集选择阈值；测试集报告 `risk@coverage`、AURC 或分层 coverage；不在结果集调阈值 | 本项目不是神经网络分类器，Reliability 权重不是 softmax probability | **是** | 否 | 置信度错校准会导致“自信地接受”；本项目需先验证 confidence 字段含义 |
| Guo et al. (2017), *On Calibration of Modern Neural Networks*, ICML | 预测置信度是否等于实际正确率？ | Reliability diagram、ECE、temperature scaling | 现代模型可严重过度自信；校准要在独立数据上评估和修正 | **数学方法；验证方法**：支持把 `confidence` 与 Reliability 概率严格区分 | 若未来将 reliability 解释为概率，使用 `ECE=sum_b |B_b|/n * |acc(B_b)-conf(B_b)|`、reliability diagram、校准集/测试集分离 | 项目当前 `c_i` 是假设支持分，不是模型概率；不能直接套 temperature scaling | **是** | 否 | ECE 对分箱敏感；无真实 outcome 时无法校准概率 |
| Angelopoulos et al. (2024), *Conformal Risk Control*, ICLR | 如何在有限样本下控制风险并保留可解释覆盖？ | Conformal calibration；按损失和目标风险选择阈值 | 在交换性等条件下可给出有限样本风险控制保证，允许按目标风险调覆盖 | **数学方法；验证方法**：为“支持不足则拒判”提供可升级的风险控制路线 | 用校准集选择最小阈值 `lambda` 使经验上界不超过目标风险；报告 coverage 与风险上界 | 需要可交换样本和可定义的外部损失；当前没有足够人工真值，不应声称已有 conformal guarantee | 视篇幅正文方法展望 | **是** | 不能用来证明当前冻结权重或阈值正确；小样本保证会很宽 |
| Little & Rubin (2019), *Statistical Analysis with Missing Data*, 3rd ed. | 缺失证据如何区分、建模和传播？ | MCAR/MAR/MNAR 框架；多重插补、加权和敏感性分析 | 缺失机制决定可识别性；缺失不等于零值，MNAR 需要敏感性分析 | **理论依据；变量选择；验证方法**：支持 `NO_EFFECTIVE_EVIDENCE` 与 missingness 单列 | 建立 missingness indicator；报告 missingness pattern；在合理机制下做多重插补/极端情景 bounds；缺失证据不填 0 | 当前文本缺失、未来 AI 内容和 unknown agent 还涉及测量/来源错误，不只是 MAR | **是** | 否 | 插补不能恢复未观测学习证据；机制假设必须透明 |
| Rubin (1976), *Inference and Missing Data*, Biometrika, DOI [10.1093/biomet/63.3.581](https://doi.org/10.1093/biomet/63.3.581) | 在什么条件下可以从缺失数据进行推断？ | 缺失机制与似然/贝叶斯推断 | 忽略缺失机制会产生偏差；可忽略性是有条件的假设 | **理论依据；变量选择**：支持把 evidence missingness 当作数据状态而非负表现 | 为每条记录保留 observation indicator `M`; 按 MCAR/MAR/MNAR 做敏感性分层，不把 `M=1` 记为 low score | 原论文是一般缺失数据理论，不是教育 AI 语境 | 可与 Little & Rubin 二选一正文 | **是** | 缺失机制无法仅凭当前日志验证 |
| Parasuraman & Riley (1997), *Humans and Automation: Use, Misuse, Disuse, Abuse*, Human Factors, DOI [10.1518/001872097778543886](https://doi.org/10.1518/001872097778543886) | 人与自动化系统如何产生过度依赖、弃用或误用？ | 自动化使用行为的概念框架 | 自动化错误会引发 misuse；不信任或忽略会引发 disuse；界面和情境影响依赖 | **理论依据；变量选择**：支持记录 AI guidance、采纳、质疑、改写和路径偏差 | 将 `AI_suggestion` 与 `student_evidence` 分离；增加 adoption/challenge/rework provenance；做剥离 AI 回答的敏感性检查 | 经典自动化研究，不是教育 LLM 实验 | **是** | 否 | 机制框架不能证明本项目存在自动化偏差 |
| Skitka, Mosier & Burdick (2000), *Does Automation Bias Decision-Making?*, International Journal of Human-Computer Studies, DOI [10.1006/ijhc.1999.0341](https://doi.org/10.1006/ijhc.1999.0341) | 自动化建议是否导致人忽略冲突证据？ | 人机决策实验；automation bias、commission/omission errors | 人可能把自动化建议当作默认答案，增加遗漏和盲目采纳 | **理论依据；变量选择；验证方法**：支持 prompt-induced、AI-origin 和 conflict evidence 标记 | 设计 AI 正确/错误、学生采纳/质疑的分层审计；比较有无 AI context 的 evidence attribution | 航空/决策任务，非学习增益研究 | **是** | 否 | 不能把实验中的偏差率外推到学生群体 |
| Bansal et al. (2021), *Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance*, CHI, DOI [10.1145/3411764.3445717](https://doi.org/10.1145/3411764.3445717) | AI 解释何时改善或损害人机团队决策？ | 人机协作实验；解释、信任、依赖和团队表现 | 解释不必然改善互补表现；信任与实际可靠性之间可能错配 | **理论依据；验证方法**：支持把 confidence/acceptance 与 correctness 分开核验 | 记录 AI reliability、student reliance、human override；报告条件化 performance，而不是只报主观信任 | 决策支持而非教育学习；不能提供本项目学习结局效应 | 可作为正文补充 | **是** | 需要明确外部效标，不能用“信任”替代学习证据 |
| Hernán & Robins (2022), *Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available*, American Journal of Epidemiology, DOI [10.1093/aje/kwab249](https://doi.org/10.1093/aje/kwab249) | 观察数据如何明确一个可识别的因果问题？ | Target trial：人群、处理、时间零点、结局、随访、estimand | 先写理想试验再检查数据映射；框架不能弥补未测混杂或无对照 | **理论依据；验证方法**：限定 `Delta_raw` 何时才有资格叫 increment | 明确 baseline pairing、AI strategy、counterfactual outcome、follow-up；缺一项就降为描述性/条件关联 | 当前项目缺少独立无 AI 结果和完整分配机制 | **是** | 否 | 不能把 target-trial 表格误写成已经识别因果效应 |

## 最值得正文引用的 5–8 篇

1. **Soderstrom & Bjork (2015)**：最直接解释 observed performance ≠ durable learning。
2. **Bastani et al. (2025)**：高质量随机证据，说明 AI 辅助表现与撤去 AI 后测可以分离。
3. **Kane (2013)**：支持“分数解释”和“分数用途”分开论证，适合形成性诊断边界。
4. **Gašević et al. (2022)**：把学习分析日志放回测量效度和评价框架。
5. **Saisana et al. (2005)**：直接支撑不确定性传播和敏感性分析。
6. **El-Yaniv & Wiener (2010)**：为 risk–coverage 与 selective prediction 提供正式基础。
7. **Guo et al. (2017)**：说明 confidence 不是概率，支撑校准要求。
8. **Hernán & Robins (2022)**：约束 `Observed AI Increment` 不被误写为因果增量。

## 最能支撑 Reliability 的论文

- **Gray & Bergner (2022)**、**Gašević et al. (2022)**、**Kane (2013)**：测量、解释和用途的效度论证。
- **Cohen (1960)**、**Krippendorff (2018)**：标注一致性统计；项目应保留混淆矩阵、支持量和 test-retest 边界。
- **Guo et al. (2017)**：若将 reliability 进一步概率化，必须在有真值的校准集上验证。
- **Saisana et al. (2005)**：把标签、缺失、权重和聚合不确定性传播到最终分数与 coverage。

## 最能支撑 abstention 的论文

- **El-Yaniv & Wiener (2010)**：`coverage` 与 `selective risk` 的基本定义。
- **Geifman & El-Yaniv (2017)**：用独立校准集选择拒判阈值并画 risk–coverage 曲线。
- **Angelopoulos et al. (2024)**：在条件满足时将拒判升级为有限样本风险控制；当前只能作为后续方法储备。
- **Little & Rubin (2019)**、**Rubin (1976)**：证据缺失应保留为状态并进入敏感性分析，不能当作零分。

## 最能解释 observed performance ≠ true learning 的论文

- **Soderstrom & Bjork (2015)**：学习与表现的经典区分。
- **Bastani et al. (2025)**：AI 辅助练习与无 AI 独立测试的现场 RCT。
- **Fan et al. (2025)**：生成式 AI 产出改善与知识/迁移改善分离。
- **Krathwohl (2002)**：Bloom 是认知过程分类语言，不是稳定能力测量。

## 可以直接增强当前数学模型的论文

1. **El-Yaniv & Wiener (2010)**：把 `ABSTAIN` 评估改成 coverage–risk 对，而不是只报告接受样本的平均分。
2. **Geifman & El-Yaniv (2017)**：为拒判阈值制定独立校准/测试分离和 risk–coverage 曲线。
3. **Guo et al. (2017)**：若将 `c_i` 解释成概率，增加 ECE/reliability diagram；在没有真值时保持“支持权重”表述。
4. **Saisana et al. (2005)**：对 `lambda_prompt`、`lambda_context`、`r_medium`、标签和缺失机制做联合敏感性/区间传播。
5. **Little & Rubin (2019)**：把 missingness indicator 与 `NO_EFFECTIVE_EVIDENCE` 纳入状态空间，禁止以 0 代替缺失。
6. **Kane (2013)**：为 Raw → Reliability → Adjusted → decision 的每一跳建立可证伪验证清单。

这些是对现有冻结模型的验证和报告增强，不是要求现在修改模型、权重或 Gate 阈值。

## 看起来相关但实际上不服务主任务的论文/材料

| 类型 | 为什么看起来相关 | 为什么不服务当前主任务 |
|---|---|---|
| 只评估 ChatGPT 输出质量、事实性或题目生成质量的论文 | 都使用教育 AI 和“质量”指标 | 不测学生可观察证据、Reliability 或独立学习结果；不能支撑 AIV。
| 只报告学生满意度、信任或使用意愿的调查 | 有 perception/acceptance 变量 | 主观感知不是学习效标；最多是协变量或机制线索。
| 只在单一数据集上优化 Bloom/认知分类器准确率的工程论文 | 与 Task/Evidence 标签词汇相同 | 若没有人工协议、混淆矩阵、外部效度和学生/AI 归属审计，不能证明本项目标签可靠。
| 仅用即时作业分数宣称长期学习提升的 AI tutor 研究 | 有 performance gain | 缺少撤去 AI、保持或迁移测验，无法支持 true learning。
| 只给出一个复合分数或排名、没有权重/缺失/敏感性分析的指标论文 | 形式上像 AIV 指数 | 不能支撑当前项目的 Reliability、support 或 abstention 边界。
| 用 PSM/DID 的教育观察研究但无处理前协变量、共同支持、时间零点或可信趋势 | 方法名与增量评价相关 | 估计器不会创造因果识别条件；当前项目只能保持描述性/条件关联。
| 被撤稿的 ChatGPT 元分析（例如 Wang & Fan 2025, HSSC, DOI [10.1057/s41599-025-04787-y](https://doi.org/10.1057/s41599-025-04787-y)） | 摘要可能给出漂亮的总体效应 | 撤稿后不得作为支持性证据或引用效应量，只能作为文献审查风险示例。

## 引用纪律

- 论文支持的是“该论文设计下的结论”；不得把相关性写成因果，把模型校准写成当前数据已校准，把拒判风险覆盖写成当前 Gate 已通过。
- 正文引用时保留场景、样本和结果时点；跨领域方法论文用于公式和验证设计时，明确标注“方法依据”，不冒充教育实证。
- 当前正式人工 R1/R2 未返回前，所有 Reliability 结论仍限于协议、开发数据和待验证设计；不得引用本表替代正式 Gate。
