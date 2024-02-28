"""
Prefect Tasks
"""

from prefect import task
from avengercon.logger import logger


@task
def hello_prefect() -> str:
    """
    A minimal example of a Prefect task
    Returns: A greeting str

    """
    l_response: str = "Hello, Prefect Tasks!"
    logger.info(l_response)
    return l_response


@task
def hello_prefect_dask() -> str:
    """
    A minimal example of a Prefect task sent to a distributed Dask cluster
    Returns: A greeting string

    """
    l_response: str = "Hello, Prefect <3's Dask"
    logger.info(l_response)
    return l_response
