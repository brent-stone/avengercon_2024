#! /usr/bin/env sh
set -e

DEFAULT_MODULE_NAME=avengercon.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8883}
LOG_LEVEL=${LOG_LEVEL:-warning}

# Run the pre-start script to trigger Alembic migration and other pre-start actions
/bin/bash prestart.sh

# Start Uvicorn without reload. Mutually exclusive with the GUNICORN startup below
# This deployment strategy should be used when using Docker Swarm or K8s to laterally scale
#exec uvicorn --host $HOST --port $PORT --log-level $LOG_LEVEL --proxy-headers --forwarded-allow-ips "*" "$APP_MODULE"

# Mutually exclusive with the single-node uvicorn deploy above and container orchestration
# replication via Docker Swarm or K8s.
# Gunicorn multiple worker paradigm
DEFAULT_GUNICORN_CONF=gunicorn_conf.py
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Start Gunicorn
exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" --forwarded-allow-ips="*" --proxy-protocol --proxy-allow-from="*" "$APP_MODULE"