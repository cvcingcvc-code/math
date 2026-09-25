# CHANGELOG

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

