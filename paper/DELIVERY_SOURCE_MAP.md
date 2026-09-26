# DELIVERY SOURCE MAP

> 状态：`DELIVERY_SOURCE_MAP = READY`。本文件是论文每一处核心声明到 canonical artifact 的完整溯源映射。
> 这是下一阶段 `FINAL_CONSISTENCY_AUDIT` 的直接输入。
> 论文 canonical 路径：`paper/paper_v2_submission_candidate.md`（HEAD `71f0276`）。

---

## 一、Claim → Data → Experiment → Result Artifact → Figure/Table → Paper Section

### C1 — Raw Signal 不能代表 Evidence Reliability

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 可观察的学生证据等级回答"表现有多高"，不回答"这条表现有多少可审查支撑" | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv`（70 行） | `data/annotations/ai/` |
| Experiment | 独立复算 raw_recount | `reports/verification/independent_bounds_summary.json::raw_recount` |
| Result Artifact | 16 条可判读（L2×5, L3×5, L4×1, L5×2, L6×3） | 同上 |
| Figure/Table | Figure 1（F1_model_flow.svg）、Table 1 | §3, §4.2 |
| Paper Section | §2.1, §3.1, §4.2 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | Demo Panel A（Raw vs Adjusted） | `reports/demo/` |

### C2 — Evidence Reliability 可以显式分离 performance 和 evidence support

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | `w_i = I(observable_i)·c_i·(1−λ_prompt·p_i)·(1−λ_context·t_i)` 把"表现有多高"与"支撑依据有多少"拆成两个量 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Reliability model 冻结运行 | `outputs/final_results.json::model_parameters` |
| Result Artifact | `c_i ∈ {high=1, medium=0.75, low=0.5}`；默认 `λ_prompt=0.5, λ_context=0.5`；16 条每条 `R=0.375` | 同上 |
| Figure/Table | Figure 2（F2_raw_vs_adjusted.svg）、Table 4 | §3.1, §6.1 |
| Paper Section | §3.2 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | Demo Panel B（λ/r 敏感性） | `reports/demo/` |

### C3 — Support/Coverage 必须与 Score 分开报告

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | `S=Σw_i`（支持质量）与 `C_eff=Σw_i/N`（覆盖率，分母 N=70）是独立于分数的两个量 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Adjusted evaluation 冻结运行 | `outputs/final_results.json::adjusted_summary` |
| Result Artifact | `N=70`；`S` 从 16 降到 6；`C_eff` 从 0.228571 降到 0.085714 | 同上 |
| Figure/Table | Figure 4（F4_parameter_perturbation.svg）、Table 3 | §6.3 |
| Paper Section | §3.4 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | Demo Panel C（Effective Coverage） | `reports/demo/` |

### C4 — 低支持或无证据时需要 ABSTAIN / NO_EFFECTIVE_EVIDENCE

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 当 `S=0` 或无有效证据时返回 `NO_EFFECTIVE_EVIDENCE`（不伪造 0 分） | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Decision layer 冻结运行 | `outputs/final_results.json::development_results.explain_records` |
| Result Artifact | 54 条返回 `NO_EFFECTIVE_EVIDENCE`；16 条可判读返回 `LOW_SUPPORT` | 同上 |
| Figure/Table | Figure 5（F5_ablation_refusal.svg）、Table 5 | §6.2, §6.4 |
| Paper Section | §3.5 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | Demo Panel E（Counterexamples） | `reports/demo/` |

### C5 — Score Stability ≠ Evidence Support Stability

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 在声明的参数范围内，归一化分数保持稳定，而有效证据支持显著变化 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | 693 格声明网格复算 | `reports/verification/independent_bounds_summary.json::bounds` |
| Result Artifact | ABL/HOT/Gap = 3.5625 / 0.375 / 1.125（不变）；effective weight 0.4–16；coverage 0.005714–0.228571 | 同上 |
| Figure/Table | Figure 3（F3_evidence_degradation.svg）、Figure 4（F4_parameter_perturbation.svg）、Table 4 | §6.3 |
| Paper Section | §9.1 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | Demo Panel B | `reports/demo/` |

### C6 — Baseline 表明 Raw-only 缺少 graded support semantics

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | Raw-only（M0）把 16 条可判读记录全部当满权重（`w=1`，support mass 16），缺少区分"证据等级"与"证据质量"的通道 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | 四候选 baseline 对比 | `experiments/model_tournament/baselines/baseline_comparison.md` |
| Result Artifact | 四模型 ABL 均 3.5625；Raw-only support mass=16，主模型=6，线性=8 | 同上 |
| Figure/Table | Table 4（Baseline 对比） | §6.1 |
| Paper Section | §6.1 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

### C7 — Ablation 表明 reliability components 会改变 support accounting

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | M0→M1→M2→M3 逐项加入 confidence / prompt / context，有效权重 16→12→6→6 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Ablation M0–M3 | `reports/development/ablation_results.csv`；`outputs/final_results.json::ablation[]` |
| Result Artifact | 16→12→6→6；分数恒 3.5625；M2/M3 相同（context 无变异） | 同上 |
| Figure/Table | Figure 5（F5_ablation_refusal.svg）、Table 5 | §6.2 |
| Paper Section | §6.2 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

### C8 — Sensitivity/Robustness 表明主现象不是单一参数点产生

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 对 `λ_prompt/λ_context/r_medium` 做 ±10%/±20% 单变量扰动，0 个 decision-state flips | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Parameter perturbation | `reports/robustness/parameter_perturbation_summary.json`；`outputs/final_results.json::sensitivity.rows` |
| Result Artifact | 15 个扰动条件 → 0 flips；693 网格、660 defined、33 undefined | 同上 |
| Figure/Table | Figure 4（F4_parameter_perturbation.svg）、Table 6 | §6.3 |
| Paper Section | §6.3 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

### C9 — Failure Cases 说明 High Raw 不一定意味着 High Support

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | P108 Raw=L6（最高）但 R=0.375、Adjusted contribution=2.25、LOW_SUPPORT/ABSTAIN | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Counterexample extraction | `outputs/final_results.json::counterexamples`；`reports/development/counterexamples.csv` |
| Result Artifact | P108 Raw=6.0、R=0.375、adj=2.25；P105 Raw=2.0、adj=0.75；P072/P035 adj=null | 同上 |
| Figure/Table | Figure 2（F2_raw_vs_adjusted.svg）、Figure 5、Table 7 | §3.1, §6.2, §6.4 |
| Paper Section | §6.4 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | Demo Panel E | `reports/demo/` |

### C10 — External Transfer 说明结构可迁移，但不能证明教育泛化或交易优势

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 同一 `Raw→Reliability→Adjusted→ACCEPT/ABSTAIN` 结构在 BTC 历史样本上可运行 | — |
| Data | BTC-USD 历史纸面模拟（n=1698） | `experiments/transfer_finance/` |
| Experiment | Information-missing validation | `experiments/transfer_finance/information_missing_validation.json` |
| Result Artifact | BTC n=1698，threshold 0.65；Gate1/Gate2 SUPPORTED，Gate3 NOT SUPPORTED；risk-coverage improvement = false | 同上 |
| Figure/Table | Figure 6（F6_external_structural_transfer.svg）、Table 8 | §6.5 |
| Paper Section | §6.5 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

### C11 — ML Challenger 不足以支持 strong ML claim

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 逻辑回归/浅层树/探索性 RF 表面 CV 指标不低，但 16 个正例、代理标签、无 holdout、缺失降级、跨学期不稳 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | ML tournament | `experiments/model_tournament/ml_results.json`；`experiments/model_tournament/ML_CHALLENGER_HANDOFF.md` |
| Result Artifact | LogReg acc≈0.876、Tree≈0.919、RF≈0.922（CV）；缺失后 0.71–0.81；RF 跨学期 0.588 | 同上 |
| Figure/Table | Table 9, Table 10 | §7 |
| Paper Section | §7 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

### C12 — Alternative Formulations 没有形成 single dominant model

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | 乘法/加法/gated/非线性四种结构无一个在拟合、安全、覆盖、可解释、迁移、复杂度上全面胜出 | — |
| Data | `data/annotations/ai/pilot_ai_provisional.csv` | `data/annotations/ai/` |
| Experiment | Formulation comparison | `experiments/model_tournament/formulations/formulation_results.json` |
| Result Artifact | B(λ=0.5) RMSE vs Raw = 0.3125（最小）；C gated 在 16 条全部 ABSTAIN；rank stability 1.0 | 同上 |
| Figure/Table | Table 11 | §8 |
| Paper Section | §8 | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

### C13 — Human Formal Gate 尚未完成

| 层 | 内容 | 路径 |
|---|---|---|
| Claim | Human R1=0/70 VALID、R2=0/70、Formal Gate `NOT_RUN`；所有结果不得升级为正式验证 | — |
| Data | `data/annotations/human/pilot_worksheet_A.csv`（R1）、`pilot_worksheet_A_retest.csv`（R2） | `data/annotations/human/` |
| Experiment | Annotation gate report | `reports/annotation_gate_report.json`；`reports/RESEARCH_GATE_STATUS.md` |
| Result Artifact | R1=0/70、R2=0/70、AI_ASSISTED=70/70（DEVELOPMENT_ONLY，非正式替代） | 同上 |
| Figure/Table | —（正文 Limitations 承载） | §10 |
| Paper Section | §10（GAP-1） | `paper/paper_v2_submission_candidate.md` |
| Demo Section | — | — |

---

## 二、canonical artifact 索引

| 用途 | 路径 |
|---|---|
| 唯一数字源 | `paper/PAPER_NUMBER_LOCK.md` |
| 声明 → 证据 → 数字 → 表/图映射（C1–C13） | `paper/PAPER_EVIDENCE_TRACE.md` |
| 文献引用映射与缺口 | `paper/LITERATURE_CITATION_MAP.md` |
| 统一事实源（JSON） | `outputs/final_results.json` |
| 独立复算源 | `reports/verification/independent_bounds_summary.json` |
| 核心数字源 | `reports/verification/core_numbers_source_of_truth.json` |
| 冻结词汇与非等价关系 | `docs/metric_dictionary.md` |
| 6 张 canonical figure | `reports/visual_evidence/final/F1–F6_*.svg` |
| 旧版 V1 论文（保留可追溯，本文不覆盖） | `paper/development_submission_candidate.md` |
| 结构重写 canonical 稿（本文的原型） | `paper/paper_v2_candidate.md` |

---

## 三、禁止进入论文的 Claim（无 canonical source）

- 任何「AI 增量 / 学习增益 / 因果效果」：`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，无合法 paired outcome。
- 任何「准确率提升 / abstain 提高精度」：`accuracy_coverage_audit = NOT_RUN`，无 true outcome。
- 任何「R 是校准概率」：`c_i/λ` 是假设参数，未外部校准。
- 任何「主模型最优 / 胜出」：`NO_SINGLE_DOMINANT_MODEL`。
- 任何「Kappa / Alpha 正式一致性」：Human Gate 未运行，test-retest（非 inter-rater）尚无结果。

---

_DELIVERY_SOURCE_MAP = READY · 下一阶段：FINAL_CONSISTENCY_AUDIT_
