"""Test sklearn pipeline builder."""

from pathlib import Path

import pandas as pd

from src.config_parser import load_config
from src.preprocessing.sklearn_pipeline_builder import build_pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestSklearnPipelineBuilder:
    def test_build_pipeline_from_config(self):
        """Test building pipeline from experiment config."""
        config_dir = PROJECT_ROOT / "tests" / "config"
        cfg = load_config(config_dir, "experiment")

        pipeline = build_pipeline(cfg)

        assert pipeline is not None
        assert len(pipeline.steps) > 0
        assert pipeline.steps[0][0] == "drop_columns"

    def test_pipeline_transforms_data(self):
        """Test pipeline executes transformations on data."""
        config_dir = PROJECT_ROOT / "tests" / "config"
        cfg = load_config(config_dir, "experiment")

        # Create toy data
        df = pd.DataFrame(
            {
                "Id": [1, 2, 3],
                "PoolQC": ["Ex", "Gd", None],  # Should be dropped
                "FireplaceQu": ["Ex", "Fa", None],  # Should be mapped
                "LotArea": [8000, 9600, 11250],
                "SalePrice": [200000, 250000, 300000],
            }
        )

        pipeline = build_pipeline(cfg)
        df_transformed = pipeline.fit_transform(df)

        # Validate drops happened
        assert "PoolQC" not in df_transformed.columns

        # Validate FireplaceQu was mapped (Ex→1, Fa→0, None→0)
        assert "FireplaceQu" in df_transformed.columns
        assert df_transformed["FireplaceQu"].tolist() == [1, 0, 0]

        # Validate other columns remain
        assert "Id" in df_transformed.columns
        assert "LotArea" in df_transformed.columns
