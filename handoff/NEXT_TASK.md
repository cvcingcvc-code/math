# NEXT TASK

Stage: S4-Pilot Annotation Gate

当前状态：**HUMAN_R1 = 0/70 VALID**（原始填写 1/70，但该行字段错位/非法，已清空；原始非法行保留于 `work/backups/pilot_worksheet_A_2026-09-26_1117_checkpoint.csv`）；HUMAN_R2 = 0/70；AI_ASSISTED = 70/70 `DEVELOPMENT_ONLY`；Formal Gate 未运行。工作表可用 UTF-8 或 GB18030 保存，Gate 读取器已兼容两种编码并已修复大小写规范化。

## 唯一下一任务

**下一优先：负责人完成真实 HUMAN R1=`data/annotations/human/pilot_worksheet_A.csv` 70/70；R1 完成后冻结并记录完成时间与 SHA-256，满足至少 24 小时重测间隔后，再由负责人独立完成 R2=`data/annotations/human/pilot_worksheet_A_retest.csv` 70/70，然后运行 Gate 分析器。**

R1 未完成前不得开始 R2；今天不得代填、不得复制 R1 到 R2、不得展示 R1 与 AI 标签对比。

执行前必读（顺序）：
1. `data/annotations/human/README_ANNOTATOR.md`
2. `docs/annotation/annotation_manual_v0.1.md`
3. `docs/annotation/annotation_clarification_v0.1.1.md`（若负责人已签署采纳）

确认输入来自 Canonical Pilot：`data/processed/pilot_sample.csv`，N = 140。不得使用旧 56 条 Pilot。
盲标表已遮蔽 AI 预标注与 agent/path 名称；不得从别处找回这些信息。

## 收到人工标注后执行

一条命令：

```
python src/run_s4_gate.py
```

它依次执行：可靠性自检 → 数据完整性核验 → 重建盲标表 → 若两份表都已填则生成 Gate Report。

等价的手动步骤：

1. `python src/verify_pilot_integrity.py`（21 项冻结不变量 + 缺陷登记）
2. 核验交回文件的 record_id 与 Canonical Pilot 一致（键表：`data/annotations/_keys/pilot_worksheet_key.csv`）
3. **不得覆盖**原始 AI 预标注与任何已交回的标注版本
4. `python src/annotation_gate_report.py --a <A.csv> --b <B.csv>`
5. 生成 adjudication 数据（分歧 + medium/low 条目）
6. 计算六级与三阶一致性，输出混淆矩阵
7. 检查 Task Bloom vs Student Evidence gap
8. 按 agent 描述 gap，但不提前宣称因果
9. 判断 annotation_manual 是否需要升级到 V0.2

Formal path check: Gate report generation now emits the frozen decision fields, but
`src/run_partial_identification.py --mode formal` remains fail-closed because the
formal source adapter is intentionally not enabled before a real Gate PASS. Do not
run or promote development inputs; after Gate PASS, implement only the minimal
formal-input adapter before the formal model run.

## Gate 必须回答

- 六级标注是否可执行？
- 三阶是否明显更稳？
- Task/Evidence 双轴是否有实际信息价值？
- 哪些类别最常混淆？
- UNDETERMINED / NO_EVIDENCE 比例是多少？
- 人工成本是否可接受？
- 智能体路径偏差是否出现初步证据？
- 是否允许进入模块 A 全量实验？

`src/annotation_gate_report.py` 会输出这 8 问的观察值；在 `validation/gate_thresholds.json` 被确认为 `preregistered: true` 之前，它**不会**给出通过判定。

## 前置动作（负责人，须在标注者开工前完成）

- [ ] 确认采纳 `annotation_clarification_v0.1.1.md`（或指出需修改处）
- [ ] 在**未查看一致性结果**的前提下确认 `validation/gate_thresholds.json`
- [x] B008 已冻结为 70 条核心样本；B010 已冻结为同一标注者 R1/R2 重测

## Gate 未通过前禁止

- 全量正式标注
- 最终 AIV
- CTQ/DHI 冻结
- PSM/DID
- 论文强结论

## 本窗口已完成的论文/答辩并行工作

