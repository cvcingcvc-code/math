# PAPER FINAL REVIEW

> 状态：`PAPER_FINAL_REVIEW = PASS`。本文件是对唯一 canonical 论文候选的最终评委视角审查报告。
> 审查对象：`paper/paper_v2_submission_candidate.md`（580 行，HEAD `71f0276`）。
> 审查日期：2026-09-27。
> 审查依据：磁盘 artifact、Git 真实状态、PAPER_NUMBER_LOCK、PAPER_EVIDENCE_TRACE、LITERATURE_CITATION_MAP。

---

## 一、审查结论摘要

| # | 检查项 | 结论 |
|---|---|---|
| 1 | Research Question 前后一致 | PASS |
| 2 | Main Conclusion 统一 | PASS |
| 3 | 数字一致性（NUMBER_DRIFT） | PASS（0 漂移） |
| 4 | Claim Boundary | PASS（零越界） |
| 5 | 五类验证服务主命题 | PASS |
| 6 | GAP-1 / GAP-2 / GAP-3 保留 | PASS |
| 7 | F1–F6 占位/位置/Caption/图源 | PASS |
| 8 | References 真实性与对应 | PASS |
| 9 | Table 编号连续性（1–11） | PASS |
| 10 | forbidden wording 扫描 | PASS（均处于否定/禁止语境） |
| 11 | TODO / FIXME / placeholder 扫描 | PASS（零命中） |
| 12 | a4429af / archive 引用扫描 | PASS（零命中） |

---

## 二、P0 问题（必须立即修）

**无。**

---

## 三、P1 问题（提交前最好修）

**无。**

P1-1（Abstract 承诺超出正文）已在 `paper_v2_submission_candidate.md` 中修复：Abstract 末句已改为「并明确 Human Gate 完成前的证据边界（详见 Limitations）」，与正文 Limitations 章节对齐。

---

## 四、P2 问题（文风/美观，本轮不处理）

### P2-1：Figure 出现顺序与编号不完全一致

- Figure 5（Ablation/Refusal）出现在 §6.2，先于 Figure 3（§6.3）和 Figure 4（§6.3）。
- 图编号与文件名 F1–F6 对齐，不影响正确性。
- 判定：P2，不修。

### P2-2：Appendix 图清单路径格式不一致

- F1 写完整路径 `reports/visual_evidence/final/F1_model_flow.svg`，F2–F6 只写文件名。
- 判定：P2，不修。

### P2-3：§9.1 公式中 Unicode 上标

- `w_i⁰` 使用 Unicode 上标字符，PDF 排版时建议改为 LaTeX 风格。
- 判定：P2，不修。

### P2-4：Gate2 coverage 小数位差异

- PAPER_NUMBER_LOCK 写 `0.394→0.001`，论文 Table 8 写 `0.3940→0.0012`。
- 二者为同一数字（0.001178）的不同舍入，无实质性冲突。
- 判定：P2，不修。

---

## 五、数字一致性核对记录

18 组锁定数字逐一对照 `PAPER_NUMBER_LOCK.md` 与磁盘 artifact，正文无抄错：

| # | 数字 | 论文 | artifact | 一致 |
|---|---|---:|---|---:|
| 1 | N=140 | 140 | `data/processed/pilot_sample.csv` | ✓ |
| 2 | 7028 turns | 7028 | `data/processed/clean_interactions.csv` | ✓ |
| 3 | N=70 | 70 | `outputs/final_results.json::data_identity.sample_count` | ✓ |
| 4 | 16 readable | 16 | `independent_bounds_summary.json::raw_recount` | ✓ |
| 5 | 19 NO_EVIDENCE | 19 | 同上 | ✓ |
| 6 | 35 UNDETERMINED | 35 | 同上 | ✓ |
| 7 | 54 NO_EFFECTIVE_EVIDENCE | 54 | `outputs/final_results.json` | ✓ |
| 8 | ABL=3.5625 | 3.5625 | `outputs/final_results.json::raw_summary` | ✓ |
| 9 | HOT=0.375 | 0.375 | 同上 | ✓ |
| 10 | Gap=1.125 | 1.125 | 同上 | ✓ |
| 11 | M0→M3 weight 16→12→6→6 | 16→12→6→6 | `outputs/final_results.json::ablation[]` | ✓ |
| 12 | coverage 0.228571→0.085714 | 0.228571→0.085714 | 同上 | ✓ |
| 13 | 693 grid (21×11×3) | 693 | `independent_bounds_summary.json::parameter_space` | ✓ |
| 14 | 660 defined / 33 undefined | 660/33 | 同上 | ✓ |
| 15 | effective weight 0.4–16.0 | 0.4–16.0 | 同上 | ✓ |
| 16 | effective coverage 0.005714–0.228571 | 0.005714–0.228571 | 同上 | ✓ |
| 17 | ±10%/±20% → 0 flips | 0 flips | `outputs/final_results.json::sensitivity.rows` | ✓ |
| 18 | P108 Raw=L6, R=0.375, adj=2.25 | L6/0.375/2.25 | `outputs/final_results.json::counterexamples` | ✓ |

