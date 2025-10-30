import numpy as np
import pandas as pd

from src.preprocessing.feature_engineering import FeatureEngineeringTransformer


class TestFeatureEngineeringTransformer:
    def test_polynomial_features(self):
        df = pd.DataFrame(
            {
                "OverallQual": [5, 7, 9],
                "GrLivArea": [1000, 1500, 2000],
                "SalePrice": [150000, 200000, 250000],
            }
        )

        config = {
            "polynomial_features": [
                {"column": "OverallQual", "degrees": [2, 3]},
                {"column": "GrLivArea", "degrees": [2]},
            ]
        }

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # Check new columns were created
        assert "OverallQual_squared" in result.columns
        assert "OverallQual_cubed" in result.columns
        assert "GrLivArea_squared" in result.columns

        # Verify calculations
        assert result["OverallQual_squared"].iloc[0] == 25
        assert result["OverallQual_cubed"].iloc[0] == 125
        assert result["GrLivArea_squared"].iloc[1] == 2250000

        # Original columns should remain
        assert "OverallQual" in result.columns
        assert "GrLivArea" in result.columns

    def test_binary_indicators(self):
        df = pd.DataFrame(
            {
                "TotalBsmtSF": [0, 500, 1000, 0],
                "GarageArea": [0, 200, 300, 400],
            }
        )

        config = {
            "binary_indicators": [
                {
                    "name": "HasBsmt",
                    "condition": {"column": "TotalBsmtSF", "operator": ">", "value": 0},
                },
                {
                    "name": "HasGarage",
                    "condition": {"column": "GarageArea", "operator": ">", "value": 0},
                },
            ]
        }

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # Check binary columns created
        assert "HasBsmt" in result.columns
        assert "HasGarage" in result.columns

        # Verify values
        assert result["HasBsmt"].tolist() == [0, 1, 1, 0]
        assert result["HasGarage"].tolist() == [0, 1, 1, 1]

    def test_log_transforms(self):
        df = pd.DataFrame(
            {
                "SalePrice": [100000, 200000, 300000],
                "GrLivArea": [1000, 2000, 3000],
            }
        )

        config = {"log_transforms": ["SalePrice", "GrLivArea"]}

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # Check log columns created
        assert "SalePrice_log" in result.columns
        assert "GrLivArea_log" in result.columns

        # Verify calculations (using log1p for safe zero handling)
        assert np.isclose(result["SalePrice_log"].iloc[0], np.log1p(100000))
        assert np.isclose(result["GrLivArea_log"].iloc[1], np.log1p(2000))

        # Original columns should remain
        assert "SalePrice" in result.columns

    def test_interaction_features(self):
        df = pd.DataFrame(
            {
                "OverallQual": [5, 7, 9],
                "GrLivArea": [1000, 1500, 2000],
            }
        )

        config = {
            "interactions": [{"columns": ["OverallQual", "GrLivArea"], "name": "Qual_x_Area"}]
        }

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # Check interaction column created
        assert "Qual_x_Area" in result.columns

        # Verify calculation
        assert result["Qual_x_Area"].iloc[0] == 5000  # 5 * 1000
        assert result["Qual_x_Area"].iloc[1] == 10500  # 7 * 1500

    def test_combined_features(self):
        df = pd.DataFrame(
            {
                "OverallQual": [5, 7, 9],
                "GrLivArea": [1000, 1500, 2000],
                "TotalBsmtSF": [0, 800, 1000],
                "SalePrice": [150000, 200000, 250000],
            }
        )

        config = {
            "polynomial_features": [{"column": "OverallQual", "degrees": [2]}],
            "binary_indicators": [
                {
                    "name": "HasBsmt",
                    "condition": {"column": "TotalBsmtSF", "operator": ">", "value": 0},
                }
            ],
            "log_transforms": ["SalePrice"],
            "interactions": [{"columns": ["OverallQual", "GrLivArea"], "name": "Qual_x_Area"}],
        }

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # All new features should exist
        assert "OverallQual_squared" in result.columns
        assert "HasBsmt" in result.columns
        assert "SalePrice_log" in result.columns
        assert "Qual_x_Area" in result.columns

        # Original columns preserved
        assert len(result) == 3  # Same number of rows
        assert "OverallQual" in result.columns

    def test_empty_config(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        transformer = FeatureEngineeringTransformer({})
        result = transformer.fit_transform(df)

        # Should return unchanged dataframe
        pd.testing.assert_frame_equal(result, df)

    def test_missing_column_handling(self):
        df = pd.DataFrame({"A": [1, 2, 3]})

        config = {
            "polynomial_features": [
                {"column": "NonExistent", "degrees": [2]}  # Column doesn't exist
            ]
        }

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # Should skip missing column gracefully
        assert "NonExistent_squared" not in result.columns
        assert "A" in result.columns

    def test_log_transform_with_zeros(self):
        df = pd.DataFrame({"Value": [0, 10, 100]})

        config = {"log_transforms": ["Value"]}

        transformer = FeatureEngineeringTransformer(config)
        result = transformer.fit_transform(df)

        # log1p(0) = 0, not -inf
        assert result["Value_log"].iloc[0] == 0
        assert np.isclose(result["Value_log"].iloc[1], np.log1p(10))
