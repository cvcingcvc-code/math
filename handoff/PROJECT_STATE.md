# PROJECT STATE

## Competition

中国第一届数学建模黑客松 · 赛道一

题目：《新时代教育中 AI 增量价值评价的建模方法》

研究方向：《考虑智能体引导偏差与标注不确定性的教育 AI 增量价值评价》

## Research object

学生在 AI 辅助学习中的可观察交互与学习表现证据。

不直接等同于长期稳定能力、独立学习增益或 AI 因果效应。

## Current stage

S4 Pilot Annotation Gate

当前状态：**BLOCKED_BY_HUMAN_ANNOTATION**（S4 协议冻结，2026-09-25 19:40）

冻结决定：Gate 使用 70 条核心样本；B010 采用同一标注者两轮、间隔至少 24 小时的 test-retest。正式 HUMAN_R1 = **0/70 VALID**（原始填写 1/70，但该行字段错位/非法，已清空；原始非法行保留于 `work/backups/pilot_worksheet_A_2026-09-26_1117_checkpoint.csv`）；HUMAN_R2 = **0/70**。尚未产生任何真实人工标签、一致性结果或 Gate 通过结论。AI_ASSISTED = **70/70**，仅为 `DEVELOPMENT_ONLY`，不得替代人工输入。

前状态为 `BLOCKED_BY_ANNOTATION`。协议侧阻塞（B002）已产出澄清件，标注包与 Gate 分析器已交付；**剩余阻塞是真实人工标签尚未返回**，该项无法由 AI 窗口推进，也不得虚构。

尚未进入：
- 全量 Bloom 标注
- 正式一致性实验
- 最终 CTQ/DHI/AIV
- PSM
- DID
- 正式因果模型

## Canonical dataset

2025 秋：
- 原始问答 845 rows
- URL-only 排除 21
- 纳入 824 rows
- 295 students
- 5019 turns
- 观察期 2025-10-09 至 2026-02-05

2026 春：
- 聚合原表 1925 rows / 528 ids
- 明确参与名单并集 131 students
- 日志匹配 109 students / 482 rows
- 排除空文本 13
- 排除 URL-only 68
- 最终 401 rows
- 106 students
- 2009 turns
- 观察期 2026-03-19 至 2026-07-27

总有效 turns：7028。

## Important data limitations

1. 2026 春原始导出不是天然春季队列；
2. 约 22 名明确参与学生没有匹配日志；
3. 缺日志不能解释为未使用 AI；
4. 秋季班级无法逐人完整映射；
5. 原始数据没有真实 session_id；
6. 当前使用原始记录行为 session_proxy；
7. CTQ 等序列指标不得跨 session_proxy 计算；
8. speaker parser 当前是全覆盖，不代表 100% accuracy；
9. 4 条连续学生标记异常已进入低置信审计；
10. agent_type unknown：740 / 7028 turns ≈ 10.5%；167 / 1225 session_proxy ≈ 13.6%；
11. Unknown agent 不得直接删除。

## Canonical Pilot

正式 Pilot V1：`data/processed/pilot_sample.csv`，N = 140（完整性已核验，见下）。

构成：
- 秋 70
- 春 70
- 探知侠 65
- 逆行侠 18
- 数模全才 23
- 数模匹配 5
- AI 学伴 6
- unknown agent 23

56 条旧 Pilot 不是正式 Pilot，不得混入 Kappa / Alpha / AIV 正式实验。

## Integrity verification (2026-09-25)

`src/verify_pilot_integrity.py`：21/21 冻结不变量通过。

- N=140、pilot_id 唯一且为 P001–P140、无旧 56 条 ID 体系混入；
- 140/140 均为 student turn（分析单位为"学生轮"）；
- AI 预标注 140 行、`annotator_type=LLM_EXPLORATORY_NOT_HUMAN`（D007 合规）；
- 复核队列 70 = 50 疑难 + 20 随机审计，manual_version=V0.1；
- `annotation_manual_v0.1.md` SHA-256 = CHANGELOG 记录值（未改动）；
- `prior_ai_context` 可被独立重建复现：prelabel 140/140、queue 70/70。

## Defect register（未解决）

**S4-F01（HIGH）** `pilot_sample.csv::ai_context_text` 是**未来** AI 内容，不是前文。

