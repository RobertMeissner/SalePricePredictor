from omegaconf import DictConfig

from src.adapters.filesystem_repository import FileSystemDataRepository
from src.domain.ports.data_repository import DataRepository


def create_data_repository(config: DictConfig) -> DataRepository:
    """
    Factory function to create appropriate data repository based on config.

    Args:
        config: Hydra DictConfig containing repository configuration
                Expected: config.data.repository_type = "filesystem" | "postgresql" | "s3" | "api"

    Returns:
        DataRepository implementation (e.g., FileSystemDataRepository)

    Raises:
        ValueError: If repository_type is unknown or unsupported
    """
    repo_type = "filesystem"

    if hasattr(config, "data") and hasattr(config.data, "repository_type"):
        repo_type = config.data.repository_type

    match repo_type:
        case "filesystem":
            return FileSystemDataRepository(config)
        case _:
            raise ValueError(
                f"Unknown repository type: '{repo_type}'. "
                f"Supported types: filesystem (postgresql, s3, api coming soon)"
            )
