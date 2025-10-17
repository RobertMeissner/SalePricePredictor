import copy
from importlib.metadata import metadata

from loguru import logger
import pandas as pd
from sklearn.pipeline import Pipeline

from src.preprocessing.base import BaseTransformer


class PreprocessingPipeline(Pipeline):
    """
    Pipeline for chaining multiple preprocessing transformers.
    Derived class to enable future enhancement without requiring changes to tool calls etc.

    Args:
        steps: List of (name, transformer) tuples defining the pipeline
    """

    def __init__(self, steps: list[tuple[str, BaseTransformer]]):
        super().__init__(steps)
        self.metadata_ = {}

    def fit(self, X: pd.DataFrame, y=None, **fit_params) -> "PreprocessingPipeline":
        logger.debug(f"Fitting pipeline with {len(self.steps)} steps...")
        super().fit(X, y, **fit_params)
        logger.debug("Pipeline fitting complete!")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        logger.debug(f"Transforming data through {len(self.steps)} steps...")
        result = super().transform(X)
        logger.debug("Pipeline transformation complete!")
        return result

    def fit_transform(self, X: pd.DataFrame, y=None, **fit_params) -> pd.DataFrame:
        logger.debug(f"Fitting and transforming with {len(self.steps)} steps...")
        self.fit(X, y, **fit_params)
        df_transformed = self.transform(X)
        return df_transformed

    @property
    def metadata(self) -> dict[str, dict]:
        if not hasattr(self, "_fitted"):
            return {}
        if not metadata:
            self.metadata_ = {
                name: step.get_metadata()
                for name, step in self.steps
                if hasattr(step, "get_metadata")
            }
        return copy.deepcopy(self.metadata_)
