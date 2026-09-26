# 跨工具协作约定（Codex / WorkBuddy / 其他编程工具）

> 目的：多个 AI 窗口 / 工具并行工作时，不读聊天历史即可知道「谁在改什么、我能改哪、如何避免撞车」。
> 本文档是对 `handoff/MULTIPROCESS_STATE.md` 与 `scripts/project_manager.py` 的补充说明，不改动现有协调机制。

## 1. 现状：单一协调中枢

- **唯一事实源**：`handoff/MULTIPROCESS_STATE.md`（Markdown + 内嵌 JSON），记录 workstream、active windows、写锁、风险与下一允许任务。
- **协调工具**：`scripts/project_manager.py`（文件锁 + 原子替换，无服务、无依赖）。
- **权威交接链**（`AGENTS.md` 规定）：`PROJECT_STATE.md` → `DECISIONS.md` → `NEXT_TASK.md` → `ARTIFACT_INDEX.md` → `BLOCKERS.md`。
- **快速快照**：`handoff/PROJECT_NOW.md`（当前 HEAD / phase / 冻结 / blocker / 权威文件）。

## 2. 任务分工与写入范围

| 角色/工作流 | 状态 | 写入范围 | 说明 |
|---|---|---|---|
| MAIN_RESEARCH | FROZEN | `CORE_MODEL` | 研究主线，唯一可授权 `--reopen` 新补充 |
| AUDIT | 视窗口 | `AUDIT_REGISTRY`（`reports/audit/`） | 独立审计报告，不改实验/模型/标签/样式 |
| HUMAN_GATE | BLOCKED | 仅负责人（人工） | R1/R2 只能由真人填写，禁止任何工具代填 |
| FORMAL_VALIDATION | BLOCKED | 无（fail-closed） | Gate PASS 前禁止写 |
| PPT / FIGURES / MODEL_PRESENTATION / BASELINE / ALTERNATIVE_FORMULATIONS | FROZEN | 只读 | 已冻结，勿重跑/改样式 |
| WorkBuddy（本工具） | 本次为文档整理 | `docs/`、`handoff/` 新增文件、`README.md`、`scripts/project_manager.py` | 只做数据结构整理与交接文档，不碰 data/ 与 reports/ 证据 |

> 规则：只写自己的 scope；写 `reports/audit/` 前先确认 `WRITE_LOCKS` 中 `AUDIT_REGISTRY` 是否被某窗口持有。

## 3. 写锁机制（如何避免同时改同一文件）

- `project_manager.py register` 时对 `--write-scope` 加锁并写入 `WRITE_LOCKS`；`handoff` 时释放。
- 两个窗口不得持有同一 scope；冲突时返回 `CONFLICT`。
- 只读审计（`--mode READONLY`）不取锁，可并行，但只能写独立输出路径。
- 锁文件：`handoff/MULTIPROCESS_STATE.md.lock`（短时独占，120s 过期自动清理）。

**任何工具写文件前**：
1. 读 `handoff/MULTIPROCESS_STATE.md`，确认目标 scope 无锁。
2. 目标若在 `data/annotations/`、`reports/` 证据目录，默认只读，不覆盖原件。
3. 新增文件用唯一命名，不 `reset` / `checkout` / 删除他人文件。

## 4. 交接记录

- Codex 窗口交接：`handoff/multiprocess/WINDOW_<时间戳>.md`（FILES_CREATED / FILES_MODIFIED / RESULTS / CLAIM_BOUNDARY / WRITE_LOCK_RELEASED）。
- 本工具（WorkBuddy）交接：`handoff/DATA_ORGANIZATION_REPORT_2026-09-26.md`（本次整理报告）。
- 持久状态更新集中在 `PROJECT_STATE.md` / `CHANGELOG.md` / `ARTIFACT_INDEX.md`，避免多文件重复状态。

## 5. 不依赖聊天记忆/私有技能

- 所有关键状态、数据路径、命令、下一步都落在仓库文件里（`handoff/`、`docs/`、`README.md`、`AGENTS.md`）。
- 运行不依赖任何特定 AI 助手的私有技能或会话记忆。
- 唯一机器相关配置在 `AI_WORKFLOW.md`（Codex/OpenCode 客户端配置，属本机环境，不在仓库内）。
