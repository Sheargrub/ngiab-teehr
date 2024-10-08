"""A collection of helper functions for the TEEHR-Nextgen project."""
import glob
import os
import logging
import sqlite3
import json

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)

USGS_NWM30_XWALK = "s3://ciroh-rti-public-data/teehr-data-warehouse/common/crosswalks/usgs_nwm30_crosswalk.conus.parquet"  # noqa
# USGS_NWM20_XWALK = "/mnt/data/ciroh/eval_system/nwm/usgs_nwm20_crosswalk.conus.parquet"  # noqa

USGS_POINT_GEOMETRY = "s3://ciroh-rti-public-data/teehr-data-warehouse/common/geometry/usgs_point_geometry.all.parquet"  # noqa
# USGS_POINT_GEOMETRY = "/mnt/data/usgs/usgs_point_geometry.conus.parquet"  # noqa


def get_usgs_nwm30_crosswalk():
    return pd.read_parquet(USGS_NWM30_XWALK)


def get_usgs_point_geometry():
    return gpd.read_parquet(USGS_POINT_GEOMETRY)


def get_simulation_output_csv(wb_id, folder_to_eval):
    """
    NOTE: ONLY WORKS FOR CSV OUTPUT

    Ref: https://github.com/JoshCu/ngiab_eval/blob/2e8fd96b21a369bb93b2a491b0c303a4018a290e/ngiab_eval/core.py
    """
    csv_file = folder_to_eval / "outputs" / "troute" / "*.csv"
    # find the nc file
    csv_files = glob.glob(str(csv_file))
    if len(csv_files) == 0:
        raise FileNotFoundError(
            "No CSV file found in the outputs/troute folder"
        )
    if len(csv_files) > 1:
        logger.warning("Multiple CSV files found in the outputs/troute folder")
        logger.warning("Using the most recent file")
        csv_files.sort(key=os.path.getmtime)
        file_to_open = csv_files[-1]
    if len(csv_files) == 1:
        file_to_open = csv_files[0]
    all_output = pd.read_csv(file_to_open)
    id_stem = wb_id.split("-")[1]
    gage_output = all_output[all_output.featureID == int(id_stem)][
        ["flow", "current_time"]
    ].copy()
    gage_output["ngen_id"] = id_stem
    return gage_output.reset_index()


def get_gages_from_hydrofabric(folder_to_eval):
    """
    Get the gages from the hydrofabric.

    Ref: https://github.com/JoshCu/ngiab_eval/blob/2e8fd96b21a369bb93b2a491b0c303a4018a290e/ngiab_eval/core.py
    """
    # search inside the folder for _subset.gpkg recursively
    gpkg_file = None
    for root, dirs, files in os.walk(folder_to_eval):
        for file in files:
            if file.endswith("_subset.gpkg"):
                gpkg_file = os.path.join(root, file)
                break

    if gpkg_file is None:
        raise FileNotFoundError("No subset.gpkg file found in folder")

    with sqlite3.connect(gpkg_file) as conn:
        results = conn.execute(
            "SELECT id, rl_gages FROM flowpath_attributes WHERE rl_gages IS NOT NULL"
        ).fetchall()
    return results


def get_simulation_start_end_time(folder_to_eval):
    """
    Get start and  end time of the simulation.

    Ref: https://github.com/JoshCu/ngiab_eval/blob/2e8fd96b21a369bb93b2a491b0c303a4018a290e/ngiab_eval/core.py#L77 # noqa
    """
    realization = folder_to_eval / "config" / "realization.json"
    with open(realization) as f:
        realization = json.load(f)
    start = realization["time"]["start_time"]
    end = realization["time"]["end_time"]
    return start, end