# PAPER FREEZE RECEIPT

> 状态：`PAPER = FROZEN`。本回执是论文正式冻结的凭证，记录最终口径与不可变指纹。

---

## 一、冻结对象

| 字段 | 值 |
|---|---|
| **canonical markdown path** | `paper/paper_v2_submission_candidate.md` |
| **markdown SHA256** | `8b478b7e5a1f7cfa7a1176ac97349c26518c4782f29cfcb78ac5f13e3bd47a15` |
| **final PDF path** | `paper/paper_submission_final.pdf` |
| **PDF SHA256** | `9910bb0f87aceedd17b9ad8ea9679b95dc82df188a97c0f18d39ff647167c391` |
| **PDF 页数** | 21 页 |
| **PDF 大小** | 1,809,725 bytes |
| **Git HEAD** | `837a192045647378c886218fd4a668a80e14e154` |
| **freeze timestamp** | 2026-09-27 01:07:52 GMT+8 |

> 注：本审计开始时任务书标注 HEAD = `71f0276`，实际 HEAD 为 `837a192`（`71f0276` 之后存在一次「paper: final export」提交，仅新增导出脚本与 `paper/final/` 下的 PDF/DOCX 产物，**未修改** canonical paper）。canonical markdown SHA256 与任务书给定值完全一致，确认论文正文在两次提交间零漂移。

---

## 二、审计结果

```
FINAL_CONSISTENCY_AUDIT = PASS
PAPER                   = FROZEN

P0                      = 0
P1                      = 0
P2                      = 4（文风/美观，不修）

NUMBER_DRIFT            = 0
CLAIM_DRIFT             = 0
DEMO_PAPER_CONSISTENCY  = PASS
PDF_VALIDATION          = PASS
```

### P2 清单（不阻塞冻结，仅记录）

- P2-1：Figure 出现顺序与编号不完全一致（F5 在 §6.2 先于 F3/F4 的 §6.3）。
- P2-2：Appendix 图清单路径格式不一致（F1 写全路径，F2–F6 只写文件名）。
- P2-3：§9.1 公式中 `w_i⁰` 使用 Unicode 上标。
- P2-4：Gate2 coverage 小数位差异（`0.394→0.001` vs `0.3940→0.0012`，同一数字不同舍入）。

---

## 三、一致性核对摘要

| 检查项 | 结论 |
|---|---|
| 18 组锁定数字 ↔ 真实 artifact（`outputs/final_results.json` / `independent_bounds_summary.json` / `ml_results.json` / `information_missing_validation.json`） | 全部一致，NUMBER_DRIFT = 0 |
| 状态字段（`AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `NOT_RUN` / `formal_gate_eligible=false` / `NOT_SUPPORTED`） | 全部一致 |
| 6 张图（F1–F6）路径 / Caption / 文件存在 | 全部一致，FIGURE_REFERENCE = PASS |
| 11 张表编号连续，数字与正文一致 | 全部一致 |
| External Transfer 仅声称 structural transfer | 一致（`DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`，Gate3 NOT SUPPORTED） |
| ML Challenger 无 strong ML claim | 一致（`INSUFFICIENT_FOR_STRONG_ML_CLAIM`） |
| Reliability 未描述成正式校准完成 | 一致（`WEAKLY_JUSTIFIED_COMPONENT`，非校准概率） |
| Human Gate 未暗示为完成 | 一致（R1=0/70，R2=0/70，NOT_RUN） |
| AI Increment 明确 NOT_SUPPORTED | 一致 |
| development slice 未升级为总体结论 | 一致（不把 70 外推为 140） |
| Paper ↔ Demo staging 对表 | DEMO_PAPER_CONSISTENCY = PASS（70/16/54、3.5625、16→6、P108、ML、BTC、Human Gate 全部吻合，Demo 无更强 Claim） |

---

## 四、Human Gate 真实状态

| 字段 | 值 |
|---|---|
| Human R1 | **0/70 VALID** |
| Human R2 | **0/70** |
| Formal Gate | **`NOT_RUN`** |
| `formal_gate_eligible` | **`false`** |
| 标注设计 | `single_annotator_test_retest`（非 inter-rater） |
| 正式一致性系数 | 尚未产生（无 Kappa / Alpha） |

---

## 五、可声称结论（CAN CLAIM）

1. **Score Stability ≠ Evidence Support Stability**（分数稳定，不等于证据支持稳定）——`descriptive / structural`，`DEVELOPMENT_ONLY`，Evidence Level 1。
2. 当前 70 条开发记录中，16 条可判读（L2×5、L3×5、L4×1、L5×2、L6×3），54 条返回 `NO_EFFECTIVE_EVIDENCE`（= 19 `NO_EVIDENCE` + 35 `UNDETERMINED`，**不是 54 个零分**）。
3. ABL / HOT / Gap = **3.5625 / 0.375 / 1.125**（Raw 与 Adjusted 相同，因「公共缩放退化」，**不是提升**）。
4. Ablation 有效权重 **16 → 12 → 6 → 6**，有效覆盖率 **0.228571 → 0.171429 → 0.085714 → 0.085714**（分母 N=70）。
5. 693 格声明网格内归一化分数恒定，而有效支持跨 0.4–16.0（中位数 5.8）、覆盖率跨 0.005714–0.228571。
6. P108（Raw=L6，R=0.375，Adjusted=2.25，`LOW_SUPPORT`/`ABSTAIN`）：**High Raw ≠ High Evidence Support**；P072/P035：**Missing Evidence ≠ Score 0**。
7. 外部结构迁移（BTC n=1698）：Gate1/Gate2 `SUPPORTED`，Gate3 `NOT SUPPORTED`（负结果保留，`risk-coverage improvement = false`）。
8. ML Challenger：`INSUFFICIENT_FOR_STRONG_ML_CLAIM`；替代公式：`NO_SINGLE_DOMINANT_MODEL`。

---

## 六、不可声称结论（CANNOT CLAIM）

1. **AI 增量 / 学习增益 / 因果效果**：`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`（无合法配对 `Outcome_AI`/`Outcome_baseline`）。
2. **准确率提升 / abstain 提高精度**：`accuracy_coverage_audit = NOT_RUN`，无 true outcome。
3. **R 是校准概率**：`c_i`/`λ` 是假设参数，未外部校准（`WEAKLY_JUSTIFIED_COMPONENT`）。
4. **主模型最优 / 胜出**：`NO_SINGLE_DOMINANT_MODEL`。
5. **Kappa / Alpha 正式一致性**：Human Gate 未运行，test-retest（非 inter-rater）尚无结果。
6. **交易优势 / 教育泛化 / universal generalization**：finance 仅 structural transfer。
7. **70 外推为 140 / 总体代表**：development slice 不得升级为正式总体结论。

---

## 七、冻结边界声明

- 论文已晋升为 `FROZEN`。在 Formal Human Gate 完成前，本文不标 `FORMAL_FINAL`。
- 后续所有 Human Gate 依赖结论保持 `PENDING / NOT_RUN`，所有 AI increment 结论保持 `NOT_SUPPORTED`。
- 冻结后不得新增模型、重新调参、重跑无关实验、修改 Human Gate、扩展研究方向、重新设计 Demo 或擅自加强 Claim（除非 MAIN_RESEARCH 明确要求并走正式变更流程）。

---

_本回执由 FINAL_CONSISTENCY_AUDIT 生成。PAPER = FROZEN。_
