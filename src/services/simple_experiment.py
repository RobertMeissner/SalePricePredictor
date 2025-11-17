from loguru import logger
import mlflow
from omegaconf import DictConfig
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.adapters.factory import create_data_repository
from src.config.hydra_loader import load_config
from src.config.paths import CONFIG_DIR, MLFLOW_TRACKING_URI
from src.domain.models.experiment_models import ExperimentSetup
from src.preprocessing.sklearn_pipeline_builder import build_pipeline
from src.utils.build_model import _build_model


# Highlight to show
class SimpleExperiment:
    """

    Implements Experiment handler
    """

    def __init__(self, experiment: ExperimentSetup) -> None:
        self._config = load_config(CONFIG_DIR, experiment.config_name)
        self._data_repository = create_data_repository(self._config)

    @property
    def config(self) -> DictConfig:
        return self._config

    def run(self) -> dict:
        logger.debug(f"Running experiment: {self._config.run_name}")
        logger.debug(f"  Experiment group: {self._config.name}")
        logger.debug(f"  Model: {self._config.model.regression_model}")

        results = self._run_experiment()
        return results

    def _setup_mlflow(self):
        mlflow.set_tracking_uri(f"file:{MLFLOW_TRACKING_URI}")
        mlflow.set_experiment(self.config.name)

    def _run_experiment(self) -> dict:
        df = self._data_repository.load_raw()

        # Apply outlier removal BEFORE train_test_split
        # This ensures X and y stay aligned
        if (
            hasattr(self.config.preprocessing, "remove_outliers")
            and self.config.preprocessing.remove_outliers
        ):
            for column, conditions in self.config.preprocessing.remove_outliers.items():
                if column not in df.columns:
                    continue

                # Apply greaterthan condition
                if "greaterthan" in conditions:
                    df = df[df[column] <= conditions["greaterthan"]]

                # Apply lessthan condition
                if "lessthan" in conditions:
                    df = df[df[column] >= conditions["lessthan"]]

            logger.debug(f"After outlier removal: {len(df)} rows remaining")

        X = df.drop(columns=[self.config.training.target_column])
        y = df[self.config.training.target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.config.training.test_size,
            random_state=self.config.training.random_state,
        )

        pipeline = build_pipeline(self.config)

        # Fit pipeline and transform data
        X_train_transformed = pipeline.fit_transform(X_train)
        X_test_transformed = pipeline.transform(X_test)

        # Select only numeric columns for simple experiment
        numeric_cols = X_train_transformed.select_dtypes(include=["number"]).columns
        X_train_transformed = X_train_transformed[numeric_cols].fillna(0)
        X_test_transformed = X_test_transformed[numeric_cols].fillna(0)

        # Train model with params from config
        model = _build_model(self.config)
        model.fit(X_train_transformed, y_train)

        # Evaluate
        y_pred = model.predict(X_test_transformed)

        metrics = {
            "r2": r2_score(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred),
            "mse": mean_squared_error(y_test, y_pred),
        }

        self._setup_mlflow()

        with mlflow.start_run(run_name=self.config.run_name):
            # Log metrics to MLflow
            mlflow.log_param("test_size", self.config.training.test_size)
            mlflow.log_param("random_state", self.config.training.random_state)
            mlflow.log_param("n_features_after_transform", X_train_transformed.shape[1])
            mlflow.log_param("model", model.__class__.__name__)

            # Log model parameters
            for param_name, param_value in self.config.model.params.items():
                mlflow.log_param(f"model_{param_name}", param_value)
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                input_example=X_train_transformed.iloc[:5],
            )  # registered_model_name="HousePricing",
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
                print(f"{metric_name}: {metric_value:.4f}")

            return metrics
