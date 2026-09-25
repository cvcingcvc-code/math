# 当前论文最大的 5 个比赛薄弱点

> 评估基于当前磁盘文件、Git 状态和已有开发审计。以下是比赛前最小修复建议，不改变冻结模型、正式数据、标注手册、Gate 阈值或核心代码。

## 1. 正式证据链尚未闭环，论文容易被看成“只有临时标签的漂亮演示”

### 为什么会失分
论文如果把 ABL/HOT/Gap 和图表放在结果中心，却没有先把 `AI_PROVISIONAL`、人工 R1/R2、Gate 和正式结果的层级讲清，评委会认为核心结论建立在未经验证的标签上。

### 当前已有证据
- `PROJECT_STATE.md` 明确为 `BLOCKED_BY_HUMAN_ANNOTATION`；
- 当前开发结果明确 `formal_gate_eligible=false`；
- 真实人工 R1/R2 仍为空；
- Gate、正式 Kappa/Alpha、正式 AIV 尚未产生。

### 比赛前最小修复方式
在摘要、方法、结果、图注和答辩开头统一增加状态声明；把开发结果单列为“识别诊断与模型行为演示”，并在论文中放置正式替换路径。人工标签返回后优先更新 Gate 和正式结果，不要把开发结果覆盖成正式结果。

## 2. 16 条可判读 Evidence 的完全分离既是亮点，也是最大解释风险

### 为什么会失分
评委可能认为 `prompt_induced=true`、`task_actor=ai`、`confidence=medium` 等结构是标签规则或数据管道制造的 artifact，而不是数据中的真实现象。若论文把它说成 prompt effect，就会被直接攻击因果越界。

### 当前已有证据
- provenance audit 显示 16 条可判读 Evidence 全部共享同一组字段；
- 识别审计显示对照单元格为空；
- 审计还指出 provisional 文件没有完整逐条生成脚本/决策日志，来源存在 `UNRESOLVED` 部分；
- 当前骨架已能区分数据生成、规则、provisional label、mapping 四类来源。

### 比赛前最小修复方式
把“完全分离”改写为识别诊断，不写成 prompt 因果发现；在正文或附录给出一张 provenance 分解表，并明确下一步人工复核的优先记录和待验证字段。保留 `selection + annotation-rule + provisional-label + mapping mixture` 的谨慎表述。

## 3. Bounds 的数学直觉还不够突出，评委可能误解“分数不变”为模型没有信息

### 为什么会失分
如果只展示 ABL/HOT/Gap 恒定，评委会问：既然参数怎么变分数都一样，为什么需要这个模型？他们可能认为惩罚项只是形式化包装，没有改变评价。

### 当前已有证据
- `partial_identification_summary.json` 显示分数范围几乎为单点；
- effective weight 从 0.4 到 16.0；
- effective coverage 从 0.0057 到 0.2286；
- `lambda_prompt=1` 时存在 33 个 undefined cells，状态应为 `NO_EFFECTIVE_EVIDENCE`。

### 比赛前最小修复方式
论文和 Demo 始终并列显示 Score、effective weight、effective coverage 和 status；口头上用一句话解释共同缩放导致的归一化分数稳定；重点展示 support collapse 与 undefined，而不要只展示一个平坦的 score 曲线。

## 4. 数据规模和结构限制会削弱“教育评价体系”的外推性

### 为什么会失分
当前开发分析只有 70 条输入、16 条可判读 Evidence，而且来源集中。评委可能认为这只能是一个小样本案例，无法支持学生级评价、跨 agent 比较或普遍性方法结论。

### 当前已有证据
- Canonical Pilot 为 140 条，但当前 development 输入为 70 条；
- 其中只有 16 条进入 L1–L6；
- `B009` 指出学生级证据稀疏、短 session 和 unknown agent 问题；
- 当前没有独立无 AI outcome，无法完成正式 AIV 因果识别。

### 比赛前最小修复方式
缩小论文声称：把当前贡献定位为“证据支持审计 + identification gate + bounds 框架”，不要包装成已经完成的学生评价系统。明确 70/140 的分母边界，并把扩展标注、分层收缩和正式 outcome 作为后续验证，而不是当前结果。

## 5. 论文、Demo 与 handoff 的状态口径容易出现不一致

### 为什么会失分
项目当前存在多个阶段文件和未提交产物；旧 handoff 某些位置仍有双人标注叙述，而最新冻结决定已采用单人 R1/R2 test-retest。如果答辩时混用“两个独立人工标注者”和“同一标注者重测”，会直接损害可信度。

### 当前已有证据
- 最新 `DECISIONS.md` 的 D016 明确 R1/R2 是同一标注者、间隔至少 24 小时的 test-retest；
- `PROJECT_STATE.md` 与 `CURRENT_HANDOFF.md` 说明人工标签为空；
- `ARTIFACT_INDEX.md` 记录 B010 已改为重测；
- Git 工作区仍有此前未提交的开发报告和代码修改。

### 比赛前最小修复方式
建立一份最终提交前的术语/状态清单：`AI_PROVISIONAL`、`DEVELOPMENT_ONLY`、`formal_gate_eligible=false`、`test-retest`、`not inter-rater`、`not causal`、`not formal AIV`。论文、PPT、Demo、handoff 全部逐项核对；在正式人工结果回来后再更新状态，不在本窗口修改冻结文件。

## 总体判断

当前最容易失分的不是公式本身，而是把一个很有价值的识别诊断故事讲成了“已经完成的教育 AI 评分模型”。最小修复方向不是增加算法，而是：

1. 把状态边界前置；
2. 把完全分离解释为待验证的识别结构；
3. 用 Score + Support 双报告呈现模型价值；
4. 严格区分 70 条开发数据、140 条 Canonical Pilot 和正式人工 Gate；
5. 统一所有材料中的 test-retest 与非因果口径。
