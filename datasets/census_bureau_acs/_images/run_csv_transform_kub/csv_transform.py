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

import numpy as np
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    year_report: str,
    api_naming_convention: str,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
    geography: str,
    report_level: str,
    concat_col: typing.List[str],
) -> None:

    logging.info(
        f"ACS {pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    json_obj_group_id = open("group_ids.json")
    group_id = json.load(json_obj_group_id)

    json_obj_state_code = open("state_codes.json")
    state_code = json.load(json_obj_state_code)

    logging.info("Extracting the data from API and loading into dataframe...")
    if report_level == "national_level":
        df = extract_data_and_convert_to_df_national_level(
            group_id, year_report, api_naming_convention, source_url
        )
    elif report_level == "state_level":
        df = extract_data_and_convert_to_df_state_level(
            group_id, state_code, year_report, api_naming_convention, source_url
        )

    logging.info("Replacing values...")
    df = df.replace(to_replace={"KPI_Name": group_id})

    logging.info("Renaming headers...")
    rename_headers(df, rename_mappings)

    logging.info("Creating column geo_id...")
    if geography == "censustract" or geography == "blockgroup":
        df["tract"] = df["tract"].apply(pad_zeroes_to_the_left, args=(6,))
        df["state"] = df["state"].apply(pad_zeroes_to_the_left, args=(2,))
        df["county"] = df["county"].apply(pad_zeroes_to_the_left, args=(3,))

    df = create_geo_id(df, concat_col)

    logging.info("Pivoting the dataframe...")
    df = df[["geo_id", "KPI_Name", "KPI_Value"]]
    df = df.pivot_table(
        index="geo_id", columns="KPI_Name", values="KPI_Value", aggfunc=np.sum
    ).reset_index()

    logging.info("Reordering headers...")
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
        f"ACS {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def string_replace(source_url, replace: dict) -> str:
    for k, v in replace.items():
        source_url_new = source_url.replace(k, v)
    return source_url_new


def extract_data_and_convert_to_df_national_level(
    group_id: dict, year_report: str, api_naming_convention: str, source_url: str
) -> pd.DataFrame:
    list_temp = []
    for key in group_id:
        logging.info(f"reading data from API for KPI {key}...")
        str1 = source_url.replace("~year_report~", year_report)
        str2 = str1.replace("~group_id~", key[0:-3])
        str3 = str2.replace("~row_position~", key[-3:])
        source_url_new = str3.replace("~api_naming_convention~", api_naming_convention)
        try:
            r = requests.get(source_url_new, stream=True)
            logging.info(f"Source url : {source_url_new}")
            logging.info(f"status code : {r.status_code}")
            if r.status_code == 200:
                text = r.json()
                frame = load_nested_list_into_df_without_headers(text)
                frame["KPI_Name"] = key
                list_temp.append(frame)
        except OSError as e:
            logging.info(f"error : {e}")
            pass
    logging.info("creating the dataframe...")
    df = pd.concat(list_temp)
    return df


def load_nested_list_into_df_without_headers(text: typing.List) -> pd.DataFrame:
    frame = pd.DataFrame(text)
    frame = frame.iloc[1:, :]
    return frame


def extract_data_and_convert_to_df_state_level(
    group_id: dict,
    state_code: dict,
    year_report: str,
    api_naming_convention: str,
    source_url: str,
) -> pd.DataFrame:
    list_temp = []
    for key in group_id:
        for sc in state_code:
            logging.info(f"reading data from API for KPI {key}...")
            logging.info(f"reading data from API for KPI {sc}...")
            str1 = source_url.replace("~year_report~", year_report)
            str2 = str1.replace("~group_id~", key[0:-3])
            str3 = str2.replace("~row_position~", key[-3:])
            str4 = str3.replace("~api_naming_convention~", api_naming_convention)
            source_url_new = str4.replace("~state_code~", sc)
            try:
                r = requests.get(source_url_new, stream=True)
                logging.info(f"Source url : {source_url_new}")
                logging.info(f"status code : {r.status_code}")
                if r.status_code == 200:
                    text = r.json()
                    frame = load_nested_list_into_df_without_headers(text)
                    frame["KPI_Name"] = key
                    list_temp.append(frame)
            except OSError as e:
                logging.info(f"error : {e}")
                pass

    logging.info("creating the dataframe...")
    df = pd.concat(list_temp)
    return df


def create_geo_id(df: pd.DataFrame, concat_col: str) -> pd.DataFrame:
    df["geo_id"] = ""
    for col in concat_col:
        df["geo_id"] = df["geo_id"] + df[col]
    return df


def pad_zeroes_to_the_left(val: str, length: int) -> str:
    if len(str(val)) < length:
        return ("0" * (length - len(str(val)))) + str(val)
    else:
        return str(val)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    rename_mappings = {int(k): str(v) for k, v in rename_mappings.items()}
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        year_report=os.environ["YEAR_REPORT"],
        api_naming_convention=os.environ["API_NAMING_CONVENTION"],
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        geography=os.environ["GEOGRAPHY"],
        report_level=os.environ["REPORT_LEVEL"],
        concat_col=json.loads(os.environ["CONCAT_COL"]),
    )
