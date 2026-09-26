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
| Blind worksheet A | `data/annotations/human/pilot_worksheet_A.csv` | S4 Pilot | Present, blank labels, 70 rows | B010 R1 第一轮人工盲标表 |
| Blind worksheet B | `data/annotations/human/pilot_worksheet_B.csv` | S4 Pilot | Present, retained legacy blank sheet, 70 rows | 当前 Gate 不使用；B010 改用单人 R1/R2 重测 |
| Annotator instructions | `data/annotations/human/README_ANNOTATOR.md` | S4 Pilot | Present | 标注者执行说明 |
| Worksheet key | `data/annotations/_keys/pilot_worksheet_key.csv` | S4 Pilot | Present, analysis-side only | 盲标映射（agent/path/抽样/预标注） |
| WorkBuddy annotations | `data/annotations/workbuddy/` | S4 Pilot | Empty, awaiting input | 预留；收到后新增，不覆盖原始数据 |

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
| Gate report generator | `src/annotation_gate_report.py` | Verified | 一致性、混淆矩阵、双轴 gap、成本、8 问 |
| Metric feasibility (draft) | `src/metric_feasibility.py` | **未运行、来源未核实**，与上一行功能重叠 | 暂不使用；待负责人决定保留或归档 |
| Indicator feasibility audit | `src/indicator_feasibility_audit.py` | Run 2026-09-25 | 无标签结构审计：CTQ/ABL/HOT/MAB 可计算性 |
| Development annotation loader | `src/development_data.py` | Added 2026-09-25 | 显式 `--mode development` 读取 AI_PROVISIONAL；默认 formal 路径不变；不可进入正式 Gate |
| Development experiment entry | `src/run_development_experiment.py` | Added 2026-09-25 | 70 条 provisional 数据的透明行级 ABL/HOT/coverage/gap 探索链路；不训练分类器、不进入正式 Gate |
| Core closure builder | `src/build_core_closure.py` | Added 2026-09-26 | Raw/Adjusted 指标、M0–M3 消融、真实反例与研究结论；仅 DEVELOPMENT_ONLY |
| Worksheet-safe reader | `src/csv_safe_read.py` | Added 2026-09-26 | 兼容 UTF-8 / GB18030 只读读取人工工作表；不改写文件与标签 |

## Reports

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