- 48/140 条在该 source_row 内**根本没有**更早的 AI 轮，但该列仍非空；
- 其中 45 条与**其后**的 AI 轮匹配；26 条完全相同、63 条为其前缀。
- 结论：该列**不是良定义的前文语境字段**，用于标注会把 AI 回答泄漏进 Task/Evidence 判断（相似性、搬运判定、任务复述）。
- 处置：`src/build_annotation_worksheets.py` 一律不使用它，前文由 `clean_interactions.csv` 的轮次顺序严格重建。

**S4-F02（HIGH）** `pilot_human_review_queue.csv` 不是盲标表。

- `task_bloom`、`student_evidence_bloom`、`confidence`、`reason`、`content_source_attribution` 已填入 AI 预标注，且含 `agent_type`、`path_case`。
- 直接下发会让标注者锚定自动标签，违反 manual V0.1 第 七.3 条（第一轮不看自动标签、遮蔽路径名称）。
- 处置：改发 `data/annotations/human/pilot_worksheet_A|B.csv`（已核验零泄漏列），映射另存 `data/annotations/_keys/pilot_worksheet_key.csv`。

## Current annotation status

140 条已有 AI 探索性预标注。人工复核计划：50 条疑难样本 + 20 条固定随机正常样本。

**已交付并可直接执行**：
- 澄清件 `docs/annotation/annotation_clarification_v0.1.1.md`（待负责人签署）
- 盲标表 A/B：`data/annotations/human/pilot_worksheet_A.csv`、`_B.csv`（70 行，无泄漏列）
- 标注者说明：`data/annotations/human/README_ANNOTATOR.md`
- B010 R1/R2：`pilot_worksheet_A.csv` →（至少 24 小时）→ `pilot_worksheet_A_retest.csv`；这是同一标注者的 test-retest reliability，不是 inter-rater reliability。
- Gate 分析器：`src/annotation_gate_report.py`（标签返回后一条命令出 Gate Report）
- 一键入口：`src/run_s4_gate.py`

**仍缺**：完整真实人工结果。正式 R1 当前为 0/70 VALID（原始填写 1/70 的非法行已清空，保存编码 GB18030），R2 `pilot_worksheet_A_retest.csv` 为 0/70；完整 R1/R2 返回前不得计算正式一致性。

禁止在人工标注完成前报告正式 Cohen Kappa、weighted Kappa、Krippendorff Alpha。

## Pending sign-off（不得由 AI 窗口自行决定）

1. `annotation_clarification_v0.1.1.md` 已于 2026-09-25 19:40 在真实人工标签产生前冻结并采纳为 Pilot 执行规则；冻结后不得根据 R1 结果临时修改。
2. `validation/gate_thresholds.json` 已于 2026-09-25 19:40 在查看任何真实标签前确认为 `preregistered: true`；不得根据结果回改。
3. B008 已冻结为当前 Gate 使用 70 条核心样本；原始 140 条 Pilot 保留，其余 70 条不属于当前 Gate 必须完成人工标签。

## Indicator feasibility (2026-09-25 晚, label-free)

见 `reports/indicator_feasibility_audit.md`。结构事实：session_proxy 学生轮中位数 2；每生学生轮中位数 8/9；春季 unknown agent 占 36.8%。
按 AI 预标注情景推算，学生级独立比例指标精度不足以做个体排名 → B009（模型结构待决）。单人参赛与双人标注设计冲突 → B010。
Gate 状态不变：仍无人工标签。

## Paper / presentation narrative closeout (2026-09-25 晚)

已完成论文与答辩收口材料，主线固定为：**Score Stability ≠ Evidence Support Stability**。

新增：
- `reports/paper/competition_paper_narrative_draft.md`
- `reports/paper/judge_story_3min.md`
- `reports/paper/elevator_pitch_30s.md`
- `reports/paper/core_figures_interpretation.md`
- `reports/review/judge_attack_questions.md`
- `reports/review/top_5_paper_weaknesses.md`

这些材料只整理现有 DEVELOPMENT_ONLY / AI_PROVISIONAL 结果，不改变冻结模型、正式数据、标注手册、Gate 阈值、provisional 标签或 Demo。当前论文最大风险是正式人工证据链尚未闭环，以及 16 条 Evidence 的完全分离可能混合了选择、规则、临时标签和映射效应。

