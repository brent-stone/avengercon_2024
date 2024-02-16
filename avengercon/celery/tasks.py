"""
Celery task declarations
"""

from avengercon.celery import celery_server
from avengercon.logger import logger


@celery_server.task(name="tasks.hello_avengercon", ignore_result=True)
def hello_avengercon() -> None:
    """
    Toy task to test celery is working as expected
    Returns: Nothing but logs a notice

    """
    logger.info("Hello, AvengerCon! <3 Celery")
