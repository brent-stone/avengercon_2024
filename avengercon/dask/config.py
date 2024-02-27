"""
Dask client configuration
"""

from pydantic import Field
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from sys import exit

from avengercon.logger import logger


class DaskConfig(BaseSettings):
    """
    Pydantic parser for Dask configuration environment variables
    """

    scheduler_address: str = Field(alias="DASK_SCHEDULER_ADDRESS")


try:
    # Note: As of 17FEB24 there's a conflict between Pydantic's dataclass behavior and
    # mypy/pyright. Ignore for now:
    # https://github.com/pydantic/pydantic-settings/issues/201#issuecomment-1950266275
    # TODO: Remove the type ignore once a fix is in place
    dask_config = DaskConfig()  # type: ignore
    logger.debug("Successfully found Dask configuration")
except ValidationError as e:
    logger.error(f"Dask configuration error: {e}")
    exit(1)
