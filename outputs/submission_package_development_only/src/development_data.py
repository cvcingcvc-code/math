"""Explicit annotation-data loader for downstream development experiments.

This adapter keeps AI provisional labels separate from formal human/Gate data.
Formal mode remains the default and reads the existing exploratory prelabel path.
Development mode must be selected explicitly and is always validated as
AI_PROVISIONAL / DEVELOPMENT_ONLY.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FORMAL_EXPLORATORY_PATH = ROOT / "data" / "processed" / "pilot_ai_prelabel.csv"
DEVELOPMENT_PATH = ROOT / "data" / "annotations" / "ai" / "pilot_ai_provisional.csv"

DataMode = Literal["formal", "development"]


def load_annotation_data(mode: DataMode = "formal", path: Path | None = None) -> pd.DataFrame:
    """Load annotation-like data without allowing silent source substitution.

    ``formal`` is the default and preserves the pre-existing path. ``development``
    requires the dedicated provisional file and validates its identity markers.
    The returned frame is never eligible as human annotation or formal Gate data.
    """
    if mode not in ("formal", "development"):
        raise ValueError(f"unsupported data mode: {mode!r}")

    expected_path = FORMAL_EXPLORATORY_PATH if mode == "formal" else DEVELOPMENT_PATH
    if path is not None and mode == "development" and Path(path).resolve() != DEVELOPMENT_PATH.resolve():
        raise ValueError("development mode only accepts data/annotations/ai/pilot_ai_provisional.csv")
    source_path = Path(path) if path is not None else expected_path
    frame = pd.read_csv(source_path, encoding="utf-8-sig", dtype=str, keep_default_na=False)

    if mode == "development":
        required = {"record_id", "annotation_source", "annotation_status"}
        missing = sorted(required - set(frame.columns))
        if missing:
            raise ValueError(f"development data missing required columns: {missing}")
        if not frame["record_id"].is_unique:
            raise ValueError("development data record_id must be unique")
        if set(frame["annotation_source"]) != {"AI_PROVISIONAL"}:
            raise ValueError("development data must remain annotation_source=AI_PROVISIONAL")
        if set(frame["annotation_status"]) != {"DEVELOPMENT_ONLY"}:
            raise ValueError("development data must remain annotation_status=DEVELOPMENT_ONLY")
        print("DATA_MODE=DEVELOPMENT_ONLY / AI_PROVISIONAL")
    else:
        print(f"DATA_MODE=FORMAL_EXPLORATORY; source={source_path.relative_to(ROOT)}")

    return frame


def formal_gate_eligible(mode: DataMode) -> bool:
    """Return whether a loaded annotation source can enter the formal Gate."""
    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load annotation data with an explicit source boundary.")
    parser.add_argument("--mode", choices=["formal", "development"], default="formal")
    args = parser.parse_args()
    data = load_annotation_data(args.mode)
    print(f"rows={len(data)}")
    if args.mode == "development":
        print("formal_gate_eligible=False")
