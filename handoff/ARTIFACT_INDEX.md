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

