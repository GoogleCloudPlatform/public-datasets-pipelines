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
import json
import logging
import math
import os
import pathlib
import subprocess
import typing

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    column_name: str,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
) -> None:

    logging.info(
        f"World Bank Health Population {pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(source_file, skip_blank_lines=True)

    logging.info(f"Transforming {source_file} ... ")

    logging.info(f"Transform: Dropping column {column_name} ...")
    delete_column(df, column_name)

    logging.info(f"Transform: Renaming columns for {pipeline_name} ...")
    rename_headers(df, rename_mappings)

    if pipeline_name == "series_times":
        logging.info(f"Transform: Extracting year for {pipeline_name} ...")
        df["year"] = df["year"].apply(extract_year)
    else:
        df = df

    if pipeline_name == "country_summary":
        logging.info("Transform: Creating a new column ...")
        df["latest_water_withdrawal_data"] = ""

        logging.info("Transform: Converting to integer ... ")
        df["latest_industrial_data"] = df["latest_industrial_data"].apply(
            convert_to_integer_string
        )
        df["latest_trade_data"] = df["latest_trade_data"].apply(
            convert_to_integer_string
        )
    else:
        df = df

    logging.info(f"Transform: Reordering headers for {pipeline_name} ...")
    df = df[headers]

    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        f"World Bank Health Population {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    subprocess.check_call(["gsutil", "cp", f"{source_url}", f"{source_file}"])


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def delete_column(df: pd.DataFrame, column_name: str) -> None:
    df = df.drop(column_name, axis=1, inplace=True)


def extract_year(string_val: str) -> str:
    # string_val example: YR2021
    return string_val[2:]


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(int(round(input, 0)))
    return str_val


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
        column_name=os.environ["COLUMN_TO_REMOVE"],
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
