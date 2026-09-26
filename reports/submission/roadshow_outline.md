# 路演 / 答辩大纲（DEVELOPMENT_ONLY 提交候选）

> 全场状态标记：`AI_PROVISIONAL · DEVELOPMENT_ONLY · formal_gate_eligible=false`。不展示 AIV 或排名数字。

**一句话主题：AI 辅助学习评价中，分数看起来稳定，并不意味着证据真的可靠。**

## 1. 开场：问题（1 分钟）

- AI 进入学习过程后，学生提交的文本混合了学生思考、AI 提示、上下文缺失。
- 看到学生交了什么 ≠ 观察到了多少可信的学生证据。
- 只给一个分数，会把"证据很稀薄"藏在"数字很精确"后面。

## 2. 我们的做法：分数与证据分开报告（1.5 分钟）

- 先判断哪些记录是可判读的学生 Evidence：70 条开发记录中只有 16 条（19 条 NO_EVIDENCE，35 条 UNDETERMINED）。
- 同时报告两样东西：**Score**（ABL / HOT / Gap）和 **Evidence Support**（有效证据权重 / 70 条记录）。
- 有效证据为零时，返回 `NO_EFFECTIVE_EVIDENCE`：**未定义，不是 0 分**。
- 用透明假设参数（`lambda_prompt`、`lambda_context`、`r_medium`，共 693 组）展示结论对假设的依赖。

## 3. 核心发现（1 分钟，配 Figure 4 / Demo）

- 660 组有定义参数下，Score 恒为 ABL=3.5625、HOT=0.375、Gap=1.125。
- 同时 Evidence Support 从 0.2286 降到 0.0057；`lambda_prompt=1` 时 33 组无定义。
- **Score 数值稳定，不代表支持它的证据稳定。**

## 4. 三个真实开发案例：我们最可能错在哪里、如何发现、如何修正（3 分钟，重点）

**案例 1：Score 稳定，一度看起来像模型稳健。**
- 现象：693 组参数下 Score 纹丝不动。
- 发现：16 条可判读 Evidence 的 prompt / context / confidence 字段完全相同，权重是公共缩放，加权平均在代数上必然不变。
- 修正：论文与 Demo 明确写为"公共缩放结构导致的性质"，不作为稳健性或因果证据。

**案例 2：Figure 4 曾把未定义点画成有值。**
- 现象：红色 Score 线一直画到 `lambda_prompt=1.00`。
- 发现：一致性审计时发现该点有效权重为 0，Score 实际未定义。
- 修正：Score 线只画有定义的点，该处标注 `NO_EFFECTIVE_EVIDENCE`；`run_all.py` 把这个标记列为必检项，防止回退。

**案例 3：70 条记录全部来自 AI 临时标注。**
- 风险：开发结果很容易被当成正式评价结果。
- 措施：所有产物带 `AI_PROVISIONAL / DEVELOPMENT_ONLY`；Gate 分析器拒绝 AI 标注作为输入；`run_all.py --mode formal` 在 Gate 未 PASS 时直接拒绝；结果表中 AIV 与 ranking 填 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

## 5. 可复现性（1 分钟）

- 干净克隆 → `pip install -r requirements.txt` → `python run_all.py`：5 步，29 项一致性检查全部通过，产物与仓库逐字节一致。
- 这些检查验证的是一致性与口径，不是效果。

## 6. 局限与下一步（1 分钟）

- 正式人工 R1/R2（单标注者 test-retest）尚未完成，Gate 为 PENDING。
- 当前不能声称：正式结论、学生真实能力、AI/prompt 因果效应、正式 AIV、排名。
- 16 条开发 Evidence 的结论不外推到 140 条正式样本或总体。
- 切换路径见 `FORMAL_GATE_SWITCH.md`：人工标注 → Gate PASS → formal 重跑。

## 7. 收尾（30 秒）

> **我们的贡献不只是给出一个分数，而是防止评价系统在证据不足时给出看似精确、实际上没有依据的数字。**

## 预备问答

- *为什么不给排名？* 排名需要正式人工标签通过 Gate；在此之前给出的排名没有测量依据。
- *Score 不变是不是说明模型好？* 不是。这是当前数据同质带来的代数结果，我们主动把它列为需要警惕的案例。
- *只有 16 条证据够吗？* 不够支撑正式结论，所以全部标为开发结果，并用 Support 指标把"证据有多少"显式报告出来。
