# S4-Pilot Annotation Gate Report

**状态：PENDING — 尚未生成。**

本文件是占位说明，不是 Gate 结果。迄今**没有**任何真实人工标注返回，因此不存在可报告的一致性系数。

## 为什么这里是空的

Gate 需要两名独立人工标注者对同一批记录完成盲标。工作已就绪：

| 就绪项 | 路径 |
|---|---|
| 盲标表 A | `data/annotations/human/pilot_worksheet_A.csv` |
| 盲标表 B | `data/annotations/human/pilot_worksheet_B.csv` |
| 标注者说明 | `data/annotations/human/README_ANNOTATOR.md` |
| 规则本体 | `docs/annotation/annotation_manual_v0.1.md` |
| 执行澄清件 | `docs/annotation/annotation_clarification_v0.1.1.md` |
| 遮蔽映射（分析侧） | `data/annotations/_keys/pilot_worksheet_key.csv` |
| 预注册阈值 | `validation/gate_thresholds.json`（当前 `preregistered: true`，但 Gate 仍为 PENDING） |

## 如何生成真正的 Gate Report

标注者交回两份带标签的工作表后：

```
python src/run_s4_gate.py
```

脚本会自动在 `data/annotations/human/` 中寻找已填写的表；若有歧义则用 `--a <fileA> --b <fileB>` 指定。

## 已经完成的核验（不是 Gate 结论）

- `src/verify_pilot_integrity.py`：21/21 冻结不变量通过。
- 缺陷登记：S4-F01（`ai_context_text` 未来内容泄漏）、S4-F02（复核队列非盲标）——两项均已从标注路径隔离。
- 可靠性算法自检：9/9 与手算值一致（`python src/reliability.py`）。

## 边界声明

- D008：人工标注完成前不计算正式 Kappa / Alpha。本文件遵守该约束。
- 在 `validation/gate_thresholds.json` 已确认为 `preregistered: true`，但 R1/R2 尚未返回，因此本文件仍只是 PENDING 占位，不构成 Gate 通过判定；阈值不得在看到结果后回改。
- 不得把 AI 预标注结果描述为人工标注（D007）。