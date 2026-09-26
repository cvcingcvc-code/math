## 2026-09-26 — 提交包验收与状态校正

- 以当前 Git 与 handoff 为准完成提交包验收：论文、Figure 4、Demo、Demo payload 与核心数字来源均可读取；开发数字与状态口径一致。
- 修正过期交付状态：`CURRENT_HANDOFF.md` 更新为实际 HEAD `f0c115f`；PENDING Gate 占位报告改为反映阈值文件已 `preregistered=true`，同时保留 Gate 未生成、R1/R2 未完成；历史 Figure 4 P1 标记改为已修复。
- 赛题终版文件实际列出四类提交物：论文 PDF、复现包 ZIP（含 README/环境/数据字典/run_all）、结果数据表 CSV、路演 PDF/PPT；当前仓库未发现这些最终封装物，命名和页数要求仍需提交前核对。
- `src/run_development_experiment.py` 与 `src/run_reliability_sensitivity.py` 因 pandas 环境安装失败，本轮标记为 `NOT RUN / BLOCKED_BY_PANDAS_ENVIRONMENT`，不得写成测试通过。
- 正式 R1/R2 Gate 保持未完成；未生成正式一致性系数、Gate PASS、正式 AIV 或学生排名。

## 2026-09-25（深夜）— Figure 4 与 Score/Support 口径修复

- 修复 `src/run_partial_identification.py` 的 Figure 4 标签并重新生成 `reports/development/core_figure_4_bounds_support.svg`：红线为 normalized Score（ABL/HOT/Gap）共同稳定水平，蓝线为 Evidence Support；横轴为 `lambda_prompt`，固定 `lambda_context=0.00`、`r_medium=0.75`。
- 图中明确 `effective coverage = effective weight / 70 development records`，并说明当前稳定来自 16 条可判读 Evidence 的公共缩放结构，不是因果效应；零支持进入 `NO_EFFECTIVE_EVIDENCE`。
- 论文 `competition_paper_narrative_draft.md`、`paper_ready_development_draft.md`、`judge_story_3min.md` 与 Demo 卡片统一 coverage 分母口径。
- 阶段提交：`2359fbf`。

## 2026-09-25（深夜）— Partial Identification 独立数值复算

- 新增 `src/verification/recompute_bounds.py`：不导入生产 Bounds 函数，直接读取 `data/annotations/ai/pilot_ai_provisional.csv`，独立重建 21×11×3 参数网格并计算 ABL/HOT/Gap、effective weight、coverage 与 undefined。
- 独立复现：70 条记录、16 条可判读 Evidence、693 个参数条件、660 defined、33 undefined；ABL=3.5625、HOT=0.375、Gap=1.125；weight=0.4–16.0；coverage=0.005714...–0.228571...。
- 确认 coverage 分母为全部 70 条 development records，不是 16 条 Evidence；基线 coverage=12/70=0.171428...。
- 确认所有可判读 Evidence 共享 prompt=true、context=false、confidence=medium、actor=ai，因此惩罚项形成公共缩放，归一化分数稳定但 support 下降。
- 新增 `reports/verification/` 下 raw recount、独立复算 CSV/JSON、Demo 一致性、论文数字一致性、source of truth 与 reproduction review。
- P0=0、P1=1、P2=1。P1 为 Figure 4 SVG 标题暗示 Score+Support 但实际仅画 coverage，横轴为 `x`；P2 为 coverage 首次出现时应显式标明 denominator=70。
- 未修改 Partial Identification 主公式、数据、标签、R1/R2、manual、Gate threshold、Demo UI 或论文叙事主体。

## 2026-09-25（晚）— 论文主叙事与评委答辩收口

