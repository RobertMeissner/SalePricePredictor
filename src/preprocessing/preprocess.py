from loguru import logger
from omegaconf import DictConfig
import pandas as pd

from src.domain.ports.data_repository import DataRepository
from src.preprocessing.sklearn_pipeline_builder import build_pipeline


def run_preprocessing(
    config: DictConfig, data_repository: DataRepository, save: bool = True
) -> pd.DataFrame:
    """
    Run the complete preprocessing pipeline using dependency injection.

    Args:
        config: Hydra configuration (DictConfig)
        data_repository: Data repository adapter implementing DataRepository port
        save: Whether to save the preprocessed data and metadata (default: True)

    Returns:
        pd.DataFrame: Preprocessed dataframe

    Example:
        >>> from src.adapters.factory import create_data_repository
        >>> from src.config_parser import load_config
        >>> from config import CONFIG_DIR
        >>>
        >>> config = load_config(CONFIG_DIR, "config")
        >>> repository = create_data_repository(config)
        >>> df = run_preprocessing(config, repository, save=True)
    """
    # Load data through injected repository
    df = data_repository.load_raw()
    logger.debug(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # Build pipeline from Hydra config
    pipeline = build_pipeline(config)
    logger.debug(f"Using pipeline config from: '{config}'")

    # Transform data
    df_preprocessed = pipeline.fit_transform(df)

    # Save through repository if requested
    if save:
        data_repository.save_interim(df_preprocessed, pipeline.metadata)
        logger.success(f"Preprocessing complete! Output shape: {df_preprocessed.shape}")

    return df_preprocessed
