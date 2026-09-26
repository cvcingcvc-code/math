"""Fail-closed adapter contract for a future HUMAN_VALIDATED run.

This module only validates and normalizes a supplied formal table. It does not
read current blank worksheets, run the Gate, or compute a formal result. The
downstream deterministic model must receive the returned frame and reuse the
same frozen scoring implementation used by development artifacts.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED = {"record_id", "task_bloom", "student_evidence_bloom", "confidence",
            "prompt_induced", "context_truncated", "annotation_source", "annotation_status"}

def load_human_validated(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = sorted(REQUIRED - set(frame.columns))
    if missing:
        raise ValueError(f"HUMAN_VALIDATED input missing columns: {missing}")
    if set(frame["annotation_source"]) != {"HUMAN_VALIDATED"}:
        raise ValueError("formal adapter accepts HUMAN_VALIDATED only")
    if set(frame["annotation_status"]) != {"HUMAN_VALIDATED"}:
        raise ValueError("formal adapter accepts HUMAN_VALIDATED only")
    if frame["record_id"].duplicated().any():
        raise ValueError("HUMAN_VALIDATED record_id must be unique")
    return frame

def adapter_status() -> dict[str, object]:
    return {"status": "READY_INTERFACE_ONLY", "input_identity": "HUMAN_VALIDATED",
            "model_identity": "frozen_deterministic_model", "formal_run_performed": False}
