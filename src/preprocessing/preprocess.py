from loguru import logger
from omegaconf import DictConfig
import pandas as pd

from src.adapters.command import write_interim, write_interim_metadata
from src.adapters.load import raw
from src.preprocessing.sklearn_pipeline_builder import pipeline_from_config


def run_preprocessing(config: DictConfig, save: bool = True) -> pd.DataFrame:
    """
    Run the complete preprocessing pipeline using the new pipeline architecture.

    Args:
        save: Whether to save the preprocessed data and metadata
        config: Hydra configuration (DictConfig)

    Returns:
        Tuple of (preprocessed_df, metadata_dict)

    Example:
        # Use pipeline
        df, metadata = run_preprocessing("default")


    """
    df = raw()
    logger.debug(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # Build pipeline from Hydra config
    pipeline = pipeline_from_config(config)
    logger.debug(f"Using pipeline config: '{config}'")

    df_preprocessed = pipeline.fit_transform(df)
    if save:
        write_interim(df_preprocessed)
        write_interim_metadata(pipeline.metadata)
        logger.success(f"Preprocessing complete! Output shape: {df_preprocessed.shape}")

    return df_preprocessed
