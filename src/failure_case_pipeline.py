"""Extract development candidates and define the formal replacement contract."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--input", type=Path, required=True); ap.add_argument("--out", type=Path, required=True); a=ap.parse_args()
    d=pd.read_csv(a.input, dtype=str, keep_default_na=False); rows=[]
    for _,r in d.iterrows():
        w=float(r.get("reliability_weight",0) or 0); status="DEVELOPMENT_ONLY"
        evidence=str(r.get("raw_interpretation", ""))
        record_id=str(r.get("record_id", ""))
        # The counterexample CSV is the frozen development source.  A readable
        # L1--L6 Evidence row has a descriptive Raw score and a deterministic
        # adjusted contribution; NO_EFFECTIVE_EVIDENCE remains undefined.
        raw_score = None
        adjusted_score = None
        if "Evidence is L" in evidence:
            marker = evidence.split("Evidence is L", 1)[1][:1]
            if marker.isdigit():
                raw_score = float(marker)
                adjusted_score = raw_score * w
        undefined = raw_score is None
        if w >= 0.75 and str(r.get("adjusted_interpretation","")).startswith("NO_EFFECTIVE_EVIDENCE") is False and str(r.get("decision_reason","")).find("risk")>=0: typ="F1"
        elif str(r.get("adjusted_interpretation","")).startswith("NO_EFFECTIVE_EVIDENCE"): typ="F2"
        else: typ="F3" if ";" in str(r.get("risk_factor","")) else "F2"
        rows.append({"case_id":f"{typ}_{record_id}","case_type":typ,"record_id":record_id,"raw_score":raw_score,"raw_score_defined":not undefined,"reliability":w,"adjusted_score":adjusted_score,"adjusted_score_defined":not undefined,"decision":"ABSTAIN" if typ=="F2" else "ACCEPT_CANDIDATE","evaluation_status":"NO_EFFECTIVE_EVIDENCE" if undefined else "LOW_SUPPORT","undefined_reason":"NO_EFFECTIVE_EVIDENCE" if undefined else "","true_label":None,"status":status})
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps({"status":"DEVELOPMENT_ONLY","formal_replacement":"WAITING_FOR_HUMAN","cases":rows},ensure_ascii=False,indent=2),encoding="utf-8"); print(f"wrote {a.out}"); return 0
if __name__=="__main__": raise SystemExit(main())
