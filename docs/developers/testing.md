## Pytest tips
See the `pyproject.toml` and `tox.ini` in the source code for a pytest configuration
reference.

- Run a specific test:
    * `pytest tests/basic_test.py -k "test_import" -vv`
    * `pytest tests/basic_test.py::test_import`

- Run a test with benchmarking (requires [pytest-benchmark](https://pypi.org/project/pytest-benchmark/))
    * `pytest tests/vertical_scale_test.py --benchmark-histogram`
