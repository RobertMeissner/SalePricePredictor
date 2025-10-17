import mlflow

from config import MLFLOW_TRACKING_URI


def setup_mlflow():
    mlflow.set_tracking_uri(f"file:{MLFLOW_TRACKING_URI}")
