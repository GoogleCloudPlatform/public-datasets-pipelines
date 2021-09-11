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
from shutil import copyfile

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

    logging.info(f"San Francisco Bikeshare Stations process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    logging.info("creating 'templates' folder")
    pathlib.Path("./templates").mkdir(parents=True, exist_ok=True)

    logging.info(f"Extracting URL for stations: {source_url}")
    source_file_stations_csv = str(source_file).replace(".csv", "") + "_stations.csv"
    source_file_stations_json = str(source_file).replace(".csv", "") + "_stations.json"

    logging.info(f"Downloading stations json file {source_url}")
    download_file_json(
        source_url, source_file_stations_json, source_file_stations_csv
    )
    copyfile(source_file_stations_json, "./templates/bikeshare_stations.json")

    logging.info(f"Opening stations file {source_file_stations_csv}")
    df = pd.read_csv(source_file_stations_csv)

    logging.info(f"Transformation Process Starting.. {source_file}")

    logging.info(f"Renaming Columns {source_file_stations_csv}")
    rename_headers(df)

    df = df[ df["station_id"] != "" ]
    df = df[ df["name"] != "" ]
    df = df[ df["lat"] != "" ]
    df = df[ df["lon"] != "" ]

    df["station_geom"] = (
        "POINT("
        + df["lon"][:].astype("string")
        + " "
        + df["lat"][:].astype("string")
        + ")"
    )

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
            "external_id",
            "eightd_has_key_dispenser",
            "has_kiosk",
            "station_geom"
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

    logging.info(f"San Francisco Bikeshare Stations process completed")


def datetime_from_int(dt_int: int) -> str:
    return datetime.datetime.fromtimestamp(dt_int).strftime("%Y-%m-%d %H:%M:%S")


def convert_dt_format(date_str: str, time_str: str) -> str:
    return str(datetime.datetime.strptime(date_str, "%m/%d/%Y").date()) + " " + time_str


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "data.stations.station_id": "station_id",
        "data.stations.name": "name",
        "data.stations.short_name": "short_name",
        "data.stations.lat": "lat",
        "data.stations.lon": "lon",
        "data.stations.region_id": "region_id",
        "data.stations.rental_methods": "rental_methods",
        "data.stations.capacity": "capacity",
        "data.stations.eightd_has_key_dispenser": "eightd_has_key_dispenser",
        "data.stations.has_kiosk": "has_kiosk",
        "data.stations.external_id": "external_id",
    }

    df.rename(columns=header_names, inplace=True)

def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


def download_file_json(
    source_url: str, source_file_json: pathlib.Path, source_file_csv: pathlib.Path
) -> None:

    # this function extracts the json from a source url and creates
    # a csv file from that data to be used as an input file

    # download json url into object r
    try:
        r = requests.get(source_url, stream=True)
        if r.status_code != 200:
            logging.error(f"Couldn't download {source_url}: {r.text}")
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print(f"Downloading JSON file {source_url} has failed {r.text}")

    # push object r (json) into json file
    try:
        with open(source_file_json, "wb") as f:
            for chunk in r:
                f.write(chunk)
    except ValueError:
        print(f"Writing JSON to {source_file_json} has failed")

    # read json file into object and write out to csv
    df = pd.read_json(source_file_json)["data"]["stations"]
    df = pd.DataFrame(df)
    df.to_csv(source_file_csv, index=False)


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
