from omegaconf import DictConfig
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        return X.drop(columns=self.columns, errors="ignore")


class CategoricalMapTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mappings):
        self.mappings = mappings

    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X = X.copy()
        for col, config in self.mappings.items():
            if col in X.columns:
                X[col] = X[col].fillna(config.get("null_value", 0))
                X[col] = X[col].map(config["mapping"]).fillna(config.get("null_value", 0))
        return X


class ImputationTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, numerical_strategy, categorical_strategy, exclude_columns):
        self.numerical_strategy = numerical_strategy
        self.categorical_strategy = categorical_strategy
        self.exclude_columns = exclude_columns or []

    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]

        # Identify column types
        self.numerical_cols_ = [
            col
            for col in X.select_dtypes(include=["number"]).columns
            if col not in self.exclude_columns
        ]
        self.categorical_cols_ = [
            col
            for col in X.select_dtypes(include=["object"]).columns
            if col not in self.exclude_columns
        ]

        # Map 'mode' to sklearn's 'most_frequent'
        cat_strategy = (
            "most_frequent" if self.categorical_strategy == "mode" else self.categorical_strategy
        )

        # Fit imputers
        if self.numerical_cols_:
            self.num_imputer_ = SimpleImputer(strategy=self.numerical_strategy)
            self.num_imputer_.fit(X[self.numerical_cols_])
        else:
            self.num_imputer_ = None

        if self.categorical_cols_:
            self.cat_imputer_ = SimpleImputer(strategy=cat_strategy)
            self.cat_imputer_.fit(X[self.categorical_cols_])
        else:
            self.cat_imputer_ = None

        return self

    def transform(self, X):
        X = X.copy()

        if self.num_imputer_ is not None:
            X[self.numerical_cols_] = self.num_imputer_.transform(X[self.numerical_cols_])

        if self.cat_imputer_ is not None:
            X[self.categorical_cols_] = self.cat_imputer_.transform(X[self.categorical_cols_])

        return X


class ScalingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, strategy, exclude_columns):
        self.strategy = strategy
        self.exclude_columns = exclude_columns or []

    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]

        # Only scale numerical columns
        self.numerical_cols_ = [
            col
            for col in X.select_dtypes(include=["number"]).columns
            if col not in self.exclude_columns
        ]

        if self.numerical_cols_:
            self.scaler_ = StandardScaler()
            self.scaler_.fit(X[self.numerical_cols_])
        else:
            self.scaler_ = None

        return self

    def transform(self, X):
        if self.scaler_ is None:
            return X

        X = X.copy()
        X[self.numerical_cols_] = self.scaler_.transform(X[self.numerical_cols_])
        return X


def build_pipeline(config: DictConfig) -> Pipeline:
    """Build sklearn pipeline from config.

    Args:
        config: DictConfig with preprocessing configuration

    Returns:
        sklearn Pipeline
    """
    steps = []
    prep_cfg = config.preprocessing

    for step_config in prep_cfg.pipeline:
        step_name = step_config["step"]

        if step_name == "drop_columns":
            transformer = DropColumnsTransformer(columns=prep_cfg.drop_columns)
            steps.append(("drop_columns", transformer))

        elif step_name == "categorical_transforms":
            if prep_cfg.categorical_transforms:
                transformer = CategoricalMapTransformer(mappings=prep_cfg.categorical_transforms)
                steps.append(("categorical_transforms", transformer))

        elif step_name == "imputation":
            transformer = ImputationTransformer(
                numerical_strategy=prep_cfg.imputation.numerical_strategy,
                categorical_strategy=prep_cfg.imputation.categorical_strategy,
                exclude_columns=prep_cfg.imputation.get("exclude_columns", []),
            )
            steps.append(("imputation", transformer))

        elif step_name == "scaling":
            transformer = ScalingTransformer(
                strategy=prep_cfg.scaling.strategy,
                exclude_columns=prep_cfg.scaling.get("exclude_columns", []),
            )
            steps.append(("scaling", transformer))

    if not steps:
        raise ValueError("No valid preprocessing steps configured")

    return Pipeline(steps)


class SklearnPipelineBuilder:
    """Builder for sklearn pipelines from config."""

    def __init__(self, config: DictConfig):
        self.config = config

    def build(self) -> Pipeline:
        """Build the pipeline."""
        return build_pipeline(self.config)