## Independent numerical verification (2026-09-25 深夜)

已从 `data/annotations/ai/pilot_ai_provisional.csv` 独立复算全部 Bounds 数字，未调用生产 Bounds 函数。结果全部复现：70 records、16 readable Evidence、21×11×3=693 grid、660 defined、33 undefined、ABL=3.5625、HOT=0.375、Gap=1.125、effective weight 0.4–16.0、effective coverage 0.005714...–0.228571...。Coverage denominator 明确为全部 70 条 development records。

所有 readable Evidence 均为 prompt=true、context=false、confidence=medium、task_actor=ai，故参数因子构成公共缩放，归一化分数稳定而 support 下降。Demo payload 逐项一致；论文数字无 P0 矛盾。发现 1 个 P1 展示问题：Figure 4 SVG 实际只画 effective coverage，标题却写 score stable；另有 1 个 P2 表达问题：coverage 首次出现时应明确 denominator=70。详细结果见 `reports/verification/reproduction_review.md`。

## Figure / Demo / Paper closeout (2026-09-25 深夜)

阶段一已完成并提交 `2359fbf`：Figure 4 现在直接显示 normalized Score 稳定与 Evidence Support 下降，横轴为真实 `lambda_prompt`，固定参数及 `effective coverage` 分母 70 均明确。论文和 Demo 同步说明：分数稳定来自当前 16 条可判读 Evidence 的公共缩放结构，不是因果效应；support 为零时返回 `NO_EFFECTIVE_EVIDENCE`，不填 0。阶段二检查确认现有真实开发输入只能支持明确的开发/合成结构演示：16 条可判读 Evidence 全部为 prompt=true、context=false、confidence=medium、task_actor=ai、task_source=ai_prompt、content_relation=reworked_with_addition，缺少异质交叉支持。因此未修改标注、不把曲线写成真实异质实验或正式结论。

## Module B evidence level

当前最高：Level 1 — 描述性差异。

在处理、对照、基线、结果、共同支持等条件确认之前，不得宣称 AI 因果增量。

## Research core closure (2026-09-26)

