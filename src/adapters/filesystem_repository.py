import json
from pathlib import Path

from loguru import logger
from omegaconf import DictConfig
import pandas as pd
import polars as pl

from src.config.paths import PROJECT_ROOT


class FileSystemDataRepository:
    """
    Filesystem adapter implementing DataRepository port.

    Loads and writes data from local CSV/Parquet files.
    Uses configuration from Hydra DictConfig for file paths.
    """

    def __init__(self, config: DictConfig):
        """
        Initialize filesystem repository with configuration.

        Args:
            config: Hydra DictConfig containing data paths under config.data
        """
        self.config = config

        # Get paths from config, with fallback to defaults
        data_config = config.data if hasattr(config, "data") else {}

        # Support both flat and nested config structures
        if hasattr(data_config, "filesystem"):
            fs_config = data_config.filesystem
            self.raw_path = self._resolve_path(fs_config.raw_path)
            self.interim_path = self._resolve_path(fs_config.interim_path)
            self.metadata_path = self._resolve_path(fs_config.metadata_path)
        else:
            # Fallback to flat structure or defaults
            self.raw_path = self._resolve_path(
                getattr(data_config, "raw_path", "data/raw/raw.csv")
            )
            self.interim_path = self._resolve_path(
                getattr(data_config, "interim_path", "data/interim/interim.parquet")
            )
            self.metadata_path = self._resolve_path(
                getattr(data_config, "metadata_path", "data/interim/interim_metadata.json")
            )

        logger.debug("FileSystemDataRepository initialized:")
        logger.debug(f"  Raw path: {self.raw_path}")
        logger.debug(f"  Interim path: {self.interim_path}")
        logger.debug(f"  Metadata path: {self.metadata_path}")

    def _resolve_path(self, path_str: str) -> Path:
        """
        Resolve path string to absolute Path, handling relative paths.

        Args:
            path_str: Path as string, may be relative or absolute

        Returns:
            Absolute Path object
        """
        path = Path(path_str)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path

    def load_raw(self) -> pd.DataFrame:
        """
        Load raw dataset from CSV file.

        Uses Polars for efficient CSV parsing with automatic type inference,
        then converts to pandas for compatibility with sklearn.

        Returns:
            pd.DataFrame: Raw house pricing data with all original features
        """
        logger.debug(f"Loading raw data from {self.raw_path}")

        df = pl.read_csv(
            self.raw_path,
            try_parse_dates=True,
            infer_schema_length=10000,
            null_values="NA",
        ).to_pandas()

        logger.debug(f"Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    def load_interim(self) -> pd.DataFrame:
        """
        Load interim preprocessed dataset from Parquet file.

        Returns:
            pd.DataFrame: Preprocessed data after initial transformations
        """
        logger.debug(f"Loading interim data from {self.interim_path}")

        df = pd.read_parquet(self.interim_path)

        logger.debug(f"Loaded interim data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    def save_interim(self, df: pd.DataFrame, metadata: dict) -> None:
        """
        Save interim preprocessed dataset with metadata.

        Args:
            df: Preprocessed dataframe to save
            metadata: Dictionary containing preprocessing metadata
        """
        # Ensure directory exists
        self.interim_path.parent.mkdir(parents=True, exist_ok=True)

        # Save dataframe as Parquet
        logger.debug(f"Saving preprocessed data to {self.interim_path}")
        df.to_parquet(self.interim_path, index=False)

        # Save metadata as JSON
        logger.debug(f"Saving preprocessing metadata to {self.metadata_path}")
        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(
            f"Saved interim data: {df.shape[0]} rows, {df.shape[1]} columns to {self.interim_path}"
        )

    def load_metadata(self) -> dict:
        """
        Load preprocessing metadata from JSON file.

        Returns:
            dict: Metadata about the preprocessing pipeline
        """
        logger.debug(f"Loading metadata from {self.metadata_path}")

        with open(self.metadata_path, "r") as f:
            metadata = json.load(f)

        logger.debug(f"Loaded metadata with keys: {list(metadata.keys())}")
        return metadata
