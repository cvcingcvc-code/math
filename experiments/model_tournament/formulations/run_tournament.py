"""Independent, preregistered comparison of alternative reliability structures.

This file deliberately reads only the AI_PROVISIONAL development slice and an
existing small external transfer case file. It does not import or modify the
frozen production model.
"""
from __future__ import annotations

import csv, json, math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments" / "model_tournament" / "formulations"
INPUT = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
TRANSFER = ROOT / "experiments" / "transfer_finance" / "information_missing_validation.json"
LEVELS = {f"L{i}": i for i in range(1, 7)}
CONF = {"high": 1.0, "medium": 0.75, "low": 0.5}

# Pre-registration: no data-driven tuning is performed.
PARAMS = {"B_lambda": [0.5, 1.0], "C_threshold": [0.5], "D_gamma": [0.5, 1.0, 2.0]}
R_PERTURB = [0.0, 0.5, 0.8, 1.0, 1.2]

def reliability(row, *, confidence=True, prompt=True, context=True):
    if row["raw"] is None:
        return 0.0
    c = CONF.get(str(row["confidence"]).lower(), 0.5) if confidence else 1.0
    p = str(row["prompt_induced"]).lower() == "true" if prompt else False
    t = str(row["context_truncated"]).lower() == "true" if context else False
    return max(0.0, min(1.0, c * (1 - 0.5 * p) * (1 - 0.5 * t)))

def score(model, raw, r, param=None):
    if raw is None:
        return None, "NO_EFFECTIVE_EVIDENCE"
    if model == "A_multiplicative":
        return raw * r, "DEFINED"
    if model == "B_additive":
        return raw - float(param) * (1 - r), "DEFINED"
    if model == "C_gated":
        return (raw, "ACCEPT") if r >= float(param) else (None, "ABSTAIN")
    if model == "D_nonlinear":
        return raw * (r ** float(param)), "DEFINED"
    raise ValueError(model)

def spearman(a, b):
    if len(a) < 2: return None
    ar = pd.Series(a).rank().to_numpy(); br = pd.Series(b).rank().to_numpy()
    if np.std(ar) == 0 or np.std(br) == 0:
        return None
    return float(np.corrcoef(ar, br)[0, 1])

