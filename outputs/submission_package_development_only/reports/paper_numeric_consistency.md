# Paper numeric consistency check

## Scope

核对范围：

- `reports/paper/*.md`
- `paper/` 目录（当前不存在）
- 独立 source of truth：`reports/verification/core_numbers_source_of_truth.json`

目标数字：`16`、`70`、`693`、`33`、`3.5625`、`0.375`、`1.125`、`16.0`、`0.4`、`0.2286`、`0.0057`。

## Findings

| 检查项 | 结果 |
|---|---|
| 70 是否被写成正式人工样本 | 未发现 |
| 16 是否被写成正式人工 Evidence | 未发现；均处于 AI provisional / development-only 语境 |
| 693 是否与参数网格一致 | 一致，21 × 11 × 3 |
| 33 是否被写成 defined cells | 未发现；被写为 undefined cells |
| ABL/HOT/Gap 是否与复算一致 | 一致 |
| 16.0 → 0.4 是否与复算一致 | 一致，指 effective evidence weight 的最大值到最小非零值 |
| 0.2286 → 0.0057 是否与复算一致 | 一致，指 effective coverage 的最大值到最小非零值 |
| coverage denominator 是否明确 | 主叙事说明为 total records；建议正式论文首次出现时显式写 denominator = 70 |
| undefined 是否写成 0 | 未发现 |
| development 是否写成 formal | 未发现 |
| support collapse 是否写成 causal effect | 未发现；材料明确禁止该解释 |
| `paper/` 目录是否有额外待核对稿件 | 没有，目录不存在 |

## 文件级结论

- `reports/paper/competition_paper_narrative_draft.md`：数字与 source of truth 一致；状态边界完整。
- `reports/paper/judge_story_3min.md`：数字与 source of truth 一致；使用 `DEVELOPMENT_ONLY / AI_PROVISIONAL` 限定。
- `reports/paper/elevator_pitch_30s.md`：数字与 source of truth 一致；明确不是正式 AIV / 因果结论。
- `reports/paper/core_figures_interpretation.md`：已正确说明 Figure 4 的 SVG 只直接展示 effective coverage，不能说同时画了 Score。
- `reports/paper/paper_ready_development_draft.md`：数字与 source of truth 一致。
- `reports/paper/method_results_skeleton.md`：作为骨架文件，没有引入冲突数字。

## Remaining presentation note

P2：正式论文第一次给出 coverage 时，建议写成：

> effective coverage = effective evidence weight / 70 development records。

当前不是数字错误，而是防止评委把 16 条可判读 Evidence 误认为 coverage 分母的表达优化。
