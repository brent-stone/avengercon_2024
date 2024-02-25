"""
Celery task declarations
"""

from avengercon.celery import celery_server
from avengercon.logger import logger


@celery_server.task(name="tasks.hello_avengercon", ignore_result=False)
def hello_avengercon() -> str:
    """
    Toy task to test celery is working as expected
    Returns: Nothing but logs a notice

    """
    l_response: str = "Hello, AvengerCon! <3 Celery"
    logger.info(l_response)
    return l_response
