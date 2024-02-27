#! /bin/bash
# stop execution instantly on non-zero status. This is to know location of error
set -e

########## Random String Generation Functions ##########
RANDOM_STRING_CORPUS='A-Za-z0-9!%&*+,-./:;<>@^_|~'
# Note, the pwgen utility by the Jack the Ripper author is a more robust solution.
# however, it would require an install making this script less portable. It would also
# potentially include problematic special characters like quotes that will disrupt
# variable substitution in this script, docker compose substitution, and internal
# container logic prior to URL encoding taking place.
# Function to generate a STRING_LENGTH string of characters
rando_string() {
  env LC_ALL=C tr -dc "$RANDOM_STRING_CORPUS" </dev/urandom | head -c 32
}
string_url_encode() {
  echo -ne "$1" | hexdump -v -e '/1 "%02x"' | sed 's/\(..\)/%\1/g'
}
# Used for Minio Access and Secret keygen. Access key is min 3 max 20 chars. Secret is max 40
RANDOM_ALPHANUM_CORPUS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rando_minio_access_key() {
  env LC_ALL=C tr -dc "$RANDOM_ALPHANUM_CORPUS" </dev/urandom | head -c 20
}
rando_minio_secret_key() {
  env LC_ALL=C tr -dc "$RANDOM_ALPHANUM_CORPUS" </dev/urandom | head -c 40
}
# Used to control the initial password setup token for the Dask Jupyter server. Must be
# lowercase alphanumeric string of a default length of 48 characters
RANDOM_ALPHANUM_CORPUS_LOWER="0123456789abcdefghijklmnopqrstuvwxyz"
rando_jupyter_token() {
  env LC_ALL=C tr -dc "$RANDOM_ALPHANUM_CORPUS_LOWER" </dev/urandom | head -c 48
}

######### Variable Declarations #############

# Output filenames
ENV_FILE="./.env"
LOCALHOST_ENV_FILE="./.localhost.env"
CLOUDFLARE_ENV_FILE="./cloudflare.env"

# Top Level Domain (TLS) the services are hosted under: e.g. 'localhost' or "tld.com"
HTTP_PORT="57073"
: "${DOMAIN:=localhost}"
# Subdomains for prod and various development deployments
SUBDOMAIN_API="api"
SUBDOMAIN_PROXY="proxy"
SUBDOMAIN_WHOAMI="whoami"
SUBDOMAIN_CACHE="cache"
SUBDOMAIN_MINIO="bucket"
SUBDOMAIN_FLOWER="celery"
SUBDOMAIN_DASK="dask"
SUBDOMAIN_NOTEBOOK="notebook"
SUBDOMAIN_PREFECT="prefect"

# Traefik endpoint rule settings
TRAEFIK_PRIVATE_IP_CLIENT_RULE="(ClientIP(\`10.0.0.0/8\`) || ClientIP(\`172.16.0.0/12\`) || ClientIP(\`192.168.0.0/16\`))"

# Used to modify services logging level
LOG_LEVEL="info"

# Used by FastAPI server
: "${SECRET_KEY:=$(rando_string)}"
DEPENDENCY_LOGIN_WAIT_SEC=2
DEPENDENCY_LOGIN_RETRY_COUNT=5
: "${GUNICORN_MAX_WORKERS:=4}"

# Redis Settings
REDIS_HOST="redis"
REDIS_PORT="6379"
: "${REDIS_PASSWORD:=$(rando_string)}"
TEST_REDIS_PORT="57076"

REDIS_PASSWORD_URL_ENCODED="$(string_url_encode "${REDIS_PASSWORD}")"
CELERY_BROKER_URL="redis://:${REDIS_PASSWORD_URL_ENCODED}@${REDIS_HOST}:${REDIS_PORT}/0"
CELERY_RESULT_BACKEND="${CELERY_BROKER_URL}"
# Modify connection to account for reverse proxy when attempting connections outside of
# internal Docker network
TEST_CELERY_BROKER_URL="redis://:${REDIS_PASSWORD_URL_ENCODED}@${DOMAIN}:${TEST_REDIS_PORT}/0"
TEST_CELERY_RESULT_BACKEND="${TEST_CELERY_BROKER_URL}"

