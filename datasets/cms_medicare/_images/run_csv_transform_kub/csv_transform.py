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
import fnmatch
import json
import logging
import os
import pathlib
import typing
from zipfile import ZipFile

import pandas as pd
import requests
from google.cloud import storage

PIPELINES_NAME_INPATIENT = [
    "inpatient_charges_2011",
    "inpatient_charges_2012",
    "inpatient_charges_2013",
    "inpatient_charges_2014",
    "inpatient_charges_2015",
]
PIPELINES_NAME_OUTPATIENT = [
    "outpatient_charges_2011",
    "outpatient_charges_2012",
    "outpatient_charges_2013",
    "outpatient_charges_2014",
]


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
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

    logging.info(f"Opening file {source_file}")

    if pipeline_name in (PIPELINES_NAME_INPATIENT + PIPELINES_NAME_OUTPATIENT):
        with ZipFile(source_file) as zipped_files:
            file_list = zipped_files.namelist()
            csv_file = fnmatch.filter(file_list, "*.csv")
            data = zipped_files.open(*csv_file)
            df = pd.read_csv(data)
    else:
        df = pd.read_csv(str(source_file))

    logging.info(f"Transformation Process Starting.. {source_file}")

    rename_headers(df, rename_mappings)

    filter_null_rows(
        df, PIPELINES_NAME_INPATIENT, PIPELINES_NAME_OUTPATIENT, pipeline_name
    )

    df = df[headers]

    logging.info(f"Transformation Process complete .. {source_file}")

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
        "CMS Medicare process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def filter_null_rows(
    df: pd.DataFrame,
    PIPELINES_NAME_INPATIENT: typing.List[str],
    PIPELINES_NAME_OUTPATIENT: typing.List[str],
    pipeline_name: str,
) -> pd.DataFrame:
    if pipeline_name in PIPELINES_NAME_INPATIENT:
        return df.dropna(subset=["drg_definition", "provider_id"], inplace=True)
    elif pipeline_name in PIPELINES_NAME_OUTPATIENT:
        return df.dropna(subset=["apc", "provider_id"], inplace=True)
    else:
        return df


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, float_format="%.0f", index=False)


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
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
