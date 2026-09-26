"""Render the Development Submission Candidate from final_results.json."""
from pathlib import Path
import html, json

ROOT = Path(__file__).resolve().parents[1]

def main():
    a = json.loads((ROOT / "outputs/final_results.json").read_text(encoding="utf-8"))
    d = a["development_results"]; raw = d["raw_summary"]; adj = d["adjusted_summary"]; t = a["transfer_validation"]
    md = f'''# 教育 AI 交互证据的可信评价：Development Submission Candidate

> **DEVELOPMENT_ONLY · NOT_HUMAN_VALIDATED**  
> Human Gate 未完成：`{a["human_validation"]["status"]}`；Formal Gate 为 `{a["human_validation"]["formal_gate_status"]}`；`formal_gate_eligible=false`。本文所有数值由 `outputs/final_results.json` 提供。

## Problem

AI 辅助学习中的最终文本同时包含学生思考、AI 引导、上下文缺失和标注不确定性。本文回答赛题的方式是建立一个**面向 AI 增量价值评价的证据支持框架**：先确认可观察 Student Evidence，再报告 Reliability 与 Adjusted Evaluation，而不是把当前开发结果解释为已经识别的真实增量或因果效应。

## Measurement Failure

开发样本共 `{a["data_identity"]["sample_count"]}` 条，其中 `{raw["included_evidence_count"]}` 条具有可判读 Student Evidence。`NO_EVIDENCE` 与 `UNDETERMINED` 不填成低分，权重为零时返回 `NO_EFFECTIVE_EVIDENCE`。

## Raw / Reliability / Adjusted

冻结模型为：`w_i = I(observable_i) × confidence_i × (1−λ_prompt prompt_i) × (1−λ_context context_i)`。

| 指标 | Raw | Adjusted |
|---|---:|---:|
| ABL | {raw["ABL"]:.4f} | {adj["ABL"]:.4f} |
| HOT | {raw["HOT"]:.4f} | {adj["HOT"]:.4f} |
| Task/Evidence Gap | {raw["Task_Evidence_Gap"]:.4f} | {adj["Task_Evidence_Gap"]:.4f} |
| Effective weight | {raw["effective_weight"]:.4f} | {adj["effective_weight"]:.4f} |
| Effective coverage | {raw["effective_coverage"]:.6f} | {adj["effective_coverage"]:.6f} |

核心开发现象是 Score 保持稳定，而 Evidence Support 下降。这不是正式人工验证结果，也不是因果效应。

## Sensitivity

What-if 接口覆盖 `lambda_prompt`、`lambda_context`、`r_medium`，每个参数使用 `-20%/-10%/baseline/+10%/+20%`。完整结果见 `reports/development/what_if_sensitivity.csv`，统一 artifact 内含全部 15 行。

## Ablation

M0–M3 共用同一确定性模型，仅逐步加入 confidence、prompt 和 context 修正。当前消融主要说明 Support 变化，不能证明预测准确率或独立 context 效应。

## Counterexamples

P105、P108、P072、P035 展示了高 Raw 分数、低支持度、上下文截断和 `NO_EFFECTIVE_EVIDENCE` 的不同组合。详细记录由 artifact 的 `counterexamples` 提供。

## External Transfer Validation

本节只同步已有公开行情验证，不重新调参、不声称交易策略：

- structural transfer：初步支持
- reliability separation：弱/部分支持
- sensitivity：DEVELOPMENT_ONLY_STRUCTURAL_SUPPORT（当前切片局部结果）
- risk–coverage improvement：未支持
- trading advantage：不得声称

源文件：`experiments/transfer_finance/transfer_validation.json`；仅作小型外部结构迁移验证。

## Limitations

Human Gate 尚未完成，结果保持 `DEVELOPMENT_ONLY`。当前数据缺少正式 HUMAN_VALIDATED 输入、充分的非 AI 对照、独立学习 outcome 和可可靠识别的原生 session。External Transfer Validation 不能提升教育主结果的正式验证等级。

## Conclusion

当前 Development Candidate 支持一个清晰的方法论结论：评价结果必须同时报告 Raw、Evidence Reliability、Adjusted 和 Evaluability。70 条开发记录中只有 16 条具有可判读 Evidence，54 条返回 `NO_EFFECTIVE_EVIDENCE`；Score 稳定不等于 Evidence Support 稳定。Formal 结论须等待 Human Gate 完成。
'''
    (ROOT / "paper/development_submission_candidate.md").write_text(md, encoding="utf-8")
    (ROOT / "paper/submission_candidate.md").write_text(md, encoding="utf-8")
    # Minimal HTML mirror for the existing paper preview.
    body = html.escape(md).replace('\n', '<br>')
    (ROOT / "paper/submission_candidate.html").write_text(f"<!doctype html><meta charset='utf-8'><title>Development Submission Candidate</title><style>body{{font-family:Arial;max-width:900px;margin:40px auto;line-height:1.6}}.wm{{color:#b45309;font-weight:bold}}</style><div class='wm'>DEVELOPMENT_ONLY · NOT_HUMAN_VALIDATED · formal_gate_eligible=false</div><pre style='white-space:pre-wrap'>{body}</pre>", encoding="utf-8")
    print("paper_candidate=written")

if __name__ == "__main__":
    main()
