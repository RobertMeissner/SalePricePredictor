"""
Data loading adapters (DEPRECATED - use FileSystemDataRepository)

These functions are kept for backward compatibility but are deprecated.
New code should use the FileSystemDataRepository class which implements
the DataRepository port interface.
"""

import json
import warnings

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
    """
    Load raw dataset from data/raw/

    DEPRECATED: Use FileSystemDataRepository.load_raw() instead.
    This function is kept for backward compatibility.
    """
    warnings.warn(
        "Function 'raw()' is deprecated. Use FileSystemDataRepository.load_raw() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return pl.read_csv(
        RAW_DATA_DIR / RAW_DATA, try_parse_dates=True, infer_schema_length=10000, null_values="NA"
    ).to_pandas()


def interim() -> pd.DataFrame:
    """
    Load interim dataset from data/interim/

    DEPRECATED: Use FileSystemDataRepository.load_interim() instead.
    This function is kept for backward compatibility.
    """
    warnings.warn(
        "Function 'interim()' is deprecated. Use FileSystemDataRepository.load_interim() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return pd.read_parquet(INTERIM_DATA_DIR / INTERIM_DATA_FILENAME)


def preprocessing_metadata() -> dict:
    """
    Load preprocessing metadata.

    DEPRECATED: Use FileSystemDataRepository.load_metadata() instead.
    This function is kept for backward compatibility.
    """
    warnings.warn(
        "Function 'preprocessing_metadata()' is deprecated. "
        "Use FileSystemDataRepository.load_metadata() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    with open(INTERIM_DATA_DIR / INTERIM_METADATA_FILENAME, "r") as f:
        return json.load(f)
