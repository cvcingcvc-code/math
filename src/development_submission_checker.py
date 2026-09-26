"""Minimal consistency checker for the Development Submission Candidate."""
from __future__ import annotations
import json, re, zipfile
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    a = json.loads((ROOT / "outputs/final_results.json").read_text(encoding="utf-8"))
    checks = {}
    checks["artifact_identity"] = a["metadata"]["annotation_status"] == "DEVELOPMENT_ONLY" and a["metadata"]["formal_gate_eligible"] is False
    checks["artifact_sections"] = all(k in a for k in ("development_results","human_validation","transfer_validation","sensitivity","ablation","counterexamples","limitations"))
    checks["sample_count"] = a["data_identity"]["sample_count"] == 70 and a["development_results"]["sample_count"] == 70
    raw, adj = a["raw_summary"], a["adjusted_summary"]
    checks["raw_adjusted"] = (raw["ABL"], raw["HOT"], raw["Task_Evidence_Gap"]) == (3.5625, 0.375, 1.125) and (adj["ABL"], adj["HOT"], adj["Task_Evidence_Gap"]) == (3.5625, 0.375, 1.125)
    checks["status_counts"] = len(a["development_results"]["explain_records"]) == 70 and sum(r["evaluation_status"] == "LOW_SUPPORT" for r in a["development_results"]["explain_records"]) == 16
    checks["sensitivity"] = len(a["sensitivity"]["rows"]) == 15 and set(a["sensitivity"]["parameters"]) == {"lambda_prompt","lambda_context","r_medium"}
    checks["ablation"] = len(a["ablation"]) == 4 and [x["effective_weight"] for x in a["ablation"]] == [16.0,12.0,6.0,6.0]
    checks["transfer"] = a["transfer_validation"]["status"] == "SYNCED_EXISTING_RESULT" and a["transfer_validation"]["trading_advantage"] == "NOT_SUPPORTED_CLAIM"
    paper = (ROOT / "paper/development_submission_candidate.md").read_text(encoding="utf-8")
    checks["paper"] = all(x in paper for x in ("DEVELOPMENT_ONLY","NOT_HUMAN_VALIDATED","External Transfer Validation","trading advantage"))
    demo = (ROOT / "reports/demo/index.html").read_text(encoding="utf-8")
    checks["demo"] = "../../outputs/final_results.json" in demo and all(x in demo for x in ("Explain","What-if","Evaluation Status"))
    checks["figures"] = all((ROOT / p).exists() for p in a["figures"].values())
    ppt = ROOT / "outputs/education_ai_evidence_roadshow_final.pptx"
    if ppt.exists():
        with zipfile.ZipFile(ppt) as z:
            text = " ".join(re.findall(r"<a:t>(.*?)</a:t>", " ".join(z.read(n).decode("utf-8","ignore") for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml"))))
        checks["ppt_core_numbers_checked"] = all(x in text for x in ("3.5625","0.375","1.125","0.228571","0.085714","DEVELOPMENT ONLY"))
    else: checks["ppt_core_numbers_checked"] = False
    result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "artifact": "outputs/final_results.json", "formal_run_performed": False}
    (ROOT / "reports/verification/development_submission_consistency.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__": raise SystemExit(main())
