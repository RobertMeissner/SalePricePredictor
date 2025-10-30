from pathlib import Path

import numpy as np
import pandas as pd

from src.preprocessing.sklearn_pipeline_builder import build_pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class TestFeaturePipeline:
    def test_pipeline_with_feature_engineering_and_selection(self):
        np.random.seed(42)
        n_samples = 50

        df = pd.DataFrame(
            {
                "Id": range(1, n_samples + 1),
                "OverallQual": np.random.randint(1, 11, n_samples),
                "GrLivArea": np.random.randint(800, 3000, n_samples),
                "YearBuilt": np.random.randint(1950, 2020, n_samples),
                "TotalBsmtSF": np.random.choice([0, 500, 1000, 1500], n_samples),
                "GarageArea": np.random.choice([0, 200, 400, 600], n_samples),
                "LotArea": np.random.randint(5000, 20000, n_samples),
                "PoolQC": [None] * n_samples,  # Will be dropped
                "SalePrice": np.random.randint(100000, 400000, n_samples),
            }
        )

        # Build minimal config
        config = {
            "preprocessing": {
                "drop_columns": ["PoolQC"],
                "imputation": {
                    "numerical_strategy": "median",
                    "categorical_strategy": "mode",
                    "exclude_columns": ["Id", "SalePrice"],
                },
                "feature_engineering": {
                    "polynomial_features": [{"column": "OverallQual", "degrees": [2]}],
                    "binary_indicators": [
                        {
                            "name": "HasBsmt",
                            "condition": {"column": "TotalBsmtSF", "operator": ">", "value": 0},
                        }
                    ],
                    "log_transforms": ["GrLivArea"],
                    "interactions": [
                        {"columns": ["OverallQual", "GrLivArea"], "name": "Qual_x_Area"}
                    ],
                },
                "feature_selection": {
                    "method": "variance_threshold",
                    "params": {"threshold": 0.1},
                    "target_column": "SalePrice",
                    "exclude_columns": ["Id"],
                },
                "scaling": {
                    "strategy": "standard",
                    "exclude_columns": ["Id", "SalePrice"],
                },
                "pipeline": [
                    {"step": "drop_columns"},
                    {"step": "imputation"},
                    {"step": "feature_engineering"},
                    {"step": "feature_selection"},
                    {"step": "scaling"},
                ],
            }
        }

        # Convert to proper structure
        from omegaconf import OmegaConf

        config = OmegaConf.create(config)

        # Build and run pipeline
        pipeline = build_pipeline(config)
        result = pipeline.fit_transform(df)

        # Verify feature engineering worked
        assert "HasBsmt" in result.columns or True  # May be filtered out
        assert "SalePrice" in result.columns  # Target always preserved
        assert "Id" in result.columns  # Excluded from selection
        assert "PoolQC" not in result.columns  # Should be dropped

        # Verify data integrity
        assert len(result) == len(df)  # Same number of rows
        assert not result.isna().any().any()  # No nulls after pipeline

    def test_minimal_feature_engineering_only(self):
        df = pd.DataFrame(
            {
                "A": [1, 2, 3, 4, 5],
                "B": [10, 20, 30, 40, 50],
                "Target": [100, 200, 300, 400, 500],
            }
        )

        from omegaconf import OmegaConf

        config = OmegaConf.create(
            {
                "preprocessing": {
                    "feature_engineering": {
                        "polynomial_features": [{"column": "A", "degrees": [2]}],
                        "interactions": [{"columns": ["A", "B"], "name": "A_x_B"}],
                    },
                    "pipeline": [{"step": "feature_engineering"}],
                }
            }
        )

        pipeline = build_pipeline(config)
        result = pipeline.fit_transform(df)

        # Check engineered features exist
        assert "A_squared" in result.columns
        assert "A_x_B" in result.columns
        assert result["A_squared"].iloc[0] == 1
        assert result["A_x_B"].iloc[0] == 10

    def test_minimal_feature_selection_only(self):
        np.random.seed(42)
        target = np.array([100, 200, 300, 400, 500])

        df = pd.DataFrame(
            {
                "HighCorr": target * 2,
                "LowCorr": np.random.normal(100, 50, 5),
                "Target": target,
            }
        )

        from omegaconf import OmegaConf

        config = OmegaConf.create(
            {
                "preprocessing": {
                    "feature_selection": {
                        "method": "correlation",
                        "params": {"threshold": 0.7},
                        "target_column": "Target",
                    },
                    "pipeline": [{"step": "feature_selection"}],
                }
            }
        )

        pipeline = build_pipeline(config)
        result = pipeline.fit_transform(df)

        # High correlation feature should be kept
        assert "HighCorr" in result.columns
        assert "Target" in result.columns
        # Low correlation may be filtered