# Minio Settings
MINIO_ENDPOINT="minio:9000"
TEST_MINIO_PORT="57079"
MINIO_USE_SSL="false"
MINIO_ROOT_USER="avengercon-minio"
: "${MINIO_ROOT_PASSWORD:=$(rando_string)}"
TEST_MINIO_ENDPOINT="${DOMAIN}:${TEST_MINIO_PORT}"

# Dask Settings
: "${DASK_JUPYTER_TOKEN:=$(rando_jupyter_token)}"
DASK_SCHEDULER_ADDRESS="tcp://dask-scheduler:8786"
TEST_DASK_SCHEDULER_TCP_PORT="57080"
TEST_DASK_SCHEDULER_ADDRESS="tcp://${DOMAIN}:${TEST_DASK_SCHEDULER_TCP_PORT}"

# Prefect Settings
PREFECT_SERVER_API_HOST="prefect"
PREFECT_SERVER_API_PORT="4200"
PREFECT_API_URL="http://${PREFECT_SERVER_API_HOST}:${PREFECT_SERVER_API_PORT}/api"
PREFECT_UI_API_URL="${PREFECT_UI_API_URL:-http://${SUBDOMAIN_PREFECT}.${DOMAIN}:${HTTP_PORT}/api}"
PREFECT_LOGGING_SERVER_LEVEL="${PREFECT_LOGGING_SERVER_LEVEL:-$LOG_LEVEL}"
PREFECT_LOGGING_EXTRA_LOGGERS="dask,scipy"
TEST_PREFECT_API_URL="http://${SUBDOMAIN_PREFECT}.${DOMAIN}:${HTTP_PORT}/api"

# As of Dec 23, Prefect's OSS codebase doesn't elegantly handle passwords with special
# characters. This preemptively URL encodes the database password to avoid parsing issues.
#PREFECT_API_DATABASE_PASSWORD_PLAIN="${PREFECT_API_DATABASE_PASSWORD:-$RANDOM_PREFECT_PW}"
#PREFECT_API_DATABASE_PASSWORD=$(string_url_encode "$PREFECT_API_DATABASE_PASSWORD_PLAIN")
#PREFECT_DB_USERNAME=autoai-prefect
#PREFECT_DB_NAME=prefect

# Bash escape is \ Docker compose escape is $ We ultimate need the double $$ to appear
# in the provided docker compose environment variable, thus \$\$
#PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://${PREFECT_DB_USERNAME}:\$\${PREFECT_API_DATABASE_PASSWORD}@${POSTGRES_SERVER}:5432/${PREFECT_DB_NAME}"
# Passing a URL encoded password via variable substitution on a client/agent is problematic as both Docker and the Python
# dotenv package (via pydantic-settings) will attempt to perform the substitution. However, Prefect expects the placeholder
# to remain, e.g. part_of_string:${PASSWORD}@rest_of_string within the environment variable if using the
# PREFECT_API_DATABASE_PASSWORD. Thus, for agents and flow development/testing, simply forgo using the separate config
# incline a URL encoded password to the DATABASE_CONNECTION_URL.
#PREFECT_API_DATABASE_CONNECTION_URL_ESCAPED="postgresql+asyncpg://${PREFECT_DB_USERNAME}:${PREFECT_API_DATABASE_PASSWORD}@${POSTGRES_SERVER}:5432/${PREFECT_DB_NAME}"

#PREFECT_API_DATABASE_ECHO="False"
#PREFECT_API_DATABASE_MIGRATE_ON_START="True"
# Unofficial variables for prefect server
PREFECT_MINIO_ACCESS_KEY="${PREFECT_MINIO_ACCESS_KEY:-$(rando_minio_access_key)}"
PREFECT_MINIO_SECRET_KEY="${PREFECT_MINIO_SECRET_KEY:-$(rando_minio_secret_key)}"
PREFECT_MINIO_FLOWS_BUCKET_NAME="prefect-flows"
PREFECT_MINIO_ARTIFACTS_BUCKET_NAME="prefect-artifacts"


