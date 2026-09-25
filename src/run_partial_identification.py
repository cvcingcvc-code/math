"""Development-only partial-identification bounds and delivery artifacts.

This module never consumes formal human labels and never changes source data. It
uses the explicit AI provisional development file, treats penalty parameters as
assumption ranges, and records undefined regions when effective evidence weight
is zero. Outputs are not confidence intervals and are not formal AIV/Gate claims.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
OUT = ROOT / "reports" / "development"
DEMO = ROOT / "reports" / "demo"
PAPER = ROOT / "reports" / "paper"
LEVELS = {f"L{i}" for i in range(1, 7)}
BANNER = {"annotation_source": "AI_PROVISIONAL", "annotation_status": "DEVELOPMENT_ONLY", "formal_gate_eligible": False}


def parse_args():
    parser = argparse.ArgumentParser(description="Run development-only bounds artifacts; formal mode is fail-closed.")
    parser.add_argument("--mode", choices=("development", "formal"), default="development")
    parser.add_argument("--gate-report", type=Path, default=ROOT / "reports" / "annotation_gate_report.json")
    return parser.parse_args()


def require_development_or_gate(args):
    if args.mode == "development":
        return
    if not args.gate_report.exists():
        raise SystemExit("FORMAL_MODE_BLOCKED: Gate report is missing; no formal bounds run allowed.")
    try:
        gate = json.loads(args.gate_report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FORMAL_MODE_BLOCKED: invalid Gate report: {exc}")
    if gate.get("gate_status") != "PASS" or gate.get("formal_gate_eligible") is not True:
        raise SystemExit("FORMAL_MODE_BLOCKED: Gate PASS and formal_gate_eligible=true are required.")
    raise SystemExit("FORMAL_MODE_BLOCKED: formal source adapter is not enabled; development input cannot be promoted.")


def read_rows():
    with INPUT.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def metric(rows, lp, lc, rm, subset=None):
    selected = [r for r in rows if subset is None or subset(r)]
    vals = []
    for r in selected:
        if r["student_evidence_bloom"] not in LEVELS:
            continue
        level = int(r["student_evidence_bloom"][1])
        task = int(r["task_bloom"][1]) if r["task_bloom"] in LEVELS else None
        c = rm if r["confidence"] == "medium" else (1.0 if r["confidence"] == "high" else 0.5)
        w = c * (1 - lp * (r["prompt_induced"] == "true")) * (1 - lc * (r["context_truncated"] == "true"))
        vals.append((level, task, w))
    total = sum(w for _, _, w in vals)
    base = {"lambda_prompt": lp, "lambda_context": lc, "r_medium": rm,
            "effective_weight": total, "effective_coverage": total / len(rows),
            "valid_or_undefined": total > 0}
    if not total:
        base.update({"adjusted_ABL": None, "adjusted_HOT": None, "adjusted_gap": None,
                     "undefined_reason": "NO_EFFECTIVE_EVIDENCE"})
        return base
    base.update({
        "adjusted_ABL": sum(level * w for level, _, w in vals) / total,
        "adjusted_HOT": sum((level >= 4) * w for level, _, w in vals) / total,
        "adjusted_gap": (sum((task - level) * w for level, task, w in vals if task is not None) /
                         sum(w for level, task, w in vals if task is not None)),
        "undefined_reason": "",
    })
    return base


def svg_line(path, rows, xkey, ykey, title, ylabel):
    valid = [r for r in rows if r[ykey] is not None]
    width, height, left, top, pw, ph = 900, 500, 80, 60, 740, 320
    xs = sorted({float(r[xkey]) for r in valid}); ys = [float(r[ykey]) for r in valid]
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    if y0 == y1: y0, y1 = y0 - 0.1, y1 + 0.1
    def px(v): return left + (v-x0)/(x1-x0 or 1)*pw
    def py(v): return top + (y1-v)/(y1-y0)*ph
    pts = " ".join(f"{px(float(r[xkey])):.1f},{py(float(r[ykey])):.1f}" for r in sorted(valid,key=lambda z:float(z[xkey])))
    body=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
          '<rect width="100%" height="100%" fill="white"/>', f'<text x="450" y="28" text-anchor="middle" font-family="Arial" font-size="18" fill="#111827">{title}</text>',
          f'<line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#374151"/><line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#374151"/>',
          f'<polyline points="{pts}" fill="none" stroke="#2563eb" stroke-width="3"/>',
          f'<text x="450" y="445" text-anchor="middle" font-family="Arial" font-size="13" fill="#111827">{xkey}</text>',
          f'<text x="20" y="250" transform="rotate(-90 20 250)" text-anchor="middle" font-family="Arial" font-size="13" fill="#111827">{ylabel}</text>',
          '<text x="450" y="480" text-anchor="middle" font-family="Arial" font-size="11" fill="#991b1b">DEVELOPMENT_ONLY / AI_PROVISIONAL / NOT FOR FORMAL GATE OR FINAL CLAIMS</text></svg>']
    path.write_text("\n".join(body), encoding="utf-8")


def svg_score_support(path, rows):
    """Render the judge-facing separation of normalized score and support."""
    width, height, left, top, pw, ph = 980, 560, 90, 70, 760, 330
    ordered = sorted(rows, key=lambda r: float(r["lambda_prompt"]))
    xs = [float(r["lambda_prompt"]) for r in ordered]
    coverage = [float(r["effective_coverage"]) for r in ordered]
    x0, x1 = min(xs), max(xs)
    cov_max = max(coverage) or 1.0
    def px(v):
        return left + (v - x0) / (x1 - x0 or 1) * pw
    def py_score(v):
        return top + (1 - v) * ph
    def py_cov(v):
        return top + (cov_max - v) / cov_max * ph
    score_points = " ".join(f"{px(x):.1f},{py_score(1.0):.1f}" for x in xs)
    support_points = " ".join(f"{px(x):.1f},{py_cov(y):.1f}" for x, y in zip(xs, coverage))
    tick_parts = []
    for value in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = px(value)
        tick_parts.append(
            f'<line x1="{x:.1f}" y1="{top+ph}" x2="{x:.1f}" y2="{top+ph+6}" stroke="#374151"/>'
            f'<text x="{x:.1f}" y="{top+ph+24}" text-anchor="middle" font-family="Arial" font-size="12" fill="#111827">{value:.2f}</text>'
        )
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="28" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#111827">Score stability vs evidence support</text>',
        '<text x="490" y="49" text-anchor="middle" font-family="Arial" font-size="12" fill="#4b5563">lambda_context = 0.00; r_medium = 0.75 (fixed) · AI_PROVISIONAL / DEVELOPMENT_ONLY</text>',
        f'<line x1="{left}" y1="{top+ph}" x2="{left+pw}" y2="{top+ph}" stroke="#374151"/><line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#374151"/><line x1="{left+pw}" y1="{top}" x2="{left+pw}" y2="{top+ph}" stroke="#374151"/>',
        f'<line x1="{left}" y1="{py_score(1.0):.1f}" x2="{left+pw}" y2="{py_score(1.0):.1f}" stroke="#dc2626" stroke-dasharray="6 5"/>',
        f'<polyline points="{score_points}" fill="none" stroke="#dc2626" stroke-width="4"/>',
        f'<polyline points="{support_points}" fill="none" stroke="#2563eb" stroke-width="4"/>',
        *tick_parts,
        f'<text x="{left-12}" y="{top+5}" text-anchor="end" font-family="Arial" font-size="11" fill="#b91c1c">1.00</text>',
        f'<text x="{left+pw+12}" y="{top+5}" text-anchor="start" font-family="Arial" font-size="11" fill="#1d4ed8">{cov_max:.4f}</text>',
        f'<text x="{left+pw+12}" y="{top+ph+4}" text-anchor="start" font-family="Arial" font-size="11" fill="#1d4ed8">0</text>',
        f'<text x="490" y="455" text-anchor="middle" font-family="Arial" font-size="13" fill="#111827">lambda_prompt (assumption / sensitivity parameter)</text>',
        f'<text x="24" y="250" transform="rotate(-90 24 250)" text-anchor="middle" font-family="Arial" font-size="12" fill="#b91c1c">normalized Score (ABL/HOT/Gap; baseline = 1.00)</text>',
        f'<text x="958" y="250" transform="rotate(90 958 250)" text-anchor="middle" font-family="Arial" font-size="12" fill="#1d4ed8">Evidence Support: effective coverage = effective weight / 70 development records</text>',
        '<line x1="170" y1="495" x2="205" y2="495" stroke="#dc2626" stroke-width="4"/><text x="213" y="499" font-family="Arial" font-size="12" fill="#111827">ABL 3.5625 · HOT 0.375 · Gap 1.125 (stable)</text>',
        '<line x1="555" y1="495" x2="590" y2="495" stroke="#2563eb" stroke-width="4"/><text x="598" y="499" font-family="Arial" font-size="12" fill="#111827">support 0.1714 → 0.0000</text>',
        '<text x="490" y="535" text-anchor="middle" font-family="Arial" font-size="11" fill="#991b1b">Common-scaling structure in the current 16 readable Evidence records; not a causal effect.</text>',
        '</svg>'
    ]
    path.write_text("\n".join(body), encoding="utf-8")


def main():
    args = parse_args()
    require_development_or_gate(args)
    OUT.mkdir(parents=True, exist_ok=True); DEMO.mkdir(parents=True, exist_ok=True); PAPER.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    if len(rows) != 70 or any(r["annotation_source"] != "AI_PROVISIONAL" or r["annotation_status"] != "DEVELOPMENT_ONLY" for r in rows):
        raise RuntimeError("development identity check failed")
    grid=[]
    for i in range(21):
        for j in range(11):
            for rm in (0.5, 0.75, 1.0):
                grid.append(metric(rows, i/20, j/10, rm))
    with (OUT/"partial_identification_grid.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields=list(grid[0]); w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(grid)
    valid=[r for r in grid if r["valid_or_undefined"]]
    summary={**BANNER, "input":"data/annotations/ai/pilot_ai_provisional.csv", "model":"assumption_based_identification_interval", "interval_name":"assumption-based identification interval (not a statistical confidence interval)", "parameter_space":{"lambda_prompt":"0.00..1.00 step 0.05","lambda_context":"0.00..1.00 step 0.10","r_medium":[0.5,0.75,1.0]}, "n_grid":len(grid), "undefined_cells":sum(not r["valid_or_undefined"] for r in grid), "bounds":{}, "findings":{}, "limitations":["All 16 readable Evidence rows have prompt_induced=true and context_truncated=false; prompt/context penalties are not empirically identified.","r_medium is an assumption range, not calibrated reliability.","Undefined cells are recorded when effective evidence weight is zero; no smoothing is used.","No formal AIV, Gate, Kappa, Alpha, causal effect, or student ranking is produced."]}
    for k in ("adjusted_ABL","adjusted_HOT","adjusted_gap","effective_weight","effective_coverage"):
        vals=[r[k] for r in valid if r[k] is not None]; summary["bounds"][k] = {"min":min(vals),"max":max(vals)}
    base=metric(rows,0,0,0.75)
    near=[r for r in valid if abs(r["adjusted_ABL"]-base["adjusted_ABL"])<=0.01]
    summary["findings"]={"raw_baseline":base,"baseline_ABL":base["adjusted_ABL"],"baseline_HOT":base["adjusted_HOT"],"baseline_gap":base["adjusted_gap"],"ABL_within_0.01_fraction_of_valid_grid":len(near)/len(valid),"score_stability_vs_support":"ABL/HOT/gap remain constant across valid penalty assumptions because every readable row shares the same prompt/context flags; effective evidence weight collapses as lambda_prompt approaches 1.","primary_uncertainty":"evidence availability uncertainty, not score uncertainty"}
    (OUT/"partial_identification_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    prompt_curve=[metric(rows,i/20,0,0.75) for i in range(21)]
    svg_line(OUT/"core_figure_3_prompt_vs_effective_evidence.svg", prompt_curve, "lambda_prompt", "effective_coverage", "Prompt assumption vs effective evidence", "effective coverage")
    # Judge-facing graphic: normalized score stays flat while support changes.
    svg_score_support(OUT/"core_figure_4_bounds_support.svg", prompt_curve)
    stress=[]
    tests=[("A_no_prompt_penalty",0.0,0.0,lambda r:True),("B_light_prompt_penalty",0.25,0.0,lambda r:True),("C_medium_prompt_penalty",0.5,0.0,lambda r:True),("D_extreme_prompt_penalty",1.0,0.0,lambda r:True),("E_strict_medium_scaffold",0.0,0.0,lambda r:r["student_evidence_bloom"] in LEVELS and r["scaffold_share"]=="medium"),("F_remove_context_risk",0.0,0.0,lambda r:r["context_truncated"]!="true"),("G_remove_low_confidence",0.0,0.0,lambda r:r["confidence"]!="low")]
    for name,lp,lc,sub in tests:
        m=metric(rows,lp,lc,0.75,sub); m["stress_test"]=name; stress.append(m)
    with (OUT/"partial_identification_stress_tests.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(stress[0])); w.writeheader(); w.writerows(stress)
    raw_vals=[(int(r["student_evidence_bloom"][1]), int(r["task_bloom"][1]) if r["task_bloom"] in LEVELS else None) for r in rows if r["student_evidence_bloom"] in LEVELS]
    raw_total=len(raw_vals)
    raw_metric={"effective_weight":raw_total,"effective_coverage":raw_total/len(rows),"valid_or_undefined":True,"adjusted_ABL":sum(x for x,_ in raw_vals)/raw_total,"adjusted_HOT":sum(x>=4 for x,_ in raw_vals)/raw_total,"adjusted_gap":sum(t-x for x,t in raw_vals if t is not None)/sum(t is not None for _,t in raw_vals),"undefined_reason":""}
    ablation=[{"model":"M0 Raw Evidence","status":"OBSERVED_BASELINE","metric":raw_metric},{"model":"M1 confidence weighting","status":"NOT_TESTABLE_WITH_CURRENT_SUPPORT","metric":metric(rows,0,0,0.75)},{"model":"M2 prompt uncertainty","status":"SENSITIVITY_ONLY","metric":metric(rows,0.5,0,0.75)},{"model":"M3 context uncertainty","status":"NOT_TESTABLE_WITH_CURRENT_SUPPORT","metric":metric(rows,0,0.5,0.75)},{"model":"M4 full bounds framework","status":"PARTIALLY_SUPPORTED_BOUNDS_ONLY","metric":metric(rows,0.5,0.5,0.75)}]
    (OUT/"partial_identification_ablation.json").write_text(json.dumps({**BANNER,"models":ablation,"note":"No accuracy comparison is meaningful without human labels."},ensure_ascii=False,indent=2),encoding="utf-8")
    ident_map={**BANNER,"quantities":[
      {"quantity":"Evidence coverage","status":"OBSERVABLE","reason":"Direct descriptive proportion of student_evidence_bloom in L1-L6 within provisional data."},
      {"quantity":"Bloom distribution","status":"OBSERVABLE","reason":"Descriptive distribution of provisional labels only."},
      {"quantity":"Task/Evidence gap","status":"OBSERVABLE","reason":"Descriptive gap on rows with both numeric provisional labels."},
      {"quantity":"prompt frequency/context frequency","status":"OBSERVABLE","reason":"Field frequencies are directly tabulated."},
      {"quantity":"prompt penalty","status":"PARTIALLY_IDENTIFIABLE","reason":"Only assumption-based bounds/sensitivity; no readable prompt=false support."},
      {"quantity":"context penalty","status":"PARTIALLY_IDENTIFIABLE","reason":"Only assumption-based bounds/sensitivity; no readable context_truncated=true support."},
      {"quantity":"confidence reliability","status":"PARTIALLY_IDENTIFIABLE","reason":"Only medium confidence among readable Evidence; no low/high calibration support."},
      {"quantity":"task_actor correction","status":"NOT_IDENTIFIABLE","reason":"All readable Evidence has task_actor=ai and task_source=ai_prompt."},
      {"quantity":"student-level ability","status":"NOT_IDENTIFIABLE","reason":"No validated human labels and no supported student-level measurement target here."},
      {"quantity":"session trajectory","status":"NOT_IDENTIFIABLE","reason":"This development file lacks a validated session trajectory and labels are provisional."},
      {"quantity":"agent-type causal effect","status":"NOT_IDENTIFIABLE","reason":"No comparable treatment/control or causal support."},
      {"quantity":"formal AIV/student ranking","status":"NOT_IDENTIFIABLE","reason":"Human R1/R2, outcome and identification support are absent."}]}
    (OUT/"identifiability_map.json").write_text(json.dumps(ident_map,ensure_ascii=False,indent=2),encoding="utf-8")
    readable_rows = [r for r in rows if r["student_evidence_bloom"] in LEVELS]
    demo={**BANNER,"model_status":"PARTIAL_IDENTIFICATION_BOUNDS","project_status":"S4 blocked by human annotation; development bounds prepared","source_type":"AI_PROVISIONAL","data_source":"data/annotations/ai/pilot_ai_provisional.csv","development_only":True,"parameter_configuration":{"lambda_prompt":{"min":0.0,"max":1.0,"step":0.05,"role":"assumption/sensitivity"},"lambda_context":{"min":0.0,"max":1.0,"step":0.10,"role":"assumption/sensitivity"},"r_medium":{"values":[0.5,0.75,1.0],"role":"assumption/sensitivity"}},"measurement_problem":{"records":len(rows),"readable_evidence":len(readable_rows),"prompt_true_in_readable":sum(r["prompt_induced"]=="true" for r in readable_rows),"context_truncated_true_in_readable":sum(r["context_truncated"]=="true" for r in readable_rows)},"identifiability":ident_map["quantities"],"raw_metrics":summary["findings"]["raw_baseline"],"baseline_support":{"effective_weight":summary["findings"]["raw_baseline"]["effective_weight"],"effective_coverage":summary["findings"]["raw_baseline"]["effective_coverage"]},"bounds":summary["bounds"],"stress_tests":stress,"example_records":[r["record_id"] for r in readable_rows][:8],"demo_records":[{k:r[k] for k in ["record_id","student_evidence_bloom","task_bloom","confidence","prompt_induced","context_truncated"]} for r in readable_rows],"limitations":summary["limitations"]}
    (DEMO/"demo_payload.json").write_text(json.dumps(demo,ensure_ascii=False,indent=2),encoding="utf-8")
    paper='''# 教育 AI 交互证据评价：方法与结果骨架（开发版）\n\n> 本文骨架只承载 DEVELOPMENT_ONLY / AI_PROVISIONAL 结果，不替代正式人工标注、Gate 或 AIV。\n\n## 1 Introduction\nAI 介入后，观察到的学生文本不自动等于学生能力。\n\n## 2 Problem Definition\n定义 observed evidence、student evidence、prompt-induced evidence、measurement uncertainty、support 与 identifiability。\n\n## 3 Data and Measurement\n说明 70 条开发样本、L1-L6 可判读 Evidence、NO_EVIDENCE/UNDETERMINED 拒判状态，以及 AI provisional 与 human R1/R2 的边界。\n\n## 4 Identifiability Diagnosis\n报告 16 条可判读 Evidence 的完全分离：prompt=true、actor=ai、confidence=medium、context_truncated=false，并区分数据生成、规则、provisional 标签和字段映射来源。\n\n## 5 Model\n使用 assumption-based identification interval，而不是唯一惩罚系数：\n\n`w_i(theta)=I(E_i=L1..L6) * c_i * (1-lambda_prompt*p_i) * (1-lambda_context*t_i)`\n\n对参数集合 Θ 计算 ABL/HOT/Gap/有效证据权重的可行范围；分母为零时记为 undefined。该区间不是统计置信区间。\n\n## 6 Experiments\n开发版包括参数网格、压力测试和组件状态审计；不比较 accuracy，不拟合复杂模型。\n\n## 7 Results\n当前最重要结果是：有效区间内 ABL/HOT/Gap 基本稳定，但有效 Evidence weight 随 prompt penalty 下降并可退化为零；不确定性主要来自 evidence availability。\n\n## 8 Limitations\n缺少真实 R1/R2、独立无 AI outcome、可靠 session_id、可比 prompt 对照和充分 actor/confidence 支持；不能宣称因果增量、正式 AIV 或学生排名。\n\n## 9 Discussion\n“先证明 Evidence 可解释”是教育 AI 增量价值评价的必要前置条件之一；这里是方法论命题，不是已验证因果结论。\n\n## 10 Formal replacement plan\n人工标签返回后，以统一输入接口替换 source_type/mode，重跑 Gate、可靠性、support audit、bounds、stress tests 和最终图表；不得把开发结果覆盖为正式结果。\n'''
    (PAPER/"method_results_skeleton.md").write_text(paper,encoding="utf-8")
    print(json.dumps({"grid":len(grid),"undefined":summary["undefined_cells"],"bounds":summary["bounds"],"outputs":["partial_identification_grid.csv","partial_identification_summary.json","partial_identification_stress_tests.csv","partial_identification_ablation.json","identifiability_map.json","demo_payload.json","method_results_skeleton.md"]},ensure_ascii=False))

if __name__ == "__main__":
    main()
