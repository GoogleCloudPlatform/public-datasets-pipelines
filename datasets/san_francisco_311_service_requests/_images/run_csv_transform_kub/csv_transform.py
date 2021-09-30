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

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("San Francisco - 311 Service Requests process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file(source_url, source_file)

    chunksz = int(chunksize)

    logging.info(f"Opening source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        sep=",",
        chunksize=chunksz,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("San Francisco - 311 Service Requests process completed")


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"downloading file {source_file} from {source_url}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = rename_headers(df)
    df = remove_empty_key_rows(df, "unique_key")
    df = resolve_datatypes(df)
    df = remove_parenthesis_long_lat(df)
    df = strip_whitespace(df)
    df = resolve_date_format(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header)
    logging.info(f"Processing batch file {target_file_batch} completed")


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Renaming headers")
    header_names = {
        "CaseID": "unique_key",
        "Opened": "created_date",
        "Closed": "closed_date",
        "Updated": "resolution_action_updated_date",
        "Status": "status",
        "Status Notes": "status_notes",
        "Responsible Agency": "agency_name",
        "Category": "category",
        "Request Type": "complaint_type",
        "Request Details": "descriptor",
        "Address": "incident_address",
        "Supervisor District": "supervisor_district",
        "Neighborhood": "neighborhood",
        "Point": "location",
        "Source": "source",
        "Media URL": "media_url",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Police District": "police_district",
    }
    df = df.rename(columns=header_names)

    return df


def remove_empty_key_rows(df: pd.DataFrame, key_field: str) -> pd.DataFrame:
    logging.info("Removing rows with empty keys")
    df = df[df[key_field] != ""]

    return df


def resolve_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving datatypes")
    df["supervisor_district"] = df["supervisor_district"].astype("Int64")

    return df


def remove_parenthesis_long_lat(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Removing parenthesis from latitude and longitude")
    df["latitude"].replace("(", "", regex=False, inplace=True)
    df["latitude"].replace(")", "", regex=False, inplace=True)
    df["longitude"].replace("(", "", regex=False, inplace=True)
    df["longitude"].replace(")", "", regex=False, inplace=True)

    return df


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Stripping whitespace")
    ws_fields = ["incident_address"]

    for ws_fld in ws_fields:
        df[ws_fld] = df[ws_fld].apply(lambda x: str(x).strip())

    return df


def resolve_date_format(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving date formats")
    date_fields = [
        "created_date",
        "closed_date",
        "resolution_action_updated_date",
    ]

    for dt_fld in date_fields:
        df[dt_fld] = df[dt_fld].apply(convert_dt_format)

    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif (
        dt_str.strip()[2] == "/"
    ):  # if there is a '/' in 3rd position, then we have a date format mm/dd/yyyy
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers")
    df = df[
        [
            "unique_key",
            "created_date",
            "closed_date",
            "resolution_action_updated_date",
            "status",
            "status_notes",
            "agency_name",
            "category",
            "complaint_type",
            "descriptor",
            "incident_address",
            "supervisor_district",
            "neighborhood",
            "location",
            "source",
            "media_url",
            "latitude",
            "longitude",
            "police_district",
        ]
    ]

    return df


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path, index=False)


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if os.path.exists(target_file_path):
        target_file = open(target_file_path, "a+")
    else:
        target_file = open(target_file_path, "w")
    if skip_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
        )
        next(data_file)
    else:
        logging.info(f"Appending batch file {batch_file_path} to {target_file_path}")
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


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
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