# NOTE: If you'd like to use basic auth middleware with Traefik, you'll need to hash
# the username and password.
# https://doc.traefik.io/traefik/middlewares/http/basicauth/
# here's a basic setup to accomplish that (which requires system level installs on a
# unix OS. For example, on Ubuntu run:
# sudo apt-get install apache2-utils
#string_brypt_hash() {
#  htpasswd -bnB "$1" "$2" | sed -e s/\\$/\\$\\$/g
#}
#BASIC_AUTH_CREDS="$(string_brypt_hash "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}")"

######### Output to ENV_FILE #############
# https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
YELLOW='\033[0;93m'
NO_COLOR='\033[0m'
# Check if .env file already exists
if [ -f $ENV_FILE ]; then
  echo -e "${YELLOW}$ENV_FILE file already exists${NO_COLOR}. To reset, remove it then \
re-run this script."
# If not, initialize it with new key:value pairs
else
  # Create the .env file
  touch $ENV_FILE

  # Write to the file
  {
    echo "# Used by run_*.sh scripts & avengercon module to dynamically configure localhost";
    echo "# development and testing environment variable coordination.";
    echo "# Valid log level values: 'critical', 'error', 'warning', 'info', 'debug'";
    echo "LOG_LEVEL=${LOG_LEVEL}";

    echo "# Traefik settings and labels";
    echo "HTTP_PORT=${HTTP_PORT}";
    echo "DOMAIN=${DOMAIN}";
    echo "TRAEFIK_PRIVATE_IP_CLIENT_RULE=${TRAEFIK_PRIVATE_IP_CLIENT_RULE}";

    echo "# Traefik subdomains for deployments";
    echo "SUBDOMAIN_API=${SUBDOMAIN_API}";
    echo "SUBDOMAIN_PROXY=${SUBDOMAIN_PROXY}";
    echo "SUBDOMAIN_WHOAMI=${SUBDOMAIN_WHOAMI}";
    echo "SUBDOMAIN_CACHE=${SUBDOMAIN_CACHE}";
    echo "SUBDOMAIN_MINIO=${SUBDOMAIN_MINIO}";
    echo "SUBDOMAIN_FLOWER=${SUBDOMAIN_FLOWER}";
    echo "SUBDOMAIN_DASK=${SUBDOMAIN_DASK}";
    echo "SUBDOMAIN_NOTEBOOK=${SUBDOMAIN_NOTEBOOK}";
    echo "SUBDOMAIN_PREFECT=${SUBDOMAIN_PREFECT}";

    echo "# FastAPI Settings";
    echo "GUNICORN_MAX_WORKERS=${GUNICORN_MAX_WORKERS}";
    echo "SECRET_KEY=${SECRET_KEY}";
    echo "DEPENDENCY_LOGIN_WAIT_SEC=${DEPENDENCY_LOGIN_WAIT_SEC}";
    echo "DEPENDENCY_LOGIN_RETRY_COUNT=${DEPENDENCY_LOGIN_RETRY_COUNT}";

    echo "# Redis Settings";
    echo "REDIS_HOST=${REDIS_HOST}";
    echo "REDIS_PORT=${REDIS_PORT}";
    echo "REDIS_PASSWORD=${REDIS_PASSWORD}";
    echo "TEST_REDIS_PORT=${TEST_REDIS_PORT}";

    echo "# MinIO Configuration Settings";
    echo "# https://min.io/docs/minio/linux/reference/minio-server/settings.html";
    echo "MINIO_ENDPOINT=${MINIO_ENDPOINT}";
    echo "MINIO_USE_SSL=${MINIO_USE_SSL}";
    echo "MINIO_ROOT_USER=${MINIO_ROOT_USER}";
    echo "MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}";
    echo "TEST_MINIO_PORT=${TEST_MINIO_PORT}";

    echo "# Celery + Flower Configuration Settings";
    echo "# Note: The Kombu dependency in Celery has a poorly documented behavior that";
    echo "# requires these two environment variables to be accurate to behave well.";
    echo "# A good indicator if there's a problem is running 'celery inspect ping'";
    echo "# 'pong' should be returned quickly. A connection error will be raised if";
    echo "# Kombu isn't configured properly";
    echo "CELERY_BROKER_URL=${CELERY_BROKER_URL}";
    echo "CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}";

    echo "# Dask settings";
    echo "DASK_SCHEDULER_ADDRESS=${DASK_SCHEDULER_ADDRESS}";
    echo "DASK_JUPYTER_TOKEN=${DASK_JUPYTER_TOKEN}";
    echo "TEST_DASK_SCHEDULER_TCP_PORT=${TEST_DASK_SCHEDULER_TCP_PORT}";

    echo "# Prefect settings";
    echo "# https://docs.prefect.io/latest/api-ref/prefect/settings";
    echo "PREFECT_API_URL=${PREFECT_API_URL}";
    echo "PREFECT_UI_API_URL=${PREFECT_UI_API_URL}";
    echo "PREFECT_SERVER_API_HOST=${PREFECT_SERVER_API_HOST}"
    echo "PREFECT_SERVER_API_PORT=${PREFECT_SERVER_API_PORT}"
    echo "PREFECT_LOGGING_SERVER_LEVEL=${PREFECT_LOGGING_SERVER_LEVEL}"
    echo "PREFECT_LOGGING_EXTRA_LOGGERS=${PREFECT_LOGGING_EXTRA_LOGGERS}";
    echo "# Unofficial Prefect server configuration values";
    echo "PREFECT_MINIO_ACCESS_KEY=${PREFECT_MINIO_ACCESS_KEY}";
    echo "PREFECT_MINIO_SECRET_KEY=${PREFECT_MINIO_SECRET_KEY}";
    echo "PREFECT_MINIO_FLOWS_BUCKET_NAME=${PREFECT_MINIO_FLOWS_BUCKET_NAME}";
    echo "PREFECT_MINIO_ARTIFACTS_BUCKET_NAME=${PREFECT_MINIO_ARTIFACTS_BUCKET_NAME}";
  } >> $ENV_FILE
