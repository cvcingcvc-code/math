# PAPER NUMBER LOCK

> 状态：`PAPER_NUMBER_LOCK`。本文件是论文唯一数字源，所有数字逐一从 canonical artifact 核验，不从聊天历史取值。
> 输入身份：`AI_PROVISIONAL / DEVELOPMENT_ONLY`，`formal_gate_eligible=false`，`NOT_HUMAN_VALIDATED`。

## 一、锁定数字（18 组）

### 1. Pilot V1 样本
- **N = 140**（秋 70 + 春 70）。
- **source**：`data/processed/pilot_sample.csv`（140 行）；`docs/DATA_STRUCTURE.md` §2。
- **论文用法**：作为「正式 Pilot V1 全量」背景数字；与 Gate 核心样本 70 区分，不得把 70 外推为 140。

### 2. clean interactions
- **7028 turns**；student = 3522；AI = 3506。
- **source**：`data/processed/clean_interactions.csv`；`docs/DATA_STRUCTURE.md` §2。
- **论文用法**：数据清洗背景。

### 3. Development sample
- **N = 70**，`AI_PROVISIONAL`。
- **source**：`data/annotations/ai/pilot_ai_provisional.csv`（70 行）；`outputs/final_results.json::data_identity.sample_count`。

### 4. Readable Evidence
- **16**（L2×5、L3×5、L4×1、L5×2、L6×3）。
- **source**：`reports/verification/independent_bounds_summary.json::raw_recount`。

### 5. NO_EVIDENCE
- **19**。
- **source**：`reports/verification/independent_bounds_summary.json::raw_recount`。

### 6. UNDETERMINED
- **35**。
- **source**：`reports/verification/independent_bounds_summary.json::raw_recount`。

### 7. NO_EFFECTIVE_EVIDENCE
- **54**（= 19 + 35）。
- **source**：`outputs/final_results.json`（explain_records 中 54 条 raw_score=null）；`reports/development/research_core_closure.md`。
- **论文用法**：54 条返回 `NO_EFFECTIVE_EVIDENCE`，不得写成「54 个 0 分」。

### 8. Raw / Adjusted 关键分数
- **ABL = 3.5625**；**HOT = 0.375**；**Gap = 1.125**（Raw 与 Adjusted 两者相同）。
- **source**：`outputs/final_results.json::raw_summary` / `::adjusted_summary`。
- **必须解释**：Raw 与 Adjusted 相同是「公共缩放退化」结果——16 条可读记录共享 `prompt=true/context=false/confidence=medium`，各加权方案对每条被纳入的分数施加同一常数因子，归一化后抵消。**不得写成 improvement**。

### 9. Ablation effective weight
- **M0 → M1 → M2 → M3 = 16 → 12 → 6 → 6**。
- **source**：`reports/development/ablation_results.csv`；`outputs/final_results.json::ablation[]`。

### 10. Ablation effective coverage
- **0.228571 → 0.171429 → 0.085714 → 0.085714**；**分母 N=70**（全部分析记录，含无证据/不可判读）。
- **source**：`reports/development/ablation_results.csv`。
- **论文用法**：首次出现 coverage 必须写「分母 = 70 development records」。

### 11. Robustness grid
- **693 total = 21 × 11 × 3**；**660 defined**；**33 undefined**。
- **source**：`reports/verification/core_numbers_source_of_truth.json`；`reports/verification/independent_bounds_summary.json::parameter_space`。

### 12. effective weight range
- **0.4 → 16.0**（中位数 5.8）。
- **source**：`reports/verification/independent_bounds_summary.json::bounds.effective_weight`。

### 13. effective coverage range
- **0.005714 → 0.228571**（中位数 0.082857）。
- **source**：`reports/verification/independent_bounds_summary.json::bounds.effective_coverage`。

### 14. parameter perturbation
- **±10% / ±20%** → **0 decision-state flips**；ranking `NOT_APPLICABLE`。
- **source**：`reports/robustness/parameter_perturbation_summary.json`；`outputs/final_results.json::sensitivity.rows`（15 行）。

### 15. Counterexample
- **P108**：Raw = L6，R = 0.375，Adjusted contribution = 2.25，`LOW_SUPPORT`/`ABSTAIN`。
- **P105**：Raw = L2，Adjusted = 0.75，`LOW_SUPPORT`。
- **P072 / P035**：`NO_EFFECTIVE_EVIDENCE`（adjusted 无定义，不填 0）。
- **source**：`outputs/final_results.json::counterexamples`、`::development_results.explain_records`；`reports/development/counterexamples.csv`。

