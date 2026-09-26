# NEXT SESSION ENTRYPOINT

> 这是新的 MAIN_RESEARCH / CONVERGENCE 窗口的唯一入口。只读本文件即可恢复当前收工状态；需要细节时再读取列出的证据文件。本入口不授权启动下一阶段。

## 0. 项目与当前快照

- 唯一项目根目录：`C:\Users\lin\Documents\Codex\2026-09-25\yu`
- 当前 branch：`master`
- 当前 Git HEAD：`667ecf7e25226366014687aa0ff77cbd80d8df34`
- 工作区非 clean：11 个 tracked 修改、58 个 untracked status 条目；不要 reset、checkout、删除或覆盖。
- 本轮扫描已完成：`PROJECT_CLOSURE_SCAN = COMPLETE`。
- 因共享工作区和未收敛冲突仍存在：`PROJECT_FREEZE = PARTIAL`。

## 1. 项目现在做到哪里

开发研究核心已经完成并冻结为：

- `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`
- 输入身份：70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY`
- 16 条 readable Evidence；54 条 `NO_EFFECTIVE_EVIDENCE`
- Raw/Adjusted ABL/HOT/Gap：`3.5625 / 0.375 / 1.125`
- Effective weight：`16 → 6`
- Effective coverage：`0.228571 → 0.085714`，分母为 70
- `run_all.py`：6 steps、32/32 checks PASS
- 核心结论限定为：**Score Stability does not imply Evidence Support Stability**
- 这些数字只能解释为当前 development slice 的结构性测量结果。

Formal 分支尚未闭环：

- HUMAN_R1：0/70 VALID
- HUMAN_R2：0/70
- Formal Human Gate：`PENDING / NOT_RUN`
- Formal AIV：`NOT_AVAILABLE_PENDING_FORMAL_GATE`
- `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`
- 当前没有合法配对的 `Outcome_AI` / `Outcome_baseline`

## 2. 哪些已经冻结

以下工作线不要重跑、调参或改公式：

- Baseline
- ML Challenger（明确 `FROZEN / HANDOFF_COMPLETE`，不是正式优胜）
- Alternative Formulations
- Robustness
- Sensitivity
- Ablation
- Model Presentation
- PPT / Slides
- Development core closure、独立数值复算、fail-closed Formal path

外部金融历史验证和 Binance shadow 只可作为受限 development/external-transfer 证据；不要把它们升级为教育泛化、因果证据或交易优势。

## 3. 哪些不能再碰

在 Human Gate 前，禁止：

- 新增数学模型、重新训练、调参、补实验；
- 修改主模型公式、参数、阈值、Formal Gate 结果；
- 修改或代填 Human R1/R2，或用 AI/WorkBuddy 回交件替代人工；
- 生成 Formal AIV、学生排名、正式准确率、因果 AI 增量或学习增益；
- 修改 Demo/UI、大规模重写 Paper；
- 删除、覆盖、reset、checkout 其他窗口文件或实验结果。

## 4. 哪些还要继续

以下状态不是完成态：

- **Main Research：** `NEEDS_CONVERGENCE`，开发 core 已冻结，但正式链和衍生材料未闭环。
- **Model Tournament / Comparison：** `NEEDS_CONVERGENCE`，final matrix 仍有 stale `PENDING`。
- **Counterexamples / Failure Cases：** `NEEDS_CONVERGENCE`，null 与 numeric 导出冲突。
- **External Transfer：** `NEEDS_CONVERGENCE`，`SUPPORTED` 与 development-only wrapper 词汇冲突。
- **Finance Transfer / Shadow：** `IN_PROGRESS`，10 条记录、0 条 evaluated、10 条等待未来回报。
- **Audit / Red Team：** `NEEDS_CONVERGENCE`，仍有 CONFLICT/STALE/NOT_RUN。
- **Demo：** `NEEDS_CONVERGENCE`，两套实现、raw/default 语义不一致。
- **Paper：** `NEEDS_CONVERGENCE`，候选已完成但 Formal 数字和提交包版本待后续处理。
- **Submission：** `IN_PROGRESS`，队号、命名、ZIP/最终交付格式尚未完成。
- **Human R1/R2/Formal Gate：** 均 `WAITING_FOR_HUMAN_GATE`。

## 5. 需要 MAIN_RESEARCH 先处理的冲突

只做证据收敛，不新增结果：

1. 统一 Demo 的 M0/raw 与 theta0/M1 的名称、默认参数和两套实现；
2. 决定 failure-case null/numeric 的权威来源并隔离旧导出；
3. 修正 Model Tournament matrix 对已收到 baseline/ML artifacts 的 stale 状态，同时保留正式 fit/holdout 仍 pending；
4. 统一 External Transfer 的 development-only 状态词；
5. 记录完整 derivative chain（artifact/figures/Paper/Demo 是 post-processing，不能假设 run_all 已覆盖）；
6. 重新核对提交包与当前 Paper/Demo 的版本、队号和命名；
7. 把旧 Git receipt、旧 paper inventory、shadow 12/10 记录标记为 stale/conflict。

本窗口不要偷偷修这些冲突；每项修复都必须可追溯、只写允许目录，并先确认没有其他窗口正在修改同一文件。

## 6. Human Gate 后的唯一主线

在 MAIN_RESEARCH 收敛完成并由负责人继续人工工作后，严格顺序为：

1. 负责人完成 R1：`data/annotations/human/pilot_worksheet_A.csv`；
2. 记录 R1 完成时间与 SHA-256；
3. 至少等待 24 小时；
4. 同一标注者独立完成 R2：`pilot_worksheet_A_retest.csv`；
5. 执行 `python src/run_s4_gate.py`；
6. 只有 `gate_status=PASS` 且 `formal_gate_eligible=true` 才能进入 `FORMAL_GATE_SWITCH.md`；
7. Gate 不通过则保留 development-only，不能回改阈值或强行 formal。

## 7. 核心证据文件

恢复顺序：

1. `AGENTS.md`
2. `handoff/PROJECT_FREEZE_STATUS_2026-09-26.md`
3. `handoff/PROJECT_STATE.md`
4. `handoff/DECISIONS.md`
5. `handoff/NEXT_TASK.md`
6. `handoff/ARTIFACT_INDEX.md`
7. `handoff/BLOCKERS.md`
8. `reports/audit/closure_audit_2026-09-26.md`
9. `reports/audit/numerical_consistency_matrix.md`
10. `reports/audit/reproducibility_audit.md`
11. `reports/audit/claim_evidence_matrix.md`
12. `reports/development/research_core_closure.json`
13. `reports/verification/core_numbers_source_of_truth.json`
14. `reports/annotation_gate_report.json`
15. `docs/claim_boundary.md`
16. `docs/metric_dictionary.md`
17. `experiments/model_tournament/ML_CHALLENGER_HANDOFF.md`
18. `experiments/model_tournament/final/model_selection_evidence.md`
19. `experiments/transfer_finance/live_shadow/live_shadow_summary.json`

## 8. 当前禁止的表述

保持：

- `DEVELOPMENT_ONLY`
- `AI_PROVISIONAL`
- `formal_gate_eligible=false`
- `AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED`
- `NO_EFFECTIVE_EVIDENCE` 不等于数值 0

不要写：

- Formal AIV 已得到；
- Adjusted Score 是 AI Increment；
- 已证明学习提升、因果效果、真实能力或学生排名；
- ML/替代公式是正式冠军；
- External Transfer 未证明教育普适性或交易优势；仅保留 DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT / no trading advantage claim。

## 9. UI_NEXT / PAPER_NEXT

- **UI_NEXT：** 收敛 Demo M0/raw、theta0/M1、默认参数与两套实现；本轮不改 UI。
- **PAPER_NEXT：** Formal Gate 后更新正式数字，并复核 Failure Case、External Transfer、coverage 分母和提交版本；本轮不重写 Paper。

## 10. 交接结束标记

新的窗口读完本文件后，应先核对：

`git rev-parse HEAD`、`git status --short --branch`、R1/R2 文件和 `reports/annotation_gate_report.json`。

不要重复已冻结实验，不要用旧 handoff 的 R1 checkpoint 或旧 HEAD receipt 覆盖当前事实。

**PROJECT_CLOSURE_SCAN = COMPLETE**

**PROJECT_FREEZE = PARTIAL**



## Fast convergence handoff — 2026-09-26 09:36:16 UTC

- 本轮已完成限定的一致性修复；不新增模型、不重跑冻结实验、不修改 Human R1/R2。
- Canonical artifact：`outputs/final_results.json`；输入：`data/annotations/ai/pilot_ai_provisional.csv`；manifest：`reports/verification/reproducibility_manifest.json`。
- Demo/Paper/Submission package 的核心数字已对齐：Raw 16/70（0.228571），Adjusted 6/70（0.085714），ABL/HOT/Gap = 3.5625/0.375/1.125；默认调整参数 .5/.5/.75。
- P105/P108 数值与核心 artifact 对齐；P072/P035 是显式 undefined refusal。
- HUMAN_R1=0/70 VALID；HUMAN_R2=0/70；Formal Gate=NOT_RUN；`formal_gate_eligible=false`。
- 当前状态：`PRE_HUMAN_GATE_CONVERGENCE = COMPLETE`；`PROJECT_STATE = FROZEN_WAITING_FOR_HUMAN_GATE`。
- 工作区 dirty 是已记录的非阻塞交付状态；下一唯一入口是负责人按冻结协议完成真实 R1，间隔至少 24 小时后完成 R2，再运行 `python src/run_s4_gate.py`。

**CURRENT_PRE_HUMAN_GATE_STATUS = COMPLETE**
**CURRENT_PROJECT_FREEZE = COMPLETE_FOR_PRE_HUMAN_GATE**
