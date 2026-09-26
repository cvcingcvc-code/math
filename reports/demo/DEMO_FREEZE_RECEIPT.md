# DEMO FREEZE RECEIPT

> 状态：`DEMO_FINAL_PROMOTION`。本文件是把通过评委视角审查的中文化 demo_staging 晋升为正式比赛 Demo 的冻结凭证。
> 生成日期：2026-09-27。
> 本文件只记录既有口径与晋升动作，**不产生任何新研究结论、不修改论文/模型/实验/Human Gate**。

---

## 一、晋升结论摘要

```
DEMO_FINAL                 = FROZEN
FUNCTIONAL_VALIDATION      = PASS
DEMO_FINAL_REVIEW          = PASS
DEMO_PROMOTION             = DONE
P0                         = 0
P1                         = 0
P2                         = favicon.ico 404 only（KNOWN_NON_BLOCKING_ISSUE）
NUMBER_DRIFT               = 0
CLAIM_DRIFT                = 0
OFFLINE_DEMO               = PASS
```

---

## 二、晋升对象与 SHA256（三条红线全部核对一致）

| 项 | 值 |
|---|---|
| 候选文件 | `C:\Users\lin\Documents\Codex\2026-09-25\demo_staging\index.html` |
| 候选 sha256 | `d15d124c256df7cc7d1d9cc6f12a458455ca30df183c4114b16c842b415a4632` |
| 目标晋升前 sha256 | `123453b038b8e91f03ef52ca60c380dd7870bc5d131748fd688187acdb926363` |
| 目标晋升前 git blob | `bf2646beba50fae9f5f66499c848f91bf2eb90be` |
| **晋升后正式 sha256** | **`d15d124c256df7cc7d1d9cc6f12a458455ca30df183c4114b16c842b415a4632`** |
| 晋升后正式 git blob | `ed70c57c5fc93a845bdebce3e8fa760fb8e3e627` |
| 字节 / 行 | 34,181 B / 510 行 |
| `<script>` 块 sha256（晋升前后恒等） | `6e373ee5466ff6b07ff6613a5321dfbecd786ec2bd3a23b58e6d63f687d83174` |

**零编辑晋升**：候选文件未在评审后再次编辑，晋升前后 sha256 完全一致（`_verify.py` 89/89 PASSED，0 FAILED）。

---

## 三、Git 状态

| 项 | 值 |
|---|---|
| GIT_BRANCH | `master` |
| GIT_HEAD_BEFORE | `837a192045647378c886218fd4a668a80e14e154` |
| GIT_HEAD_AFTER | `837a192045647378c886218fd4a668a80e14e154`（未变） |
| 工作区改动 | `M reports/demo/index.html`（仅此一处 Demo 改动） |
| 未跟踪文件 | `paper/DELIVERY_SOURCE_MAP.md`、`paper/FINAL_CLAIM_LOCK.md`、`paper/PAPER_FINAL_REVIEW.md`、`paper/PAPER_FREEZE_CHECKLIST.md`（均非本轮产物，属 FINAL_CONSISTENCY_AUDIT） |
| COMMIT | **NO**（按 DEMO_PROMOTION_CHECKLIST §7，提交须负责人单独授权） |
| PUSH | **NO** |

> 说明：HEAD 始终为 `837a192`，未出现新的 freeze commit。本轮仅改 `reports/demo/index.html` 一处；
> `paper/`、`data/`、`outputs/`、`reports/visual_evidence/` 均**零改动**。

---

## 四、并发写入核查

- `handoff/MULTIPROCESS_STATE.md` 写锁仅 `AUDIT_REGISTRY`（WINDOW_20260926_180938），**不含** `reports/demo/`。
- 活动窗口均为 AUDIT / FORMAL_VALIDATION（READONLY 或 AUDIT_REGISTRY 写范围），最后更新于 2026-09-26T18:22（晋升时已陈旧）。
- 晋升期间检测到 `paper/FINAL_CLAIM_LOCK.md` 新出现（FINAL_CONSISTENCY_AUDIT 并发产物），但落在 `paper/` 侧，
  **未触碰 `reports/demo/`**，不构成 Demo 并发写入冲突。
