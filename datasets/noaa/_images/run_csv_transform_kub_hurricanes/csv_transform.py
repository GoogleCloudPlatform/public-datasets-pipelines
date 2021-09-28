# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import logging
import os
import pathlib
import subprocess

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("NOAA - Hurricanes process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading {source_url} into {source_file}")
    download_file(source_url, source_file)

    logging.info(f"Remove second header from {source_file}")
    subprocess.call([f"sed -i '2d' {source_file}"], shell=True)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(
        source_file,
    )

    logging.info(f"Transformation Process Starting.. {source_file}")

    logging.info(f"Transform: Renaming Headers.. {source_file}")
    df.columns = df.columns.str.lower()
    rename_headers(df)

    df = reorder_headers(df)

    logging.info(f"Transformation Process complete .. {source_file}")

    logging.info(f"Saving to output file.. {target_file}")

    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("NOAA - Hurricanes process completed")


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "sid",
            "season",
            "number",
            "basin",
            "subbasin",
            "name",
            "iso_time",
            "nature",
            "latitude",
            "longitude",
            "wmo_wind",
            "wmo_pressure",
            "wmo_agency",
            "track_type",
            "dist2land",
            "landfall",
            "iflag",
            "usa_agency",
            "usa_latitude",
            "usa_longitude",
            "usa_record",
            "usa_status",
            "usa_wind",
            "usa_pressure",
            "usa_sshs",
            "usa_r34_ne",
            "usa_r34_se",
            "usa_r34_sw",
            "usa_r34_nw",
            "usa_r50_ne",
            "usa_r50_se",
            "usa_r50_sw",
            "usa_r50_nw",
            "usa_r64_ne",
            "usa_r64_se",
            "usa_r64_sw",
            "usa_r64_nw",
            "usa_poci",
            "usa_roci",
            "usa_rmw",
            "usa_eye",
            "tokyo_latitude",
            "tokyo_longitude",
            "tokyo_grade",
            "tokyo_wind",
            "tokyo_pressure",
            "tokyo_r50_dir",
            "tokyo_r50_longitude",
            "tokyo_r50_short",
            "tokyo_r30_dir",
            "tokyo_r30_long",
            "tokyo_r30_short",
            "tokyo_land",
            "cma_latitude",
            "cma_longitude",
            "cma_cat",
            "cma_wind",
            "cma_pressure",
            "hko_latitude",
            "hko_longitude",
            "hko_cat",
            "hko_wind",
            "hko_pressure",
            "newdelhi_latitude",
            "newdelhi_longitude",
            "newdelhi_grade",
            "newdelhi_wind",
            "newdelhi_pressure",
            "newdelhi_ci",
            "newdelhi_dp",
            "newdelhi_poci",
            "reunion_latitude",
            "reunion_longitude",
            "reunion_type",
            "reunion_wind",
            "reunion_pressure",
            "reunion_tnum",
            "reunion_ci",
            "reunion_rmw",
            "reunion_r34_ne",
            "reunion_r34_se",
            "reunion_r34_sw",
            "reunion_r34_nw",
            "reunion_r50_ne",
            "reunion_r50_se",
            "reunion_r50_sw",
            "reunion_r50_nw",
            "reunion_r64_ne",
            "reunion_r64_se",
            "reunion_r64_sw",
            "reunion_r64_nw",
            "bom_latitude",
            "bom_longitude",
            "bom_type",
            "bom_wind",
            "bom_pressure",
            "bom_tnum",
            "bom_ci",
            "bom_rmw",
            "bom_r34_ne",
            "bom_r34_se",
            "bom_r34_sw",
            "bom_r34_nw",
            "bom_r50_ne",
            "bom_r50_se",
            "bom_r50_sw",
            "bom_r50_nw",
            "bom_r64_ne",
            "bom_r64_se",
            "bom_r64_sw",
            "bom_r64_nw",
            "bom_roci",
            "bom_poci",
            "bom_eye",
            "bom_pos_method",
            "bom_pressure_method",
            "wellington_latitude",
            "wellington_longitude",
            "wellington_wind",
            "wellington_pressure",
            "nadi_latitude",
            "nadi_longitude",
            "nadi_cat",
            "nadi_wind",
            "nadi_pressure",
            "ds824_latitude",
            "ds824_longitude",
            "ds824_stage",
            "ds824_wind",
            "ds824_pressure",
            "td9636_latitude",
            "td9636_longitude",
            "td9636_stage",
            "td9636_wind",
            "td9636_pressure",
            "td9635_latitude",
            "td9635_longitude",
            "td9635_wind",
            "td9635_pressure",
            "td9635_roci",
            "neumann_latitude",
            "neumann_longitude",
            "neumann_class",
            "neumann_wind",
            "neumann_pressure",
            "mlc_latitude",
            "mlc_longitude",
            "mlc_class",
            "mlc_wind",
            "mlc_pressure",
            "usa_atcf_id",
        ]
    ]
    return df


def convert_dt_format(date_str: str, time_str: str) -> str:
    return str(datetime.datetime.strptime(date_str, "%m/%d/%Y").date()) + " " + time_str


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "lat": "latitude",
        "lon": "longitude",
        "wmo_pres": "wmo_pressure",
        "usa_lat": "usa_latitude",
        "usa_lon": "usa_longitude",
        "usa_pres": "usa_pressure",
        "tokyo_lat": "tokyo_latitude",
        "tokyo_lon": "tokyo_longitude",
        "tokyo_pres": "tokyo_pressure",
        "tokyo_r50_long": "tokyo_r50_longitude",
        "cma_lat": "cma_latitude",
        "cma_lon": "cma_longitude",
        "cma_pres": "cma_pressure",
        "hko_lat": "hko_latitude",
        "hko_lon": "hko_longitude",
        "hko_pres": "hko_pressure",
        "newdelhi_lat": "newdelhi_latitude",
        "newdelhi_lon": "newdelhi_longitude",
        "newdelhi_pres": "newdelhi_pressure",
        "reunion_lat": "reunion_latitude",
        "reunion_lon": "reunion_longitude",
        "reunion_pres": "reunion_pressure",
        "bom_lat": "bom_latitude",
        "bom_lon": "bom_longitude",
        "bom_pres": "bom_pressure",
        "bom_pres_method": "bom_pressure_method",
        "wellington_lat": "wellington_latitude",
        "wellington_lon": "wellington_longitude",
        "wellington_pres": "wellington_pressure",
        "nadi_lat": "nadi_latitude",
        "nadi_lon": "nadi_longitude",
        "nadi_pres": "nadi_pressure",
        "ds824_lat": "ds824_latitude",
        "ds824_lon": "ds824_longitude",
        "ds824_pres": "ds824_pressure",
        "td9636_lat": "td9636_latitude",
        "td9636_lon": "td9636_longitude",
        "td9636_pres": "td9636_pressure",
        "td9635_lat": "td9635_latitude",
        "td9635_lon": "td9635_longitude",
        "td9635_pres": "td9635_pressure",
        "neumann_lat": "neumann_latitude",
        "neumann_lon": "neumann_longitude",
        "neumann_pres": "neumann_pressure",
        "mlc_lat": "mlc_latitude",
        "mlc_lon": "mlc_longitude",
        "mlc_pres": "mlc_pressure",
    }

    df.rename(columns=header_names, inplace=True)


def filter_null_rows(df: pd.DataFrame) -> None:
    df = df[df.season != "Year"]


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
