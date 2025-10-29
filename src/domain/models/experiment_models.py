from dataclasses import dataclass
from typing import Literal

from omegaconf import DictConfig
import pandas as pd


@dataclass(frozen=True)
class MetricsInput:
    x_test: pd.DataFrame
    y_test: pd.DataFrame


@dataclass(frozen=True)
class MetricsOutput:
    r2: float
    mae: float
    mse: float


@dataclass(frozen=True)
class Experiment:
    config: DictConfig
    model_type: Literal["linear", "ridge", "lasso"]


@dataclass(frozen=True)
class ExperimentSetup:
    config_name: str
    run_name: str
