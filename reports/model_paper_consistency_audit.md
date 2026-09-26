# Model–Paper Consistency Audit

日期：2026-09-26。范围：`docs/metric_dictionary.md`、`docs/claim_boundary.md`、`docs/model_presentation/`、`reports/demo/index.html`、`paper/submission_candidate.md`、`docs/model_presentation/judge_defense_qa.md`。

## 已一致

- 主链统一为 Observed Student Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision。
- 公式统一为 `w_i=I(observable_i)c_i(1−λ_prompt p_i)(1−λ_context t_i)` 与 `Adjusted_i=Raw_i×w_i`。
- Coverage 明确区分行覆盖与有效覆盖；当前 `C_eff=Σw_i/N` 的开发分母为 70。
- `Adjusted Score` 与 `Delta_raw` / `Delta_reliable` 分离；AI Increment 在所有材料中为 `NOT_SUPPORTED`。
- Demo 已移除金融场景，按 Research Question → Raw 不足 → Pipeline → Scenario → Raw/Reliability/Adjusted → Support/Coverage → Decision → Failure → Validation → Boundary 展示。
- 真实案例 P108、P105、P072、P035 的 Raw、Reliability、Adjusted、Decision 与 `outputs/final_results.json` 一致，并标记 `DEVELOPMENT EXAMPLE`。
- `c_i`、`lambda_prompt`、`lambda_context` 在组件表、答辩稿和论文中均标为弱依据组件，不包装成概率。

## 已修复

- `reports/demo/index.html` 原有 BTC/金融术语、未来 outcome 与交易 Gate 文案已替换为教育证据模型。
- 新增 `judge_3min_story.md`、`final_model_overview.md`、`model_component_table.md`、`validation_story.md`、`judge_defense_qa.md`、`judge_3min_script.md`。
- 旧 `model_overview.md` 改为 canonical pointer，避免两套主图定义。
- 论文候选末尾补充统一词汇、Coverage 分母和 AI Increment 识别边界。

## 仍存在风险

- 论文中的 External Transfer Validation 仍保留为附录级结构迁移材料；它不属于教育主模型验证，答辩时必须明确这一身份。
- 论文中现有开发数字仍来自 AI_PROVISIONAL；不能在 Formal Gate 前改写为正式指标。
- Formal Gate 尚未运行，无法声称 Accuracy、校准概率或因果学习增益。

## Formal Gate 后必须更新

替换所有 `DEVELOPMENT_ONLY` 数字、Development Example 标签、Gate 状态、Formal 指标、论文结果段和 Figure/Demo 状态；同时保留 AI Increment 只有在存在合法配对 outcome 时才可识别的条件。

## 结论

- Demo：**PASS**（主链、案例、边界已统一）。
- Paper：**PARTIAL**（核心模型口径一致；Formal 数字和附录迁移材料仍需 Gate 后复核）。
- Judge Defense：**PASS**（22 个问题均遵守 Claim Boundary；Human Gate 未完成明确标出）。
