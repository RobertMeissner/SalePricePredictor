from dotenv import load_dotenv
import hydra
from hydra import compose, initialize
from loguru import logger
import typer

from config import CONFIG_DIR
from src.preprocessing.preprocess import run_preprocessing

app = typer.Typer()

load_dotenv()


@app.command("preprocess")
def preprocess(config: str = "default") -> None:
    """
    Run the preprocessing pipeline to transform raw data into intermediate dataset.

    params: config: name of the configuration file.
    """
    with initialize(config_path=CONFIG_DIR, version_base=None):
        config = compose(config_name=f"preprocessing/{config}")
        df_preprocessed = run_preprocessing(config=config)
        logger.debug(f"Output shape: {df_preprocessed.shape}")
    typer.echo("Preprocessing done!", fg="green")


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
@hydra.main(version_base="1.3")
def experiment(name: str = "experiment") -> None:
    # TODO: Repository pattern, depends for data
    #   wrap MLFlow stuff (?)
    #   execute pipeline non-blocking?
    # TODO: Add more data to experiment yaml, cover more data
    pass


if __name__ == "__main__":
    app()
