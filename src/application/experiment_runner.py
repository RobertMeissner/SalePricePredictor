"""
Experiment Runner

Refactored experiment logic from iterative_preprocessing.py into a reusable function
with dependency injection. This allows running experiments via CLI or programmatically.
"""

import warnings

import mlflow
from omegaconf import DictConfig
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.domain.ports.data_repository import DataRepository
from src.preprocessing.sklearn_pipeline_builder import build_pipeline
from src.utils.mlflow_setup import setup_mlflow

warnings.warn("experiment_runner.py is deprecated, use ExperimentManager", DeprecationWarning)


def run_experiment(cfg: DictConfig, data_repository: DataRepository) -> dict:
    """
    Execute a complete ML experiment based on Hydra configuration.

    This function orchestrates the full experiment workflow:
    1. Load data through repository
    2. Split into train/test sets
    3. Build and apply preprocessing pipeline
    4. Train model
    5. Evaluate and log to MLflow

    Args:
        cfg: Hydra DictConfig with experiment configuration
             Must contain: training.target_column, training.test_size,
                          training.random_state, model.regression_model, etc.
        data_repository: DataRepository adapter implementing the port interface

    Returns:
        dict: Dictionary containing evaluation metrics
              Keys: test_r2, test_mae, test_mse

    Example:
        >>> from config import CONFIG_DIR
        >>> from src.adapters.factory import create_data_repository
        >>> from src.config_parser import load_config
        >>>
        >>> cfg = load_config(CONFIG_DIR, "config")
        >>> repository = create_data_repository(cfg)
        >>> metrics = run_experiment(cfg, repository)
        >>> print(f"R² Score: {metrics['test_r2']:.4f}")
    """
    # Setup MLflow
    setup_mlflow()
    mlflow.set_experiment(cfg.name)

    # Load data through injected repository
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
        model = _build_model(cfg)
        mlflow.log_param("model", model.__class__.__name__)

        # Log model parameters
        for param_name, param_value in cfg.model.params.items():
            mlflow.log_param(f"model_{param_name}", param_value)

        model.fit(X_train_transformed, y_train)

        # Log model with signature
        input_example = X_train_transformed.iloc[:5]
        mlflow.sklearn.log_model(
            model,
            name="model",
            registered_model_name="HousePricing",
            input_example=input_example,
        )

        # Evaluate
        y_pred = model.predict(X_test_transformed)

        metrics = {
            "r2": r2_score(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred),
            "mse": mean_squared_error(y_test, y_pred),
        }

        # Log metrics to MLflow
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
            print(f"{metric_name}: {metric_value:.4f}")

        return metrics


def _build_model(cfg: DictConfig):
    """
    Build model based on config.

    Args:
        cfg: Hydra DictConfig with model.regression_model and model.params

    Returns:
        Instantiated sklearn model
    """
    match cfg.model.regression_model:
        case "linear":
            return LinearRegression(**cfg.model.params)
        case "ridge":
            return Ridge(**cfg.model.params)
        case "lasso":
            return Lasso(**cfg.model.params)
        case _:
            # Default fallback
            return LinearRegression(**cfg.model.params)
