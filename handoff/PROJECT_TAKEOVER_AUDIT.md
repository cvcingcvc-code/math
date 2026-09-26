# PROJECT TAKEOVER AUDIT

> 生成时间：2026-09-26 21:20（+08:00）。只读核验，未删除/移动任何文件。
> 本文档用于项目接管：记录磁盘真实状态、信息架构分类、跨仓库冲突与 GitHub 状态。

## 1. Git 状态核验

| 项 | 结果 |
|---|---|
| branch | `master`（仅本地） |
| HEAD | `667ecf7` `submission: add final package checklist and step six` |
| remote（本地配置） | **无**（`git remote -v` 为空） |
| remote（GitHub 实际） | `cvcingcvc-code/math` 存在，**空仓库**（0 commit，public，从未 push） |
| working tree | **dirty**：15 个 tracked 修改 + 73 个 untracked 条目 |
| .git 完整性 | 完整（HEAD/objects/refs/logs 均正常）；已备份到 `C:\Users\lin\.workbuddy\yu-git-safe-20260926\.git` |
| git 身份 | 全局 `user.name=Your Name`、`user.email=you@example.com`（占位） |
| push 凭据 | `gh` CLI 已登录 `cvcingcvc-code`（token 含 `repo` scope），credential helper 指向 `gh auth git-credential`，可 push |

## 2. 并发写入发现（重要）

- `paper/` 在本轮开始时（21:13–21:16）仍被另一进程写入：新增 `PAPER_NUMBER_LOCK.md`、`LITERATURE_CITATION_MAP.md`，并扩展了 `development_submission_candidate.md`（→26536B）与 `PAPER_EVIDENCE_TRACE.md`（→13915B），且重跑了 checker（`development_submission_consistency.json` = PASS 12/12）。
- `handoff/MULTIPROCESS_STATE.md` 的 `LAST_UPDATED` 停留在 18:22，4 个 Codex 窗口仍标 RUNNING 但已 3 小时未更新 → **这些窗口已实际停止**，但状态文件未收口。
- 21:16 之后 `paper/` 时间戳稳定（5 秒 + 3 分钟无变化）→ 并发写入已停止，可以安全收口。
- 结论：论文当前已进入 `PAPER_FINAL_DRAFT` 状态，带数字锁 + 文献映射 + 证据溯源，内容完整。

## 3. 信息架构分类（现状映射）

| 类别 | 目录/文件 | 状态 |
|---|---|---|
| CURRENT_CANONICAL | `outputs/final_results.json`；`data/annotations/ai/pilot_ai_provisional.csv`；`data/processed/pilot_sample.csv` | 唯一事实源 |
| DEVELOPMENT_EVIDENCE | `reports/development/`、`reports/verification/`、`reports/robustness/`、`reports/perturbation/`、`reports/external_transfer/`、`reports/failure_cases/`、`reports/visual_evidence/final/` | DEVELOPMENT_ONLY |
| EXPERIMENTAL | `experiments/model_tournament/`、`experiments/transfer_finance/` | DEVELOPMENT_ONLY |
| ARCHIVED / LEGACY | `outputs/` 多版 PPT、`.codex-finalizer/`、`work/`（gitignored） | 历史版本 |
| AUDIT | `reports/audit/`、`reports/review/`、`reports/RESEARCH_GATE_STATUS.md` | 审计 |
| HANDOFF | `handoff/`（PROJECT_STATE/NOW/NEXT_TASK/ARTIFACT_INDEX/BLOCKERS/DECISIONS/MULTIPROCESS_STATE/...） | 交接 |
| PAPER | `paper/development_submission_candidate.md`（canonical）、`paper/PAPER_*.md`、`paper/submission_candidate.*` | canonical + 历史候选 |
| DEMO | `reports/demo/index.html`、`reports/demo/serve_demo.py` | DEVELOPMENT_ONLY |
| DATA | `data/processed/`、`data/annotations/` | 原始已处理 + 标注 |
| SRC | `src/`、`scripts/`、`run_all.py` | 代码 |
| REPORTS | `reports/`（除上述子类外） | 报告 |

## 4. 跨仓库冲突（以 canonical evidence 与已过 checker 的论文边界为准）

来源：`paper/PAPER_NUMBER_LOCK.md`（已由前序进程登记）+ 本次复核。**论文侧已选 USED_SOURCE，本轮不改 Demo/实验。**

| # | 冲突 | USED（论文口径） | REJECTED | 处理 |
|---|---|---|---|---|
| 1 | Demo raw semantics | `final_results.json` M0 Raw = 16 / 0.228571 | Demo `demo_payload.json` raw_metrics = 12 / 0.171429（实为 theta0/M1 confidence-only） | 论文用统一事实源，Demo 本轮不修 |
| 2 | failure-case null vs 数值 | `final_results.json::counterexamples`（P105=2.0/0.75、P108=6.0/2.25，P072/P035=null） | `reports/failure_cases/development_candidates.json`（P105/P108 也写 null） | 论文用 final_results |
| 3 | Demo 默认参数 | `final_results.json` λ=0.5/0.5（M3） | Demo 默认 λ=0/0（theta0/M1） | 论文用 M3 口径 |
| 4 | run_all.py 32/32 范围 | 描述为「开发版核心链路可复现」 | 不声称覆盖全链路 | 论文已写进 Limitations |

数字无冲突：N=70、16 可判读（L2×5/L3×5/L4×1/L5×2/L6×3）、19 NO_EVIDENCE、35 UNDETERMINED、54 NO_EFFECTIVE_EVIDENCE、ABL/HOT/Gap=3.5625/0.375/1.125、effective weight 16→6、coverage 0.228571→0.085714、消融 16/12/6/6、693/660/33 —— 全部能定位到 canonical artifact。

## 5. GitHub 一致性

| 项 | 本地 | GitHub `cvcingcvc-code/math` |
|---|---|---|
| 内容 | 完整历史（HEAD 667ecf7）+ 未提交工作 | **空仓库**（0 commit） |
| 一致性 | — | **不一致：远程为空，从未 push** |

## 6. 结论

- 本地仓库完整、证据链齐全、论文已 `PAPER_FINAL_DRAFT`、checker 12/12 PASS。
- 远程为空仓库，等待首次 push。
- 唯一关键前置：确认 15 tracked + 73 untracked 的收口 commit 内容，再 push。
- 并发写入已停止，可安全收口。
