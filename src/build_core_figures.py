"""Render five lightweight SVG figures with only the Python standard library."""
from pathlib import Path
import json, csv
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'reports/development'
def save(name,title,body,xlabel,ylabel):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="460"><rect width="720" height="460" fill="#fffdf7"/><text x="360" y="32" text-anchor="middle" font-family="Arial" font-size="20" fill="#173b35">{title}</text><line x1="72" y1="390" x2="680" y2="390" stroke="#555"/><line x1="72" y1="70" x2="72" y2="390" stroke="#555"/>{body}<text x="376" y="438" text-anchor="middle" font-family="Arial" font-size="13">{xlabel}</text><text transform="translate(18 235) rotate(-90)" text-anchor="middle" font-family="Arial" font-size="13">{ylabel}</text></svg>'
    (OUT/name).write_text(s,encoding='utf-8')
def main():
    rec=json.loads((OUT/'explain_records.json').read_text(encoding='utf-8')); d=[r for r in rec if r['raw_score'] is not None]
    pts=''.join(f'<circle cx="{72+(r["raw_score"]-1)*121.6:.1f}" cy="{390-r["adjusted_score"]/6*300:.1f}" r="5" fill="#2f6f5e"/>' for r in d)
    save('raw_vs_adjusted_scatter.svg','Raw vs Adjusted',pts+'<line x1="72" y1="340" x2="680" y2="90" stroke="#999" stroke-dasharray="5,5"/>','Raw score (Evidence L1–L6)','Adjusted contribution')
    bins=[0]*5
    for r in rec: bins[min(4,int(r['evidence_reliability']*5))]+=1
    bars=''.join(f'<rect x="{100+i*110}" y="{390-n*8}" width="70" height="{n*8}" fill="#2f6f5e"/><text x="{135+i*110}" y="410" text-anchor="middle" font-size="12">{i/5:.1f}–{(i+1)/5:.1f}</text><text x="{135+i*110}" y="{380-n*8}" text-anchor="middle" font-size="12">{n}</text>' for i,n in enumerate(bins))
    save('evidence_reliability_distribution.svg','Evidence Reliability Distribution',bars,'Reliability bins','Records')
    rows=list(csv.DictReader((OUT/'what_if_sensitivity.csv').open(encoding='utf-8-sig'))); colors={'lambda_prompt':'#2f6f5e','lambda_context':'#e07a3f','r_medium':'#b24c4c'}; lines=''
    for j,p in enumerate(colors):
        g=[r for r in rows if r['parameter']==p]; coords=' '.join(f'{110+i*125},{240-float(r["delta_reliability"])*6000:.1f}' for i,r in enumerate(g)); lines+=f'<polyline points="{coords}" fill="none" stroke="{colors[p]}" stroke-width="3"/><text x="560" y="{100+j*22}" fill="{colors[p]}" font-size="13">{p}</text>'
    save('parameter_sensitivity.svg','Parameter Sensitivity (What-if)',lines,'−20%  −10%  baseline  +10%  +20%','Δ mean reliability')
    art=json.loads((ROOT/'outputs/final_results.json').read_text(encoding='utf-8')); ab=art['ablation']; bars=''.join(f'<rect x="{100+i*140}" y="{390-float(r["effective_coverage"])*1000:.1f}" width="80" height="{float(r["effective_coverage"])*1000:.1f}" fill="#e07a3f"/><text x="{140+i*140}" y="410" text-anchor="middle" font-size="11">M{i}</text>' for i,r in enumerate(ab)); save('ablation_comparison.svg','Ablation Comparison',bars,'M0 → M3','Effective coverage')
    ce=art['counterexamples']; bars=''.join(f'<rect x="{120+i*125}" y="{390-float(r["reliability_weight"])*300:.1f}" width="60" height="{float(r["reliability_weight"])*300:.1f}" fill="#b24c4c"/><text x="{150+i*125}" y="410" text-anchor="middle" font-size="11">{r["record_id"]}</text>' for i,r in enumerate(ce)); save('counterexamples.svg','Counterexamples',bars,'Representative records','Reliability weight')
    print('generated=5')
if __name__=='__main__': main()
