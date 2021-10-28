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
import os
import pathlib

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url_json: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("San Francisco - Bikeshare Status process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Extracting URL for status: {source_url_json}")
    source_file_status_json = str(source_file).replace(".csv", "") + "_status.json"

    logging.info(f"Downloading states json file {source_url_json}")
    download_file_json(source_url_json, source_file_status_json, source_file)

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=chunksz,  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("San Francisco - Bikeshare Status process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = rename_headers(df)
    df = filter_empty_data(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "data.stations.eightd_has_available_keys": "eightd_has_available_keys",
        "data.stations.is_installed": "is_installed",
        "data.stations.is_renting": "is_renting",
        "data.stations.is_returning": "is_returning",
        "data.stations.last_reported": "last_reported",
        "data.stations.num_bikes_available": "num_bikes_available",
        "data.stations.num_bikes_disabled": "num_bikes_disabled",
        "data.stations.num_docks_available": "num_docks_available",
        "data.stations.num_docks_disabled": "num_docks_disabled",
        "data.stations.num_ebikes_available": "num_ebikes_available",
        "data.stations.station_id": "station_id",
    }

    df.rename(columns=header_names, inplace=True)

    return df


def filter_empty_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Filter rows with empty key data")
    df = df[df["station_id"] != ""]
    df = df[df["num_bikes_available"] != ""]
    df = df[df["num_docks_available"] != ""]
    df = df[df["is_installed"] != ""]
    df = df[df["is_renting"] != ""]
    df = df[df["is_returning"] != ""]
    df = df[df["last_reported"] != ""]

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Re-ordering Headers")
    df = df[
        [
            "station_id",
            "num_bikes_available",
            "num_bikes_disabled",
            "num_docks_available",
            "num_docks_disabled",
            "is_installed",
            "is_renting",
            "is_returning",
            "last_reported",
            "num_ebikes_available",
            "eightd_has_available_keys",
        ]
    ]

    return df


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
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


def download_file_json(
    source_url_json: str, source_file_json: str, source_file_csv: str
) -> None:

    # This function extracts the json from a source url and creates
    # a csv file from that data to be used as an input file

    # Download json url into object r
    r = requests.get(source_url_json + ".json", stream=True)

    # Push object r (json) into json file
    try:
        with open(source_file_json, "wb") as f:
            for chunk in r:
                f.write(chunk)
    except ValueError:
        print(f"Writing JSON to {source_file_json} has failed")

    f = open(
        source_file_json.strip(),
    )
    json_data = json.load(f)
    df = pd.DataFrame(json_data["data"]["stations"])
    df.to_csv(source_file_csv, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url_json=os.environ["SOURCE_URL_JSON"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
