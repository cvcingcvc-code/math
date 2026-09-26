# 数学模型一张主图

> 状态：`DEVELOPMENT_ONLY / AI_PROVISIONAL`；`AI_INCREMENT_IDENTIFICATION = NOT_SUPPORTED`。

```text
DATA
  Task Bloom, Student Evidence Bloom, confidence, prompt/context flags
    ↓
OBSERVED PERFORMANCE
  可观察的学生证据记录
    ↓
RAW SIGNAL
  y_i：Student Evidence 的 L1–L6；不可判读则不强行编码
    ↓
EVIDENCE RELIABILITY
  w_i = I(observable_i)c_i(1−λ_prompt p_i)(1−λ_context t_i)
    ↓
ADJUSTED EVALUATION
  Adjusted_i = Raw_i × w_i；汇总时用 Σw_i
    ↓
SUPPORT / COVERAGE
  S = Σw_i；C_eff = Σw_i / N，当前 N=70
    ↓
DECISION
  ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE
```

`LOW_SUPPORT` 是支持等级：可保留 Raw 信号，但不按高支持证据接受。权重为零不等于 0 分，而是 `NO_EFFECTIVE_EVIDENCE`。

灰色理论分支：

```text
AI Increment（当前不可识别）
Delta_raw = Outcome_AI − Outcome_baseline
    ↓  paired baseline unavailable
NOT_SUPPORTED
Delta_reliable = Delta_raw × R = NOT_SUPPORTED
```

当前可运行链是教育开发切片的可观察证据评价；灰色分支不进入 Adjusted Score，也不进入因果结论。
