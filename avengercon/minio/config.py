"""
MinIO client configuration
"""

from pydantic import Field
from pydantic import SecretStr
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from sys import exit

from avengercon.logger import logger


class MinioConfig(BaseSettings):
    """
    Pydantic parser for MinIO configuration environment variables.
    """

    endpoint: str = Field(alias="MINIO_ENDPOINT")
    access_key: str = Field(alias="MINIO_ROOT_USER")
    secret_key: SecretStr = Field(alias="MINIO_ROOT_PASSWORD")
    secure: bool = Field(alias="MINIO_USE_SSL")

    @property
    def protocol(self) -> str:
        """
        The protocol to use when connecting to MinIO
        Returns: http or https

        """
        if self.secure:
            return "https"
        return "http"


try:
    # Note: As of 17FEB24 there's a conflict between Pydantic's dataclass behavior and
    # mypy/pyright. Ignore for now:
    # https://github.com/pydantic/pydantic-settings/issues/201#issuecomment-1950266275
    # TODO: Remove the type ignore once a fix is in place
    minio_config = MinioConfig()  # type: ignore
    logger.debug("Successfully found MinIO configuration")
except ValidationError as e:
    logger.error(f"MinIO configuration error: {e}")
    exit(1)
