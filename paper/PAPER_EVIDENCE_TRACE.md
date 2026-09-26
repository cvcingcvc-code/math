# PAPER EVIDENCE TRACE

> 唯一 Claim → Evidence → Number → Table/Figure → Source 映射。
> 状态：`PAPER_EVIDENCE_LOCK`。本文件把 `paper/development_submission_candidate.md` 的每一处声明绑定到 canonical artifact。
> 全部数字来自 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 输入；`formal_gate_eligible=false`；`NOT_HUMAN_VALIDATED`。
> 未在本文件登记为「有 canonical source」的声明，不得进入正式论文。

## 表与图固定编号

| 编号 | 内容 | 源 artifact |
|---|---|---|
| Table 1 | 数据与证据结构分布 | `reports/verification/independent_bounds_summary.json` |
| Table 2 | 五条互补验证路径 | `docs/research_story/research_story_summary.md` §5 |
| Table 3 | Baseline 对比（Raw-only / Linear / Rule / Current） | `experiments/model_tournament/baselines/baseline_comparison.md` |
| Table 4 | Ablation（M0–M3） | `reports/development/ablation_results.csv` |
| Table 5 | 反例 / 失败案例 | `outputs/final_results.json::counterexamples` |
| Table 6 | External Transfer 三 Gate | `experiments/transfer_finance/information_missing_validation.json` |
| Table 7 | Alternative Formulations | `experiments/model_tournament/formulations/formulation_results.json` |
| Table 8 | ML Challenger 指标 | `experiments/model_tournament/ml_results.json` |
| Figure 1 | 模型总流程 F1 | `reports/visual_evidence/final/F1_model_flow.svg` |
| Figure 2 | Raw vs Adjusted F2 | `reports/visual_evidence/final/F2_raw_vs_adjusted.svg` |
| Figure 3 | Evidence degradation F3 | `reports/visual_evidence/final/F3_evidence_degradation.svg` |
| Figure 4 | 参数扰动 F4 | `reports/visual_evidence/final/F4_parameter_perturbation.svg` |
| Figure 5 | Ablation 拒判 F5 | `reports/visual_evidence/final/F5_ablation_refusal.svg` |
| Figure 6 | External structural transfer F6 | `reports/visual_evidence/final/F6_external_structural_transfer.svg` |

---

## C1 — Raw Signal 不能代表 Evidence Reliability

