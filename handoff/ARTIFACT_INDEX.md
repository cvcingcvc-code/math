# ARTIFACT INDEX

项目根目录：`C:\Users\lin\Documents\Codex\2026-09-25\yu`

## Research / design

| Artifact | Canonical Path | Stage | Status | Purpose |
|---|---|---|---|---|
| Evidence matrix | `docs/03_evidence_matrix.md` | S2 | Present | 文献证据矩阵 |
| literature_review_v1 | `docs/literature/literature_review_v1.md` | S2 | Not found | 未发现该文件；勿按记忆引用 |
| Research spec | `research/research_spec.md` | S3 | Present | 冻结研究对象与范围 |
| Variable map | `variable/variable_map.md` | S3 | Present | 变量定义 |
| Module A model | `research/module_a_model.md` | S3 | Present | A 模块候选方法 |
| Target trial | `research/ideal_target_trial.md` | S3 | Present | B 模块目标试验与识别边界 |
| Module C candidates | `research/module_c_candidates.md` | S3 | Present | 指标候选 |
| Validation plan | `validation/validation_plan.md` | S3 | Present | 验证与压力测试计划 |
| Gate thresholds | `validation/gate_thresholds.json` | S4 Pilot | **Frozen, preregistered=true (2026-09-25 19:40)** | 真实人工标签前冻结；70 core records；不得回改 |

## Data

| Artifact | Canonical Path | Stage | Status | Purpose |
|---|---|---|---|---|
| Clean interactions | `data/processed/clean_interactions.csv` | S4 | Present, 7028 turns | 清洗后的交互记录 |
| Cohort flow | `data/processed/cohort_flow.csv` | S4 | Present | 样本纳入流 |
| Exclusion log | `data/processed/exclusion_log.csv` | S4 | Present | 排除记录与原因 |
| Speaker audit | `data/processed/speaker_audit.csv` | S4 | Present | 话语主体人工审计样本 |
| Canonical Pilot | `data/processed/pilot_sample.csv` | S4 | Present, N=140, verified | 正式 Pilot V1 |
| AI prelabel | `data/processed/pilot_ai_prelabel.csv` | S4 Pilot | Present, exploratory | AI 探索性预标注；不是人工标签 |
| Human review queue | `data/processed/pilot_human_review_queue.csv` | S4 Pilot | **Not blind — do not hand out** | 含 AI 预标注与 agent/path；仅分析侧 |
| Blind worksheet A | `data/annotations/human/pilot_worksheet_A.csv` | S4 Pilot | Present, 70 rows, HUMAN_R1 0/70 VALID | B010 R1 第一轮人工盲标表；非法首行已清空 |
| Blind worksheet B | `data/annotations/human/pilot_worksheet_B.csv` | S4 Pilot | Present, retained legacy blank sheet, 70 rows | 当前 Gate 不使用；B010 改用单人 R1/R2 重测 |
| Annotator instructions | `data/annotations/human/README_ANNOTATOR.md` | S4 Pilot | Present | 标注者执行说明 |
| Worksheet key | `data/annotations/_keys/pilot_worksheet_key.csv` | S4 Pilot | Present, analysis-side only | 盲标映射（agent/path/抽样/预标注） |
| WorkBuddy annotations | `data/annotations/workbuddy/pilot_worksheet_B_submitted.csv` | S4 Pilot | Received, 70 rows, audited | 队友 B 交回件；独立审计见 `reports/workbuddy_annotation_audit.md`; 不作为冻结 B010 R1/R2 |

## Annotation rules

| Artifact | Canonical Path | Stage | Status | Purpose |
|---|---|---|---|---|
| Annotation manual | `docs/annotation/annotation_manual_v0.1.md` | S4 Pilot | Present, frozen; SHA-256 `F8E42B17…C64F119` | 标注规则本体 |
| Clarification V0.1.1 | `docs/annotation/annotation_clarification_v0.1.1.md` | S4 Pilot | **Frozen and signed off (2026-09-25 19:40)** | 8 个失败点的可执行判定程序；语义不变 |
| Annotation template | `docs/annotation/pilot_annotation_template.csv` | S4 Pilot | Present, frozen; SHA-256 `2E4C9FBD…31F021B` | 8 列最小模板 |

