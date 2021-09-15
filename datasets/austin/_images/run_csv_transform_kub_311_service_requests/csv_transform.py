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
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("Austin 311 Service Requests By Year process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file, engine="python", encoding="utf-8", quotechar='"', chunksize=chunksz
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            processChunk(df, target_file_batch)
            logging.info(f"Appending batch {chunk_number} to {target_file}")
            if chunk_number == 0:
                subprocess.run(["cp", target_file_batch, target_file])
            else:
                subprocess.check_call(f"sed -i '1d' {target_file_batch}", shell=True)
                subprocess.check_call(
                    f"cat {target_file_batch} >> {target_file}", shell=True
                )
            subprocess.run(["rm", target_file_batch])

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("Austin 311 Service Requests By Year process completed")


def processChunk(df: pd.DataFrame, target_file_batch: str) -> None:

    logging.info("Transforming.")
    rename_headers(df)
    convert_values(df)
    delete_newlines_from_column(df, col_name="location")
    filter_null_rows(df)

    logging.info("Saving to target file.. {target_file_batch}")

    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving to target file: {e}.")

    logging.info(f"Saved transformed source data to target file .. {target_file_batch}")


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "Service Request (SR) Number": "unique_key",
        "SR Type Code": "complaint_type",
        "SR Description": "complaint_description",
        "Owning Department": "owning_department",
        "Method Received": "source",
        "SR Status": "status",
        "Status Change Date": "status_change_date",
        "Created Date": "created_date",
        "Last Update Date": "last_update_date",
        "Close Date": "close_date",
        "SR Location": "incident_address",
        "Street Number": "street_number",
        "Street Name": "street_name",
        "City": "city",
        "Zip Code": "incident_zip",
        "County": "county",
        "State Plane X Coordinate": "state_plane_x_coordinate",
        "State Plane Y Coordinate": "state_plane_y_coordinate",
        "Latitude Coordinate": "latitude",
        "Longitude Coordinate": "longitude",
        "(Latitude.Longitude)": "location",
        "Council District": "council_district_code",
        "Map Page": "map_page",
        "Map Tile": "map_tile",
    }

    for old_name, new_name in header_names.items():
        df.rename(old_name, new_name)


def convert_dt_format(dt_str: str) -> str:
    # if the format is %m/%d/%Y then...
    if str(dt_str).strip()[3] == "/":
        return datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    else:
        return str(dt_str)


def convert_values(df: pd.DataFrame) -> None:
    dt_cols = [
        "status_change_date",
        "created_date",
        "last_update_date",
        "close_date",
    ]

    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)

    int_cols = ["council_district_code"]
    for int_col in int_cols:
        df[int_col] = df[int_col].astype("int32")


def delete_newlines(val: str) -> str:
    return val.replace("\n", "")


def delete_newlines_from_column(df: pd.DataFrame, col_name: str) -> None:
    if df[col_name] is not None & df[col_name].str.len() > 0:
        df[col_name] = df[col_name].apply(delete_newlines)


def filter_null_rows(df: pd.DataFrame) -> None:
    df = df[df.unique_key != ""]


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.export_csv(file_path)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
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
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
