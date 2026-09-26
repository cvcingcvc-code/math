# FINAL CROSS-ARTIFACT CONSISTENCY AUDIT — 2026-09-26

> 生成时间：2026-09-26 21:38（+08:00）。只读审计 + 仅修复 docs/ 一处已确认的 stale 语义。
> 未修改 data/、人工标注、Human Gate、模型、参数、实验、论文结论、UI；未 push、未删除。

## 1. Canonical source hierarchy（事实源优先级）

1. `outputs/final_results.json`（canonical experiment artifact）
2. `paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字 + 4 个冲突处置）
3. `paper/PAPER_EVIDENCE_TRACE.md`（数字→源映射）
4. `paper/development_submission_candidate.md`（论文）
5. `reports/demo/index.html`（Demo）
6. `docs/` / `handoff/`（说明与交接）

## 2. 核心数字表（全部核验一致）

| 指标 | 值 | 核验 |
|---|---|---|
| Pilot N | 140 | ✓ |
| Development N | 70 | ✓ |
| Readable Evidence | 16（L2×5/L3×5/L4×1/L5×2/L6×3） | ✓ |
| NO_EFFECTIVE_EVIDENCE | 54 | ✓ |
| ABL / HOT / Gap | 3.5625 / 0.375 / 1.125 | ✓ |
| Ablation support | M0=16 → M1=12 → M2=6 → M3=6 | ✓ |
| Coverage | 0.228571 → 0.171429 → 0.085714 → 0.085714 | ✓ |
| Robustness grid | 693 total / 660 defined / 33 undefined | ✓ |
| P108 | Raw=L6, R=0.375, Adjusted=2.25 | ✓ |
| External Transfer | BTC n=1698；Gate1/Gate2 SUPPORTED，Gate3 NOT SUPPORTED | ✓ |
| ML RF cross-semester | 0.588 | ✓ |
| Alternative B additive | RMSE vs Raw = 0.3125（λ=0.5） | ✓ |
| Human | R1=0/70, R2=0/70, Formal Gate=NOT_RUN | ✓ |
| AI Increment | NOT_SUPPORTED | ✓ |

## 3. Paper 状态

`PAPER_DEVELOPMENT_SUBMISSION_READY`。canonical 路径 `paper/development_submission_candidate.md`，checker 12/12 PASS。

## 4. Demo 状态

`JUDGE_DEMO_READY`。`reports/demo/index.html` 已与论文对齐：M0 Raw-only=16/0.228571、M1 confidence-only=12/0.171429、M2/M3=6/0.085714；`FORMAL GATE NOT_RUN`；finance 标注 `STRUCTURAL ONLY`、不写 trading advantage。**注意：该文件正被另一进程持续小幅改写（见第 9 节）**。

## 5. Human Gate 状态

Human R1 = 0/70，Human R2 = 0/70，Formal Gate = `NOT_RUN`。未被错误升级。filled_from_B 已核验为派生副本，不作为 R1/R2。

## 6. External Transfer 状态

BTC n=1698 历史纸面模拟，`DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT`。Gate1/Gate2 SUPPORTED，Gate3 NOT SUPPORTED；risk-coverage improvement = false；**未**包装为交易优势。

## 7. 已修复 stale 项（本轮，仅 docs/）

| 文件 | 位置 | 修复 |
|---|---|---|
| `docs/data_dictionary.md` | §4.2 `baseline_weight` 字段 | 澄清该字段是 **M1 confidence-only**（λ=0/0, r_medium=0.75），不是 M0 Raw-only（M0 权重恒 1.0） |
| `docs/data_dictionary.md` | §4.3 summary 行 | 「基线 Support 12.0 / 0.1714」改为完整消融序列：**M0=16/0.228571、M1=12/0.171429、M2/M3=6/0.085714** |

## 8. 未修复 conflict（仅登记，不处理）

| # | 冲突 | 处置 |
|---|---|---|
| 1 | Demo raw semantics（历史 12 vs 16） | 已由并发进程修复 Demo 为 M0=16 口径；`demo_payload.json` 保留 M0/M1 两段（属 ablation 数据） |
| 2 | failure-case null vs 数值 | 论文用 `final_results.json`，`failure_cases/development_candidates.json` 的 null 保留 |
| 3 | Demo 默认参数 0/0 vs 0.5/0.5 | 论文用 M3 λ=0.5/0.5 |
| 4 | run_all 32/32 覆盖范围 | 论文已写进 Limitations（≠ full-chain） |

## 9. Git 状态

| 项 | 值 |
|---|---|
| branch | `master`（tracking origin/master，已修复 `[gone]`） |
| HEAD | `e44dcd77e3d94213137456720d8f2dd2202e57d0` |
| remote | `https://github.com/cvcingcvc-code/math.git`（origin），已 push |
| 未提交（本轮） | `docs/data_dictionary.md`（我的修复） |
| 未提交（其他进程） | `reports/demo/index.html`（并发进程仍在小幅改写） |
| 其他工具是否仍在写 | **是**——`reports/demo/index.html` 仍在被改动（未停止） |

## 10. 最短运行方法

```bash
python src/verify_pilot_integrity.py      # 21/21 + 2 known defects
python run_all.py                         # 32/32 PASS（开发版核心链路）
cd reports/demo && python serve_demo.py 4173   # Demo 本地预览
```

## 11. 下一步任务

负责人完成真实 HUMAN R1（`pilot_worksheet_A.csv` 70/70）→ 记录时间+SHA-256 → ≥24h → R2 → `python src/run_s4_gate.py`。Gate 非 PASS 前保持 development-only。

## 12. 最终状态

**FINAL_CROSS_ARTIFACT_CONSISTENCY = PASS**

核心数字无冲突；data dictionary stale 已修复；Paper↔Demo 一致；F1–F6 引用有效；Human Gate 未错误升级；Finance 未包装成交易优势；ML/Alternative 未写成 winner；无禁止项被修改。
（唯一残留风险：`reports/demo/index.html` 仍被另一进程持续改写，需人工确认该窗口已关闭后做一次 Demo 收尾 commit。）
