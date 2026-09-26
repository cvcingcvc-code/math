"""Deterministic M0-M3 external information-missing validation.

Uses the frozen 7-day momentum signal and the existing historical BTC snapshot.
M1 evidence is explicitly synthetic/controlled; it is not presented as news data.
"""
import csv, json, math, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / "record_level.csv").open(encoding="utf-8")))

def f(r, k):
    return float(r[k])

def clip(x): return max(0.0, min(1.0, x))

def evaluate(completeness=1.0, mode="normal"):
    out=[]
    for i,r in enumerate(rows):
        raw=f(r,"raw_signal")
        # Controlled external evidence: agreement with raw direction, with a fixed
        # conflict cadence. Identity is declared synthetic and never re-optimized.
        evidence_dir = 1 if (i % 11) not in (0,1) else -1
        agreement = 1.0 if evidence_dir == (1 if raw >= 0 else -1) else 0.0
        quality = clip(f(r,"stability"))
        freshness = clip(f(r,"calibration"))
        if mode == "delayed": freshness *= 0.55
        if mode == "conflicting": agreement = 1.0 - agreement
        if mode == "low_trust": quality *= 0.45
        comp = clip(completeness)
        reliability = clip(0.30*quality + 0.30*comp + 0.20*agreement + 0.20*freshness)
        adjusted = raw * reliability
        accepted = reliability >= 0.65
        correct = (raw * f(r,"next_return") > 0)
        out.append({"raw":raw,"reliability":reliability,"adjusted":adjusted,
                    "accepted":accepted,"correct":correct,"quality":quality,
                    "completeness":comp,"freshness":freshness,"agreement":agreement})
    return out

def summary(es):
    n=len(es); acc=[x for x in es if x["accepted"]]; low=[x for x in es if x["reliability"]<0.65]
    return {"n":n,"accept_n":len(acc),"abstain_n":n-len(acc),"coverage":len(acc)/n,
            "abstain_rate":(n-len(acc))/n,
            "mean_reliability":statistics.mean(x["reliability"] for x in es),
            "median_reliability":statistics.median(x["reliability"] for x in es),
            "error_rate_accepted":(1-statistics.mean(x["correct"] for x in acc)) if acc else None,
            "error_rate_low_reliability":(1-statistics.mean(x["correct"] for x in low)) if low else None}

m0=[{"raw":f(r,"raw_signal"),"decision":"ACCEPT" if abs(f(r,"raw_signal"))>=0.65 else "ABSTAIN",
     "correct":f(r,"raw_signal")*f(r,"next_return")>0} for r in rows]
m1=evaluate(1.0,"normal")
m2=m1
scenarios={"full":m2,"missing_evidence":evaluate(.35,"normal"),
           "delayed_evidence":evaluate(1.0,"delayed"),
           "conflicting_evidence":evaluate(1.0,"conflicting"),
           "low_trust_evidence":evaluate(1.0,"low_trust")}

gate1={"criterion":"Reliability decreases when information quality/completeness decreases",
       "full_mean":summary(scenarios["full"])["mean_reliability"],
       "missing_mean":summary(scenarios["missing_evidence"])["mean_reliability"],
       "full_median":summary(scenarios["full"])["median_reliability"],
       "missing_median":summary(scenarios["missing_evidence"])["median_reliability"],
       "paired_n":len(rows),"supported":summary(scenarios["missing_evidence"])["mean_reliability"] < summary(scenarios["full"])["mean_reliability"]}
gate2={"criterion":"Lower reliability increases abstention and reduces coverage",
       "full":summary(scenarios["full"]),"missing":summary(scenarios["missing_evidence"]),
       "supported":summary(scenarios["missing_evidence"])["abstain_rate"] > summary(scenarios["full"])["abstain_rate"]}
gate3={"criterion":"Low-reliability decisions have higher future error rate",
       "high_reliability_error_rate":summary(scenarios["full"])["error_rate_accepted"],
       "low_reliability_error_rate":summary(scenarios["full"])["error_rate_low_reliability"],
       "supported":(summary(scenarios["full"])["error_rate_low_reliability"] is not None and summary(scenarios["full"])["error_rate_accepted"] is not None and summary(scenarios["full"])["error_rate_low_reliability"] > summary(scenarios["full"])["error_rate_accepted"])}

cases=[]
for label, es in [("Case 1 · full high reliability", scenarios["full"]),("Case 2 · missing evidence", scenarios["missing_evidence"]),("Case 3 · conflicting evidence", scenarios["conflicting_evidence"])]:
    j=max(range(len(es)), key=lambda i: abs(es[i]["raw"]))
    x=es[j]; cases.append({"label":label,"timestamp":rows[j]["date"],"raw_signal":x["raw"],"reliability":x["reliability"],"adjusted_signal":x["adjusted"],"decision":"ACCEPT" if x["accepted"] else "ABSTAIN","future_outcome":f(rows[j],"next_return"),"components":{"data_quality":x["quality"],"information_completeness":x["completeness"],"evidence_freshness":x["freshness"],"signal_agreement":x["agreement"]}})

result={"study_type":"External Information-Missing Validation","data_identity":{"source":"historical BTC-USD daily snapshot","evidence_identity":"synthetic / controlled evidence; no live news feed","sample_size":len(rows)},"frozen_parameters":{"strategy":"A_7d_momentum","threshold":0.65,"weights":{"data_quality":0.30,"information_completeness":0.30,"signal_agreement":0.20,"evidence_freshness":0.20}},"models":{"M0_Raw_Baseline":summary([{"reliability":1.0,"correct":x["correct"],"accepted":x["decision"]=="ACCEPT"} for x in m0]),"M1_AI_Information_Added":summary(m1),"M2_AI_Information_Reliability":summary(m2),"M3_Stress_Test":{k:summary(v) for k,v in scenarios.items()}},"gates":{"Gate_1":gate1,"Gate_2":gate2,"Gate_3":gate3},"cases":cases,"status":"DEVELOPMENT_ONLY","paper_use":"External Transfer Validation only; no trading advantage claim"}
(ROOT/"information_missing_validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"status":"ok","gate1":gate1["supported"],"gate2":gate2["supported"],"gate3":gate3["supported"]}))
