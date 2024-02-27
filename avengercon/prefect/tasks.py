"""
Prefect Tasks
"""

from prefect import task
from avengercon.logger import logger
from dask import datasets
from avengercon.dask import get_dask_client


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
def hello_prefect_dask():
    """
    A minimal example of a Prefect task sent to a distributed Dask cluster
    Returns: A Dask dataframe

    """
    with get_dask_client() as client:
        df = datasets.timeseries("2000", "2001", partition_freq="4w")
        summary_df = client.compute(df.describe()).result()
    return summary_df
    # l_response: str = "Hello, Prefect <3's Dask"
    # logger.info(l_response)
    # return l_response