- 新增 `reports/paper/competition_paper_narrative_draft.md`：按 Problem Background → Research Question → Measurement Problem → Identification Strategy → Mathematical Model → Development Findings → Extreme Case → Limitations → Formal Validation Path 重构竞赛论文主叙事。
- 新增 `reports/paper/judge_story_3min.md`：面向第一次接触项目评委的约 3 分钟口头稿。
- 新增 `reports/paper/elevator_pitch_30s.md`：问题→方法→发现→价值的 30 秒版本。
- 新增 `reports/paper/core_figures_interpretation.md`：为四张核心图补充论文级图名、caption、评委可读结论与不可推出事项。
- 新增 `reports/review/judge_attack_questions.md`：18 个潜在评委攻击问题及短答，明确不掩盖 AI provisional、识别不足和非因果边界。
- 新增 `reports/review/top_5_paper_weaknesses.md`：从评委角度判断当前最容易失分的五个地方及最小修复方式。
- 全部叙事保持 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` / `formal_gate_eligible=false`；未修改正式人工 R1/R2、标注手册、Gate 阈值、原始数据、provisional 标签、Partial Identification 数学定义或 Demo 实现。
- 核心主线固定为：**Score Stability ≠ Evidence Support Stability**。


## 2026-09-25（晚）— DEVELOPMENT_ONLY Evidence Reliability / Bias Correction 敏感性模型

- 新增 `src/run_reliability_sensitivity.py`，只读 `data/annotations/ai/pilot_ai_provisional.csv`，不训练复杂模型、不计算正式 AIV。
- 使用透明权重：`w_i=I(observable_i)*c_i*(1-lambda_prompt*prompt_i)*(1-lambda_context*truncation_i)`；`c_i` 采用 high=1、medium=0.75、low=0.5，prompt/context 惩罚均以有限网格敏感性分析，不宣称唯一参数。
- 生成 `reports/development/reliability_sensitivity.csv`、`reliability_model.json`、`reliability_sensitivity.svg`；15 个参数条件，全部保留 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。
- 运行验证通过：70 条输入、身份未丢失、输出可重复；未修改 R1/R2、Gate、冻结标注手册、阈值和原始数据。

## 2026-09-25（晚）— DEVELOPMENT_ONLY 最小建模指标链路

- 新增 `src/run_development_experiment.py`，显式读取 `data/annotations/ai/pilot_ai_provisional.csv`，不训练监督分类器。
- 采用 Module C 已有透明候选：数值化 `student_evidence_bloom` 的 ABL、L4-L6 的 HOT、可判读覆盖率、`task_level - evidence_level` gap；另报 prompt/context/置信度描述统计。
- 输出 `reports/development/development_metrics.csv` 与 `reports/development/development_results.json`，结果逐行保留 `annotation_source=AI_PROVISIONAL`、`annotation_status=DEVELOPMENT_ONLY`，并写入 `NOT FOR FORMAL GATE OR FINAL CLAIMS`。
- 70/70 行成功执行；重复运行成功；`formal_gate_eligible=false`。未运行完整模型、未计算正式 Gate，未修改 R1/R2、冻结手册、Gate 阈值、原始数据或正式 Gate 判定逻辑。

## 2026-09-25（晚）— 开发数据入口与正式 Gate 隔离

- 新增 `src/development_data.py`：默认 `formal` 保持读取 `data/processed/pilot_ai_prelabel.csv`；显式 `--mode development` 才读取 `data/annotations/ai/pilot_ai_provisional.csv`。
- 开发模式启动输出固定包含 `DEVELOPMENT_ONLY / AI_PROVISIONAL`，并校验 70 行、`record_id` 唯一、`annotation_source` 与 `annotation_status` 不得漂移。
- `src/annotation_gate_report.py` 增加拒绝保护：`AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 数据不能作为正式 Gate 输入。
- 最小测试通过；未运行完整模型、未计算正式 Gate，未修改 R1/R2、冻结手册或 Gate 阈值。

## 2026-09-25（晚）— 指标可计算性审计（无标签）

- 新增 `src/indicator_feasibility_audit.py`（只读 `clean_interactions.csv` 结构；情景部分读 AI 预标注但明确标为假设）。
- 新增 `reports/indicator_feasibility_audit.md|.json`。
- 发现（事实，结构层面）：每 session_proxy 学生轮中位数 = 2（秋/春）；≥3 学生轮 session 占 41.5% / 34.7%；每生学生轮中位数 8 / 9；unknown agent 全部集中在春季（春季 turn 的 36.8%，秋季 0%）。
- 情景（假设，非人工结果）：若有等级证据比例≈AI 预标注值（秋 0.50、春 0.21），每生期望证据轮中位数 4.0 / 1.9，中位学生 HOT 最坏标准误 0.25 / 0.36 → 学生级独立比例估计不足以支撑个体排名。登记为 B009。
- 未改动任何源数据、标注文件、manual、阈值或 DECISIONS。Gate 状态不变。

