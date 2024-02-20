"""
Batch data ingest
"""

from fastapi import APIRouter
from fastapi import UploadFile

from avengercon.logger import logger

from avengercon.minio import put_data
from os import stat

router = APIRouter()


@router.post(
    path="/upload",
    response_model=bool,
)
async def upload_file(
    file: UploadFile,
) -> bool:
    """
    Upload a file to MinIO S3 bucket
    Args:
        file: An UploadFile object from FastAPI

    Returns: True if the upload was successful; False otherwise

    """
    try:
        l_file_size: int = stat(file.file.fileno()).st_size
    except (ValueError, TypeError, AttributeError) as e:
        logger.warning(e)
        return False
    return put_data(
        a_bucket_name="avengercon",
        a_file_name=file.filename,
        a_file_size=l_file_size,
        a_file=file.file,
        a_auto_create=True,
    )
