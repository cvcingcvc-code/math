# 路演 / 答辩大纲（DEVELOPMENT_ONLY 提交候选）

> 全程标注：70 条开发记录为 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。不出现 AIV 数值、排名或因果表述。

**核心一句话：AI 辅助学习评价中，分数看起来稳定，并不意味着证据真的可靠。**

**贡献一句话：我们的贡献不只是给出一个分数，而是防止评价系统在证据不足时给出看似精确、实际上没有依据的数字。**

## 1. 开场：一个看起来很稳的分数（1 分钟）

- AI 进入学习过程后，学生提交的文本混合了学生思考、AI 提示、上下文缺失。
- 我们看到的“稳定分数”，可能建立在越来越薄的学生证据上。
- 抛出问题：评委如何判断一个分数背后有多少真正属于学生的证据？

## 2. 我们报告两样东西，而不是一样（1.5 分钟）

- **Score**：ABL、HOT、Gap。
- **Evidence Support**：effective evidence weight，以及以全部 70 条记录为分母的 effective coverage。
- 有效权重为 0 时返回 `NO_EFFECTIVE_EVIDENCE`：**未定义，不是 0 分**。
- 展示 Figure 4：红线（Score）平直，蓝线（Support）从 0.2286 降到 0.0057，在 `lambda_prompt=1` 处断开并标注未定义。

## 3. 三个真实开发案例：我们最可能错在哪里，怎么发现并修正（4 分钟，主体）

**案例 1：Score 稳定，起初像“模型稳健”。**
- 现象：693 个参数组合中，660 个有定义组合的 Score 完全不变（ABL 3.5625、HOT 0.375、Gap 1.125）。
- 审计发现：16 条可判读 Evidence 的参数相关字段完全相同，所有权重同比例缩放，加权平均必然不变。
- 结论修正：这是**公共缩放结构的代数结果**，不是稳健性证据；论文与 Demo 均按此表述。

**案例 2：Figure 4 曾把未定义点画成有值。**
- 现象：旧图红色 Score 线一直画到 `lambda_prompt=1.00`，而此处有效权重为 0。
- 审计发现：图形把“无法计算”显示成“数值不变”，正是本项目要防止的错误。
- 修正：Score 线只画有定义的点，断点标注 `NO_EFFECTIVE_EVIDENCE`；`run_all.py` 把这个标注列为自动检查项，防止回退。

**案例 3：70 条开发记录全部来自 AI 临时标注。**
- 风险：AI 标注的结果很容易被当成正式人工评价。
- 设计：每个文件都带 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 标记；Gate 分析器拒收 AI 数据；`run_all.py --mode formal` 在 Gate 未 PASS 时直接拒绝运行。
- 结果表中 AIV 与 ranking 明确写 `NOT_AVAILABLE_PENDING_FORMAL_GATE`，不估算、不占位。

## 4. Demo 演示（2 分钟）

1. 顶部横幅：`DEVELOPMENT_ONLY · AI_PROVISIONAL`。
2. 70 条记录中只有 16 条进入 L1–L6（19 条 NO_EVIDENCE，35 条 UNDETERMINED）。
3. 拖动 `lambda_prompt`：Score 不动，Support 下降。
4. 拖到 1.0：状态变为 `NO_EFFECTIVE_EVIDENCE`，Score 不显示为 0。

## 5. 可复现与边界（1 分钟）

- 从干净 Git 克隆：安装 `requirements.txt` → `python run_all.py` → 6 步全部成功，32 项一致性检查全部通过，产物逐字节一致。
- 32 项是**一致性与口径检查**，不是效果验证。
- **不能声称**：正式 Gate 通过、正式 AIV、学生排名、学生真实能力、prompt/agent 的因果效应，或把 16 条开发 Evidence 外推到总体。

## 6. 下一步（30 秒）

- 同一标注者完成人工 R1，间隔至少 24 小时完成 R2 → 冻结阈值下运行 Gate。
- Gate PASS 后按 `FORMAL_GATE_SWITCH.md` 以 formal 模式重跑，替换开发版表格；Gate 不通过则报告不达标并缩小结论。

## 备答：评委可能的追问

- **为什么不直接给排名？** 没有通过 Gate 的人工标注，任何排名都是没有依据的精确数字。
- **Score 不变是不是说明模型没用？** 当前数据的 Evidence 完全同质，所以只能展示 Support 这一维的变化；异质数据下 Score 是否变化，需要正式数据检验，我们不用合成数据冒充结论。
- **为什么阈值是 0.667？** 这是事前冻结的操作性选择（Krippendorff 探索性下限惯例），看到结果后不得回改。

