# Reproduction Notes（DEVELOPMENT_ONLY）

> 本复现包只复现 **开发版** 结果：70 条 `AI_PROVISIONAL` 记录，`annotation_status=DEVELOPMENT_ONLY`，`formal_gate_eligible=false`。它**不**复现、也不声称正式 Gate、正式 AIV、学生排名或因果效应。

## 1. 环境

- Python：3.13（已验证 3.13.14，Windows）。
- 外部依赖：仅 `pandas`、`numpy`，版本见仓库根目录 `requirements.txt`。
- 安装（只用预编译 wheel，避免 pandas 源码构建失败）：

```bash
python -m venv .venv
.venv/Scripts/python -m pip install --only-binary=:all: -r requirements.txt   # Windows
# Linux/macOS: .venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
```

## 2. 运行（从仓库根目录）

```bash
python run_all.py                # 开发版完整链路 + 一致性检查
python run_all.py --mode formal  # 预期被拒绝，见第 5 节
```

`run_all.py` 先检查必需输入是否存在；缺失时输出 `RUN_ALL_BLOCKED` 并以退出码 2 结束，不会猜测或补齐。

## 3. 步骤与预期输出

| # | 命令 | 主要输出 |
|---|---|---|
| 1 | `src/run_development_experiment.py` | `reports/development/development_metrics.csv`、`development_results.json` |
| 2 | `src/run_reliability_sensitivity.py` | `reports/development/reliability_sensitivity.csv/.svg`、`reliability_model.json` |
| 3 | `src/run_partial_identification.py --mode development` | 693 格参数网格、**Figure 4**（`core_figure_4_bounds_support.svg`）、Figure 3、Demo 数据 `reports/demo/demo_payload.json`、`reports/paper/method_results_skeleton.md` |
| 4 | `src/verification/recompute_bounds.py` | 独立复算：`reports/verification/core_numbers_source_of_truth.json` 等 |
| 5 | `src/build_development_results_csv.py` | 开发版结果表：`reports/submission/development_results_record_level.csv`、`development_results_summary.csv` |

最终写出 `reports/submission/run_all_report.json`，并打印 `checks: 29/29 passed; result=PASS`。

## 4. 29 项检查的含义

原有 27 项加上结果 CSV 的 2 项，全部是**一致性与口径检查，不是效果验证**：

- 记录计数：70 / 16 / 19 / 35；参数网格 693 / 660 / 33。
- Score 在所有有定义格上恒为 ABL=3.5625、HOT=0.375、Gap=1.125（容差 1e-9）。
- effective weight 范围为 0.4–16.0；coverage 最大值 = 16/70、最小值 = 0.4/70，即**分母为全部 70 条记录**。
- source of truth、Demo payload 与 Demo HTML 都带有 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 标记。
- Figure 4 包含真实参数名、固定参数、`/ 70 development records`、`NO_EFFECTIVE_EVIDENCE` 和 “not a causal effect”。
- 正式 Gate 状态**不是** PASS（R1/R2 未完成时这就是预期状态）。
- 结果 CSV 共 70 行，其中 16 行计分；AIV 与 ranking 全部为 `NOT_AVAILABLE_PENDING_FORMAL_GATE`。

## 5. 为什么 formal 模式被拒绝

`run_all.py --mode formal` 转交 `src/run_partial_identification.py --mode formal` 执行。后者读取 `reports/annotation_gate_report.json`，只有同时满足 `gate_status == "PASS"` 且 `formal_gate_eligible == true` 才会运行。当前 Gate 报告为 PENDING，因此输出 `FORMAL_MODE_BLOCKED` 并以非零退出码结束。此外，`src/annotation_gate_report.py` 会拒绝任何 `AI_PROVISIONAL` / `DEVELOPMENT_ONLY` 数据进入正式 Gate。

## 6. 可以复现的内容

- 70 条开发记录中有 16 条可判读 Evidence（19 条 NO_EVIDENCE，35 条 UNDETERMINED）。
- 693 个参数组合中，660 个有定义，33 个无定义（全部位于 `lambda_prompt=1.0`）。
- Score 恒定；Evidence Support 从 0.2286 降到 0.0057，并在 `lambda_prompt=1` 时变为 `NO_EFFECTIVE_EVIDENCE`。
- Figure 4、Demo 数据和开发版结果 CSV。
- 同一输入重跑，输出逐字节一致（2026-09-26 在隔离副本与干净克隆中验证）。

## 7. 绝对不能声称已正式验证的内容

- 正式人工 R1/R2、test-retest 信度、Gate PASS。
- 正式 AIV、学生级排名、学生真实能力。
- prompt 或 agent 的因果效应、AI 增量价值的因果估计。
- “Score 稳定证明模型稳健”：当前 Score 稳定是 16 条 Evidence 参数字段完全相同带来的**公共缩放代数结果**。
- 把 16 条开发 Evidence 的结论外推到 140 条正式样本或总体。