## Code (`src/`)

| Artifact | Canonical Path | Status | Purpose |
|---|---|---|---|
| Gate entry point | `src/run_s4_gate.py` | Verified | 一键跑完整 S4 Gate 流程 |
| Integrity verifier | `src/verify_pilot_integrity.py` | Verified, 21/21 pass | 冻结不变量 + 缺陷登记 |
| Worksheet builder | `src/build_annotation_worksheets.py` | Verified, blind=True | 生成盲标表（不使用泄漏列） |
| Reliability lib | `src/reliability.py` | Verified, 9/9 self-tests | Krippendorff α / Cohen κ；无外部依赖 |
| Gate report generator | `src/annotation_gate_report.py` | Verified, case-normalization + multi-code validation fixed | 一致性、混淆矩阵、双轴 gap、成本、8 问；未来报告写入 Gate decision fields |
| Metric feasibility (draft) | `src/metric_feasibility.py` | **未运行、来源未核实**，与上一行功能重叠 | 暂不使用；待负责人决定保留或归档 |
| Indicator feasibility audit | `src/indicator_feasibility_audit.py` | Run 2026-09-25 | 无标签结构审计：CTQ/ABL/HOT/MAB 可计算性 |
| Development annotation loader | `src/development_data.py` | Added 2026-09-25 | 显式 `--mode development` 读取 AI_PROVISIONAL；默认 formal 路径不变；不可进入正式 Gate |
| Development experiment entry | `src/run_development_experiment.py` | Added 2026-09-25 | 70 条 provisional 数据的透明行级 ABL/HOT/coverage/gap 探索链路；不训练分类器、不进入正式 Gate |
| Core closure builder | `src/build_core_closure.py` | Added 2026-09-26 | Raw/Adjusted 指标、M0–M3 消融、真实反例与研究结论；仅 DEVELOPMENT_ONLY |
| Worksheet-safe reader | `src/csv_safe_read.py` | Added 2026-09-26 | 兼容 UTF-8 / GB18030 只读读取人工工作表；不改写文件与标签 |

## Reports
| WorkBuddy B audit | `reports/workbuddy_annotation_audit.md|.json` | Generated 2026-09-26 | 70-row structural/controlled-value audit; formal_gate_eligible=false |
| WorkBuddy B summary | `reports/workbuddy_annotation_summary.md|.json` | Generated 2026-09-26 | Single-coder descriptive distribution; no agreement/formal inference |

