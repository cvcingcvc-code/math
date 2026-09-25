# BLOCKERS

## B001 — Annotation（OPEN，已不再是协议阻塞）

正式人工 Pilot 标注尚未完成。当前只差**真实人工标签**；此项不得由 AI 窗口代理或虚构。

- 已解除的部分：可执行规则（V0.1.1）、盲标表、说明、分析器均已交付。
- 剩余：两名独立人工标注者返回 `pilot_worksheet_A|B.csv`。

## B002 — Annotation protocol（ADDRESSED，待签署）

S3 与 annotation manual V0.1 在 speaker/source 定义、Task Bloom 执行对象、内容来源编码方面的边界不统一。

- 处置：`docs/annotation/annotation_clarification_v0.1.1.md`，把 8 个失败点写成判定程序，**不改变 V0.1 判级语义**。
- 待办：负责人确认采纳后才生效（D014）。V0.2 仍保留给真实 pilot 分歧驱动。

## B003 — Session（OPEN，数据固有限制）

无原生 session_id，当前仅有 session_proxy。序列指标不得跨 proxy 计算。

## B004 — Outcome（OPEN，数据固有限制）

缺独立无 AI 学习结果，模块 B 暂不支持 AI 因果增量识别。

## B005 — Agent identity（OPEN）

约 10.5% turn 的 agent_type 为 unknown。D011：必须保留并报告，不得删除或按文件名反推。

## B006 — Future-content leakage in canonical file（OPEN，已隔离）

`data/processed/pilot_sample.csv::ai_context_text` 是当前 turn **之后**的 AI 内容，不是前文。

- 证据：48/140 条该 source_row 内无更早 AI 轮但该列非空；其中 45 条与其后的 AI 轮匹配。
- 影响：若作为标注语境会泄漏 AI 回答，污染 Task 复述判断、搬运判定与相似性判断。
- 处置：已从标注路径隔离（`src/build_annotation_worksheets.py` 不使用该列）。
- 待办：在下游任何模块使用该列前必须先修复或弃用；建议在数据字典中标记为 deprecated。

## B007 — Non-blind review queue（RESOLVED，保留记录）

`data/processed/pilot_human_review_queue.csv` 含 AI 预标注与 agent/path 标识，不能直接下发。

- 处置：改发 `data/annotations/human/pilot_worksheet_A|B.csv`，映射另存 `_keys/`。
- 核验：盲标表泄漏列为 0。

## B009 — Student-level evidence sparsity（OPEN，模型结构问题，需负责人决定）

来源：`reports/indicator_feasibility_audit.md`。

- 事实：每 session_proxy 学生轮中位数 2；每生学生轮中位数 8（秋）/ 9（春）；春季 36.8% turn 的 agent 为 unknown（秋季 0%）。
- 情景（仅假设，基于 AI 探索性预标注）：每生可赋级证据轮中位数约 4（秋）/ 2（春），学生级 HOT 最坏 SE 0.25–0.36。
- 影响：C6 的"逐生独立比例 + 线性加权 AIV 排名"在多数学生上精度不足；CTQ 在短 session 上高度离散；春季 MAB 受 unknown agent 严重影响。
- 候选处置（未执行，待确认）：学生级指标改为分层收缩估计（如 Beta-Binomial / 有序 logit 随机效应），AIV 报告后验区间与"不可排名"标记；MAB 限秋季或只作描述。须在人工标签返回前预注册，不得看结果后选择。

## B010 — 单人参赛与"双人独立人工标注"设计冲突（FROZEN，采用单人重测）

负责人已确认选项 (b)：R1=`data/annotations/human/pilot_worksheet_A.csv`，R2=`data/annotations/human/pilot_worksheet_A_retest.csv`，两轮间隔至少 24 小时、顺序打乱、盲重标。

最终报告必须明确：**这是同一标注者的 test-retest reliability，不是 inter-rater reliability。** 不得将单人重测包装成双标注者一致性；AI 预标注也不得作为第二人工标注者。工具链已准备，但两轮真实标签尚未产生。

## B008 — Scope inconsistency（FROZEN，Gate 使用 70 条核心样本）

Pilot Gate 的人工标注分母冻结为 70 条核心样本（50 条疑难 + 20 条随机审计）。原始 Canonical Pilot V1 的 140 条记录继续保留，不删除；其余 70 条暂不属于当前 Gate 必须完成的人工标签。

Gate 通过后，再决定剩余 70 条用于扩展标注、稳健性验证、困难样本分析或模型开发集。不得将当前 Gate 的 70 条结果外推为 140 条全量人工标注结果。