- `git status --short` 晋升前后均无 `reports/demo/` 的他人改动。

---

## 五、Paper ↔ Demo 数字对表（NUMBER_DRIFT = 0）

以 `paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字）+ `paper/FINAL_CLAIM_LOCK.md`（核心数量表）+ `paper/PAPER_EVIDENCE_TRACE.md`（C1–C13）为唯一 Claim 来源，逐项核对 Demo：

| 数字 | 锁定值 | Demo 展示 | 一致 |
|---|---|---|---:|
| Development slice | N = 70 | 横幅/§3/§8「70」 | ✓ |
| 可判读 Student Evidence | 16（L2×5/L3×5/L4×1/L5×2/L6×3） | §3「16 条可判读（L2×5…L6×3）」、§8「16」 | ✓ |
| NO_EVIDENCE / UNDETERMINED | 19 / 35 | §3「19 条 NO_EVIDENCE + 35 条 UNDETERMINED」 | ✓ |
| NO_EFFECTIVE_EVIDENCE | 54（= 19 + 35，非 54 个零分） | §3/§8「54」 | ✓ |
| ABL / HOT / Gap | 3.5625 / 0.375 / 1.125（Raw=Adjusted，非提升） | 指标卡 + §3「3.5625 / 0.375 / 1.125」「不是提升」 | ✓ |
| Ablation weight | 16 → 12 → 6 → 6 | 指标卡 + §3 表 | ✓ |
| Ablation coverage | 0.228571 → 0.171429 → 0.085714 → 0.085714（N=70） | §3 表 + 指标卡 | ✓ |
| Robustness grid | 693 = 21×11×3；660 defined / 33 undefined | §4「693 网格 660 defined / 33 undefined」 | ✓ |
| parameter perturbation | ±10%/±20% → 0 flips；NOT_APPLICABLE | §4「±10%/±20% → 0 个 decision-state flips」「NOT_APPLICABLE」 | ✓ |
| 反例 P108 | L6 / R=0.375 / Adj=2.25 / LOW_SUPPORT→ABSTAIN | §5 + 交互盒「0.375 / 2.25 / LOW_SUPPORT → ABSTAIN」 | ✓ |
| 反例 P105 | L2 / R=0.375 / Adj=0.75 / LOW_SUPPORT | §5 note「P105 参考：Raw=L2、R=0.375、Adjusted=0.75」 | ✓ |
| 反例 P072 / P035 | NO_EFFECTIVE_EVIDENCE（null，不填 0） | §5「P072/P035 · 无有效证据，Adjusted=null」 | ✓ |
| ML Challenger | LogReg 0.876 / Tree 0.919 / RF 0.922；缺失 0.71–0.81；RF 跨学期 0.588 | §6 卡片 | ✓ |
| External Transfer | BTC n=1698；threshold 0.65；Gate1/2 SUPPORTED、Gate3 NOT SUPPORTED；risk-coverage=false | §7 表 + note | ✓ |
| Gate1 数字 | Reliability 0.603 → 0.408 | §7 | ✓ |
| Gate2 数字 | coverage 0.394 → 0.001 | §7 | ✓ |
| Gate3 数字 | 0.525 vs 0.528（无改善） | §7 | ✓ |
| Human Gate | R1=0/70、R2=0/70、Formal Gate=NOT_RUN | 横幅 + §8 | ✓ |
| AI Increment | NOT_SUPPORTED | §8「NOT_SUPPORTED」 | ✓ |
| 关键常量 | λ_prompt=0.5、λ_context=0.5、c_i∈{1,0.75,0.5}、R=0.375 | §2 公式 + 解释 | ✓ |

**NUMBER_DRIFT = 0**。

---

## 六、Claim 边界核对（CLAIM_DRIFT = 0）

| 要求 | Demo 措辞 | 判定 |
|---|---|---|
| External Transfer 不得写成外部效果证明 | §7「STRUCTURAL ONLY（结构迁移演示），不写 profitable trading / prediction advantage / universal generalization」 | ✓ |
| ML Challenger 不得写成 ML winner | §6「不做 winner 排名」「INSUFFICIENT_FOR_STRONG_ML_CLAIM」 | ✓ |
| Human Gate 不得暗示完成 | 横幅/§8「FORMAL GATE NOT_RUN」「R1 0/70 · R2 0/70」 | ✓ |
| AI Increment 不得暗示已识别 | §8「NOT_SUPPORTED —— 无合法配对的 Outcome_AI / Outcome_baseline」 | ✓ |
| 不写成 improvement | 指标卡/§3「公共缩放退化，不是提升」「不得写成 improvement」 | ✓ |
| Main Conclusion | §3「分数稳定 ≠ 证据支撑稳定（Score Stability ≠ Evidence Support Stability）」 | ✓ |
| 不声称 FORMAL_SUPPORTED | 全程 DEVELOPMENT_ONLY / AI_PROVISIONAL | ✓ |
| 不声称 R 是校准概率 | §2「w_i：确定性支持权重（不是概率）」「WEAKLY_JUSTIFIED_COMPONENT」 | ✓ |

**CLAIM_DRIFT = 0**。

---

## 七、离线演示验证（OFFLINE_DEMO = PASS）

| # | 检查项 | 结果 |
|---|---|---:|
| 1 | 无网络条件下能打开 | PASS（外部请求 0，字体走系统栈） |
| 2 | 首页正常 | PASS（HTTP 200，34,181 B） |
| 3 | 六张核心图能展示 | PASS（F1–F6 全部 HTTP 200） |
| 4 | 所有主要交互可使用 | PASS（按钮纯前端确定性复算，无网络依赖） |
| 5 | 无 404 / missing asset | PASS（服务日志零 404） |
| 6 | 无 localhost 外部依赖 | PASS（0 处 http/https/localhost/127.0.0.1 引用） |
| 7 | 不依赖临时 build 文件 | PASS（单文件自包含，仅 6 张 SVG 相对引用） |
| 8 | 中文正常 | PASS（UTF-8，中文内容完整可读） |
| 9 | 浏览器刷新后仍可运行 | PASS（纯静态，无服务端状态） |
| 10 | 讲完主线不需开发工具 | PASS（静态 HTML，直接打开或静态服务即可） |

**30 秒理解模拟**（首屏 545px / 768px，最小笔记本无需滚动）：
- 问题是什么 → 首屏研究问题「观察到的结果 ≠ 可靠证据」；
- 为什么 Raw 不够 → 副标题「把表现水平与证据支持分开」+ §1；
- Reliability 做什么 → §2 流水线 + 公式 + 人话解释；
- 为什么存在 ABSTAIN → §2 判定卡「证据不足或冲突时暂缓判断」；
- Main Conclusion → §3「分数稳定 ≠ 证据支撑稳定」。

以上结论复用自 `demo_staging/DEMO_STAGING_REVIEW.md`（R1–R7 PASS，Playwright 实测），
本晋升文件与受评文件字节级一致（同一 sha256），结论直接有效。

---

## 八、Paper 引用

- 唯一 canonical paper：`paper/paper_v2_submission_candidate.md`（SHA256 `8b478b7e5a1f7cfa7a1176ac97349c26518c4782f29cfcb78ac5f13e3bd47a15`）
- 数字源：`paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字）
- 声明映射：`paper/PAPER_EVIDENCE_TRACE.md`（C1–C13）
- 口径锁定：`paper/FINAL_CLAIM_LOCK.md`（FINAL_CONSISTENCY_AUDIT 生成）
- 冻结检查：`paper/PAPER_FREEZE_CHECKLIST.md`（PAPER_FREEZE_READY=YES）
- 评委审查：`paper/PAPER_FINAL_REVIEW.md`（PAPER_FINAL_REVIEW=PASS）
- 最终 PDF：`paper/final/数学建模论文_最终排版版_2026-09-27.pdf`

