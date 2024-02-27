#!/usr/bin/env bash
# exit immediately upon error
set -e

echo "Be sure to run this command from a terminal which has activated the /backend \
Python poetry virtual environment"

prefect config set PREFECT_API_URL="http://prefect.localhost:57073/api"