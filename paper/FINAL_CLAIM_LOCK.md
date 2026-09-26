# FINAL CLAIM LOCK

> 状态：`FINAL_CLAIM_LOCK`。本文件是论文冻结前的最终口径锁定，只读提取自 canonical paper 与数字锁，**不产生任何新研究结论**。
> 唯一 canonical paper：`paper/paper_v2_submission_candidate.md`（SHA256 `8b478b7e5a1f7cfa7a1176ac97349c26518c4782f29cfcb78ac5f13e3bd47a15`）。
> 数字唯一源：`paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字）+ `outputs/final_results.json`。
> 输入身份：`AI_PROVISIONAL / DEVELOPMENT_ONLY`，`formal_gate_eligible = false`，`NOT_HUMAN_VALIDATED`。

---

## A. Research Question（全文唯一正式研究问题）

> 当观测证据存在缺失、冲突或可信度差异时，如何避免直接把 Raw Signal 当成可信结论，并构建一个能够显式报告 Evidence Reliability 与 Support / Coverage，且在证据不足时允许 ABSTAIN 的可审查评价框架？

**问题类型**：`measurement / identifiability`（测量与可识别性）问题。

**它明确不是**（必须锁定为否定边界）：
- 不是「AI 是否提高成绩」；
- 不是「学生真实能力预测」；
- 不是「AI causal learning gain」；
- 不是「AI 与 baseline 的正式效果识别」。

上述问题都需要当前项目不具备的条件（合法配对的 `Outcome_AI` / `Outcome_baseline`、独立学习 outcome、正式人工标注），当前状态为 `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。

---

## B. Main Pipeline（主模型链路，固定不变）

```
Observed Evidence
  → Raw Signal
  → Evidence Reliability
  → Adjusted Evaluation
  → Support / Coverage
  → ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE
```

**固定要点**：
- Raw 与 Reliability 是两个独立层（这是全文结论的结构前提）。
- `w_i = I(observable_i) · c_i · (1 − λ_prompt · p_i) · (1 − λ_context · t_i)`。
- `c_i ∈ {high=1.0, medium=0.75, low=0.5}`；默认 `λ_prompt = 0.5`、`λ_context = 0.5`、`r_medium = 0.75`（冻结声明参数，`WEAKLY_JUSTIFIED_COMPONENT`）。
- `Adjusted_i = Raw_i × w_i`（仅在 `I(observable_i) = 1` 时有定义）。
- `S = Σ w_i`；`C_eff = Σ w_i / N`（分母 `N = 70`）。
- 决策语义：`ABSTAIN` 是合理输出（不是模型失败）；`NO_EFFECTIVE_EVIDENCE` 是「无可评价证据」（**不是 0 分**）。
- fail-closed 规则：`Σw_i = 0` 时返回 `NO_EFFECTIVE_EVIDENCE`，不填 0。

---

## C. Main Conclusion（主结论，唯一）

> **Score Stability ≠ Evidence Support Stability.**
> 分数稳定，不等于证据支持稳定——稳定的评分不意味着支撑该评分的证据同样稳定、充分或可信。

**结论级别**：`descriptive / structural`（Evidence Level 1），标记 `DEVELOPMENT_ONLY`。

**不升级为**：universal theorem；任何模型最优；任何预测准确率提升；任何因果 AI 增量；跨域普适性。

**三条负结果必须保留**：
1. External Transfer Gate3 `NOT SUPPORTED`；
2. `NO_SINGLE_DOMINANT_MODEL`（替代公式与 ML 均无胜者）；
3. `INSUFFICIENT_FOR_STRONG_ML_CLAIM`（ML Challenger 不足以支持 strong ML claim）。

---

## D. 状态边界（STATUS BOUNDARY）

| 字段 | 锁定值 |
|---|---|
| 输入身份 | `AI_PROVISIONAL` |
| 状态 | `DEVELOPMENT_ONLY` |
| Human R1 | **0/70 VALID** |
| Human R2 | **0/70** |
| Formal Gate | **`NOT_RUN`** |
| `formal_gate_eligible` | **`false`** |
| `AI_INCREMENT_IDENTIFICATION` | **`NOT_SUPPORTED`** |
| 论文晋升状态 | `PAPER_V2_CANONICAL_DEVELOPMENT`（不标 `FORMAL_FINAL`） |
| 标注设计 | `single_annotator_test_retest`（非 inter-rater） |
| 统一事实源 | `outputs/final_results.json` |

