@echo off
SETLOCAL EnableDelayedExpansion

WHERE pyenv >nul 2>&1
IF ERRORLEVEL 0 (
    ECHO pyenv-win may not always self-update cleanly. Run 'pyenv update' manually
) ELSE (
    ECHO pyenv not found: https://pyenv-win.github.io/pyenv-win/
)

pip install --upgrade pip

WHERE poetry >nul 2>&1
IF ERRORLEVEL 0 (
    poetry self update
    poetry self add poetry-plugin-up
    poetry self add poetry-plugin-export
    poetry config warnings.export false
    poetry config virtualenvs.in-project true
    poetry up
) ELSE (
    ECHO Poetry is not installed. Please install poetry then retry.
    ECHO https://python-poetry.org/docs/#installing-with-the-official-installer
    EXIT /B 1
)

pre-commit autoupdate

@REM Output a success notice to the developer.
ECHO "Your dev environment is on the latest hotness."
ECHO "Run tox before committing to verify nothing broke."