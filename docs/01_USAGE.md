# Usage Guide

## Running the integration

An option to run the TEEHR integration will be provided when using the `guide.sh` script from NGIAB's Docker distribution, NGIAB-CloudInfra. <!-- TODO: Link -->
It can also be run manually via `runTeehr.sh`.
For more information, please see the NGIAB documentation.

## Navigating the evaluation directory

Within the NGIAB model run directory, the evaluation outputs will be saved to the `/teehr/` folder.
This folder adheres to the TEEHR directory structure. For more information, please see ["The TEEHR Framework"](https://rtiinternational.github.io/teehr/getting_started/teehr_framework.html)
within TEEHR's documentation.

In addition to the usual directory structure, the following files will be output:
- A table containing calculated efficiency metrics from the evaluation, saved as `metrics.csv`.
- A timeseries plot comparing the model outputs to the NWM v3.0 retrospective, saved as a PNG file. <!-- TODO: Is there a pattern to the filename? -->

For each gage, `metrics.csv` will provide the following evaluation metrics: <!-- TODO: link to explainers? -->
- Kling-Gupta Efficiency
- Nash-Sutcliffe Efficiency
- Relative Bias
- Root Mean Standard Deviation Ratio

## Visualization

For information on visualization, please see the NGIAB Data Visualizer documentation. <!-- TODO: Link -->