**不可声称**：
- 不声称 FORMAL_SUPPORTED；
- 不声称 AI 提高学习效果 / 导致成绩提升；
- 不声称 AI increment 已被识别 / causal learning gain；
- 不声称 ML winner / ML 被击败 / handcrafted 优于 ML；
- 不声称 accuracy 提升 / 准确率提升；
- 不声称交易优势 / 教育泛化 / universal generalization；
- 不声称 R 是校准概率；
- 不声称 Kappa / Alpha 正式一致性（Human Gate 未运行）。

---

## E. 核心数量（CORE NUMBERS，全部锁定）

以下数字来自 `paper/PAPER_NUMBER_LOCK.md` 18 组锁定数字，正文、表格、图、Demo 均不得偏离。

| # | 量 | 锁定值 |
|---|---|---|
| 1 | Pilot V1 全量样本 | **N = 140**（秋 70 + 春 70） |
| 2 | 上游清洗主结果 | **7028 turns**（student 3522 / AI 3506） |
| 3 | 当前 development slice | **N = 70**（`AI_PROVISIONAL`） |
| 4 | 可判读 Student Evidence | **16**（L2×5、L3×5、L4×1、L5×2、L6×3） |
| 5 | `NO_EVIDENCE` | **19** |
| 6 | `UNDETERMINED` | **35** |
| 7 | `NO_EFFECTIVE_EVIDENCE` | **54**（= 19 + 35，不是 54 个零分） |
| 8 | ABL / HOT / Gap | **3.5625 / 0.375 / 1.125**（Raw = Adjusted） |
| 9 | Ablation effective weight | **16 → 12 → 6 → 6**（M0 → M1 → M2 → M3） |
| 10 | Ablation effective coverage | **0.228571 → 0.171429 → 0.085714 → 0.085714**（分母 N=70） |
| 11 | Robustness grid | **693 = 21 × 11 × 3**；660 defined；33 undefined |
| 12 | effective weight range | **0.4 – 16.0**（中位数 5.8） |
| 13 | effective coverage range | **0.005714 – 0.228571**（中位数 0.082857） |
| 14 | parameter perturbation | **±10% / ±20% → 0 decision-state flips**；ranking `NOT_APPLICABLE` |
| 15 | 反例 P108 | Raw = **L6**，R = **0.375**，Adjusted = **2.25**，`LOW_SUPPORT`/`ABSTAIN` |
| 15b | 反例 P105 | Raw = **L2**，R = **0.375**，Adjusted = **0.75**，`LOW_SUPPORT` |
| 15c | 反例 P072 / P035 | `NO_EFFECTIVE_EVIDENCE`（adjusted = null，不填 0） |
| 16 | ML Challenger | LogReg acc ≈ **0.876** / Tree ≈ **0.919** / RF ≈ **0.922**；缺失后 0.71–0.81；RF 跨学期 **0.588** |
| 17 | External Transfer | BTC **n = 1698**；threshold 0.65；Gate1 SUPPORTED、Gate2 SUPPORTED、Gate3 **NOT SUPPORTED**；risk-coverage improvement = **false** |
| 18 | Human Gate | R1 = **0/70**；R2 = **0/70**；Formal Gate = **`NOT_RUN`** |

**关键常量**：
- 16 条可判读记录共享同一组因子取值（`prompt=true`、`context=false`、`confidence=medium`、`actor=ai`），因此每条 `R = 0.75 × (1 − 0.5 × 1) × (1 − 0.5 × 0) = 0.375`。
- 这一「公共缩放退化（degenerate common-scaling slice）」是 ABL/HOT/Gap 恒为 3.5625 / 0.375 / 1.125 的根本原因，也是「分数稳定而支持下降」的机制来源。

---

## 冻结边界（FREEZE BOUNDARY）

以下操作在 `PAPER = FROZEN` 后**不得发生**（除非 MAIN_RESEARCH 明确要求并走正式变更流程）：
- 不新增模型；不重新调参；不重跑无关实验；
- 不修改 Human Gate；不扩展论文研究方向；
- 不重新设计 Demo；不擅自加强 Claim；
- 不修改 `data/`、`outputs/final_results.json`、`reports/visual_evidence/final/` 6 张图。

---

_本文件由 FINAL_CONSISTENCY_AUDIT 生成，仅锁定既有口径，不新增任何研究结论。_
