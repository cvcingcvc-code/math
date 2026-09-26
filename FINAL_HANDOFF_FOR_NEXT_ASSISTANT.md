# FINAL HANDOFF FOR NEXT ASSISTANT

> 给后续新窗口 / 另一个助手的完整接管说明。
> 生成日期：2026-09-27。**禁止新助手凭记忆改数字，一切以本文件 + canonical 锁文件为准。**

---

## 一、项目根目录

```
C:\Users\lin\Documents\Codex\2026-09-25\yu
```

## 二、Git 状态（已冻结，勿再动）

| 项 | 值 |
|---|---|
| 分支 | `master` |
| HEAD | `16be8b7aacce4bb2d1bb759c89248d4e329a851e` |
| origin/master | `16be8b7aacce4bb2d1bb759c89248d4e329a851e`（与 HEAD 一致） |
| 远程 | `https://github.com/cvcingcvc-code/math.git` |
| 工作区未跟踪 | `reports/demo_competition_staging/`（本地候选副本，勿纳入 Git） |

**注意**：过夜交接阶段 `COMMIT = NO`、`PUSH = NO`。正式 release 已同步，除非负责人明确授权，不要提交。

## 三、当前最终状态

| 项 | 值 |
|---|---|
| Paper | PASS（FROZEN） |
| PPT | PASS（FROZEN，10 页） |
| Demo | FROZEN（`reports/demo/index.html`） |
| Figures | 6/6（F1–F6） |
| Submission Package | PASS |
| Manifest | 42/42 PASS |
| P0 | 0 |
| P1 | 0 |
| P2 | `/favicon.ico` 404（KNOWN_NON_BLOCKING）+ 两条 CSS/字号级 P2（见 DEMO_FREEZE_RECEIPT） |

## 四、正式交付文件位置（勿改）

| 交付物 | 路径 |
|---|---|
| canonical paper | `paper/paper_v2_submission_candidate.md` |
| 最终 PDF | `paper/paper_submission_final.pdf` |
| 可编辑 DOCX | `paper/final/数学建模论文_可编辑版_2026-09-27.docx` |
| 最终 PPT | `outputs/education_ai_evidence_roadshow_final.pptx` |
| 正式 Demo | `reports/demo/index.html` |
| 六图 | `reports/visual_evidence/final/F1–F6.svg` |
| 统一事实源 | `outputs/final_results.json` |
| 提交包 | `outputs/submission_package_development_only/` |

## 五、桌面最终交付目录

```
C:\Users\lin\Desktop\数学建模比赛_最终提交_2026-09-27\
  01_最终论文.pdf
  02_最终论文_可编辑版.docx
  03_最终路演.pptx
  04_Demo_启动说明.txt
  05_提交包\
  06_明日路演卡片.txt
```

## 六、唯一事实源（改数字前必须先读）

- `paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字）
- `paper/FINAL_CLAIM_LOCK.md`（口径 + 主结论 + 状态边界）
- `paper/PAPER_EVIDENCE_TRACE.md`（C1–C13 声明映射）
- `docs/metric_dictionary.md`（冻结词汇）

## 七、冻结研究主线（一字不改）

- **Main RQ**：观测证据缺失/冲突/可信度不一时，如何避免把 Raw Signal 当可靠结论，并显式报告 Reliability、Support/Coverage、允许 ABSTAIN。
- **主模型链**：`Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support/Coverage → Decision`。
- **核心语义**：High Raw ≠ High Evidence Support；Missing Evidence ≠ Zero Performance；ABSTAIN；NO_EFFECTIVE_EVIDENCE。
- **唯一主结论**：Score Stability ≠ Evidence Support Stability。

## 八、关键数字（全部锁定）

- Development N = **70**；Readable = **16**；NO_EFFECTIVE_EVIDENCE = **54**（19 NO_EVIDENCE + 35 UNDETERMINED）
- ABL / HOT / Gap = **3.5625 / 0.375 / 1.125**（1.125 = aggregate Gap；2.25 = P108 单记录 Adjusted contribution）
- Ablation = **16 → 12 → 6 → 6**；Coverage = **0.228571 → 0.171429 → 0.085714 → 0.085714**
- Grid = **693**（660 defined / 33 undefined）
- Counterexamples = **P108 / P105 / P072 / P035**
- ML = **0.876 / 0.919 / 0.922** → `INSUFFICIENT_FOR_STRONG_ML_CLAIM`
- Alternative Formulations = `NO_SINGLE_DOMINANT_MODEL`
- BTC = **n=1698**；Gate1/2 SUPPORTED，Gate3 NOT SUPPORTED
- Human = **R1=0/70 / R2=0/70 / NOT_RUN**；AI Increment = `NOT_SUPPORTED`

## 九、External Transfer 的真正作用

不是第二个项目，不是金融预测。作用是检验同一个 `Raw → Reliability → Adjusted → Coverage → Decision` 结构能否迁移到另一种 noisy-signal domain。定位：`STRUCTURAL TRANSFER ONLY`。**必须保留 Gate3 = NOT SUPPORTED**，因为它证明 Reliability 未被证明是未来正确性的 calibrated predictor。

## 十、明天开始前的第一读

1. `WAKE_UP_FIRST_READ.md`（1 页速览）
2. `presentation/MORNING_OPTIMIZATION_PLAN.md`
3. `presentation/JUDGE_RED_TEAM_FINAL.md`

## 十一、红线（严禁）

- 严禁凭记忆改任何锁定数字
- 严禁修改 canonical paper / 最终 PDF / DOCX / PPT / 正式 Demo / F1–F6 / final_results / model code / data / Human labels / Gate
- 严禁 `git add -A`；严禁未经授权 commit / push
- 严禁把 DEVELOPMENT_ONLY 包装成 FORMAL_FINAL
- 严禁声称 AI 提升学习、因果增量、预测准确率提升、交易优势、通用泛化
