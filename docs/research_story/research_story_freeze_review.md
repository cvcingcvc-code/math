# Research Story Freeze Review

## Review scope

本审查只准备 Human Review 与冻结，不进入 Phase 2–7。未修改 `research_story_summary.md`、模型、参数、阈值、人工标签、实验结果、Demo UI 或论文主体。

审查快照：

- Git HEAD：`667ecf7e25226366014687aa0ff77cbd80d8df34`
- 工作区：dirty；本轮摘要仍是未跟踪文件，项目已有其他窗口的未提交/未跟踪交付物
- 人工状态：`HUMAN_R1=0/70 VALID`、`HUMAN_R2=0/70`
- Formal Gate：`NOT_RUN`；`formal_gate_eligible=false`
- AI Increment：`AI_INCREMENT_IDENTIFICATION=NOT_SUPPORTED`
- 开发输入：70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY`；16 条可判读 Evidence；54 条 `NO_EVIDENCE + UNDETERMINED`
- 当前最高证据等级：`Level 1 — descriptive / structural development evidence`

核对来源包括：`docs/research_story/research_story_summary.md`、`docs/claim_boundary.md`、`docs/model_presentation/`、`handoff/PROJECT_STATE.md`、`handoff/CURRENT_HANDOFF.md`、`handoff/MULTIPROCESS_STATE.md`、`reports/verification/core_numbers_source_of_truth.json`、`outputs/final_results.json`、baseline / robustness / external-transfer artifacts，以及现有 audit reports。

## A. 最终一句话 Research Question

> 当 AI 参与学习环境中的观测证据存在缺失、冲突或可信度差异时，如何避免把 `Raw Signal` 直接当成可信结论，并构建一个显式报告 `Evidence Reliability`、`Support/Coverage` 且能在证据不足时降权或 `ABSTAIN` 的可审查评价框架？

审查结论：**唯一。** 这是 measurement / identifiability 问题，研究对象是可观察 Student Evidence 及其支持程度；没有扩展为“AI 是否提升真实学习效果”。

## B. 最终一句话 Model Idea

> `Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision`：仅让可判读 Evidence 进入 `Raw`，按置信度、prompt 风险和上下文风险得到支持权重 `w_i`，用 `Raw×Reliability` 调整贡献，同时报告 `Σw_i` 与 `Σw_i/N`，证据不足时输出 `LOW_SUPPORT/ABSTAIN`，支持为零时输出 `NO_EFFECTIVE_EVIDENCE`。

当前冻结模型为：

```text
w_i = I(observable_i)c_i(1−λ_prompt p_i)(1−λ_context t_i)
Adjusted_i = Raw_i × w_i
Support = Σ_i w_i
C_eff = Σ_i w_i / N,  N = 70 development records
```

`Reliability` 是当前开发假设下的支持权重，不是校准概率、因果系数或真实能力估计。

## C. 当前可说的核心结论

### DEVELOPMENT-SLICE CONCLUSION — Formal Gate 前不得升级

> 在当前 70 条 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 记录和声明参数范围内，Reliability layer 可以把 `Raw Performance` 与 `Evidence Support` 分开：归一化 `ABL/HOT/Gap` 约为 `3.5625/0.375/1.125` 并保持稳定，而有效权重从 `16` 降到 `6`、有效覆盖从 `0.228571` 降到 `0.085714`；支持归零时模型返回 `NO_EFFECTIVE_EVIDENCE`，不把缺失证据填成 0 分。因此，**Score Stability ≠ Evidence Support Stability**。

这句话只能作为当前开发切片的 Level 1 描述性/结构性结论。它支持以下范围：

- Raw Signal 与 Evidence Support 应同时报告；
- 弱支持记录可以被降权，并进入 `LOW_SUPPORT/ABSTAIN` 语义；
- 缺失或不可判读证据可以被 fail-closed 为 `NO_EFFECTIVE_EVIDENCE`；
- 当前公式、消融、有限参数扰动和案例行为可复算。

它不支持把乘法结构称为唯一最优，也不支持准确率、预测优越性、真实能力、正式 AIV 或因果学习增益。

## D. 当前不可说的结论

以下结论在 Human Gate 完成前均不可说；其中部分即使 Gate 通过也仍需要额外 outcome / identification 设计：

- `Adjusted Score`、`Support` 或 `Coverage` 是 `AI Increment`、正式 AIV 或学习增益；
- AI 导致学生真实能力提升、长期学习效果或因果 learning gain；
- `R` 是概率、校准可靠度或学生能力估计；
- 当前结果提升了预测准确率，或 `ABSTAIN` 已被证明提高安全性/准确率；
- 当前 70 条 Gate 样本可外推为 140 条正式人工标注结果或学生排名；
- 当前模型、ML Challenger、Alternative Formulation 或 Finance Shadow 已经选出普适赢家；
- BTC/Finance 结果证明教育泛化、跨领域普适性或交易优势；
- 没有合法配对的 `Outcome_AI` 与 `Outcome_baseline` 时，存在可识别的 `Delta_raw` 或 `Delta_reliable`。

## E. 五条验证分别证明什么

五条线是对同一个核心结论的互补攻击路径，不是五个平行研究：

| Validation | 它攻击的质疑 | 当前证明内容 | 证据边界 |
|---|---|---|---|
| **Baseline Comparison** | “Reliability 层没有必要。” | Raw-only、线性和规则基线能给出 Raw 数值，但不能表达同样高 Raw 背后的支持质量差异；主模型把当前 16 条可判读记录保留为 `LOW_SUPPORT`，有效权重从 `16` 计为 `6`。 | 结构差异，不是模型胜负、准确率或乘法形式必需性的证明。当前简单线性结果存在于 baseline artifacts，但 `MULTIPROCESS_STATE` 仍把 Simple Linear 标为 pending，需后续 registry 统一状态。 |
| **Ablation** | “Reliability / 关键组件只是装饰。” | `M0→M1→M2→M3` 有效权重为 `16→12→6→6`；当前归一化分数不变，prompt 模块产生主要支持下降，context 在可判读记录中无变异。 | 说明组件改变 support accounting；不证明独立因果作用、预测准确率或 context 效应。 |
| **Sensitivity / Robustness** | “结果只是某个参数点调出来的。” | 已声明的 `±10%/±20%` 单变量扰动产生 `0` 个 decision-state flips；normalized score 保持，support 变化；学生 ranking 为 `NOT_APPLICABLE`。 | 只是有限参数网格的局部结构稳定性，不是置信区间或全局稳健性；context 平坦是缺少变异，不能解释为 context 无作用。 |
| **Counterexample / Failure** | “真正困难样本下框架没有用。” | P108 为 `Raw=L6`、`R=.375`、adjusted contribution `2.25`，被标为 `LOW_SUPPORT` 并可进入 `ABSTAIN`；P072/P035 证据不可判读，返回 `NO_EFFECTIVE_EVIDENCE`，不填 0。 | 这是结构性案例；没有 true outcome，不能判断预测正确/错误，也不能声称 abstention 已改善准确率。 |
| **External Transfer** | “模型只是对当前教育数据硬写。” | BTC 历史/受控信息缺失场景复用 `Raw→Reliability→Adjusted→ACCEPT/ABSTAIN`；A/B 有有限结构支持，C 提供失败边界，information-missing Gate 1/2 支持而 Gate 3 不支持。 | 仅 `EXTERNAL_TRANSFER / DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`；Finance 只作 external structural demonstration，不是教育泛化、因果或交易研究。 |

统一方法句：**One research question, one core model, and five independent lines of validation.**

## F. Human Gate 完成后哪些结果必须重新计算

先按冻结协议完成同一标注者 R1、间隔至少 24 小时后的独立 R2，再运行 Gate。Human Gate 只提供标注 test-retest / Gate 证据，不自动产生 AI 因果增量。

如果 Gate PASS，必须用真实 Human 输入替换开发输入并重新计算：

1. R1/R2 字段完整性、标签合法性、test-retest reliability、预注册阈值判定和 Gate 状态；
2. 70 条 Gate 记录的 `Student Evidence` 可判读数、`NO_EVIDENCE`、`UNDETERMINED`、冲突/低信任/上下文缺失分布；
3. 每条记录的 `Raw Signal`、`Reliability`、`Adjusted`、`LOW_SUPPORT`、`ABSTAIN`、`NO_EFFECTIVE_EVIDENCE`；
4. 汇总 `ABL/HOT/Gap`、`Support=Σw_i`、`Coverage=Σw_i/70`、有效证据分母和状态计数；
5. `M0–M3` Ablation、参数 Sensitivity/Robustness、零支持 undefined cells 和可适用性标记；
6. Counterexample / Failure Case 的人工标签解释。没有真实 outcome 时，仍不得写成预测准确/错误；
7. 依赖这些数字的 F1–F6 图表、Paper 结果表、Demo case cards 和统一 registry payload；
8. 仅在另有合法配对 `Outcome_AI` / `Outcome_baseline`、独立 outcome 与预注册识别设计时，才重新评估 `Delta_raw`、正式 AI Increment 或 causal learning gain。

如果 Gate FAIL，必须只报告 Gate 结果，保留 `DEVELOPMENT_ONLY`，不得把上述开发数字升级为 Formal。

## G. 哪些论文 / Demo / 图表字段后续必须统一替换

后续 Evidence Integration 阶段必须从单一事实源统一替换以下字段，不能让 Paper、Demo、Figures 各自保留一套数字：

| 字段组 | 必须统一的字段 |
|---|---|
| **Evidence / Formal status** | `annotation_source`、`annotation_status`、`HUMAN_R1`、`HUMAN_R2`、`human_gate_status`、`formal_gate_status`、`formal_gate_eligible`、`Evidence Level`、`AI_INCREMENT_IDENTIFICATION` |
| **Sample and denominator** | `N`、readable Evidence、`NO_EVIDENCE`、`UNDETERMINED`、`NO_EFFECTIVE_EVIDENCE`、`Support`、`effective_weight`、`Coverage` 及其分母（当前为 70） |
| **Core model outputs** | Raw/Adjusted `ABL`、`HOT`、Task/Evidence Gap、每行 `Raw/R/Adjusted/Decision`、`ACCEPT`/`ABSTAIN`/`LOW_SUPPORT` 计数 |
| **Validation outputs** | Baseline comparison role、`M0→M3` support、敏感性 state flips、ranking `NOT_APPLICABLE`、counterexample outcome availability、External Transfer scope and failure boundary |
| **Paper fields** | 摘要、Research Question、Main Conclusion、五条 Validation 标题与结论句、Limitations、Conclusion、首次 Coverage 说明（`N=70`）；所有开发数字保留 `AI_PROVISIONAL / DEVELOPMENT_ONLY` 标签 |
| **Demo fields** | Screen 1–6 的同一 Research Question、模型链、五条攻击模块、交互案例的 `Raw/R/Adjusted/Decision`、Claim Boundary 状态卡；所有数字从统一 payload 读取 |
| **Figure fields** | 图题、坐标轴、注释、caption/footer 中的 `DEVELOPMENT_ONLY`、`Formal Gate NOT_RUN`、coverage 分母、`NO_EFFECTIVE_EVIDENCE` 语义、External Transfer 限定 |
| **Future registry / consistency fields** | `reports/integration/experiment_registry.json`、`reports/demo/data/model_summary.json`、`validation_summary.json`、`case_studies.json`、`evidence_status.json`、`reports/integration/final_research_consistency.md` 中的同一状态、数字、source path 和 evidence level |

## Conflicts found; record only, do not repair in this round

1. **严格标签缺失：** 摘要写了 `AI_PROVISIONAL / DEVELOPMENT_ONLY / Evidence Level 1`，也写了“当前开发切片”，但没有字面量 `DEVELOPMENT-SLICE CONCLUSION`。建议 Human Review 后，在摘要冻结版本中把核心句显式标成该标签，并保留“Formal Human Gate 前不得升级”的句子。本轮不改摘要。
2. **Audit 状态未闭环：** `handoff/MULTIPROCESS_STATE.md` 仍显示 `AUDIT=RUNNING`、`DEMO_UI=REVIEW_REQUIRED`，并保留 Demo/unified artifact 的历史 M0/M1 raw 口径、失败案例 null 值和旧 receipt 冲突。最新 handoff / `outputs/final_results.json` 已记录修复后的主链，但尚无本轮新的最终 Audit 结论。建议以单一最终 payload 完成一次 re-audit 后再做交付冻结。
3. **Baseline 登记状态不一致：** `experiments/model_tournament/baselines/baseline_results.json` 与 `baseline_evidence_matrix.md` 已有 Simple Linear 结果；`MULTIPROCESS_STATE` 的风险栏仍写“final matrix still marks Simple Linear as PENDING”。建议后续 registry 明确“artifact exists / claim status pending”的区别，避免把 Baseline 线写成已完成的 formal comparison。
4. **旧 handoff 时间点：** `CURRENT_HANDOFF.md` 保留 R1 曾有 1/70 非法填写的 checkpoint，而 `PROJECT_STATE.md`、Gate report 和实际当前正式状态为 `0/70 VALID`。建议后续统一以当前有效状态 `0/70 VALID` 表达，并保留非法 checkpoint 只作为审计历史。
5. **验证 PASS 范围有限：** `development_submission_consistency.json=PASS` 只证明该检查器覆盖的开发 artifact 一致，不等于整个工作区、所有旧副本和最终封装已完成一致性冻结。建议不要将该 PASS 扩写为全项目 Formal/Submission closure。

## Final freeze decision

```text
RESEARCH_STORY_FREEZE = NOT_READY
```

阻止冻结的问题：

- 摘要没有按要求显式写出 `DEVELOPMENT-SLICE CONCLUSION`，核心句的开发切片边界目前是语义表达而非明确标签；
- Audit/交付状态仍有未闭环的历史副本与 registry 冲突，尚未形成单一最终一致性凭证。

研究方向、唯一 Research Question、主模型链、五条验证定位、ML Challenger 边界、Finance external structural demonstration 边界，以及 `Outcome_AI / Outcome_baseline` 对 AI Increment / causal learning gain 的限制均已通过本轮审查。Human Review 可针对上述两个阻塞点确认后，再决定是否将冻结状态提升为 `READY_FOR_HUMAN_CONFIRMATION`。
