"""
Global logger and logging configuration for AutoAI
"""

from enum import Enum
from logging import captureWarnings
from logging import error
from logging import getLogger
from logging.config import dictConfig
from os import getenv
from sys import exit


class LogLevel(str, Enum):
    """
    Explicit enumerated class for acceptable log level values.
    """

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


_log_level: str = getenv(key="LOG_LEVEL", default="INFO").upper()
try:
    _ = LogLevel(_log_level)
except ValueError:
    error(f"Invalid LOG_LEVEL configuration value: {_log_level}.")
    exit(1)

LOG_CONFIG = {
    "version": 1,
    # "disable_existing_loggers": True,
    # Possible format metadata which can be used:
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    "formatters": {
        "default": {
            "format": "%(levelname)s:\t [%(module)s:%(funcName)s:%(lineno)d]:\t "
            "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": _log_level,
        },
    },
    "root": {"handlers": ["console"], "level": _log_level},
    "loggers": {
        "gunicorn": {"propagate": True},
        "gunicorn.access": {"propagate": True},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "uvicorn.error": {"propagate": True},
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#logging
        "celery": {"propagate": True},
        "celery.task": {"propagate": True},
        "celery.app.trace": {"propagate": True},
    },
}

captureWarnings(True)
try:
    dictConfig(LOG_CONFIG)
    logger = getLogger(__name__)
    logger.debug("Successfully configured logger")
except ValueError as e:
    error(f"Logging configuration error: {e}")
    exit(1)
