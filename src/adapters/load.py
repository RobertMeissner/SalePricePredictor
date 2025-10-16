import pandas as pd
import polars as pl

from config import RAW_DATA, RAW_DATA_DIR


def raw() -> pd.DataFrame:
    return pl.read_csv(
        RAW_DATA_DIR / RAW_DATA, try_parse_dates=True, infer_schema_length=10000, null_values="NA"
    ).to_pandas()
