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
import requests
from google.cloud import storage

# from numpy import source


def main(
    source_url: str,
    source_file_zip_file: pathlib.Path,
    source_file_path: pathlib.Path,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    csv_headers: typing.List[str],
    # rename_mappings: dict,
    pipeline_name: str,
) -> None:

    logging.info(
        f"FEC{pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file from {source_url}...")
    download_file(source_url, source_file_zip_file)
    unzip_file(source_file_zip_file, source_file_path)

    logging.info(f"Opening file {source_file}...")
    df = pd.read_table(
        source_file,
        sep="|",
        header=None,
        names=csv_headers,
        dtype=object,
        index_col=False,
    )

    logging.info(f"Transforming {source_file}... ")

    # logging.info("Transform: Rename columns... ")
    # rename_headers(df, rename_mappings)

    if "candidate_20" in pipeline_name:
        logging.info("Transform: Trimming white spaces in headers... ")
        df = df.rename(columns=lambda x: x.strip())

    elif "committee_20" in pipeline_name:
        df.drop(df[df["cmte_id"] == "C00622357"].index, inplace=True)

    elif "committee_contributions_20" in pipeline_name:
        df["transaction_dt"] = df["transaction_dt"].astype(str)
        # df["transaction_dt"] = df["transaction_dt"].str[:-2]
        date_for_length(df, "transaction_dt")
        df = resolve_date_format(df, "transaction_dt", pipeline_name)

    elif "other_committee_tx_20" in pipeline_name:
        df["transaction_dt"] = df["transaction_dt"].astype(str)
        # df["transaction_dt"] = df["transaction_dt"].str[:-2]
        date_for_length(df, "transaction_dt")
        df = resolve_date_format(df, "transaction_dt", pipeline_name)

    elif "opex" in pipeline_name:
        df["transaction_dt"] = df["transaction_dt"].astype(str)
        # df["transaction_dt"] = df["transaction_dt"].str[:-2]
        date_for_length(df, "transaction_dt")
        df = resolve_date_format(df, "transaction_dt", pipeline_name)

    # elif pipeline_name == "individuals_":
    #     df["transaction_dt"] = df["transaction_dt"].astype(str)
    #     #df["transaction_dt"] = df["transaction_dt"].str[:-2]
    #     date_for_length(df, "transaction_dt")
    #     df = resolve_date_format(df, "transaction_dt", pipeline_name)
    #     df = df.rename(columns=lambda x: x.strip())

    else:
        pass

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
        f"FEC {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def resolve_date_format(
    df: pd.DataFrame,
    field_name: str,
    pipeline: str,
) -> pd.DataFrame:
    if "opex" not in pipeline:
        logging.info("Resolving date formats")
        df[field_name] = df[field_name].apply(convert_dt_format)
        return df
    else:
        logging.info("Resolving date formats")
        df[field_name] = df[field_name].apply(convert_dt_format_opex)
        return df


def convert_dt_format(dt_str: str) -> str:
    if (
        not dt_str
        or str(dt_str).lower() == "nan"
        or str(dt_str).lower() == "nat"
        or dt_str == "-"
    ):
        return ""
    else:
        return str(
            datetime.datetime.strftime(
                datetime.datetime.strptime(dt_str, "%m%d%Y"), "%Y-%m-%d"
            )
        )


def convert_dt_format_opex(dt_str: str) -> str:
    if (
        not dt_str
        or str(dt_str).lower() == "nan"
        or str(dt_str).lower() == "nat"
        or dt_str == "-"
    ):
        return ""
    else:
        return str(
            datetime.datetime.strftime(
                datetime.datetime.strptime(dt_str, "%m/%d/%Y"), "%Y-%m-%d"
            )
        )


def date_for_length(df: pd.DataFrame, field_name: str):
    date_list = df[field_name].values
    new_date_list = []
    for item in date_list:
        if item != "NaN":
            if len(item) == 7:
                item = "0" + item
                new_date_list.append(item)
            elif len(item) == 6:
                item = "0" + item[0:1] + "0" + item[1:]
                new_date_list.append(item)
            else:
                new_date_list.append(item)
                continue
        else:
            new_date_list.append(item)
    df[field_name] = new_date_list
    return df[field_name]


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file_zip_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file_zip_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file_zip_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def unzip_file(
    source_file_zip_file: pathlib.Path, source_file_path: pathlib.Path
) -> None:
    logging.info(f"Unzipping {source_file_zip_file}")
    with ZipFile(source_file_zip_file, "r") as zipObj:
        zipObj.extractall(source_file_path)


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
        source_file_zip_file=pathlib.Path(
            os.environ["SOURCE_FILE_ZIP_FILE"]
        ).expanduser(),
        source_file_path=pathlib.Path(os.environ["SOURCE_FILE_PATH"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        csv_headers=json.loads(os.environ["CSV_HEADERS"]),
        # rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
