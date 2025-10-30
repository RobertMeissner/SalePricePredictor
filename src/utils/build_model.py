from omegaconf import DictConfig
from sklearn.linear_model import Lasso, LinearRegression, Ridge


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
            return LinearRegression(**cfg.model.params)
