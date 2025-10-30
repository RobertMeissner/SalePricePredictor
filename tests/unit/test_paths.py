"""
Unit tests for paths configuration.
"""

from pathlib import Path

from src.config.paths import CONFIG_DIR, PROJECT_ROOT


class TestPaths:
    """Test path configurations."""

    def test_project_root_is_path(self):
        """Test that PROJECT_ROOT is a Path object."""
        assert isinstance(PROJECT_ROOT, Path)

    def test_config_dir_is_path(self):
        """Test that CONFIG_DIR is a Path object."""
        assert isinstance(CONFIG_DIR, Path)
