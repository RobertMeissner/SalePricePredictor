from typing import Protocol

import pandas as pd


class DataRepository(Protocol):
    """
    Port interface for data access operations
    """

    def load_raw(self) -> pd.DataFrame: ...

    def load_interim(self) -> pd.DataFrame: ...

    def save_interim(self, df: pd.DataFrame, metadata: dict) -> None: ...

    def load_metadata(self) -> dict: ...
