# WAKE_UP_FIRST_READ

> 醒来后先看这一页，再决定做什么。生成日期：2026-09-27（问题原生最终收敛后）。

## 项目状态

**PASS，未 BLOCKED。** `READY_FOR_SUBMISSION = YES`，`READY_FOR_REHEARSAL = YES`，`TOMORROW_CODE_CHANGE_REQUIRED = NO`。

## 最终文件位置

| 交付物 | 路径 |
|---|---|
| 论文 PDF | `paper/paper_submission_final.pdf` |
| 可编辑 DOCX | `paper/final/数学建模论文_可编辑版_2026-09-27.docx` |
| 路演 PPT（10 页） | `outputs/education_ai_evidence_roadshow_final.pptx` |
| 正式 Demo | `reports/demo/index.html` |
| 六图 | `reports/visual_evidence/final/F1–F6.svg` |
| 桌面交付 | `C:\Users\lin\Desktop\数学建模比赛_最终提交_2026-09-27\` |

## Git

- 分支：`master`，本地与 `origin/master` 已同步。
- 最终 commit 以 `git rev-parse HEAD` 为准（本次问题原生收敛 commit 之后）。

## 明天需不需要改代码

**不需要。** 除真正的 P0（数字/结论错误）外，不再新增模型、实验、案例、数据、算法、网页模块或研究问题。

## 路演第一句话

> 我们不是重新给学生打分，而是在回答：这个分数，到底有多少证据值得相信？

（30 秒核心发现：分数仍是 3.5625，但有效支持从 16 降到 6、覆盖率从 22.86% 降到 8.57%——所以分数稳定 ≠ 证据支撑稳定。）

## 三个最危险问题

1. **Reliability 是不是拍脑袋？** → 不是，是透明声明假设 + 693 格敏感性检验兜底，只声称结构性行为。
2. **16 条是不是太少？** → 是限制，但恰恰暴露了 evidence availability 问题；54 条不是零分，是 NO_EFFECTIVE_EVIDENCE。
3. **Score 没变模型有什么用？** → 分数没变正说明只看 Score 会看不到支持已大幅下降。

## 红线（一秒钟记住）

- 禁止改 canonical paper / PDF / DOCX / PPT / 正式 Demo / F1–F6 / final_results / model code / data / Human labels / Gate。
- 禁止 `git add -A`；未经授权不 commit / push。
- 禁止把 DEVELOPMENT_ONLY 包装成 FORMAL_FINAL；禁止声称 AI 提升学习 / 因果增量 / 预测准确率 / 交易优势 / 通用泛化。