---

## 九、已知局限（Known Limitations，均不阻塞）

### 研究边界（状态不变）

- `DEVELOPMENT_ONLY` / `AI_PROVISIONAL` / `NOT_HUMAN_VALIDATED`。
- Human Gate = `NOT_RUN`（R1=0/70、R2=0/70）；`formal_gate_eligible=false`。
- `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`（无合法 paired outcome）。
- Main Conclusion 级别：descriptive / structural（Evidence Level 1），不升级。

### P2（仅记录，不修）

- **KNOWN_NON_BLOCKING_ISSUE / P2**｜`/favicon.ico` 404 only：浏览器自动请求站点图标时返回 404；页面主体、F1–F6、交互和离线演示均正常。按用户裁定保留现状，不修改 `serve_demo.py`，不修改 `index.html`，不重新晋升，不回滚，不生成新 Demo 版本。
- **P2-1**｜`.pos/.warn/.neg` 在 `<td>` 上不生效（CSS 后代选择器 `td .pos` 与 `<td class="pos">` 不匹配，7 个单元格拿不到预期颜色）。基线既有缺陷，非中文化引入；信息仍完整可读。
- **P2-2**｜F6 图内最小字号 10.2px（其余五张 11.1px），属 `reports/visual_evidence/final/` canonical 图件固有，禁止修改。

