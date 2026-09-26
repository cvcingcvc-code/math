# CURRENT HANDOFF

## PROJECT ROOT
`C:\Users\lin\Documents\Codex\2026-09-25\yu`

## CURRENT HEAD / BRANCH / GIT STATUS
- Branch: `master`
- R1 安全检查点：`e8d4f67` (`chore: checkpoint human R1 progress`)
- 本轮随后提交编码修复与 Demo 修复；准确 HEAD 以 `git log --oneline -5` 为准。
- 工作区另有其他窗口已完成的 parallel closeout 文档改动（README / data dictionary / handoff / submission 说明），已随本轮提交固化。
- 未跟踪的用户可交付材料：`outputs/`、`paper/submission_candidate.html/.pdf`、`slides/`、`.codex-finalizer/`、部分 audit 报告。**不得删除、覆盖或强制回滚。**

## HUMAN ANNOTATION STATUS (2026-09-26)
- **HUMAN_R1 = IN_PROGRESS**：`data/annotations/human/pilot_worksheet_A.csv` 已由负责人开始填写；检查点 2026-09-26 11:17 为 1/70 行带标签（record_id P072）。负责人明天继续。
- **HUMAN_R2 = NOT_STARTED / WAITING_FOR_HUMAN**：`pilot_worksheet_A_retest.csv` 仍为 0/70 空白，不得代填、不得复制 R1。
- **FORMAL_HUMAN_GATE = NOT_RUN**：`reports/annotation_gate_report.json` 保持 PENDING；未计算任何正式一致性系数。
- R1 本地备份：`work/backups/pilot_worksheet_A_2026-09-26_1117_checkpoint.csv`（SHA-256 `8FB6D38D…8A585E`）。
- R1 保护规则：不得补全、修改、清洗、覆盖 R1；不得把 AI_PROVISIONAL 标签写入人工表；今天不得执行 R2、不得向负责人展示 R1 与 AI 标签对比。

## CURRENT RESEARCH STAGE
S4 Pilot Annotation Gate — `BLOCKED_BY_HUMAN_ANNOTATION`。除正式人工验证外的开发主线均已冻结完成。

## COMPLETED
Reliability model、Raw vs Adjusted、Sensitivity、M0–M3 Ablation、Counterexamples、core closure（`RESEARCH_CORE_FROZEN_FOR_SUBMISSION`）、独立数值复算、论文/答辩材料、10 页路演 PPT、开发版提交包。

## TODAY'S WORK (2026-09-26)
1. R1 安全检查点：备份 + Git 提交 `e8d4f67`，未改动任何标签。
2. **修复 Gate 读取编码崩溃（P0）**：负责人编辑器把 R1 保存为 GB18030，`run_s4_gate.py` 原读取直接 `UnicodeDecodeError`。新增 `src/csv_safe_read.py`，并让 `run_s4_gate.py`、`annotation_gate_report.py`、`solo_retest_gate.py` 兼容 UTF-8 与 GB18030；只读解码、不回写、不修改标签。用 GB18030 合成文件完成端到端软件测试。
3. **修复 Demo 数字口径（P3）**：Demo 原先把 effective coverage 除以 16 条可判读记录（显示 75%），与论文/报告的分母 70 不一致；已改为 `total/N`，基线正确显示 17.14%。
4. **Demo 增强**：Panel C 增加 Raw baseline（λ=0）与 Adjusted Score 标注；新增 Panel E · Counterexamples 表格；保留 `NO_EFFECTIVE_EVIDENCE` 行为。Node 运行时自检 10/10 通过，`run_all.py` 32/32 PASS。
5. **提交包同步**：`outputs/submission_package_development_only/` 更新 `demo/index.html` 并补入 4 张核心图到 `development/`；MANIFEST 35 项逐一核对一致。
6. `python src/run_s4_gate.py` 在 R1 部分填写、R2 空白时正确保持 PENDING，且 R1 文件哈希前后不变。

