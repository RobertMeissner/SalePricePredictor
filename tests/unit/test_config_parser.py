"""Test config parser."""

from pathlib import Path

from omegaconf import DictConfig

from src.config_parser import load_config

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestConfigParser:
    def test_load_main_config(self):
        """Test loading main config.yaml with Hydra composition."""
        config_dir = PROJECT_ROOT / "tests" / "config"
        cfg = load_config(config_dir, "config")

        assert isinstance(cfg, DictConfig)
        assert "training" in cfg
        assert "preprocessing" in cfg
        assert cfg.save is True

    def test_load_test_experiment_config(self):
        """Test loading test experiment config."""
        config_dir = PROJECT_ROOT / "tests" / "config"
        cfg = load_config(config_dir, "experiment")

        assert isinstance(cfg, DictConfig)

        # Validate preprocessing section
        assert "preprocessing" in cfg
        assert "drop_columns" in cfg.preprocessing
        assert "PoolQC" in cfg.preprocessing.drop_columns

        # Validate categorical transforms
        assert "categorical_transforms" in cfg.preprocessing
        assert "FireplaceQu" in cfg.preprocessing.categorical_transforms
        assert cfg.preprocessing.categorical_transforms.FireplaceQu.type == "binary"

        # Validate pipeline structure
        assert "pipeline" in cfg.preprocessing
        assert len(cfg.preprocessing.pipeline) == 4
        assert cfg.preprocessing.pipeline[0].step == "drop_columns"

        # Validate training section
        assert "training" in cfg
        assert cfg.training.test_size == 0.2
        assert cfg.training.target_column == "SalePrice"
        assert "r2_score" in cfg.training.metrics

        # Validate model section
        assert "model" in cfg
        assert cfg.model.params.fit_intercept is True
