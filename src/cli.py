from dotenv import load_dotenv
import typer

from src.domain.models.experiment_models import ExperimentSetup, MetricsOutput
from src.domain.ports.experiment_manager_port import ExperimentManagerPort
from src.services.experiment_manager import ExperimentManager

app = typer.Typer()

load_dotenv()


@app.command("train")
def train(config: str = "default") -> None:
    """
    Train the model on a dataset.
    """
    typer.echo("Training started.", fg="green")
    typer.echo("Training done.", fg="green")


@app.command("feature")
def feature(config: str = "default") -> None:
    """
    Build features from interim dataset and store to processed
    """

    typer.echo()


@app.command("experiment")
def experiment(
    config_name: str = typer.Option("config", help="Config file name (without .yaml)"),
    run_name: str = typer.Option(None, help="Override run name"),
) -> None:
    """
    Run a complete ML experiment with Hydra configuration.

    Executes the full experiment workflow with dependency injection:
    - Loads data through configured repository adapter
    - Applies preprocessing pipeline from config
    - Trains model with configured parameters
    - Evaluates and logs metrics to MLflow

    Examples:
        uv run -m src.main experiment
        uv run -m src.main experiment --config-name config
        uv run -m src.main experiment --experiment-name my-experiment
        uv run -m src.main experiment --run-name ridge-test
    """
    manager: ExperimentManagerPort = ExperimentManager()

    manager.setup_experiment(ExperimentSetup(config_name=config_name, run_name=run_name))

    result = manager.run()

    # display last experiment
    # fixme: add return? How to better display metrics?
    (metrics_dict,) = result.values()
    metrics = MetricsOutput(**metrics_dict)

    # Display results
    typer.echo("\nMetrics:")
    typer.echo(f"  R² Score: {metrics.r2:.4f}")
    typer.echo(f"  MAE:      ${metrics.mae:.2f}")
    typer.echo(f"  MSE:      {metrics.mse:.2f}")


if __name__ == "__main__":
    app()