### 16. ML Challenger
- Logistic Regression acc ≈ **0.876**（balanced ≈ 0.863）；Tree ≈ **0.919**（balanced ≈ 0.901）；RF ≈ **0.922**（balanced ≈ 0.894）。
- missing degradation：约 **0.71–0.81**（20%/40% 缺失）。
- RF cross-semester：**0.588**（2026春→2025秋）。
- 必须同时写：**`INSUFFICIENT_FOR_STRONG_ML_CLAIM`**。
- **source**：`experiments/model_tournament/ml_results.json` / `ml_results.csv`；`experiments/model_tournament/ML_CHALLENGER_HANDOFF.md`。

### 17. External Transfer
- BTC **n = 1698**；threshold 0.65。
- **Gate1 SUPPORTED**（信息质量降 → Reliability 0.603→0.408）。
- **Gate2 SUPPORTED**（低 Reliability → coverage 0.394→0.001，abstention 升）。
- **Gate3 NOT SUPPORTED**（低 R future error ≈ **0.525** vs 高 R ≈ **0.528**，无改善）。
- **risk-coverage improvement = false**。
- **source**：`experiments/transfer_finance/transfer_validation.json`；`experiments/transfer_finance/information_missing_validation.json`。

### 18. Human Gate
- **R1 = 0/70**；**R2 = 0/70**；**Formal Gate = NOT_RUN**。
- **source**：`reports/annotation_gate_report.json`；`outputs/final_results.json::reproducibility.formal_boundary`。

---

## 二、数据冲突处理（不得静默选择）

> 论文只使用 canonical experiment artifact。Demo 冲突本轮不修 Demo，仅在论文侧避开并说明。

### CONFLICT 1 — Demo raw semantics（12 vs 16）
- **冲突**：`reports/demo/demo_payload.json` 的 raw_metrics = 12.0 / 0.171429（theta0/M1 confidence-only），而 `outputs/final_results.json` M0 Raw = 16.0 / 0.228571。
- **USED_SOURCE**：`outputs/final_results.json`（M0 Raw = 16 / 0.228571）。
- **REJECTED_SOURCE**：`reports/demo/demo_payload.json` 的 raw_metrics（12 / 0.171429）。
- **WHY**：Demo 的「raw」是 confidence-only theta0/M1（λ_prompt=0、λ_context=0、r_medium=.75），不是无校正的 M0 Raw。论文统一采用统一事实源 `outputs/final_results.json` 的 M0/M3 口径。

### CONFLICT 2 — failure-case null vs 数值
- **冲突**：`reports/failure_cases/development_candidates.json` 把 P105/P108/P072/P035 的 raw_score/adjusted_score 全写 null；`counterexamples.csv` / `final_results.json` 对 P105/P108 有数值（P105 raw=2.0/adj=0.75，P108 raw=6.0/adj=2.25）。
- **USED_SOURCE**：`outputs/final_results.json::counterexamples`（P105=2.0/0.75，P108=6.0/2.25，P072/P035=null）。
- **REJECTED_SOURCE**：`reports/failure_cases/development_candidates.json`（对 P105/P108 的 null 值）。
- **WHY**：`final_results.json` 是统一事实源；P105/P108 是可判读案例，其 raw/adjusted 有定义。P072/P035 不可判读，null 正确保留为 `NO_EFFECTIVE_EVIDENCE`（不填 0）。

### CONFLICT 3 — Demo 默认参数（0/0 vs 0.5/0.5）
- **冲突**：Demo 默认 `λ_prompt=0、λ_context=0`；adjusted artifact 使用 `λ_prompt=0.5、λ_context=0.5`。
- **USED_SOURCE**：`outputs/final_results.json::model_parameters.adjusted_default`（λ=0.5/0.5，M3）。
- **REJECTED_SOURCE**：Demo 默认 λ=0/0（theta0/M1）。
- **WHY**：论文的 Adjusted 口径是 M3（confidence + prompt + context）。Demo 的默认只是展示态初始值，不代表论文默认。

### CONFLICT 4 — run_all.py 32/32 覆盖范围
- **冲突**：`run_all.py` 32/32 只覆盖开发检查，不覆盖 final artifact / figure / Paper / Demo builders。
- **处理**：论文把 32/32 描述为「开发版核心链路可复现」，**不**声称覆盖全链路。复现边界写进 Limitations。
- **USED_SOURCE**：`reports/submission/run_all_report.json`（32/32，六步，exit-code 0）。
- **WHY**：数字真实，但 scope 必须如实标注。

---

## 三、数字一致性基线

- `run_all.py` 开发检查：32/32 PASS（六步 exit-code 0）。
- `src/verify_pilot_integrity.py`：21/21 冻结不变量 + 2 open defects（S4-F01 未来内容泄漏、S4-F02 非盲标队列，均已从标注路径隔离）。
- 独立复算：`reports/verification/core_numbers_source_of_truth.json` 与 `independent_bounds_summary.json` 复现 70/16/19/35、693/660/33、ABL/HOT/Gap、weight/coverage bounds。
