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
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
    integer_string_col: typing.List[str],
) -> None:

    logging.info(
        f"New York trees{pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file from {source_url}...")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}...")
    df = pd.read_csv(str(source_file))

    logging.info(f"Transforming {source_file}... ")

    logging.info("Transform: Rename columns... ")
    rename_headers(df, rename_mappings)

    if pipeline_name == "tree_census_2005":
        logging.info("Transform: Trimming white spaces in headers... ")
        df = df.rename(columns=lambda x: x.strip())
    else:
        df = format_date_time(df, "created_at", "strptime", "%m/%d/%Y")
        df = format_date_time(df, "created_at", "strftime", "%Y-%m-%d")

    convert_values_to_integer_string(df, integer_string_col)

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

    logging.info(
        f"New York trees {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def format_date_time(
    df: pd.DataFrame, field_name: str, str_pf_time: str, dt_format: str
) -> pd.DataFrame:
    if str_pf_time == "strptime":
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from datetime to {dt_format}  "
        )
        df[field_name] = df[field_name].apply(
            lambda x: datetime.datetime.strptime(x, dt_format)
        )
    else:
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from {dt_format} to datetime "
        )
        df[field_name] = df[field_name].apply(
            lambda x: datetime.datetime.strftime(x, dt_format)
        )
    return df


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    if not input or (math.isnan(input)):
        return ""
    else:
        return str(int(round(input, 0)))


def convert_values_to_integer_string(
    df: pd.DataFrame, integer_string_col: typing.List
) -> None:
    logging.info("Transform: Converting to integers..")
    for cols in integer_string_col:
        df[cols] = df[cols].apply(convert_to_integer_string)


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
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        integer_string_col=json.loads(os.environ["INTEGER_STRING_COL"]),
    )
