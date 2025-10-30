"""
Unit tests for FileSystemDataRepository adapter.
"""

import json
from pathlib import Path

from omegaconf import DictConfig, OmegaConf
import pandas as pd
import pytest

from src.adapters.filesystem_repository import FileSystemDataRepository


class TestFileSystemDataRepository:
    """Test FileSystemDataRepository adapter."""

    def test_init_with_flat_config(self, sample_config: DictConfig):
        """Test initialization with flat config structure."""
        repo = FileSystemDataRepository(sample_config)

        assert repo.raw_path.name == "raw.csv"
        assert repo.interim_path.name == "interim.parquet"
        assert repo.metadata_path.name == "interim_metadata.json"

    def test_init_with_nested_config(self):
        """Test initialization with nested config structure."""
        config = OmegaConf.create(
            {
                "data": {
                    "filesystem": {
                        "raw_path": "data/raw/test.csv",
                        "interim_path": "data/interim/test.parquet",
                        "metadata_path": "data/interim/test_meta.json",
                    }
                }
            }
        )
        repo = FileSystemDataRepository(config)

        assert repo.raw_path.name == "test.csv"
        assert repo.interim_path.name == "test.parquet"
        assert repo.metadata_path.name == "test_meta.json"

    def test_init_with_absolute_paths(self, tmp_path: Path):
        """Test initialization with absolute paths."""
        config = OmegaConf.create(
            {
                "data": {
                    "raw_path": str(tmp_path / "raw.csv"),
                    "interim_path": str(tmp_path / "interim.parquet"),
                    "metadata_path": str(tmp_path / "metadata.json"),
                }
            }
        )
        repo = FileSystemDataRepository(config)

        assert repo.raw_path.is_absolute()
        assert repo.interim_path.is_absolute()
        assert repo.metadata_path.is_absolute()

    def test_load_raw(self, tmp_path: Path, sample_dataframe: pd.DataFrame):
        """Test loading raw CSV data."""
        # Create test CSV
        raw_path = tmp_path / "raw.csv"
        sample_dataframe.to_csv(raw_path, index=False)

        # Configure repository
        config = OmegaConf.create(
            {
                "data": {
                    "raw_path": str(raw_path),
                    "interim_path": str(tmp_path / "interim.parquet"),
                    "metadata_path": str(tmp_path / "metadata.json"),
                }
            }
        )
        repo = FileSystemDataRepository(config)

        # Load and verify
        df = repo.load_raw()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert "SalePrice" in df.columns
        pd.testing.assert_frame_equal(df, sample_dataframe)

    def test_save_and_load_interim(
        self, tmp_path: Path, sample_dataframe: pd.DataFrame
    ):
        """Test saving and loading interim data with metadata."""
        # Configure repository
        config = OmegaConf.create(
            {
                "data": {
                    "raw_path": str(tmp_path / "raw.csv"),
                    "interim_path": str(tmp_path / "interim.parquet"),
                    "metadata_path": str(tmp_path / "metadata.json"),
                }
            }
        )
        repo = FileSystemDataRepository(config)

        # Save interim data
        metadata = {
            "columns": list(sample_dataframe.columns),
            "rows": len(sample_dataframe),
            "preprocessing": "test",
        }
        repo.save_interim(sample_dataframe, metadata)

        # Verify files exist
        assert repo.interim_path.exists()
        assert repo.metadata_path.exists()

        # Load and verify interim data
        df_loaded = repo.load_interim()
        pd.testing.assert_frame_equal(df_loaded, sample_dataframe)

        # Load and verify metadata
        metadata_loaded = repo.load_metadata()
        assert metadata_loaded["columns"] == list(sample_dataframe.columns)
        assert metadata_loaded["rows"] == len(sample_dataframe)
        assert metadata_loaded["preprocessing"] == "test"

    def test_save_interim_creates_directory(self, tmp_path: Path):
        """Test that save_interim creates parent directories if needed."""
        # Configure repository with nested path that doesn't exist
        interim_path = tmp_path / "nested" / "dir" / "interim.parquet"
        config = OmegaConf.create(
            {
                "data": {
                    "raw_path": str(tmp_path / "raw.csv"),
                    "interim_path": str(interim_path),
                    "metadata_path": str(tmp_path / "nested" / "dir" / "metadata.json"),
                }
            }
        )
        repo = FileSystemDataRepository(config)

        # Save should create directories
        df = pd.DataFrame({"A": [1, 2, 3]})
        metadata = {"test": "data"}
        repo.save_interim(df, metadata)

        # Verify directory was created and file exists
        assert interim_path.parent.exists()
        assert interim_path.exists()

    def test_load_metadata_with_complex_data(self, tmp_path: Path):
        """Test loading metadata with nested structures."""
        # Create metadata file
        metadata_path = tmp_path / "metadata.json"
        metadata = {
            "preprocessing": {
                "steps": ["drop", "impute", "encode"],
                "params": {"strategy": "mean"},
            },
            "features": ["A", "B", "C"],
            "timestamp": "2024-01-01",
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

        # Configure repository
        config = OmegaConf.create(
            {
                "data": {
                    "raw_path": str(tmp_path / "raw.csv"),
                    "interim_path": str(tmp_path / "interim.parquet"),
                    "metadata_path": str(metadata_path),
                }
            }
        )
        repo = FileSystemDataRepository(config)

        # Load and verify
        loaded = repo.load_metadata()
        assert loaded["preprocessing"]["steps"] == ["drop", "impute", "encode"]
        assert loaded["features"] == ["A", "B", "C"]

    def test_resolve_path_relative(self, sample_config: DictConfig):
        """Test that relative paths are resolved correctly."""
        repo = FileSystemDataRepository(sample_config)

        resolved = repo._resolve_path("data/test.csv")
        assert resolved.is_absolute()
        assert "data/test.csv" in str(resolved)

    def test_resolve_path_absolute(self, sample_config: DictConfig):
        """Test that absolute paths remain unchanged."""
        repo = FileSystemDataRepository(sample_config)

        abs_path = "/absolute/path/test.csv"
        resolved = repo._resolve_path(abs_path)
        assert str(resolved) == abs_path
