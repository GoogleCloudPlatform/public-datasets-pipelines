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
import re
import subprocess
import typing

import pandas as pd
from google.cloud import storage


def main(
    source_urls: typing.List[str],
    source_files: typing.List[pathlib.Path],
    chunksize: str,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    reorder_headers_list: typing.List[str],
    pipeline_name: str,
    joining_key: str,
    trim_space_columns: typing.List[str],
) -> None:
    logging.info(
        f"BLS {pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    logging.info("Downloading file...")
    download_file(source_urls, source_files)
    logging.info("Processing file(s)....")
    process_source_file(
        source_file_list=source_files,
        target_file=target_file,
        joining_key=joining_key,
        pipeline_name=pipeline_name,
        chunksize=chunksize,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        reorder_headers_list=reorder_headers_list,
        trim_space_columns=trim_space_columns,
    )
    logging.info(
        f"BLS {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def download_file(
    source_urls: typing.List[str], source_files: typing.List[pathlib.Path]
) -> None:
    for url, file in zip(source_urls, source_files):
        logging.info(f"Downloading file from {url} ...")
        subprocess.check_call(["gcloud", "storage", "cp", f"{url}", f"{file}"])


def load_helper_dataframe(source_file: str) -> pd.DataFrame:
    if os.path.splitext(source_file)[1] == ".csv":
        df = pd.read_csv(source_file)
    else:
        df = pd.read_csv(source_file, sep="\t")
    return df


def process_source_file(
    source_file_list: typing.List[str],
    target_file: str,
    joining_key: str,
    pipeline_name: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    reorder_headers_list: typing.List[str],
    trim_space_columns: typing.List[str],
) -> None:
    main_file = source_file_list[0]
    if len(source_file_list) == 2:
        logging.info(f"Loading helper file {source_file_list[1]}")
        df_helper = load_helper_dataframe(source_file_list[1])
        logging.info(f"Merging file {main_file} with {source_file_list[1]}")
    else:
        df_helper = pd.DataFrame()
        logging.info(f"Loading file {main_file}")
    with pd.read_csv(
        main_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),
        sep=("," if os.path.splitext(main_file)[1] == ".csv" else "\t"),
        header=0,
        keep_default_na=True,
        na_values=[" "],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number).zfill(10) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df=df,
                df_helper=df_helper,
                joining_key=joining_key,
                pipeline_name=pipeline_name,
                target_file_batch=target_file_batch,
                target_gcs_bucket=target_gcs_bucket,
                target_gcs_path=target_gcs_path,
                reorder_headers_list=reorder_headers_list,
                trim_space_columns=trim_space_columns,
            )


def process_chunk(
    df: pd.DataFrame,
    df_helper: pd.DataFrame,
    joining_key: str,
    pipeline_name: str,
    target_file_batch: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    reorder_headers_list: typing.List[str],
    trim_space_columns: typing.List[str],
) -> None:
    df.columns = df.columns.str.strip()
    if not (df_helper.empty):
        logging.info("Merging data for chunk.")
        df_helper.columns = df_helper.columns.str.strip()
        df = pd.merge(df, df_helper, how="left", on=joining_key)
    else:
        logging.info("Skipping merge data for chunk.")
    logging.info("Transform: Trim Column Header Whitespaces...")
    trim_white_spaces(df, trim_space_columns)
    if pipeline_name == "unemployment_cps":
        logging.info("Transform: Replacing values...")
        df["value"] = df["value"].apply(reg_exp_tranformation, args=(r"^(\-)$", ""))
    logging.info("Transform: Reordering headers..")
    df = df[reorder_headers_list]
    logging.info(f"Saving to output file.. {target_file_batch}")
    try:
        df.to_csv(str(target_file_batch), index=False)
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    target_gcs_batch_path = os.path.join(
        os.path.dirname(target_gcs_path), os.path.basename(target_file_batch)
    )
    logging.info(
        f"Uploading output batch file {target_file_batch} to gs://{target_gcs_bucket}/{target_gcs_batch_path}"
    )
    upload_file_to_gcs(target_file_batch, target_gcs_bucket, target_gcs_batch_path)
    os.unlink(target_file_batch)


def trim_white_spaces(df: pd.DataFrame, columns: typing.List[str]) -> None:
    for col in columns:
        df[col] = df[col].astype(str).str.strip()


def reg_exp_tranformation(str_value: str, search_pattern: str, replace_val: str) -> str:
    return re.sub(search_pattern, replace_val, str_value)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_urls=json.loads(os.environ["SOURCE_URLS"]),
        source_files=json.loads(os.environ["SOURCE_FILES"]),
        chunksize=os.environ["CHUNKSIZE"],
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        reorder_headers_list=json.loads(os.environ["CSV_HEADERS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        joining_key=os.environ["JOINING_KEY"],
        trim_space_columns=json.loads(os.environ["TRIM_SPACE"]),
    )
