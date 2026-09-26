"""Development-only simple ML challenger for evidence readability.

The target is the AI provisional label `student_evidence_bloom in L1..L6`.
This is a weak development target, not a human truth label.  Features are
restricted to fields available before the provisional evidence label.
"""
from __future__ import annotations

import json
import os
import random
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, brier_score_loss,
                             f1_score, log_loss, roc_auc_score)
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "experiments" / "model_tournament"
OUT.mkdir(parents=True, exist_ok=True)
AI_PATH = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"
PILOT_PATH = ROOT / "data" / "processed" / "pilot_sample.csv"

LEVELS = {f"L{i}" for i in range(1, 7)}
FEATURES = [
    "text_length_chars", "agent_confidence", "speaker_confidence", "context_truncated",
    "semester", "length_stratum", "question_form_stratum",
    "possible_bloom_surface_signal", "path_case",
]
NUMERIC = ["text_length_chars", "agent_confidence", "speaker_confidence", "context_truncated"]
CATEGORICAL = [c for c in FEATURES if c not in NUMERIC]


def read_csv(path: Path) -> pd.DataFrame:
    for enc in ("utf-8-sig", "gb18030", "utf-8"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError("csv", b"", 0, 1, f"could not decode {path}")


def build_data() -> pd.DataFrame:
    ai = read_csv(AI_PATH)
    pilot = read_csv(PILOT_PATH)
    pilot["record_id"] = pilot["pilot_id"].astype(str)
    keep = ["record_id", "student_id"] + [c for c in FEATURES if c != "context_truncated"]
    df = ai[["record_id", "student_evidence_bloom", "context_truncated"]].merge(pilot[keep], on="record_id", how="left", validate="one_to_one")
    # These are the only labels used as a development target.
    df["target_readable"] = df["student_evidence_bloom"].isin(LEVELS).astype(int)
    df["target_level"] = pd.to_numeric(df["student_evidence_bloom"].str.extract(r"L([1-6])")[0], errors="coerce")
    df["context_truncated"] = df["context_truncated"].astype(str).str.lower().map({"true": 1, "false": 0}).fillna(1)
    return df


def make_models() -> Dict[str, Pipeline]:
    prep = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUMERIC),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
    ])
    return {
        "logistic_regression": Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=2000, class_weight="balanced", C=1.0, random_state=1))]),
        "shallow_decision_tree": Pipeline([("prep", prep), ("model", DecisionTreeClassifier(max_depth=2, min_samples_leaf=5, class_weight="balanced", random_state=1))]),
        "random_forest": Pipeline([("prep", prep), ("model", RandomForestClassifier(n_estimators=100, max_depth=3, min_samples_leaf=4, class_weight="balanced", random_state=1, n_jobs=1))]),
    }


def metric_row(name: str, y: np.ndarray, p: np.ndarray, prob: np.ndarray, split: str, rep: int) -> Dict:
    return {"model": name, "split": split, "repeat": rep,
            "n": int(len(y)), "positive_rate": float(np.mean(y)),
            "accuracy": float(accuracy_score(y, p)),
            "balanced_accuracy": float(balanced_accuracy_score(y, p)),
            "f1": float(f1_score(y, p, zero_division=0)),
            "roc_auc": float(roc_auc_score(y, prob)) if len(np.unique(y)) == 2 else None,
            "brier": float(brier_score_loss(y, prob)),
            "log_loss": float(log_loss(y, np.column_stack([1-prob, prob]), labels=[0,1]))}


def repeated_cv(df: pd.DataFrame, models: Dict[str, Pipeline]) -> List[Dict]:
    X, y = df[FEATURES], df.target_readable.to_numpy()
    rows: List[Dict] = []
    cv = RepeatedStratifiedKFold(n_splits=4, n_repeats=25, random_state=20260926)
    for rep, (tr, te) in enumerate(cv.split(X, y), 1):
        for name, model in models.items():
            model.fit(X.iloc[tr], y[tr])
            prob = model.predict_proba(X.iloc[te])[:, 1]
            rows.append(metric_row(name, y[te], (prob >= .5).astype(int), prob, "repeated_stratified_cv", rep))
    return rows


