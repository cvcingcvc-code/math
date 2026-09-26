# Independent reproduction review

## 1. Scope and method

本次复算直接读取：

`data/annotations/ai/pilot_ai_provisional.csv`

没有调用生产 summary、production metric 函数或 Demo payload 作为输入。独立脚本为：

`src/verification/recompute_bounds.py`

它单独实现了行级权重、ABL、HOT、Gap、effective weight、coverage 与 zero-denominator handling，并生成了参数笛卡尔积。

## 2. Reproduction verdict

| 项目 | 独立结果 | 声称结果 | 结论 |
|---|---:|---:|---|
| 总记录数 | 70 | 70 | 复现 |
| 可判读 Evidence | 16 | 16 | 复现 |
| NO_EVIDENCE | 19 | 19 | 复现 |
| UNDETERMINED | 35 | 35 | 复现 |
| 理论参数网格 | 693 | 693 | 复现 |
| defined cells | 660 | 隐含为 660 | 复现 |
| undefined cells | 33 | 33 | 复现 |
| ABL | 3.5625 | 3.5625 | 复现 |
| HOT | 0.375 | 0.375 | 复现 |
| Gap | 1.125 | 1.125 | 复现 |
| effective weight 最大值 | 16.0 | 16.0 | 复现 |
| effective weight 最小非零值 | 0.4 | 0.4 | 复现 |
| effective coverage 最大值 | 16/70 = 0.228571... | 0.2286 | 复现 |
| effective coverage 最小非零值 | 0.4/70 = 0.005714... | 0.0057 | 复现 |

参数网格理论大小为：

```text
21 个 lambda_prompt
× 11 个 lambda_context
× 3 个 r_medium
= 693
```

不存在过滤或隐藏组合；693 的口径正确。

## 3. Raw input recount

### 全部 70 条

- `student_evidence_bloom`：
  - `UNDETERMINED`: 35
  - `NO_EVIDENCE`: 19
  - `L2`: 5
  - `L3`: 5
  - `L4`: 1
  - `L5`: 2
  - `L6`: 3
- `prompt_induced`: true 53，false 17
- `context_truncated`: true 28，false 42
- `confidence`: low 51，medium 19
- `task_actor`: ai 53，student 11，unknown 6
- `task_source`: ai_prompt 53，student_request 11，unknown 6

### 16 条可判读 Evidence

- `prompt_induced=true`: 16/16
- `context_truncated=false`: 16/16
- `confidence=medium`: 16/16
- `task_actor=ai`: 16/16
- `task_source=ai_prompt`: 16/16

## 4. Coverage denominator

独立复算确认 effective coverage 的分母是**全部 70 条 development records**，不是 16 条 interpretable Evidence：

```text
effective_coverage = sum(w_i) / len(all_rows)
```

因此：

- 最大 coverage = `16 / 70 = 0.228571...`
- 最小非零 coverage = `0.4 / 70 = 0.005714...`
- 基线 coverage = `12 / 70 = 0.171428...`

这部分生产代码、summary、Demo payload 与独立复算一致。论文主叙事中目前对基线 coverage 使用了 0.1714，但对 bounds 使用 0.2286 → 0.0057；口径是一致的，只是建议在正式论文首次出现时明确写出 denominator = 70。

## 5. Why scores are stable

独立复算确认所有可判读 Evidence 具有相同的参数相关状态：

- 相同的 prompt factor：`prompt_induced=true`
- 相同的 context factor：`context_truncated=false`
- 相同的 confidence factor：`confidence=medium`

因此可以写成：

```text
w_i(theta) = k(theta) * base_weight_i
```

其中 `k(theta)` 是所有可判读记录共同拥有的 prompt/context/reliability 缩放因子。于是：

```text
sum(w_i * score_i) / sum(w_i)
= sum(k * base_weight_i * score_i) / sum(k * base_weight_i)
= sum(base_weight_i * score_i) / sum(base_weight_i)
```

