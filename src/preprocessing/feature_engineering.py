import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineeringTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer for feature engineering operations.

    Supports:
    - Polynomial features (x^2, x^3, etc.)
    - Binary indicators (e.g., HasBsmt based on TotalBsmtSF > 0)
    - Log transformations
    - Interaction features (product of two columns)
    """

    def __init__(self, config: dict):
        """
        Initialize transformer with configuration.

        Args:
            config: Dictionary containing feature engineering specifications
        """
        self.config = config

    def fit(self, X: pd.DataFrame, y=None):
        """
        Fit the transformer (no-op for feature engineering).

        Args:
            X: Input dataframe
            y: Target (unused)

        Returns:
            self
        """
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering transformations.

        Returns:
            Transformed dataframe with engineered features
        """
        X = X.copy(deep=True)

        if "polynomial_features" in self.config:
            X = self._add_polynomial_features(X, self.config["polynomial_features"])

        if "binary_indicators" in self.config:
            X = self._add_binary_indicators(X, self.config["binary_indicators"])

        if "log_transforms" in self.config:
            X = self._add_log_transforms(X, self.config["log_transforms"])

        if "interactions" in self.config:
            X = self._add_interactions(X, self.config["interactions"])

        return X

    def _add_polynomial_features(self, X: pd.DataFrame, configs: list) -> pd.DataFrame:
        """
        Add polynomial features (x^2, x^3, etc.).

        Args:
            configs: List of polynomial feature configs

        Returns:
            Dataframe with polynomial features added
        """
        for config in configs:
            column = config["column"]
            degrees = config["degrees"]

            if column in X.columns:
                for degree in degrees:
                    if degree == 2:
                        new_col_name = f"{column}_squared"
                    elif degree == 3:
                        new_col_name = f"{column}_cubed"
                    else:
                        new_col_name = f"{column}_pow{degree}"

                    X[new_col_name] = X[column] ** degree

        return X

    def _add_binary_indicators(self, X: pd.DataFrame, configs: list) -> pd.DataFrame:
        """
        Add binary indicator features based on conditions.

        Args:
            configs: List of binary indicator configs

        Returns:
            Dataframe with binary indicators added
        """
        for config in configs:
            name = config["name"]
            condition = config["condition"]
            column = condition["column"]
            operator = condition["operator"]
            value = condition["value"]

            if column in X.columns:
                if operator == ">":
                    X[name] = (X[column] > value).astype(int)
                elif operator == ">=":
                    X[name] = (X[column] >= value).astype(int)
                elif operator == "<":
                    X[name] = (X[column] < value).astype(int)
                elif operator == "<=":
                    X[name] = (X[column] <= value).astype(int)
                elif operator == "==":
                    X[name] = (X[column] == value).astype(int)
                elif operator == "!=":
                    X[name] = (X[column] != value).astype(int)

        return X

    def _add_log_transforms(self, X: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Add log-transformed versions of columns.

        Uses log1p (log(1+x)) to handle zeros safely.

        Args:
            columns: List of column names to log-transform

        Returns:
            Dataframe with log-transformed features added
        """
        for column in columns:
            if column in X.columns:
                # Use log1p to safely handle zeros
                X[f"{column}_log"] = np.log1p(X[column])

        return X

    def _add_interactions(self, X: pd.DataFrame, configs: list) -> pd.DataFrame:
        """
        Add interaction features (product of two or more columns).

        Args:
            X: Input dataframe
            configs: List of interaction configs

        Returns:
            Dataframe with interaction features added
        """
        for config in configs:
            columns = config["columns"]
            name = config["name"]

            # Check all columns exist
            if not all(col in X.columns for col in columns):
                continue

            # Create interaction as product of columns
            X[name] = X[columns[0]]
            for col in columns[1:]:
                X[name] = X[name] * X[col]

        return X