def semester_transfer(df: pd.DataFrame, models: Dict[str, Pipeline]) -> List[Dict]:
    rows = []
    for train_sem, test_sem in [("2025秋", "2026春"), ("2026春", "2025秋")]:
        # Encoding is sometimes mojibake in source files; use the two observed values.
        vals = list(df.semester.dropna().unique())
        train_val = next((v for v in vals if str(v).startswith(train_sem[:4])), None)
        test_val = next((v for v in vals if v != train_val), None)
        if train_val is None or test_val is None:
            continue
        tr, te = df.semester == train_val, df.semester == test_val
        for name, model in models.items():
            model.fit(df.loc[tr, FEATURES], df.loc[tr, "target_readable"])
            prob = model.predict_proba(df.loc[te, FEATURES])[:, 1]
            rows.append(metric_row(name, df.loc[te, "target_readable"].to_numpy(), (prob >= .5).astype(int), prob,
                                    f"semester_transfer:{str(train_val)}_to_{str(test_val)}", 1))
    return rows


def robustness(df: pd.DataFrame, models: Dict[str, Pipeline]) -> List[Dict]:
    """Evaluate test-time feature missingness, preserving the target labels."""
    rng = np.random.default_rng(20260926)
    X, y = df[FEATURES], df.target_readable.to_numpy()
    out = []
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=77)
    for condition, frac in [("clean", 0.0), ("20pct_feature_missing", 0.2), ("40pct_feature_missing", 0.4)]:
        for name, model in models.items():
            preds, probs, ys = [], [], []
            for tr, te in cv.split(X, y):
                train = X.iloc[tr].copy(); test = X.iloc[te].copy()
                if frac:
                    for c in FEATURES:
                        mask = rng.random(len(test)) < frac
                        test.loc[mask, c] = np.nan
                model.fit(train, y[tr])
                probs.extend(model.predict_proba(test)[:, 1]); preds.extend(model.predict(test)); ys.extend(y[te])
            out.append(metric_row(name, np.array(ys), np.array(preds), np.array(probs), f"missingness:{condition}", 1))
    return out


def interpretability(df: pd.DataFrame, models: Dict[str, Pipeline]) -> Dict:
    X, y = df[FEATURES], df.target_readable
    result = {}
    for name, model in models.items():
        model.fit(X, y)
        prep = model.named_steps["prep"]
        names = prep.get_feature_names_out()
        est = model.named_steps["model"]
        if name == "logistic_regression":
            co = est.coef_[0]
            result[name] = {"intercept": float(est.intercept_[0]), "top_positive_coefficients": [{"feature": str(names[i]), "coefficient": float(co[i])} for i in np.argsort(co)[-10:][::-1]], "top_negative_coefficients": [{"feature": str(names[i]), "coefficient": float(co[i])} for i in np.argsort(co)[:10]]}
        elif name == "shallow_decision_tree":
            result[name] = {"rules": export_text(est, feature_names=list(names), decimals=3)}
        else:
            imp = est.feature_importances_
            result[name] = {"feature_importance": [{"feature": str(names[i]), "importance": float(imp[i])} for i in np.argsort(imp)[::-1][:15]], "interpretation_note": "Associational importance only; not causal."}
    return result


