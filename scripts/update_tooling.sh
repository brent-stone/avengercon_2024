#!/usr/bin/env bash
# exit immediately upon error
set -e

if ! pyenv --version | grep -q "pyenv"; then
  echo "pyenv is not installed. Please install pyenv then retry."
  exit
fi

# Update pyenv
case "$(uname -sr)" in

   Darwin*)
     echo 'Mac OS detected... using brew to update pyenv'
     brew upgrade pyenv
     ;;

   Linux*Microsoft*)
     echo 'Windows WSL detected... using pyenv internal update tool'
     pyenv update
     ;;

   Linux*)
     echo 'Linux detected... using pyenv internal update tool'
     pyenv update
     ;;

   CYGWIN*|MINGW*|MSYS*)
     echo 'MS Windows detected... using pyenv internal update tool but please not that Windows is not officially supported. Try using WSL'
     pyenv update
     ;;

   *)
     echo 'Unknown operating system. Please manually update pyenv.'
     ;;
esac

pip install --upgrade pip

if ! poetry --version | grep -q "Poetry"; then
  echo "Poetry is not installed. Please install poetry then retry.";
  echo "https://python-poetry.org/docs/#installing-with-the-official-installer";
  exit
fi

poetry self update

if ! which python | grep -q ".venv"; then
  echo "Poetry shell is not activated. Activate it with the force_poetry_shell.sh script";
  exit
fi

if ! poetry self show plugins | grep -q "poetry-plugin-up"; then
  echo "poetry-plugin-up not installed. Adding it now";
  poetry self add poetry-plugin-up
fi

if ! poetry self show plugins | grep -q "poetry-plugin-export"; then
  echo "poetry-plugin-export not installed. Adding it now";
  poetry self add poetry-plugin-export
fi

poetry config warnings.export false

# Requires the `up` plugin. See README.md
poetry up

pre-commit autoupdate

# Output a success notice to the developer.
echo "🚀 Your dev environment is on the latest hotness."
echo "Run tox before committing to verify nothing broke."