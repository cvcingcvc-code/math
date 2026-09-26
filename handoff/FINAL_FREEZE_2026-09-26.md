# FINAL FREEZE — 2026-09-26

> 冻结阶段：`FINAL_FREEZE_AND_GIT_DELIVERY`。本文档只登记冻结状态，不新增研究结论。
> 生成时间：2026-09-26（+08:00）。branch `master`，remote `https://github.com/cvcingcvc-code/math.git`。

## 1. Research Question

当观测证据存在缺失、冲突或可信度差异时，如何避免把 Raw Signal 直接当成可信结论，并通过 Evidence Reliability、Support/Coverage 以及 ABSTAIN 机制避免过度确定的判断？

（这是一个 measurement / identifiability 问题，不是预测问题，也不是因果识别问题。）

## 2. Main Conclusion

**Score Stability ≠ Evidence Support Stability.**

归一化分数（ABL/HOT/Gap = 3.5625 / 0.375 / 1.125）在加入可靠性权重前后保持不变，但有效证据权重从 16 降到 6、有效覆盖率从 0.228571 降到 0.085714（分母 N=70）。分数看起来稳定，并不能保证支撑它的证据充分、可靠或完整。

## 3. Paper status

`PAPER_DEVELOPMENT_SUBMISSION_READY`。全部结果 `AI_PROVISIONAL / DEVELOPMENT_ONLY`，`NOT_HUMAN_VALIDATED`，`formal_gate_eligible=false`。

## 4. Demo status

`JUDGE_DEMO_READY`。`reports/demo/index.html` 已与论文对齐：M0=16/0.228571、M1=12/0.171429、M2/M3=6/0.085714；Human Gate 0/70·0/70·NOT_RUN；finance 标注 `STRUCTURAL ONLY`。启动 smoke test 通过（HTTP 200，首页 + F1–F6 均加载）。

## 5. Consistency audit status

`FINAL_CROSS_ARTIFACT_CONSISTENCY = PASS`。核心数字无冲突；Paper ↔ Demo ↔ `outputs/final_results.json` 一致；Human Gate 未错误升级；Finance 未包装为交易优势。

### Checker 状态（当前真实状态，非历史）

- **CURRENT_CHECKER = 11/12**
- **DEMO_SMOKE = PASS**
- **CHECKER_CONTRACT_DRIFT = OPEN**

`src/development_submission_checker.py` 的 12 项检查中 11 项 PASS，唯一 FAIL 是 `demo` 检查。该检查是**旧版 Demo contract 的启发式字符串断言**，要求 demo 含旧 fetch 路径 `../../outputs/final_results.json` 以及 `Explain`/`What-if`/`Evaluation Status` 标签。当前新 Demo 已重构为「内联数字 + 内联 JS」，上述字符串被移除，故该检查 FAIL。**这是 checker 与 demo 的 contract 漂移，不是 PAPER/DATA/DEMO 数字错误**：新 Demo 已独立验证——HTTP smoke test 通过（首页 + F1–F6 全部 200）、canonical 数字一致、页面正常运行。

`reports/verification/development_submission_consistency.json` 记录的是本次真实运行结果（`status=FAIL`、`demo=false`、11/12），**未用历史 PASS 冒充当前状态**。不得为得到 12/12 而回改 Demo。

## 6. Human Gate status

Human R1 = 0/70，Human R2 = 0/70，Formal Gate = `NOT_RUN`。不得因 Git 收口修改。

## 7. Known limitations

- 输入为 AI provisional 标签，非人工验证；可判读 16 条高度同质（全部 prompt=true / context=false / confidence=medium / task_actor=ai）。
- 无合法配对的 `Outcome_AI` / `Outcome_baseline` → `AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`，不识别因果增量。
- 稳健性只覆盖当前同质切片，不构成 universal robustness。
- External Transfer（BTC n=1698）是 synthetic/controlled 结构演示，非教育泛化；Gate3 NOT SUPPORTED。
- 2 个已知数据缺陷（`verify_pilot_integrity.py` 缺陷登记）：S4-F01（ai_context_text 含未来 AI 内容泄漏）、S4-F02（人工复核队列非盲）。

## 8. Demo run command

```bash
cd reports/demo && python serve_demo.py 4173
```

## 9. Paper file

`paper/development_submission_candidate.md`（canonical development paper）

## 10. Canonical number lock file

`paper/PAPER_NUMBER_LOCK.md`（18 组锁定数字 + 4 个冲突处置）；事实源 `outputs/final_results.json`；溯源 `paper/PAPER_EVIDENCE_TRACE.md`。

## 11. 下一步仅剩

- PPT / roadshow 制作
- Human R1 / R2 / Formal Gate（真实人工标注，`python src/run_s4_gate.py`）

---

**当前项目状态：`COMPETITION_DEVELOPMENT_BUILD_FROZEN`**
