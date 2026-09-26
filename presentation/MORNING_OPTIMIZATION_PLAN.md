# MORNING OPTIMIZATION PLAN

> 明早 2–4 小时高价值优化计划。生成日期：2026-09-27。
> 原则：**不改**模型、实验、调参、Human Gate、数据、论文正文、正式 Demo、六图、final_results。
> 只做：表达收敛、路演节奏、Demo 路径、Q&A 排练。

---

## PHASE 1 · 30 分钟 —— 确认最终文件可打开、版本、提交规则

1. 打开并确认：
   - `paper/paper_submission_final.pdf`（PDF 可打开、6 图完整、无截断、无 placeholder）
   - `outputs/education_ai_evidence_roadshow_final.pptx`（10 页、页脚编号正确）
   - `reports/demo/index.html`（浏览器可打开，F1–F6 显示正常，P108 按钮可用）
   - 桌面目录 `数学建模比赛_最终提交_2026-09-27\` 六项齐全
2. 确认版本：
   - `git rev-parse HEAD` = `16be8b7aacce4bb2d1bb759c89248d4e329a851e`
   - `git ls-remote origin refs/heads/master` 同值
   - 工作区仅余未跟踪 `reports/demo_competition_staging/`
3. 确认提交规则：非负责人明确授权，`COMMIT = NO`、`PUSH = NO`。

## PHASE 2 · 60–90 分钟 —— PPT / 路演收敛

1. 按 `presentation/PPT_STORYLINE_FINAL.md` 的 10 页顺序过一遍。
2. 逐页做「口播锚点化」：每页只留一个必须让评委记住的判断，删掉整句堆叠的重复解释。
3. 重点强化三处（不改数字、不改研究内容，只改措辞节奏）：
   - 第 1 页开场：先抛「观察到的结果 ≠ 可靠证据」。
   - 第 4 页：把「54 不是 54 个零分」讲透。
   - 第 8 页：把「BTC 是刻意选的 noisy-signal stress test，Gate3 失败是诚实边界」讲透。
4. 检查是否把 DEVELOPMENT_ONLY 讲成正式验证，如有则改回。

## PHASE 3 · 45–60 分钟 —— Demo 路径 + Q&A

1. 按 `presentation/DEMO_RUNBOOK_FINAL.md` 走一遍 60–90 秒路线。
2. 固定四个口播锚点：研究问题 → 模型链路 → 70/16/54 → P108 失败案例。
3. 过一遍 `presentation/JUDGE_RED_TEAM_FINAL.md` 的 10 个追问，逐题用自己的话复述一遍，不要照读。
4. 特别背牢三个「不能答错」：
   - 54 不是 54 个零分，是 `NO_EFFECTIVE_EVIDENCE`（Adjusted=null）。
   - Reliability 不是概率，是未校准的声明性支持权重。
   - 没有证明 AI 提高学习（AI Increment = NOT_SUPPORTED，Human Gate = NOT_RUN）。

## PHASE 4 · 30 分钟 —— 完整计时彩排

1. 用秒表完整走一遍：8 分钟主讲 + 90 秒 Demo + 预备 2 分钟 Q&A。
2. 记录超时点与卡顿点，微调口播（不改文件）。
3. 确认离线 fallback：若现场不稳定，直接用静态 Demo 或六张冻结图 F1→F3→F4→F5→F6。

---

## 不安排（红线）

- 新模型 / 新实验 / 重新调参
- Human Gate 伪完成
- 大量 UI 重构
- 修改任何冻结文件

---

## 完成后验收

- `READY_FOR_MORNING_OPTIMIZATION = YES`
- 正式交付文件零改动
- 路演节奏可复述、Q&A 可脱稿、Demo 路径顺畅
