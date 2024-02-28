"""
Example "flows" (borrowing term from Prefect) for Celery tasks
"""

from avengercon.celery import tasks
from avengercon.logger import logger


if __name__ == "__main__":
    tasks.hello_avengercon()
    logger.info("We ran the Celery hello_avengercon task")
