# FINAL_ALIGNMENT_MATRIX

> 最终项目收口五方对表。仅记录既有冻结 artifact 的一致性，不新增研究结论。

## 结论

```text
CORE_IDEA_PAPER = PASS
CORE_IDEA_DEMO = PASS
CORE_IDEA_PPT = PASS
NUMBER_DRIFT = 0
CLAIM_DRIFT = 0
```

## 核心研究想法

| 核心口径 | Paper | Demo | PPT | F1-F6 | 判定 |
|---|---|---|---|---|---|
| Raw Signal 不应直接解释为可靠结论 | 有，Problem Formulation / Conclusion | 有，首屏和 Research Question | 有，Problem / Model 页 | F1/F2 | PASS |
| Observed Evidence → Raw Signal → Reliability → Adjusted → Support/Coverage → Decision | 有 | 有，Core Model 流程 | 有，Model 流程 | F1 | PASS |
| `ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE` | 有 | 有，Decision cards | 有 | F1/F5 | PASS |
| High Raw ≠ High Evidence Support | 有，P108 | 有，Failure Case | 有 | F2/F5 | PASS |
| Missing Evidence ≠ Zero Performance | 有，P072/P035 | 有，null 不填 0 | 有 | F2/F5 | PASS |
| Score Stability ≠ Evidence Support Stability | 唯一 Main Conclusion | Core Finding | 核心页明确突出 | F3/F4/F5 | PASS |
| measurement / identifiability 而非 AI 因果增量 | 有 | 有 | 有 | — | PASS |

## 数字与语义

| 指标 | Canonical 含义 | Paper | Demo | PPT | 判定 |
|---|---|---|---|---|---|
| `N=70` | development slice | ✓ | ✓ | ✓ | PASS |
| `16` | 可判读 Evidence | ✓ | ✓ | ✓ | PASS |
| `54` | NO_EFFECTIVE_EVIDENCE = 19 + 35 | ✓ | ✓ | ✓ | PASS |
| `3.5625 / 0.375 / 1.125` | ABL / HOT / aggregate Gap | ✓ | ✓ | ✓ | PASS |
| `2.25` | P108 单记录 Adjusted contribution = 6 × 0.375 | ✓ | ✓ | ✓ | PASS |
| `16 → 12 → 6 → 6` | Ablation effective weight | ✓ | ✓ | ✓ | PASS |
| `0.228571 → 0.171429 → 0.085714 → 0.085714` | Coverage，分母 N=70 | ✓ | ✓ | ✓ | PASS |
| `693 / 660 / 33` | parameter grid / defined / undefined | ✓ | ✓ | ✓ | PASS |
| P108/P105/P072/P035 | frozen counterexamples | ✓ | ✓ | ✓ | PASS |
| ML | only `INSUFFICIENT_FOR_STRONG_ML_CLAIM` | ✓ | ✓ | ✓ | PASS |
| BTC `n=1698` | structural transfer only | ✓ | ✓ | ✓ | PASS |
| Human Gate | R1=0/70, R2=0/70, NOT_RUN | ✓ | ✓ | ✓ | PASS |
| AI Increment | NOT_SUPPORTED | ✓ | ✓ | ✓ | PASS |

## 交叉一致性

```text
PAPER ↔ DEMO   = PASS
PAPER ↔ PPT    = PASS
PAPER ↔ FIGURES = PASS
DEMO ↔ PPT     = PASS
```

## 交付说明

旧的 10 页 `outputs/education_ai_evidence_roadshow_final.pptx` 未作为最终路演源继续使用；当前最终路演源为：

`presentation/final_defense_ppt/教育AI证据可靠性_现场答辩终稿.pptx`

该终稿为 19 页，实际文本包含全部核心锚点：Main Conclusion、54、ABSTAIN、NO_EFFECTIVE_EVIDENCE、NOT_RUN、NOT_SUPPORTED、BTC n=1698、ML Claim Boundary。

Demo 已冻结；已知 `/favicon.ico` 404 记录为非阻塞 P2，不修复、不重新晋升。
