"""
Celery orchestration server and workers
"""

from typing import Optional, Dict
from avengercon.logger import logger

from avengercon.config import avengercon_config
from celery import Celery
from kombu.exceptions import ConnectionError
from kombu.exceptions import OperationalError
from time import sleep
from avengercon.celery import config
from sys import exit


celery_server: Celery = Celery(main="avengercon")
try:
    celery_server.config_from_object(obj=config, silent=False, force=True)
except (ImportError, AttributeError, ModuleNotFoundError) as e:
    logger.error(f"Failed to configure celery server: {e}")
    exit(1)


def verify_celery_connection(a_celery_server: Celery) -> bool:
    """
    Verifies that the celery server is reachable
    Args:
        a_celery_server: An initialized Celery object

    Returns: True if the server connection is successful; False otherwise

    """
    for i in range(avengercon_config.DEPENDENCY_LOGIN_RETRY_COUNT):
        try:
            response: Optional[Dict[str, Dict[str, str]]] = (
                a_celery_server.control.inspect().ping()
            )
            if isinstance(response, dict) and bool(response):
                logger.info("Celery successfully connected.")
                return True
        except (ConnectionError, OperationalError):
            pass
        logger.warning("Celery failed to connect")
        logger.warning(
            f"\t{avengercon_config.DEPENDENCY_LOGIN_RETRY_COUNT - i} retries pending...",
        )
        sleep(avengercon_config.DEPENDENCY_LOGIN_WAIT_SEC)
    return False
