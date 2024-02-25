#! /bin/bash
# stop execution instantly on non-zero status. This is to know location of error
set -e

export DOCKER_BUILDKIT=1

# Networks and other thing from a previous run may still be around
# This ensures a relatively clean slate
docker compose down --remove-orphans

docker compose -f docker-compose.yaml up --build