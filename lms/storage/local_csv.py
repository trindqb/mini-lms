
# lms/storage/local_csv.py
import os
from typing import Dict, Any
import pandas as pd
from .base import StorageBackend
from lms.config import CSV_LOCAL

class LocalCSVStorage(StorageBackend):
    def _append_row(self, new_row: Dict[str, Any]) -> None:
        df = pd.read_csv(CSV_LOCAL)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_LOCAL, index=False)

    def save_text(self, row: Dict[str, Any]) -> None:
        self._append_row(row)

    def save_mcq(self, row: Dict[str, Any]) -> None:
        self._append_row(row)

    def save_audio(self, row: Dict[str, Any]) -> None:
        self._append_row(row)

    def fetch_recent(self, limit: int = 50) -> pd.DataFrame:
        df = pd.read_csv(CSV_LOCAL)
        if df.empty:
            return df
        # Assume ts is ISO string; sort by it descending
        df = df.sort_values("ts", ascending=False)
        return df.head(limit)

    def export_all(self) -> pd.DataFrame:
        return pd.read_csv(CSV_LOCAL)
