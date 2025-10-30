"""
Unit tests for experiment domain models.
"""

from src.domain.models.experiment_models import ExperimentSetup, MetricsOutput


class TestExperimentSetup:
    """Test ExperimentSetup model."""

    def test_create_experiment_setup_with_required_fields(self):
        """Test creating ExperimentSetup with required fields."""
        setup = ExperimentSetup(config_name="config", run_name="test-run")

        assert setup.config_name == "config"
        assert setup.run_name == "test-run"

    def test_create_experiment_setup_with_none_run_name(self):
        """Test creating ExperimentSetup with None run_name."""
        setup = ExperimentSetup(config_name="config", run_name=None)

        assert setup.config_name == "config"
        assert setup.run_name is None


class TestMetricsOutput:
    """Test MetricsOutput model."""

    def test_create_metrics_output(self):
        """Test creating MetricsOutput with all metrics."""
        metrics = MetricsOutput(r2=0.85, mae=5000.0, mse=50000000.0)

        assert metrics.r2 == 0.85
        assert metrics.mae == 5000.0
        assert metrics.mse == 50000000.0

    def test_metrics_output_with_different_values(self):
        """Test MetricsOutput with different metric values."""
        metrics = MetricsOutput(r2=0.92, mae=3500.5, mse=25000000.25)

        assert metrics.r2 == 0.92
        assert metrics.mae == 3500.5
        assert metrics.mse == 25000000.25