| Artifact | Canonical Path | Status | Purpose |
|---|---|---|---|
| Data audit | `reports/data_audit.md` | Present | 数据审计说明 |
| Pilot rule failure report | `reports/pilot_rule_failure_report.md` | Present | V0.1 规则压力测试发现 |
| Annotation Gate report | `reports/annotation_gate_report.md` | **PENDING placeholder** | 待人工标注返回后由 `src/run_s4_gate.py` 生成 |
| Annotation Gate report (json) | `reports/annotation_gate_report.json` | **PENDING placeholder** | 同上 |
| Indicator feasibility audit | `reports/indicator_feasibility_audit.md` / `.json` | Present（`src/indicator_feasibility_audit.py`） | 无标签结构审计：CTQ/ABL/HOT/MAB 可计算性与学生级精度；见 B009 |
| Integrity report | `work/s4_integrity_report.json` | Present | 21 项核验 + 2 项缺陷明细 |
| Worksheet build report | `work/worksheet_build_report.json` | Present | 盲标构建与泄漏自检结果 |
| Retest worksheet builder | `src/build_retest_worksheet.py` | Run 2026-09-25, self-check pass | B010 选项(b)：第 2 轮盲表 |
| Retest blank worksheet (R2) | `data/annotations/human/pilot_worksheet_A_retest.csv` | Blank 0/70 | 第 1 轮提交 ≥24h 后才可打开 |
| Solo retest Gate runner | `src/solo_retest_gate.py` (`report` 子命令) | Pipeline-tested on synthetic only | 输出须标注“intra-rater，非 inter-rater” |
| Development metrics CSV | `reports/development/development_metrics.csv` | Generated 2026-09-25 | 70 行；每行保留 AI_PROVISIONAL / DEVELOPMENT_ONLY；供后续 Demo/图表读取 |
| Development results JSON | `reports/development/development_results.json` | Generated 2026-09-25 | 指标汇总、模型定义、字段限制与 formal_gate_eligible=false |
| Reliability sensitivity CSV | `reports/development/reliability_sensitivity.csv` | Generated 2026-09-25 | 15 个 prompt/context 惩罚条件；原始 vs 校正 ABL/HOT/coverage/gap |
| Reliability model JSON | `reports/development/reliability_model.json` | Generated 2026-09-25 | 权重公式、参数网格、敏感性范围与数学边界 |
| Reliability sensitivity plot | `reports/development/reliability_sensitivity.svg` | Generated 2026-09-25 | 简单 adjusted ABL 对 lambda_prompt / lambda_context 图 |
| Raw/Adjusted metrics | `reports/development/raw_adjusted_metrics.csv` | Generated 2026-09-26 | 统一 Raw vs Adjusted 指标、变化量与支持度 |
| Ablation results | `reports/development/ablation_results.csv` | Generated 2026-09-26 | M0 无校正、M1 置信度、M2 加 prompt、M3 加 context |
| Counterexamples | `reports/development/counterexamples.csv` | Generated 2026-09-26 | 4 条来自 70 条 development records 的真实反例 |
| Research core closure | `reports/development/research_core_closure.md|.json` | Generated 2026-09-26 | 六问研究结论与 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION` 状态 |
| Separation provenance audit | `reports/development/separation_provenance_audit.csv|.json` | Generated 2026-09-25 | 16 条可判读 Evidence 的来源追踪、字段映射与人工复核优先级 |
| Identifiability map | `reports/development/identifiability_map.json` | Generated 2026-09-25 | 核心量 OBSERVABLE / PARTIALLY_IDENTIFIABLE / NOT_IDENTIFIABLE 分类 |
| Partial identification grid | `reports/development/partial_identification_grid.csv` | Generated 2026-09-25 | lambda_prompt/context 与 r_medium 的 assumption-based bounds 扫描 |
| Partial identification summary | `reports/development/partial_identification_summary.json` | Generated 2026-09-25 | ABL/HOT/Gap/有效 Evidence weight 区间及 undefined 区域 |
| Stress tests / ablation | `reports/development/partial_identification_stress_tests.csv`, `partial_identification_ablation.json` | Generated 2026-09-25 | 开发版反例压力测试与组件可测试性 |
| Core figures | `reports/development/core_figure_2_support_heatmap.svg`, `core_figure_3_prompt_vs_effective_evidence.svg`, `core_figure_4_bounds_support.svg`, `core_figure_5_model_flow.svg` | Generated 2026-09-25 | 支持缺口、分数/证据权重边界与模型流程 |
| Demo payload | `reports/demo/demo_payload.json` | Generated 2026-09-25 | Demo 读取的统一开发版数据接口，含参数配置、基线支持、bounds 与 undefined 状态 |
| Demo page | `reports/demo/index.html` | Generated 2026-09-25 | 单一 Bounds Demo 页面：Evidence Overview、Assumption Controls、Score vs Support、Interpretation |
| Paper skeleton | `reports/paper/method_results_skeleton.md` | Generated 2026-09-25 | 方法、识别边界、开发结果与正式替换计划骨架 |
| Paper-ready development draft | `reports/paper/paper_ready_development_draft.md` | Generated 2026-09-25 | 可直接整理进论文的开发版方法/结果草稿，保留正式结果占位 |
| Competition paper narrative | `reports/paper/competition_paper_narrative_draft.md` | Generated 2026-09-25 | 面向竞赛论文的完整主叙事：问题、识别、Bounds、结果、边界与闭环 |
| Judge story | `reports/paper/judge_story_3min.md` | Generated 2026-09-25 | 面向首次接触项目评委的 3 分钟口头故事 |
| Elevator pitch | `reports/paper/elevator_pitch_30s.md` | Generated 2026-09-25 | 问题→方法→发现→价值的 30 秒版本 |
| Core figure interpretation | `reports/paper/core_figures_interpretation.md` | Generated 2026-09-25 | 四张核心图的论文级图名、caption、可解释边界 |
| Judge attack questions | `reports/review/judge_attack_questions.md` | Generated 2026-09-25 | 18 个评委攻击问题与可直接答辩的短答 |
| Top five paper weaknesses | `reports/review/top_5_paper_weaknesses.md` | Generated 2026-09-25 | 当前提交最容易失分的五个论文/答辩薄弱点 |
| Independent bounds recompute | `src/verification/recompute_bounds.py` | Verified 2026-09-25 | 不调用生产函数的只读独立复算器 |
| Raw input recount | `reports/verification/raw_input_recount.json|.csv` | Verified 2026-09-25 | 直接从 provisional CSV 统计原始分布 |
| Independent reproduction grid | `reports/verification/independent_bounds_reproduction.csv` | Verified 2026-09-25 | 693 个参数条件的独立行级复算 |
| Independent reproduction summary | `reports/verification/independent_bounds_summary.json` | Verified 2026-09-25 | 独立 bounds、support、coverage 与 undefined 汇总 |
| Demo consistency report | `reports/verification/demo_payload_consistency.json` | Verified 2026-09-25 | Demo payload 与独立复算逐项核对 |
| Paper numeric consistency | `reports/verification/paper_numeric_consistency.md` | Verified 2026-09-25 | 论文数字和状态口径核对 |
| Core numbers source of truth | `reports/verification/core_numbers_source_of_truth.json` | Verified 2026-09-25 | 当前开发数字唯一验真汇总 |
| Reproduction review | `reports/verification/reproduction_review.md` | Verified 2026-09-25 | 独立审稿式复算结论与 P0/P1/P2 分类 |


## Parallel closeout artifacts (2026-09-26)
| Roadshow deck | outputs/education_ai_evidence_roadshow_v1_final.pptx | Complete, 10 slides, validation receipt in .codex-finalizer | Competition roadshow |
| Development submission package | outputs/submission_package_development_only/ | Complete, 35 manifest entries | Internal review/demo package only |
| Untracked audit | reports/verification/untracked_files_audit_2026-09-26.json | Complete, review-only, no deletions | Source ownership audit |


| Roadshow deck v2 | outputs/education_ai_evidence_roadshow_final.pptx | Complete, editorial green/cream/orange style, 10 slides | Competition roadshow |


| Explain records | `reports/development/explain_records.json` | Generated current round | Deterministic per-record explanation schema |
| What-if sensitivity | `reports/development/what_if_sensitivity.csv` | Generated current round | 3 parameters × 5 perturbations with deltas/status/core-conclusion flags |
| Unified final artifact | `outputs/final_results.json` | Generated current round | Single fact source for paper/demo/PPT/figures; development-only |
| Core figures (five) | `reports/development/raw_vs_adjusted_scatter.svg`, `evidence_reliability_distribution.svg`, `parameter_sensitivity.svg`, `ablation_comparison.svg`, `counterexamples.svg` | Generated current round | Required judge-facing core figures |
| Artifact builder | `src/build_final_artifact.py` | Verified deterministic | No LLM; AI_PROVISIONAL input only |
| Figure builder | `src/build_core_figures.py` | Verified | Standard-library SVG renderer |
| Development Submission Candidate | `paper/development_submission_candidate.md` | Generated current round | Complete development-only paper with transfer boundaries |
| Formal adapter contract | `src/formal_input_adapter.py` | READY_INTERFACE_ONLY | HUMAN_VALIDATED input validation; no formal run |
| Development consistency checker | `src/development_submission_checker.py` | PASS | Cross-checks artifact, figures, paper, demo, PPT, transfer |
| Consistency report | `reports/verification/development_submission_consistency.json` | PASS | 12 checks passed |
| Competition alignment audit | `reports/review/competition_alignment_audit.md` | PASS | Mapping, measurement boundary, NO_EFFECTIVE_EVIDENCE causes, cases, sensitivity, ablation, transfer and three-minute story |

## External transfer validation artifacts (2026-09-26)
| Binance shadow runner | `experiments/transfer_finance/live_shadow/run_live_shadow.py` | Public GET-only; fail-closed safety gate; frozen model |
| Shadow log | `experiments/transfer_finance/live_shadow/live_shadow_log.csv` | 12 BTCUSDT 1m records; pending future outcomes |
| Shadow state | `experiments/transfer_finance/live_shadow/live_shadow_state.json` | Public-only safety state; zero orders/account requests |
| Shadow summary | `experiments/transfer_finance/live_shadow/live_shadow_summary.json` | Current status `INSUFFICIENT_DATA` |
| Shadow README | `experiments/transfer_finance/live_shadow/README.md` | Reproduction and safety scope |

### External Information-Missing Validation
- xperiments/transfer_finance/run_information_missing_validation.py — M0-M3 与 Gate 计算脚本
- xperiments/transfer_finance/information_missing_validation.json — 结构化结果、案例与失败边界
-
eports/demo/index.html — Interactive Model Validation Demo


| Metric dictionary | docs/metric_dictionary.md | Complete | Canonical metric definitions |
| Claim boundary | docs/claim_boundary.md | Complete | Supported vs unsupported claim crosscheck |
| Reliability audit | reports/reliability_component_audit.md | Complete | Weakly justified component register |
| Formal preflight | src/formal_validation_pipeline.py | READY_FAIL_CLOSED | Gate/schema/SHA preflight; no formal metrics before PASS |


| Demo visual acceptance report | `reports/demo/visual_acceptance.md` | PASS | Chrome Headless checks at 1366x768, 1440x900, 1920x1080, 390x844; no P0/P1 blockers |
| Demo acceptance screenshots | `reports/demo/visual_acceptance/1366x768.png`, `1440x900.png`, `1920x1080.png`, `390x844.png` | Complete | Real browser visual evidence |

## Presentation convergence artifacts (2026-09-26)
- `docs/model_presentation/judge_3min_story.md`
- `docs/model_presentation/final_model_overview.md`
- `docs/model_presentation/model_component_table.md`
- `docs/model_presentation/validation_story.md`
- `docs/model_presentation/judge_defense_qa.md`
- `docs/model_presentation/judge_3min_script.md`
- `reports/model_paper_consistency_audit.md`
- `handoff/PROJECT_NOW.md`
| Demo local launcher | `reports/demo/serve_demo.py` | Read-only | 4173 server with project-root experiment data mapping |
## Model tournament evaluator (2026-09-26)

| Artifact | Canonical Path | Status | Purpose |
|---|---|---|---|
| Frozen tournament protocol | `experiments/model_tournament/protocol/model_tournament_protocol.md` | Frozen | Predeclared dimensions, harness, anti-bias audit, and Pareto decision rule |
| Comparison matrix | `experiments/model_tournament/final/model_comparison_matrix.csv` | Development-only | Candidate-by-dimension statuses and provenance |
| Tradeoff report | `experiments/model_tournament/final/model_tradeoff_report.md` | Complete with limitations | Pareto tradeoffs and operating conditions |
| Failure summary | `experiments/model_tournament/final/model_failure_summary.md` | Complete with limitations | Candidate and cross-cutting failure modes |
| Selection evidence | `experiments/model_tournament/final/model_selection_evidence.md` | Complete with limitations | Holdout/leakage/search audit and selection conclusion |
| Paper-ready comparison | `experiments/model_tournament/final/paper_ready_model_comparison.md` | Development-only | Basis for Model Comparison / Robustness / Alternative Specification / Model Selection |
| Defense Q&A | `experiments/model_tournament/final/defense_model_selection_qa.md` | Complete with limitations | Evidence-bounded defense answers |
## Robustness validation artifacts (2026-09-26)
- `src/run_robustness_validation.py`
- `reports/development/robustness_validation_summary.md`
- `reports/robustness/parameter_perturbation.csv` and `.json` / `.svg`
- `reports/perturbation/evidence_perturbation_cases.csv`, `counterfactual_cases.csv`, and `.md`
- `reports/external_transfer/external_transfer_summary.json`, `three_raw_signals_unified.csv`, `evidence_quality_cases.csv`, `.svg`
- `reports/failure_cases/robustness_boundary_findings.json`
- `docs/model_presentation/validation_story.md`

| Core model comparison table | `experiments/model_tournament/final/core_model_comparison_table.md` | Complete, development-only | Reusable five-standard comparison without ranking |
| Model trade-off figure specification | `experiments/model_tournament/final/model_tradeoff_figure_spec.md` | Complete, non-ranking | Demo/PPT design specification |

## Final visual evidence convergence (2026-09-26)
| Artifact | Canonical Path | Status | Purpose |
|---|---|---|---|
| F1 Model Flow | `reports/visual_evidence/final/F1_model_flow.svg` | Final, development-only | Observed Evidence → Reliability → Decision; AIV NOT_SUPPORTED |
| F2 Raw vs Adjusted | `reports/visual_evidence/final/F2_raw_vs_adjusted.svg` | Final, development-only | P108/P105 per-record contribution and 54 undefined records |
| F3 Evidence Degradation | `reports/visual_evidence/final/F3_evidence_degradation.svg` | Final, controlled contrast | P108/P072 support and refusal boundary |
| F4 Parameter Perturbation | `reports/visual_evidence/final/F4_parameter_perturbation.svg` | Final, development-only | Support sensitivity and NOT_APPLICABLE ranking |
| F5 Ablation / Refusal | `reports/visual_evidence/final/F5_ablation_refusal.svg` | Final, development-only | M0–M3 support mass and refusal states |
| F6 External Structural Transfer | `reports/visual_evidence/final/F6_external_structural_transfer.svg` | Final, external structural only | low/medium/high-R ordering and Strategy C boundary |
| Visual manifest | `reports/visual_evidence/final/manifest.json` | Frozen | Placement and stopped-reference registry |
| Visual convergence handoff | `reports/visual_evidence/FINAL_VISUAL_CONVERGENCE.md` | Complete | Main Research citation, conflicts, and risk boundary |

## Cross-tool entry points (2026-09-26, data organization by WorkBuddy)
| Artifact | Canonical Path | Status | Purpose |
|---|---|---|---|
| Data structure index | `docs/DATA_STRUCTURE.md` | Added 2026-09-26 | 7 类数据分类索引（raw/processed/model-input/human-annotation/dev/formal/demo） |
| Data dictionary (full) | `docs/data_dictionary.md` | Extended 2026-09-26 | 全部数据文件字段级字典 + 表间关联 |
| Run guide | `docs/RUN_GUIDE.md` | Added 2026-09-26 | 环境、命令、预期输出、检查方法 |
| Cross-tool handoff | `handoff/CROSS_TOOL_HANDOFF.md` | Added 2026-09-26 | Codex/WorkBuddy 多工具协作、写锁、任务分工 |
| Organization report | `handoff/DATA_ORGANIZATION_REPORT_2026-09-26.md` | Added 2026-09-26 | 本次整理报告（核验结果、修改清单、剩余问题） |
| README | `README.md` | Updated 2026-09-26 | 唯一接手入口 + 指向上述文档 |
