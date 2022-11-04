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

import json
import logging
import math
import os
import pathlib
import typing

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: str,
    project_id: str,
    column_name: str,
    target_file: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
) -> None:
    logging.info(f"World Bank Health Population {pipeline_name} process started")
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file_gcs(
        project_id=project_id,
        source_location=source_url,
        destination_folder=os.path.split(source_file)[0],
    )
    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(source_file, skip_blank_lines=True)
    delete_column(df, column_name)
    rename_headers(df, rename_mappings)
    if pipeline_name == "series_times":
        logging.info(f"Transform: Extracting year for {pipeline_name} ...")
        df["year"] = df["year"].apply(extract_year)
    if pipeline_name == "country_summary":
        logging.info("Transform: Converting to integer ... ")
        df["latest_industrial_data"] = df["latest_industrial_data"].apply(
            convert_to_integer_string
        )
        df["latest_trade_data"] = df["latest_trade_data"].apply(
            convert_to_integer_string
        )
    reorder_headers(df, headers)
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
    logging.info(f"World Bank Health Population {pipeline_name} process completed")


def download_file_gcs(
    project_id: str, source_location: str, destination_folder: str
) -> None:
    logging.info(
        f"Downloading file from {source_location} in project {project_id} to {destination_folder}"
    )
    object_name = os.path.basename(source_location)
    dest_object = f"{destination_folder}/{object_name}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def reorder_headers(df, headers):
    logging.info("Transform: Reordering headers")
    df = df[headers]


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Transform: Renaming columns ...")
    df.rename(columns=rename_mappings, inplace=True)


def delete_column(df: pd.DataFrame, column_name: str) -> None:
    logging.info(f"Transform: Dropping column {column_name} ...")
    df = df.drop(column_name, axis=1, inplace=True)


def extract_year(string_val: str) -> str:
    return string_val[2:]


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    logging.info("Saving to output file")
    df.to_csv(file_path, index=False)


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(int(round(input, 0)))
    return str_val


def upload_file_to_gcs(file_path: str, gcs_bucket: str, gcs_path: str) -> None:
    logging.info(f"Uploading output file to.. gs://{gcs_bucket}/{gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=os.environ.get("SOURCE_FILE", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        column_name=os.environ.get("COLUMN_TO_REMOVE", ""),
        target_file=os.environ.get("TARGET_FILE", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        headers=json.loads(os.environ.get("CSV_HEADERS", r"[]")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS", r"{}")),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
    )