开发版测量闭环已完成并标记为 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`。`src/build_core_closure.py` 生成统一 Raw/Adjusted 指标、M0–M3 消融、真实记录反例和六问结论；`run_all.py` 已纳入该步骤，当前 32/32 检查通过。

本冻结不改变正式 Gate、R1/R2、原始数据、标注手册、阈值或 Formal AIV 边界。16 条可判读 Evidence 全部 `prompt_induced=true`，因此当前数据只能支持“分数稳定与证据支持不稳定并存”的开发版测量结论；Formal AIV 仍为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

## Parallel closeout (2026-09-26)
- Roadshow deck completed: outputs/education_ai_evidence_roadshow_v1_final.pptx (10 slides; structural/layout/import validation passed).
- Demo, core numbers, status boundaries, and development artifacts rechecked; run_all.py passed 32/32.
- Development-only submission package assembled at outputs/submission_package_development_only/ with manifest; no R1/Gate labels read or inferred.

## Human R1 checkpoint and Gate-readiness fix (2026-09-26 late morning)
- HUMAN_R1 = **0/70 VALID**（`pilot_worksheet_A.csv` 原始填写 1/70 但字段非法，已清空）；HUMAN_R2 = **0/70**；AI_ASSISTED = **70/70 DEVELOPMENT_ONLY**；FORMAL_HUMAN_GATE = **NOT_RUN**。
- 修复 Gate 读取崩溃：R1 被本地编辑器保存为 GB18030，新增 `src/csv_safe_read.py` 并让 Gate 三个脚本兼容 UTF-8/GB18030（只读，不回写）；另修复 Gate 分析器对大小写标签的规范化，未改阈值或标签。
- 修复 Demo coverage 分母错误（原按 16 条可判读记录计算，显示 75%；现按 70 条记录，显示 17.14%），并新增 Raw baseline 与 Counterexamples 面板；`run_all.py` 仍 32/32 PASS。
- 提交包同步 `demo/index.html` 与 4 张核心图，MANIFEST 35 项一致。未修改论文主体、阈值、R1/R2 标签。



## Presentation style revision (2026-09-26)
- Reworked the roadshow deck into an editorial green/cream/orange visual system based on the supplied references; content and Formal Gate boundaries unchanged.
- Final deck: outputs/education_ai_evidence_roadshow_final.pptx; 10 slides; package integrity, layout, font, and first-party import checks passed.


## Paper-only closeout (2026-09-26)
- PPT visual work paused at user request; no further style changes planned until user finishes evening beautification.
- Paper Markdown and HTML candidate tightened around Raw/Adjusted stability, effective weight 16→6, and coverage 0.228571→0.085714; Formal Gate wording unchanged.
- Waiting state: formal human annotation; no R1 labels read or inferred.

## Submission-readiness handoff (2026-09-26)
- AI_ASSISTED remains 70/70 and `DEVELOPMENT_ONLY`; it is a separate development artifact and is not HUMAN_R1/R2 or Formal Gate input.
- Formal HUMAN_R1/R2 remain 0/70 VALID and 0/70; `reports/annotation_gate_report.json` remains the PENDING placeholder and Formal Human Gate is `NOT_RUN`.
- `src/annotation_gate_report.py` now normalizes controlled-value casing in memory, validates semicolon-separated `ambiguity_type` safely, and emits preregistered Gate decision fields for the future formal path. No thresholds, labels, or manual text were changed.
- Submission paper candidate now states AI_ASSISTED / AI_PROVISIONAL separation and explicit HUMAN_R1/R2 status; development figures, Demo, and package remain unchanged.


## External design absorption (2026-09-25 current round)
- AI annotation remains isolated as `AI_PROVISIONAL / DEVELOPMENT_ONLY`; `src/build_final_artifact.py` consumes only the deterministic structured CSV and never calls an LLM.
- Added deterministic single-record Explain schema: `reports/development/explain_records.json` with raw_score, evidence_reliability, adjusted_score, evaluation_status, positive_factors, negative_factors, explanation.
- Added 15-row What-if interface for lambda_prompt, lambda_context and r_medium at -20%, -10%, baseline, +10%, +20%: `reports/development/what_if_sensitivity.csv`.
- Added unified fact source: `outputs/final_results.json`; it links metadata, data identity, Raw/Reliability/Adjusted summaries, sensitivity, ablation, counterexamples, five core figures, human and transfer status.
- Added five standard-library SVG figures: raw vs adjusted scatter, reliability distribution, parameter sensitivity, ablation comparison, and counterexamples.
- Formal Gate remains `NOT_RUN`; no human labels, thresholds, research question, or core formula were changed.

## Development Submission Candidate closeout (current round)
- Existing `experiments/transfer_finance/transfer_validation.json` synchronized into `outputs/final_results.json`; boundaries remain structural transfer preliminary support, reliability separation weak/partial support, sensitivity robustness supported, risk–coverage improvement not supported, and no trading advantage claim.
- Existing Binance shadow branch remains independent public-data-only, no real orders, no main-model parameter changes, and no short-term returns promoted to the main conclusion.
- `outputs/final_results.json` now contains development_results, human_validation, transfer_validation, sensitivity, ablation, counterexamples, limitations, and figure references.
- Paper candidate: `paper/development_submission_candidate.md`; Demo now reads `outputs/final_results.json`; consistency checker passes all checks including PPT core-number scan.
- Formal adapter contract is interface-ready only (`src/formal_input_adapter.py`); no Formal Gate or Formal result was run.

## Competition alignment audit (current round)
- `reports/review/competition_alignment_audit.md` confirms the competition-to-model mapping is PASS when the claim is framed as an evidence-support framework for AI incremental-value evaluation.
- Main deviation risk is overclaiming True Ability, causal AI effect, or Formal AIV. The audit classifies 54 `NO_EFFECTIVE_EVIDENCE` cases as jointly caused by missing/undetermined evidence with overlapping context, prompt/AI influence, and low-confidence signals; no single-cause attribution is supported.
- Paper candidate now states the competition-facing evidence-support framing and foregrounds 16 readable vs 54 no-effective-evidence records.

## External Transfer Validation — Binance forward/shadow (2026-09-26)
- Added isolated `experiments/transfer_finance/live_shadow/` using only Binance official public market-data GET endpoint `https://data-api.binance.vision/api/v3/klines` for BTCUSDT 1m snapshots plus 1d context.
- No API key, secret, account, balance, order, cancel, spot, margin, futures, transfer, or withdrawal interface. Startup is fail-closed unless `LIVE_ORDERING_ENABLED` is explicitly `false`; `true` and missing env both emit `UNSAFE_PERMISSION_DETECTED` and stop.
- Frozen model version `btc_usdt_7d_momentum_market_evidence_v1`; parameters unchanged: 7-day momentum, 0.30/0.30/0.20/0.20 reliability weights, threshold 0.65.
- Corrected batch look-ahead risk: each 1m record computes features using its own observed close and timestamp; calibration uses only completed daily bars. Future returns are backfilled only after target time + 24h.
- Current shadow log: 10 records, all `ABSTAIN`, 0 evaluated, status `INSUFFICIENT_DATA`; see `experiments/transfer_finance/live_shadow/live_shadow_summary.json`.


