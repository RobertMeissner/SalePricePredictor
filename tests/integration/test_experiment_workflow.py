"""
Integration tests for end-to-end experiment workflow.
"""

from pathlib import Path

from omegaconf import OmegaConf
import pandas as pd
import pytest

from src.adapters.factory import create_data_repository
from src.adapters.filesystem_repository import FileSystemDataRepository


class TestExperimentWorkflow:
    """Test complete experiment workflow integration."""

    def test_create_repository_from_config(self):
        """Test creating repository through factory."""
        config = OmegaConf.create(
            {
                "data": {
                    "repository_type": "filesystem",
                    "raw_path": "data/raw/test.csv",
                    "interim_path": "data/interim/test.parquet",
                    "metadata_path": "data/interim/test_meta.json",
                }
            }
        )

        repo = create_data_repository(config)
        assert isinstance(repo, FileSystemDataRepository)
        assert repo.raw_path.name == "test.csv"

    def test_full_data_pipeline_with_repository(
        self, tmp_path: Path, sample_dataframe: pd.DataFrame
    ):
        """Test complete data pipeline: save raw -> load raw -> save interim -> load interim."""
        # Setup paths
        raw_path = tmp_path / "raw.csv"
        interim_path = tmp_path / "interim.parquet"
        metadata_path = tmp_path / "metadata.json"

        # Save raw data
        sample_dataframe.to_csv(raw_path, index=False)

        # Create repository
        config = OmegaConf.create(
            {
                "data": {
                    "repository_type": "filesystem",
                    "raw_path": str(raw_path),
                    "interim_path": str(interim_path),
                    "metadata_path": str(metadata_path),
                }
            }
        )
        repo = create_data_repository(config)

        # Load raw
        df_raw = repo.load_raw()
        assert len(df_raw) == 5

        # Save interim
        metadata = {"step": "test", "rows": len(df_raw)}
        repo.save_interim(df_raw, metadata)

        # Load interim
        df_interim = repo.load_interim()
        pd.testing.assert_frame_equal(df_interim, df_raw)

        # Load metadata
        loaded_metadata = repo.load_metadata()
        assert loaded_metadata["step"] == "test"
        assert loaded_metadata["rows"] == 5

    def test_repository_handles_missing_raw_file(self, tmp_path: Path):
        """Test that repository handles missing raw file gracefully."""
        config = OmegaConf.create(
            {
                "data": {
                    "repository_type": "filesystem",
                    "raw_path": str(tmp_path / "nonexistent.csv"),
                    "interim_path": str(tmp_path / "interim.parquet"),
                    "metadata_path": str(tmp_path / "metadata.json"),
                }
            }
        )
        repo = create_data_repository(config)

        # Should raise appropriate error
        with pytest.raises(Exception):  # FileNotFoundError or similar
            repo.load_raw()

    def test_repository_handles_missing_interim_file(self, tmp_path: Path):
        """Test that repository handles missing interim file gracefully."""
        config = OmegaConf.create(
            {
                "data": {
                    "repository_type": "filesystem",
                    "raw_path": str(tmp_path / "raw.csv"),
                    "interim_path": str(tmp_path / "nonexistent.parquet"),
                    "metadata_path": str(tmp_path / "metadata.json"),
                }
            }
        )
        repo = create_data_repository(config)

        # Should raise appropriate error
        with pytest.raises(Exception):  # FileNotFoundError or similar
            repo.load_interim()

    def test_multiple_save_load_cycles(self, tmp_path: Path, sample_dataframe: pd.DataFrame):
        """Test multiple save/load cycles maintain data integrity."""
        config = OmegaConf.create(
            {
                "data": {
                    "repository_type": "filesystem",
                    "raw_path": str(tmp_path / "raw.csv"),
                    "interim_path": str(tmp_path / "interim.parquet"),
                    "metadata_path": str(tmp_path / "metadata.json"),
                }
            }
        )
        repo = create_data_repository(config)

        # First cycle
        metadata1 = {"cycle": 1}
        repo.save_interim(sample_dataframe, metadata1)
        df1 = repo.load_interim()
        pd.testing.assert_frame_equal(df1, sample_dataframe)

        # Second cycle - overwrite
        modified_df = sample_dataframe.copy()
        modified_df["NewColumn"] = [1, 2, 3, 4, 5]
        metadata2 = {"cycle": 2}
        repo.save_interim(modified_df, metadata2)
        df2 = repo.load_interim()

        # Verify overwrite worked
        assert "NewColumn" in df2.columns
        pd.testing.assert_frame_equal(df2, modified_df)

        # Verify metadata was overwritten
        loaded_metadata = repo.load_metadata()
        assert loaded_metadata["cycle"] == 2
