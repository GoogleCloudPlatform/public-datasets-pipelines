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
import typing

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    pipeline_name: str,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    remove_source_file: str,
    delete_target_file: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    rename_mappings: dict
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        pipeline_name=pipeline_name,
        chunksize=chunksize,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        drop_dest_table=drop_dest_table,
        input_field_delimiter=input_field_delimiter,
        remove_source_file=remove_source_file,
        delete_target_file=delete_target_file,
        input_csv_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        rename_mappings=rename_mappings
    )
    logging.info(f"{pipeline_name} process completed")

def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    pipeline_name: str,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    remove_source_file: str,
    delete_target_file: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    rename_mappings: dict
)

    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}...")
    df = pd.read_csv(str(source_file))

    logging.info(f"Transforming {source_file}... ")

    logging.info(f"Transform: Rename columns.. {source_file}")
    rename_headers(df, rename_mappings)

    logging.info(f"Transform: Converting to integer {source_file}... ")
    convert_values_to_integer_string(df)

    logging.info("Transform: Reordering headers..")
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



# def convert_to_integer_string(input: typing.Union[str, float]) -> str:
#     str_val = ""
#     if not input or (math.isnan(input)):
#         str_val = ""
#     else:
#         str_val = str(int(round(input, 0)))
#     return str_val


# def convert_values_to_integer_string(df: pd.DataFrame) -> None:
#     cols = [
#         "retail_and_recreation_percent_change_from_baseline",
#         "grocery_and_pharmacy_percent_change_from_baseline",
#         "parks_percent_change_from_baseline",
#         "transit_stations_percent_change_from_baseline",
#         "workplaces_percent_change_from_baseline",
#         "residential_percent_change_from_baseline",
#     ]

#     for cols in cols:
#         df[cols] = df[cols].apply(convert_to_integer_string)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


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
        pipeline_name=os.environ["PIPELINE_NAME"],
        chunksize=os.environ["CHUNKSIZE"],
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        schema_path=os.environ["SCHEMA_PATH"],
        drop_dest_table=os.environ["DROP_DEST_TABLE"],
        input_field_delimiter=os.environ["INPUT_FIELD_DELIMITER"],
        remove_source_file=os.environ["REMOVE_SOURCE_FILE"],
        delete_target_file=os.environ["DELETE_TARGET_FILE"],
        input_csv_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"])
    )
