from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
logger.debug(f"PROJ_ROOT path is: {PROJECT_ROOT}")

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJECT_ROOT / "models"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

MLFLOW_TRACKING_URI = PROJECT_ROOT / "mlruns"

CONFIG_DIR = PROJECT_ROOT / "config"

# Files

RAW_DATA = "raw.csv"
INTERIM_DATA_FILENAME = "interim.parquet"
INTERIM_METADATA_FILENAME = "interim_metadata.json"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    try:
        logger.remove(0)
    except ValueError:
        pass
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
