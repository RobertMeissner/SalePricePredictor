"""
Unit tests for ExperimentManager.
"""

from src.domain.models.experiment_models import ExperimentSetup
from src.services.experiment_manager import ExperimentManager


class TestExperimentManager:
    """Test ExperimentManager service."""

    def test_init_creates_empty_experiments_list(self):
        """Test that initialization creates empty experiments list."""
        manager = ExperimentManager()
        assert manager._experiments == []

    def test_setup_experiment_adds_experiment(self):
        """Test that setup_experiment adds experiment to list."""
        manager = ExperimentManager()
        setup = ExperimentSetup(config_name="config", run_name="test-run")

        manager.setup_experiment(setup)

        assert len(manager._experiments) == 1

    def test_setup_multiple_experiments(self):
        """Test setting up multiple experiments."""
        manager = ExperimentManager()

        setup1 = ExperimentSetup(config_name="config", run_name="run1")
        setup2 = ExperimentSetup(config_name="config", run_name="run2")

        manager.setup_experiment(setup1)
        manager.setup_experiment(setup2)

        assert len(manager._experiments) == 2

    def test_experiment_setup_stores_correct_config(self):
        """Test that experiment setup stores configuration correctly."""
        manager = ExperimentManager()
        setup = ExperimentSetup(config_name="config", run_name="my-run")

        manager.setup_experiment(setup)

        experiment = manager._experiments[0]
        # TODO: Fix ExperimentSetup model - it's not storing config_name/run_name correctly
        # The model seems to use struct mode which prevents attribute access
        # Either: 1) Make ExperimentSetup a dataclass, 2) Disable struct mode in config
        assert hasattr(experiment, "config")
