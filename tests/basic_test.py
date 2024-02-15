"""
Basic tests to establish that the testing environment is valid
"""

import avengercon
from pytest import fail


def test_import() -> None:
    """
    Validate that the AutoAI package is importable by pytest and using semantic

    Returns: None

    """
    assert isinstance(avengercon.__version__, str)
    try:
        major, minor, patch = avengercon.__version__.split(".")
        assert isinstance(int(major), int)
        assert isinstance(int(minor), int)
        assert isinstance(int(patch), int)
    except ValueError as e:
        fail(f"Module is not using semantic versioning: {e}")
