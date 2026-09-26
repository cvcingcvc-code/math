# NATIONAL COMPETITION FINAL GAP

> 国赛评委视角的只读差距审计。生成日期：2026-09-27。
> 本审计不改任何正式文件，只打分与列差距。状态：`COMPETITION_GAP_AUDIT = PASS`（交付物就绪，非评审结论）。

---

## 一、逐维度打分

| # | 维度 | 判定 | 说明 |
|---|---|---|---|
| A | 研究问题是否清楚 | PASS | measurement / identifiability 定位明确，且在摘要/引言/结论反复出现。 |
| B | 数学抽象是否充分 | PASS | 六层链路 + 公式 + Support/Coverage/Decision 定义完整。 |
| C | 模型假设是否明确 | PASS | Reliability 不是概率/不是因果系数；参数是透明声明假设，非 learned optimum。 |
| D | 公式解释是否自然 | PASS | 论文有「人话版本」：Observable / Confidence / Prompt / Context。 |
| E | 数据是否足够透明 | PASS | 明确区分 140 vs 70，明确 19/35/54 的语义。 |
| F | 五类验证是否围绕同一 RQ | PASS | 论文明确「五条攻击路径攻击同一命题」。 |
| G | Baseline 是否合理 | PASS | Raw-only 与主模型同 70 条记录对照，直接回答「不建 Reliability 会怎样」。 |
| H | Ablation 是否有意义 | PASS | 16→12→6→6 解释为 support accounting 变化，非 accuracy 提升。 |
| I | Sensitivity 是否防调参质疑 | PASS_WITH_LIMIT | 693 网格 + 0 翻转；已诚实声明是 local stability，非置信区间。 |
| J | Failure Case 是否真实有说服力 | PASS | P108/P105/P072/P035 均真实，且明确 AI_PROVISIONAL 标签。 |
| K | External Transfer 是否合理 | PASS | 定位为 structural validation，Gate3 负结果保留。 |
| L | ML Challenger 是否喧宾夺主 | PASS | 明确不是主模型、不选 winner。 |
| M | Claim Boundary 是否严谨 | PASS | 三条负结果 + 状态边界完整保留。 |
| N | Paper 是否像研究论文 | PASS | 结构完整、引用齐全、结论分级明确。 |
| O | PPT 是否像比赛路演 | MINOR_GAP | 10 页结构已到位，但逐页文字密度偏高，部分页仍需「口播锚点化」而非整句堆叠。 |
| P | Demo 是否像模型演示系统 | MINOR_GAP | 信息完整且冻结，但对首次进入的评委仍有信息偏多风险；演示路径依赖 runbook 而非页内引导。 |
| Q | 可复现性是否可信 | MINOR_GAP | 开发核心可复算，但「代码→数据生成→实验→图→论文/Demo」全链路未单命令重建；需在答辩口径上守住。 |
| R | 评委最可能攻击哪里 | 见下方 TOP 5 | 集中在「参数主观性」「16/70 证据量」「Score 不变=无效」「BTC 硬塞」「Human Gate 未做」。 |

---

## 二、TOP 5 COMPETITION GAPS

> 只列最关键的 5 个，不堆问题。

### GAP-1 · Reliability 定义可能被质疑「人为/主观」

- **问题**：`λ_prompt=0.5`、`λ_context=0.5`、`r_medium=0.75` 是声明参数，容易被问「为什么不是 0.4 或 0.6」。
- **影响**：若答成「我们定的」，会被认为模型是拍脑袋。
- **是否明天能修**：能，靠话术 + PPT 一页「参数是透明假设，用 693 格敏感性检验其影响」，不靠改模型。
- **成本**：30–45 分钟。
- **需改 Paper/PPT/Demo**：仅 PPT 措辞强化（不改数字、不重做）。
- **优先级**：P0

### GAP-2 · 16/70 readable 是否削弱证据

- **问题**：评委可能问「70 条里只有 16 条有用，结论能信吗」。
- **影响**：若不点破「16 条同质→公共缩放退化」这一机制，会显得证据稀薄。
- **是否明天能修**：能，把「54 不是 54 个零分，而是没有有效证据」作为开场锚点。
- **成本**：20 分钟。
- **需改 Paper/PPT/Demo**：PPT 口播 + 已有一页（第 4 页）强化即可。
- **优先级**：P0

### GAP-3 · Score 不变会被误解成「模型无效」

- **问题**：ABL/HOT/Gap 恒为 3.5625/0.375/1.125，评委可能问「分数没变，你这模型不是白做」。
- **影响**：这是最容易翻车的误读，必须主动讲「分数稳定 ≠ 证据支持稳定」。
- **是否明天能修**：能，主结论本身就是答案，只需在 PPT 与 Demo 路径里连续三次点破。
- **成本**：20 分钟。
- **需改 Paper/PPT/Demo**：不涉及内容变更，靠节奏。
- **优先级**：P0

### GAP-4 · External Transfer 是否显得「硬塞 BTC」

- **问题**：评委可能觉得「教育研究为何拿 BTC 来验证，是不是凑数」。
- **影响**：若不解释「刻意选一个 noisy-signal 域做 stress test」，会显得突兀。
- **是否明天能修**：能，用一句话讲清「同一结构能否跨域」+「Gate3 失败正是诚实边界」。
- **成本**：20 分钟。
- **需改 Paper/PPT/Demo**：PPT 第 8 页口播强化。
- **优先级**：P1

### GAP-5 · Human Gate NOT_RUN 如何防守

- **问题**：评委可能追问「人工验证没做，结论可信到什么程度」。
- **影响**：若含糊会损失可信度；若过度辩解会显得在掩盖。
- **是否明天能修**：能，靠「结论级别 = descriptive/structural/development-only」的口径一致性。
- **成本**：15 分钟（Q&A 背诵）。
- **需改 Paper/PPT/Demo**：无需改，已有边界页。
- **优先级**：P1

---

## 三、结论

- `COMPETITION_GAP_AUDIT = PASS`
- 无 MAJOR_GAP、无 NOT_FIXABLE_TONIGHT；核心研究故事已稳固。
- 剩余差距全部是「表达/节奏/Q&A」层，非「研究内容」层，均可在 2–4 小时内收敛。
- 今晚**不改**任何正式交付文件，全部差距留待明早按 `MORNING_OPTIMIZATION_PLAN.md` 处理。
