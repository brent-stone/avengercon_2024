"""
Avengercon VIII Workshop: Horizontally Scaling Python for Production
"""

import importlib.metadata
from importlib.metadata import PackageNotFoundError
from logging import error
from logging import info
from os import getenv

from dotenv import find_dotenv
from dotenv import load_dotenv

_localhost_settings_filename: str = ".localhost.env"


def get_version() -> str:  # pragma: no cover
    """
    Attempt to retrieve the current version number from the package metadata

    Returns: A string like "0.1.0" using the package metadata

    """
    try:
        return importlib.metadata.version("avengercon")
    except PackageNotFoundError as e:
        error(
            f"{e}. If this is being run in interactive mode (dev), please run 'poetry"
            " shell' and 'poetry install' then try again. If this is being run as a"
            " distributed package, please try `pip install <path_to_wheel.whl>`",
        )
        return "ERROR:NOT FOUND"


# PEP 8 and PEP 396 compliance
# https://peps.python.org/pep-0008/#module-level-dunder-names
# https://peps.python.org/pep-0396/
__version__: str = get_version()


def _inject_dev_settings() -> None:
    """
    Attempt to retrieve environment settings from a remote dev oriented .env file if
    environment variables are not already set

    Returns: Nothing but mutates the active environment variables as needed

    """
    try:
        l_env_path: str = find_dotenv(
            _localhost_settings_filename,
            usecwd=True,
            raise_error_if_not_found=True,
        )
        if load_dotenv(dotenv_path=l_env_path, verbose=True, override=False):
            info(f"Loaded development configuration info from {l_env_path}")
        else:
            raise IOError
    except IOError:
        error("Failed to dynamically load development configuration")


# Use the CELERY_BROKER_URL environment variable as a canary for whether the broader
# corpus of required environment variables are currently set.
if not getenv("CELERY_BROKER_URL"):
    _inject_dev_settings()
