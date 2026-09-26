"""Encoding-tolerant reader for human annotation worksheets.

Human worksheets can be saved by local spreadsheet editors as UTF-8 or as
GB18030/GBK.  This helper only selects a decoding that preserves the file
bytes as text; it never rewrites or normalizes label values.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ENCODINGS = ("utf-8-sig", "gb18030")


def detect_text_encoding(path: Path) -> str:
    raw = Path(path).read_bytes()
    for enc in ENCODINGS:
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return "gb18030"


def read_worksheet(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False,
                       encoding=detect_text_encoding(path))