- **Claim**：可观察的学生证据等级（Raw Signal，Bloom L2–L6）回答「表现有多高」，不回答「这条表现有多少可审查支撑」；二者是不同量。
- **允许措辞**：Raw Signal 是描述性证据等级，不是 AI 增量、不是可靠性、不是真实能力。
- **禁止措辞**：把 Raw Signal 写成 Delta_raw / AI 增量 / 学习增益 / 真实能力 / 校准概率。
- **canonical source**：`docs/metric_dictionary.md`（"Raw Signal"、"Non-equivalences"）；`docs/model_presentation/final_model_overview.md`。
- **对应数字**：16 条可判读构成 L2×5、L3×5、L4×1、L5×2、L6×3。
- **对应 Table**：Table 1。
- **对应 Figure**：Figure 1（Raw 与 Reliability 是两个独立层）。
- **状态**：`DEVELOPMENT_ONLY`；`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。

## C2 — Evidence Reliability 可以显式分离 performance 和 evidence support

- **Claim**：`w_i = I(observable_i)·c_i·(1−λ_prompt·p_i)·(1−λ_context·t_i)` 把「表现有多高」与「支撑依据有多少」拆成两个量，弱支持贡献被降权而非放大。
- **允许措辞**：Reliability 是声明性支持权重，不是校准概率、不是因果系数；它显式分离 performance 与 evidence support。
- **禁止措辞**：把 R 写成校准概率 / 真实可靠度 / 能力估计 / 因果系数。
- **canonical source**：`docs/model_presentation/model_equations.md`；`docs/model_presentation/reliability_decomposition.md`。
- **对应数字**：`c_i ∈ {high=1, medium=0.75, low=0.5}`；默认 `λ_prompt=0.5, λ_context=0.5`；16 条可判读每条 `R=0.375`。
- **对应 Table**：Table 4（support accounting 变化）。
- **对应 Figure**：Figure 2（Raw vs Adjusted 分离）。
- **状态**：`DEVELOPMENT_ONLY`；`λ_prompt/λ_context/r_medium` 为 `WEAKLY_JUSTIFIED_COMPONENT`（待 Human Gate）。

## C3 — Support/Coverage 必须与 Score 分开报告

- **Claim**：`S=Σw_i`（支持质量）与 `C_eff=Σw_i/N`（覆盖率，分母 N=70）是独立于分数的两个量，必须同时报告。
- **允许措辞**：Support 与 Coverage 与 Score 分开报告；coverage 首次出现必须写明分母 = 全部 70 条 development records。
- **禁止措辞**：把 coverage 分母写成 16；把 support 与 row coverage 混用；把支持量当成分数。
- **canonical source**：`docs/metric_dictionary.md`（"Coverage"、"Non-equivalences"）。
- **对应数字**：`N=70`；`S` 从 16 降到 6；`C_eff` 从 0.228571 降到 0.085714。
- **对应 Table**：Table 3（各模型 coverage 列）。
- **对应 Figure**：Figure 4（Score 稳定 vs Support/Coverage 变化）。
- **状态**：`DEVELOPMENT_ONLY`。

## C4 — 低支持或无证据时需要 ABSTAIN / NO_EFFECTIVE_EVIDENCE

- **Claim**：当 `S=0` 或无有效证据时返回 `NO_EFFECTIVE_EVIDENCE`（不伪造 0 分）；低支持时 `ABSTAIN` / `LOW_SUPPORT`（不按高支持接受）。
- **允许措辞**：ABSTAIN 是「暂缓判断」，NO_EFFECTIVE_EVIDENCE 是「无可评价证据」，均不等于 0 分、不等于「模型失败」。
- **禁止措辞**：把 ABSTAIN 宣传为准确率提升；把 NEE 写成 0 分；把拒绝评分写成「预测错误」。
- **canonical source**：`docs/metric_dictionary.md`（"ABSTAIN"、"NO_EFFECTIVE_EVIDENCE"）；`docs/model_presentation/final_model_overview.md`。
- **对应数字**：54 条（19 NO_EVIDENCE + 35 UNDETERMINED）返回 `NO_EFFECTIVE_EVIDENCE`；16 条可判读返回 `LOW_SUPPORT`。
- **对应 Table**：Table 5。
- **对应 Figure**：Figure 5（拒判语义）。
- **状态**：`DEVELOPMENT_ONLY`；未经 Formal Gate。

## C5 — Score Stability ≠ Evidence Support Stability

- **Claim**：在声明的参数范围内，归一化分数保持稳定，而有效证据支持显著变化，二者稳定性不同。
- **允许措辞**：Score Stability ≠ Evidence Support Stability（分数稳定不等于证据支持稳定）。
- **禁止措辞**：把分数相等解释为任何公式有效/等价/winner；解释为 accuracy parity 或 predictive superiority。
- **canonical source**：`reports/verification/independent_bounds_summary.json`（693 网格 ABL_min=ABL_max=3.5625，effective_weight 0.4–16）；`reports/development/ablation_results.csv`。
- **对应数字**：ABL/HOT/Gap = 3.5625 / 0.375 / 1.125（不变）；effective weight 16→6；coverage 0.228571→0.085714。
- **对应 Table**：Table 4。
- **对应 Figure**：Figure 3、Figure 4。
- **状态**：`DEVELOPMENT_ONLY`，Level 1 descriptive/structural；`formal_gate_eligible=false`。

## C6 — Baseline 表明 Raw-only 缺少 graded support semantics

- **Claim**：Raw-only（M0）把 16 条可判读记录全部当满权重（`w=1`，support mass 16），缺少区分「证据等级」与「证据质量」的通道。
- **允许措辞**：Raw-only 是必要 baseline；它缺少 graded support semantics，不能完整回答研究问题。
- **禁止措辞**：写「Raw-only 错误」；把分数相同写成 Raw-only「与主模型等价」。
- **canonical source**：`experiments/model_tournament/baselines/baseline_comparison.md`。
- **对应数字**：四模型 ABL 均 3.5625；Raw-only support mass=16，主模型=6，线性=8。
- **对应 Table**：Table 3。
- **对应 Figure**：—（Table 3 承载）。
- **状态**：`DEVELOPMENT_ONLY`；`NO_SINGLE_DOMINANT_MODEL`。

## C7 — Ablation 表明 reliability components 会改变 support accounting

- **Claim**：M0→M1→M2→M3 逐项加入 confidence / prompt / context，有效权重 16→12→6→6，组件确实改变支持记账与拒判边界，而非装饰。
- **允许措辞**：组件改变 support accounting；prompt 模块承担当前切片主要支持下降。
- **禁止措辞**：把模块差异解释成独立因果效应；声称 context 已证明「无作用」。
- **canonical source**：`reports/development/ablation_results.csv`；`docs/model_presentation/ablation_story.md`。
- **对应数字**：16→12→6→6；分数恒 3.5625；M2/M3 相同（context 无变异）。
- **对应 Table**：Table 4。
- **对应 Figure**：Figure 5。
- **状态**：`DEVELOPMENT_ONLY`。

## C8 — Sensitivity/Robustness 表明主现象不是单一参数点产生

- **Claim**：对 `λ_prompt/λ_context/r_medium` 做 ±10%/±20% 单变量扰动，0 个 decision-state flips，分数稳定而 support 变化；主现象是局部结构现象。
- **允许措辞**：局部结构稳定性；在有限声明网格内结论不锁定单一参数点。
- **禁止措辞**：写成统计置信区间 / 全局稳健性 / 参数已校准。
- **canonical source**：`reports/robustness/parameter_perturbation_summary.json`；`reports/verification/independent_bounds_summary.json`。
- **对应数字**：15 个扰动条件 → 0 flips；693 网格、660 defined、33 undefined；effective weight 0.4–16、coverage 0.005714–0.228571；ranking `NOT_APPLICABLE`。
- **对应 Table**：Table 2（Sensitivity 行）。
- **对应 Figure**：Figure 4。
- **状态**：`DEVELOPMENT_ONLY`。

## C9 — Failure Cases 说明 High Raw 不一定意味着 High Support

- **Claim**：P108 Raw=L6（最高）但 R=0.375、Adjusted contribution=2.25、LOW_SUPPORT/ABSTAIN；P072/P035 无可判读证据返回 NEE，不填 0。
- **允许措辞**：High Raw ≠ High Evidence Support；Missing Evidence ≠ Score 0。
- **禁止措辞**：写成「模型预测正确/错误」；写成 accuracy 或真实错误率；写「ABSTAIN 后实际正确」。
- **canonical source**：`outputs/final_results.json::counterexamples`；`reports/development/counterexamples.csv`。
- **对应数字**：P108 Raw=6.0、R=0.375、adj=2.25；P105 Raw=2.0、adj=0.75；P072/P035 adj=null。
- **对应 Table**：Table 5。
- **对应 Figure**：Figure 2、Figure 5。
- **状态**：`DEVELOPMENT_ONLY`；无 true outcome，`OUTCOME NOT AVAILABLE`。

## C10 — External Transfer 说明结构可迁移，但不能证明教育泛化或交易优势

- **Claim**：同一 `Raw→Reliability→Adjusted→ACCEPT/ABSTAIN` 结构在 BTC 历史样本上可运行，说明结构可迁移；但仅 structural transfer。
- **允许措辞**：structural portability / 有限结构迁移；`EXTERNAL_TRANSFER / DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`。
- **禁止措辞**：教育泛化、交易优势、预测优越、universal generalization。
- **canonical source**：`experiments/transfer_finance/transfer_validation.json`；`experiments/transfer_finance/information_missing_validation.json`。
- **对应数字**：BTC n=1698，threshold 0.65；Gate1/Gate2 SUPPORTED，Gate3 NOT SUPPORTED；risk-coverage improvement = false。
- **对应 Table**：Table 6。
- **对应 Figure**：Figure 6。
- **状态**：`EXTERNAL_TRANSFER`。

## C11 — ML Challenger 不足以支持 strong ML claim

- **Claim**：逻辑回归/浅层树/探索性 RF 表面 CV 指标不低，但 16 个正例、代理标签、无 holdout、缺失降级、跨学期不稳，结论为 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`。
- **允许措辞**：ML 是有价值的 robustness challenger；`INSUFFICIENT_FOR_STRONG_ML_CLAIM`；`NO_SINGLE_DOMINANT_MODEL`。
- **禁止措辞**：写 ML 失败/被击败；写 handcrafted 模型优于 ML；写 ML winner。
- **canonical source**：`experiments/model_tournament/ML_CHALLENGER_HANDOFF.md`。
- **对应数字**：LogReg acc≈0.876、Tree≈0.919、RF≈0.922（CV）；缺失后 0.71–0.81；RF 跨学期 0.588。
- **对应 Table**：Table 8。
- **对应 Figure**：—（Table 8 承载）。
- **状态**：`DEVELOPMENT_ONLY`；`ML_CHALLENGER / FINAL_HANDOFF`。

