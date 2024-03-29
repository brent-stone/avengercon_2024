@echo off
@REM Manually export pyproject.toml defined environments to requirements.txt files for
@REM use by CI and tox pipelines

poetry export --format requirements.txt --output requirements/requirements.txt --without-hashes
poetry export --format requirements.txt --output requirements/requirements-dev.txt --without-hashes --with dev
poetry export --format requirements.txt --output requirements/requirements-pytest.txt --without-hashes --with pytest
poetry export --format requirements.txt --output requirements/requirements-mypy.txt --without-hashes --with mypy
poetry export --format requirements.txt --output requirements/requirements-mkdocs.txt --without-hashes --with mkdocs