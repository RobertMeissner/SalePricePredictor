from loguru import logger
import numpy as np
from omegaconf import DictConfig, OmegaConf

from src.preprocessing.pipeline import PreprocessingPipeline

TRANSFORMER_REGISTRY = {}


def pipeline_from_config(cfg: DictConfig) -> PreprocessingPipeline:
    """
    Build a preprocessing pipeline from a Hydra/OmegaConf configuration.

    Args:
        cfg: OmegaConf DictConfig from Hydra
    """
    logger.debug(
        f"Building pipeline from Hydra config: '{cfg.preprocessing.get('name', 'custom')}'"
    )

    steps = []
    for step_cfg in cfg.preprocessing.pipeline:
        step_name = step_cfg.name
        transformer_name = step_cfg.transformer

        params = OmegaConf.to_container(step_cfg.params, resolve=True)

        # Handle special categorical transforms with mappings
        if "transforms" in params:
            transforms = params["transforms"]
            for cat_feature, cat_config in transforms.items():
                if "mapping" in cat_config:
                    mapping = cat_config["mapping"]

                    # If there's a null_value field, add it to mapping for None and np.nan
                    if "null_value" in cat_config:
                        null_val = cat_config["null_value"]
                        mapping[None] = null_val
                        mapping[np.nan] = null_val
                        # Remove null_value from config as it's not part of the transform spec
                        del cat_config["null_value"]

        # Instantiate transformer
        transformer_class = TRANSFORMER_REGISTRY[transformer_name]
        transformer = transformer_class(**params)

        steps.append((step_name, transformer))
        logger.debug(f"  Added step: {step_name} ({transformer})")

    pipeline = PreprocessingPipeline(steps)
    logger.debug(f"Pipeline created with {len(pipeline)} steps")

    return pipeline
