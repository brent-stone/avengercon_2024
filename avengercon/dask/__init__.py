"""
Dask client and related functions
https://docs.dask.org/en/latest/futures.html#distributed.Client
"""

from dask.distributed import Client
from avengercon.dask.config import dask_config
from prefect_dask import get_dask_client as prefect_get_dask_client

# Note: This will implicitly get configured via the DASK_SCHEDULER_ADDRESS environment
# variable
dask_client = Client(
    address=dask_config.scheduler_address,
    asynchronous=False,
    name="DaskClientSync",
)


def get_dask_client() -> Client:
    """
    Wrapper for the prefect_dask get_dask_client() function that pre-populates the Dask
    cluster information.
    Returns: A Dask client

    """
    with prefect_get_dask_client(
        address=dask_config.scheduler_address,
        asynchronous=False,
        name="DaskClientSync",
    ) as l_client:
        yield l_client
