### Testing `Dockerfile` setups

To quickly verify whether a Dockerfile is properly configured, try independently running
`docker build` outside of docker compose.

For example, with the Api.Dockerfile:
```bash
docker build -t <image_name> -f Api.Dockerfile .
```

### Docker Commands
- `docker exec -it [CONTAINER_ID] /bin/bash` or `/bin/sh` to get terminal a container
- `docker ps` lists running containers, their status, and ports
- Remove 'everything' in Docker (images, etc.): `docker system prune -a`
- Remove all containers: `docker container prune`
- Remove all volumes: `docker volume prune`
- Remove all 'dangling' images: `docker rmi $(docker images -f "dangling=true" -q)`
- List containers: `docker container ps --all`
- Stop container: `docker stop <container-id>`
- Delete stopped container: `docker rm <container-id>`
- List images: `docker images`
- Delete image: `docker image rm <image-id>`
- [Docker Compose Anchors and Extensions](https://www.howtogeek.com/devops/how-to-simplify-docker-compose-files-with-yaml-anchors-and-extensions/)

### Docker Compose
Docker compose 2 looks for `docker-compose.yml` to begin orchestration. However, it then
also looks at `docker-compose.override.yml` to override/merge the settings from the base
configuration. See the [merge compose files](https://docs.docker.com/compose/multiple-compose-files/merge/)
documentation for the detailed rules on how this happens.

- `docker-compose.override.yml` is the 'dev' settings enabling hot reload and mounting
local files into the backend and frontend containers.

- `docker-compose.yml` forgoes dev only services, hot reload, and local file system mounting.

