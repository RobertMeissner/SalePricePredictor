from typing import Protocol

from omegaconf import DictConfig

from src.domain.models.experiment_models import ExperimentSetup, MetricsOutput


class Experiment(Protocol):
    """

    Experiment handler
    """

    def __init__(self, experiment: ExperimentSetup) -> None: ...
    @property
    def config(self) -> DictConfig: ...

    def run(self) -> dict: ...

    def metrics(self) -> MetricsOutput: ...
