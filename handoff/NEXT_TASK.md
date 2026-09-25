# NEXT TASK

Stage: S4-Pilot Annotation Gate

当前状态：**READY_FOR_ANNOTATION**。协议阻塞已处理，标注包已交付；只差真实人工标签。

## 唯一下一任务

**由两名独立人工标注者执行 `data/annotations/human/pilot_worksheet_A.csv` 与 `_B.csv` 的盲标，然后运行 Gate 分析器。**

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
- [ ] 裁定 B008（"140 条" 与 "70 条双标" 的口径）

## Gate 未通过前禁止

- 全量正式标注
- 最终 AIV
- CTQ/DHI 冻结
- PSM/DID
- 论文强结论

## 本窗口已完成的论文/答辩并行工作

- 论文主叙事、3 分钟故事、30 秒 pitch、核心图 caption、评委攻击问题与五个薄弱点已整理到 `reports/paper/` 与 `reports/review/`。
- 这些材料不改变冻结模型或正式 Gate；必须继续沿用 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `formal_gate_eligible=false` 口径。

## 与人工标注并行、不依赖标签的任务（负责人确认 B009、B010 后）

在 `research/module_c_candidates.md` 增补"小样本收缩 AIV"：Beta-Binomial / 经验贝叶斯 HOT、最低证据量门槛、
CTQ 降为 session/组级；用合成标签做误差传播与排名稳定性模拟（明确标为模拟，不是结果）。
