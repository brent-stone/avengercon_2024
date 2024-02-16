"""
Global AutoAI configuration configured via environment variables values.
"""

from pydantic import SecretStr
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from sys import exit

from avengercon.logger import logger


class AvengerconConfig(BaseSettings):
    """
    Shared Pydantic parser for environment variables used throughout the backend.
    """

    DOMAIN: str
    SUBDOMAIN_API: str
    SECRET_KEY: SecretStr
    # Controls the number of retries and pauses between retries for upstream services
    # like redis or MinIO
    DEPENDENCY_LOGIN_WAIT_SEC: int = 5
    DEPENDENCY_LOGIN_RETRY_COUNT: int = 5


try:
    avengercon_config = AvengerconConfig()  # type: ignore
    logger.debug("Successfully found API configurations")
except ValidationError as e:
    logger.error(f"Invalid configuration: {e}")
    exit(1)
