from hydra import compose, initialize
from loguru import logger
import typer

from config import CONFIG_DIR
from src.preprocessing.preprocess import run_preprocessing

app = typer.Typer()


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
    typer.secho("Preprocessing done!", fg="green")


if __name__ == "__main__":
    app()
