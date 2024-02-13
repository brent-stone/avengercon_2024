## General OS Configurations

### Docker Buildkit
Enabling Docker BuildKit will help ensure pip and npm aren't constantly downloading the same
packages over and over again.
   - On your host machine, enable BuildKit using an environment variable: `export DOCKER_BUILDKIT=1`
   - To permanently set the DOCKER_BUILDKIT flag on Ubuntu:
     - `gedit ~/.profile`
     - Add the following to the .profile: `export DOCKER_BUILDKIT=1`

### Available Scripts

Be sure to mark scripts as executable with `chmod +x <script_path>`

- `customize_deploy_config.sh` prepared a `.env` deployment configuration with a custom
Top Level Domain (TLD) and reverse proxy port target. Use the `-h` argument for directions.
- `full_reset.sh` removes all containers, `.env` configs, TLS key pairs, and volumes then
recreates all of them using `initialize_env.sh`.
- `initialize_env.sh` attempts to create a new `.env` deployment config and TLS
key pair.
- `run_dev.sh` runs a Docker Compose deployment in a Development configuration.
  - A database administration tool is available at [`https://db.localhost`](https://db.localhost)
  - A redis administration tool is available at [`https://flower.localhost`](https://flower.localhost)
- `run_prod.sh` runs a Docker Compose deployment in a Production configuration.
- `setup_stack_yml.sh` prepares a Docker Swarm deployment specification.
- `soft_reset.sh` removes containers and resets `.env` configs and TLS key pairs. Volumes
and stateful authentication credentials such as the API's PostgreSQL client password are
retained.
- `openssl.cnf` is a configuration for generating the self-signed keypairs using openssl.
  - The DNS records at the bottom should match the `DOMAIN` setting in the `.env` configuration.
  - Let's Encrypt should be used when associating the servers with a legitimate domain.

## Windows
!!! warning
    Update your git settings so all files are not auto-converted to
    Windows style line endings: `git config --global core.autocrlf false`