## 2026-09-25 — S4 标注协议收口与盲标包交付

### 1. 数据完整性核验（新增 `src/verify_pilot_integrity.py`）

21/21 冻结不变量通过：Pilot N=140、ID P001–P140 唯一、无旧 56 条混入、140/140 为 student turn、
预标注 140 行且 `annotator_type=LLM_EXPLORATORY_NOT_HUMAN`、复核队列 70=50+20、
manual V0.1 与 template 的 SHA-256 与既有记录一致、unknown agent 保留。
`prior_ai_context` 可独立重建复现（prelabel 140/140、queue 70/70）。**未改动任何源数据。**

### 2. 缺陷登记（新发现，均未修改源数据）

| ID | 级别 | 事实 | 处置 |
|---|---|---|---|
| S4-F01 | HIGH | `pilot_sample.csv::ai_context_text` 是**未来** AI 内容：48/140 条该 source_row 内无更早 AI 轮但该列非空，其中 45 条与其后的 AI 轮匹配（26 条完全相同、63 条为前缀） | 标注路径一律不使用该列；前文由 `clean_interactions.csv` 轮次顺序严格重建 |
| S4-F02 | HIGH | `pilot_human_review_queue.csv` 已在 `task_bloom`/`student_evidence_bloom`/`confidence`/`reason`/`content_source_attribution` 填入 AI 预标注，且含 `agent_type`/`path_case`，不能直接下发 | 改发盲标表；映射另存 `_keys/` |

### 3. 新增文件

| Path | Size (bytes) | SHA-256 | 说明 |
|---|---:|---|---|
| `docs/annotation/annotation_clarification_v0.1.1.md` | 12926 | `84319152CDC4EAB6BA7C47FC4D238C0777FC9E6A55F78BE7D4CE680FC28888C2` | 8 个失败点的可执行判定程序；不改 V0.1 判级语义；**待负责人签署** |
| `data/annotations/human/pilot_worksheet_A.csv` | — | `C638B4BF1851B93EC27845F581B89BFFBB7522948071CE1A419D3FAF5607FD27` | 盲标表 A，70 行，标签列全空，泄漏列 0 |
| `data/annotations/human/pilot_worksheet_B.csv` | — | `C638B4BF1851B93EC27845F581B89BFFBB7522948071CE1A419D3FAF5607FD27` | 盲标表 B（与 A 同序同内容，以文件名为标识） |
| `data/annotations/human/README_ANNOTATOR.md` | 6660 | — | 标注者执行说明 |
| `data/annotations/_keys/pilot_worksheet_key.csv` | — | `4AC4E2E94558DF3113E55E1FA912F30088A0D7B7DFA3F5A81A6591E9ECAC7BBD` | 分析侧映射（agent/path/抽样/预标注/顺序） |
| `validation/gate_thresholds.json` | — | `8A0160EF7B0B9311970881AD54087199E31519044CD4F6CC4A7C7976DE9A0CD8` | 候选阈值，`preregistered=false` |
| `src/run_s4_gate.py` | — | `C885EC116CAFE7839928CD25C3F912CD0BCA13CC3539EB27168D9DC2C91F16A6` | S4 Gate 一键入口 |
| `src/reliability.py` | — | `FC69CADACA280ECA3E950888BEB66BF08A23E95BAD737CEB0E77F498566E98AF` | Krippendorff α / Cohen κ，9/9 手算自检通过 |
| `src/verify_pilot_integrity.py` | — | `A6DFA03F55121F5F2ECF7E5583C22E1F595B321D6749AC38BBCE5823C6F061F1` | 不变量核验 + 缺陷登记 |
| `src/build_annotation_worksheets.py` | — | `BE0B4DA2896D4323FF4F2154E907E26744BBB22395379C2F44B421E691FD4DA4` | 盲标表生成 |
| `src/annotation_gate_report.py` | — | `046EE5D10F54D9D10F9D18F23B257632F9F230E211A006E1D071BC11DCF5C592` | Gate Report 生成 |

