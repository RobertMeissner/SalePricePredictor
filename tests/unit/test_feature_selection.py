import numpy as np
import pandas as pd

from src.preprocessing.feature_selection import FeatureSelectionTransformer


class TestFeatureSelectionTransformer:
    def test_correlation_based_selection(self):
        np.random.seed(42)
        target = np.array([100, 200, 300, 400, 500])

        df = pd.DataFrame(
            {
                "HighCorr": target * 2 + np.random.normal(0, 10, 5),  # High correlation
                "MedCorr": target * 0.5 + np.random.normal(0, 50, 5),  # Medium correlation
                "LowCorr": np.random.normal(100, 50, 5),  # Low/no correlation
                "Target": target,
            }
        )

        config = {
            "method": "correlation",
            "params": {"threshold": 0.7},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Should keep HighCorr (high correlation), drop LowCorr
        assert "HighCorr" in result.columns
        assert "Target" in result.columns
        # LowCorr should be dropped
        assert "LowCorr" not in result.columns

    def test_variance_threshold_selection(self):
        df = pd.DataFrame(
            {
                "HighVar": [1, 100, 200, 300, 400],  # High variance
                "LowVar": [5, 5, 5, 5, 6],  # Low variance
                "NoVar": [10, 10, 10, 10, 10],  # No variance
                "Target": [100, 200, 300, 400, 500],
            }
        )

        config = {
            "method": "variance_threshold",
            "params": {"threshold": 100},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Should keep HighVar and Target
        assert "HighVar" in result.columns
        assert "Target" in result.columns
        # Should drop LowVar and NoVar
        assert "LowVar" not in result.columns
        assert "NoVar" not in result.columns

    def test_mutual_info_selection(self):
        np.random.seed(42)
        target = np.array([100, 200, 300, 400, 500])

        df = pd.DataFrame(
            {
                "Relevant": target * 2,  # Perfectly related
                "SemiRelevant": target + np.random.normal(0, 20, 5),
                "Irrelevant": np.random.normal(100, 50, 5),
                "Target": target,
            }
        )

        config = {
            "method": "mutual_info",
            "params": {"threshold": 0.5, "n_neighbors": 3},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Should keep relevant features
        assert "Relevant" in result.columns
        assert "Target" in result.columns

    def test_target_column_always_preserved(self):
        df = pd.DataFrame(
            {
                "A": [1, 2, 3, 4, 5],
                "B": [5, 4, 3, 2, 1],
                "Target": [10, 20, 30, 40, 50],
            }
        )

        config = {
            "method": "variance_threshold",
            "params": {"threshold": 100},  # High threshold
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Target should always be preserved
        assert "Target" in result.columns

    def test_fit_transform_stores_selected_features(self):
        df = pd.DataFrame(
            {
                "A": [1, 100, 200, 300, 400],
                "B": [5, 5, 5, 5, 5],  # Low variance
                "Target": [100, 200, 300, 400, 500],
            }
        )

        config = {
            "method": "variance_threshold",
            "params": {"threshold": 10},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        transformer.fit(df)

        # Should have stored selected features
        assert hasattr(transformer, "selected_features_")
        assert "A" in transformer.selected_features_
        assert "Target" in transformer.selected_features_
        assert "B" not in transformer.selected_features_

    def test_transform_uses_fitted_features(self):
        df_train = pd.DataFrame(
            {
                "A": [1, 100, 200, 300, 400],
                "B": [5, 5, 5, 5, 5],  # Low variance
                "Target": [100, 200, 300, 400, 500],
            }
        )

        df_test = pd.DataFrame(
            {
                "A": [50, 150, 250],
                "B": [100, 200, 300],  # High variance in test, but was low in train
                "Target": [150, 250, 350],
            }
        )

        config = {
            "method": "variance_threshold",
            "params": {"threshold": 10},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        transformer.fit(df_train)
        result = transformer.transform(df_test)

        # Should only keep features selected during training
        assert "A" in result.columns
        assert "Target" in result.columns
        assert "B" not in result.columns  # Was dropped during fit

    def test_exclude_columns_preserved(self):
        df = pd.DataFrame(
            {
                "Id": [1, 2, 3, 4, 5],
                "LowVar": [5, 5, 5, 5, 6],
                "Target": [100, 200, 300, 400, 500],
            }
        )

        config = {
            "method": "variance_threshold",
            "params": {"threshold": 10},
            "target_column": "Target",
            "exclude_columns": ["Id"],
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Id should be preserved even though it might fail selection criteria
        assert "Id" in result.columns
        assert "Target" in result.columns
        assert "LowVar" not in result.columns

    def test_empty_dataframe_handling(self):
        df = pd.DataFrame({"A": [1], "Target": [100]})

        config = {
            "method": "correlation",
            "params": {"threshold": 0.5},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Should handle gracefully
        assert "Target" in result.columns

    def test_all_features_below_threshold(self):
        df = pd.DataFrame(
            {
                "A": [5, 5, 5, 5, 5],  # No variance
                "B": [10, 10, 10, 10, 10],  # No variance
                "Target": [100, 200, 300, 400, 500],
            }
        )

        config = {
            "method": "variance_threshold",
            "params": {"threshold": 1},
            "target_column": "Target",
        }

        transformer = FeatureSelectionTransformer(config)
        result = transformer.fit_transform(df)

        # Should at least keep target
        assert "Target" in result.columns
        # Other columns should be dropped
        assert "A" not in result.columns
        assert "B" not in result.columns
