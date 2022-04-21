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
from zipfile import ZipFile

import pandas as pd
from google.cloud import storage

SPEND_RANGE_COLUMNS = [
    "spend_range_max_usd",
    "spend_range_max_eur",
    "spend_range_max_inr",
    "spend_range_max_bgn",
    "spend_range_max_hrk",
    "spend_range_max_czk",
    "spend_range_max_dkk",
    "spend_range_max_huf",
    "spend_range_max_pln",
    "spend_range_max_ron",
    "spend_range_max_gbp",
    "spend_range_max_sek",
    "spend_range_max_nzd",
]

NUMERIC_COLUMNS = [
    "spend_usd",
    "spend_eur",
    "spend_inr",
    "spend_bgn",
    "spend_hrk",
    "spend_czk",
    "spend_dkk",
    "spend_huf",
    "spend_pln",
    "spend_ron",
    "spend_gbp",
    "spend_sek",
    "spend_nzd",
]


def main(
    source_bucket: str,
    source_object: str,
    zip_file: pathlib.Path,
    csv_file: str,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    table_name: str,
) -> None:

    logging.info(
        f"google political ads {table_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file gs://{source_bucket}/{source_object}")
    download_blob(source_bucket, source_object, zip_file)

    logging.info(f"Opening file {zip_file}")
    df = read_csv_file(zip_file, csv_file)

    logging.info(f"Transforming.. {csv_file}")

    logging.info(f"Transform: Rename columns for {table_name}..")
    rename_headers(df, rename_mappings)

    if table_name == "creative_stats":
        logging.info(f"Transform: converting to integer for {table_name}..")
        for col in SPEND_RANGE_COLUMNS:
            df = convert_to_int(df, col)

    logging.info(f"Transform: Reordering headers for {table_name}.. ")
    df = df[headers]

    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, str(target_file), table_name)
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        f"Google Political Ads {table_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def save_to_new_file(df: pd.DataFrame, file_path: str, table_name: str) -> None:
    if table_name != "creative_stats" and "spend_usd" in df:
        for column in NUMERIC_COLUMNS:
            df[column] = pd.to_numeric(df[column]).astype(int)
    df.to_csv(file_path, index=False, chunksize=10000)


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


def read_csv_file(source_file: pathlib.Path, source_csv_name: str) -> pd.DataFrame:
    with ZipFile(source_file) as zipfiles:
        return pd.read_csv(zipfiles.open(source_csv_name), dtype=object)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def convert_to_int(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].fillna(0)
    df[column_name] = df[column_name].astype(int)
    return df


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_bucket=os.environ["SOURCE_GCS_BUCKET"],
        source_object=os.environ["SOURCE_GCS_OBJECT"],
        zip_file=pathlib.Path(os.environ["ZIP_FILE"]).expanduser(),
        csv_file=os.environ["CSV_FILE"],
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        table_name=os.environ["TABLE_NAME"],
    )
