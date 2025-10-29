from loguru import logger
from omegaconf import DictConfig

from src.adapters.factory import create_data_repository
from src.config import CONFIG_DIR
from src.config_parser import load_config
from src.domain.models.experiment_models import ExperimentSetup, MetricsOutput
from src.experiments.runner import run_experiment


class SimpleExperiment:
    """

    Implements Experiment handler
    """

    def __init__(self, experiment: ExperimentSetup):
        self._config = load_config(CONFIG_DIR, experiment.config_name)

    @property
    def config(self) -> DictConfig:
        return self._config

    def run(self) -> dict:
        logger.debug(f"Running experiment: {self._config.run_name}")
        logger.debug(f"  Experiment group: {self._config.name}")
        logger.debug(f"  Model: {self._config.model.regression_model}")

        data_repository = create_data_repository(self._config)

        results = run_experiment(self._config, data_repository)
        return results

    def metrics(self) -> MetricsOutput: ...
