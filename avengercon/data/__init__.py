"""
Internal static data with relevant self-read functions
"""

from avengercon.logger import logger
from os.path import exists
from typing import Optional

from importlib.resources import files
from importlib.resources.abc import Traversable


def get_abs_path(a_submodule: str, a_file_name: str) -> Optional[str]:
    """
    Use the importlib library to robustly derive a packaged file's absolute path.

    :param a_submodule: The name of the submodule just like using an import statement.
    :param a_file_name: The name of the file without any path elements.
    :return: An absolute path to the file's location given the current package's
    installation location; None upon error
    """
    try:
        l_path: Traversable = files(a_submodule).joinpath(a_file_name)
        l_abs_path: str = str(l_path)
        if not exists(l_abs_path):
            logger.warning(f"File doesn't exist: {l_abs_path}")
            return None
        return l_abs_path
    except (ModuleNotFoundError, AttributeError) as e:
        logger.warning(e)
        return None
