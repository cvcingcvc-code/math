# S3 验证与红队计划

> **DECISION** 以下为预注册式候选验证计划，不代表已运行的结果。先完成清洗、人工标注和指标计算后再执行；本 S3 不训练模型。诊断阈值目前是项目操作性建议，需在看到结果前确认，不能事后挑通过阈值。

## 共同分析和输出

每项扰动至少报告：样本量/覆盖率、组件 ABL/HOT/CTQ/DHI/MAB、AIV 分布及区间、Spearman/Kendall 排序相关、top-k 集合 Jaccard、学生级分数变化、各 semester/agent 子组结果。bootstrap 以 student 为主要 cluster；同学生多个 session/turn 随 cluster 一起抽取。

**暂定工程稳定线（ASSUMPTION，需人工确认）**：一般小扰动下 rank Spearman ≥ .90 且 top 20% Jaccard ≥ .80；阈值用于“稳定性诊断”，不证明效度。若不达标，结论需报告不稳定排名/分数区间，不通过改阈值修饰结果。攻击测试中预先规定的强不变量（如移除 AI 回答后 student-only 分数、虚增未使用 agent 后 MAB）要求完全不变。

| 实验 | 输入扰动 | 输出指标 | 成功标准 | 失败如何解释/后续动作 |
|---|---|---|---|---|
| **1. 标签扰动** | 用 A 模块人工校验得到的 class confusion/probability labels 重抽 (Y_i)；低置信标签按校准概率重复抽样，保留同一学生 cluster。再以六级与三阶标签分别重算。 | ABL/HOT/CTQ/DHI/AIV 的区间；名次 Spearman/Kendall、top-k Jaccard；各类标签不确定贡献。 | 对“个体高低/前列诊断”作稳定解释时，暂定 Spearman ≥ .90、top 20% overlap ≥ .80；否则仅报告总体趋势/置信区间。 | 若名次大幅波动，表示标签噪声会改变诊断；应停止个体排名解释、增加校验或给模糊等级/区间。若六级失败而三阶通过，三阶只能用作粗粒度描述，不能隐匿六级误差。 |
| **2. Bootstrap 样本扰动** | 按 student cluster 有放回抽样；session/turn 随学生一起抽；另做 cohort/agent 分层 bootstrap。 | 主要指标 95% 区间、排名分布、top-k 进入频率、空/短序列比例。 | 点估计和区间可复现；总体教学诊断结论对多数 bootstrap 样本同向，区间不被报告为零不确定。稳定性线按共同工程线评估。 | 宽区间/排名不稳代表样本覆盖或学生数不足；缩小声称范围，补样本或仅报告组级统计。普通 turn-level bootstrap 会低估相关性，视为方法失败。 |
| **3. 权重 ±10%** | 对每个 baseline 权重分别乘 0.9/1.1，再归一到总和 1；同时抽取多种非负权重邻域作辅助敏感性分析。 | AIV 变化、Spearman/Kendall、top-k Jaccard、单项贡献。 | 在待人工确认的 ±10% 局部范围内通过工程稳定线；并且组件权重正向、归一正确。 | 若排名变化大，说明排序主要由建模选择决定；比较权重情景并改为 profile/多维诊断，不宣称唯一综合排名。不要把数据驱动权重当成解决方案。 |
| **4. Leave-one-agent-out** | 每次去掉一种 agent 暴露记录/该 agent 对应会话，重算可比较 cohort；对共同 agent 集合单独分析。 | 各指标分布和排名；不同 agent 的 task/evidence 轨迹；结论方向/差异。 | 不要求不同 agent 的分数相同。若报告跨 agent 普遍结论，剔除单一 agent 后结论方向应保持或有证据支持同质；否则明确 agent-specific。 | 结果明显改变说明综合结论受单一 agent 构成驱动，或各路径真实不同；缩小到 agent-specific 结论，不把异质性强行校准掉。 |
| **5. Leave-one-semester-out** | 分别只用秋季、只用春季重算指标；另限制到共同测量字段、同一 agent/任务可比子集。 | 组件分布、AIV 候选、分层结果、measurement/coverage 差异。 | 不要求两学期相等。跨学期泛化声称只有在同口径共同子集和测量/覆盖诊断支持时才保留；不能仅以 z 分数标准化作为 pass。 | 一学期剔除后方向/排名大变，说明 cohort 或工具依赖；将结论限在期别，不做跨期 AIV 可比排名。 |
| **6. 重复高阶问题攻击** | 对少量低/中阶互动复制完全相同高阶形式问题，或重复相同 student turn 多次；比较原数据、原始计数口径与去重/有效证据口径。 | ABL/HOT/CTQ/AIV 增量；重复相似 turns 对单人分值/排名的影响。 | 精确重复在去重/攻击稳健口径中应无额外增值；主结果变化不得被误称新证据，分值增量应落在自然抽样误差内。 | 复制后指标机械上涨表示频次与能力混淆/潜在 Goodhart 风险；报告攻击幅度，需引入去重或曝光校正后重做，不声称抗操纵。 |
| **7. Bloom 关键词堆砌攻击** | 保持语义推理/证据不变，只添加“分析、评价、创新、设计”等高阶动词；由盲标者在原始/改写版本编码，机器预标签不提供给人类。 | 预标签/人工标签变化，六级/三阶混淆，HOT/ABL/AIV delta。 | 单加关键词不应系统提高 student-evidence Bloom；攻击引起的分数变化不超过盲标一致性误差带，且 task level 与 evidence level 能区分。 | 若高阶标签上涨，表明词汇捷径或 codebook 欠清晰；补充反例规则、复标，并把原先结果标为可能受构念无关方差影响。 |
| **8. AI 回答移除测试** | 从副本中移除所有 `ai_text`，保留 student_text、turn 时间和主体标签；另保留 AI 文本副本用于任务上下文对照。 | student-evidence 标签、ABL/HOT/CTQ/AIV student components；task_bloom/path 作为对照；speaker Unknown 比率。 | 纯 student-evidence 指标必须完全不因 AI 回答文本本身的内容变化；移除上下文若令 task/path 不可识别，可使 task/path 标 U，但不得把 AI 词汇计为学生证据。 | 如果 ABL/HOT 改变，说明 AI 内容泄漏进学生指标或解析器混淆主体；修正来源隔离并重新标注。若只有 task/path 变缺失，需报告上下文依赖。 |
| **9. 虚增智能体数量攻击** | 在数据副本中添加未使用 agent 名称、别名拆分，或重复/空互动；再比较 agent canonicalization 前后。 | 去重 agent count (m_s)、MAB、AIV、rank changes、Unknown agent coverage。 | 无有效 student interaction 的新 agent、agent alias、重复调用不得改变 canonical (m_s)、MAB 或 AIV（强不变量）。真实、核实的新 agent 才可能改变 MAB，且受上限饱和。 | 若空记录/别名抬分，说明 agent mapping 与 MAB 易操纵；停止比较 MAB，先建立版本化 canonical catalog，并回测。 |

