import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import mutual_info_regression


class FeatureSelectionTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer for feature selection operations.

    Supports:
    - Correlation-based selection (correlation with target)
    - Variance threshold selection (remove low variance features)
    - Mutual information selection

    Config structure:
        {
            "method": "correlation",  # or "variance_threshold", "mutual_info"
            "params": {
                "threshold": 0.5  # for correlation: min correlation with target
                                  # for variance: min variance
                                  # for mutual_info: min MI score (normalized 0-1)
            },
            "target_column": "SalePrice",
            "exclude_columns": ["Id"]  # optional: columns to always keep
        }
    """

    def __init__(self, config: dict):
        """
        Initialize transformer with configuration.

        Args:
            config: Dictionary containing feature selection specifications
        """
        self.config = config
        self.method = config.get("method", "correlation")
        self.params = config.get("params", {})
        self.target_column = config.get("target_column")
        self.exclude_columns = config.get("exclude_columns", [])

    def fit(self, X, y=None):
        """
        Fit the transformer by selecting features.

        Args:
            X: Input dataframe
            y: Target (unused, target is in X)

        Returns:
            self
        """
        self.n_features_in_ = X.shape[1]

        if self.target_column is None or self.target_column not in X.columns:
            # If no target specified or target not found, keep all features
            self.selected_features_ = list(X.columns)
            return self

        feature_cols = [col for col in X.columns if col != self.target_column]
        target = X[self.target_column]

        if self.method == "correlation":
            selected = self._select_by_correlation(X[feature_cols], target)
        elif self.method == "variance_threshold":
            selected = self._select_by_variance(X[feature_cols])
        elif self.method == "mutual_info":
            selected = self._select_by_mutual_info(X[feature_cols], target)
        else:
            # Unknown method, keep all features
            selected = feature_cols

        # Always include target and excluded columns
        self.selected_features_ = list(set(selected + [self.target_column] + self.exclude_columns))

        # Only keep columns that actually exist in X
        self.selected_features_ = [col for col in self.selected_features_ if col in X.columns]

        return self

    def transform(self, X):
        """
        Transform by keeping only selected features.

        Args:
            X: Input dataframe

        Returns:
            Dataframe with only selected features
        """
        # Only select features that exist in X
        available_features = [col for col in self.selected_features_ if col in X.columns]
        return X[available_features].copy()

    def _select_by_correlation(self, X: pd.DataFrame, target: pd.Series) -> list:
        """
        Select features based on correlation with target.

        Args:
            X: Feature dataframe
            target: Target series

        Returns:
            List of selected feature names
        """
        threshold = self.params.get("threshold", 0.5)

        # Only correlate numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols:
            return []

        # Calculate correlations
        correlations = X[numeric_cols].corrwith(target).abs()

        # Select features above threshold
        selected = correlations[correlations >= threshold].index.tolist()

        # Add back non-numeric columns (we don't want to drop them automatically)
        non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
        selected.extend(non_numeric_cols)

        return selected

    def _select_by_variance(self, X: pd.DataFrame) -> list:
        """
        Select features based on variance threshold.

        Args:
            X: Feature dataframe

        Returns:
            List of selected feature names
        """
        threshold = self.params.get("threshold", 0.0)

        # Only check variance for numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols:
            return []

        # Calculate variances
        variances = X[numeric_cols].var()

        # Select features above threshold
        selected = variances[variances > threshold].index.tolist()

        # Add back non-numeric columns
        non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
        selected.extend(non_numeric_cols)

        return selected

    def _select_by_mutual_info(self, X: pd.DataFrame, target: pd.Series) -> list:
        """
        Select features based on mutual information with target.

        Args:
            X: Feature dataframe
            target: Target series

        Returns:
            List of selected feature names
        """
        threshold = self.params.get("threshold", 0.5)
        n_neighbors = self.params.get("n_neighbors", 3)

        # Only use numeric columns for mutual info
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols or len(X) < n_neighbors:
            return list(X.columns)

        # Calculate mutual information
        mi_scores = mutual_info_regression(
            X[numeric_cols], target, n_neighbors=min(n_neighbors, len(X) - 1), random_state=42
        )

        # Normalize scores to 0-1 range
        if mi_scores.max() > 0:
            mi_scores = mi_scores / mi_scores.max()

        # Select features above threshold
        selected = [numeric_cols[i] for i, score in enumerate(mi_scores) if score >= threshold]

        # Add back non-numeric columns
        non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
        selected.extend(non_numeric_cols)

        return selected
