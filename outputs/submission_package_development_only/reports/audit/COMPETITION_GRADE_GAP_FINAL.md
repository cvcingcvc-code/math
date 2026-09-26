# COMPETITION_GRADE_GAP_FINAL

状态：`COMPETITION_GRADE_AUDIT = PASS_WITH_DECLARED_LIMITS`
日期：2026-09-27
项目：教育 AI 增量价值评价（Development-only convergence）

## 0. 审计口径

本审计只核对既有 canonical paper、`FINAL_CLAIM_LOCK.md`、冻结 F1–F6、最终 PPT、正式 Demo 与真实外部迁移 artifact；不新增实验、不修改原始数据、不提升研究 Claim。

唯一研究问题：当观测证据存在缺失、冲突或可信度差异时，如何避免直接把 Raw Signal 当成可信结论，并显式报告 Evidence Reliability、Support / Coverage，且在证据不足时允许 `ABSTAIN`？

## 1. 结构审计

| 维度 | 状态 | 结论 |
|---|---|---|
| Problem Definition | PASS | Paper、PPT、Demo 均明确 measurement / identifiability 问题、研究对象、输出变量与边界；不声称 AI 学习增益。 |
| Assumptions | PASS | `Reliability` 明确不是 probability、不是 causal coefficient；`lambda_prompt`、`lambda_context`、`confidence weight` 被声明为透明设计假设，并标注校准不足。 |
| Symbol / Formula Consistency | PASS | `w_i`、`Adjusted_i`、Support、Coverage、Decision 在锁、论文、Demo 中语义一致；Coverage 分母固定为 N=70。 |
| Data Audit | PASS | 明确区分 Pilot N=140 与 development N=70；16 readable、19 NO_EVIDENCE、35 UNDETERMINED、54 NO_EFFECTIVE_EVIDENCE。没有把 70 外推为总体。 |
| Baseline | PASS | Raw-only 与当前模型在同一 70 条记录上对照，直接回答“不建 Reliability 会怎样”。 |
| Ablation | PASS | `16 → 12 → 6 → 6` 与 coverage `0.228571 → 0.171429 → 0.085714 → 0.085714` 清楚解释为 support accounting / refusal boundary，不是 accuracy gain。 |
| Sensitivity / Robustness | PASS_WITH_LIMIT | 693=21×11×3，660 defined、33 undefined，扰动 0 decision-state flips；Paper/Demo/PPT 均声明这是 local structural stability，不是 universal robustness 或置信区间。 |
| Failure / Counterexamples | PASS | P108、P105、P072、P035 均保留；高 Raw 可 `ABSTAIN`，无证据返回 `NO_EFFECTIVE_EVIDENCE`，不填 0。 |
| Challenger | PASS | ML 与 alternative formulations 被定位为挑战者；保留 `INSUFFICIENT_FOR_STRONG_ML_CLAIM` 与 `NO_SINGLE_DOMINANT_MODEL`，没有制造 winner。 |
| External Transfer | PASS | BTC n=1698 仅作 structural transfer；Gate1 SUPPORTED、Gate2 SUPPORTED、Gate3 NOT SUPPORTED，且保留 `risk-coverage improvement = false`。 |
| Limitations | PASS | Human Gate `R1=0/70`、`R2=0/70`、Formal Gate `NOT_RUN`，AI Increment `NOT_SUPPORTED`，16 条同质性、无 true outcome、参数未校准均已前置/明确展示。 |
| Reproducibility | NEEDS_MINIMAL_FIX | 开发核心 `run_all.py` 可复算 70/16/19/35、693/660/33 与核心指标；但 provisional label 生成脚本缺失，最终图/论文/Demo 全链路未由单一命令重建。该边界已在 package README 与 paper limitation 中声明。 |

## 2. 最终数据锁核验

| 项目 | 锁定值 | 状态 |
|---|---:|---|
| Development N | 70 | PASS |
| Readable Evidence | 16 | PASS |
| NO_EVIDENCE / UNDETERMINED | 19 / 35 | PASS |
| NO_EFFECTIVE_EVIDENCE | 54 | PASS |
| ABL / HOT / aggregate Gap | 3.5625 / 0.375 / 1.125 | PASS |
| P108 Adjusted contribution | 2.25 (= 6×0.375) | PASS，未与 aggregate Gap 混淆 |
| Ablation effective weight | 16 → 12 → 6 → 6 | PASS |
| Ablation coverage | 0.228571 → 0.171429 → 0.085714 → 0.085714 | PASS |
| Parameter grid | 693 / 660 defined / 33 undefined | PASS |
| ML challenger | 0.876 / 0.919 / 0.922 | PASS |
| BTC transfer | n=1698；Gate1/2 supported；Gate3 not supported | PASS |
| Human / AI status | R1 0/70；R2 0/70；NOT_RUN；NOT_SUPPORTED | PASS |

## 3. 五方语义对表

- `FINAL_CLAIM_LOCK ↔ Paper`：主研究问题、六层链路、主结论与负结果一致。
- `Paper ↔ F1–F6`：六图来源与 caption 已列入论文附录，F6 明确为 structural transfer，不是交易主张。
- `Paper ↔ PPT`：10 页故事线按问题→模型→70/16/54→核心机制→验证→Failure→Challenger/Transfer→Claim Boundary→Conclusion 展开。
- `Paper ↔ Demo`：正式 Demo 首屏、模型链、核心发现、Failure、External Transfer、Evidence Status 覆盖同一锁定口径。
- `NUMBER_DRIFT = 0`、`CLAIM_DRIFT = 0`、`SEMANTIC_DRIFT = 0`。

## 4. 竞赛级判断

`CORE_RESEARCH_STORY = PASS`

数学建模贡献不是“做了一个网页”或“跑了很多模型”，而是把现实问题抽象为：

`Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support / Coverage → Decision`

并用 baseline、ablation、sensitivity、failure、challenger、external structural transfer 从不同角度攻击同一个 Research Question。

`External Transfer = STRUCTURAL VALIDATION ONLY`：Gate1/2 支持结构行为可以迁移；Gate3 失败说明 Reliability 尚未被证明是未来正确性的 calibrated predictor。

## 5. 已知非阻塞边界

- Formal Human Gate：`NOT_RUN`。
- AI Increment：`NOT_SUPPORTED`。
- ML strong claim：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`。
- External Gate3：`NOT_SUPPORTED`。
- Demo `/favicon.ico` 404：已知非阻塞 P2，冻结文件不修。
- 端到端最终工件自动重建：尚未证明，不应包装为完全可复现。

## 6. 最终状态

- `COMPETITION_GRADE_AUDIT = PASS_WITH_DECLARED_LIMITS`
- `CORE_RESEARCH_STORY = PASS`
- `MATHEMATICAL_MODEL_PRESENTATION = PASS`
- `VALIDATION_CHAIN = PASS`
- `FAILURE_CASES = PASS`
- `QUANT_STRUCTURAL_TRANSFER = PASS`
- `P0 = 0`
- `P1 = 0`
- `TOMORROW_CODE_CHANGE_REQUIRED = NO`

本报告是审计记录，不改变正式 Demo、论文、六图或研究数据。
