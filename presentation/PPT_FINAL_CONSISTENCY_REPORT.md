# PPT_FINAL_CONSISTENCY_REPORT

状态：`READY_FOR_REHEARSAL`

## 五方一致性结论

| 对象 | 核验内容 | 结果 |
|---|---|---|
| PAPER | 研究问题、模型链路、结论、限制与 Claim 边界 | PASS |
| CLAIM LOCK | `FINAL_CLAIM_LOCK.md` 中的状态、负结果和不可声称项 | PASS |
| FIGURES | F1–F6 使用冻结 SVG，未重绘核心数字 | PASS |
| PPT | 10 页结构、数字、状态标签、负结果和页码 | PASS |
| DEMO | 四锚点路线、P108 交互、离线 fallback | PASS |

## 数字核对

- Development slice：`N=70`
- 可判读：`16`
- `NO_EVIDENCE=19`、`UNDETERMINED=35`、`NO_EFFECTIVE_EVIDENCE=54`
- ABL / HOT / Gap：`3.5625 / 0.375 / 1.125`
- Effective weight：`16 → 12 → 6 → 6`
- Coverage：`0.228571 → 0.171429 → 0.085714 → 0.085714`
- Robustness：`693=21×11×3`；`660 defined / 33 undefined`
- 参数扰动：`±10% / ±20% → 0 decision-state flips`
- P108：`L6 / R=0.375 / Adjusted=2.25 / LOW_SUPPORT / ABSTAIN`
- P105：`L2 / R=0.375 / Adjusted=0.75 / LOW_SUPPORT`
- P072/P035：`NO_EFFECTIVE_EVIDENCE`，Adjusted=null
- ML：`LogReg≈0.876 / Tree≈0.919 / RF≈0.922`；RF 跨学期 `0.588`
- BTC：`n=1698`；Gate1/2 `SUPPORTED`；Gate3 `NOT SUPPORTED`；risk-coverage improvement=`false`
- Human Gate：`R1=0/70`、`R2=0/70`、Formal Gate=`NOT_RUN`

## Claim 核对

- 唯一主结论：`Score Stability ≠ Evidence Support Stability.`
- 未声称 AI 提高学习效果、causal learning gain、准确率提升、交易优势或通用泛化。
- 未声称 ML winner；保留 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`。
- External Transfer 仅表述为 `STRUCTURAL ONLY`。
- `ABSTAIN` 被定义为合理输出；`NO_EFFECTIVE_EVIDENCE` 不被写成 0 分。

## 冻结边界

- 未修改 `paper/` canonical source。
- 未修改 `data/`、`outputs/final_results.json`、`reports/visual_evidence/final/`。
- 未修改正式 Demo `reports/demo/index.html`。
- 新 PPT 和现场材料全部位于 `presentation/`。
- `COMMIT=NO`；`PUSH=NO`。

## 风险与处理

- PPT 工具批量命令的包装层退出码回显不稳定；已分段逐页执行 lint/upsert，10 个页面源均已写入，PPTX 文件已生成。
- 已知 Demo P2 缺陷沿用冻结凭证记录，不在本阶段修复。
- 结论级别保持 `descriptive / structural`、`DEVELOPMENT_ONLY`。

## 最终状态

`P0=0`；未发现阻塞性 `P1`；`NEXT=READY_FOR_REHEARSAL`。
