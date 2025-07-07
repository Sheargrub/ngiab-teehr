# Scripts

The `scripts/` folder is responsible for handling the automated evaluation. Its contents are run in a [uv-based](https://docs.astral.sh/uv/) virtual environment defined by `requirements.txt`.

# `teehr_ngen.py`

Consists of an end-to-end `main()` function that gets executed as the container entrypoint.

# `utils.py`

This file consists of helper functions that are called by `teehr_ngen.py`.

## `get_usgs_nwm30_crosswalk()`

Fetches and returns a location crosswalk that relates USGS gage locations to NWM 3.0 gage locations.

## `get_usgs_point_geometry()`

Fetches and returns the point geometry for USGS streamflow gage locations.

## `get_simulation_output_format(folder_to_eval)`

Checks the output format of an NGIAB model run, where:
- `folder_to_eval` is a path to an NGIAB model run directory.

Returns:
- `"netcdf"` if `.nc` files are found in `[folder_to_eval]/outputs/troute/`.
- Otherwise, `"csv"` if `.csv` files are found in `[folder_to_eval]/outputs/troute/`.
- Otherwise, raises a `FileNotFoundError`.

## `get_simulation_output_netcdf(wb_id, folder_to_eval)`

Reads NetCDF-based NextGen simulation output for a single gage, where:
- `wb_id` is an internal hydrofabric ID. <!-- TODO: verify! -->
- `folder_to_eval` is a path to an NGIAB model run directory.

Returns a `DataFrame` consisting of gage outputs. <!-- TODO: Data type? -->

## `get_simulation_output_csv(wb_id, folder_to_eval)`

Reads CSV-based NextGen simulation output for a single gage, where:
- `wb_id` is an internal hydrofabric ID. <!-- TODO: verify! -->
- `folder_to_eval` is a path to an NGIAB model run directory.

Returns a `DataFrame` consisting of gage outputs. <!-- TODO: Data type? -->

## `get_gages_from_hydrofabric(folder_to_eval)`

Searches a model run folder for `_subset.gpkg`, then fetches all gages from within the geopackage.
- `folder_to_eval` is a path to an NGIAB model run directory.

Returns a list of tuples consisting of hydrofabric IDs and USGS gage identifiers. <!-- TODO: verify! -->

## `get_simulation_start_end_time(folder_to_eval)`

Fetches the start and end times from an NGIAB simulation, where:
- `folder_to_eval` is a path to an NGIAB model run directory.

Returns a tuple containing the start and end times. <!-- TODO: Data type? -->


<!-- TODO: NGIAB model run directory mentions should link to documentation. -->