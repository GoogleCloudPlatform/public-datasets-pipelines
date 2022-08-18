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
import json
import logging
import os
import pathlib
import typing

import pandas as pd
from google.cloud import storage


def main(
    source_bucket: str,
    source_object: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    table_name: str,
) -> None:

    logging.info(
        f"FEC {table_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file gs://{source_bucket}/{source_object}")
    download_blob(source_bucket, source_object, source_file)

    logging.info(f"Opening file...{source_file}")
    df = read_csv_file(source_file)

    logging.info(f"Transforming.. {source_file}")

    logging.info(f"Transform: Rename columns for {table_name}..")
    rename_headers(df, rename_mappings)

    df["transaction_dt"] = df["transaction_dt"].astype(str)
    date_for_length(df, "transaction_dt")
    df = resolve_date_format(df, "transaction_dt")
    df = df.rename(columns=lambda x: x.strip())

    logging.info(f"Transform: Reordering headers for {table_name}.. ")
    df = df[headers]

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
        f"FEC {table_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def date_for_length(df: pd.DataFrame, field_name: str):
    date_list = df[field_name].values
    new_date_list = []
    for item in date_list:
        if item != "NaN":
            if len(item) == 7:
                item = "0" + item
                new_date_list.append(item)
            elif len(item) == 6:
                item = "0" + item[0:1] + "0" + item[1:]
                new_date_list.append(item)
            else:
                new_date_list.append(item)
                continue
        else:
            new_date_list.append(item)
    df[field_name] = new_date_list
    return df[field_name]


def resolve_date_format(
    df: pd.DataFrame,
    field_name: str,
) -> pd.DataFrame:
    logging.info("Resolving date formats")
    df[field_name] = df[field_name].apply(convert_dt_format)
    return df


def convert_dt_format(dt_str: str) -> str:
    if (
        not dt_str
        or str(dt_str).lower() == "nan"
        or str(dt_str).lower() == "nat"
        or dt_str == "-"
    ):
        return ""
    else:
        return str(
            datetime.datetime.strftime(
                datetime.datetime.strptime(dt_str, "%m%d%Y"), "%Y-%m-%d"
            )
        )


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path, chunk_size=1000 * pow(2, 18))
    blob.upload_from_filename(file_path)


def download_blob(bucket, object, target_file):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(object)
    blob.download_to_filename(target_file)


def read_csv_file(source_file: pathlib.Path) -> pd.DataFrame:
    return pd.read_table(source_file, dtype=object, index_col=False)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_bucket=os.environ["SOURCE_GCS_BUCKET"],
        source_object=os.environ["SOURCE_GCS_OBJECT"],
        source_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        table_name=os.environ["TABLE_NAME"],
    )
