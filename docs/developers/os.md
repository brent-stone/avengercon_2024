## General OS Configurations

### Windows
!!! warning
    Update your git settings so all files are not auto-converted to
    Windows style line endings: `git config --global core.autocrlf false`

### Docker Buildkit
Enabling Docker BuildKit will help ensure pip and npm aren't constantly downloading the same
packages over and over again.
   - On your host machine, enable BuildKit using an environment variable: `export DOCKER_BUILDKIT=1`
   - To permanently set the DOCKER_BUILDKIT flag on Ubuntu:
     - `gedit ~/.profile`
     - Add the following to the .profile: `export DOCKER_BUILDKIT=1`

### Available Scripts

Be sure to mark scripts as executable with `chmod +x <script_path>`

- `run_dev.sh` runs a Docker Compose deployment in a Development configuration.
- `soft_reset.sh` removes containers and resets `.env` configs. Volumes
and stateful authentication credentials such as passwords are retained.
- `full_reset.sh` removes containers and resets `.env` configs. Volumes are deleted.
- `initialize_env.sh` attempts to create a new `.env` deployment config.
- `export_poetry_to_req_txt.[sh|bat]` use poetry to export the various Python environment
dependencies to `requirements.txt` format compatible with `pip`.
- `update_tooling.[sh|bat]` attempts to run self-update features of the recommended dev
tooling.
- `setup_linux_kvm_amd.sh` helps set up a Docker user and virtualization on Linux
- `force_poetry_shell.sh` helps activate a poetry virtual environment in the current
terminal when `poetry shell` isn't working.
