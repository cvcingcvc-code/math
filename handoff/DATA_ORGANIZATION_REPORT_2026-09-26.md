# 数据结构整理与跨工具交接报告

> 时间：2026-09-26（晚间窗口，WorkBuddy）
> 范围：数据结构整理 + 跨工具接手入口，**不含**推送/发布/上传，**不含**数据清洗改写，**不改变**任何冻结阈值、标注、模型结论或正式门禁状态。

## 1. 现状核验结果（全部在磁盘上重新核验，非照抄历史）

| 项 | 核验结果 |
|---|---|
| Git | `master` 分支，HEAD `667ecf7`；工作区 dirty（11 tracked 修改 + 58 untracked，非阻塞交付态）；**未配置 remote**（预期仓库 `github.com/cvcingcvc-code/math` 待核验） |
| 其他工具写入 | `MULTIPROCESS_STATE.md` 记录 4 个 Codex 窗口（2 AUDIT、2 FORMAL_VALIDATION），`WRITE_LOCKS: AUDIT_REGISTRY → WINDOW_20260926_180938`；本轮未触碰 `reports/audit/` |
| 完整性核验 | `python src/verify_pilot_integrity.py` → **21/21 通过**，2 open HIGH 缺陷（S4-F01 未来内容泄漏、S4-F02 非盲队列） |
| Pilot | `pilot_sample.csv` N=140，`pilot_id` P001–P140 唯一，140/140 学生轮 |
| clean_interactions | 7028 turns（student 3522 / ai 3506） |
| AI provisional | 70 行，16 可判读（L2=5/L3=5/L4=1/L5=2/L6=3）+ 19 NO_EVIDENCE + 35 UNDETERMINED |
| 人工标注 | R1 `pilot_worksheet_A.csv` 70 行（GB18030）**0/70 有效**；R2 `_retest.csv` 70 行 **0/70**；B 遗留空白 70 行 |
| Gate 报告 | `reports/annotation_gate_report.json` = PENDING（`gate_report_generated=false`） |

> 历史聊天中的「完成」「冻结」「标注数量」均重新核验，与上述一致，未发现偏差。

## 2. 数据结构整理

- 新增 `docs/DATA_STRUCTURE.md`：按「原始 / 处理中间 / 模型输入 / 人工标注 / 开发结果 / 正式结果 / 演示样例」7 类盘点全部数据，明确路径、行数、编码、用途与状态。
- 扩展 `docs/data_dictionary.md`：从「开发版链路」扩展为覆盖 `clean_interactions`、`pilot_sample`、`cohort_flow`、`exclusion_log`、`speaker_audit`、`pilot_ai_prelabel`、`pilot_human_review_queue`、盲标表、`_keys`、workbuddy 交回件、provisional/assisted 的字段级字典，并补充表间关联。
- **未移动任何文件**，因此无代码/配置引用需要同步更新（零迁移）。

## 3. 格式清洗说明

**本次未实施任何数据清洗。** 理由：现有数据已由既有管线完成清洗（轨迹固化于 `cohort_flow.csv` + `exclusion_log.csv`），未发现「依据明确」的格式问题需要改写。发现的疑似问题一律登记为待处理，**不删除、不填补、不修改**：

- 原始数据 `data/raw/` 为空（未入库，复现起点缺失）——待负责人补充。
- `pilot_ai_assisted_full.csv` 与 `workbuddy/pilot_worksheet_B_submitted.csv` 使用 L1–L6 + NOT_APPLICABLE 尺度，与冻结手册 L2–L6 不一致——仅作开发记录，不混入正式输入；尺度差异待核验是否需手册 V0.2 说明。

**清洗前后行数：无清洗操作，全部数据行数不变**（证据：本节与第 1 节行数一致）。

## 4. 修改 / 新增文件清单

| 文件 | 动作 | 说明 |
|---|---|---|
| `docs/DATA_STRUCTURE.md` | 新增 | 数据分类与目录索引 |
| `docs/data_dictionary.md` | 覆盖重写 | 完整字段级数据字典 |
| `docs/RUN_GUIDE.md` | 新增 | 环境、命令、预期输出、检查方法 |
| `handoff/CROSS_TOOL_HANDOFF.md` | 新增 | 多工具协作约定 |
| `handoff/DATA_ORGANIZATION_REPORT_2026-09-26.md` | 新增 | 本报告 |
| `README.md` | 更新 | 增加唯一接手入口 + 指向新文档 |
| `scripts/project_manager.py` | 修改 1 处 | `DEFAULT_ROOT` 由个人绝对路径改为 `Path(__file__).resolve().parents[1]`（项目相对） |

**未改动的证据文件**：`data/**`、`reports/**`、`validation/**`、`paper/**`、`outputs/**`、`experiments/**` 均未触碰；冻结阈值、R1/R2、模型参数、论文结论、正式门禁状态均未变。

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| 只读完整性核验 `verify_pilot_integrity.py` | 21/21 通过，2 open HIGH 缺陷（预期） |
| 数据行数/编码/主键/标注状态核验（stdlib 只读脚本） | 全部与文档一致 |
| `scripts/project_manager.py status`（改后） | 待见下方（相对路径解析正常） |
| 绝对路径扫描（`*.py`） | 仅 `project_manager.py` 1 处，已改；其余 src 均 `Path(__file__).parents[1]` 相对定位 |
| 文档路径有效性 | 本报告引用的所有文件均存在（见第 1 节核验） |
| 代码引用未断 | 未移动文件，引用无需改动；`project_manager.py` 改动不改变对外接口（`--root` 仍可覆盖） |

## 6. 剩余问题（未解决，登记不处理）

1. `data/raw/` 为空 → 原始 Excel 导出未入库（待负责人补充路径）。
2. L1 尺度漂移（assisted + workbuddy）→ 待核验是否需手册 V0.2 说明。
3. git remote 未配置 → 预期仓库待核验；本任务不推送。
4. 4 个 Codex 窗口状态仍为 RUNNING（`MULTIPROCESS_STATE.md` 最后更新 18:22，距本次约 2 小时）→ 建议下一窗口先确认其是否已交接。

## 7. 其他编程工具的最短阅读顺序（2 分钟上手）

1. `README.md`（接手入口）
2. `handoff/PROJECT_NOW.md`（当前状态）
3. `handoff/NEXT_TASK.md`（下一步）
4. `docs/DATA_STRUCTURE.md` + `docs/data_dictionary.md`（数据）
5. `docs/RUN_GUIDE.md`（怎么跑）

## 8. 下一项可执行任务

**负责人完成真实 HUMAN R1**（`data/annotations/human/pilot_worksheet_A.csv` 70/70）→ 记录完成时间与 SHA-256 → 至少 24 小时后完成 R2（`pilot_worksheet_A_retest.csv`）→ 运行 `python src/run_s4_gate.py`。Gate 非 PASS 前保持 development-only，不回改阈值。
