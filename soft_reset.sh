#! /bin/bash
# stop execution instantly on non-zero status. This is to know location of error
set -e

export DOCKER_BUILDKIT=1

GREEN="\e[32m"
BLUE="\e[34m"
ENDCOLOR="\e[0m"

# Export all current .env values. Passwords and secrets will be re-used so that Postgres
# and other stateful containers don't need to be wiped because new passwords/secrets were
# generated
if [ -f ".env" ]; then
  # Store the current .env settings
  export "$(grep -v '^#' .env | xargs)"
fi

if [ -n "$1" ]; then
    # Apply override settings, if present
    DOMAIN="${1}"
    export DOMAIN
    echo -e "${GREEN}[INFO]${ENDCOLOR} DOMAIN is now set to ${BLUE}${DOMAIN}${ENDCOLOR}"
else
  echo -e "${GREEN}[INFO]${ENDCOLOR} Optionally provide a top level domain \
(e.g. mydomain.com) as an argument to this script to change which domain hosting is \
configured for. Default is 'localhost'"
  read -p ">> Enter your hosting top level domain [localhost]: " tld
  DOMAIN=${tld:-localhost}
  export DOMAIN
  echo -e "${GREEN}[INFO]${ENDCOLOR} DOMAIN is now set to ${BLUE}${DOMAIN}${ENDCOLOR}"
fi

# Environment variable paths used throughout the project
declare -a PathArray=(
  ".env" \
)
# Iterate over the paths and remove the files if present
# The [@] operator is get all elements, space-separated
for l_path in "${PathArray[@]}"; do
  if [ -f "$l_path" ]; then
  rm "$l_path"
  fi
done

# Run the .env and key initialization script
/bin/bash ./initialize_env.sh

# Stop any currently running containers for this project.
# Remove containers for services not defined in the Compose file.
docker compose down --remove-orphans
