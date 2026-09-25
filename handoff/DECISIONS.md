# FROZEN DECISIONS

**D001** 唯一正式项目根目录：`C:\Users\lin\Documents\Codex\2026-09-25\yu`

**D002** 研究对象：学生在 AI 辅助学习中的可观察交互与学习表现证据。

**D003** Task Bloom 与 Student Evidence 分轴标注。

**D004** AIV 当前定位为形成性教学诊断工具。

**D005** Canonical Pilot V1 = 140 条；原始 140 条不得删除。

**D015** S4 Pilot Gate 当前使用 70 条核心样本；其余 70 条保留，但不属于当前 Gate 必须完成人工标签。后续用途（扩展标注、稳健性验证、困难样本分析或模型开发集）在 Gate 通过后另行决定。

**D016** B010 采用单人两轮间隔重测：R1=`data/annotations/human/pilot_worksheet_A.csv`，R2=`data/annotations/human/pilot_worksheet_A_retest.csv`，间隔至少 24 小时。最终信度只能称为“同一标注者的 test-retest reliability”，不是 inter-rater reliability；不得将其包装为双标注者一致性。

**D017** `docs/annotation/annotation_clarification_v0.1.1.md` 与 `validation/gate_thresholds.json` 在 2026-09-25 19:40、真实人工标签产生前冻结。冻结后不得依据 R1 结果临时改规则或阈值；如需修改必须升版本并进入新的验证阶段。

**D006** 56 条旧 Pilot / ID 不匹配版本不进入正式实验。

**D007** 不得把两个 AI 标注结果描述为两名真实人工标注者。

**D008** 人工标注完成前不计算正式 Kappa / Alpha。

**D009** speaker parser coverage 不等于 accuracy。

**D010** 原始记录行暂作为 session_proxy；序列指标不得跨 proxy 计算。

**D011** unknown agent 必须保留并报告。

**D012** B 模块在识别条件不足时保持描述/条件关联，禁止用 PSM、DID 等方法制造不存在的因果识别。

**D013** 算法必须由真实失败点驱动，而不是先选算法再寻找问题。

**D014** 重大方向改变必须经过 Gate Review，不得由单个 Codex 窗口自行修改。
