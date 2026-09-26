# 数据结构与目录索引

> 本文件是项目全部数据的**分类索引**：按「原始数据 / 处理中间数据 / 模型输入 / 人工标注 / 开发结果 / 正式结果 / 演示样例」七类盘点，明确每类的现有路径与用途。
> 字段级定义见 `docs/data_dictionary.md`；运行方法见 `docs/RUN_GUIDE.md`。
> 本文档只描述现状，不改变任何冻结阈值、标注、模型结论或正式门禁状态。凡未在磁盘上核验的信息，一律标注「待核验」。

## 0. 一句话数据流

```
(仓库外原始 Excel 问答导出，未入库)
        │  清洗：纳入/排除（cohort_flow + exclusion_log）
        ▼
data/processed/clean_interactions.csv  (7028 turns，主清洗结果)
        │  抽样：秋 70 + 春 70 = 140
        ▼
data/processed/pilot_sample.csv  (N=140，正式 Pilot V1)
        │  盲标表构建（遮蔽 AI 预标注与 agent/path）
        ▼
data/annotations/human/pilot_worksheet_A.csv  (R1，70 行，待人工填写)
data/annotations/human/pilot_worksheet_A_retest.csv  (R2，70 行，≥24h 后填写)
        │  人工返回后：python src/run_s4_gate.py
        ▼
reports/annotation_gate_report.json  (当前 PENDING；PASS 后才进入 Formal)
```

旁路（开发版，非正式证据链）：`data/annotations/ai/pilot_ai_provisional.csv`（70 条 AI 预标注）驱动 `run_all.py` 的开发版复现，产出 `outputs/final_results.json` 与全部 DEVELOPMENT_ONLY 图表/论文/PPT/Demo。

## 1. 原始数据（Raw）— `data/raw/`

| 项 | 现状 |
|---|---|
| `data/raw/` | **空目录（0 个文件）**。原始问答 Excel 导出未入库。 |
| 来源 | 2025 秋与 2026 春两个学期的「Q&A 工作表」原始 Excel 导出（含学生提问与 AI 回答文本），由项目负责人持有，本仓库不含原件。 |
| 入库存档 | 未配置。如需复现「原始 → clean_interactions」这一步，需负责人补充原始导出并说明路径（**待核验/待补充**）。 |

> 原始数据的纳入/排除轨迹已固化在 `data/processed/cohort_flow.csv`（8 行流程计数）与 `data/processed/exclusion_log.csv`（2770 行逐条排除原因），不依赖原始 Excel 即可核验下游行数。

## 2. 处理中间数据（Processed）— `data/processed/`

| 文件 | 行数 | 编码 | 用途 |
|---|---|---|---|
| `clean_interactions.csv` | 7028 turns | UTF-8 BOM | 主清洗结果：每个发言一条；`speaker_role` student=3522 / ai=3506 |
| `pilot_sample.csv` | 140 | UTF-8 BOM | **正式 Pilot V1**，`pilot_id` P001–P140 唯一，分析单位为「学生轮」 |
| `pilot_ai_prelabel.csv` | 140 | UTF-8 BOM | AI 探索性预标注（`annotator_type=LLM_EXPLORATORY_NOT_HUMAN`，非人工标签） |
| `pilot_human_review_queue.csv` | 70 | UTF-8 BOM | 人工复核队列（50 疑难 + 20 随机）；**非盲表**，仅供分析侧，禁止下发标注者 |
| `cohort_flow.csv` | 8 | UTF-8 BOM | 两学期纳入/排除流程计数（845→824→5019；1925→401→2009） |
| `exclusion_log.csv` | 2770 | UTF-8 BOM | 逐条排除记录与原因（url_only / empty_text / outside_roster） |
| `speaker_audit.csv` | 120 | UTF-8 BOM | 话语主体人工审计样本（auto vs audited） |

## 3. 模型输入（Model input）— `data/annotations/ai/`

| 文件 | 行数 | 编码 | 用途 |
|---|---|---|---|
| `pilot_ai_provisional.csv` | 70 | UTF-8 BOM | **开发版模型唯一输入**。Bloom 取值为冻结手册 V0.1 的 L2–L6 + NO_EVIDENCE + UNDETERMINED；16 条可判读 Evidence、19 NO_EVIDENCE、35 UNDETERMINED。`annotation_source=AI_PROVISIONAL`、`annotation_status=DEVELOPMENT_ONLY` |
| `pilot_ai_assisted_full.csv` | 70 | UTF-8 BOM | AI 辅助标注（opencode CLI / deepseek-flash 生成）。**取值尺度为 L1–L6 + NOT_APPLICABLE，与冻结手册 L2–L6 不一致**，仅作开发记录，不得作正式输入 |
| `pilot_ai_provisional_meta.json` | — | — | provisional 生成说明与免责声明 |
| `pilot_ai_assisted_full_meta.json` | — | — | assisted 生成说明、执行环境、计数与源文件 SHA-256 |

## 4. 人工标注（Human annotation）— `data/annotations/human/`、`_keys/`、`workbuddy/`

