# PAPER FREEZE CHECKLIST

> 状态：`PAPER_FREEZE_READY = YES`。本文件是论文冻结前的最终检查清单。
> 检查对象：`paper/paper_v2_submission_candidate.md`（580 行，HEAD `71f0276`）。
> 检查日期：2026-09-27。

---

## 一、冻结前扫描结果

| # | 扫描项 | 结果 |
|---|---|---|
| 1 | NUMBER_DRIFT | 0 |
| 2 | overclaim wording | 0（所有 forbidden 措辞均在否定/禁止语境） |
| 3 | figure paths | PASS（6 张图路径正确，文件存在） |
| 4 | citation placeholders | 0（已清空） |
| 5 | TODO | 0 |
| 6 | FIXME | 0 |
| 7 | [FIGURE HERE] | 0 |
| 8 | stale references | 0 |
| 9 | old demo references | 0 |
| 10 | archive references | 0 |
| 11 | 重复论文候选 | 已确认唯一 canonical（见下） |

---

## 二、唯一 canonical 论文候选

| 字段 | 值 |
|---|---|
| 文件路径 | `paper/paper_v2_submission_candidate.md` |
| Git HEAD | `71f02769144350295227be6b48647460cc6600bd` |
| Git blob hash | `4e60375bd6e8383fd6dda94e9223138657b2763d` |
| SHA256 | `8b478b7e5a1f7cfa7a1176ac97349c26518c4782f29cfcb78ac5f13e3bd47a15` |
| 行数 | 580 |
| 字数 | 3480 |
| 文件大小 | 45732 bytes |
| 状态标记 | `PAPER_V2_CANONICAL_DEVELOPMENT` |

### 其他论文文件（非 canonical，保留可追溯）

| 文件 | 角色 | 是否 canonical |
|---|---|---:|
| `paper/paper_v2_submission_candidate.md` | **提交候选**（P1 已修） | **✓ YES** |
| `paper/paper_v2_full_draft.md` | 全稿 v2（PAPER_DRAFT_0） | NO（原型） |
| `paper/paper_v2_candidate.md` | 结构重写候选 | NO（原型） |
| `paper/development_submission_candidate.md` | V1 开发提交候选 | NO（旧版） |
| `paper/submission_candidate.md` | 旧提交候选 | NO（旧版） |

---

## 三、冻结检查项

### 3.1 研究问题一致性

- [x] Main RQ 贯穿全文：观测证据缺失/冲突/可信度不一时，如何避免把 Raw Signal 当可信结论
- [x] 不是因果识别问题、不是预测问题
- [x] `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED` 声明贯穿全文

### 3.2 数字锁定

- [x] 18 组锁定数字逐一从 canonical artifact 核验
- [x] `outputs/final_results.json` 为统一事实源
- [x] `reports/verification/independent_bounds_summary.json` 为独立复算源
- [x] NUMBER_DRIFT = 0

### 3.3 Claim Boundary

- [x] 不声称 FORMAL_SUPPORTED
- [x] 不声称 AI 提高学习效果
- [x] 不声称 AI 导致成绩提升
- [x] 不声称 AI increment 已被识别
- [x] 不声称 causal learning gain
- [x] 不声称 ML winner
- [x] 不声称 ML 被击败
- [x] 不声称 accuracy 提升
- [x] 不声称 准确率提升
- [x] 不声称 交易优势
- [x] 不声称 教育泛化
- [x] CLAIM_BOUNDARY_VIOLATION = 0

### 3.4 图表

- [x] 6 张 canonical figure 真实存在
- [x] 路径正确（`../reports/visual_evidence/final/F*.svg`）
- [x] caption 正确
- [x] 正文引用正确
- [x] 没有引用旧图
- [x] 没有引用 archive
- [x] 没有引用 stale a4429af
- [x] 不超出证据边界
- [x] Table 编号 1–11 连续无缺
- [x] FIGURE_REFERENCE = PASS

### 3.5 文献

- [x] 不存在虚构 DOI
- [x] 不存在虚构 citation
- [x] 正文 claim 与引用匹配
- [x] citation placeholder 已清空
- [x] 不存在 TODO citation
- [x] 不存在"看起来像引用但无法追溯"的内容
- [x] LITERATURE_CHECK = PASS

### 3.6 五类验证

- [x] VQ1 Baseline（§6.1）：四模型同分但支持记账不同
- [x] VQ2 Ablation（§6.2）：组件确实改变 support accounting
- [x] VQ3 Sensitivity（§6.3）：693 格内分数恒定而支持变化
- [x] VQ4 Failure（§6.4）：P108 High Raw ≠ High Support
- [x] VQ5 External（§6.5）：结构可迁移但 Gate3 NOT SUPPORTED
- [x] ML = Challenger（不是 Main Model）
- [x] Finance = External Structural Demonstration（不是盈利能力证明）

### 3.7 Limitations 保留

- [x] GAP-1：Human Gate 尚未完成（R1=0/70, R2=0/70, Formal Gate NOT_RUN）
- [x] GAP-2：Reliability 参数正式校准不足（WEAKLY_JUSTIFIED_COMPONENT）
- [x] GAP-3：AI Increment / causal learning gain 无法识别
- [x] 其他限制保留（无 true outcome、finance 仅 structural transfer、ML strong claim unsupported、no single dominant formulation、复现边界、数据完整性 open defects）

### 3.8 禁止事项核对

- [x] 未改变研究问题
- [x] 未改变主模型
- [x] 未重新运行冻结实验
- [x] 未修改原始数据
- [x] 未调参数
- [x] 未创造新数字
- [x] 未创造新实验
- [x] 未扩大结论
- [x] 未修改 Demo
- [x] 未修改 canonical visual evidence

---

## 四、冻结状态

```
PAPER_FINAL_REVIEW         = PASS
PAPER_FREEZE_READY         = YES
P0                         = 0
P1                         = 0
P2                         = 4（不修）
NUMBER_DRIFT               = 0
CLAIM_BOUNDARY_VIOLATION   = 0
FIGURE_REFERENCE           = PASS
LITERATURE_CHECK           = PASS
DELIVERY_SOURCE_MAP        = READY
DEMO_CHANGED               = NO
DATA_CHANGED               = NO
EXPERIMENT_CHANGED         = NO
COMMIT                     = NO
PUSH                       = NO
```

**WINDOW_STATUS = FROZEN / WAITING_FOR_FINAL_CONSISTENCY_AUDIT**

---

_PAPER_V2_CANONICAL_DEVELOPMENT · Formal Human Gate 仍未完成 · 不标 FORMAL_FINAL_
