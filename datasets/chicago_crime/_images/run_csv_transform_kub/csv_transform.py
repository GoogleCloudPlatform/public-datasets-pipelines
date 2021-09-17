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
) -> None:

    logging.info(
        "chicago crime process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(source_file)

    logging.info(f"Transforming {source_file} ...")

    logging.info(f"Transform: Rename columns {source_file} ...")
    rename_headers(df)

    logging.info("Transform: Converting date format.. ")
    convert_values(df)

    logging.info("Transform: Removing null values.. ")
    filter_null_rows(df)

    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "unique_key",
            "case_number",
            "date",
            "block",
            "iucr",
            "primary_type",
            "description",
            "location_description",
            "arrest",
            "domestic",
            "beat",
            "district",
            "ward",
            "community_area",
            "fbi_code",
            "x_coordinate",
            "y_coordinate",
            "year",
            "updated_on",
            "latitude",
            "longitude",
            "location",
        ]
    ]

    logging.info("Transform: converting to integers..")

    # df["unique_key"] = df["unique_key"].apply(convert_to_integer_string)
    # df["beat"] = df["beat"].apply(convert_to_integer_string)
    # df["district"] = df["district"].apply(convert_to_integer_string)
    # df["ward"] = df["ward"].apply(convert_to_integer_string)
    # df["community_area"] = df["community_area"].apply(convert_to_integer_string)
    # df["year"] = df["year"].apply(convert_to_integer_string)

    convert_values_to_integer_string(df)

    logging.info("Transform: converting to float..")

    # df["x_coordinate"] = df["x_coordinate"].apply(resolve_nan)
    # df["y_coordinate"] = df["y_coordinate"].apply(resolve_nan)
    # df["latitude"] = df["latitude"].apply(resolve_nan)
    # df["longitude"] = df["longitude"].apply(resolve_nan)

    removing_nan_values(df)

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
        "Chicago crime process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def resolve_nan(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(input)
    return str_val.replace("None", "")


def removing_nan_values(df: pd.DataFrame) -> None:
    cols = ["x_coordinate", "y_coordinate", "latitude", "longitude"]

    for cols in cols:
        df[cols] = df[cols].apply(convert_dt_format)


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(int(round(input, 0)))
    return str_val


def convert_values_to_integer_string(df: pd.DataFrame) -> None:
    cols = ["unique_key", "beat", "district", "ward", "community_area", "year"]

    for cols in cols:
        df[cols] = df[cols].apply(convert_dt_format)


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "ID": "unique_key",
        "Case Number": "case_number",
        "Date": "date",
        "Block": "block",
        "IUCR": "iucr",
        "Primary Type": "primary_type",
        "Description": "description",
        "Location Description": "location_description",
        "Arrest": "arrest",
        "Domestic": "domestic",
        "Beat": "beat",
        "District": "district",
        "Ward": "ward",
        "Community Area": "community_area",
        "FBI Code": "fbi_code",
        "X Coordinate": "x_coordinate",
        "Y Coordinate": "y_coordinate",
        "Year": "year",
        "Updated On": "updated_on",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Location": "location",
    }

    df.rename(columns=header_names, inplace=True)


def convert_dt_format(dt_str: str) -> str:
    # Old format: MM/dd/yyyy hh:mm:ss aa
    # New format: yyyy-MM-dd HH:mm:ss
    if dt_str is None or len(dt_str) == 0:
        return dt_str
    else:
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )


def convert_values(df: pd.DataFrame) -> None:
    dt_cols = ["date", "updated_on"]

    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)


def filter_null_rows(df: pd.DataFrame) -> None:
    df = df[df.unique_key != ""]


def save_to_new_file(df: pd.DataFrame, file_path: pathlib.Path) -> None:
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
    )
