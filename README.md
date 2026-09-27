# 教育AI证据可靠性评估模型

中国第一届数学建模黑客松 · 赛道一：《新时代教育中 AI 增量价值评价的建模方法》

**队名**：起名困难队　·　**汇报人**：张镇源

> **状态**：Development submission。所有结果为 `AI_PROVISIONAL / DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。Human R1/R2 尚未产生，Formal Gate `NOT_RUN`。

---

## 核心问题

> 当观测结果存在缺失、冲突或可信度差异时，如何避免直接把 Raw Signal 当成可靠结论？

## 核心框架

`Raw → Reliability → Adjusted → Support / Coverage → Decision`

## 核心结论

> **Score Stability ≠ Evidence Support Stability**
>
> 分数稳定，不等于证据支持稳定。

## 项目简介

本项目针对教育AI评价中证据缺失、冲突和可信度差异问题，构建“Raw–Reliability–Adjusted–Support/Decision”评估框架，将原始表现与证据可靠性分离，并在证据不足时主动拒判。通过敏感性、消融、失败案例和机器学习对照等验证发现：分数稳定不等于证据支持稳定，从而提升评价结果的可解释性与可信度。

## 当前研究边界

| 边界项 | 状态 |
|---|---|
| 数据与标注 | `DEVELOPMENT_ONLY`（仅开发阶段开发切片） |
| 人工验证 | `NOT_HUMAN_VALIDATED`（尚未人工验证，Human R1 = 0/70、R2 = 0/70） |
| AI 增量识别 | `AI_INCREMENT = NOT_SUPPORTED` |

**本项目不主张**：已证明 AI 提升学习效果、已证明因果增益、已找到 ML winner、已证明交易盈利能力。

---

## 🌐 Live Demo

在线演示（GitHub Pages）：**https://cvcingcvc-code.github.io/math/**

## 入口 Entries

- 🌐 **Live Demo**：https://cvcingcvc-code.github.io/math/（正式比赛 Demo）
- 📄 **Paper**：`paper/development_submission_candidate.md`（canonical development paper）
- 📊 **PPT**：`presentation/final_defense_ppt/教育AI证据可靠性_现场答辩终稿.pptx`（10 页现场答辩终稿；`outputs/education_ai_evidence_roadshow_final.pptx` 为同一份文件）
- 🔁 **Reproducibility**：`python run_all.py`（开发版复现，32/32 检查），详见 `docs/RUN_GUIDE.md`
- 💻 **Source Code**：`src/`、`scripts/`、`run_all.py`

---

## Research Question

当观测到的学习表现存在**缺失、冲突或可信度差异**时，如何显式建模**证据可靠性（Evidence Reliability）**，并在证据不足时拒绝给出过度确定的结论（`ABSTAIN` / `NO_EFFECTIVE_EVIDENCE`），而不是把 Raw Signal 直接当成可信结论？

## Main Conclusion

**Score Stability ≠ Evidence Support Stability.**

归一化分数（ABL/HOT/Gap = 3.5625 / 0.375 / 1.125）在加入可靠性权重前后保持不变，但有效证据权重从 16 降到 6、有效覆盖率从 0.228571 降到 0.085714（分母为全部 70 条开发记录）。**分数看起来稳定，并不能保证支撑它的证据充分、可靠或完整。**

## Main Model

```
Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision
```

- **Raw Signal**：Student Evidence 的 Bloom 层级（冻结手册 L2–L6），只回答"证据有多高"。
- **Reliability**：`w_i = I(observable_i) · c_i · (1 − λ_prompt·p_i) · (1 − λ_context·t_i)`，把证据质量/冲突/低可信显式纳入（不是校准概率，是声明性支持权重）。
- **Adjusted**：`Adjusted_i = Raw_i × w_i`，弱支持不被放大。
- **Support/Coverage**：`S = Σ w_i`、`C_eff = S / N`（分母 N=70，含无证据/不可判读记录）。
- **Decision**：`ACCEPT` / `ABSTAIN`（`LOW_SUPPORT`）/ `NO_EFFECTIVE_EVIDENCE`（有效证据为零时**不填 0 分**）。

## Validation Framework

五条互补路径攻击同一核心命题：

1. **Baseline Comparison** — 可靠性层是否必要（Raw-only 忽略支持质量）。
2. **Ablation Study** — 组件是否真正改变支持语义（M0→M3 有效权重 16→12→6→6）。
3. **Sensitivity / Robustness** — 结论是否非单点偶然（±10%/±20% 扰动 0 决策翻转）。
4. **Failure / Counterexample** — 高 Raw 是否仍应被接受（P108 L6 → LOW_SUPPORT）。
5. **External Transfer** — 结构能否迁移到另一证据场景（BTC 历史模拟，非泛化）。

外加两个对照：**ML Challenger**（`INSUFFICIENT_FOR_STRONG_ML_CLAIM`）与 **Alternative Formulations**（`NO_SINGLE_DOMINANT_MODEL`）。

## Repository Structure

| 目录 | 内容 |
|---|---|
| `paper/` | 论文与溯源（`development_submission_candidate.md`、`PAPER_NUMBER_LOCK.md`、`PAPER_EVIDENCE_TRACE.md`、`LITERATURE_CITATION_MAP.md`） |
| `data/` | 已处理数据与标注（`processed/` 主清洗结果、`annotations/` AI/人工标注） |
| `src/` `scripts/` `run_all.py` | 代码与入口 |
| `docs/` | 数据字典、数据结构、运行指南、指标字典、声明边界、模型呈现、研究故事 |
| `reports/` | 开发结果、验证、审计、稳健性、失败案例、可视化证据 |
| `experiments/` | 模型锦标赛与外部迁移 |
| `outputs/` | 统一事实源 `final_results.json`、PPT、提交包 |
| `handoff/` | 持久项目状态与多工具交接 |
| `validation/` | 冻结 Gate 阈值（`preregistered=true`） |

## How to Run

```bash
# 只读完整性核验（21 项冻结不变量 + 2 个已知缺陷）
python src/verify_pilot_integrity.py

