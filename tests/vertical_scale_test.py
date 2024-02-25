"""
Demonstration tests for performance difference when using lru_cache or taichi
These functions and example tests are a synthesis of the examples from lru_cache,
pytest-benchmark, and taichi:
1. https://docs.python.org/3/library/functools.html#functools.lru_cache
2. https://pypi.org/project/pytest-benchmark/
3. https://docs.taichi-lang.org/docs/accelerate_python#dynamic-programming-longest-common-subsequence

Run these tests alone using:
pytest tests/vertical_scale_test.py --benchmark-histogram
"""

from functools import lru_cache
from logging import INFO, info
from pytest import mark
import taichi as ti
from numba import jit
from numba import uint64 as numba_uin64
from tests.conftest import l_fib_vals_small, l_fib_vals_max_u64, l_fib_vals_large
from pytest import LogCaptureFixture
from pytest_benchmark.fixture import BenchmarkFixture

# Initialize the Taichi kernel ahead of testing.
# Note: Taichi's default behavior is to cache compiled kernels to reduce launch overhead
# so this isn't strictly necessary.
# https://docs.taichi-lang.org/docs/kernel_function#kernel
ti.init(arch=ti.cpu, debug=True)


def fib(n: int) -> int:
    """
    Recursively compute fibonacci number
    Args:
        n: Length of sequence to calculate the Fibonacci Number

    Returns: Fibonacci number

    """
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    """
    Remake of fib() using lru_cache to leverage memoization
    Note: functools.cache() has the same effect as lru_cache(maxsize=None)
    Args:
        n: Length of sequence to calculate the Fibonacci Number

    Returns: Fibonacci number

    """
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


@ti.kernel
def fib_taichi(n: ti.u64) -> ti.u64:
    """
    Compute fibonacci number using Taichi. Use a loop-based approach to
    maximize the ability for Taichi just-in-time (JIT) compilation to take place
    Args:
        n: Length of sequence to calculate the Fibonacci Number

    Returns: Fibonacci number

    """
    result = ti.u64(0)
    if n < 1:
        result = 0
    elif n == 1:
        # Note: Only one return statement is allowed in Taichi functions. We must assign
        # the scope level 'result' variable and wait until the one and only return can
        # be made.
        # https://docs.taichi-lang.org/docs/kernel_function#at-most-one-return-statement
        result = 1
    elif n > 1:
        current_val = ti.u64(0)
        next_val = ti.u64(1)
        for index in range(n):
            current_val, next_val = next_val, current_val + next_val
        result = current_val
    return result


@jit
def fib_numba(n: numba_uin64) -> numba_uin64:
    """
    Recursively compute fibonacci number using Numba just-in-time (JIT) compilation
    Args:
        n: Length of sequence to calculate the Fibonacci Number

    Returns: Fibonacci number

    """
    if n < 2:
        return n
    return fib_numba(n - 1) + fib_numba(n - 2)


@jit
def fib_numba_loop(n: numba_uin64) -> numba_uin64:
    """
    Recursively compute fibonacci number using Numba just-in-time (JIT) compilation
    Args:
        n: Length of sequence to calculate the Fibonacci Number

    Returns: Fibonacci number

    """
    result = numba_uin64(0)
    if n == 1:
        result = numba_uin64(1)
    elif n > 1:
        current_val = numba_uin64(0)
        next_val = numba_uin64(1)
        for index in range(n):
            current_val, next_val = next_val, current_val + next_val
        result = current_val
    return result


@mark.parametrize("n,expected", l_fib_vals_small)
def test_fib(n: int, expected: int, benchmark: BenchmarkFixture) -> None:
    """
    Benchmark the baseline performance of fib() without memoization
    Args:
        n: the number to compute its Fibonacci Number
        expected: the expected Fibonacci Number
        benchmark: pytest-benchmark fixture

    Returns: None

    """
    result = benchmark(fib, n)
    assert result == expected


@mark.parametrize("n,expected", l_fib_vals_large)
def test_fib_cached(
    n: int,
    expected: int,
    benchmark: BenchmarkFixture,
    caplog: LogCaptureFixture,
) -> None:
    """
    Benchmark the baseline performance of fib_cached() with memoization
    Args:
        n: the number to compute its Fibonacci Number
        expected: the expected Fibonacci Number
        benchmark: pytest-benchmark fixture
        caplog: pytest built-in logging fixture

    Returns: None

    """
    result = benchmark(fib_cached, n)
    assert result == expected
    with caplog.at_level(INFO):
        # Self-verify that the LRU cache persists between tests and get a sense for the
        # scale of cache hits/miss
        info(f"n: {n}. {fib_cached.cache_info()}")


@mark.parametrize("n,expected", l_fib_vals_max_u64)
def test_fib_taichi(n: int, expected: int, benchmark: BenchmarkFixture) -> None:
    """
    Benchmark the baseline performance of fib_taichi()
    Args:
        n: the number to compute its Fibonacci Number
        expected: the expected Fibonacci Number
        benchmark: pytest-benchmark fixture

    Returns: None

    """
    result = benchmark(fib_taichi, n)
    assert result == expected


@mark.parametrize("n,expected", l_fib_vals_small)
def test_fib_numba_recursion(
    n: int,
    expected: int,
    benchmark: BenchmarkFixture,
) -> None:
    """
    Benchmark the baseline performance of fib_numba()
    Args:
        n: the number to compute its Fibonacci Number
        expected: the expected Fibonacci Number
        benchmark: pytest-benchmark fixture

    Returns: None

    """
    result = benchmark(fib_numba, n)
    assert result == expected


@mark.parametrize("n,expected", l_fib_vals_max_u64)
def test_fib_numba_loop(n: int, expected: int, benchmark: BenchmarkFixture) -> None:
    """
    Benchmark the baseline performance of fib_numba()
    Args:
        n: the number to compute its Fibonacci Number
        expected: the expected Fibonacci Number
        benchmark: pytest-benchmark fixture

    Returns: None

    """
    result = benchmark(fib_numba_loop, n)
    assert result == expected
