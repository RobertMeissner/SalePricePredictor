from typing import Protocol

from src.domain.models.experiment_models import ExperimentSetup


class ExperimentManagerPort(Protocol):
    """

    Experiment Manager. Handles a single experiment
    """

    def __init__(self) -> None: ...

    def run(self) -> dict[str, dict]: ...

    def setup_experiment(self, experiment: ExperimentSetup) -> None: ...
