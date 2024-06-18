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
import math
import os
import pathlib

import pandas as pd
import requests
from google.cloud import storage


def main(
    pipeline: str,
    source_url: str,
    source_file: str,
    gcs_bucket: str,
    csv_gcs_path: str,
    source_object_folder: str,
    rename_mappings: dict,
    non_na_columns: list,
    output_object_folder: str,
    data_types: dict,
    date_cols: list,
    batch_count: int,
) -> None:
    logging.info(
        f'Chicago Taxi Trips Dataset pipeline process started at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )
    logging.info(
        f"Creating './files', './source' & './output' folder under pwd - {os.getcwd()}"
    )
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    pathlib.Path("./source").mkdir(parents=True, exist_ok=True)
    pathlib.Path("./output").mkdir(parents=True, exist_ok=True)
    if pipeline:
        logging.info(f"Pipeline = {pipeline} process started")
        download_file(source_url, source_file)
        upload_file_to_gcs(source_file, gcs_bucket, csv_gcs_path)
        logging.info(
            f"Chicago Taxi Trips Dataset pipeline {pipeline} process completed at "
            + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        return
    logging.info(f"Reading list of files in gs://{gcs_bucket}/{source_object_folder}/*")
    storage_client = storage.Client(gcs_bucket)
    blobs = storage_client.list_blobs(
        bucket_or_name=gcs_bucket, prefix=str(source_object_folder) + "/"
    )
    blobs = [blob for blob in blobs if not blob.name.endswith("/")]
    batch_size = math.ceil(len(blobs) / 6)
    start, stop = batch_size * (batch_count - 1), batch_size * batch_count
    logging.info(
        f"bathch_count = {batch_count}, batch_size = {batch_size}, start= {start}, stop= {stop - 1} Inclusive"
    )
    logging.info(
        f"\t\t\t\tBatch-{batch_count} files list for processing\n {[blob.name for blob in blobs[start:stop]]}"
    )
    for blob in blobs[start:stop]:
        source_gcs_object = blob.name
        file_name = source_gcs_object.split("/")[-1]
        target_file = f"./source/{file_name}"
        download_blob(gcs_bucket, source_gcs_object, target_file)
        file_count = target_file.split("_")[-1]
        output_file = f"./output/data_output_{file_count}.csv"
        chunk_process(
            target_file,
            data_types,
            date_cols,
            rename_mappings,
            non_na_columns,
            output_file,
        )
        target_gcs_path = f"{output_object_folder}/{output_file.split('/')[-1]}"
        upload_file_to_gcs(output_file, gcs_bucket, target_gcs_path)
        logging.info(f"Removing {output_file} file")
        os.remove(output_file)
    logging.info(
        f'Chicago Taxi Trips Dataset pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


def download_file(source_url: str, source_file: str) -> None:
    logging.info(f"Downloading data from {source_url} to {source_file} .")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for idx, chunk in enumerate(res):
                fb.write(chunk)
                if not idx % 10000000:
                    file_size = os.stat(source_file).st_size / (1024**3)
                    logging.info(
                        f"\t{idx} chunks of data downloaded & current file size is {file_size} GB"
                    )
    else:
        logging.info(f"Couldn't download {source_url}: {res.text}")
    logging.info(
        f"Successfully downloaded data from {source_url} into {source_file} - {os.stat(source_file).st_size / (1024 ** 3)} GB"
    )


def download_blob(gcs_bucket: str, source_gcs_object: str, target_file: str) -> None:
    """Downloads a blob from the bucket."""
    logging.info(
        f"Downloading data from gs://{gcs_bucket}/{source_gcs_object} to {target_file} ..."
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(source_gcs_object)
    blob.download_to_filename(target_file)
    logging.info("Downloading Completed.")


def chunk_process(
    target_file: str,
    data_types: dict,
    date_cols: list,
    rename_mappings: dict,
    non_na_columns: list,
    output_file: str,
) -> None:
    logging.info(f"Process started for {output_file} file")
    logging.info(f"Reading file {target_file} to pandas dataframe...")
    chunks = pd.read_csv(
        target_file,
        chunksize=500000,
        dtype=data_types,
        parse_dates=date_cols,
        dayfirst=False,
    )
    logging.info(f"Removing {target_file} file")
    os.remove(target_file)
    for idx, chunk in enumerate(chunks):
        logging.info("\tRenaming headers")
        rename_headers(chunk, rename_mappings)
        logging.info(
            f"\tDropping null rows from specified columns in list = {non_na_columns}"
        )
        drop_null_rows(chunk, non_na_columns)
        if not idx:
            logging.info(f"\tWriting data to output file = {output_file}")
            chunk.to_csv(output_file, mode="w", index=False, header=True)
        else:
            logging.info(f"\tAppending data to output file = {output_file}")
            chunk.to_csv(output_file, mode="a", index=False, header=False)
    logging.info(f"Process completed for {output_file} file")


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def drop_null_rows(df: pd.DataFrame, null_columns: list) -> None:
    df.dropna(subset=null_columns, inplace=True)


def upload_file_to_gcs(
    target_csv_file: str, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_csv_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        pipeline=os.environ.get("PIPELINE", ""),
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=os.environ.get("SOURCE_FILE", ""),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        csv_gcs_path=os.environ.get("CSV_GCS_PATH", ""),
        source_object_folder=os.environ.get("SOURCE_OBJECT_FOLDER", ""),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS", "{}")),
        non_na_columns=json.loads(os.environ.get("NON_NA_COLUMNS", "[]")),
        output_object_folder=os.environ.get("OUTPUT_OBJECT_FOLDER", ""),
        data_types=json.loads(os.environ.get("DATA_TYPES", "{}")),
        date_cols=json.loads(os.environ.get("DATE_COLS", "[]")),
        batch_count=int(os.environ.get("BATCH_COUNT", "0")),
    )
