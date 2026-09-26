# Final submission checklist

更新时间：2026-09-26。当前包是**开发版内部评审 / 演示包**，不代表 Formal Gate 已通过。

## 已完成

- [x] 提交目录：`outputs/submission_package_development_only/`
- [x] MANIFEST：37 个文件，逐项 SHA-256 校验通过
- [x] 复现入口：`run_all.py`，预期 6 步、32 项一致性检查通过
- [x] 环境与说明：`requirements.txt`、`README.md`、`SUBMISSION_PACKAGE_README.md`、`FORMAL_GATE_SWITCH.md`
- [x] 论文候选：PDF/HTML 已放入包内，明确 `DEVELOPMENT_ONLY` 和 `AI_PROVISIONAL`
- [x] 路演 PPT：10 页；当前规范命名候选为 `outputs/education_ai_evidence_roadshow_final.pptx`，包内副本 SHA-256 一致
- [x] PPT 结构检查：10 页、16:9、无结构或几何布局错误；每页已渲染检查
- [x] Demo：`demo/index.html`、`demo_payload.json`、4 张核心图；根目录和包内脚本语法检查通过
- [x] Demo 状态：支持 Raw baseline、Adjusted Score、λ/r 敏感性、Counterexamples、`NO_EFFECTIVE_EVIDENCE`
- [x] 核心数字统一：70 / 16 / 19 / 35；ABL/HOT/Gap = 3.5625 / 0.375 / 1.125；effective weight 16→6；coverage 0.228571→0.085714（分母 70）

补充：包内同时保留 v1 与 editorial v2 两个已验收版本，均为 10 页；提交前按队号规则选定一个最终文件名，避免重复递交。

## 提交前必须补齐

- [ ] 队号与最终命名规则
- [ ] 真实人工 R1、至少间隔 24 小时的 R2，以及 Gate 报告
- [ ] Gate PASS 后的正式结果（若 Gate FAIL，保留开发边界并缩小结论）
- [ ] 队号命名的最终论文、PPT、结果 CSV 和 ZIP
- [ ] 最终提交渠道、截止时间和页数规则的现场核对

## 当前禁止替代

- 不得用 AI_PROVISIONAL 替代人工 R1/R2
- 不得生成 Formal AIV 或学生排名
- 不得把开发版 PPT、Demo 或论文候选稿描述为正式验证结果
