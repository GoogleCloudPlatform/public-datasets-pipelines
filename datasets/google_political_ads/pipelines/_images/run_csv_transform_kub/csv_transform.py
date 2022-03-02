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
import math
import os
import pathlib
import typing
from zipfile import ZipFile

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    source_csv_name: str,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
) -> None:

    logging.info(
        f"google political ads {pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = read_csv_file(source_file, source_csv_name)

    logging.info(f"Transforming.. {source_file}")

    logging.info(f"Transform: Rename columns for {pipeline_name}..")
    rename_headers(df, rename_mappings)

    if pipeline_name == "creative_stats":
        logging.info(f"Transform: converting to integer for {pipeline_name}..")
        df["spend_range_max_usd"] = df["spend_range_max_usd"].apply(convert_to_int)
        df["spend_range_max_eur"] = df["spend_range_max_eur"].apply(convert_to_int)
        df["spend_range_max_inr"] = df["spend_range_max_inr"].apply(convert_to_int)
        df["spend_range_max_bgn"] = df["spend_range_max_bgn"].apply(convert_to_int)
        df["spend_range_max_hrk"] = df["spend_range_max_hrk"].apply(convert_to_int)
        df["spend_range_max_czk"] = df["spend_range_max_czk"].apply(convert_to_int)
        df["spend_range_max_dkk"] = df["spend_range_max_dkk"].apply(convert_to_int)
        df["spend_range_max_huf"] = df["spend_range_max_huf"].apply(convert_to_int)
        df["spend_range_max_pln"] = df["spend_range_max_pln"].apply(convert_to_int)
        df["spend_range_max_ron"] = df["spend_range_max_ron"].apply(convert_to_int)
        df["spend_range_max_gbp"] = df["spend_range_max_gbp"].apply(convert_to_int)
        df["spend_range_max_sek"] = df["spend_range_max_sek"].apply(convert_to_int)
        df["spend_range_max_nzd"] = df["spend_range_max_nzd"].apply(convert_to_int)
    else:
        df = df

    logging.info(f"Transform: Reordering headers for {pipeline_name}.. ")
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
        f"Google Political Ads {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def read_csv_file(source_file: pathlib.Path, source_csv_name: str) -> pd.DataFrame:
    with ZipFile(source_file) as zipfiles:
        file_list = zipfiles.namelist()
        csv_files = fnmatch.filter(file_list, source_csv_name)
        data = [pd.read_csv(zipfiles.open(file_name)) for file_name in csv_files]
    df = pd.concat(data)
    return df


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def convert_to_int(input: str) -> str:
    str_val = ""
    if input == "" or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(int(round(input, 0)))
    return str_val


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        source_csv_name=os.environ["FILE_NAME"],
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