fi

# Check if .env file already exists
if [ -f $LOCALHOST_ENV_FILE ]; then
  echo -e "${YELLOW}$LOCALHOST_ENV_FILE file already exists${NO_COLOR}. To reset, remove \
it then re-run this script."
# If not, initialize it with new key:value pairs
else
  # Create the .env file
  touch $LOCALHOST_ENV_FILE

  # Write to the file
  {
    echo "# Used as a fallback by python interpreters running the python module";
    echo "# outside of a container (e.g. the dev's localhost). These configs will be";
    echo "# temporarily loaded into the running interpreter's environment variables using";
    echo "# the _inject_dev_settings() function in __init__.py"
    echo "# Valid log level values: 'critical', 'error', 'warning', 'info', 'debug'";
    echo "LOG_LEVEL=${LOG_LEVEL}";

    echo "# Traefik settings and labels";
    echo "HTTP_PORT=${HTTP_PORT}";
    echo "DOMAIN=${DOMAIN}";

    echo "# Traefik subdomains for deployments";
    echo "SUBDOMAIN_API=${SUBDOMAIN_API}";
    echo "SUBDOMAIN_PROXY=${SUBDOMAIN_PROXY}";
    echo "SUBDOMAIN_WHOAMI=${SUBDOMAIN_WHOAMI}";
    echo "SUBDOMAIN_CACHE=${SUBDOMAIN_CACHE}";
    echo "SUBDOMAIN_MINIO=${SUBDOMAIN_MINIO}";
    echo "SUBDOMAIN_FLOWER=${SUBDOMAIN_FLOWER}";
    echo "SUBDOMAIN_DASK=${SUBDOMAIN_DASK}";
    echo "SUBDOMAIN_NOTEBOOK=${SUBDOMAIN_NOTEBOOK}";

    echo "# FastAPI Settings";
    echo "SECRET_KEY=${SECRET_KEY}";
    echo "DEPENDENCY_LOGIN_WAIT_SEC=${DEPENDENCY_LOGIN_WAIT_SEC}";
    echo "DEPENDENCY_LOGIN_RETRY_COUNT=${DEPENDENCY_LOGIN_RETRY_COUNT}";

    echo "# Redis Settings";
    echo "REDIS_HOST=${DOMAIN}";
    echo "REDIS_PORT=${TEST_REDIS_PORT}";
    echo "REDIS_PASSWORD=${REDIS_PASSWORD}";

    echo "# MinIO Configuration Settings";
    echo "# https://min.io/docs/minio/linux/reference/minio-server/settings.html";
    echo "MINIO_ENDPOINT=${TEST_MINIO_ENDPOINT}";
    echo "MINIO_USE_SSL=${MINIO_USE_SSL}";
    echo "MINIO_ROOT_USER=${MINIO_ROOT_USER}";
    echo "MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}";

    echo "# Celery + Flower Configuration Settings";
    echo "# Note: The Kombu dependency in Celery has a poorly documented behavior that";
    echo "# requires these two environment variables to be accurate to behave well.";
    echo "# A good indicator if there's a problem is running 'celery inspect ping'";
    echo "# 'pong' should be returned quickly. A connection error will be raised if";
    echo "# Kombu isn't configured properly";
    echo "CELERY_BROKER_URL=${TEST_CELERY_BROKER_URL}";
    echo "CELERY_RESULT_BACKEND=${TEST_CELERY_RESULT_BACKEND}";

    echo "# Dask settings";
    echo "DASK_JUPYTER_TOKEN=${DASK_JUPYTER_TOKEN}";
    echo "DASK_SCHEDULER_ADDRESS=${TEST_DASK_SCHEDULER_ADDRESS}";

    echo "# Prefect settings";
    echo "# https://docs.prefect.io/latest/api-ref/prefect/settings";
    echo "PREFECT_API_URL=${TEST_PREFECT_API_URL}";
    echo "PREFECT_UI_API_URL=${PREFECT_UI_API_URL}";
    echo "PREFECT_SERVER_API_HOST=${PREFECT_SERVER_API_HOST}"
    echo "PREFECT_SERVER_API_PORT=${PREFECT_SERVER_API_PORT}"
    echo "PREFECT_LOGGING_SERVER_LEVEL=${PREFECT_LOGGING_SERVER_LEVEL}"
    echo "PREFECT_LOGGING_EXTRA_LOGGERS=${PREFECT_LOGGING_EXTRA_LOGGERS}";
    echo "# Unofficial Prefect server configuration values";
    echo "PREFECT_MINIO_ACCESS_KEY=${PREFECT_MINIO_ACCESS_KEY}";
    echo "PREFECT_MINIO_SECRET_KEY=${PREFECT_MINIO_SECRET_KEY}";
    echo "PREFECT_MINIO_FLOWS_BUCKET_NAME=${PREFECT_MINIO_FLOWS_BUCKET_NAME}";
    echo "PREFECT_MINIO_ARTIFACTS_BUCKET_NAME=${PREFECT_MINIO_ARTIFACTS_BUCKET_NAME}";
  } >> $LOCALHOST_ENV_FILE
fi

# Not used in the actual workshop but included for those who'd like to leverage a
# cloudflare tunnel (see the commented out service in docker-compose.yaml) to enable
# TLS communication via Traefik
if [ -f CLOUDFLARE_ENV_FILE ]; then
  echo -e "${YELLOW}${CLOUDFLARE_ENV_FILE} already exists${NO_COLOR}. To reset, remove \
it then re-run this script."
else
  touch $CLOUDFLARE_ENV_FILE
  {
    echo "TUNNEL_TOKEN=<COPY-PASTE-TOKEN-HERE>";
  } >> $CLOUDFLARE_ENV_FILE
fi