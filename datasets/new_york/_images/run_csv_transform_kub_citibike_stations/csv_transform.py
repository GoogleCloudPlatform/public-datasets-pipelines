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
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info(
        "New York Citibike - Citibike Stations process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    source_url_stations = source_url.split("|")[0]
    source_file_stations = str(source_file).replace(".csv", "") + "_stations.csv"
    logging.info(f"Extracting URL for stations: {source_url_stations}")

    source_url_status = source_url.split("|")[1]
    source_file_status = str(source_file).replace(".csv", "") + "_status.csv"
    logging.info(f"Extracting URL for status: {source_url_status}")

    logging.info(f"Downloading stations file {source_url_stations}")
    download_file_json(source_url_stations, source_file_stations)

    logging.info(f"Downloading stations file {source_url_status}")
    download_file_json(source_url_status, source_file_status)

    logging.info(f"Opening stations file {source_file_stations}")
    df_stations = pd.read_csv(source_file_stations)

    logging.info(f"Opening status file {source_file_status}")
    df_status = pd.read_csv(source_file_status)

    logging.info("Merging files")
    df = df_stations.merge(df_status, left_on="station_id", right_on="station_id")

    logging.info("Re-ordering Headers")
    df = df[
        [
            "station_id",
            "name",
            "short_name",
            "lat",
            "lon",
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

    logging.info("Cleaning data points - Rental Methods")
    df["rental_methods"] = df_stations["rental_methods"].astype("string")
    df["rental_methods"] = (
        str(pd.Series(df_stations["rental_methods"])[0])
        .replace("[", "")
        .replace("'", "")
        .replace("]", "")
    )

    logging.info("Resolving boolean datapoints")
    if str(df["eightd_has_key_dispenser"]) == "0":
        df["eightd_has_key_dispenser"] = "false"
    else:
        df["eightd_has_key_dispenser"] = "true"
    if str(df["is_installed"]) == "0":
        df["is_installed"] = "false"
    else:
        df["is_installed"] = "true"
    if str(df["is_renting"]) == "0":
        df["is_renting"] = "false"
    else:
        df["is_renting"] = "true"
    if str(df["is_returning"]) == "0":
        df["is_returning"] = "false"
    else:
        df["is_returning"] = "true"

    logging.info(f"Transformation Process Starting.. {source_file}")

    logging.info("Converting Datetime")
    df["last_reported"] = (
        df["last_reported"].astype(str).astype(int).apply(datetime_from_int)
    )

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

    logging.info(
        "New York Citibike - Citibike Stations process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def datetime_from_int(dt_int: int) -> str:
    return datetime.datetime.fromtimestamp(dt_int).strftime("%Y-%m-%d %H:%M:%S")


def convert_dt_format(date_str: str, time_str: str) -> str:
    return str(datetime.datetime.strptime(date_str, "%m/%d/%Y").date()) + " " + time_str


def rename_headers(df) -> None:
    header_names = {
        "lat": "latitude",
        "lon": "longitude",
    }

    for old_name, new_name in header_names.items():
        df.rename(old_name, new_name)


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, float_format="%.0f", index=False)


def download_file_json(source_url: str, source_file: pathlib.Path) -> None:

    # this function extracts the json from a source url and creates
    # a csv file from that data to be used as an input file

    # download json url into object r
    try:
        logging.info(f"Downloading {source_url} into {source_file}.json")
        r = requests.get(source_url, stream=True)
        if r.status_code != 200:
            logging.error(f"Couldn't download {source_url}: {r.text}")
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print(f"Downloading JSON file {source_url} has failed {r.text}")

    # # push object r (json) into json file
    source_file_json = str(source_file) + ".json"
    try:
        with open(source_file_json, "wb") as f:
            for chunk in r:
                f.write(chunk)
    except ValueError:
        print(f"Writing JSON to {source_file} has failed")

    # read json file into object and write out to csv
    df = pd.read_json(source_file_json)["data"]["stations"]

    # convert df [list] to df [DataFrame]
    df = pd.DataFrame(df)

    df.to_csv(source_file, index=False)


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
