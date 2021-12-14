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
) -> None:

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)
    chunksz = int(chunksize)

    logging.info(f"Reading csv file {source_url}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        compression="gzip",
        chunksize=chunksz,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])

            logging.info(" Renaming headers...")
            rename_headers(df, rename_mappings)
            logging.info("Transform: Reordering headers..")
            df = df[headers]
            if pipeline_name == "sentinel_2_index":
                df["total_size"] = df["total_size"].astype("Int64")

            process_chunk(df, target_file_batch)

            logging.info(f"Appending batch {chunk_number} to {target_file}")
            if chunk_number == 0:
                subprocess.run(["cp", target_file_batch, target_file])
            else:
                subprocess.check_call([f"sed -i '1d' {target_file_batch}"], shell=True)
                subprocess.check_call(
                    [f"cat {target_file_batch} >> {target_file}"], shell=True
                )
            subprocess.run(["rm", target_file_batch])

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def process_chunk(df: pd.DataFrame, target_file_batch: str) -> None:

    logging.info(f"Saving to output file.. {target_file_batch}")
    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    logging.info("..Done!")


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df = df.rename(columns=rename_mappings, inplace=True)


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
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
