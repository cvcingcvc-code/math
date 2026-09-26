# FORMAL_GATE_SWITCH — 开发结果如何切换为正式结果

> 当前状态（2026-09-26）：**Gate = PENDING，formal 模式拒绝运行。**
> 仓库内全部结果均为 `annotation_source=AI_PROVISIONAL`、`status=DEVELOPMENT_ONLY`、`formal_gate_eligible=false`。
> 本文件只规定切换流程，不修改任何冻结阈值、R1/R2 或冻结手册。

## 1. 允许进入 formal 的前置条件（全部满足，缺一不可）

1. **真实人工标签到位**：同一标注者完成 R1（`data/annotations/human/pilot_worksheet_A.csv`），间隔至少 24 小时后完成 R2（`pilot_worksheet_A_retest.csv`），即冻结设计的单标注者 test-retest；不得由 AI 预标签复制或改写而来（D007/D008）。
2. **Gate 分析器正式运行**：`python src/run_s4_gate.py` 以 `validation/gate_thresholds.json`（`preregistered=true`，2026-09-25 冻结）为唯一阈值来源，生成新的 `reports/annotation_gate_report.json`。
3. **Gate 报告同时满足**：`gate_status == "PASS"` 且 `formal_gate_eligible == true`。冻结阈值包括：完整度 = 1.0；六级与三阶 Krippendorff α ≥ 0.667 且三阶 > 六级；每轴 UNDETERMINED ≤ 0.20；二次复核率 ≤ 0.40；evidence span 可定位率 ≥ 0.80；估计所需记录 ≥ 60；每条中位耗时 ≤ 120 秒。
4. **开放缺陷关闭**：Gate 报告 `defects_open`（当前 S4-F01、S4-F02）为空，或已按 DECISIONS 记录处置。

任一条件不满足：**报告不达标并缩小结论范围，不得回改阈值**（见 `gate_thresholds.json` notes）。

## 2. 需要替换的输入

| 当前开发输入 | 正式替换为 |
|---|---|
| `data/annotations/ai/pilot_ai_provisional.csv`（AI 临时标注，70 条） | 通过 Gate 的人工标签（R1 为主，R2 仅用于信度） |
| `reports/annotation_gate_report.json`（PENDING） | `run_s4_gate.py` 生成的 PASS 报告 |
| `src/development_data.py` 的 development 路径 | formal 路径（该模块在 development 模式下拒绝任何其他路径，formal 模式需 Gate PASS） |

AI 标注文件保留在仓库中作为开发记录，**不得**作为正式输入，也不得与人工标签混合。

## 3. 需要重新计算的字段

全部由脚本重算，不手工修改：

- 记录分类计数（可判读 Evidence / NO_EVIDENCE / UNDETERMINED），分母仍为全部记录。
- `effective_weight`、`effective_coverage`（Evidence Support）及 693 格参数网格。
- ABL、HOT、Gap（Score）；`lambda_prompt=1` 等有效权重为 0 的格仍为 `NO_EFFECTIVE_EVIDENCE`（未定义，不是 0）。
- Figure 3 / Figure 4、Demo payload、独立复算 source of truth、结果 CSV。
- 状态字段：`annotation_source` 改为人工来源，`formal_gate_eligible=true` 只能由 Gate 报告写入。

## 4. AIV 与 ranking 何时允许产生

- 仅当第 1 节全部满足，且在正式标签上完成学生级聚合、并有对应的信度与不确定性报告之后。
- 在此之前，结果 CSV 中 `AIV`、`ranking` 一律为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`；不得估算、插值、用开发数据代替或生成占位数字。
- 即使 Gate PASS，AIV 也不是 prompt/agent 的因果效应；因果解释需要另行的识别设计，不在当前项目范围内。

## 5. 为什么现在 `run_all.py --mode formal` 被拒绝

`run_all.py --mode formal` 只做一件事：转交 `src/run_partial_identification.py --mode formal`。后者读取 `reports/annotation_gate_report.json`，当前 `status=PENDING`，不满足 `gate_status=="PASS" and formal_gate_eligible==true`，于是输出 `FORMAL_MODE_BLOCKED` 并以非零码退出；`run_all.py` 随即打印 `RUN_ALL_FORMAL_BLOCKED`。
另外 `src/annotation_gate_report.py` 会拒绝任何全部为 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 的数据作为 Gate 输入。

## 6. 禁止人工绕过 Gate

以下行为一律禁止：

- 手工编辑 `annotation_gate_report.json` 把状态改为 PASS 或 `formal_gate_eligible=true`；
- 修改 `validation/gate_thresholds.json` 的阈值或 `preregistered` 标记；
- 把 AI 预标签填入人工工作表或标为人工来源；
- 注释、删除或短路 formal 模式的 Gate 检查；
- 把 DEVELOPMENT_ONLY 输出改名、去标记后作为正式结果提交。

切换必须通过：人工标注 → `run_s4_gate.py` → Gate PASS → `run_all.py --mode formal`，并在 `handoff/DECISIONS.md` 记录。