## External Information-Missing Validation (2026-09-26)
- 当前状态：DEVELOPMENT_ONLY，历史 BTC-USD paper simulation；M0/M1/M2/M3 RUNNABLE。
- Gate 1 = SUPPORTED；Gate 2 = SUPPORTED；Gate 3 = NOT SUPPORTED。Gate 3 不得写成已验证。
- M1 证据身份为 synthetic / controlled evidence；金融仅作 External Transfer Validation，不改变教育主线或冻结参数。
- Demo 已改为模型验证交互页，统一读取 outputs/final_results.json 与 xperiments/transfer_finance/information_missing_validation.json。


## Research-line repair and formal readiness (2026-09-26)
- AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED: current pilot has no paired comparable Outcome_AI and Outcome_baseline; Raw Signal is provisional Student Evidence.
- Added docs/metric_dictionary.md, docs/claim_boundary.md, reports/reliability_component_audit.md, Accuracy-Coverage and Failure Case contracts.
- Added fail-closed src/formal_validation_pipeline.py; no human labels or formal metrics are modified before Gate PASS.

## Presentation convergence (2026-09-26)
本轮 MAIN_RESEARCH / PRESENTATION_CONVERGENCE 已完成教育证据主链统一。新增评委 3 分钟故事、canonical 主图、组件解释表、验证故事、QA 与 3 分钟讲稿；Demo 已移除金融场景并使用真实 development cases。Formal/Human 状态未改变。

## Visual evidence convergence (2026-09-26)
- Final F1–F6 visual layer is frozen at `reports/visual_evidence/final/` with manifest and deterministic renderer; no model, parameter, data, Human R1/R2, or Formal Gate change was made.
- Paper main visual chain uses F1–F5; F6 is external structural transfer / limitation evidence. Demo home uses F1–F3 and the three result cards P108, 16→6 support, and P072 refusal.
- Old high-risk SVGs remain as historical artifacts but are no longer referenced by the main Paper/Demo/fact index. All final figures retain `AI_PROVISIONAL · DEVELOPMENT_ONLY · Formal Gate NOT_RUN`.
## Independent model tournament evaluator (2026-09-26)

The tournament protocol is frozen before candidate result review at `experiments/model_tournament/protocol/model_tournament_protocol.md`. Existing comparison evidence is development-only and includes the current reliability model, raw-only baseline, gated rule, and fixed multiplicative/additive/nonlinear formulations. Simple linear and ML challengers have no auditable result artifacts and are `PENDING`. The current decision is `NO_SINGLE_DOMINANT_MODEL`; this work does not change the main model or Formal Gate state.
## Robustness / perturbation validation (2026-09-26)
- Added `src/run_robustness_validation.py` and reports under `reports/robustness/`, `reports/perturbation/`, and `reports/external_transfer/`.
- ±10%/±20% one-at-a-time parameter perturbations: 0 state flips, 0 ranking changes; max record reliability change 0.075; support is more sensitive than normalized score.
- P108 prompt-risk counterfactual changes LOW_SUPPORT→SUPPORTED when risk is removed; P072 remains NO_EFFECTIVE_EVIDENCE when context alone is restored.
- Existing three-strategy finance transfer remains auxiliary: framework/cross-strategy reliability SUPPORTED, selective gain PARTIAL, strategy C unsupported.
- Human R1/R2 and Formal Gate unchanged and still pending.
