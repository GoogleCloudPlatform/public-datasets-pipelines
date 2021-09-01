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
import re

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

    logging.info("Austin Bikeshare - Bikeshare Trips process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(str(source_file))

    logging.info(f"Transformation Process Starting.. {source_file}")

    logging.info(f"Transform: Renaming Headers.. {source_file}")
    rename_headers(df)

    logging.info(f"Transform: Filtering null identity records.. {source_file}")
    filter_null_rows(df)

    logging.info(f"Transform: Acquiring start_time.. {source_file}")
    df["start_time"] = df["time"] + " " + df["checkout_time"]
    df["start_time"] = df["start_time"].apply(convert_dt_format)

    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "trip_id",
            "subscriber_type",
            "bikeid",
            "start_time",
            "start_station_id",
            "start_station_name",
            "end_station_id",
            "end_station_name",
            "duration_minutes",
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

    logging.info("Austin Bikeshare - Bikeshare Trips process completed")


def convert_dt_format(dt_str: str) -> str:
    a = ""
    if dt_str is None or len(str(dt_str)) == 0 or str(dt_str) == "nan":
        return str(a)
    else:
        return str(
            datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


def rename_headers(df):
    header_names = {
        "Trip ID": "trip_id",
        "Membership Type": "subscriber_type",
        "Bicycle ID": "bikeid",
        "Checkout Date": "time",
        "Checkout Kiosk ID": "start_station_id",
        "Checkout Kiosk": "start_station_name",
        "Return Kiosk ID": "end_station_id",
        "Return Kiosk": "end_station_name",
        "Trip Duration Minutes": "duration_minutes",
        "Checkout Time": "checkout_time",
        "Month": "month",
        "Year": "year",
    }

    df.rename(columns=header_names, inplace=True)


def replace_value(val):
    if val is None or len(val) == 0:
        return val
    else:
        if val.find("\n") > 0:
            return re.sub(r"(^\d):(\d{2}:\d{2})", "0$1:$2", val)
        else:
            return val


def filter_null_rows(df):
    df = df[df.trip_id != ""]


def save_to_new_file(df, file_path):
    df.to_csv(file_path, float_format="%.0f", index=False)


def download_file(source_url: str, source_file: pathlib.Path):
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