## C12 — Alternative Formulations 没有形成 single dominant model

- **Claim**：乘法/加法/gated/非线性四种结构无一个在拟合、安全、覆盖、可解释、迁移、复杂度上全面胜出。
- **允许措辞**：`NO_SINGLE_DOMINANT_MODEL`；作为 structural robustness check。
- **禁止措辞**：选出「最佳」公式或阈值；声称某公式预测/因果更优。
- **canonical source**：`experiments/model_tournament/final/model_selection_evidence.md`；`experiments/model_tournament/formulations/formulation_results.json`。
- **对应数字**：B(λ=0.5) RMSE vs Raw = 0.3125（最小）；C gated 在 16 条全部 ABSTAIN；rank stability 1.0。
- **对应 Table**：Table 7。
- **对应 Figure**：—（Table 7 承载）。
- **状态**：`DEVELOPMENT_ONLY`。

## C13 — Human Formal Gate 尚未完成

- **Claim**：Human R1=0/70 VALID、R2=0/70、Formal Gate `NOT_RUN`；所有结果不得升级为正式验证。
- **允许措辞**：`PENDING_REAL_HUMAN_R1_R2`；`NOT_HUMAN_VALIDATED`；Formal Gate `NOT_RUN`；同一标注者 test-retest（非 inter-rater）。
- **禁止措辞**：Kappa / Alpha 已有正式结果；Formal Gate 已 PASS；把 AI provisional 标签当人工标签；把 filled_from_B 派生副本当 R1/R2。
- **canonical source**：`reports/annotation_gate_report.json`；`reports/RESEARCH_GATE_STATUS.md`；`FORMAL_GATE_SWITCH.md`。
- **对应数字**：R1=0/70、R2=0/70、AI_ASSISTED=70/70（DEVELOPMENT_ONLY，非正式替代）。
- **对应 Table**：—（正文 Limitations 承载）。
- **对应 Figure**：—。
- **状态**：`BLOCKED_BY_HUMAN_ANNOTATION`；`PENDING HUMAN-ANNOTATION INTAKE VERIFICATION`。

---

## 无法进入论文的 Claim（无 canonical source）

- 任何「AI 增量 / 学习增益 / 因果效果」：`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，无合法 paired outcome。
- 任何「准确率提升 / abstain 提高精度」：`accuracy_coverage_audit = NOT_RUN`，无 true outcome。
- 任何「R 是校准概率」：`c_i/λ` 是假设参数，未外部校准。
- 任何「主模型最优 / 胜出」：`NO_SINGLE_DOMINANT_MODEL`。
- 任何「Kappa / Alpha 正式一致性」：Human Gate 未运行，test-retest（非 inter-rater）尚无结果。