**NUMBER_DRIFT = 0**

---

## 六、Claim Boundary 核对记录

forbidden 措辞扫描（FORMAL_SUPPORTED / causal learning gain / AI 提高学习效果 / AI 导致学习效果提升 / ML winner / ML 被击败 / accuracy 提升 / 准确率提升）——命中项均处于否定或禁止语境（如「不声称任何模型最优」「challenge completed, winner unselected」「不得声称 AI 导致学习效果提升」）。

**CLAIM_BOUNDARY_VIOLATION = 0**

---

## 七、图源核对记录

6 张 SVG 全部存在于 `reports/visual_evidence/final/`，标题与内容匹配：

| 图 | 文件 | 位置 | Caption | 一致 |
|---|---|---|---|---:|
| F1 | F1_model_flow.svg | §3 开头 | 整体框架六层链路 | ✓ |
| F2 | F2_raw_vs_adjusted.svg | §3.1 | Raw vs Adjusted 逐记录分离 | ✓ |
| F3 | F3_evidence_degradation.svg | §6.3 | Evidence degradation 响应 | ✓ |
| F4 | F4_parameter_perturbation.svg | §6.3 | Score 稳定 vs Support 变化 | ✓ |
| F5 | F5_ablation_refusal.svg | §6.2 | Ablation 拒判语义 | ✓ |
| F6 | F6_external_structural_transfer.svg | §6.5 | External structural transfer | ✓ |

**FIGURE_REFERENCE = PASS**

---

## 八、文献核对记录

- References 共 22 篇，全部来自 `LITERATURE_CITATION_MAP.md` 中登记的真实文献。
- 不存在虚构 DOI；不存在虚构 citation。
- 正文 claim 与引用匹配。
- citation placeholder 已清空。
- 不存在 TODO citation。
- 不存在"看起来像引用但无法追溯"的内容。

**LITERATURE_CHECK = PASS**

---

## 九、五类验证服务主命题核对

| VQ | 攻击的质疑 | 论文章节 | 服务主命题 |
|---|---|---|---|
| VQ1 Baseline | "Reliability 层其实没必要" | §6.1 | ✓ 四模型同分但支持记账不同 |
| VQ2 Ablation | "公式里的组件只是装饰" | §6.2 | ✓ 组件确实改变 support accounting |
| VQ3 Sensitivity | "结果只是某个参数点碰巧调出来的" | §6.3 | ✓ 693 格内分数恒定而支持变化 |
| VQ4 Failure | "遇到最困难的记录时模型就没用了" | §6.4 | ✓ P108 High Raw ≠ High Support |
| VQ5 External | "模型只是为当前教育数据硬写的" | §6.5 | ✓ 结构可迁移但 Gate3 NOT SUPPORTED |

**主线核对：PASS**

- Observed Evidence → Raw Signal → Reliability → Adjusted Evaluation → Support / Coverage → Decision ✓
- ML = Challenger（不是 Main Model）✓
- Finance = External Structural Demonstration（不是盈利能力证明）✓

---

## 十、Human Gate 真实状态

- Human R1 = **0/70 VALID**（`data/annotations/human/pilot_worksheet_A.csv`，1/70 行带标签）
- Human R2 = **0/70**（`pilot_worksheet_A_retest.csv` 空白）
- Formal Gate = **`NOT_RUN`**
- `formal_gate_eligible = false`
- `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`

论文状态声明与磁盘真实状态一致。

---

**PAPER_FINAL_REVIEW = PASS**

_PAPER_V2_CANONICAL_DEVELOPMENT · Formal Human Gate 仍未完成 · 不标 FORMAL_FINAL_
