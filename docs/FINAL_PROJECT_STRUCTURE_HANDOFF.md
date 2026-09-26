# FINAL PROJECT STRUCTURE HANDOFF

> 给一个完全没参与过本项目的新助手：5 分钟看懂这个项目是什么、做了什么、哪些能碰、哪些不能碰。
> 生成日期：2026-09-27。状态：`FINAL_COMPETITION_CONVERGENCE = PASS`。
> 本文件是只读地图，不含新研究结论。

---

## 1. 研究问题是什么

**Main Research Question（全文唯一）**：

> 当观测证据存在缺失、冲突或可信度差异时，如何避免把 Raw Signal 直接当作可靠结论，并构建一个能够显式报告 Evidence Reliability 与 Support / Coverage，且在证据不足时允许 `ABSTAIN` 的可审查评价框架？

**问题类型**：`measurement / identifiability`（测量与可识别性）问题。

**它明确不是**：AI 是否提高成绩；学生真实能力预测；AI causal learning gain；AI 与 baseline 的正式效果识别。

---

## 2. 主模型是什么

```
Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support / Coverage → Decision
```

- `w_i = I(observable_i) · c_i · (1 − λ_prompt·p_i) · (1 − λ_context·t_i)`
- `Adjusted_i = Raw_i × w_i`（仅在 `I(observable_i)=1` 时有定义）
- `S = Σw_i`；`C_eff = Σw_i / N`（分母 `N = 70`）
- 决策状态：`ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE`

**核心语义**：
- `High Raw ≠ High Evidence Support`（高原始信号 ≠ 高证据支持）
- `Missing Evidence ≠ Zero Performance`（缺失证据 ≠ 零表现）
- 证据不足 → `ABSTAIN`（合理输出，不是模型失败）
- 无有效证据 → `NO_EFFECTIVE_EVIDENCE`（**不是 0 分**）

**唯一 Main Conclusion**：

> **Score Stability ≠ Evidence Support Stability.**
> 分数稳定，不等于证据支持稳定。

---

## 3. 数据结构

| 层级 | 事实 | 路径 |
|---|---|---|
| Pilot V1 全量 | N = 140（秋 70 + 春 70） | `data/processed/pilot_sample.csv` |
| 上游清洗主结果 | 7028 turns（student 3522 / AI 3506） | `data/processed/clean_interactions.csv` |
| 当前 development slice | N = 70（AI_PROVISIONAL，DEVELOPMENT_ONLY） | `data/annotations/ai/pilot_ai_provisional.csv` |

Development N = 70 的构成：
- 可判读 Student Evidence = **16**（L2×5、L3×5、L4×1、L5×2、L6×3）
- `NO_EVIDENCE` = **19**
- `UNDETERMINED` = **35**
- `NO_EFFECTIVE_EVIDENCE` = **54**（= 19 + 35，不是 54 个零分）

**关键限制**：16 条可判读记录共享同一组因子（prompt=true、context=false、confidence=medium、actor=ai），每条 `R = 0.75 × (1−0.5×1) × (1−0.5×0) = 0.375`。这是「公共缩放退化（degenerate common-scaling slice）」——它是「分数稳定、支持下降」的机制来源，也是当前切片只支持结构性结论的根本原因。

---

## 4. 五类验证（VQ1–VQ5，围绕同一个 RQ）

| VQ | 名称 | 一句话问题 |
|---|---|---|
| VQ1 | Baseline | 如果完全不建模 Reliability，会发生什么？ |
| VQ2 | Ablation | 公式里的组件只是装饰吗？ |
| VQ3 | Sensitivity / Robustness | 结论只是某个参数点碰巧调出来的？ |
| VQ4 | Failure / Counterexample | 高 Raw 是否仍被无条件接受？缺失证据是否被填 0？ |
| VQ5 | External Structural Transfer | 模型是否只为当前教育数据硬写？ |

每条路径统一报告 `WHY → SETUP → RESULT → SUPPORTED → NOT SUPPORTED`。

---

## 5. ML Challenger

