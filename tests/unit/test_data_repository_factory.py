"""
Unit tests for data repository factory.
"""

from omegaconf import OmegaConf
import pytest

from src.adapters.factory import create_data_repository
from src.adapters.filesystem_repository import FileSystemDataRepository


class TestDataRepositoryFactory:
    """Test create_data_repository factory function."""

    def test_create_filesystem_repository(self):
        """Test creating filesystem repository."""
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

    def test_create_repository_defaults_to_filesystem(self):
        """Test that factory defaults to filesystem if type not specified."""
        config = OmegaConf.create(
            {
                "data": {
                    "raw_path": "data/raw/test.csv",
                }
            }
        )

        repo = create_data_repository(config)
        assert isinstance(repo, FileSystemDataRepository)

    def test_create_repository_with_no_data_config(self):
        """Test creating repository with minimal config."""
        config = OmegaConf.create({})

        repo = create_data_repository(config)
        assert isinstance(repo, FileSystemDataRepository)

    def test_create_repository_unknown_type_raises_error(self):
        """Test that unknown repository type raises ValueError."""
        config = OmegaConf.create(
            {
                "data": {
                    "repository_type": "unknown_type",
                }
            }
        )

        with pytest.raises(ValueError, match="Unknown repository type"):
            create_data_repository(config)

    def test_create_repository_with_unsupported_type(self):
        """Test that unsupported types (postgresql, s3, api) raise ValueError."""
        for repo_type in ["postgresql", "s3", "api"]:
            config = OmegaConf.create(
                {
                    "data": {
                        "repository_type": repo_type,
                    }
                }
            )

            with pytest.raises(ValueError, match="Unknown repository type"):
                create_data_repository(config)
