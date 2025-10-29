"""Test sklearn pipeline builder."""

from pathlib import Path

import pandas as pd

from src.config.hydra_loader import load_config
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
                "FireplaceQu": ["Ex", "Fa", None],  # Should be mapped then scaled
                "LotArea": [8000, 9600, 11250],
                "SalePrice": [200000, 250000, 300000],
            }
        )

        pipeline = build_pipeline(cfg)
        df_transformed = pipeline.fit_transform(df)

        # Validate drops happened
        assert "PoolQC" not in df_transformed.columns

        # Validate FireplaceQu was mapped and scaled
        assert "FireplaceQu" in df_transformed.columns
        # After mapping (Ex→1, Fa→0, None→0) and scaling, mean should be ~0
        assert abs(df_transformed["FireplaceQu"].mean()) < 1e-10

        # Validate other columns remain
        assert "Id" in df_transformed.columns
        assert "LotArea" in df_transformed.columns

    def test_pipeline_with_imputation_and_scaling(self):
        """Test pipeline with all steps: drops, transforms, imputation, and scaling."""
        config_dir = PROJECT_ROOT / "tests" / "config"
        cfg = load_config(config_dir, "experiment")

        # Create toy data with nulls
        df = pd.DataFrame(
            {
                "Id": [1, 2, 3, 4],
                "PoolQC": ["Ex", None, "Gd", None],  # Should be dropped
                "FireplaceQu": ["Ex", "Fa", None, "Gd"],  # Should be mapped
                "LotArea": [8000, None, 11250, 9600],  # Should be imputed and scaled
                "YearBuilt": [2000, 2010, None, 1995],  # Should be imputed and scaled
                "SalePrice": [200000, 250000, 300000, 275000],  # Should be excluded from scaling
            }
        )

        pipeline = build_pipeline(cfg)
        df_transformed = pipeline.fit_transform(df)

        # Validate drops
        assert "PoolQC" not in df_transformed.columns

        # Validate categorical mapping and scaling
        # FireplaceQu is mapped (Ex→1, Fa→0, None→0, Gd→1) then scaled
        assert "FireplaceQu" in df_transformed.columns
        # After scaling, numeric columns have mean ~0
        assert abs(df_transformed["FireplaceQu"].mean()) < 1e-10

        # Validate imputation - no nulls remain in LotArea and YearBuilt
        assert not df_transformed["LotArea"].isnull().any()
        assert not df_transformed["YearBuilt"].isnull().any()

        # Validate scaling - LotArea, YearBuilt, and FireplaceQu should be scaled (mean ~0, std ~1)
        # but Id and SalePrice should not be scaled (they're in exclude_columns)
        assert abs(df_transformed["LotArea"].mean()) < 1e-10  # Close to 0
        assert abs(df_transformed["YearBuilt"].mean()) < 1e-10
        assert df_transformed["Id"].mean() == 2.5  # Original scale: (1+2+3+4)/4
        assert df_transformed["SalePrice"].mean() == 256250  # Original scale
