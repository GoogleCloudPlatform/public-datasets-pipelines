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
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("New York Citibike - Citibike Stations process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_and_merge_source_files(
        source_url_stations_json, source_url_status_json, source_file
    )

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

    logging.info("New York Citibike - Citibike Stations process completed")


def download_and_merge_source_files(
    source_url_stations_json: str, source_url_status_json: str, source_file: str
) -> None:

    source_file_stations_csv = str(source_file).replace(".csv", "") + "_stations.csv"
    source_file_stations_json = str(source_file).replace(".csv", "") + "_stations"
    source_file_status_csv = str(source_file).replace(".csv", "") + "_status.csv"
    source_file_status_json = str(source_file).replace(".csv", "") + "_status"

    download_file_json(
        source_url_stations_json, source_file_stations_json, source_file_stations_csv
    )

    download_file_json(
        source_url_status_json, source_file_status_json, source_file_status_csv
    )

    df_stations = pd.read_csv(
        source_file_stations_csv, engine="python", encoding="utf-8", quotechar='"'
    )

    df_status = pd.read_csv(
        source_file_status_csv, engine="python", encoding="utf-8", quotechar='"'
    )

    logging.info("Merging files")
    df = df_stations.merge(df_status, left_on="station_id", right_on="station_id")

    save_to_new_file(df, source_file)


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


def save_to_new_file(df, file_path) -> None:
    logging.info(f"Saving to output file.. {file_path}")
    df.to_csv(file_path, index=False)


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = convert_datetime_from_int(df)
    df = clean_data_points(df)
    df = rename_headers(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def convert_datetime_from_int(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Converting Datetime columns")
    columns = ["last_reported"]

    for column in columns:
        df[column] = df[column].astype(str).astype(int).apply(datetime_from_int)
    return df


def datetime_from_int(dt_int: int) -> str:
    return datetime.datetime.fromtimestamp(dt_int).strftime("%Y-%m-%d %H:%M:%S")


def clean_data_points(df: pd.DataFrame) -> pd.DataFrame:
    df = resolve_datatypes(df)
    df = normalize_data_list(df)
    df = resolve_boolean_datapoints(df)

    return df


def resolve_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving datatypes")
    columns = {"station_id": "Int64", "region_id": "Int64", "rental_methods": "string"}

    for column, datatype in columns.items():
        df[column] = df[column].astype(datatype)

    return df


def normalize_data_list(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Normalizing data lists")
    columns = ["rental_methods"]

    for column in columns:
        df[column] = (
            str(pd.Series(df[column])[0])
            .replace("[", "")
            .replace("'", "")
            .replace("]", "")
        )

    return df


def resolve_boolean_datapoints(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving boolean datapoints")
    columns = ["eightd_has_key_dispenser", "is_installed", "is_renting", "is_returning"]

    for column in columns:
        df[column] = df[column].apply(lambda x: "True" if x == "0" else "False")

    return df


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    header_names = {
        "lat": "latitude",
        "lon": "longitude",
    }
    df.rename(columns=header_names, inplace=True)

    return df


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
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
