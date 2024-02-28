"""
Prefect storage management
"""

from typing import List, Dict, Any

from avengercon.minio import create_buckets
from avengercon.prefect.config import prefect_config
from avengercon.minio.config import minio_config
from avengercon.minio.schemas import BucketCreationResult
from avengercon.logger import logger
from prefect.filesystems import RemoteFileSystem
from prefect.exceptions import PrefectException

_default_buckets: List[str] = []
try:
    _default_buckets.append(prefect_config.prefect_flows_bucket)
    _default_buckets.append(prefect_config.prefect_artifacts_bucket)
except (AttributeError, TypeError, ValueError) as e:
    logger.error(f"Failed to configure default Prefect S3 buckets: {e}")


def create_default_prefect_buckets() -> bool:
    """
    Attempt to create default buckets used by Prefect for flows and other artifacts
    Returns: True if successful; False otherwise

    """
    l_result: BucketCreationResult = create_buckets(_default_buckets)
    if bool(l_result.failure):
        logger.warning(f"Failed to create default Prefect buckets: {l_result.failure}")
        return False
    return True


def create_default_prefect_blocks() -> BucketCreationResult:
    """
    Attempt to create default Prefect storage blocks using the default S3 buckets
    Returns: True if successful; False otherwise

    """
    l_result = BucketCreationResult()
    l_settings: Dict[str, Any] = {
        "use_ssl": minio_config.secure,
        "key": minio_config.access_key,
        "secret": minio_config.secret_key.get_secret_value(),
        "client_kwargs": {
            "endpoint_url": f"{minio_config.protocol}://{minio_config.endpoint}",
        },
    }
    for l_bucket_name in _default_buckets:
        try:
            block_storage = RemoteFileSystem(
                basepath=f"s3://{l_bucket_name}",
                # key_type="hash",
                settings=dict(
                    use_ssl=minio_config.secure,
                    key=minio_config.access_key,
                    secret=minio_config.secret_key.get_secret_value(),
                    client_kwargs=l_settings,
                ),
            )
            block_storage.save(f"{l_bucket_name}", overwrite=True)
            l_result.success.append(l_bucket_name)
        except (ValueError, PrefectException) as e:
            logger.warning(f"Failed to create Prefect block {l_bucket_name}: {e}")
            l_result.failure.append(l_bucket_name)
    return l_result
