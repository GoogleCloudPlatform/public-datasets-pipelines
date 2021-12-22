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
import subprocess
import typing
from glob import glob

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
) -> None:

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    all_csv_files = []
    for path, subdir, files in os.walk(source_file):
        for file in glob(os.path.join(path, "*.csv")):
            all_csv_files.append(file)
    read_csv_file = [
        pd.read_csv(filename, low_memory=False) for filename in all_csv_files
    ]
    df = pd.concat(read_csv_file, axis=0, ignore_index=True)

    logging.info("Search and replacing values..")
    df.drop(
        df[df.settlement_date.astype(str).str.startswith("Trailer")].index, inplace=True
    )
    df["settlement_date"] = pd.to_datetime(
        df["settlement_date"].astype(str), errors="coerce"
    )
    df["total_shares"] = df["total_shares"].fillna(0).astype(int)
    df = df.replace(
        to_replace={
            "share_price": {'"': ""},
        }
    )
    df = df.replace(
        to_replace={"share_price": {"^.$": "", "\n": ""}, "company_name": {"\n": ""}},
        regex=True,
    )

    logging.info("Transform: Reordering headers..")
    df = df[headers]

    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    logging.info("..Done!")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def save_to_new_file(df, file_path):
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    subprocess.check_call(["gsutil", "cp", "-r", f"{source_url}", f"{source_file}"])


# # def download_file(source_url: str, source_file: pathlib.Path) -> None:
# #     logging.info(f"Downloading {source_url} into {source_file}")
# #     r = requests.get(source_url, stream=True)
# #     if r.status_code == 200:
# #         with open(source_file, "wb") as f:
# #             for chunk in r:
# #                 f.write(chunk)
#     else:
#         logging.error(f"Couldn't download {source_url}: {r.text}")


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
    )
