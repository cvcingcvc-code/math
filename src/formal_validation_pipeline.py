"""Fail-closed formal validation preflight."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"record_id", "task_bloom", "student_evidence_bloom", "confidence", "annotation_source", "annotation_status"}
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--r1",type=Path,required=True); ap.add_argument("--r2",type=Path,required=True); ap.add_argument("--gate",type=Path,default=ROOT/"reports/annotation_gate_report.json"); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args()
    issues=[]; gate=json.loads(a.gate.read_text(encoding="utf-8")) if a.gate.exists() else {}
    if gate.get("gate_status") != "PASS" or gate.get("formal_gate_eligible") is not True: issues.append("FORMAL_GATE_NOT_PASS")
    inputs=[]
    for label,p in (("R1",a.r1),("R2",a.r2)):
        if not p.exists(): issues.append(f"{label}_MISSING"); continue
        try: d=pd.read_csv(p,dtype=str,keep_default_na=False,encoding="utf-8-sig")
        except UnicodeDecodeError: d=pd.read_csv(p,dtype=str,keep_default_na=False,encoding="gb18030")
        miss=sorted(REQUIRED-set(d.columns));
        if miss: issues.append(f"{label}_MISSING_COLUMNS:{','.join(miss)}")
        if len(d)==0 or d.get("record_id",pd.Series(dtype=str)).duplicated().any(): issues.append(f"{label}_INVALID_ROWS_OR_DUPLICATES")
        inputs.append({"round":label,"rows":len(d),"sha256":sha256(p)})
    payload={"status":"BLOCKED" if issues else "READY_TO_RUN","formal_metrics_written":False,"issues":issues,"inputs":inputs,"next_steps":["run R1/R2 consistency","run preregistered Gate","run Raw/Adjusted, sensitivity, ablation, counterexamples, accuracy-coverage, failure cases","emit Formal vs Development table"]}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(payload,ensure_ascii=False)); return 1 if issues else 0
if __name__=="__main__": raise SystemExit(main())
