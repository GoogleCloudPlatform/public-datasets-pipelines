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

import pandas as pd
from google.cloud import storage


def main(
    source_bucket: str,
    source_object: str,
    source_file: pathlib.Path,
    source_storage_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    chunksize: str,
    pipeline_name: str,
    csv_headers: typing.List[str],
) -> None:
    logging.info(
        f"HACKERNEWS{pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_blob(source_bucket, source_object, source_file)
    process_source_file(
        source_file,
        source_storage_file,
        target_file,
        chunksize,
        pipeline_name,
        csv_headers,
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def process_source_file(
    source_file: str,
    source_storage_file: str,
    target_file: str,
    chunksize: str,
    pipeline_name: str,
    csv_headers: typing.List[str],
) -> None:
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512 << 10)
    csv.register_dialect("TabDialect", quotechar='"', delimiter="\t", strict=True)
    with open(source_file, newline="") as f_input, open(
        source_storage_file, "w", newline=""
    ) as f_output:
        csv_input = csv.reader(f_input, skipinitialspace=True)
        csv_output = csv.writer(f_output, quoting=csv.QUOTE_NONNUMERIC)
        index = 0
        chunk_number = 1
        for row_input in csv_input:
            row_output = []
            for col in row_input:
                try:
                    row_output.append(int(col))
                except ValueError:
                    try:
                        row_output.append(float(col))
                    except ValueError:
                        row_output.append(col)
            index = index + 1
            csv_output.writerow(row_output)
            if int(index) % int(chunksize) == 0 and int(index) > 0:
                process_dataframe_chunk(
                    source_storage_file,
                    target_file,
                    chunk_number,
                    pipeline_name,
                    csv_headers,
                )
                index = 0
                chunk_number += 1
                f = open(source_storage_file, "w+")
                f.close()
        if index:
            process_dataframe_chunk(
                source_storage_file,
                target_file,
                chunk_number,
                pipeline_name,
                csv_headers,
            )


def process_dataframe_chunk(
    source_storage_file: str,
    target_file: str,
    chunk_number: int,
    pipeline_name: str,
    csv_headers: typing.List[str],
) -> None:
    df = pd.read_csv(
        source_storage_file, names=csv_headers, index_col=None, dtype=object, skiprows=1
    )
    df = df.replace("\n", "", regex=True)
    df = df.replace("\r", "", regex=True)
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        target_file_batch=target_file_batch,
        target_file=target_file,
        pipeline_name=pipeline_name,
        skip_header=(not chunk_number == 1),
    )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    pipeline_name: str,
    skip_header: bool,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    save_to_new_file(df, file_path=str(target_file_batch), sep=",")
    append_batch_file(target_file_batch, target_file, skip_header)
    logging.info(f"Processing batch file {target_file_batch} completed")


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = ",") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=",")


def append_batch_file(
    target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    with open(target_file_batch, "r") as data_file:
        with open(target_file, "a+") as target_file:
            if skip_header:
                logging.info(
                    f"Appending batch file {target_file_batch} to {target_file} with skipheader..."
                )
                next(data_file)
            else:
                logging.info(
                    f"Appending batch file {target_file_batch} to {target_file}"
                )
            target_file.write(data_file.read())
            if os.path.exists(target_file_batch):
                os.remove(target_file_batch)


def download_blob(bucket, object, target_file) -> None:
    logging.info(f"Downloading file gs://{bucket}/{target_file}")
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(object)
    blob.download_to_filename(target_file)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info(f"Uploading output file to.. gs://{gcs_bucket}/{gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_bucket=os.environ.get("SOURCE_GCS_BUCKET", ""),
        source_object=os.environ.get("SOURCE_GCS_OBJECT", ""),
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        source_storage_file=pathlib.Path(
            os.environ["SOURCE_STORAGE_FILE"]
        ).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        csv_headers=json.loads(os.environ["CSV_HEADERS"]),
    )
