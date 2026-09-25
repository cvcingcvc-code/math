# CURRENT HANDOFF

1. 当前 Git 分支

`master`

2. 最新 commit SHA

`c041e283fd97c437a4ce19c337c86fba03744627`

3. 当前唯一主任务

S4 Pilot Annotation Gate：等待冻结流程规定的真实人工标注结果；AI 临时标签和 DEVELOPMENT_ONLY 测量模型不能替代人工 R1/R2。

4. 已完成到哪一步

- S4 协议、70 条核心样本范围、B010 单人 test-retest 设计已冻结。
- 已建立 `src/development_data.py`：显式 development 入口读取 `data/annotations/ai/pilot_ai_provisional.csv`，正式默认路径保持不变。
- 已建立 `src/run_development_experiment.py`：70 条 AI_PROVISIONAL 数据的透明行级 ABL/HOT/coverage/gap 开发链路。
- 已建立 `src/run_reliability_sensitivity.py`：可观察性、置信度、prompt 引导和 context truncation 的透明权重敏感性模型，生成 15 个参数条件的 ABL/HOT/coverage/gap 结果。
- 已修复并提交 Figure 4：直接展示 normalized Score 稳定红线与 Evidence Support 下降蓝线；横轴为真实 `lambda_prompt`，固定参数和 coverage 分母均在图中明确标注。稳定性解释为当前 16 条可判读 Evidence 的公共缩放结构，不是因果效应。
- 已在论文与 Demo 口径中明确 `effective coverage = effective evidence weight / 70 development records`，并保持 `NO_EFFECTIVE_EVIDENCE` 不填 0。
- 上述开发结果均明确为 `DEVELOPMENT_ONLY`、`AI_PROVISIONAL`、`NOT FOR FORMAL GATE OR FINAL CLAIMS`，`formal_gate_eligible=false`。
- 未运行完整模型，未计算正式 Gate、正式 AIV、Kappa 或 Alpha。

5. 当前唯一阻塞

真实人工标签尚未返回。当前 R1/R2 仍为空；该阻塞不能由 AI 临时标签或开发模型替代。

6. 下一步唯一动作

按冻结说明完成真实人工 R1；随后至少间隔 24 小时完成同一标注者 R2，之后才运行既有 Gate 流程。

7. 已冻结、禁止修改的文件/规则

- `data/annotations/human/pilot_worksheet_A.csv`（R1）
- `data/annotations/human/pilot_worksheet_A_retest.csv`（R2）
- `docs/annotation/annotation_manual_v0.1.md`
- `docs/annotation/annotation_clarification_v0.1.1.md`
- `validation/gate_thresholds.json`
- `src/annotation_gate_report.py` 的正式 Gate 判定逻辑
- Canonical Pilot `data/processed/pilot_sample.csv`
- D008：人工标注完成前不计算正式 Kappa / Alpha
- D010：序列指标不得跨 session_proxy 计算
- D011：unknown agent 必须保留并报告
- D012：不得在识别条件不足时制造因果结论

8. 下一步真正需要读取的最少文件

- `handoff/CURRENT_HANDOFF.md`
- `data/annotations/human/README_ANNOTATOR.md`
- `docs/annotation/annotation_manual_v0.1.md`
- `docs/annotation/annotation_clarification_v0.1.1.md`
- `data/annotations/human/pilot_worksheet_A.csv`
- `data/annotations/human/pilot_worksheet_A_retest.csv`
- 收到标签后再读取：`src/run_s4_gate.py`

9. 当前是否有未提交修改

有。

10. 未提交修改的具体文件及原因

- `handoff/ARTIFACT_INDEX.md`：登记开发数据入口、开发实验入口及开发结果文件。
- `handoff/CHANGELOG.md`：记录开发数据入口、透明开发模型和可靠性敏感性模型的真实完成内容。
- `src/annotation_gate_report.py`：增加 AI_PROVISIONAL / DEVELOPMENT_ONLY 进入正式 Gate 的拒绝保护。
- `src/development_data.py`：新增显式 formal/development 数据加载适配层。
- `src/run_development_experiment.py`：新增最小 DEVELOPMENT_ONLY 建模、指标和结果输出入口。
- `src/run_reliability_sensitivity.py`：新增 Evidence Reliability / Bias Correction 敏感性模型。
- `data/annotations/ai/`：现有 AI provisional 开发数据及元数据，当前未纳入 Git。
- `reports/development/`：开发模型输出的 CSV、JSON 和 SVG 结果，当前未纳入 Git。

这些修改尚未提交，因为本轮只生成交接摘要，没有执行提交动作；下一窗口应先审阅这些未提交内容，再决定是否提交。 
