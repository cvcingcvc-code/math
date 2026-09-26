# FINAL DELIVERY HANDOFF

> 状态：`FINAL_DELIVERY_CONVERGENCE`（收敛完成，等待提交）。
> 生成时间：2026-09-27（提交日）。
> 本文件只记录最终交付口径，不新增研究结论、不修改任何模型/数字/标签。
> 唯一文字最高依据：`paper/paper_v2_submission_candidate.md`（已冻结）。
> 唯一数字最高依据：`outputs/final_results.json` + `paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字）。

---

## 0. 最终状态

```
PAPER                = FROZEN          (paper_v2_submission_candidate.md, P0=0/P1=0/P2=4)
DEMO                 = PROMOTED        (中文版已写入 reports/demo/index.html；尚未 commit)
PPT                  = FROZEN          (education_ai_evidence_roadshow_final.pptx, 10 页)
CLAIM_DRIFT          = 0               (论文 ↔ Demo ↔ PPT 逐项核对一致)
NUMBER_DRIFT         = 0               (18 组锁定数字三载体一致)
REHEARSAL            = PASS            (论文终审 PASS / Demo 评审 PASS / PPT 结构检查 PASS)
SUBMISSION_PACKAGE   = VERIFIED        (development_only 包已刷新，MANIFEST 41/41 PASS)
FORMAL_HUMAN_GATE    = PENDING         (R1=0/70, R2=0/70, NOT_RUN)
```

---

## 1. 最终文件路径

| 角色 | 路径 |
|---|---|
| 论文 canonical（唯一提交文字） | `paper/paper_v2_submission_candidate.md` |
| 论文最终 PDF | `paper/final/数学建模论文_最终排版版_2026-09-27.pdf` |
| 论文可编辑 DOCX | `paper/final/数学建模论文_可编辑版_2026-09-27.docx` |
| 正式 Demo（中文版，已晋升） | `reports/demo/index.html` |
| Demo 服务脚本（离线可跑） | `reports/demo/serve_demo.py` |
| Demo 数据 payload | `reports/demo/demo_payload.json` |
| 6 张最终图 | `reports/visual_evidence/final/F1–F6_*.svg` |
| 路演 PPT（最终版） | `outputs/education_ai_evidence_roadshow_final.pptx` |
| 开发版提交包（已刷新并校验） | `outputs/submission_package_development_only/`（41 项 manifest，逐项 PASS） |
| 统一数字事实源 | `outputs/final_results.json` |
| 数字锁 | `paper/PAPER_NUMBER_LOCK.md` |
| 声明口径锁 | `paper/FINAL_CLAIM_LOCK.md` |

---

## 2. 文件 hash（SHA-256）

| 文件 | SHA-256 |
|---|---|
| `paper/paper_v2_submission_candidate.md` | `8b478b7e5a1f7cfa7a1176ac97349c26518c4782f29cfcb78ac5f13e3bd47a15` |
| `paper/final/数学建模论文_最终排版版_2026-09-27.pdf` | `9910bb0f87aceedd17b9ad8ea9679b95dc82df188a97c0f18d39ff647167c391` |
| `paper/final/数学建模论文_可编辑版_2026-09-27.docx` | `6f16362406d4328799cf868b91a1eb7376beb40882880e891c355e78181bdd8f` |
| `reports/demo/index.html` | `d15d124c256df7cc7d1d9cc6f12a458455ca30df183c4114b16c842b415a4632` |
| `reports/demo/demo_payload.json` | `fd9dd49f7a6813225cbe292335b86f1aa9511cf3c662c8c6fb00c2c2237922e2` |
| `outputs/final_results.json` | `47ca1c7228ad9bd6a1777434dd693776f27345f04c2c543237d781e1bcb1723e` |
| `outputs/education_ai_evidence_roadshow_final.pptx` | `bfe2d6453701b92e8608b3e11bb267b5c950b82d7b80c04b4b368f96be219a16` |

> PDF 完整性：`%PDF-1.4`、1.8 MB、含 63 个图片引用、EOF 正常，6 张图矢量嵌入，可正常打开。
> Demo 完整性：正式版中文版 510 行，6/6 图可解析，按钮确定性复算，外部请求 0（离线自包含）；提交包内 Demo 已改为引用包内 `development/F1–F6`，脱离仓库打开仍可显示。

---

## 3. Git HEAD

- Branch：`master`
- HEAD：`27c0c08`（当前真实 Git HEAD；本地短 SHA 已核验）
- 工作区（当前核查时点）：
  - ` M reports/demo/index.html`（Demo 中文晋升，**尚未 commit**）
  - ` M outputs/submission_package_development_only/MANIFEST.sha256.json`
  - ` M outputs/submission_package_development_only/demo/index.html`
  - ` M outputs/submission_package_development_only/paper/submission_candidate.md`
  - ` M outputs/submission_package_development_only/paper/submission_candidate.pdf`
  - 删除旧版包内 4 张 core figure、旧 HTML、旧 v1 PPT；新增 F1–F6、最终论文 Markdown/PDF/DOCX、最终 PPT
  - 未跟踪：`FINAL_DELIVERY_HANDOFF.md`、`reports/demo/DEMO_FREEZE_RECEIPT.md`、`presentation/` 及上述新增提交包文件
- 提交前必须 `git fetch` + `git ls-remote` 核实远端指向（本地无 `origin/master` 跟踪 ref，历史存在「已推 a4429af」与「reset 回 27afa49」的潜在不一致）。

---

## 4. 可声称结论（以冻结论文 + CLAIM_LOCK 为准）

- **Research Question**：观测证据存在缺失、冲突或可信度差异时，如何避免把 Raw Signal 直接当成可靠结论，并构建可显式报告 Evidence Reliability 与 Support/Coverage、证据不足时允许 ABSTAIN 的评价框架。
- **Main Conclusion**：**Score Stability ≠ Evidence Support Stability**（分数稳定 ≠ 证据支持稳定）。级别：`descriptive / structural`，`DEVELOPMENT_ONLY`。
- 主链路：`Observed Evidence → Raw Signal → Reliability → Adjusted Evaluation → Support / Coverage → ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE`。
- Raw 与 Reliability 是两个独立层；`w_i = I(observable_i)·c_i·(1−λ_prompt·p_i)·(1−λ_context·t_i)`。
- Support / Coverage 与 Score 分开报告：`S=Σw_i`、`C_eff=Σw_i/N`（分母 N=70）。
- 核心数字：N=140（全量）→ N=70（development slice）→ 16 可判读 → 54 `NO_EFFECTIVE_EVIDENCE`（=19+35，非零分）；ABL/HOT/Gap = 3.5625/0.375/1.125；ablation 16→12→6→6；coverage 0.228571→0.085714。
- 五类验证服务主命题：Baseline / Ablation / Sensitivity(693 格) / Failure(P108) / External(BTC n=1698, Gate3 NOT SUPPORTED)。

---

## 5. 不可声称结论（禁止，且三载体已一致不含）

- ❌ FORMAL_SUPPORTED / 正式验证通过
- ❌ AI 提高学习效果 / 导致成绩提升 / causal learning gain / AI Increment 已识别
- ❌ ML winner / ML 被击败 / 手工规则优于 ML
- ❌ accuracy 提升 / 准确率提升
- ❌ 交易优势 / 教育泛化 / universal generalization
- ❌ R 是校准概率（c_i/λ 为假设参数，未外部校准）
- ❌ Kappa / Alpha 正式一致性（Human Gate 未运行；标注设计为 single-annotator test-retest，非 inter-rater）

---

## 6. 已知限制（必须保留）

- **GAP-1**：Human Formal Gate 未完成（R1=0/70 VALID、R2=0/70、`NOT_RUN`、`formal_gate_eligible=false`）。
- **GAP-2**：Reliability 参数正式校准不足（`WEAKLY_JUSTIFIED_COMPONENT`）。
- **GAP-3**：`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`（无合法配对 Outcome_AI/Outcome_baseline）。
- BTC 外部迁移 Gate3 `NOT SUPPORTED`；`NO_SINGLE_DOMINANT_MODEL`；`INSUFFICIENT_FOR_STRONG_ML_CLAIM`。
- 16 条可判读记录共享同一组因子取值（prompt=true/context=false/confidence=medium/actor=ai），故每条 R=0.375（degenerate common-scaling slice）——这是「分数稳定而支持下降」的机制来源，也是样本稀疏的现实边界。

---

## 7. 提交前最后人工检查项

1. **负责人完成真实 HUMAN R1（70/70）**，保存冻结并记录完成时间与 SHA-256。
2. 满足 **R1→R2 至少 24 小时间隔**后，由负责人独立完成 **HUMAN R2（70/70）**。
3. R1/R2 齐后运行 `python src/run_s4_gate.py`（或 `python src/solo_retest_gate.py report --r1 ... --r2 ...`），产出 Gate 报告。
4. **Demo 晋升 commit 决策**：`M reports/demo/index.html` 尚未提交，需负责人确认后 `git add reports/demo/index.html` 并 commit（不要 `git add -A`）。
5. **提交包已刷新**：`outputs/submission_package_development_only/` 已同步冻结论文 Markdown/PDF/DOCX、中文晋升 Demo、最终 PPT 与 F1–F6；`MANIFEST.sha256.json` 共 41 项，逐项校验 PASS。包内 Demo 图件引用已切换为包内相对路径；包内旧 `run_all.py` 仍保留历史复现链路说明，不将其表述为脱离仓库的独立复现 PASS。
6. **队号（TEAMID）与最终命名规则**：按比赛要求统一论文/PPT/结果 CSV/ZIP 的文件名。
7. **提交渠道、截止时间、页数规则**：现场核对。
8. 现场演示：`python reports/demo/serve_demo.py 4190` 离线可跑，无需网络。

---

## 附：三载体一致性核验记录（本轮只读复验）

| 核对项 | 论文 | Demo | PPT | 结论 |
|---|---|---|---|---|
| N=70 / 16 可判读 / 54 NO_EFFECTIVE_EVIDENCE | ✓ | ✓ | ✓ | 无漂移 |
| ABL/HOT/Gap = 3.5625/0.375/1.125 | ✓ | ✓ | ✓ | 无漂移 |
| ablation 16→12→6→6 | ✓ | ✓ | ✓ | 无漂移 |
| coverage 0.228571→0.085714 | ✓ | ✓ | ✓ | 无漂移 |
| P108 L6/R=0.375/adj=2.25 | ✓ | ✓ | — | 无漂移 |
| ML 0.876/0.919/0.922/0.588 | ✓ | ✓ | ✓ | 无漂移 |
| BTC n=1698 / Gate3 NOT SUPPORTED | ✓ | ✓ | ✓ | 无漂移 |
| DEVELOPMENT_ONLY / AI_PROVISIONAL / NOT_RUN | ✓ | ✓ | ✓ | 无漂移 |

**CLAIM_DRIFT = 0 · NUMBER_DRIFT = 0**

---

_本手稿为提交日收敛产物；Formal Human Gate 仍未完成，任何升级为正式验证的表述均禁止。_