## 补充诊断

### 抽样与标注质量

- 比较双人六级与三阶的加权 Cohen κ / ordinal Krippendorff α、置信区间、混淆矩阵和各层覆盖；人工校验按抽样概率校正。
- 检查 `speaker_confidence` 低的 turns、链接型文本、AI 代答/复制段和不同 agent 的误差率。
- 每个阶段冻结规则版本、原始 ID、排除原因和随机种子。若 codebook 中途改变，旧/新版对一小批共同样本双重标注以识别漂移。

### 缺失与跨期

- 将名单 eligible 数、出现日志人数、可解析 turns、有效学生证据 turns 分阶段作为覆盖漏斗报告。
- “没有可见日志”不记作 0 分；比较名单未匹配与匹配者的可观察 roster 特征，若无特征则说明无法评估选择偏差。
- 跨期敏感性首先限制共同字段/共同任务/共同 agent；若无锚定任务或可比测量，验证结果只支持“不可比较/范围受限”，不进行强制校准。

## 决策规则

1. 任一强不变量失败（AI 回答移除泄漏、空 agent 改分、精确重复在去重口径仍显著加分）时，AIV 不能进入对外诊断，先修复并重跑。
2. 统计稳定线失败不等同模型“错误”，但必须将表述从个人排序降到分组描述/区间，并解释敏感来源。
3. Leave-one-agent/semester 失败表示可迁移性有限或存在异质性；不能通过事后提高权重或标准化让它通过。
4. 任何 validation pass 只表示经测试的稳健性条件成立，不证明构念效度或因果识别；后者需独立 outcome 与有效设计。
