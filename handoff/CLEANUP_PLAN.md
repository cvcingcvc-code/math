# CLEANUP PLAN

> 本文件是清理**计划**，不执行删除。每个候选项标注路径/用途/是否被引用/是否 canonical/建议/删除风险。
> 原则：不破坏论文引用、实验复现与证据链；历史实验与原始证据保留。

## 一、重复 / 过期 PPT（outputs/）

| 路径 | 用途 | 是否被引用 | canonical? | 建议 | 风险 |
|---|---|---|---|---|---|
| `outputs/education_ai_evidence_roadshow_final.pptx` | 最终路演 PPT（10 页，视觉冻结） | 是（README/PROJECT_STATE） | **是** | KEEP | — |
| `outputs/education_ai_evidence_roadshow_v1.pptx` | 旧版 v1 | 否 | 否 | ARCHIVE | 无（未被引用） |
| `outputs/education_ai_evidence_roadshow_v1_final.pptx` | v1 定稿（与 v1 同大小） | 否 | 否 | ARCHIVE | 无 |
| `outputs/education_ai_evidence_roadshow_v2_editorial.pptx` | v2 editorial | 否 | 否 | ARCHIVE | 无 |
| `outputs/education_ai_evidence_roadshow_v2_editorial_final.pptx` | v2 editorial 定稿（与 final 同大小） | 否 | 否 | ARCHIVE | 无 |
| `outputs/education_ai_evidence_roadshow_v*.inspect.ndjson`（×2） | PPT 校验导出 | 否 | 否 | DELETE（派生校验产物） | 无 |
| `outputs/_render_v1/` `_render_v2/` + `*_montage.png` | 渲染缩略图 | 否 | 否 | ARCHIVE | 无 |
| `outputs/demo_ui_reference/` | Demo UI 参考 | 否 | 否 | ARCHIVE | 无 |

## 二、论文候选稿（paper/）

| 路径 | 用途 | canonical? | 建议 | 风险 |
|---|---|---|---|---|
| `paper/development_submission_candidate.md` | **canonical 开发版论文** | **是** | KEEP | — |
| `paper/PAPER_EVIDENCE_TRACE.md` | 证据溯源 | 是 | KEEP | — |
| `paper/PAPER_NUMBER_LOCK.md` | 数字锁 | 是 | KEEP | — |
| `paper/LITERATURE_CITATION_MAP.md` | 文献映射 | 是 | KEEP | — |
| `paper/submission_candidate.md` | 旧「正式候选」稿（Formal Gate 未完成） | 否（历史候选） | ARCHIVE | 若 README/论文指向它需改指 development 稿 |
| `paper/submission_candidate.html/.pdf` | 上述候选的渲染件 | 否 | KEEP（渲染产物） | 无 |

## 三、临时/杂项

| 路径 | 用途 | 建议 | 风险 |
|---|---|---|---|
| `work/`（约 40 个 probe/patch/临时脚本） | 开发 scratch | KEEP（已被 .gitignore 排除，不入库） | 无 |
| `.codex-finalizer/`（2 个 PPT validation.json） | PPT 校验收据 | ARCHIVE（保留为审计凭证） | 无 |
| `__pycache__/`（多处） | Python 缓存 | 已被 .gitignore 排除 | 无 |

## 四、无需处理（canonical，保留）

`data/`（processed + annotations）、`src/`、`scripts/project_manager.py`、`reports/development|verification|robustness|perturbation|external_transfer|failure_cases|visual_evidence/final`、`experiments/model_tournament|transfer_finance`、`docs/`、`validation/`、`research/`、`variable/`、`slides/`、`handoff/`、`run_all.py`、`requirements.txt`。

## 五、执行策略

- 本轮**不删除、不移动**任何文件（遵循「先出计划、确认后再处理」）。
- 若后续执行：ARCHIVE 项移入 `archive/`（或标记 `LEGACY`），DELETE 项仅限派生校验产物（inspect.ndjson）。
- 首要动作是**收口 commit + push**，让 GitHub 首次看到完整、结构清楚的仓库；清理可留待人工确认后再做。
