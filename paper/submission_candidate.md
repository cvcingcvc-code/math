# 教育 AI 交互证据的可信评价：Development Submission Candidate

> **DEVELOPMENT_ONLY · NOT_HUMAN_VALIDATED**
> Human Gate 未完成：`PENDING_REAL_HUMAN_R1_R2`；Formal Gate 为 `NOT_RUN`；`formal_gate_eligible=false`。本文所有数值由 `outputs/final_results.json` 提供。

## Problem

AI 辅助学习中的最终文本同时包含学生思考、AI 引导、上下文缺失和标注不确定性。本文回答赛题的方式是建立一个**面向 AI 增量价值评价的证据支持框架**：先确认可观察 Student Evidence，再报告 Reliability 与 Adjusted Evaluation，而不是把当前开发结果解释为已经识别的真实增量或因果效应。

## Measurement Failure

开发样本共 `70` 条，其中 `16` 条具有可判读 Student Evidence。`NO_EVIDENCE` 与 `UNDETERMINED` 不填成低分，权重为零时返回 `NO_EFFECTIVE_EVIDENCE`。

## Raw / Reliability / Adjusted

冻结模型为：`w_i = I(observable_i) × confidence_i × (1−λ_prompt prompt_i) × (1−λ_context context_i)`。

| 指标 | Raw | Adjusted |
|---|---:|---:|
| ABL | 3.5625 | 3.5625 |
| HOT | 0.3750 | 0.3750 |
| Task/Evidence Gap | 1.1250 | 1.1250 |
| Effective weight | 16.0000 | 6.0000 |
| Effective coverage | 0.228571 | 0.085714 |

核心开发现象是 Score 保持稳定，而 Evidence Support 下降。这不是正式人工验证结果，也不是因果效应。

## Sensitivity

What-if 接口覆盖 `lambda_prompt`、`lambda_context`、`r_medium`，每个参数使用 `-20%/-10%/baseline/+10%/+20%`。完整结果见 `reports/development/what_if_sensitivity.csv`，统一 artifact 内含全部 15 行。

## Ablation

M0–M3 共用同一确定性模型，仅逐步加入 confidence、prompt 和 context 修正。当前消融主要说明 Support 变化，不能证明预测准确率或独立 context 效应。

## Model Comparison

Model comparison is organized around five fixed standards: research-question alignment, interpretability, missing-evidence behavior, robustness/sensitivity, and additional assumptions/complexity. The comparison is `DEVELOPMENT_ONLY`: formal outcome fit, Human Gate evidence, and outcome-based external transfer remain unavailable.

The Current Evidence Reliability Model is retained because its rationale is **research-question alignment + transparency + explicit missing-evidence semantics**. It separates observed performance from the support behind that observation, keeps the computation auditable, and distinguishes `NO_EFFECTIVE_EVIDENCE` from a numeric zero. This is not a claim of predictive superiority. Raw-only is the simplest reference; the gated rule is stronger when abstention safety is prioritized; additive and nonlinear formulations expose alternative attenuation behavior. These are operating-condition trade-offs, not a ranking.

| Candidate | Research-question alignment | Interpretability | Missing-evidence behavior | Robustness / sensitivity | Additional assumptions / complexity |
|---|---|---|---|---|---|
| Current Evidence Reliability Model | Strong: evaluates support for observable performance | Strong: reliability components and support are traceable | Explicit `NO_EFFECTIVE_EVIDENCE`; weak support reduces contribution | Development sensitivity and ablation are reproducible; formal validation pending | Low structural complexity; weights are assumptions, not calibrated probabilities |
| Raw-only Baseline | Partial: describes observed signal but ignores support quality | Strongest computational simplicity | Can preserve a score without reliability qualification | Fixed reference; no reliability sensitivity by design | Lowest complexity; omits the support question |
| Rule-based Gated Baseline | Strong for safety-oriented decisions | Strong `ACCEPT / ABSTAIN` semantics | Strong abstention; current threshold has zero defined outputs on observed evidence | Strong available counterexample behavior; threshold-sensitive | Adds threshold and discontinuity; threshold not outcome-validated |
| Multiplicative Formulation | Strong: proportional support attenuation matches the measurement question | Strong and direct | Explicit undefined state and attenuation toward zero | Stable structural behavior in development; formal outcome test pending | No extra attenuation parameter beyond reliability components |
| Additive Formulation (lambda=0.5, 1.0) | Partial: penalty is score-scale dependent | Moderate: simple but less intrinsic | Missing rows remain undefined; low-support scores may remain high | Parameter-dependent behavior; no outcome-based selection | Adds lambda and score-scale assumption |
| Nonlinear Formulation (gamma=0.5, 1.0, 2.0) | Partial to strong: alternative attenuation shapes | Moderate: curvature is explainable but less direct | Explicit undefined state; stronger attenuation as gamma increases | Useful functional-form sensitivity; gamma not identified | Adds gamma and curvature assumption |

