"""
Example Prefect flows
"""

from prefect import flow
from avengercon.prefect import tasks
from avengercon.logger import logger
from prefect_dask import DaskTaskRunner
from avengercon.dask.config import dask_config

_dask_task_runner = DaskTaskRunner(
    address=dask_config.scheduler_address,
    # client_kwargs={
    #     "address": dask_config.scheduler_address,
    # },
)


@flow
def hello_prefect_flow() -> str:
    """
    A minimal example of a Prefect flow
    Returns: A greeting string

    """
    l_greeting = tasks.hello_prefect()
    logger.info(f"Hello, Prefect Flows!")
    return l_greeting


@flow(task_runner=_dask_task_runner)
def hello_prefect_dask_flow() -> None:
    """
    A minimal example of a Prefect flow using a Dask cluster
    Returns: An example Dask dataframe

    """
    tasks.hello_prefect_dask.submit()
