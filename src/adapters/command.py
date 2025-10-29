"""
Data writing adapters (DEPRECATED - use FileSystemDataRepository)

These functions are kept for backward compatibility but are deprecated.
New code should use the FileSystemDataRepository class which implements
the DataRepository port interface.
"""

import json
import warnings

from loguru import logger

from src.config import (
    INTERIM_DATA_DIR,
    INTERIM_DATA_FILENAME,
    INTERIM_METADATA_FILENAME,
)


def write_interim(df_preprocessed):
    """
    Parquet file storage of interim data

    DEPRECATED: Use FileSystemDataRepository.save_interim() instead.
    This function is kept for backward compatibility.
    """
    warnings.warn(
        "Function 'write_interim()' is deprecated. "
        "Use FileSystemDataRepository.save_interim() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    output_path = INTERIM_DATA_DIR / INTERIM_DATA_FILENAME
    logger.debug(f"Saving preprocessed data to {output_path}")
    df_preprocessed.to_parquet(output_path, index=False)


def write_interim_metadata(metadata):
    """
    JSON file storage of metadata, e.g., used configuration

    DEPRECATED: Use FileSystemDataRepository.save_interim() instead.
    This function is kept for backward compatibility.
    """
    warnings.warn(
        "Function 'write_interim_metadata()' is deprecated. "
        "Use FileSystemDataRepository.save_interim() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    metadata_path = INTERIM_DATA_DIR / INTERIM_METADATA_FILENAME
    logger.debug(f"Saving preprocessing metadata to {metadata_path}")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
