from omegaconf import DictConfig
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


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
            # Skip for now - not implemented
            pass

        elif step_name == "scaling":
            # Skip for now - not implemented
            pass

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
