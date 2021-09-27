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

# CSV transform for: austin_311.311_service_request

import datetime
import logging
import os
import pathlib

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url_stations_json: str,
    source_url_status_json: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("New York Citibike - Citibike Stations process started")

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    df = download_and_merge_source_files(
        source_url_stations_json, source_url_status_json, source_file
    )
    df = clean_data_points(df)
    rename_headers(df)
    df = reorder_headers(df)

    logging.info(f"Transformation Process Starting.. {source_file}")
    df = convert_datetime_from_int(df)
    logging.info(f"Transformation Process complete .. {source_file}")

    save_to_new_file(df, file_path=str(target_file))
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("New York Citibike - Citibike Stations process completed")


def clean_data_points(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning data points - Rental Methods")
    df["rental_methods"] = df["rental_methods"].astype("string")
    df["rental_methods"] = (
        str(pd.Series(df["rental_methods"])[0])
        .replace("[", "")
        .replace("'", "")
        .replace("]", "")
    )
    logging.info("Cleaning data points - Station ID")
    df["station_id"] = df["station_id"].astype("Int64")
    df["region_id"] = df["region_id"].astype("Int64")

    logging.info("Resolving boolean datapoints")
    df["eightd_has_key_dispenser"] = df["eightd_has_key_dispenser"].apply(
        lambda x: "True" if x == "0" else "False"
    )
    df["is_installed"] = df["is_installed"].apply(
        lambda x: "True" if x == "0" else "False"
    )
    df["is_renting"] = df["is_renting"].apply(lambda x: "True" if x == "0" else "False")
    df["is_returning"] = df["is_returning"].apply(
        lambda x: "True" if x == "0" else "False"
    )

    return df


def convert_datetime_from_int(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Converting Datetime columns")
    df["last_reported"] = (
        df["last_reported"].astype(str).astype(int).apply(datetime_from_int)
    )
    return df


def download_and_merge_source_files(
    source_url_stations_json: str, source_url_status_json: str, source_file: str
) -> pd.DataFrame:

    source_file_stations_csv = str(source_file).replace(".csv", "") + "_stations.csv"
    source_file_stations_json = str(source_file).replace(".csv", "") + "_stations"
    source_file_status_csv = str(source_file).replace(".csv", "") + "_status.csv"
    source_file_status_json = str(source_file).replace(".csv", "") + "_status"

    logging.info(f"Downloading stations file {source_url_stations_json}")
    download_file_json(
        source_url_stations_json, source_file_stations_json, source_file_stations_csv
    )

    logging.info(f"Downloading status file {source_url_status_json}")
    download_file_json(
        source_url_status_json, source_file_status_json, source_file_status_csv
    )

    logging.info(f"Opening stations file {source_file_stations_csv}")
    df_stations = pd.read_csv(
        source_file_stations_csv, engine="python", encoding="utf-8", quotechar='"'
    )

    logging.info(f"Opening status file {source_file_status_csv}")
    df_status = pd.read_csv(
        source_file_status_csv, engine="python", encoding="utf-8", quotechar='"'
    )

    logging.info("Merging files")
    df = df_stations.merge(df_status, left_on="station_id", right_on="station_id")

    return df


def datetime_from_int(dt_int: int) -> str:
    return datetime.datetime.fromtimestamp(dt_int).strftime("%Y-%m-%d %H:%M:%S")


def convert_dt_format(date_str: str, time_str: str) -> str:
    return str(datetime.datetime.strptime(date_str, "%m/%d/%Y").date()) + " " + time_str


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    header_names = {
        "lat": "latitude",
        "lon": "longitude",
    }
    df.rename(columns=header_names, inplace=True)


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Re-ordering Headers")
    df = df[
        [
            "station_id",
            "name",
            "short_name",
            "latitude",
            "longitude",
            "region_id",
            "rental_methods",
            "capacity",
            "eightd_has_key_dispenser",
            "num_bikes_available",
            "num_bikes_disabled",
            "num_docks_available",
            "num_docks_disabled",
            "is_installed",
            "is_renting",
            "is_returning",
            "eightd_has_available_keys",
            "last_reported",
        ]
    ]
    return df


def save_to_new_file(df, file_path) -> None:
    logging.info(f"Saving to output file.. {file_path}")
    df.to_csv(file_path, index=False)


def download_file_json(
    source_url: str, source_file_json: pathlib.Path, source_file_csv: pathlib.Path
) -> None:
    logging.info(f"Downloading file {source_url}.json.")
    r = requests.get(source_url + ".json", stream=True)
    with open(source_file_json + ".json", "wb") as f:
        for chunk in r:
            f.write(chunk)
    df = pd.read_json(source_file_json + ".json")["data"]["stations"]
    df = pd.DataFrame(df)
    df.to_csv(source_file_csv, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info(f"Uploading output file to.. gs://{gcs_bucket}/{gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url_stations_json=os.environ["SOURCE_URL_STATIONS_JSON"],
        source_url_status_json=os.environ["SOURCE_URL_STATUS_JSON"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