- 论文主叙事、3 分钟故事、30 秒 pitch、核心图 caption、评委攻击问题与五个薄弱点已整理到 `reports/paper/` 与 `reports/review/`。
- 这些材料不改变冻结模型或正式 Gate；必须继续沿用 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `formal_gate_eligible=false` 口径。

## 本窗口已完成的独立数值复算

- 已从 provisional CSV 独立重算 70 条、16 条 Evidence、693 个网格条件、33 个 undefined 和全部核心数字。
- 结果、Demo payload 与论文数字已完成交叉核对；详细报告见 `reports/verification/reproduction_review.md`。
- 未修改冻结模型、正式数据、标签、Demo UI 或论文主体。

## 与人工标注并行、不依赖标签的任务（负责人确认 B009、B010 后）

在 `research/module_c_candidates.md` 增补"小样本收缩 AIV"：Beta-Binomial / 经验贝叶斯 HOT、最低证据量门槛、
CTQ 降为 session/组级；用合成标签做误差传播与排名稳定性模拟（明确标为模拟，不是结果）。

## Parallel closeout completed (2026-09-26)
- Continue only non-R1 work: preserve deck/demo/package; after formal R1/R2 are complete, run the frozen Gate workflow supplied by the owner.


## User-directed pause
- Do not modify PPT styling until the user signals final beautification is complete.
- Continue only paper/text work that does not depend on R1/Gate.


## Current round completed
- External design absorption is complete for the four requested items: provenance separation confirmed, Explain output added, What-if output added, and unified final artifact added.
- Core figures are generated from the unified artifact inputs; no decorative dashboard or new model was introduced.

## Next recommended action
- Owner completes real HUMAN_R1 and HUMAN_R2 under the frozen protocol; then run `python src/run_s4_gate.py`. After Gate PASS, add only the minimal formal-input adapter and re-run the same deterministic artifact path.

## Development submission candidate status
- Human validation is intentionally paused. Do not repeat R1/R2 checks or emit a blocked report unless the owner resumes validation.
- Development candidate is unified and consistency-checked. Formal adapter is READY_INTERFACE_ONLY, with no formal run.
- Next work after user resumes validation: complete the frozen human Gate, then use the existing adapter and frozen deterministic model.

## External Transfer Validation — current round
- Binance public-data shadow pipeline is isolated at `experiments/transfer_finance/live_shadow/`.
- Do not change frozen parameters or historical `experiments/transfer_finance/transfer_validation.json`.
- Continue only by rerunning with `$env:LIVE_ORDERING_ENABLED='false'`; wait for 24h matured records before assessing forward quality. Never add private/account/trading calls.

## Presentation convergence handoff (2026-09-26)
- Model/Demo/Paper/Judge Defense 已按 `metric_dictionary.md` 收敛。
- Demo=PASS；Paper=PARTIAL（等待 Formal 数字）；Judge Defense=PASS。
- 下一步仍是负责人完成真实 HUMAN R1/R2，不得由 AI 代填。
## Model tournament evaluator (2026-09-26)

- Tournament protocol frozen before candidate-result review: `experiments/model_tournament/protocol/model_tournament_protocol.md`.
- Current comparison artifacts: `experiments/model_tournament/final/`.
- Result boundary: development-only; Formal HUMAN_R1/R2 and Formal Gate remain pending.
- `NO_SINGLE_DOMINANT_MODEL`; ML challenger is complete at `experiments/model_tournament/ML_CHALLENGER_HANDOFF.md` with `INSUFFICIENT_FOR_STRONG_ML_CLAIM`.
## Robustness round complete (2026-09-26)
The requested robustness/perturbation/external-transfer validation is complete as DEVELOPMENT_ONLY / EXTERNAL_TRANSFER. Do not start a new research line. Next action remains owner-completed HUMAN_R1 then HUMAN_R2 after 24 hours, followed by the frozen Gate command.

## Visual evidence convergence complete (2026-09-26)
- Final F1–F6 files: `reports/visual_evidence/final/`.
- Paper uses F1–F5 in the main evidence chain and F6 in External Transfer / Limitations; Demo home uses F1–F3 only.
- No further visual expansion, model work, tuning, or result recalculation is authorized in this window. Stage status: `VISUAL_EVIDENCE_CONVERGENCE = DONE`.
