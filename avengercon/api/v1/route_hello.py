"""
Toy routes to ensure basic deployment is working correctly
"""
from typing import Dict, Any

from fastapi import APIRouter

from avengercon import __version__
from avengercon.celery import verify_celery_connection
from avengercon.celery.tasks import hello_avengercon
from celery.result import AsyncResult
from avengercon.prefect.flows import hello_prefect_flow
from avengercon.dask import get_dask_client
from fastapi import HTTPException, status
from avengercon.redis.tasks import hello_redis

router = APIRouter()


@router.get(
    path="/hello_fastapi",
    response_model=str,
)
async def hello_fastapi_route() -> str:
    """
    Most basic test to validate the API is accessible
    Returns: A greeting string

    """
    return f"Hello from the Avengercon Workshop API. I'm version {__version__}"


@router.get(
    path="/hello_celery",
    response_model=str,
)
async def hello_celery_route() -> str:
    """
    Most basic test to validate the Celery service is accessible
    Returns: A greeting string

    """
    if verify_celery_connection():
        l_response: AsyncResult = hello_avengercon.delay()
        return l_response.get()
    return f"Couldn't connect to Celery =\\"


@router.get(
    path="/hello_dask",
    response_model=str,
)
async def hello_dask_route() -> str:
    """
    Most basic test to validate the Dask scheduler is accessible
    Returns: A greeting string

    """
    l_client = get_dask_client()
    l_client_info: Dict[str, Any] = l_client.nthreads()  # type: ignore
    return f"Hello from Dask! Current cluster state: {l_client.status}. Workers: {l_client_info}"


@router.get(
    path="/hello_prefect",
    response_model=str,
)
async def hello_prefect_route() -> str:
    """
    Most basic test to validate the Prefect service is accessible
    Returns: A greeting string

    """
    return hello_prefect_flow()


@router.get(
    path="/hello_redis",
    response_model=str,
)
async def hello_redis_route() -> str:
    """
    Most basic test to validate the Redis service is accessible
    Returns: A greeting string

    """
    l_greeting = hello_redis()
    if l_greeting is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis not connected",
        )
    return l_greeting
