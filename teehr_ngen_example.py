"""This is an example of how to use TEEHR in NGEN."""
from pathlib import Path
import shutil

# import numpy as np
import pandas as pd
from teehr import Evaluation
from teehr import Metrics as metrics
from teehr.models.tables import Configuration

from utils import (
    get_usgs_nwm30_crosswalk,
    get_usgs_point_geometry,
    get_simulation_output_csv,
    get_gages_from_hydrofabric,
    get_simulation_start_end_time
)

# In NGEN this will be provided by NGEN.
NGEN_DATA_DIR = Path("/home/sam/git/NextGen/ngen-data/AWI_16_2853886_006")

# TODO: Set ownership/permissions of NGEN_DATA_DIR?

# Set a path to the directory where the evaluation will be created
TEST_STUDY_DIR = Path(NGEN_DATA_DIR, "teehr")
shutil.rmtree(TEST_STUDY_DIR, ignore_errors=True)
TEST_STUDY_DIR.mkdir(parents=True, exist_ok=True)

# Create a TEEHR Evaluation object and initialize a dataset.
ev = Evaluation(dir_path=TEST_STUDY_DIR)
ev.enable_logging()
ev.clone_template()
ev.spark.conf.set(
  "spark.sql.sources.partitionOverwriteMode", "dynamic"
)
# print(ev.spark.conf.get("spark.sql.sources.partitionOverwriteMode"))

LOCATIONS = Path(TEST_STUDY_DIR, "cache", "locations.parquet")
NWM_USGS_XWALK = Path(TEST_STUDY_DIR, "nwm_usgs_crosswalk.parquet")
NGEN_USGS_XWALK = Path(TEST_STUDY_DIR, "ngen_usgs_crosswalk.parquet")
NGEN_CACHE_OUTPUT = Path(TEST_STUDY_DIR, "cache", "ngen_output.parquet")

# Get the start and end time of the simulation.
start_date, end_date = get_simulation_start_end_time(NGEN_DATA_DIR)

# Get the USGS to NWM crosswalk and USGS point geometry.
usgs_nwm_xwalk_df = get_usgs_nwm30_crosswalk()
usgs_nwm_xwalk_df = usgs_nwm_xwalk_df.set_index("primary_location_id")

usgs_point_geom = get_usgs_point_geometry()
usgs_point_geom = usgs_point_geom.set_index("id")

ngen_usgs_gages = get_gages_from_hydrofabric(NGEN_DATA_DIR)

# Read the NGEN output timeseries and link to USGS and NWM ID's
gage_output_list = []
for gage_pair in ngen_usgs_gages:
    gage_output = get_simulation_output_csv(gage_pair[0], NGEN_DATA_DIR)
    gage_output["ngen_id"] = "ngen-" + gage_pair[0].split("-")[1]
    gage_output["usgs_id"] = "usgs-" + gage_pair[1]
    gage_output["nwm_id"] = usgs_nwm_xwalk_df["secondary_location_id"].loc["usgs-" + gage_pair[1]]
    gage_output_list.append(gage_output)
all_ngen_output = pd.concat(gage_output_list)
all_ngen_output.to_parquet(NGEN_CACHE_OUTPUT)

# FOR TESTING: Limit to a single day.
end_date = "2018-04-02 01:00:00"
all_ngen_output = all_ngen_output[all_ngen_output["current_time"] <= end_date]

# Get primary locations and load to dataset.
locations_df = usgs_point_geom.loc[all_ngen_output["usgs_id"].unique()]
locations_df.reset_index(inplace=True)
locations_df.to_parquet(LOCATIONS)

# Load the location data (USGS points)
ev.locations.load_spatial(in_path=LOCATIONS)

# Load the USGS-NWM Crosswalk.
usgs_nwm_eval_xwalk_df = usgs_nwm_xwalk_df.loc[locations_df.id]
usgs_nwm_eval_xwalk_df.reset_index(inplace=True)
usgs_nwm_eval_xwalk_df.to_parquet(NWM_USGS_XWALK)
ev.location_crosswalks.load_parquet(
    in_path=NWM_USGS_XWALK
)

# Load the USGS-NGEN Crosswalk.
tmp_df = all_ngen_output[~all_ngen_output["ngen_id"].duplicated()]
ngen_usgs_eval_xwalk_df = tmp_df[["usgs_id", "ngen_id"]].copy()
ngen_usgs_eval_xwalk_df.rename(
    columns={
        "usgs_id": "primary_location_id",
        "ngen_id": "secondary_location_id"
    }, inplace=True
)
ngen_usgs_eval_xwalk_df.to_parquet(NGEN_USGS_XWALK)
ev.location_crosswalks.load_parquet(
    in_path=NGEN_USGS_XWALK
)

# Load the NGEN simulation timeseries
ev.configurations.add(
    Configuration(
        name="ngen",
        type="secondary",
        description="Nextgen simulation output"
    )
)

# Load the NWM retrospective timeseries
ev.fetch.nwm_retrospective_points(
    nwm_version="nwm30",
    variable_name="streamflow",
    start_date=start_date,
    end_date=end_date
)

ev.secondary_timeseries.load_parquet(
    in_path=NGEN_CACHE_OUTPUT,
    field_mapping={
        "current_time": "value_time",
        "flow": "value",
        "ngen_id": "location_id"
    },
    constant_field_values={
        "reference_time": None,
        "unit_name": "m^3/s",
        "variable_name": "streamflow_hourly_inst",
        "configuration_name": "ngen"
    }
)

# Load the USGS observations timeseries
ev.fetch.usgs_streamflow(
    start_date=start_date,
    end_date=end_date
)

# Create the joined timeseries table
ev.joined_timeseries.create(execute_udf=False)

# Calculate some metrics
df = ev.metrics.query(
    order_by=["primary_location_id", "configuration_name"],
    group_by=["primary_location_id", "configuration_name"],
    include_metrics=[
        metrics.KlingGuptaEfficiency(),
        metrics.NashSutcliffeEfficiency(),
        metrics.RelativeBias()
    ]
).to_pandas()

df.to_csv(Path(TEST_STUDY_DIR, "metrics.csv"), index=False)