| 文件 | 行数 | 编码 | 用途 / 状态 |
|---|---|---|---|
| `pilot_worksheet_A.csv` | 70 | **GB18030** | B010 R1 盲标表；当前 **0/70 已填**（原 1 条非法行已清空，备份于 `work/backups/`） |
| `pilot_worksheet_A_retest.csv` | 70 | UTF-8 BOM | B010 R2 盲标表；当前 **0/70 已填**（须 R1 ≥24h 后由同一人独立填写） |
| `pilot_worksheet_B.csv` | 70 | UTF-8 BOM | 旧双人方案遗留空白表，**当前 Gate 不使用** |
| `README_ANNOTATOR.md` | — | — | 标注者执行说明 |
| `_keys/pilot_worksheet_key.csv` | 70 | UTF-8 BOM | 盲标映射（agent/path/抽样/预标注），**仅分析侧**，不得随盲标表下发 |
| `workbuddy/pilot_worksheet_B_submitted.csv` | 70 | UTF-8 BOM（文件只读） | 队友 B 交回件；**取值尺度 L1–L6 + NOT_APPLICABLE，与冻结手册不一致**；不作为冻结 B010 的 R1/R2，不计算一致性 |

> 人工标注原件（worksheet A / retest / B）一律保留原件，不删除、不代填、不覆盖。清洗结果（如有）写入独立派生文件，不回写人工工作表。

## 5. 开发结果（Development results）

全部 `DEVELOPMENT_ONLY` / `AI_PROVISIONAL` / `formal_gate_eligible=false`，不得作为正式证据。

| 目录 / 文件 | 内容 |
|---|---|
| `reports/development/` | 开发指标、消融、反例、信度敏感性、部分识别网格、核心图、`research_core_closure.json` |
| `reports/verification/` | 独立数值复算、`core_numbers_source_of_truth.json`、`reproducibility_manifest.json` |
| `reports/robustness/` `perturbation/` `external_transfer/` `failure_cases/` | 稳健性 / 扰动 / 外部迁移 / 失败案例（DEVELOPMENT_ONLY / EXTERNAL_TRANSFER） |
| `reports/review/` `paper/` | 竞赛对齐审计、评委问答、论文叙事草稿 |
| `experiments/model_tournament/` | 模型锦标赛（baselines / formulations / ML challenger / final） |
| `experiments/transfer_finance/` | 金融外部迁移验证 + Binance live shadow（公共行情 GET-only，fail-closed） |
| `outputs/final_results.json` | 统一事实源（paper/demo/PPT/figures 共同读取），development-only |

## 6. 正式结果（Formal results）

| 文件 | 状态 |
|---|---|
| `reports/annotation_gate_report.json` | **PENDING**（`gate_report_generated=false`），正式人工标注返回前不生成 |
| `validation/gate_thresholds.json` | 冻结阈值，`preregistered=true`（2026-09-25 19:40），不得回改 |
| `FORMAL_GATE_SWITCH.md` | 开发 → 正式切换流程（正式 AIV/排名仅在 Gate PASS 后允许） |

正式门禁链：负责人完成 R1 → ≥24h → R2 → `python src/run_s4_gate.py` → `gate_status=PASS` 且 `formal_gate_eligible=true` → 才可走 `FORMAL_GATE_SWITCH.md`。

## 7. 演示样例（Demo / deliverable）

| 文件 | 用途 |
|---|---|
| `reports/demo/index.html` | 模型验证交互页，顶部标注 `DEVELOPMENT_ONLY · AI_PROVISIONAL` |
| `reports/demo/demo_payload.json` | Demo 数据接口 |
| `reports/demo/serve_demo.py` | 本地只读启动器（端口 4173） |
| `outputs/education_ai_evidence_roadshow_final.pptx` | 路演 PPT（10 页，视觉冻结，暂停样式改动） |
| `outputs/submission_package_development_only/` | 内部开发版提交包（含 MANIFEST） |
| `reports/visual_evidence/final/` | F1–F6 最终图（paper 用 F1–F5，Demo 用 F1–F3） |

## 8. 关键状态标记（全项目统一口径）

| 标记 | 含义 |
|---|---|
| `AI_PROVISIONAL` / `AI_ASSISTED` | AI 生成，非人工验证 |
| `DEVELOPMENT_ONLY` | 仅开发/演示，不得作为正式结论 |
| `formal_gate_eligible=false` | 不满足正式门禁 |
| `HUMAN_R1 / HUMAN_R2 = 0/70` | 真实人工标签尚未返回 |
| `NO_EFFECTIVE_EVIDENCE` | 未定义（≠ 数值 0） |
| `AIV / ranking = NOT_AVAILABLE_PENDING_FORMAL_GATE` | 正式值待门禁 |

## 9. 待核验 / 待处理问题（本索引登记）

1. `data/raw/` 为空：原始 Excel 导出未入库，复现起点缺失（**待负责人补充**）。
2. `pilot_ai_assisted_full.csv` 与 `workbuddy/pilot_worksheet_B_submitted.csv` 使用 L1–L6 + NOT_APPLICABLE 尺度，与冻结手册 L2–L6 不一致（**仅开发记录，不混入正式输入**；尺度差异待核验是否需在手册 V0.2 说明）。
3. `scripts/project_manager.py` 原 `DEFAULT_ROOT` 硬编码个人绝对路径（**已于本次改为项目相对路径**）。
4. 本仓库未配置 git remote（预期仓库 `https://github.com/cvcingcvc-code/math` **待核验**；本次不涉及推送）。