No candidate is designated a champion. The reusable comparison table and trade-off figure specification are in `experiments/model_tournament/final/core_model_comparison_table.md` and `experiments/model_tournament/final/model_tradeoff_figure_spec.md`.

## Alternative Model Formulation / Robustness Check

本节将替代结构用于 Robustness Check，而不是 Model Selection。实验使用 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 输入，不能证明任何模型唯一最优，也不支持 predictive superiority 或 causal superiority。

正式核心模型保持为 Multiplicative Model A：`S_adj = S_raw × R`。主模型保留理由统一为 **research-question alignment + transparency + explicit missing-evidence semantics**：它直接回答“观察到的表现有多少证据支持”，结构透明，并在支持为零时返回 `NO_EFFECTIVE_EVIDENCE`。这不是因为 predictive superiority；当前开发数据没有正式 outcome holdout。

| Model | Formula | New parameters | `R→0` behavior | Missing Evidence | Interpretability | Role in this study |
|---|---|---|---|---|---|---|
| A Multiplicative | `S_raw × R` | None | `S_adj→0` | `NO_EFFECTIVE_EVIDENCE` | Direct support scaling | Primary structure and fixed control |
| B Additive | `S_raw − λ(1−R)` | `λ∈{0.5,1.0}` | Retains `S_raw−λ` | `NO_EFFECTIVE_EVIDENCE` | Simple penalty, score-scale dependent | Failure-case comparison |
| C Gated | `R<τ ⇒ ABSTAIN`, else `S_raw` | `τ=0.5` | `ABSTAIN` | `NO_EFFECTIVE_EVIDENCE` | Explicit `ACCEPT / ABSTAIN` | Optional decision layer |
| D Nonlinear | `S_raw × R^γ` | `γ∈{0.5,1.0,2.0}` | `S_adj→0` | `NO_EFFECTIVE_EVIDENCE` | Curvature adds a functional-form choice | Functional-form robustness test |

C 仅作为 `ACCEPT / ABSTAIN` 的操作层候选，不替代连续 Adjusted Score，当前不得宣称最佳 threshold。D 只作为 functional-form robustness / sensitivity test，禁止根据当前数据选择最佳 γ。B 的 failure case 是高 Raw + 低 Reliability 时仍可能保留较高输出；例如开发记录 `P108` 在 Raw=L6、`R=0.375` 时，λ=0.5 输出 5.6875，λ=1.0 输出 5.375。

The alternative-model analysis does not establish the multiplicative specification as uniquely optimal. Instead, it demonstrates that alternative functional forms imply materially different behavior under weak evidence. We therefore retain the multiplicative specification as the parameter-free and transparent primary evaluation structure, while treating gating as an optional decision-layer mechanism and nonlinear formulations as robustness checks.

完整比较结果见 `experiments/model_tournament/formulations/`。所有结果仍为 `DEVELOPMENT_ONLY`，不构成预测或因果优越性证据。

## Counterexamples

P105、P108、P072、P035 展示了高 Raw 分数、低支持度、上下文截断和 `NO_EFFECTIVE_EVIDENCE` 的不同组合。详细记录由 artifact 的 `counterexamples` 提供。

## Core visual evidence (final F1–F6)

The final visual layer uses one frozen interface across the model, evidence, figures, Demo, and presentation. All figures are `AI_PROVISIONAL · DEVELOPMENT_ONLY · Formal Gate NOT_RUN`.

