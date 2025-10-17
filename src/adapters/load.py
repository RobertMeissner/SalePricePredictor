import json

import pandas as pd
import polars as pl

from src.config import (
    INTERIM_DATA_DIR,
    INTERIM_DATA_FILENAME,
    INTERIM_METADATA_FILENAME,
    RAW_DATA,
    RAW_DATA_DIR,
)


def raw() -> pd.DataFrame:
    """Load raw dataset from data/raw/"""
    return pl.read_csv(
        RAW_DATA_DIR / RAW_DATA, try_parse_dates=True, infer_schema_length=10000, null_values="NA"
    ).to_pandas()


def interim() -> pd.DataFrame:
    """Load interim dataset from data/interim/"""
    return pd.read_parquet(INTERIM_DATA_DIR / INTERIM_DATA_FILENAME)


def preprocessing_metadata() -> dict:
    with open(INTERIM_DATA_DIR / INTERIM_METADATA_FILENAME, "r") as f:
        return json.load(f)