只要 `k(theta) > 0`，ABL、HOT、Gap 的归一化结果就保持不变；但 `sum(w_i)` 与 coverage 会下降。当 `lambda_prompt=1` 时 `k(theta)=0`，分母为 0，必须返回 `NO_EFFECTIVE_EVIDENCE`，三个分数为 undefined，不是 0。

这不是“模型神奇稳定”，而是当前数据支持结构产生的公共缩放效应。

## 6. Figure 2–5 review

### Figure 2

图中四个联合结构的计数与原始重算一致：可判读 Evidence 只出现在 prompt=true、context=false、confidence=medium、actor=ai 的格子。图自身写明 zero cells shown as 0；这表示 cell count 为 0，不表示模型指标被填成 0。没有发现数值错误。

### Figure 3

图实际绘制的是 `lambda_prompt` 与 `effective coverage` 的单条曲线，数据来自 21 个 prompt 条件、context=0、r_medium=0.75。曲线端点与独立复算一致：0.171428... 到 0。没有发现数值错误。

### Figure 4

已修复并重新生成：图现在直接绘制 normalized Score 稳定红线与 Evidence Support（effective coverage）下降蓝线；横轴明确为 `lambda_prompt`，副标题注明固定 `lambda_context=0.00` 与 `r_medium=0.75`，右轴明确 coverage 分母为全部 70 条 development records。图下注明稳定来自当前 16 条可判读 Evidence 的公共缩放结构，不是因果效应；`lambda_prompt=1` 时 support 归零并进入 `NO_EFFECTIVE_EVIDENCE`。

### Figure 5

这是流程图，不承载数值。流程明确显示当前 development result 在 formal AIV 之前停止。没有发现数字或状态错误。

## 7. Demo payload consistency

Demo payload 与独立复算一致的项目包括：

- records = 70
- readable_evidence = 16
- readable prompt true = 16
- baseline ABL = 3.5625
- baseline HOT = 0.375
- baseline Gap = 1.125
- baseline effective weight = 12.0
- baseline coverage = 12/70 = 0.171428...
- bounds weight = 0.4–16.0
- bounds coverage = 0.005714...–0.228571...
- zero-weight condition = `NO_EFFECTIVE_EVIDENCE`
- `annotation_source = AI_PROVISIONAL`
- `annotation_status = DEVELOPMENT_ONLY`
- `source_type = AI_PROVISIONAL`
- `formal_gate_eligible = false`

Demo payload 中的 stress test `E_strict_medium_scaffold` 会得到 ABL=3.75、Gap=0.375，因为它是过滤子集压力测试，不是主 bounds 网格的结果；不应与主结论混写。Payload 将其放在 `stress_tests` 下，口径可区分。

## 8. Paper numeric consistency

检查了 `reports/paper/`。没有发现把 70 条 development 结果写成 140 条正式人工结果、把 AI provisional 写成 formal、把 support collapse 写成 causal effect，或把 undefined 写成 0 的核心矛盾。

当前论文数字口径与 source of truth 一致：

- 70 条 development records；
- 16 条 interpretable Evidence；
- ABL/HOT/Gap = 3.5625 / 0.375 / 1.125；
- weight = 16.0 → 0.4；
- coverage = 0.2286 → 0.0057；
- `NO_EFFECTIVE_EVIDENCE` 与 undefined 处理正确。

`paper/` 目录当前不存在，因此没有发现额外论文文件可核对。

## 9. Difference classification

- P0：0 个
- P1：0 个（Figure 4 原 P1 已修复并由提交 `2359fbf` 固化）
  - 历史问题：Figure 4 曾只画 effective coverage 且横轴为 `x`；当前 SVG 已直接画出 Score 与 Support，横轴也已修正。
- P2：1 个
  - 正式论文首次介绍 coverage 时应显式注明 denominator = 70，避免评委误以为 denominator 是 16。现有数字没有算错，属于表达清晰度问题。

## 10. Model changes

本次没有修改：

- Partial Identification 主公式；
- R1/R2；
- human annotations；
- frozen manual；
- Gate threshold；
- raw data；
- provisional labels；
- Demo UI；
- paper narrative 主体。

仅新增独立复算脚本和 verification artifacts。
