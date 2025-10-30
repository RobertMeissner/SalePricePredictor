from pathlib import Path

from hydra import compose, initialize_config_dir
from omegaconf import DictConfig


# Highlight to show
def load_config(config_dir: Path, config_name: str = "config") -> DictConfig:
    """Load configuration using Hydra.

    Args:
        config_dir: Absolute path to config directory
        config_name: Name of config file (without .yaml extension)

    """
    with initialize_config_dir(config_dir=str(config_dir), version_base="1.3"):
        cfg = compose(config_name=config_name)
    return cfg