> 本窗口冻结后不再处理 Demo。

---

## 十、晋升动作记录

| 项 | 值 |
|---|---|
| 备份路径 | `C:\Users\lin\Documents\Codex\2026-09-25\promotion_backup\20260927_010246\`（含 index.html / serve_demo.py / demo_payload.json 的 `.pre_promotion` 副本） |
| 备份 index.html sha256 | `123453b0…`（= 晋升前目标值，可回滚） |
| 执行动作 | 仅 `cp demo_staging/index.html → yu/reports/demo/index.html`；**未动** serve_demo.py |
| 回滚预案 | 将 `promotion_backup/20260927_010246/index.html.pre_promotion` 覆盖回 `yu/reports/demo/index.html` 即可回到 `123453b0…` |

---

## 十一、最终输出

```
DEMO_FINAL                 = FROZEN
FUNCTIONAL_VALIDATION      = PASS
DEMO_FINAL_REVIEW          = PASS
DEMO_PROMOTION             = DONE
P0                         = 0
P1                         = 0
P2                         = favicon.ico 404 only
KNOWN_NON_BLOCKING_ISSUE   = /favicon.ico 404 only
NUMBER_DRIFT               = 0
CLAIM_DRIFT                = 0
OFFLINE_DEMO               = PASS
FORMAL_DEMO_PATH           = C:\Users\lin\Documents\Codex\2026-09-25\yu\reports\demo\index.html
FORMAL_DEMO_SHA256         = d15d124c256df7cc7d1d9cc6f12a458455ca30df183c4114b16c842b415a4632
PAPER_CHANGED              = NO
DEMO_CHANGED               = NO（冻结后不再处理 Demo）
GIT_HEAD_BEFORE            = 27c0c083b132533a187ff3c83d6fbaacbea26ce6
GIT_HEAD_AFTER             = 27c0c083b132533a187ff3c83d6fbaacbea26ce6
COMMIT                     = NO
PUSH                       = NO
NEXT_STAGE                 = FINAL_DELIVERY_ALIGNMENT_AND_REHEARSAL
```

---

_DEMO_FINAL_PROMOTION · 中文化 Demo 晋升完成 · 论文/模型/实验/Human Gate 均零改动 · 不标 FORMAL_FINAL_
