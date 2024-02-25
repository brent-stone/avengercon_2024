"""
MinIO SDK functions
"""

from typing import Iterable, BinaryIO
from typing import Optional

from minio import Minio
from minio.error import MinioException
from urllib3.exceptions import MaxRetryError

from avengercon.logger import logger
from avengercon.minio.config import minio_config
from avengercon.minio.schemas import BucketCreationResult
from minio.helpers import ObjectWriteResult


def get_minio_client() -> Optional[Minio]:
    """
    Get Minio client instance

    Returns: Minio client object; None upon error
    """
    l_client = Minio(
        endpoint=minio_config.endpoint,
        access_key=minio_config.access_key,
        secret_key=minio_config.secret_key.get_secret_value(),
        secure=minio_config.secure,
    )
    try:
        _ = l_client.list_buckets()
        logger.debug(f"MinIO connected at {minio_config.endpoint}")
        return l_client
    except (MinioException, MaxRetryError) as e:
        logger.warning(f"MinIO connection failed: {e}")
    return None


def create_buckets(a_bucket_names: Iterable[str]) -> BucketCreationResult:
    """
    Attempt to create a series of buckets
    Returns: BucketCreationResult classifying each creation attempt

    """
    l_result = BucketCreationResult()
    l_client: Optional[Minio] = get_minio_client()
    if not isinstance(l_client, Minio):
        l_result.failure += list(a_bucket_names)
        return l_result
    for l_name in a_bucket_names:
        try:
            if l_client.bucket_exists(l_name):
                l_result.preexisting.append(l_name)
            else:
                l_client.make_bucket(l_name)
                l_result.success.append(l_name)
        except (MinioException, MaxRetryError, ValueError) as e:
            l_result.failure.append(l_name)
            logger.warning(e)
    return l_result


def put_data(
    a_bucket_name: str,
    a_file_name: Optional[str],
    a_file_size: int,
    a_file: BinaryIO,
    a_auto_create: bool = True,
) -> bool:
    """
    Attempt to load data into a bucket. If no bucket exists and auto create is true,
    create a new bucket and return its info. Caution: this function will overwrite
    any object that already exists at the provided bucket + file name.

    Args:
        a_bucket_name: The bucket used to store a new object with the file name & data
        a_file_name: The name to associate with the new object
        a_file_size: The size of the file in bytes
        a_file: The UploadFile object received from a FastAPI route
        a_auto_create: Auto-create a bucket if it doesn't exist; default True

    Returns: True upon success; False otherwise

    """
    if a_file_size <= 0:
        logger.info(f"Invalid file size: {a_file_size}")
        return False
    if not isinstance(a_file_name, str) or not bool(a_file_name):
        logger.info(f"Invalid file name: {a_file_name}")
        return False
    l_client: Optional[Minio] = get_minio_client()
    if not isinstance(l_client, Minio):
        return False
    if not l_client.bucket_exists(a_bucket_name):
        if a_auto_create:
            try:
                l_client.make_bucket(a_bucket_name)
                logger.info(f"Bucket created: {a_bucket_name}")
            except (MinioException, MaxRetryError, ValueError) as e:
                logger.warning(e)
                return False
        else:
            logger.info(f"Bucket doesn't exist: {a_bucket_name}")
            return False
    try:
        # l_file_size: int = stat(a_file.file.fileno()).st_size
        logger.info(
            f"Uploading {a_file_name} [{a_file_size} bytes] to bucket "
            f"{a_bucket_name}",
        )
        # Note: fput_object() will close the file descriptor but the calling function
        # (likely a FastAPI route with UploadFile) may be expecting to close the file
        # itself. Assume the caller is properly managing their file descriptors and use
        # put_object() instead.
        _: ObjectWriteResult = l_client.put_object(
            bucket_name=a_bucket_name,
            object_name=a_file_name,
            data=a_file,
            length=a_file_size,
        )
        return True
    except (MinioException, MaxRetryError, ValueError, TypeError) as e:
        logger.warning(e)
    return False
