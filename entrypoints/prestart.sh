#! /usr/bin/env sh
set -e
# Do anything like wait for DB to migrate/startup here
# uvicorn/gunicorn will execute after this script runs
echo "Beginning FastAPI container pre-start"
#echo "Running Alembic migration"
#(exec alembic upgrade head)
#sleep 0.1
echo "FastAPI container pre-start complete."