### 4. 修改文件

- `handoff/PROJECT_STATE.md`：状态 `BLOCKED_BY_ANNOTATION` → `READY_FOR_ANNOTATION`；加入完整性核验结论、缺陷登记、待签署项。
- `handoff/NEXT_TASK.md`：改为"两名人工标注者执行盲标 → 运行 `src/run_s4_gate.py`"，列出前置签署项。
- `handoff/BLOCKERS.md`：B002 转 ADDRESSED；新增 B006（未来内容泄漏）、B007（非盲标队列，已解决）、B008（140 vs 70 口径待裁定）。
- `handoff/ARTIFACT_INDEX.md`：补齐 `src/`、盲标表、澄清件、阈值文件与 PENDING 报告。
- `reports/annotation_gate_report.md|.json`：写入 PENDING 占位说明（**不是** Gate 结果）。

### 5. 未做（有意）

- 未生成任何人工标签、未计算任何一致性系数（D008）。
- 未修改 `annotation_manual_v0.1.md`（hash 不变）、未锁定 V0.2。
- 未执行 `--scope all`（140 条）版本，以免改变冻结抽样设计（待 B008 裁定）。
- 未修改 `handoff/DECISIONS.md`（D014：重大决策须 Gate Review 由负责人确认）。

### 6. 环境记录

Python 3.14.2 / pandas 3.0.1 / numpy 2.4.1 / scipy 1.18.0 / scikit-learn 1.9.0。
`krippendorff` 包未安装，因此 α 在仓库内自行实现，保证复现包离线可跑。

## 2026-09-25（19:00–19:12）— B010 单人重测通道（工具，不含任何标签）

- 新增 `src/build_retest_worksheet.py` → `data/annotations/human/pilot_worksheet_A_retest.csv`（70 行，同一 record 集合，种子 20260926，与第 1 轮位置相同 0 条，顺序 Spearman −0.26，标签列全空，无泄漏列）；自检报告 `work/retest_build_report.json`（pass=true）。
- `src/solo_retest_gate.py report --r1 … --r2 …`：检查 R1→R2 ≥24h，调用现有 `annotation_gate_report.py`，输出 `reports/solo_retest_gate_report.md|.json` 并在报告头加“单人重测、非评定者间”横幅。
- 管线测试（**仅合成 e2e 数据，不是研究结果**）：相同标签换序 → 全部一致性指标 = 1.0；B 表换成重测顺序 → 分析器输出与原顺序完全相同（行顺序无关）。
- 未改动：`pilot_worksheet_A.csv`、`pilot_worksheet_B.csv`、`_keys/`、`annotation_gate_report.py`、`gate_thresholds.json`、DECISIONS。
- 人工标签仍为 0/70，Gate 仍 BLOCKED。

## 2026-09-25 19:51 — S4 Gate 冻结提交

- B008 冻结：当前 Pilot Gate 使用 70 条核心样本；Canonical Pilot 140 条保留，其余 70 条暂不要求人工标签。
- B010 冻结：R1/R2 单人间隔重测，至少 24 小时；最终只称 test-retest reliability，不称 inter-rater reliability。
- `validation/gate_thresholds.json` 已在真实人工标签产生前设为 `preregistered=true`；V0.1.1 澄清件已冻结，不得根据 R1 结果临时改版。
- 首次 Git 提交：`d04c3d813fbd8ed4754a62fc3b55f616fc6ada21`；提交时间 `2026-09-25T19:51:01+08:00`；提交后工作区 clean。
- `work/` 为本地审计/临时产物，未进入 Git；原始 140 条 Pilot 数据与盲标材料已进入 Git。未发现 API key、secret、token 文件。
- 本轮未填写真实标签、未运行真实 Gate、未计算真实一致性结果。
- 阈值口径核对：分析器已有 exact agreement、Cohen kappa、quadratic weighted kappa、六级/三阶 alpha、混淆矩阵与 CI；相邻一致率/总 disagreement rate 没有既有独立 Gate 阈值，本轮未擅自新增或编造。
- 当前冻结后的唯一下一步：开始第一轮人工标注 R1；不得先运行真实 Gate 或填写 R2。

