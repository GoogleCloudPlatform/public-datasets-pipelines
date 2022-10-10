# Copyright 2022 Google LLC
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

import pandas as pd
import requests
from google.cloud import storage


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

    logging.info(
        f"FDIC{pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file from {source_url}...")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}...")
    df = pd.read_csv(str(source_file))

    logging.info(f"Transforming {source_file}... ")

    logging.info("Renaming Columns...")
    rename_headers(df, rename_mappings)

    if pipeline_name == "locations":
        logging.info("Replacing bool values...")
        replace_bool_list = [
            "main_office",
            "cbsa_division_flag",
            "cbsa_metro_flag",
            "cbsa_micro_flag",
            "csa_flag",
        ]
        replace_bool(replace_bool_list, df)
        df["cbsa_division_fips_code"] = df["cbsa_division_fips_code"].astype(
            "Int64", errors="ignore"
        )
        logging.info("Replacing date values...")
        format_date_list = ["date_established", "last_updated"]
        format_date(format_date_list, df)
        logging.info("Replacing with null values...")
        df["cbsa_metro_fips_code"] = df["cbsa_metro_fips_code"].replace(0, "NULL")
    else:
        logging.info("Replacing bool values...")
        replace_bool_list = [
            "active",
            "conservatorship",
            "denovo_institute",
            "federal_charter",
            "iba",
            "inactive_flag",
            "credit_card_institution",
            "bank_insurance_fund_member",
            "insured_commercial_bank",
            "deposit_insurance_fund_member",
            "fdic_insured",
            "saif_insured",
            "insured_savings_institute",
            "oakar_institute",
            "state_chartered",
            "sasser_institute",
            "law_sasser",
            "cfpb_supervisory_flag",
            "ffiec_call_report_filer",
            "holding_company_flag",
            "ag_lending_flag",
            "ownership_type",
            "csa_indicator",
            "cbsa_metro_flag",
            "cbsa_micro_flag",
            "cbsa_division_flag",
            "subchap_s_indicator",
        ]
        replace_bool(replace_bool_list, df)
        logging.info("Replacing date values...")
        replace_date_list = [
            "last_updated",
            "effective_date",
            "end_effective_date",
            "deposit_insurance_date",
            "last_structural_change",
            "report_date",
            "reporting_period_end_date",
            "run_date",
            "cfpb_supervisory_start_date",
            "cfpb_supervisory_end_date",
        ]
        replace_date(replace_date_list, df)
        logging.info("Formatting date values...")
        format_date_list = [
            "established_date",
            "last_updated",
            "effective_date",
            "end_effective_date",
            "deposit_insurance_date",
            "last_structural_change",
            "report_date",
            "reporting_period_end_date",
            "run_date",
        ]
        format_date(format_date_list, df)
        logging.info("Filling null values...")
        null_list = [
            "total_assets",
            "total_deposits",
            "equity_capital",
            "offices_count",
            "total_domestic_deposits",
            "net_income",
            "quarterly_net_income",
            "office_count_domestic",
            "office_count_foreign",
            "office_count_us_territories",
        ]
        fill_null(null_list, df)

    logging.info("Transform: Reordering headers..")
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
        f"FDIC {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def replace_bool(replace_bool_list: list, df: pd.DataFrame):
    for item in replace_bool_list:
        df[item] = df[item].replace([0, 1], [False, True])


def format_date(format_date_list: list, df: pd.DataFrame):
    for item in format_date_list:
        df[item] = pd.to_datetime(df[item])
        df[item] = df[item].dt.strftime("%Y-%m-%d")


def replace_date(replace_date_list: list, df: pd.DataFrame):
    for item in replace_date_list:
        empty_list = []
        df[item] = df[item].astype(str)
        df[item] = df[item].replace("nan", "")
        for value in df[item]:
            if "9999" in value:
                value = ""
                empty_list.append(value)
            else:
                empty_list.append(value)
        df[item] = empty_list
        df[item] = pd.to_datetime(df[item], format="%m-%d-%Y", errors="ignore")


def fill_null(null_list: list, df: pd.DataFrame):
    for item in null_list:
        df[item] = df[item].fillna(0)
        df[item] = df[item].astype(int)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
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
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
