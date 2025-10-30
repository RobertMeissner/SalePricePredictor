"""
Shared test fixtures for SalePricePredictor tests.
"""

import tempfile
from pathlib import Path
from typing import Generator

from omegaconf import DictConfig, OmegaConf
import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create a sample dataframe for testing."""
    return pd.DataFrame(
        {
            "Id": [1, 2, 3, 4, 5],
            "MSSubClass": [60, 20, 60, 70, 60],
            "LotArea": [8450, 9600, 11250, 9550, 14260],
            "OverallQual": [7, 6, 7, 7, 8],
            "YearBuilt": [2003, 1976, 2001, 1915, 2000],
            "GrLivArea": [1710, 1262, 1786, 1717, 2198],
            "BedroomAbvGr": [3, 3, 3, 3, 4],
            "SalePrice": [208500, 181500, 223500, 140000, 250000],
        }
    )


@pytest.fixture
def sample_raw_csv_path(sample_dataframe: pd.DataFrame) -> Generator[Path, None, None]:
    """Create a temporary CSV file with sample data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "raw.csv"
        sample_dataframe.to_csv(csv_path, index=False)
        yield csv_path


@pytest.fixture
def sample_config() -> DictConfig:
    """Create a sample Hydra configuration for testing."""
    config_dict = {
        "data": {
            "repository_type": "filesystem",
            "raw_path": "data/raw/raw.csv",
            "interim_path": "data/interim/interim.parquet",
            "metadata_path": "data/interim/interim_metadata.json",
        },
        "preprocessing": {
            "drop_columns": ["Id"],
            "target_column": "SalePrice",
        },
    }
    return OmegaConf.create(config_dict)


@pytest.fixture
def sample_config_with_temp_paths(
    tmp_path: Path,
) -> DictConfig:
    """Create a config with temporary file paths."""
    config_dict = {
        "data": {
            "repository_type": "filesystem",
            "raw_path": str(tmp_path / "raw.csv"),
            "interim_path": str(tmp_path / "interim.parquet"),
            "metadata_path": str(tmp_path / "interim_metadata.json"),
        },
        "preprocessing": {
            "drop_columns": ["Id"],
            "target_column": "SalePrice",
        },
    }
    return OmegaConf.create(config_dict)


@pytest.fixture
def sample_preprocessing_config() -> DictConfig:
    """Create a sample preprocessing configuration."""
    config_dict = {
        "preprocessing": {
            "drop_columns": ["Id"],
            "target_column": "SalePrice",
            "imputation": {
                "strategy": "mean",
                "columns": ["LotArea", "GrLivArea"],
            },
        }
    }
    return OmegaConf.create(config_dict)


@pytest.fixture
def sample_experiment_config() -> DictConfig:
    """Create a sample experiment configuration."""
    config_dict = {
        "name": "test-experiment",
        "run_name": "test-run",
        "save": False,
        "data": {
            "repository_type": "filesystem",
            "raw_path": "data/raw/raw.csv",
        },
        "preprocessing": {
            "drop_columns": ["Id"],
            "target_column": "SalePrice",
        },
        "model": {
            "type": "linear",
            "params": {
                "fit_intercept": True,
            },
        },
    }
    return OmegaConf.create(config_dict)
