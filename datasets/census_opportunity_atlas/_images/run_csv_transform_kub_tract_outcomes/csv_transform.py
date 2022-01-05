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
import logging
import os
import pathlib
from urllib.parse import urlparse
from zipfile import ZipFile

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    source_file_unzipped: str,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    english_pipeline_name: str
) -> None:
    logging.info(f"{english_pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    source_zipfile = str.replace(str(source_file), ".csv", ".zip")
    source_file_path = source_file.parent
    download_file(source_url, source_zipfile)
    zip_decompress(source_zipfile, source_file_path, True)
    os.rename(source_file_unzipped, target_file)
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
    logging.info(f"{english_pipeline_name} process completed")


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading file {source_url}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def zip_decompress(infile: str, topath: str, remove_zipfile: bool = False) -> None:
    logging.info(f"Decompressing {infile} to {topath}")
    with ZipFile(infile, "r") as zip:
        zip.extractall(topath)
    if remove_zipfile:
        os.unlink(infile)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info("Uploading to GCS {gcs_bucket} in {gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        source_file_unzipped=pathlib.Path(os.environ["SOURCE_FILE_UNZIPPED"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        english_pipeline_name=os.environ["ENGLISH_PIPELINE_NAME"],
    )