# 开发版复现（6 步、32/32 检查）
python run_all.py

# 门禁入口（需真实人工 R1/R2 后）
python src/run_s4_gate.py
```

环境：需使用已装 pandas 的 Python（实测系统 Python 3.14.2 + pandas 3.0.1；`requirements.txt` 钉 pandas==3.0.6/numpy==2.5.3）。详见 `docs/RUN_GUIDE.md`。

## Paper / Demo / Evidence

- **论文**：`paper/development_submission_candidate.md`（canonical development paper）
- **Demo**：`reports/demo/index.html`（顶部标注 `DEVELOPMENT_ONLY · AI_PROVISIONAL`）
- **统一事实源**：`outputs/final_results.json`
- **核心数字源**：`paper/PAPER_NUMBER_LOCK.md`；证据映射 `paper/PAPER_EVIDENCE_TRACE.md`

## Current Evidence Status

最高证据等级 **Level 1 — descriptive / structural development evidence**。70 条开发记录中 16 条可判读（L2×5/L3×5/L4×1/L5×2/L6×3）、19 条 NO_EVIDENCE、35 条 UNDETERMINED；后两者（共 54 条）返回 `NO_EFFECTIVE_EVIDENCE`。16 条可判读记录高度同质（全部 `prompt=true / context=false / confidence=medium`），因此只能支持公共缩放层面的结构性结论。

## Limitations

- 输入为 AI provisional 标签，非人工验证。
- 无合法配对的 `Outcome_AI` / `Outcome_baseline` → `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，不识别因果增量。
- 稳健性只覆盖当前同质切片，不构成 universal robustness。
- External Transfer 是 synthetic/controlled 结构演示，非教育泛化。

## Formal Human Gate Status

- **Human R1 = 0/70**，**Human R2 = 0/70**，**Formal Gate = NOT_RUN**。
- 冻结设计为同一标注者 test-retest（R1 → ≥24h → R2），**不是** inter-rater reliability。
- 最近收到的 `filled_from_B_master_all.zip` 已核验为同一 B 标签的派生副本，**不作为** R1/R2（见 `work/intake/.../INTAKE_RECEIPT.md`）。
- 在 Formal Gate PASS 前，所有结果保持 `DEVELOPMENT_ONLY`，不报告正式一致性、正式 AIV、学生排名或因果 AI 增量。

---

**接手入口**：`handoff/PROJECT_NOW.md` → `handoff/PROJECT_STATE.md` → `handoff/NEXT_TASK.md`。仓库审计见 `handoff/PROJECT_TAKEOVER_AUDIT.md`，清理计划见 `handoff/CLEANUP_PLAN.md`。