def rows_from_input():
    d = pd.read_csv(INPUT, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    if len(d) != 70 or set(d.annotation_source) != {"AI_PROVISIONAL"} or set(d.annotation_status) != {"DEVELOPMENT_ONLY"}:
        raise ValueError("development identity or size changed")
    out = []
    for _, x in d.iterrows():
        raw = LEVELS.get(x.student_evidence_bloom)
        rec = {"record_id": x.record_id, "raw": raw, "confidence": x.confidence,
               "prompt_induced": x.prompt_induced, "context_truncated": x.context_truncated}
        rec["R"] = reliability(rec)
        out.append(rec)
    return out

def model_specs():
    return [("A_multiplicative", None)] + [("B_additive", x) for x in PARAMS["B_lambda"]] + [("C_gated", x) for x in PARAMS["C_threshold"]] + [("D_nonlinear", x) for x in PARAMS["D_gamma"]]

def aggregate(records, model, param, r_override=None):
    raw, vals, statuses = [], [], []
    for x in records:
        r = x["R"] if r_override is None else r_override(x)
        v, s = score(model, x["raw"], r, param)
        if x["raw"] is not None:
            raw.append(x["raw"])
        if v is not None: vals.append(v)
        statuses.append(s)
    observed = [x for x in records if x["raw"] is not None]
    paired = [(x["raw"], score(model, x["raw"], x["R"] if r_override is None else r_override(x), param)[0]) for x in observed]
    paired = [(a,b) for a,b in paired if b is not None]
    rmse = math.sqrt(sum((a-b)**2 for a,b in paired)/len(paired)) if paired else None
    return {"n": len(records), "raw_observed": len(observed), "defined_n": len(vals),
            "coverage_observed": len(vals)/len(observed) if observed else 0.0,
            "missing_evidence_n": len(records)-len(observed),
            "abstain_n": sum(s == "ABSTAIN" for s in statuses),
            "no_effective_evidence_n": sum(s == "NO_EFFECTIVE_EVIDENCE" for s in statuses),
            "mean_output": float(np.mean(vals)) if vals else None,
            "rmse_vs_raw": rmse,
            "rank_stability_vs_raw": spearman([a for a,b in paired], [b for a,b in paired]) if paired else None}

def run_suite(records):
    results, sens, abl, extreme, counter = [], [], [], [], []
    for model, param in model_specs():
        base = aggregate(records, model, param)
        results.append({"suite":"sample_in","model":model,"parameter":param,"scenario":"baseline",**base})
        # Sensitivity: deterministic multiplicative perturbation of R.
        for mult in R_PERTURB:
            m = aggregate(records, model, param, lambda x, mult=mult: max(0,min(1,x["R"]*mult)))
            sens.append({"model":model,"parameter":param,"r_multiplier":mult,**m})
        # Ablation: remove one declared reliability component.
        for name, kwargs in [("raw",dict(confidence=False,prompt=False,context=False)),
                             ("no_confidence",dict(confidence=False,prompt=True,context=True)),
                             ("no_prompt",dict(confidence=True,prompt=False,context=True)),
                             ("no_context",dict(confidence=True,prompt=True,context=False))]:
            abl.append({"model":model,"parameter":param,"ablation":name,**aggregate(records, model, param, lambda x, kwargs=kwargs: reliability(x, **kwargs))})
        # Extreme R behavior on a small, fixed synthetic grid.
        for raw in [1.0, 6.0]:
            for r in [0.0, 0.01, 0.25, 0.5, 1.0]:
                v,s=score(model,raw,r,param); extreme.append({"model":model,"parameter":param,"raw":raw,"R":r,"output":v,"status":s})
        # Fixed real development counterexamples.
        for rid in ["P108","P072","P035"]:
            x=next(z for z in records if z["record_id"]==rid); v,s=score(model,x["raw"],x["R"],param)
            counter.append({"model":model,"parameter":param,"record_id":rid,"raw":x["raw"],"R":x["R"],"output":v,"status":s})
    return results,sens,abl,extreme,counter

def external_transfer(records):
    ext = json.loads(TRANSFER.read_text(encoding="utf-8"))
    cases=[]
    for group in ["cases"]:
        for c in ext.get(group, []):
            raw = c.get("raw_signal"); r = c.get("reliability")
            for model,param in model_specs():
                v,s=score(model,raw,r,param)
                cases.append({"model":model,"parameter":param,"case":c.get("label"),"raw":raw,"R":r,"output":v,"status":s,"future_outcome_available":True})
    return {"source": str(TRANSFER.relative_to(ROOT)), "sample_size": ext.get("data_identity",{}).get("sample_size"),
            "scope":"three fixed cases from existing small external transfer artifact; structural transfer only",
            "cases":cases, "limitations":["No row-level external dataset is imported here; no model is claimed predictive.","External evidence is synthetic/controlled and DEVELOPMENT_ONLY."]}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rec=rows_from_input(); results,sens,abl,extreme,counter=run_suite(rec)
    external=external_transfer(rec)
    payload={"status":"DEVELOPMENT_ONLY","annotation_source":"AI_PROVISIONAL","input":"data/annotations/ai/pilot_ai_provisional.csv",
             "preregistration":{"models":"A fixed; B lambda in [0.5,1.0]; C threshold=0.5; D gamma in [0.5,1.0,2.0]","R_perturbations":R_PERTURB,"tuning":"none"},
             "results":results,"sensitivity":sens,"ablation":abl,"extreme_R":extreme,"counterexamples":counter,"external_transfer":external}
    (OUT/"formulation_results.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    pd.DataFrame(results).to_csv(OUT/"formulation_results.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(sens).to_csv(OUT/"sensitivity.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(abl).to_csv(OUT/"ablation.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(extreme).to_csv(OUT/"extreme_R.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame(counter).to_csv(OUT/"counterexamples.csv",index=False,encoding="utf-8-sig")
    (OUT/"external_transfer.json").write_text(json.dumps(external,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"rows":len(rec),"models":len(model_specs()),"result_rows":len(results),"status":"PASS"},ensure_ascii=False))

if __name__ == "__main__": main()