# 2026-09-26 — Research core closure

- 新增 `src/build_core_closure.py`，沿用既有 reliability weight 公式生成 Raw/Adjusted 指标、M0–M3 消融、4 条真实记录反例与六问研究结论。
- 生成 `reports/development/raw_adjusted_metrics.csv`、`ablation_results.csv`、`counterexamples.csv`、`research_core_closure.md|.json`。
- `run_all.py` 纳入核心闭环步骤；6 步、32/32 checks 通过。
- 开发版结论：Raw ABL/HOT/Gap=3.5625/0.375/1.125；调整后分数保持不变，effective weight 16→6，coverage 0.228571→0.085714；16 条可判读 Evidence 全部 prompt-induced。
- 未修改正式 R1/R2、Gate 阈值、冻结标注手册、原始数据或 Formal AIV 边界；来源不明的未跟踪成果未纳入。

# 2026-09-26 — Align Gate runner with frozen test-retest design

- 修正 `src/run_s4_gate.py` 的入口行为：默认使用 R1 `pilot_worksheet_A.csv` 与 R2 `pilot_worksheet_A_retest.csv`，保留已存在文件，不再以旧 B 表覆盖人工输入。
- Gate 占位报告同步标注 `single_annotator_test_retest` / `inter_rater=false`；正式 Gate 判定逻辑与阈值未改。
- 空标签状态下运行 `python src/run_s4_gate.py`：21/21 integrity checks 通过，正确保持 PENDING。

- 2026-09-26: completed 10-slide roadshow deck, assembled development-only submission package, updated README/reproduction status to 6 steps/32 checks, audited untracked files without deletion, and reran run_all.py (32/32 PASS). Formal R1/Gate untouched.

# 2026-09-26 — Human R1 checkpoint + Gate 编码修复 + Demo 口径修复

- **R1 保护**：为已开始填写的 `data/annotations/human/pilot_worksheet_A.csv` 建立备份（`work/backups/…_2026-09-26_1117_checkpoint.csv`）并提交 Git 检查点 `e8d4f67`；未改动任何标签。R1 状态记为 `IN_PROGRESS`（检查点 1/70），R2 `NOT_STARTED`，Formal Gate `NOT_RUN`。
- **修复 Gate 读取编码崩溃（P0）**：负责人编辑器将 R1 保存为 GB18030，`src/run_s4_gate.py` 读取时 `UnicodeDecodeError`。新增 `src/csv_safe_read.py`（只读检测 UTF-8/GB18030），`src/run_s4_gate.py`、`src/annotation_gate_report.py`、`src/solo_retest_gate.py` 改用该读取器；不修改、不回写人工文件。用 GB18030 合成工作表完成 Gate 报告端到端软件测试。
- **修复 Demo coverage 分母（P3）**：`reports/demo/index.html` 原先按 16 条可判读记录计算 effective coverage（显示 75%），与论文/报告的分母 70 不一致；改为 `total / 70`，基线恢复 17.14%。
- **Demo 增强（P4）**：Panel C 增加 Raw baseline（λ=0）与 Adjusted Score 标注；新增 Panel E · Counterexamples（读取 `reports/development/counterexamples.csv`）；保留 `NO_EFFECTIVE_EVIDENCE`（不填 0）。Node 运行时自检 10/10 通过。
- **提交包同步**：`outputs/submission_package_development_only/` 更新 `demo/index.html`、补入 4 张核心图至 `development/`，重新生成 MANIFEST（35 项逐一核对一致）。
- `python run_all.py`：6 步 32/32 PASS；`python src/run_s4_gate.py` 在 R2 空白时保持 PENDING，R1 文件哈希前后不变。
- 未修改：论文主体、冻结阈值、标注手册/澄清件、provisional 标签、正式 Gate 判定逻辑。


