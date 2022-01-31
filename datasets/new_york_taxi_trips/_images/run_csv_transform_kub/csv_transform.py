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
import typing
from datetime import datetime, timedelta

import pandas as pd
import requests
from airflow import DAG
from google.cloud import storage
from airflow.contrib.operators import gcs_to_bq

def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    data_dtypes: dict,
    pipeline_name: str,
) -> None:
    logging.info("New York taxi trips - green trips process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    start_date_year = int(
        datetime.strftime((datetime.now() + timedelta(days=-1825)), "%Y")
    )
    current_year = int(datetime.strftime(datetime.now(), "%Y"))

    execute_pipeline(current_year,
                     str(target_file),
                     source_url,
                     str(source_file),
                     chunksize,
                     headers,
                     data_dtypes,
                     pipeline_name,
                     target_gcs_bucket,
                     target_gcs_path)

    logging.info("New York taxi trips - green trips process completed")

def execute_pipeline(current_year: int,
                     target_file: str,
                     source_url: str,
                     source_file: str,
                     chunksize: str,
                     headers: typing.List[str],
                     data_dtypes: dict,
                     pipeline_name: str,
                     target_gcs_bucket: str,
                     target_gcs_path: str
    ) -> None:
    # for year_data in range((current_year), start_date_year - 1, -1):
    for year_number in range(2021, 2022):  #test
        target_file_ordinal = str(current_year - year_data)
        target_file_name = str.replace(
                            target_file,
                            ".csv",
                            "_" + target_file_ordinal + ".csv",
                            )
        process_year_data(
                        year_number,
                        target_file,
                        target_file_ordinal,
                        target_file_name,
                        source_url,
                        source_file,
                        chunksize,
                        headers,
                        data_dtypes,
                        pipeline_name,
                        target_gcs_bucket,
                        target_gcs_path)


def process_year_data(year_number: int,
                      target_file: str,
                      target_file_ordinal: str,
                      target_file_name: str,
                      source_url: str,
                      source_file: str,
                      chunksize: str,
                      headers: typing.List[str],
                      data_dtypes: dict,
                      pipeline_name: str,
                      target_gcs_bucket: str,
                      target_gcs_path: str
    ) -> None:
    logging.info(f"Processing year {year_number} as ordinal {target_file_ordinal}")
    for month_number in range(1, 13):
        process_month(year_number,
                      month_number,
                      target_file,
                      target_file_ordinal,
                      target_file_name,
                      source_url,
                      source_file,
                      chunksize,
                      headers,
                      data_dtypes,
                      pipeline_name,
                      target_gcs_bucket,
                      target_gcs_path)
    logging.info(f"Processing year {year_number} as ordinal {target_file_ordinal} completed")


def process_month(year_number: int,
                  month_number: int,
                  target_file: str,
                  target_file_ordinal: str,
                  target_file_name: str,
                  source_url: str,
                  source_file: str,
                  chunksize: str,
                  headers: typing.List[str],
                  data_dtypes: dict,
                  pipeline_name: str,
                  target_gcs_bucket: str,
                  target_gcs_path: str
    ) -> None:
    logging.info(f"Processing {year_number}-{month_number} as ordinal {target_file_ordinal}")
    process_month = str(year_number) + "-" + str(month_number).zfill(2)
    source_url_to_process = source_url + process_month + ".csv"
    source_file_to_process = str(source_file).replace(".csv", "-" + process_month + ".csv")
    successful_download = download_file(source_url_to_process, source_file_to_process)
    if successful_download:
        with pd.read_csv(
            source_file_to_process,
            engine="python",
            encoding="utf-8",
            quotechar='"',
            chunksize=int(chunksize),
            sep=",",
            names=headers,
            skiprows=1,
            dtype=data_dtypes,
        ) as reader:
            for chunk_number, chunk in enumerate(reader):
                logging.info(f"Processing batch {chunk_number}")
                target_file_batch = str(target_file).replace(
                    ".csv",
                    "_"
                    + str(target_file_ordinal)
                    + "-"
                    + str(chunk_number)
                    + ".csv",
                )
                df = pd.DataFrame()
                df = pd.concat([df, chunk])
                process_chunk(
                    df,
                    target_file_batch,
                    target_file_name,
                    (not chunk_number == 0),
                    (month_data == 1),
                    headers,
                    pipeline_name,
                )
        upload_file_to_gcs(
            target_file_name,
            target_gcs_bucket,
            str.replace(
                target_gcs_path, ".csv", "_" + str(target_file_ordinal) + ".csv"
            ),
        )
    logging.info(f"Processing {year_number}-{month_number} as ordinal {target_file_ordinal} completed")


def create_table_bigquery(table_name: str) -> None:
    print(f"Creating table {table_name}")

def load_from_gcs_to_bigquery(gcs_bucket: str, gcs_file: str, table_name: str) -> None:
    print(f"Loading data from gcs bucket {gcs_bucket} into table")

def download_file(source_url: str, source_file: pathlib.Path) -> bool:
    logging.info(f"Downloading {source_url} into {source_file}")
    success = True
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)
    # if the file contains the string "<Code>NoSuchKey</Code>" then the url returned
    # that it could not locate the respective file
    if open(source_file, "rb").read().find(b"<Code>NoSuchKey</Code>") > -1:
        success = False
    if success:
        logging.info(f"Download {source_url} to {source_file} complete.")
    else:
        logging.info(
            f"Unable to download {source_url} to {source_file} at this time.  The URL may not exist."
        )
    return success


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    truncate_file: bool,
    headers: typing.List[str],
    pipeline_name: str,
) -> None:
    if pipeline_name == "tlc_green_trips":
        df["distance_between_service"] = ""
        df["time_between_service"] = ""
    df = format_date_time(df, "pickup_datetime", "strftime", "%m/%d/%Y %H:%M:%S %p")
    df = format_date_time(df, "dropoff_datetime", "strftime", "%m/%d/%Y %H:%M:%S %p")
    df = df[headers]
    df = remove_null_rows(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, truncate_file)
    # import pdb; pdb.set_trace()
    logging.info(f"Processing Batch {target_file_batch} completed")


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Renaming headers...")
    df.rename(columns=rename_mappings, inplace=True)
    return df


def remove_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Removing Null rows... ")
    df = df.dropna(axis=0, subset=["vendor_id"])
    return df


def format_date_time(
    df: pd.DataFrame, field_name: str, str_pf_time: str, dt_format: str
) -> pd.DataFrame:
    if str_pf_time == "strptime":
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from datetime to {dt_format}  "
        )
        df[field_name] = df[field_name].apply(lambda x: datetime.strptime(x, dt_format))
    else:
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from {dt_format} to datetime "
        )
        df[field_name] = df[field_name].apply(lambda x: x.strftime(dt_format))
    return df


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path, index=False)


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if skip_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
        )
        next(data_file)
    else:
        logging.info(f"Appending batch file {batch_file_path} to {target_file_path}")
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


def upload_file_to_gcs(
    file_path: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    if os.path.exists(file_path):
        logging.info(
            f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket(target_gcs_bucket)
        blob = bucket.blob(target_gcs_path)
        blob.upload_from_filename(file_path)
    else:
        logging.info(
            f"Cannot upload file to gs://{target_gcs_bucket}/{target_gcs_path} as it does not exist."
        )


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
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
