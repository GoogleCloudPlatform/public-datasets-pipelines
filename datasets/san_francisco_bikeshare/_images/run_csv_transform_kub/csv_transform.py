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
import typing

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
    transform_list: list,
    logging_english_name: str,
    json_node_name: str,
    rename_headers_list: dict,
    filter_rows_list: typing.List[str],
    geom_field_list: typing.List[typing.List],
    field_type_list: typing.List[typing.List],
    reorder_headers_list: typing.List[str],
) -> None:

    logging.info(f"{logging_english_name} started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    source_file_stations_json = (
        str(source_file).replace(".csv", "") + f"_{json_node_name}.json"
    )
    download_file_json(
        source_url_json, source_file_stations_json, source_file, json_node_name
    )

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
            process_chunk(
                df,
                target_file_batch,
                target_file,
                (not chunk_number == 0),
                transform_list,
                rename_headers_list,
                filter_rows_list,
                geom_field_list,
                field_type_list,
                reorder_headers_list,
            )

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(f"{logging_english_name} completed")


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    transform_list: list,
    rename_headers_list: dict,
    filter_rows_list: list,
    geom_field_list: list,
    field_type_list: list,
    reorder_headers_list: list,
) -> None:
    for transform in transform_list:
        if transform == "rename_headers":
            df = rename_headers(df, rename_headers_list)
        elif transform == "filter_empty_data":
            df = filter_empty_data(df, filter_rows_list)
        elif transform == "generate_location":
            df = generate_location(df, geom_field_list)
        elif transform == "resolve_datatypes":
            df = resolve_datatypes(df, field_type_list)
        elif transform == "reorder_headers":
            df = reorder_headers(df, reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def rename_headers(df: pd.DataFrame, header_list: dict) -> None:
    logging.info("Renaming Headers")
    header_names = header_list
    df.rename(columns=header_names)

    return df


def filter_empty_data(df: pd.DataFrame, filter_rows_list: list) -> pd.DataFrame:
    for column in filter_rows_list:
        logging.info(f"Remove rows with empty {column} data")
        df = df[df[column] != ""]

    return df


def generate_location(df: pd.DataFrame, geom_field_list: list) -> pd.DataFrame:
    logging.info("Generating location data")
    for columns in geom_field_list:
        column = columns[0]
        longitude = columns[1]
        latitude = columns[2]
        df[column] = (
            "POINT("
            + df[longitude][:].astype("string")
            + " "
            + df[latitude][:].astype("string")
            + ")"
        )

    return df


def resolve_datatypes(df: pd.DataFrame, field_type_list: list) -> pd.DataFrame:
    logging.info("Resolving datatypes")
    for columns in field_type_list:
        column = columns[0]
        datatype = columns[1]
        df[column] = df[column].astype(datatype)

    return df


def reorder_headers(df: pd.DataFrame, headers_list: list) -> pd.DataFrame:
    logging.info("Reordering Headers")
    df = df[headers_list]

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


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


def download_file_json(
    source_url_json: str,
    source_file_json: str,
    source_file_csv: str,
    json_node_name: str,
) -> None:

    # this function extracts the json from a source url and creates
    # a csv file from that data to be used as an input file
    logging.info(f"Downloading stations json file {source_url_json}")

    # download json url into object r
    r = requests.get(source_url_json + ".json", stream=True)

    # push object r (json) into json file
    with open(source_file_json, "wb") as f:
        for chunk in r:
            f.write(chunk)

    f = open(
        source_file_json.strip(),
    )
    json_data = json.load(f)
    df = pd.DataFrame(json_data["data"][json_node_name])
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
        transform_list=json.loads(os.environ["TRANSFORM_LIST"]),
        logging_english_name=os.environ["LOGGING_ENGLISH_NAME"],
        json_node_name=os.environ["JSON_NODE_NAME"],
        rename_headers_list=json.loads(os.environ["RENAME_HEADERS"]),
        filter_rows_list=json.loads(os.environ["FILTER_ROWS_LIST"]),
        geom_field_list=json.loads(os.environ["GEOM_FIELD_LIST"]),
        field_type_list=json.loads(os.environ["FIELD_TYPE_LIST"]),
        reorder_headers_list=json.loads(os.environ["REORDER_HEADERS"]),
    )
