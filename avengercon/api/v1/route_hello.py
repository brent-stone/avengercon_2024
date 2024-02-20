"""
Toy routes to ensure basic deployment is working correctly
"""

from fastapi import APIRouter

from avengercon import __version__
from avengercon.celery import verify_celery_connection
from avengercon.celery.tasks import hello_avengercon
from celery.result import AsyncResult

router = APIRouter()


@router.get(
    path="/hello_fastapi",
    response_model=str,
)
async def hello_fastapi() -> str:
    """
    Most basic test to validate the API is accessible
    Returns: A greeting string

    """
    return f"Hello from the Avengercon Workshop API. I'm version {__version__}"


@router.get(
    path="/hello_celery",
    response_model=str,
)
async def hello_celery() -> str:
    """
    Most basic test to validate the Celery service is accessible
    Returns: A greeting string

    """
    if verify_celery_connection():
        l_response: AsyncResult = hello_avengercon.delay()
        return l_response.get()
    return f"Couldn't connect to Celery =\\"