## DEVELOPMENT_ONLY BOUNDARY
- 开发输入：`data/annotations/ai/pilot_ai_provisional.csv`（`AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `formal_gate_eligible=false`）。
- 核心数字：70 条记录、16 条可判读 Evidence；ABL/HOT/Gap = 3.5625/0.375/1.125；effective weight 16→6；effective coverage 0.228571→0.085714（分母 70）；零支持 → `NO_EFFECTIVE_EVIDENCE`。
- Formal AIV = `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

## DEMO / PAPER / PPT / PACKAGE
- Demo：`reports/demo/index.html`（顶部 DEVELOPMENT_ONLY · AI_PROVISIONAL；Raw vs Adjusted；λ/r 敏感性；Counterexamples；NO_EFFECTIVE_EVIDENCE）。
- Paper：`paper/submission_candidate.html/.pdf`；底稿 `reports/paper/competition_paper_narrative_draft.md`。本轮未修改论文主体与结论边界。
- PPT：`outputs/education_ai_evidence_roadshow_v1_final.pptx`（10 页：Problem / Measurement Problem / Reliability Model / Raw vs Adjusted / Sensitivity / Ablation / Counterexamples / Human Gate / Demo / Submission）。
- Package：`outputs/submission_package_development_only/`；MANIFEST 35 项全部一致。

## CORE NUMBERS
Development-only：70 / 16 / 19 / 35；693 格中 660 defined、33 undefined；ABL 3.5625、HOT 0.375、Gap 1.125；coverage 分母 70。

## BLOCKERS
- **P0**：正式人工 R1/R2 未完成 → Gate PENDING → 正式一致性系数、Formal AIV、学生排名均不可产生。
- **P1**：team-ID 命名与最终封装命名/页数核对尚未完成；提交包目前只对内部评审/演示有效。

## NEXT STEP (明天第一优先：继续 HUMAN R1)
1. **负责人继续并完成 HUMAN R1 70/70**（`data/annotations/human/pilot_worksheet_A.csv`）；R1 未完成前不进入 R2。
2. R1 完成后保存并冻结，记录完成时间与文件 SHA-256（备份到 `work/backups/`）。
3. 按冻结标注协议满足 R1→R2 所需的重测间隔（至少 24 小时）。
4. 再由负责人在不查看 R1 的前提下独立完成 HUMAN R2 70/70（`data/annotations/human/pilot_worksheet_A_retest.csv`）。
5. R1、R2 都完整后运行：
   ```
   python src/run_s4_gate.py
   ```
   等价手动命令：
   ```
   python src/solo_retest_gate.py report --r1 data/annotations/human/pilot_worksheet_A.csv --r2 data/annotations/human/pilot_worksheet_A_retest.csv
   ```
6. Gate PASS 后按 `FORMAL_GATE_SWITCH.md` 运行 `python run_all.py --mode formal` 并替换正式结果。
7. 若 Gate 未通过：不修改预注册阈值、不倒推标签、不强行 formal，保持 `DEVELOPMENT_ONLY` 并如实报告验证结果。

工作表保存为 UTF-8 或 GB18030 均可，读取器已兼容（只读，不回写标签）。

## DO NOT REDO / DO NOT TOUCH
- 不重跑已冻结的开发实验（`run_all.py` 一致性验证除外）。
- 不覆盖 R1/R2；不修改 `validation/gate_thresholds.json`、`annotation_manual_v0.1.md`、`annotation_clarification_v0.1.1.md`。
- 不删除未跟踪交付物；不 `reset --hard`、不强制 checkout、不覆盖其他窗口改动。
- 不得把 AI 标签冒充人工标签；不得宣称 Formal AIV、排名或因果效应。

## FILES NEXT WINDOW MUST READ
`AGENTS.md`; `handoff/PROJECT_STATE.md`; `handoff/DECISIONS.md`; `handoff/NEXT_TASK.md`; `handoff/CURRENT_HANDOFF.md`; `FORMAL_GATE_SWITCH.md`.

## NEW WINDOW START (5–10 lines)
Read `AGENTS.md`, `handoff/CURRENT_HANDOFF.md`, and current Git HEAD/status. Restore disk state. Treat marked DONE steps as complete. Continue the first unfinished main-line task. Keep development and formal inputs separate. Do not touch human R1/R2. Do not bypass the Formal Gate.
