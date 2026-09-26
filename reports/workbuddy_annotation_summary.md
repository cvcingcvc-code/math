# WorkBuddy B 单标注描述性汇总

- 来源：`data/annotations/workbuddy/pilot_worksheet_B_submitted.csv`
- 记录数：70
- 用途：为后续人工 Gate/适配准备描述性数据；不计算一致性系数。

## 关键比例

- Task 数值等级（L1–L6）：0.7
- Student Evidence 数值等级（L1–L6）：0.5143
- NO_EVIDENCE：0.2429
- Task UNDETERMINED：0.2857
- Evidence UNDETERMINED：0.2429
- 需二审：0.5143

## 分布

### Task Bloom

```json
{
  "UNDETERMINED": 20,
  "L2": 17,
  "L4": 13,
  "L5": 7,
  "L3": 6,
  "L1": 4,
  "L6": 2,
  "NOT_APPLICABLE": 1
}
```

### Student Evidence Bloom

```json
{
  "NO_EVIDENCE": 17,
  "UNDETERMINED": 17,
  "L2": 11,
  "L4": 8,
  "L3": 6,
  "L1": 5,
  "L5": 5,
  "L6": 1
}
```

### Confidence

```json
{
  "high": 34,
  "low": 21,
  "medium": 15
}
```

### Content relation

```json
{
  "independent": 25,
  "reworked_with_addition": 19,
  "not_comparable": 18,
  "reworked_without_addition": 7,
  "copied_verbatim": 1
}
```

### Correctness

```json
{
  "": 34,
  "correct": 20,
  "partially_correct": 11,
  "not_assessable": 4,
  "incorrect": 1
}
```

## 边界

该文件是队友 B 的交回件。它不替代冻结 B010 的 R1/R2，不与自身或 AI 标签计算一致性，不产生 Formal AIV、学生排名或因果结论。