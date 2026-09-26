# PPT_FINAL_CONVERGENCE：8 分钟主讲故事线

状态：`READY_FOR_REHEARSAL_CANDIDATE`

## 一、主讲目标

让评委在 8 分钟内记住一个可检验的判断：

> **Score Stability ≠ Evidence Support Stability.**
> 分数稳定，不等于证据支撑稳定。

本次演示只解释一个 measurement / identifiability 问题：当观测证据存在缺失、冲突或可信度差异时，如何避免直接把 Raw Signal 当成可信结论，并允许在证据不足时 ABSTAIN。

## 二、固定链路

`Observed Evidence → Raw Signal → Evidence Reliability → Adjusted Evaluation → Support / Coverage → ACCEPT / ABSTAIN / NO_EFFECTIVE_EVIDENCE`

## 三、10 页结构

| 页 | 标题 | 页面任务 | L1 视觉 | 预计口播 |
|---:|---|---|---|---:|
| 1 | 观察到的结果，不等于可靠证据 | 抛出研究问题和唯一主结论 | 研究问题 + 主结论 | 35s |
| 2 | 为什么 Raw Signal 不够 | 区分表现水平与证据支持 | F2：Raw vs Adjusted | 45s |
| 3 | Reliability-aware evaluation | 给出固定模型链路、公式和 fail-closed 语义 | F1：Model Flow | 55s |
| 4 | Development slice：70 条记录，只有 16 条可判读 | 交代样本边界与证据缺失 | F3：Evidence Degradation | 45s |
| 5 | 公共缩放退化：分数不动，但支持下降 | 解释 ABL/HOT/Gap 与 coverage 变化的机制 | F4：Parameter Perturbation | 60s |
| 6 | 五条验证路径回答同一个问题 | 汇总 robustness、ablation、failure、ML、transfer | F4/F5/F6 缩略证据带 | 55s |
| 7 | 失败不是 0 分：ABSTAIN 与 NO_EFFECTIVE_EVIDENCE | 用 P108、P105、P072/P035 说明决策语义 | F5：Ablation/Refusal | 55s |
| 8 | Challenger 与外部迁移：支持边界同样重要 | 保留 ML 和 BTC 的负结果，不升级 Claim | F6：External Transfer | 65s |
| 9 | 研究边界：现在能说什么，不能说什么 | 明确 Human Gate、AI Increment、DEVELOPMENT_ONLY | 状态边界表 | 45s |
| 10 | 结论与现场 Demo | 收束唯一结论，进入 60–90 秒 Demo | 主结论 + Demo 路线 | 35s |

总口播约 8 分钟，不把数字讲成效果提升，不把 DEVELOPMENT_ONLY 讲成正式验证。

## 四、逐页核心信息

### 01｜研究问题

开场直接说：我们研究的不是“AI 是否提高成绩”，而是观测到的结果能否被可靠地解释。核心风险是把一个 Raw Signal 直接当成结论。最终要回答的是：当证据质量不同甚至不可判读时，系统能否把“表现”“证据支持”和“暂缓判断”分开。

### 02｜Raw 与 Support 分离

左侧保留 Raw Signal，右侧引入 Evidence Reliability。强调：Raw 与 Reliability 是两个独立层。即便归一化后的 Raw/Adjusted 指标看起来相同，也不能因此认为证据支持同样稳定。

### 03｜框架

展示固定链路和公式：

`w_i = I(observable_i) · c_i · (1 − λ_prompt · p_i) · (1 − λ_context · t_i)`

`Adjusted_i = Raw_i × w_i`，`S = Σw_i`，`C_eff = Σw_i / N`，其中 `N=70` development records。证据不足时不是填 0，而是返回 `NO_EFFECTIVE_EVIDENCE`；低支持时允许 `ABSTAIN`。

### 04｜数据现实

当前 development slice 是 70 条 AI provisional records。16 条可判读，19 条 NO_EVIDENCE，35 条 UNDETERMINED，因此 54 条进入 `NO_EFFECTIVE_EVIDENCE`。这里的 54 不是 54 个零分，而是没有可用证据支持数值判断。

### 05｜机制性发现

16 条可判读记录共享 `prompt=true`、`context=false`、`confidence=medium`，每条 `R=0.375`。因此公共缩放会被归一化抵消：ABL/HOT/Gap 仍为 `3.5625 / 0.375 / 1.125`；但 effective weight 从 `16 → 12 → 6 → 6`，coverage 从 `0.228571 → 0.171429 → 0.085714 → 0.085714`。这正是“分数稳定、支持下降”。

### 06｜验证不是五个新主张

五条验证路径共同回答同一个问题：当 score 看似稳定时，evidence support 是否也稳定？Robustness grid 为 `693=21×11×3`，660 defined、33 undefined；参数扰动 ±10%/±20% 产生 0 个 decision-state flips。Ablation 显示支持下降，failure cases 显示系统能拒绝无证据输出，ML 和 external transfer 则约束外推边界。

### 07｜拒绝错误确定性

P108：Raw=L6，R=0.375，Adjusted=2.25，状态为 `LOW_SUPPORT / ABSTAIN`。P105：Raw=L2，Adjusted=0.75，仍为低支持。P072/P035：`NO_EFFECTIVE_EVIDENCE`，Adjusted 为 null，不填 0。ABSTAIN 是合理输出，不是模型失败。

### 08｜挑战与迁移

ML challenger：LogReg ≈0.876，Tree ≈0.919，RF ≈0.922，但 RF 跨学期为 0.588，故保留 `INSUFFICIENT_FOR_STRONG_ML_CLAIM`，不声称 winner。BTC n=1698：Gate1/2 supported，Gate3 not supported，risk-coverage improvement=false；这只能叫 `STRUCTURAL ONLY`。

### 09｜Claim boundary

这是 `AI_PROVISIONAL / DEVELOPMENT_ONLY / NOT_HUMAN_VALIDATED`。Human R1=0/70，R2=0/70，Formal Gate=NOT_RUN；AI increment identification=NOT_SUPPORTED。不能声称 AI 提高学习效果、因果增量、预测准确率提升、交易优势或通用泛化。

### 10｜收束与 Demo

最终只留下一个结论：稳定的 score 不能替代稳定的 evidence support。Demo 只走四个锚点：研究问题、模型链路、主结果、P108 失败案例；若现场不稳定，直接使用离线静态 Demo 和六张冻结图。

## 五、设计硬约束

- 画布：1280×720，学术答辩风。
- 背景：白色 / `#F7F9FC`；主色：`#1E4FA8`；深色：`#0E3F8C`；警示红仅用于负结果和限制。
- 复用冻结 F1–F6，不重绘核心证据图。
- 每页保留标题、主视觉、底部结论/页码；正文不低于可读字号。
- 不使用营销语言，不新增研究结论，不把负结果隐藏到附录。
