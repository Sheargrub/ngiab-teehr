# NGIAB TEEHR Integration

> Automatic evaluation for NGIAB models — no extra configuration, no hassle.

This integration couples the [TEEHR](https://rtiinternational.github.io/teehr/) evaluation toolset
with [Nextgen-In-A-Box (NGIAB)](https://github.com/jameshalgren/NGIAB-CloudInfra) simulation output.
It automatically generates a TEEHR evaluation based on joined timeseries with
[USGS streamflow observations](https://waterdata.usgs.gov/nwis/rt) and [NWM v3.0 retrospective data](https://registry.opendata.aws/nwm-archive/).

## Features

- **On-demand evaluation**: Immediately generate [TEEHR Framework](https://rtiinternational.github.io/teehr/getting_started/teehr_framework.html)
compliant evaluation directories, laying the groundwork for in-depth analyiss
- **Baselines, at a glance**: Perform preliminary assessments with automated efficiency metrics and time-series plots.
- **Visualize results**: Use the NGIAB Data Visualizer to dynamically explore evaluation results in a dynamic context.

| | |
| --- | --- |
| ![alt text](https://ciroh.ua.edu/wp-content/uploads/2022/08/CIROHLogo_200x200.png) | Funding for this project was provided by the National Oceanic & Atmospheric Administration (NOAA), awarded to the Cooperative Institute for Research to Operations in Hydrology (CIROH) through the NOAA Cooperative Agreement with The University of Alabama (NA22NWS4320003). |


## Navigating this repository

This integration is included as a base component of NGIAB's Docker distribution, where it is loaded from [`awiciroh/ciroh-ngen-image`](https://hub.docker.com/r/awiciroh/ciroh-ngen-image) on DockerHub.
As such, if you would like to run this repository as a part of the NGIAB workflow, please see [NGIAB-CloudInfra](https://github.com/CIROH-UA/NGIAB-CloudInfra) for more info.

HPC support is unfortunately not yet available at this time.

### For general use

- `docs/`: This documentation folder contains information on what you can expect from this integration's outputs, along with the finer details of how the integration's container is built and invoked.
  - For broader ecosystem-wide documentation, please visit DocuHub at [docs.ciroh.org/products/ngiab](https://docs.ciroh.org/products/ngiab), where all of the information from this and other NGIAB repositories is mirrored.
- `Changelog.md`: A per-release changelog of what's been changed recently

### For development

- `scripts/`: These Python scripts form the core of the integration. The main function from `teehr_ngen.py` is invoked as the container entrypoint.
- `requirements.txt`: The set of Python requirements used by the Docker container's virtual environment. 
- `Dockerfile`: The build instructions for the Docker container.
  - Releases built from this folder are available at [https://hub.docker.com/r/awiciroh/ciroh-ngen-image](https://hub.docker.com/r/awiciroh/ciroh-ngen-image).
- `example_guide.sh`: An example of a guide script to be run outside of the container.
  - This is currently unmaintained and should be considered experimental.
  - The canonical guide script implementation, `runTeehr.sh`, is currently hosted in [NGIAB-CloudInfra](https://github.com/CIROH-UA/NGIAB-CloudInfra).
- `.github`: Workflows, issue templates, and other GitHub-focused configuration files.
- `pyproject.toml`: Defines project build properties for development purposes. Otherwise unused
  - `poetry.lock` is directly associated with this and should not be edited. <!-- TODO: These might be vestigial and worth removing? -->

### Docker image

To maximize its portability and ease of use, this integration runs from a Docker container, which is built from the Dockerfile at the root of the repository.


### To build and push the TEEHR image to the AWI CIROH registry

Customize the metrics calculated by TEEHR or any other code related to the workflow:

1. Create a branch off of main
2. Make your edits to `scripts/teehr_ngen.py` and/or `scripts/utils.py`
3. Update the `Changelog` so that your changes can be associated with a tag
4. Submit and PR and merge
5. Then checkout main and pull the new changes, and push your tag:
```bash
git checkout main
git pull
git tag -a v0.x.x -m "version 0.x.x"
git push origin v0.x.x
```

This will trigger a `github action` to build and push the image with your tag, and the `latest` tag, to the AWI CIROH registry.

To build and push locally:
```
docker build -t awiciroh/ngiab-teehr:<tag name> .
docker push awiciroh/ngiab-teehr:<tag name>
```

Now you can specify the image tag in the guide.sh script.


## Contributing

Interested in contributing? Please see our [contribution guide](09_CONTRIBUTE.md) for more information.

## Additional resources

- [NGIAB TEEHR Integration on DocuHub](https://docs.ciroh.org/docs/products/ngiab/components/ngiab-teehr/)
- [NGIAB Website](https://ngiab.ciroh.org)
- [NGIAB 101 Training Module](https://docs.ciroh.org/training-NGIAB-101/)