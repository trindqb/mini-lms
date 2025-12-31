
# lms/storage/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd

class StorageBackend(ABC):
    @abstractmethod
    def save_text(self, row: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def save_mcq(self, row: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def save_audio(self, row: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def fetch_recent(self, limit: int = 50) -> pd.DataFrame:
        pass

    @abstractmethod
    def export_all(self) -> pd.DataFrame:
        pass
