# PAPER FAST REVIEW

> 只读快速审查报告，对象：`paper/paper_v2_full_draft.md`（PAPER_DRAFT_0，冻结于 `d4b87c8`）。
> 分级：P0 = 必须立即修；P1 = 提交前最好修；P2 = 文风/美观，可后修。
> 本轮只处理 P0 + 明显 P1。

## 审查结论摘要

| # | 检查项 | 结论 |
|---|---|---|
| 1 | Research Question 前后一致 | PASS |
| 2 | Main Conclusion 统一 | PASS |
| 3 | 数字一致性（NUMBER_DRIFT） | PASS（0 漂移） |
| 4 | Claim Boundary | PASS（零越界） |
| 5 | 五类验证服务主命题 | PASS |
| 6 | GAP-1 / GAP-2 / GAP-3 保留 | PASS |
| 7 | References 真实性与对应 | PASS（见 P1-2 观察项） |
| 8 | F1–F6 占位/位置/Caption/图源 | PASS |

## P0 问题（必须立即修）

**无。**

## P1 问题（提交前最好修）

### P1-1 Abstract 承诺与正文不对齐（前后不一致）

- **位置**：Abstract 末句「并给出可执行的 Formal Evidence Upgrade Protocol」。
- **问题**：正文没有对应的「Formal Evidence Upgrade Protocol」独立章节（canonical 论文有 §13，但 full draft 精简后未保留）；正文仅在 Limitations GAP-1 与 Conclusion 提到 Human Gate 未完成。
- **修法**：将 Abstract 该句改为与正文一致的表述——「并明确 Human Gate 完成前的证据边界（详见 Limitations）」。
- **判定**：P1（Abstract 承诺超出正文内容，答辩时可能被追问「Protocol 在哪」）。

### P1-2 References 含正文未直接引用的背景文献（观察项，建议保留）

- **现象**：References 共 21 篇，正文直接引用的约 9 篇（Soderstrom & Bjork、Bastani、Kane、Gašević、Krathwohl、Guo、Little & Rubin、Rubin、Hernán & Robins、El-Yaniv & Wiener）。其余 12 篇（Fan、Gray & Bergner、Saisana、OECD、Putnick、Geifman、Angelopoulos、Parasuraman & Riley、Skitka、Bansal、Cohen、Krippendorff）为 canonical 文献综述（`LITERATURE_CITATION_MAP.md`）的真实背景支撑，full draft 精简 Literature Review 后未逐个在正文点引。
- **判定**：P1 观察项。**不删除**——这些是真实文献、DOI 无虚构，删除反而违背「不为了好看而删」。可选处理：在 References 开头加一行说明「以下背景文献来自冻结文献映射，支撑 Introduction 的效度/缺失/拒判/AI 来源四类论断」。
- **处理**：本轮保留 References 原文不动，仅在审查报告登记。

## P2 问题（文风/美观，本轮不处理）

- P2-1：§9.1 公式中 `w_i⁰` 用 Unicode 上标字符，PDF 排版时建议改为 LaTeX 风格 `w_i^0`。
- P2-2：§6.3 中 F3（evidence degradation）与 F4（parameter perturbation）的插入位置可与图内容进一步对齐（F3 内容偏 Failure-case 语义，可移至 §6.4 附近）。
- P2-3：Abstract 可进一步压缩关键词堆叠感（不影响正确性）。

## 数字一致性核对记录

18 组锁定数字逐一对照 `PAPER_NUMBER_LOCK.md` 与磁盘 artifact，正文无抄错：140 / 7028 / 3522 / 3506 / 70 / 16 / 19 / 35 / 54 / 3.5625 / 0.375 / 1.125 / 16→12→6→6 / 0.228571→0.171429→0.085714 / 693 / 660 / 33 / 0.4–16.0 / P108（L6/0.375/2.25）/ ML 0.876/0.919/0.922/0.588 / BTC 1698 / Gate1-2 SUPPORTED + Gate3 NOT SUPPORTED。**NUMBER_DRIFT = 0**。

## Claim Boundary 核对记录

forbidden 措辞扫描（FORMAL_SUPPORTED / causal learning gain / AI incremental effect / student ranking / ML superior / winner / 唯一最优模型）——命中项均处于否定或禁止语境（如「不声称任何模型最优」「challenge completed, winner unselected」）。`DEVELOPMENT_ONLY` / `AI_PROVISIONAL` / `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED` 状态声明贯穿全文。**零越界**。

## 图源核对记录

6 张 SVG 全部存在于 `reports/visual_evidence/final/`，标题与内容匹配：
F1 框架、F2 Raw vs Adjusted、F3 Evidence degradation、F4 Parameter perturbation、F5 Ablation/Refusal、F6 External transfer。**无 FIGURE_MISSING**。
