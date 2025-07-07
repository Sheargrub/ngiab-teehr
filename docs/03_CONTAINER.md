# Container Management


## Pulling the container

The TEEHR container is hosted on DockerHub as `awiciroh/ngiab-teehr`. Its latest versions are tagged as `latest` and `x86` fot ARM64 and AMD64 systems, respectively. Be sure to choose the appropriate tag for your system's architecture.

## Running the container manually

> Please note that these steps are mostly relevant for development purposes. Most users should launch the container using the guide scripts in NGIAB-CloudInfra. <!-- TODO: Link -->

The following Docker command will launch and run the TEEHR integration, where `[RUN_DIR]` is replaced with the absolute path of your model run directory:
```bash
docker run --rm -v "[RUN_DIR]:/app/data" "awiciroh/ngiab-teehr:[tag]"
```
Here's a breakdown of what this command does:
- `--rm` instructs Docker to tear down and delete the container upon exiting. This is important for saving storage.
- `-v "[RUN_DIR]:/ngen/ngen/data"` mounts your data folder's contents to `app/data/` within the container.
- `"awiciroh/ngiab-teehr:[tag]"` identifies the image. Be sure to select the correct tag for your system.

## Updating the container

Updates to the TEEHR integration container are handled automatically via the `docker_publish.yaml` script.
They can be triggered as follows:

1. Locally checkout and pull the most recent version of the repository's main branch:
```bash
git checkout main
git pull
```
2. Push a new tag, designating a new release version.
```bash
git tag -a v0.x.x -m "version 0.x.x"
git push origin v0.x.x
```

These steps will trigger a `github action` to build and push the image with your tag, and the `latest` tag, to the AWI CIROH registry.

If necessary, the container can also be built and pushed locally:
```bash
docker build -t awiciroh/ngiab-teehr:<tag name>
docker push awiciroh/ngiab-teehr:<tag name>
```
However, in the interest of version management, this is strongly discouraged.

> Note that new versions can only be triggered by maintainers with the appropriate permissions.