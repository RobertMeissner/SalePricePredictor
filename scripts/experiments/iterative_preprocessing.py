from dataclasses import dataclass

import mlflow
import pandas as pd
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.adapters.factory import create_data_repository
from src.config.hydra_loader import load_config
from src.config.paths import CONFIG_DIR
from src.preprocessing.sklearn_pipeline_builder import build_pipeline
from src.utils.mlflow_setup import setup_mlflow


@dataclass(frozen=True)
class MetricsInput:
    x_test: pd.DataFrame
    y_test: pd.DataFrame
    mlflow: mlflow
    model: LinearRegression


def metrics(_metrics: MetricsInput) -> None:
    y_pred = _metrics.model.predict(_metrics.x_test)
    test_r2 = r2_score(_metrics.y_test, y_pred)
    test_mae = mean_absolute_error(_metrics.y_test, y_pred)
    test_mse = mean_squared_error(_metrics.y_test, y_pred)
    _metrics.mlflow.log_metric("test_r2", test_r2)
    _metrics.mlflow.log_metric("test_mae", test_mae)
    _metrics.mlflow.log_metric("test_mse", test_mse)
    print(f"Test R2: {test_r2}")
    print(f"Test MAE: {test_mae}")
    print(f"Test MSE: {test_mse}")


def main():
    # Setup
    setup_mlflow()
    mlflow.set_experiment("house-pricing")

    # Load config
    config_dir = CONFIG_DIR
    cfg = load_config(config_dir, "config")

    # Create data repository and load data (dependency injection)
    data_repository = create_data_repository(cfg)
    df = data_repository.load_raw()

    # Split data
    X = df.drop(columns=[cfg.training.target_column])
    y = df[cfg.training.target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=cfg.training.test_size, random_state=cfg.training.random_state
    )

    # Build preprocessing pipeline from config
    pipeline = build_pipeline(cfg)

    with mlflow.start_run(run_name=cfg.run_name):
        # Log config params
        mlflow.log_param("test_size", cfg.training.test_size)
        mlflow.log_param("random_state", cfg.training.random_state)

        # Fit pipeline and transform data
        X_train_transformed = pipeline.fit_transform(X_train)
        X_test_transformed = pipeline.transform(X_test)

        # Select only numeric columns for simple experiment
        numeric_cols = X_train_transformed.select_dtypes(include=["number"]).columns
        X_train_transformed = X_train_transformed[numeric_cols].fillna(0)
        X_test_transformed = X_test_transformed[numeric_cols].fillna(0)

        mlflow.log_param("n_features_after_transform", X_train_transformed.shape[1])

        # Train model with params from config
        match cfg.model.regression_model:
            case "linear":
                model = LinearRegression(**cfg.model.params)
            case "ridge":
                model = Ridge(**cfg.model.params)
            case "lasso":
                model = Lasso(**cfg.model.params)
            case _:
                model = LinearRegression(**cfg.model.params)

        mlflow.log_param("model", model.__class__.__name__)
        model.fit(X_train_transformed, y_train)

        # Log model with signature
        mlflow.sklearn.log_model(
            model,
            name="config_driven_model",
            registered_model_name="HousePricing",
            input_example=X_train_transformed.iloc[:5],
        )

        # Evaluate
        metrics(MetricsInput(x_test=X_test_transformed, model=model, y_test=y_test, mlflow=mlflow))


if __name__ == "__main__":
    main()