1. **F1 Model Flow** — `reports/visual_evidence/final/F1_model_flow.svg`: Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision. Unreadable Evidence returns `NO_EFFECTIVE_EVIDENCE`; AI Increment is `NOT_SUPPORTED`.
2. **F2 Raw vs Adjusted** — `reports/visual_evidence/final/F2_raw_vs_adjusted.svg`: P108 (`L6`, `R=.375`, contribution `2.25`) and P105 (`L2`, contribution `.75`) are per-record contributions. The panel retains `N=70`, `16` readable records, and `54` `NO_EFFECTIVE_EVIDENCE` records; undefined records are not plotted as zero.
3. **F3 Evidence Degradation** — `reports/visual_evidence/final/F3_evidence_degradation.svg`: controlled development contrasts show P108 support changing when prompt risk is removed, while P072 remains `NO_EFFECTIVE_EVIDENCE` after context-only restoration. This is not a causal experiment.
4. **F4 Parameter Perturbation** — `reports/visual_evidence/final/F4_parameter_perturbation.svg`: local ±20% perturbations show support movement and zero recorded state flips; ranking is `NOT_APPLICABLE`, finite grids are not confidence intervals, and context flatness is `NOT_IDENTIFIED` in this slice.
5. **F5 Ablation / Refusal** — `reports/visual_evidence/final/F5_ablation_refusal.svg`: M0→M1→M2→M3 effective weight is `16→12→6→6`, with P105/P108 low support and P072/P035 refusal states. No accuracy improvement is claimed without true outcomes.
6. **F6 External Structural Transfer** — `reports/visual_evidence/final/F6_external_structural_transfer.svg`: low/medium/high reliability groups are shown for A/B/C strategies. Strategy C reverses the ordering; this is partial structural transfer evidence from a BTC historical paper simulation, not education validation or a trading claim.

## External Transfer Validation (Development-only structural evidence)

本节只同步已有公开行情验证，不重新调参、不声称交易策略：

- structural transfer：DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT（有限结构证据）
- reliability separation：PARTIAL（描述性、开发阶段）
- sensitivity：DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT（当前切片局部结果）
- risk–coverage improvement：未支持
- trading advantage：不得声称

源文件：`experiments/transfer_finance/transfer_validation.json`；仅作小型外部结构迁移验证。

## Limitations

Human Gate 尚未完成，结果保持 `DEVELOPMENT_ONLY`。当前数据缺少正式 HUMAN_VALIDATED 输入、充分的非 AI 对照、独立学习 outcome 和可可靠识别的原生 session。External Transfer 仅提供有限结构迁移证据，不能提升教育主结果的正式验证等级，也不能证明真实跨域泛化。

## Conclusion

当前 Development Candidate 支持一个清晰的方法论结论：评价结果必须同时报告 Raw、Evidence Reliability、Adjusted 和 Evaluability。70 条开发记录中只有 16 条具有可判读 Evidence，54 条返回 `NO_EFFECTIVE_EVIDENCE`；Score 稳定不等于 Evidence Support 稳定。Formal 结论须等待 Human Gate 完成。

## Model vocabulary and identification boundary

本文统一使用以下定义：`Raw Signal` 是 Student Evidence 的可观察等级；`Reliability` 是支持权重 `w_i`，不是概率；`Adjusted` 是 `Raw×Reliability` 的证据加权结果；`Support` 是 `Σw_i`；`Coverage` 为 `n_observed/N` 或 `Σw_i/N`，当前开发分母 `N=70`。证据不足时报告 `ABSTAIN`，有效证据缺失时报告 `NO_EFFECTIVE_EVIDENCE`。`Adjusted Score` 不等于 `AI Increment`。

理论上的 `Delta_raw = Outcome_AI − Outcome_baseline` 需要合法配对的 baseline。当前没有该配对，因此 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，不能将 Adjusted、Support 或 Coverage 解释为 AI 因果增量。所有开发数值标记为 `AI_PROVISIONAL / DEVELOPMENT_ONLY`，HUMAN R1/R2 和 Formal Gate 完成后才可替换为正式结果。
