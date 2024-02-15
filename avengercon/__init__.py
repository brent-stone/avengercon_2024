"""
Avengercon VIII Workshop: Horizontally Scaling Python for Production
"""

import importlib.metadata
from importlib.metadata import PackageNotFoundError
from logging import error


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
        return "ERROR-NOT FOUND"


# PEP 8 and PEP 396 compliance
# https://peps.python.org/pep-0008/#module-level-dunder-names
# https://peps.python.org/pep-0396/
__version__: str = get_version()
