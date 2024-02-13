#!/usr/bin/env bash
# Force the poetry shell to re-activate despite the common "Virtual environment already activated: ..." notice
# Run this using source. E.G. 'source scripts/force_poetry_shell.sh'
source "$(poetry env info --path)/bin/activate"