ML 不是 Main Model，而是独立挑战者，检查「更灵活的数据驱动模型是否暴露主框架没捕捉到的结构」。
- Logistic Regression ≈ 0.876 / Decision Tree ≈ 0.919 / Random Forest ≈ 0.922（重复 4-fold × 25 次 = 100 folds）
- 结论：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`（16 positives、代理标签、无 holdout、缺失降级 0.71–0.81、RF 跨学期 0.588）

---

## 6. Alternative Formulations

比较四种函数形式（乘法 A / 加法 B / 门控 C / 非线性 D），结论保持 `NO_SINGLE_DOMINANT_MODEL`。主模型被保留的理由是「研究问题对齐 + 透明 + 显式缺失语义 + 拒判结构」，**不是**「已证明最优」。

---

## 7. External Structural Transfer

把 `Raw → Reliability → Adjusted → Coverage → Decision` 结构复用到 BTC-USD 历史纸面模拟（n = 1698，公开行情，synthetic / controlled evidence），做三个 information-missing Gate：

| Gate | 判据 | 结果 |
|---|---|---|
| Gate1 | 信息质量/完整度下降 → Reliability 下降 | **SUPPORTED** |
| Gate2 | 低 Reliability → abstention 上升、coverage 下降 | **SUPPORTED** |
| Gate3 | 低 Reliability 决策有更高 future error rate | **NOT SUPPORTED** |

**定位**：`STRUCTURAL TRANSFER ONLY`。不是交易策略、不是盈利预测、不是投资建议、不是金融泛化。Gate3 失败必须保留——它证明当前 Reliability 尚未被证明是未来正确性的 calibrated predictor。

---

## 8. Human Gate 为什么还没完成

- Human R1 = **0/70 VALID**，R2 = **0/70**，Formal Gate = **`NOT_RUN`**
- 近期收到的一份标注文件已核验为同一 B 标签的派生副本（`filled_from_B`），不是独立 R1/R2
- 冻结设计是 `single_annotator_test_retest`（非 inter-rater），正式一致性系数尚未产生
- 因此全项目状态为 `AI_PROVISIONAL / DEVELOPMENT_ONLY / NOT_HUMAN_VALIDATED`，**不标 FORMAL_FINAL**

---

## 9. Paper / Demo / PPT 在哪里

| 交付物 | 正式路径 | 状态 |
|---|---|---|
| 唯一 canonical paper | `paper/paper_v2_submission_candidate.md` | FROZEN |
| 最终 PDF | `paper/paper_submission_final.pdf` | FROZEN |
| 可编辑 DOCX | `paper/final/数学建模论文_可编辑版_2026-09-27.docx` | FROZEN |
| 最终 PPT | `outputs/education_ai_evidence_roadshow_final.pptx`（10 页） | FROZEN |
| 正式 Demo | `reports/demo/index.html`（SHA256 `d15d124c…`） | FROZEN |
| 六张证据图 | `reports/visual_evidence/final/F1–F6.svg` | FROZEN |

---

## 10. 哪些文件是 canonical（唯一事实源）

- 唯一数字源：`paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字）+ `outputs/final_results.json`
- 口径锁定：`paper/FINAL_CLAIM_LOCK.md`
- 声明→证据映射：`paper/PAPER_EVIDENCE_TRACE.md`（C1–C13）
- 文献映射：`paper/LITERATURE_CITATION_MAP.md`
- 冻结词汇与非等价关系：`docs/metric_dictionary.md`

---

## 11. 哪些文件严禁再改

- `paper/paper_v2_submission_candidate.md`（canonical paper）
- 最终 PDF / DOCX
- 最终 PPT
- `reports/demo/index.html`（正式 Demo）
- `reports/visual_evidence/final/F1–F6.svg`（六图）
- `outputs/final_results.json`（统一事实源）
- `data/`（原始数据与标注）
- 模型代码（`src/`）
- Human labels / Gate 状态

---

## 12. 当前 Git 状态

- 仓库：`https://github.com/cvcingcvc-code/math.git`
- 分支：`master`
- HEAD：`16be8b7aacce4bb2d1bb759c89248d4e329a851e`
- origin/master：`16be8b7aacce4bb2d1bb759c89248d4e329a851e`（一致）
- 工作区：仅余未跟踪 `reports/demo_competition_staging/`（与正式 Demo 逐字一致的本地候选副本，未纳入 Git）

---

## 13. 当前最终 commit

`16be8b7aacce4bb2d1bb759c89248d4e329a851e` — "submission: competition-grade final convergence"

---

## 14. 明天继续优化应该从哪里开始

1. 先打开 `WAKE_UP_FIRST_READ.md`（1 页速览）
2. 再读 `presentation/MORNING_OPTIMIZATION_PLAN.md`（PHASE 1–4 计划）
3. 最可能的高价值动作：PPT 路演收敛（不重做 PPT）、Demo 演示路径 + Q&A 排练
4. **不要**：新模型、新实验、重新调参、Human Gate 伪完成、大量 UI 重构

---

## 附：核心数字速查（全部锁定）

`70 / 16 / 54`（19 NO_EVIDENCE + 35 UNDETERMINED）
`3.5625 / 0.375 / 1.125`（ABL / HOT / aggregate Gap；1.125 是 aggregate Gap，2.25 是 P108 单记录 Adjusted contribution，勿混）
Ablation `16 → 12 → 6 → 6`；Coverage `0.228571 → 0.171429 → 0.085714 → 0.085714`
Grid `693 = 21×11×3`（660 defined / 33 undefined）
Counterexamples `P108 / P105 / P072 / P035`
ML `0.876 / 0.919 / 0.922` → `INSUFFICIENT_FOR_STRONG_ML_CLAIM`
BTC `n=1698`，Gate1/2 SUPPORTED，Gate3 NOT SUPPORTED
Human `R1=0/70 / R2=0/70 / NOT_RUN`；AI Increment `NOT_SUPPORTED`
