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

import glob
import json
import logging
import os
import pathlib
import subprocess
import typing
import datetime
import pandas as pd
from google.cloud import storage
from pandas.io.parsers import read_csv


def main(
    source_url: typing.List[str],
    source_file: typing.List[pathlib.Path],
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    pipeline_name: str,
    joining_key: str,
    columns: typing.list[str],
    # filter_headers: typing.List[str],
    # trim_space: typing.List[str],
) -> None:

    logging.info(
        f"BLS {pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file...")
    download_file(source_url, source_file)

    logging.info(f"Reading the file(s)....")
    # if pipeline_name == "employment_hours_earnings_series" or pipeline_name == "unemployment_cps_series" or pipeline_name == "unemployment_cps_series" :
    #     df = pd.read_csv(source_file[0],sep="\t")
    # else:
    #     df1 = pd.read_csv(source_file[0])
    #     df2 = pd.read_csv(source_file[1])
    #     df = pd.merge(df1, df2, how="left", on=["series_id"])

    df=read_files(source_file,joining_key)

    # logging.info("Filter Headers ...")
    # df = df[filter_headers]

    logging.info("Trim Whitespaces...")
    # trim_spaces(df, trim_space)
    # df['series_id']= df['series_id'].str.strip()
    # df['footnote_codes']= df['footnote_codes'].astype(str).str.strip()
    # df['series_title']= df['series_title'].str.strip()

    tream_white_spaces(df,columns)

    # logging.info("Search and Replacing the values..")
    # if pipeline_name == "midyear_population_age_sex":
    #     df["sex"] = df["sex"].apply({2: "Male", 3: "Female"}.get)
    # else:
    #     df = df

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

    logging.info(
        f"BLS {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

# def trim_spaces(df: pd.DataFrame, trim_space: typing.List[str]) -> None:
#     df[trim_space]=df[trim_space].apply(lambda x: x.str.strip())

def save_to_new_file(df, file_path):
    df.to_csv(file_path, index=False)

def download_file(
    source_url: typing.List[str], source_file: typing.List[pathlib.Path]
) -> None:
    for url, file in zip(source_url, source_file):
        logging.info(f"Downloading file from {url} ...")
        subprocess.check_call(["gsutil", "cp", f"{url}", f"{file}"])

# def read_files(path: pathlib.Path) -> pd.DataFrame:
#     all_files = glob.glob(path + "/*.csv")
#     df_temp = []
#     for filename in all_files:
#         frame = pd.read_csv(filename, index_col=None, header=0)
#         df_temp.append(frame)
#     df = pd.concat(df_temp, axis=0, ignore_index=True)
#     return df

def read_files(source_file,joining_key) :
    if len(source_file) >1 :
        if source_file[0][-3:] == 'csv' :
                df1 = pd.read_csv(source_file[0])
        else :
            df1 = pd.read_csv(source_file[0], sep='\t')
        if source_file[1][-3:] == 'csv':
            df2 = pd.read_csv(source_file[1])
        else :
            df2 = pd.read_csv(source_file[1], sep='\t')
        df = pd.merge(df1,df2,how="left", on=joining_key)
    else :
        if source_file[0][-3:] == 'csv' :
                df = pd.read_csv(source_file[0])
        else :
            df = pd.read_csv(source_file[0], sep='\t')
    return df

def tream_white_spaces(df,columns) :
    for col in columns :
        df[col]= df[col].astype(str).str.strip()


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=json.loads(os.environ["SOURCE_URL"]),
        source_file=json.loads(os.environ["SOURCE_FILE"]),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        joining_key=os.environ["JOINING_KEY"],
        columns=json.loads(os.environ["TRIM_COL"])
        # filter_headers=json.loads(os.environ["FILTER_HEADERS"]),
        # trim_space=json.loads(os.environ["TRIM_SPACE"]),
    )
