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
import math
import os
import pathlib
import typing
from datetime import datetime

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
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
    integer_string_col: typing.List[str],
) -> None:

    logging.info("New York taxi trips - green trips process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    # download_file(source_url, source_file)

    logging.info(f"Reading csv file {source_url}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        # compression="csv",
        chunksize=int(chunksize),
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
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
                headers,
                rename_mappings,
                pipeline_name,
                integer_string_col,
            )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
    logging.info("New York taxi trips - green trips process completed")


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
    integer_string_col: typing.List[str],
) -> None:
    logging.info(f"Processing Batch {target_file_batch}")
    df = rename_headers(df, rename_mappings)
    df = remove_null_rows(df)
    if pipeline_name == "tlc_green_trips_2018":
        df["distance_between_service"] = ""
        df["time_between_service"] = ""
        df = format_date_time(df, "pickup_datetime", "strptime", "%m/%d/%Y %I:%M:%S %p")
        df = format_date_time(
            df, "dropoff_datetime", "strptime", "%m/%d/%Y %I:%M:%S %p"
        )
    df = format_date_time(df, "pickup_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = format_date_time(df, "dropoff_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    convert_values_to_integer_string(df, integer_string_col)
    df = df[headers]
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info("..Done!")


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


def format_date_time(
    df: pd.DataFrame, field_name: str, str_pf_time: str, dt_format: str
) -> pd.DataFrame:
    if str_pf_time == "strptime":
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from datetime to {dt_format}  "
        )
        df[field_name] = df[field_name].apply(lambda x: datetime.strptime(x, dt_format))
    else:
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from {dt_format} to datetime "
        )
        df[field_name] = df[field_name].apply(lambda x: x.strftime(dt_format))
    return df


def remove_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Transform: Removing Null rows... ")
    df = df.dropna(axis=0, subset=["vendor_id"])
    return df


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info(" Renaming headers...")
    df = df.rename(columns=rename_mappings, inplace=True)
    return df


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    if not input or (math.isnan(input)):
        return ""
    return str(int(round(input, 0)))


def convert_values_to_integer_string(
    df: pd.DataFrame, integer_string_col: typing.List
) -> None:
    logging.info("Transform: Converting to integers..")
    for cols in integer_string_col:
        df[cols] = df[cols].apply(convert_to_integer_string)
    return df


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
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


def upload_file_to_gcs(
    file_path: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
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
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        integer_string_col=json.loads(os.environ["INTEGER_STRING_COL"]),
    )
