"""Build the frozen F1-F6 visual evidence layer from existing artifacts.

This script only renders already-recorded CSV/JSON values. It does not fit,
re-estimate, tune, or alter the Evidence Reliability model.
"""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "visual_evidence" / "final"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#19231d"
MUTED = "#667269"
CREAM = "#f7f3e8"
CARD = "#fffdf7"
GREEN = "#176b52"
ORANGE = "#d56634"
RED = "#a94442"
BLUE = "#3f6f8f"
LINE = "#dcd8ca"
GRAY = "#d9ded7"


def read_csv(rel: str):
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def text(x, y, value, size=18, fill=INK, weight="400", anchor="start", family="Arial,Microsoft YaHei,sans-serif"):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}px" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>'


def rect(x, y, w, h, fill=CARD, stroke=LINE, rx=12, sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke=LINE, sw=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def circle(cx, cy, r, fill=GREEN, stroke="none", sw=1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def svg(title, subtitle, body, width=1200, height=700):
    footer = "AI_PROVISIONAL · DEVELOPMENT_ONLY · Formal Gate NOT_RUN"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="{width}" height="{height}" fill="{CREAM}"/>
{text(48, 54, title, 29, INK, "700")}
{text(48, 84, subtitle, 15, MUTED)}
{body}
{line(48, height-42, width-48, height-42, LINE, 1)}
{text(48, height-16, footer, 12, MUTED)}
</svg>'''


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")


def f1():
    labels = [
        (55, "Observed Evidence", "student text / context"),
        (245, "Raw Signal", "L1–L6 if readable"),
        (435, "Evidence Reliability", "wᵢ = I·c·risk factors"),
        (625, "Adjusted Evaluation", "Raw × Reliability"),
        (815, "Support / Coverage", "Σwᵢ and Σwᵢ/N"),
        (1005, "Decision", "ACCEPT / ABSTAIN"),
    ]
    body = ""
    for i, (x, head, sub) in enumerate(labels):
        body += rect(x, 205, 150, 132, CARD, GREEN if i in (0, 2, 5) else LINE, 13, 2 if i in (0, 2, 5) else 1)
        body += text(x+75, 247, head, 17, GREEN if i in (0, 2, 5) else INK, "700", "middle")
        body += text(x+75, 280, sub, 13, MUTED, "400", "middle")
        if i < len(labels)-1:
            body += text(x+168, 278, "→", 25, ORANGE, "700", "middle")
    body += line(55, 390, 1145, 390, GREEN, 3)
    body += text(55, 428, "Readable Evidence", 16, GREEN, "700")
    body += text(55, 456, "continue through support accounting", 14, MUTED)
    body += text(610, 428, "Evidence not readable", 16, RED, "700")
    body += text(610, 456, "→ NO_EFFECTIVE_EVIDENCE (undefined; never score = 0)", 14, RED)
    body += rect(55, 510, 450, 72, "#e9eee5", GREEN, 10, 1)
    body += text(75, 542, "AI Increment", 17, MUTED, "700") + text(75, 568, "NOT_SUPPORTED · no valid paired baseline", 14, MUTED)
    body += rect(650, 510, 495, 72, "#f5e9df", ORANGE, 10, 1)
    body += text(670, 542, "Fail-closed boundary", 17, ORANGE, "700") + text(670, 568, "ABSTAIN when support is insufficient", 14, INK)
    write("F1_model_flow.svg", svg("F1 · Observed Evidence → Reliability → Decision", "The model separates observed signal from the support behind it; AIV remains outside the current development result.", body))


def f2():
    body = ""
    # Plot area
    x0, y0, w, h = 110, 170, 640, 390
    body += rect(x0, y0, w, h, CARD, LINE, 10)
    for val in range(1, 7):
        x = x0 + (val-1) * w/5
        body += line(x, y0, x, y0+h, LINE, 1, "4 6") + text(x, y0+h+28, f"L{val}", 14, MUTED, "400", "middle")
    for val in [0, 1, 2, 3, 4, 5, 6]:
        y = y0+h - val*h/6
        body += line(x0, y, x0+w, y, LINE, 1, "4 6") + text(x0-14, y+5, str(val), 13, MUTED, "400", "end")
    body += text(x0+w/2, y0+h+58, "Raw Evidence level", 15, MUTED, "700", "middle")
    body += text(x0-55, y0+10, "Adjusted", 14, MUTED, "700", "middle")
    # P105 and P108 positions
    def px(raw): return x0 + (raw-1)*w/5
    def py(adj): return y0+h - adj*h/6
    body += line(px(2), py(.75), px(2), y0+h, ORANGE, 2, "5 5")
    body += circle(px(2), py(.75), 10, ORANGE) + text(px(2)+18, py(.75)-10, "P105 · L2 × .375 = .75", 15, ORANGE, "700")
    body += line(px(6), py(2.25), px(6), y0+h, GREEN, 2, "5 5")
    body += circle(px(6), py(2.25), 11, GREEN) + text(px(6)-18, py(2.25)-16, "P108 · L6 × .375 = 2.25", 15, GREEN, "700", "end")
    body += rect(815, 175, 315, 165, "#e9eee5", GREEN, 12, 1)
    body += text(840, 214, "Same Raw scale, different support", 18, GREEN, "700")
    body += text(840, 250, "P108: R = 0.375", 16, INK)
    body += text(840, 278, "LOW_SUPPORT / ABSTAIN", 16, ORANGE, "700")
    body += text(840, 314, "P105: R = 0.375", 16, INK)
    body += text(840, 342, "LOW_SUPPORT / ABSTAIN", 16, ORANGE, "700")
    body += rect(815, 380, 315, 170, "#f5e9df", ORANGE, 12, 1)
    body += text(840, 420, "Development boundary", 18, ORANGE, "700")
    body += text(840, 456, "N = 70 records", 16, INK)
    body += text(840, 484, "16 readable Evidence", 16, INK)
    body += text(840, 512, "54 NO_EFFECTIVE_EVIDENCE", 16, RED, "700")
    body += text(840, 540, "undefined records are not plotted as zero", 13, MUTED)
    write("F2_raw_vs_adjusted.svg", svg("F2 · Raw Evidence Is Not the Same as Supported Evidence", "Per-record adjusted contribution, not an aggregate score. The 54 undefined records remain explicit.", body))


def f3():
    body = ""
    x = [180, 410, 640]
    # P108 band
    body += text(80, 180, "P108 · controlled development contrast", 18, GREEN, "700")
    body += line(130, 300, 700, 300, LINE, 2)
    vals = [("Original", .375, 2.25, ORANGE, "LOW_SUPPORT"), ("Prompt removed", .75, 4.5, GREEN, "SUPPORTED*"), ("Confidence low", .25, 1.5, RED, "LOW_SUPPORT")]
    for i,(lab,r,a,col,state) in enumerate(vals):
        cy = 300 - a*28
        body += circle(x[i], cy, 11, col) + text(x[i], cy-20, f"R={r:.3f}", 15, col, "700", "middle") + text(x[i], 340, lab, 14, INK, "700", "middle") + text(x[i], 365, f"adjusted={a:.2f} · {state}", 13, col, "700", "middle")
        if i < 2: body += line(x[i]+12, cy, x[i+1]-12, 300 - vals[i+1][2]*28, col, 3)
    body += text(760, 175, "P072 · context-only recovery", 18, RED, "700")
    body += rect(760, 205, 365, 180, "#f5e9df", RED, 12, 1)
    body += text(790, 248, "Original", 16, INK, "700") + text(790, 276, "UNDETERMINED → NO_EFFECTIVE_EVIDENCE", 15, RED)
    body += text(790, 318, "Context restored", 16, INK, "700") + text(790, 346, "Evidence unchanged → still NO_EFFECTIVE_EVIDENCE", 15, RED)
    body += text(80, 500, "Interpretation", 18, INK, "700")
    body += text(80, 532, "Removing a declared risk can increase support; restoring a field cannot create new Evidence.", 16, MUTED)
    body += text(80, 564, "*SUPPORTED here means the declared support threshold in a controlled development contrast; it is not a Formal Gate result.", 14, MUTED)
    body += text(80, 590, "These are controlled development contrasts, not randomized or causal experiments.", 15, MUTED)
    write("F3_evidence_degradation.svg", svg("F3 · Evidence Degradation Changes Support; Missing Evidence Triggers Refusal", "Paired stress contrasts from the frozen development artifacts. The contrasts are controlled, not causal.", body))


def f4():
    rows = read_csv("reports/robustness/parameter_perturbation.csv")
    body = ""
    # left plot mean abs R change by perturbation
    x0,y0,w,h = 90,190,620,330
    body += rect(x0,y0,w,h,CARD,LINE,10)
    changes = ["−20%","−10%","baseline","+10%","+20%"]
    for j, param in enumerate(["lambda_prompt", "lambda_context", "r_medium"]):
        vals = [r for r in rows if r["parameter"] == param]
        col = [GREEN, BLUE, ORANGE][j]
        pts=[]
        for i,r in enumerate(vals):
            xx=x0+60+i*(w-120)/4
            yy=y0+h-float(r["mean_abs_reliability_change"])/.02*(h-50)
            pts.append((xx,yy))
            body += circle(xx,yy,5,col)
            if i==0: body += text(x0+12, yy-8-j*17, param, 13, col, "700")
        body += "<polyline points=\""+" ".join(f"{a},{b}" for a,b in pts)+f"\" fill=\"none\" stroke=\"{col}\" stroke-width=\"3\"/>"
    for i,c in enumerate(changes):
        xx=x0+60+i*(w-120)/4; body += line(xx,y0,xx,y0+h,LINE,1,"4 6") + text(xx,y0+h+26,c,13,MUTED,"400","middle")
    body += text(x0+w/2,y0+h+55,"local parameter perturbation",14,MUTED,"700","middle")
    body += text(x0-25,y0+12,"mean |ΔR|",13,MUTED,"700","middle")
    # right cards
    body += rect(770,190,355,145,"#e9eee5",GREEN,12,1)
    body += text(795,226,"Recorded local behavior",18,GREEN,"700")
    body += text(795,258,"status flips = 0",17,INK,"700")
    body += text(795,286,"ranking = NOT_APPLICABLE",16,INK)
    body += text(795,314,"finite grid ≠ confidence interval",14,MUTED)
    body += rect(770,365,355,155,"#f5e9df",ORANGE,12,1)
    body += text(795,402,"Support boundary",18,ORANGE,"700")
    body += text(795,434,"baseline: weight 6 / coverage .085714",15,INK)
    body += text(795,462,"full grid: weight .4–16 / coverage .005714–.228571",14,INK)
    body += text(795,494,"context flatline = variation not identified",14,MUTED)
    body += text(90,590,"Score stability here is a common-scaling property of the 16 readable rows; it is not calibration or a formal interval.",14,MUTED)
    write("F4_parameter_perturbation.svg", svg("F4 · Local Parameter Perturbation: Support Moves, Ranking Is Not Applicable", "Finite development stress grid: reliability/support sensitivity is shown with explicit identifiability limits.", body))


def f5():
    rows = read_csv("reports/development/ablation_results.csv")
    cases = read_csv("reports/development/counterexamples.csv")
    body = ""
    # left bars
    body += text(80,170,"Component ablation",18,INK,"700")
    x0,y0,w,h=100,205,510,310
    body += rect(x0,y0,w,h,CARD,LINE,10)
    vals=[float(r["effective_weight"]) for r in rows]
    for i,r in enumerate(rows):
        xx=x0+55+i*115; bh=vals[i]/16*230; yy=y0+260-bh
        body += rect(xx,yy,58,bh,GREEN if i<2 else ORANGE,GREEN if i<2 else ORANGE,6,1)
        body += text(xx+29,yy-10,f"{vals[i]:.0f}",16,INK,"700","middle")
        body += text(xx+29,y0+288,f"M{i}",15,INK,"700","middle")
    body += text(x0+w/2,y0+340,"effective weight: 16 → 12 → 6 → 6",15,MUTED,"700","middle")
    # right state cases
    body += text(700,170,"Failure / refusal boundary",18,INK,"700")
    y=215
    for r in cases:
        rid=r["record_id"]; rw=float(r["reliability_weight"]); contrib=r["effective_evidence_contribution"]
        if rid in ("P105","P108"):
            state="LOW_SUPPORT / ABSTAIN"; col=ORANGE; value=f"R={rw:.3f} · contribution={contrib}"
        else:
            state="NO_EFFECTIVE_EVIDENCE"; col=RED; value="undefined · not zero"
        body += rect(700,y,425,62,"#fffdf7",col,9,2)
        body += text(720,y+25,rid,16,col,"700") + text(790,y+25,value,14,INK) + text(720,y+49,state,14,col,"700")
        y += 76
    body += text(80,600,"Ablation changes support accounting; without true labels/outcomes it cannot be called accuracy improvement.",14,MUTED)
    write("F5_ablation_refusal.svg", svg("F5 · Component Ablation and the Refusal Boundary", "Confidence/prompt/context components change evidence support; missing Evidence remains a state, not a zero-height score.", body))


def f6():
    rows=read_csv("reports/external_transfer/three_raw_signals_unified.csv")
    body=""
    x0,y0,w,h=100,180,720,360
    body += rect(x0,y0,w,h,CARD,LINE,10)
    groups=[("low_R", "low-R"), ("medium_R","medium-R"), ("high_R","high-R")]
    maxv=.60; minv=.40
    for tick in [.40,.45,.50,.55,.60]:
        yy=y0+h-(tick-minv)/(maxv-minv)*(h-70)
        body += line(x0,yy,x0+w,yy,LINE,1,"4 6") + text(x0-12,yy+5,f"{tick:.2f}",12,MUTED,"400","end")
    colors=[GREEN,BLUE,ORANGE]
    for i,r in enumerate(rows):
        base=x0+110+i*210
        body += text(base+55,y0+h+32,r["strategy"].replace("_"," "),13,INK,"700","middle")
        for j,(key,label) in enumerate(groups):
            val=float(r[key+"_quality"]); xx=base+j*52; bh=(val-minv)/(maxv-minv)*(h-70); yy=y0+h-bh
            body += rect(xx,yy,34,bh,colors[j],colors[j],4,1) + text(xx+17,yy-8,f"{val:.3f}",11,colors[j],"700","middle")
    body += text(x0+w/2,y0+h+58,"quality / hit-rate proxy",14,MUTED,"700","middle")
    body += rect(870,180,260,160,"#e9eee5",GREEN,12,1)
    body += text(895,218,"Partial transfer support",18,GREEN,"700")
    body += text(895,252,"A/B: high-R > low-R",15,INK,"700")
    body += text(895,280,"C: ordering reverses",15,RED,"700")
    body += text(895,310,"boundary retained",14,MUTED)
    body += rect(870,375,260,165,"#f5e9df",ORANGE,12,1)
    body += text(895,414,"Scope",18,ORANGE,"700")
    body += text(895,448,"BTC historical paper simulation",14,INK)
    body += text(895,476,"DEVELOPMENT_ONLY",14,ORANGE,"700")
    body += text(895,504,"no education / trading claim",14,MUTED)
    write("F6_external_structural_transfer.svg", svg("F6 · External Structural Transfer: Reliability Ordering Is Partial", "Low / medium / high-R are shown together; Strategy C is the retained counterexample. This is structural transfer only.", body))


def main():
    f1(); f2(); f3(); f4(); f5(); f6()
    manifest = {
        "status": "DEVELOPMENT_ONLY",
        "formal_gate": "NOT_RUN",
        "figures": {
            "F1": "reports/visual_evidence/final/F1_model_flow.svg",
            "F2": "reports/visual_evidence/final/F2_raw_vs_adjusted.svg",
            "F3": "reports/visual_evidence/final/F3_evidence_degradation.svg",
            "F4": "reports/visual_evidence/final/F4_parameter_perturbation.svg",
            "F5": "reports/visual_evidence/final/F5_ablation_refusal.svg",
            "F6": "reports/visual_evidence/final/F6_external_structural_transfer.svg",
        },
        "paper_main": ["F1", "F2", "F3", "F4", "F5"],
        "paper_external_or_appendix": ["F6"],
        "demo_home": ["F1", "F2", "F3"],
        "source_artifacts": [
            "reports/development/ablation_results.csv",
            "reports/development/counterexamples.csv",
            "reports/perturbation/evidence_perturbation_cases.csv",
            "reports/robustness/parameter_perturbation.csv",
            "reports/external_transfer/three_raw_signals_unified.csv",
        ],
        "old_figures_not_mainline": [
            "reports/development/reliability_sensitivity.svg",
            "reports/development/evidence_reliability_distribution.svg",
            "reports/development/counterexamples.svg",
            "reports/development/core_figure_2_support_heatmap.svg",
            "reports/development/core_figure_3_prompt_vs_effective_evidence.svg",
            "experiments/transfer_finance/figure1-4.svg",
            "reports/external_transfer/three_raw_signals_quality.svg",
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "README.md").write_text("# Final visual evidence layer\n\nF1–F6 are deterministic renderings of existing development artifacts. They do not recompute or change the model. All figures retain `AI_PROVISIONAL · DEVELOPMENT_ONLY · Formal Gate NOT_RUN`.\n\nSee `manifest.json` for the six paths and placement map.\n", encoding="utf-8")


if __name__ == "__main__":
    main()
