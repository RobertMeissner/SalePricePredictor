import mlflow
import sklearn

from utils.mlflow_setup import setup_mlflow


def export(model: sklearn.linear_model.LinearRegression) -> None:
    setup_mlflow()
    mlflow.sklearn.log_model(
        model, name="hhouse_pricing_model", registered_model_name="HousePricing"
    )
