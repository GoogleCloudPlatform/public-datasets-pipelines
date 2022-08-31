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

import csv
import datetime
import json
import logging
import os
import pathlib
import typing

from google.cloud import storage
from pgdumplib import dump, load


def main(
    output_folder: pathlib.Path,
    source_gcs_bucket: str,
    source_gcs_object: str,
    source_file: pathlib.Path,
    tables: typing.List[str],
    target_gcs_bucket: str,
    target_gcs_folder: str,
) -> None:
    logging.info(
        f"EMBL EBI ChEMBL Dataset pipeline process started for table(s) -  {tables} at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info(f"Creating '{output_folder}' folder.")
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
    download_blob(source_gcs_bucket, source_gcs_object, source_file)
    logging.info(f"Reading {source_file}")
    dump_data = load(source_file)
    write_table_to_csv(dump_data, tables, output_folder)
    for file in os.listdir(output_folder):
        full_path = f"{output_folder}/{file}"
        target_gcs_path = f"{target_gcs_folder}/{file}"
        upload_file_to_gcs(full_path, target_gcs_bucket, target_gcs_path)
    logging.info(
        f"EMBL EBI ChEMBL Dataset pipeline process completed for table(s) -  {tables} at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def download_blob(
    source_gcs_bucket: str, source_gcs_object: str, target_file: pathlib.Path
) -> None:
    """Downloads a blob from the bucket."""
    logging.info(
        f"Downloading data from gs://{source_gcs_bucket}/{source_gcs_object} to {target_file} ..."
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(source_gcs_bucket)
    blob = bucket.blob(source_gcs_object)
    blob.download_to_filename(target_file)
    logging.info("Downloading Completed.")


def write_table_to_csv(
    dump_data: dump.Dump, tables: typing.List[str], output_folder: pathlib.Path
) -> None:
    length = len(tables)
    for idx, table in enumerate(tables):
        output_file = f"{output_folder}/{table}_data_output.csv"
        logging.info(f"\t\t\t{idx+1} out of {length} tables.")
        logging.info(f"Writing {table} - table to {output_file} file")
        with open(output_file, "w") as fb:
            writer = csv.writer(
                fb, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            for line in dump_data.table_data("public", table):
                writer.writerow(line)


def upload_file_to_gcs(
    source_file: str, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(
        f"Uploading output file {source_file} to gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(source_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        output_folder=pathlib.Path(os.environ.get("OUTPUT_FOLDER", "")).expanduser(),
        source_gcs_bucket=os.environ.get("SOURCE_GCS_BUCKET", ""),
        source_gcs_object=os.environ.get("SOURCE_GCS_OBJECT", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        tables=json.loads(os.environ.get("TABLES", "[]")),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_folder=os.environ.get("TARGET_GCS_FOLDER", ""),
    )
