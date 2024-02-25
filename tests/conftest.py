"""
Shared pytest fixtures
https://docs.pytest.org/en/latest/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

from os.path import exists
from typing import Optional, List, Tuple

from importlib.resources import files
from importlib.resources.abc import Traversable
from csv import reader


def get_abs_path(a_submodule: str, a_file_name: str) -> Optional[str]:
    """
    Use the importlib library to robustly derive a file's absolute path.

    :param a_submodule: The name of the module just like using an import statement
    :param a_file_name: The name of the file without any path elements
    :return: An absolute path to the file's location given the current package's
    installation location; None upon error
    """
    try:
        l_path: Traversable = files(a_submodule).joinpath(a_file_name)
        l_abs_path: str = str(l_path)
        if not exists(l_abs_path):
            return None
        return l_abs_path
    except (ModuleNotFoundError, AttributeError) as e:
        return None


_l_fib_csv: Optional[str] = get_abs_path("tests", "fibonacci.csv")
_l_fib_test_vals: List[Tuple[int, int]] = []
if isinstance(_l_fib_csv, str):
    with open(_l_fib_csv, "rt") as l_fd:
        l_fib = reader(l_fd)
        for line in l_fib:
            _l_fib_test_vals.append((int(line[0]), int(line[1])))

l_fib_vals_small: List[Tuple[int, int]] = []
l_fib_vals_med: List[Tuple[int, int]] = []
l_fib_vals_max_u64: List[Tuple[int, int]] = []
l_fib_vals_large: List[Tuple[int, int]] = []
if bool(_l_fib_test_vals):
    l_fib_vals_small = _l_fib_test_vals[8:16]
    l_fib_vals_med = l_fib_vals_small + _l_fib_test_vals[50:52]
    # UIN64 max is 18,446,744,073,709,551,615
    # the 93rd Fibonacci number is the largest that doesn't exceed this value:
    #              12,200,160,415,121,876,738
    l_fib_vals_max_u64 = l_fib_vals_med + [_l_fib_test_vals[93]]
    l_fib_vals_large = l_fib_vals_max_u64 + [_l_fib_test_vals[-1]]
