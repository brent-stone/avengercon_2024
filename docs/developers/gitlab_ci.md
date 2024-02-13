Gitlab Continuous Integration (CI) is a way for automatically testing and building
artifacts when commits are made to certain branches. For example, base container images,
the mkdocs-material documentation hosted on GitLab Pages, etc.

### Testing CI locally
The [gitlab-runner](https://docs.gitlab.com/runner/) is available as both an [installable
binary](https://docs.gitlab.com/runner/install/linux-repository.html) or docker image.

To test a CI pipeline before committing (and thus triggering a 'real' CI job), the
gitlab-runner can be used locally.

Locally installed binary example run to generate mkdocs documentation site:
```bash
gitlab-runner exec docker .pages-localhost
```

Docker-in-docker deployment:
```bash
docker run gitlab/gitlab-runner exec docker .pages-localhost
```

!!! note
    Additional details of publishing mkdocs-material generated sites to GitLab is
    [available here](https://squidfunk.github.io/mkdocs-material/publishing-your-site/#gitlab-pages).

### Using CI to build and pushing images to the container registry
To use GitLab CI/CD to build and push images,
[this documentation](https://docs.gitlab.com/ee/user/packages/container_registry/build_and_push_images.html#container-registry-examples-with-gitlab-cicd)
walks through each step of the process.


### Manually publishing images to the container registry
- See [this page](https://docs.gitlab.com/ee/user/packages/container_registry/index.html) for documentation.
- Look for the "CLI Commands" button in top right corner of project's
**Packages & registries** menu.
- `docker login registry.gitlab.com`
  - Use a personal access token for your password
- Use a URL style tag for the image then build it.
  - `docker build -t registry.gitlab.com/stoneguard-software/autoai/<image_name> .`
- Use the URL style tag to then push to the container registry.
  - `docker push registry.gitlab.com/stoneguard-software/autoai/autoai-backend-prod`
