# 教育 AI 交互证据评价：Partial Identification / Bounds（开发版）

> **状态声明**：本文档只承载 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 结果，`formal_gate_eligible=false`。所有数值均不是正式人工标注结果、统计置信区间、因果效应、正式 AIV 或学生排名。

## 1. Introduction

AI 介入后的交互日志同时包含学生行为、智能体引导和上下文限制。观察到的学生文本不自动等于学生能力，因此评价模型必须先回答：哪些文本可作为可解释的 Evidence，以及这些 Evidence 在偏差假设下是否仍有足够支持。

## 2. Problem definition

令 `E_i=1` 表示第 `i` 条记录的 `student_evidence_bloom` 属于 L1–L6。`p_i` 表示 `prompt_induced=true`，`t_i` 表示 `context_truncated=true`。本项目中的 support 指可用于指标计算的有效 Evidence 权重，不等同于学习效果或能力真值。

## 3. Data and measurement

开发入口仅为 `data/annotations/ai/pilot_ai_provisional.csv`，共 70 条记录，其中 16 条进入 L1–L6。16 条全部为 `prompt_induced=true`、`task_actor=ai`、`confidence=medium`、`context_truncated=false`。该分离结构已在 provenance audit 中追踪；字段仍属于 provisional 标注结果，不能替代人工 R1/R2。

冻结规则要求存在可定位证据 span，并将复制、来源不可比、上下文不足或无法判断的记录保留为 `NO_EVIDENCE` / `UNDETERMINED`。这会使 L1–L6 分母受到选择机制影响。

## 4. Identification strategy

当前没有 readable Evidence 的 `prompt_induced=false` 对照，也没有 context、confidence、actor 的充分交叉支持。因此 prompt penalty、context penalty、confidence reliability 和 actor correction 均不能作为观察数据估计的点参数。它们只能进入透明的 assumption-based sensitivity / bounds 分析。

## 5. Partial-identification model

对可判读记录定义：

```text
w_i(θ) = I(E_i=1) × c_i × (1 - λ_prompt p_i) × (1 - λ_context t_i)
```

其中 `c_i=1`（high）、`r_medium`（medium）或 `0.5`（low）。本开发版扫描：

```text
λ_prompt = 0.00, 0.05, ..., 1.00
λ_context = 0.00, 0.10, ..., 1.00
r_medium ∈ {0.50, 0.75, 1.00}
```

定义：

```text
ABL(θ) = Σ w_i Bloom_i / Σ w_i
HOT(θ) = Σ w_i I(Bloom_i ≥ L4) / Σ w_i
Gap(θ) = Σ w_i(Task_i - Bloom_i) / Σ w_i
```

当 `Σw_i=0` 时返回 `NO_EFFECTIVE_EVIDENCE`，不平滑、不插值、不填 0。所得区间是 **assumption-based identification interval**，不是统计置信区间。

## 6. Development experiments

实验包括参数网格、A–G stress tests 和 M0–M4 组件状态审计。没有拟合复杂模型，也没有以 accuracy 作为比较目标，因为当前缺少人工标签真值。`formal` 模式接口采用 fail-closed：没有 Gate PASS 且 `formal_gate_eligible=true` 时拒绝运行，且当前尚未启用正式数据适配器。

## 7. Development results

基线（`λ_prompt=0`、`λ_context=0`、`r_medium=0.75`）为：`ABL=3.5625`、`HOT=0.375`、`Gap=1.125`。本文中 `effective coverage = effective evidence weight / 70 development records`，分母为全部 70 条开发记录，而不是 16 条可判读 Evidence。在有效参数网格中，这三个分数几乎不变；但 effective evidence weight 从 16.0 降至 0.4，effective coverage 从 0.2286 降至 0.0057。这里 coverage 的分母是全部 70 条 development records，而不是 16 条可判读 Evidence。当 `λ_prompt=1` 时，当前数据进入 `NO_EFFECTIVE_EVIDENCE`。

因此当前开发版最重要的结果是：**Score Stability ≠ Evidence Support Stability**。主要不确定性来自 evidence availability，而不是分数本身；这不是已识别的 prompt causal effect。

## 8. Limitations

- 缺少真实人工 R1/R2 和 Gate 通过结果；当前数据不能支持正式 reliability 或 AIV。
- 没有 readable `prompt_induced=false`、`context_truncated=true`、low/high confidence 或非-ai actor 对照。
- provisional 文件未提供完整可复现的逐条生成决策日志，部分分离来源保持 `UNRESOLVED`。
- 没有独立无 AI 学习 outcome、可靠 session_id 或可比 treatment/control，因此不能宣称因果增量、学生能力或排名。
- 不能将 70 条 development 结果外推为 140 条正式人工标注结论。

## 9. Formal replacement plan

人工 R1/R2 返回后，必须按以下顺序执行：

```text
Human R1/R2
→ reliability and Gate
→ Gate PASS + formal_gate_eligible=true
→ formal source adapter
→ support / identifiability audit
→ bounds / stress tests
→ Demo and paper outputs
```

正式结果位置：`[TBD AFTER HUMAN R1/R2 GATE]`。开发版文件不得被覆盖为正式结果。