def failure_cases(df: pd.DataFrame, models: Dict[str, Pipeline]) -> List[Dict]:
    X, y = df[FEATURES], df.target_readable.to_numpy(); rows=[]
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=20260926)
    for name, model in models.items():
        oof = np.zeros(len(df))
        for tr, te in cv.split(X, y):
            model.fit(X.iloc[tr], y[tr]); oof[te] = model.predict_proba(X.iloc[te])[:,1]
        for i in np.argsort(np.abs(oof-y))[::-1][:5]:
            rows.append({"model": name, "record_id": str(df.iloc[i].record_id), "target_readable": int(y[i]), "predicted_probability": float(oof[i]), "error": int((oof[i]>=.5)!=y[i]), "reason": "high-confidence disagreement with AI provisional target"})
    return rows


def main() -> None:
    df = build_data(); models = make_models()
    rows = repeated_cv(df, models)
    transfer = semester_transfer(df, models)
    robust = robustness(df, models)
    interp = interpretability(df, models)
    failures = failure_cases(df, models)
    all_metrics = rows + transfer + robust
    summary = []
    for (model, split), g in pd.DataFrame(rows).groupby(["model", "split"]):
        summary.append({"model": model, "split": split, "n_folds": int(len(g)), **{f"{c}_mean": float(g[c].mean()) for c in ["accuracy","balanced_accuracy","f1","roc_auc","brier","log_loss"]}, **{f"{c}_sd": float(g[c].std(ddof=1)) for c in ["accuracy","balanced_accuracy","f1","roc_auc","brier","log_loss"]}})
    def sha(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    try:
        head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        head = "UNAVAILABLE"
    meta = {"status": "DEVELOPMENT_ONLY", "claim_gate": "INSUFFICIENT_FOR_STRONG_ML_CLAIM", "target": "AI provisional readability (L1..L6 vs NO_EVIDENCE/UNDETERMINED)", "n": int(len(df)), "positive_n": int(df.target_readable.sum()), "negative_n": int((1-df.target_readable).sum()), "human_r1_valid": 0, "human_r2_valid": 0, "formal_gate": "NOT_RUN", "git_head_at_run": head, "input_sha256": {str(AI_PATH.relative_to(ROOT)): sha(AI_PATH), str(PILOT_PATH.relative_to(ROOT)): sha(PILOT_PATH)}, "split_policy": "No true validation/holdout/external labels. Repeated 4-fold CV (25 repeats) is development evidence only.", "external_transfer": "NOT_EVALUABLE: remaining 70 Pilot records have no labels; no independent external dataset.", "features": FEATURES, "excluded_label_derived_features": ["student_evidence_bloom", "evidence_confidence", "confidence", "prompt_induced", "content_relation", "task_bloom"], "handcrafted_comparison": "Current handcrafted model is a post-label reliability-weighted measurement transform, not a pre-label predictor; direct predictive superiority comparison is not identified."}
    (OUT/"ml_results.csv").write_text(pd.DataFrame(all_metrics).to_csv(index=False), encoding="utf-8")
    (OUT/"ml_results.json").write_text(json.dumps({"metadata":meta,"summary":summary,"all_metrics":all_metrics,"interpretability":interp,"failure_cases":failures}, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT/"ml_interpretability.md").write_text("# ML challenger interpretability\n\nStatus: `DEVELOPMENT_ONLY`; coefficients and rules describe associations with the AI provisional target. They are not causal explanations.\n\n" + "\n".join(f"## {k}\n\n```text\n{json.dumps(v, ensure_ascii=False, indent=2) if k != 'shallow_decision_tree' else v['rules']}\n```" for k,v in interp.items()), encoding="utf-8")
    fdf = pd.DataFrame(failures)
    cols = list(fdf.columns)
    table = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    table += ["| " + " | ".join(str(row[c]).replace("|", "/") for c in cols) + " |" for _, row in fdf.iterrows()]
    (OUT/"ml_failure_cases.md").write_text("# ML challenger failure cases\n\nThese are disagreements with the AI provisional readability target, not human-label errors.\n\n" + "\n".join(table), encoding="utf-8")
    print(json.dumps({"out": str(OUT), "n": len(df), "positive": int(df.target_readable.sum()), "summary": summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
