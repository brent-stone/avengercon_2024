"""
Prefect client configuration
"""

from pydantic import Field
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from avengercon.logger import logger
from sys import exit


class PrefectConfig(BaseSettings):
    """
    Pydantic parser for Prefect client configuration environment variables.
    https://docs.prefect.io/latest/api-ref/prefect/settings/
    """

    # bespoke configurations unrelated to the Prefect Python SDK official configurations
    prefect_flows_bucket: str = Field(alias="PREFECT_MINIO_FLOWS_BUCKET_NAME")
    prefect_artifacts_bucket: str = Field(alias="PREFECT_MINIO_ARTIFACTS_BUCKET_NAME")


try:
    # Note: As of 17FEB24 there's a conflict between Pydantic's dataclass behavior and
    # mypy/pyright. Ignore for now:
    # https://github.com/pydantic/pydantic-settings/issues/201#issuecomment-1950266275
    # TODO: Remove the type ignore once a fix is in place
    prefect_config = PrefectConfig()  # type: ignore
    logger.debug("Successfully found Prefect client configuration")
except ValidationError as e:
    logger.error(f"Prefect configuration error: {e}")
    exit(1)
