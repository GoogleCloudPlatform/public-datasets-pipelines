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
import logging
import os
import pathlib
import typing

import requests
from google.cloud import storage


def main(
    base_url: str,
    folder: pathlib.Path,
    version: str,
    gcs_bucket: str,
    target_gcs_folder: str,
    pipeline: str,
):
    logging.info(
        f"Human Variant Annotation Dataset {pipeline} pipeline process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info(f"Creating './files/{folder}'")
    pathlib.Path(f"./files/{folder}").mkdir(parents=True, exist_ok=True)
    dates = get_dates()
    for date in dates:
        date_time = datetime.datetime.strptime(date, "%Y%m%d")
        get_files(date_time, base_url, version, folder, gcs_bucket, target_gcs_folder)

    logging.info(
        f"Human Variant Annotation Dataset {pipeline} pipeline process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def get_dates() -> typing.List[str]:
    today = datetime.datetime.now()
    start_date = datetime.datetime(today.year, today.month - 1, 1)
    end_date = today
    delta = datetime.timedelta(days=1)
    dates = []
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y%m%d"))
        start_date += delta
    return dates


def get_files(
    date_time: datetime.datetime,
    base_url: str,
    version: str,
    folder: pathlib.Path,
    gcs_bucket: str,
    target_gcs_folder: str,
):
    file_name = f"clinvar_{date_time.strftime('%Y%m%d')}.vcf.gz"
    source_url = base_url + f"archive_{version}/{date_time.strftime('%Y')}/{file_name}"
    source_file = f"./files/{folder}/{file_name}"
    status_code = download_gzfile(source_url, source_file)
    if status_code == 200:
        target_gcs_path = f"{target_gcs_folder}{file_name}"
        upload_file_to_gcs(source_file, gcs_bucket, target_gcs_path)


def download_gzfile(source_url: str, source_file: str):
    logging.info(f"Downloading data from {source_url} to {source_file} .")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
        logging.info(f"\tDownloaded data from {source_url} into {source_file}")
    else:
        logging.info(f"Couldn't download {source_url}: Error {res.status_code}")
    return res.status_code


def upload_file_to_gcs(
    source_file: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(source_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        base_url=os.environ.get("BASE_URL", ""),
        folder=pathlib.Path(os.environ.get("FOLDER", "")).expanduser(),
        version=os.environ.get("VERSION", "2.0"),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        target_gcs_folder=os.environ.get("TARGET_GCS_FOLDER", ""),
        pipeline=os.environ.get("PIPELINE", ""),
    )
