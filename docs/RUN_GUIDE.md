# 运行指南与可复现流程

> 目标：任何新工具/新窗口不读聊天历史即可在本机复现检查与开发版流程。
> 只描述「怎么跑」；「跑到哪、下一步做什么」见 `handoff/PROJECT_NOW.md` 与 `handoff/NEXT_TASK.md`。

## 1. 环境

| 项 | 值 | 备注 |
|---|---|---|
| 工作目录 | 项目根目录 `C:\Users\lin\Documents\Codex\2026-09-25\yu` | 所有脚本用 `Path(__file__).parents[1]` 定位根目录，可在任意子目录调，但建议在根目录运行 |
| Python | **3.14.2**（实测通过） | 本机可用：`C:\Users\lin\AppData\Local\Programs\Python\Python314\python.exe` |
| pandas | 3.0.1（实测通过） | `requirements.txt` 钉 `pandas==3.0.6`，但本机现装 3.0.1 亦可跑通全部只读/开发脚本 |
| numpy | 2.4.1（实测通过） | `requirements.txt` 钉 `numpy==2.5.3` |
| 其它依赖 | 无 | 开发链路只用 pandas + numpy + 标准库 |

> **环境注意（本次核验发现）**：WorkBuddy 自带的 managed Python（`C:\Users\lin\.workbuddy\binaries\python\versions\3.13.12`）**未装 pandas**，直接 `python src/…` 会 `ModuleNotFoundError: No module named 'pandas'`。请使用装了 pandas 的 Python（系统 Python 3.14.2，或自建 venv 后 `pip install --only-binary=:all: -r requirements.txt`）。

安装依赖（若用全新 venv）：
```bash
python -m pip install --only-binary=:all: -r requirements.txt
```

## 2. 只读检查（默认、安全，不改数据）

这些脚本只读数据、不写源文件，可随时运行：

```bash
# 1) 冻结不变量核验（21 项 + 缺陷登记），输出到 work/s4_integrity_report.json
python src/verify_pilot_integrity.py

# 2) 可靠性库自检（Krippendorff α / Cohen κ，9 项）
python src/reliability.py

# 3) 多窗口协调状态（只读）
python scripts/project_manager.py status
python scripts/project_manager.py status --json
```

预期输出：
- `verify_pilot_integrity.py` → `INVARIANT CHECKS: 21/21 passed`，`DEFECT REGISTER: 2 open`（S4-F01、S4-F02）。
- `reliability.py` → 9/9 self-tests pass。
- `project_manager.py status` → 各 workstream 状态与 WRITE LOCKS。

## 3. 正式门禁链（需真实人工标注，禁止 AI 代跑）

```bash
python src/run_s4_gate.py
```

依次执行：可靠性自检 → 数据完整性核验 → 重建盲标表 → 若 R1/R2 均已填则生成 Gate Report。
当前 `reports/annotation_gate_report.json` 为 PENDING；R1/R2 未返回前不会产生正式一致性（D008）。

## 4. 开发版复现（DEVELOPMENT_ONLY，会写 reports/）

```bash
python run_all.py
```

6 步：run_development_experiment → run_reliability_sensitivity → run_partial_identification(--mode development) → recompute_bounds → build_development_results_csv → build_core_closure，然后 32 项一致性检查。
预期：`checks: 32/32 passed; result=PASS`。

```bash
python run_all.py --mode formal   # 期望被拒绝（fail-closed）：Gate 非 PASS 时输出 FORMAL_MODE_BLOCKED
```

> 开发版复现会**重新生成** `reports/` 下的派生文件与 `work/` 产物；不影响原始数据与人工标注。若担心覆盖，运行前先看 `git status` 与 `MULTIPROCESS_STATE.md` 的 WRITE_LOCKS。

## 5. Demo 本地预览（只读）

```bash
python reports/demo/serve_demo.py   # 启动本地服务（端口 4173），浏览器打开
```

或直接打开 `reports/demo/index.html`（顶部标注 `DEVELOPMENT_ONLY · AI_PROVISIONAL`）。

## 6. 检查方法小结

| 目的 | 命令 | 通过标志 |
|---|---|---|
| 数据完整 | `python src/verify_pilot_integrity.py` | 21/21 + 2 open defects |
| 可靠库 | `python src/reliability.py` | 9/9 |
| 开发复现 | `python run_all.py` | 32/32, result=PASS |
| 门禁状态 | 读 `reports/annotation_gate_report.json` | `status=PENDING`（未返回标签前） |
| 文档一致性 | `python src/development_submission_checker.py` | PASS |

## 7. 复现注意事项

- 清洗流程的**幂等性**：`run_all.py` 重复运行只重算派生数字，不回写 `data/processed/*` 与 `data/annotations/*` 原件；原始证据（原始 Excel 未入库、人工工作表原件）不会被覆盖。
- 人工工作表可用 UTF-8 或 GB18030 保存，读取器 `src/csv_safe_read.py` 两种编码兼容（只读、不回写）。
- 本任务不包含推送/发布/上传；`git remote` 当前未配置（预期仓库 `https://github.com/cvcingcvc-code/math` 待核验）。
