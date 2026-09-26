# CURRENT HANDOFF

1. 当前 Git 分支

`master`

2. 最新 commit SHA

本 handoff 更新提交后，以 `git log --oneline -1` 为准。

3. 当前唯一主任务

S4 Pilot Annotation Gate：等待真实人工 R1/R2。开发版比赛提交候选包已完成并可从干净克隆复现。

4. 已完成到哪一步（2026-09-26 比赛可提交化阶段）

- **复现输入收口**：AI_PROVISIONAL 开发数据 `data/annotations/ai/`、`src/development_data.py`、`src/run_development_experiment.py`、`src/run_reliability_sensitivity.py`、`src/annotation_gate_report.py` 的拒绝保护均已纳入 Git（`eee1a51`），全部仍为 `AI_PROVISIONAL / DEVELOPMENT_ONLY / formal_gate_eligible=false`。
- **run_all.py**：6 步（开发实验 → 信度敏感性 → 识别网格/Figure 3/4/Demo → 独立复算 → 结果 CSV → 核心闭环验收）+ 32 项一致性检查。
- **研究核心闭环已完成**：新增 `src/build_core_closure.py`，生成 Raw/Adjusted 指标、M0–M3 消融、4 条真实记录反例和研究结论；状态为 `RESEARCH_CORE_FROZEN_FOR_SUBMISSION`。该冻结只覆盖开发版测量闭环，不代表正式 Gate 或 Formal AIV 已通过。
- 核心数值：Raw ABL/HOT/Gap = 3.5625/0.375/1.125；在 λ_prompt=0.5、λ_context=0.5、confidence 权重下，Adjusted 数值相同，effective weight 由 16 降为 6，coverage 由 0.228571 降为 0.085714。
- **Figure 4 修正**：Score 线不再画到 `lambda_prompt=1.00`，该处标注 `NO_EFFECTIVE_EVIDENCE`（未定义，不是 0）；计算未改。
- **新增文件**：`requirements.txt`（pandas 3.0.6 / numpy 2.5.3，仅 wheel 安装）、`FORMAL_GATE_SWITCH.md`、`docs/data_dictionary.md`、`src/build_development_results_csv.py`、`paper/submission_candidate.md`、`reports/submission/`（reproduction_notes、roadshow_outline、record-level 与 summary 结果 CSV、run_all_report.json、`TEAMID_PENDING_paper_submission_candidate.html/.pdf` 5 页）。
- **结果 CSV**：记录级 70 行，16 行进入 Score 分母；AIV 与 ranking 全部 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。开发数据无验证过的学生级聚合，因此不提供学生级表。

5. Clean clone 验证（2026-09-26）

- `git clone` → 新 venv（Python 3.13.14）→ `pip install --only-binary=:all: -r requirements.txt` → `python run_all.py`
- `python run_all.py`：6 步全部退出码 0；**32/32 PASS**。
- `python run_all.py --mode formal` → `FORMAL_MODE_BLOCKED` / `RUN_ALL_FORMAL_BLOCKED`，退出码 1。

6. 当前 formal Gate 状态

`reports/annotation_gate_report.json`：`PENDING`。R1/R2 为空。formal 模式拒绝运行。未修改阈值、R1/R2、冻结手册。

7. 当前唯一阻塞

真实人工标签尚未返回，不能由 AI 临时标签或开发模型替代。

8. 下一步唯一动作

按冻结说明完成真实人工 R1；至少间隔 24 小时后同一标注者完成 R2；再运行 `python src/run_s4_gate.py`；流程见 `FORMAL_GATE_SWITCH.md`。

9. 尚未完成的比赛提交项

- **队号未知**：`reports/submission/TEAMID_PENDING_*` 需在得到队号后按 `队号_模块_文件名` 改名（论文 PDF/HTML；结果 CSV、复现包 ZIP 同样需要命名）。
- 复现包 ZIP 未打包（等队号）。
- 正式 AIV、学生排名、正式 Gate 结论：须 Gate PASS 后产生。
- 路演 PPT：只有大纲 `reports/submission/roadshow_outline.md`；`slides/` 目录为其他来源，未审阅。
- 论文 PDF 为 Markdown→Edge 打印版，未做正式排版；页数 5，未超 30 页限制。

10. 已冻结、禁止修改的文件/规则

- `data/annotations/human/pilot_worksheet_A.csv`（R1）、`pilot_worksheet_A_retest.csv`（R2）
- `docs/annotation/annotation_manual_v0.1.md`、`annotation_clarification_v0.1.1.md`
- `validation/gate_thresholds.json`
- `src/annotation_gate_report.py` 的正式 Gate 判定逻辑（本轮只提交了此前已存在的"拒绝 AI_PROVISIONAL 输入"保护，未改判定与阈值）
- Canonical Pilot `data/processed/pilot_sample.csv`
- D008 / D010 / D011 / D012

11. 未纳入 Git、来源未查明的文件（不覆盖、不删除、不提交、不追查）

- `paper/submission_candidate.html`、`paper/submission_candidate.pdf`
- `reports/development/core_figure_2_support_heatmap.svg`、`core_figure_5_model_flow.svg`
- `reports/development/identifiability_audit.*`、`provenance_separation_audit.*`
- `slides/`

以上均不是 `run_all.py`、论文、Figure 4、Demo 或结果 CSV 的依赖。

12. 本轮已纳入 Git 的核心闭环产物

- `src/build_core_closure.py`
- `reports/development/raw_adjusted_metrics.csv`
- `reports/development/ablation_results.csv`
- `reports/development/counterexamples.csv`
- `reports/development/research_core_closure.md|.json`

13. 非阻断备注

- 本机出现多次"写入已落盘但工具回执丢失"现象（Figure 4 08:40:17、paper html/pdf、run_all.py、FORMAL_GATE_SWITCH.md、commit `eee1a51`）；每次均用 stat / md5 / git show 核实内容与预期一致。
- Git Bash 中 `/tmp` 与 git 的路径映射不一致；clean clone 请使用 Windows 绝对路径（如 `C:/Users/lin/AppData/Local/Temp/...`）。
