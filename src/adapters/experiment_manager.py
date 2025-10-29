from src.adapters.simple_experiment import SimpleExperiment
from src.domain.models.experiment_models import ExperimentSetup
from src.domain.ports.experiment import Experiment


class ExperimentManager:
    """
    Implements ExperimentManagerPort
    """

    _experiments: list[Experiment]

    def __init__(self) -> None:
        self._experiments = []

    def run(self) -> dict[str, dict]:
        result = {}
        for experiment in self._experiments:
            result.update({experiment.config.run_name: experiment.run()})
        return result

    def setup_experiment(self, experiment: ExperimentSetup) -> None:
        self._experiments.append(SimpleExperiment(experiment))
