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

# import modules
import logging
import os
import pathlib
from subprocess import PIPE, Popen

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("Sunroof Solar Potential By Postal Code process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file from {source_url} to {source_file}")
    download_file_gs(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(source_file)

    logging.info(f"Transformation Process Starting.. {source_file}")

    logging.info(f"Transform: Renaming Headers.. {source_file}")
    rename_headers(df)

    logging.info("Transform: Removing NULL text")
    remove_nan_cols(df)

    logging.info("Transform: Adding geography field")
    df["center_point"] = (
        "POINT( " + df["lng_avg"].map(str) + " " + df["lat_avg"].map(str) + " )"
    )

    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "region_name",
            "state_name",
            "lat_max",
            "lat_min",
            "lng_max",
            "lng_min",
            "lat_avg",
            "lng_avg",
            "yearly_sunlight_kwh_kw_threshold_avg",
            "count_qualified",
            "percent_covered",
            "percent_qualified",
            "number_of_panels_n",
            "number_of_panels_s",
            "number_of_panels_e",
            "number_of_panels_w",
            "number_of_panels_f",
            "number_of_panels_median",
            "number_of_panels_total",
            "kw_median",
            "kw_total",
            "yearly_sunlight_kwh_n",
            "yearly_sunlight_kwh_s",
            "yearly_sunlight_kwh_e",
            "yearly_sunlight_kwh_w",
            "yearly_sunlight_kwh_f",
            "yearly_sunlight_kwh_median",
            "yearly_sunlight_kwh_total",
            "install_size_kw_buckets",
            "carbon_offset_metric_tons",
            "existing_installs_count",
        ]
    ]

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

    logging.info("Sunroof Solar Potential By Postal Code process completed")


def remove_nan(dt_str: str) -> int:
    if dt_str is None or len(str(dt_str)) == 0 or str(dt_str) == "nan":
        return int()
    else:
        return int(dt_str)


def remove_nan_cols(df: pd.DataFrame) -> None:
    cols = {
        "count_qualified",
        "existing_installs_count",
        "number_of_panels_n",
        "number_of_panels_s",
        "number_of_panels_e",
        "number_of_panels_w",
        "number_of_panels_f",
        "number_of_panels_median",
        "number_of_panels_total",
    }

    for col in cols:
        df[col] = df[col].apply(remove_nan)


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {"install_size_kw_buckets_json": "install_size_kw_buckets"}

    df = df.rename(columns=header_names, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path, index=False)


def download_file_gs(source_url: str, source_file: pathlib.Path) -> None:
    try:
        process = Popen(
            ["gsutil", "cp", source_url, source_file], stdout=PIPE, stderr=PIPE
        )
        process.communicate()
    except ValueError:
        logging.error(f"Couldn't download {source_url}: {ValueError}")


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
