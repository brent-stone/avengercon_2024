"""
Redis client configuration metadata
"""

from urllib.parse import quote_plus

from pydantic import Field
from pydantic import SecretStr
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from sys import exit

from avengercon.logger import logger


class RedisConfig(BaseSettings):
    """
    Pydantic parser for Redis configuration environment variables.
    """

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    redis_password: SecretStr = Field(alias="REDIS_PASSWORD")

    @property
    def redis_dsn(self) -> str:
        """
        Dynamically construct a Redis connection string from the available configs
        Returns: A URL escaped connection string

        """
        return (
            f"redis://:{quote_plus(self.redis_password.get_secret_value())}@"
            f"{self.redis_host}:{self.redis_port}/0"
        )

    @property
    def redis_dsn_printable(self) -> str:
        """
        Dynamically construct a Redis connection string from the available configs but
        retain obfuscation of the password. This should only be used for logging
        Returns: A URL escaped connection string

        """
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/0"


try:
    redis_config = RedisConfig()  # type: ignore
    logger.debug("Successfully found Redis configuration")
except ValidationError as e:
    logger.error(f"Redis configuration error: {e}")
    exit(1)
