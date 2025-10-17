import json

from loguru import logger

from src.config import (
    INTERIM_DATA_DIR,
    INTERIM_DATA_FILENAME,
    INTERIM_METADATA_FILENAME,
)


def write_interim(df_preprocessed):
    """
    Parquet file storage of interim data
    """
    output_path = INTERIM_DATA_DIR / INTERIM_DATA_FILENAME
    logger.debug(f"Saving preprocessed data to {output_path}")
    df_preprocessed.to_parquet(output_path, index=False)


def write_interim_metadata(metadata):
    """
    JSON file storage of metadata, e.g., used configuration
    """
    metadata_path = INTERIM_DATA_DIR / INTERIM_METADATA_FILENAME
    logger.debug(f"Saving preprocessing metadata to {metadata_path}")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
