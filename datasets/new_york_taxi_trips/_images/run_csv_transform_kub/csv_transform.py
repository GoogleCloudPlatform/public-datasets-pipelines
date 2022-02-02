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
from datetime import datetime

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_years_to_load: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
    pipeline_name: str,
) -> None:
    logging.info(f"New York taxi trips - {pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url,
        source_years_to_load,
        str(source_file),
        str(target_file),
        chunksize,
        input_headers,
        data_dtypes,
        output_headers,
        pipeline_name,
        target_gcs_bucket,
        target_gcs_path,
    )

    logging.info(f"New York taxi trips - {pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_years_to_load: str,
    source_file: str,
    target_file: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
    pipeline_name: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    for year_number in source_years_to_load.split("|"):
        target_file_name = str.replace(target_file, ".csv", "_" + year_number + ".csv")
        process_year_data(
            source_url,
            int(year_number),
            source_file,
            target_file,
            target_file_name,
            chunksize,
            input_headers,
            data_dtypes,
            output_headers,
            pipeline_name,
            target_gcs_bucket,
            target_gcs_path,
        )


def process_year_data(
    source_url: str,
    year_number: int,
    source_file: str,
    target_file: str,
    target_file_name: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
    pipeline_name: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    logging.info(f"Processing year {year_number}")
    for month_number in range(1, 13):
        process_month(
            source_url,
            year_number,
            month_number,
            source_file,
            target_file,
            target_file_name,
            chunksize,
            input_headers,
            data_dtypes,
            output_headers,
            pipeline_name,
            target_gcs_bucket,
            target_gcs_path,
        )
    upload_file_to_gcs(
        target_file_name,
        target_gcs_bucket,
        str(target_gcs_path).replace(".csv", "_" + str(year_number) + ".csv"),
    )
    logging.info(f"Processing year {year_number} completed")


def process_month(
    source_url: str,
    year_number: int,
    month_number: int,
    source_file: str,
    target_file: str,
    target_file_name: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
    pipeline_name: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    process_month = str(year_number) + "-" + str(month_number).zfill(2)
    logging.info(f"Processing {process_month} started")
    source_url_to_process = source_url + process_month + ".csv"
    source_file_to_process = str(source_file).replace(
        ".csv", "_" + process_month + ".csv"
    )
    successful_download = download_file(source_url_to_process, source_file_to_process)
    if successful_download:
        with pd.read_csv(
            source_file_to_process,
            engine="python",
            encoding="utf-8",
            quotechar='"',
            chunksize=int(chunksize),
            sep=",",
            names=input_headers,
            skiprows=1,
            dtype=data_dtypes,
        ) as reader:
            for chunk_number, chunk in enumerate(reader):
                logging.info(
                    f"Processing chunk #{chunk_number} of file {process_month} started"
                )
                target_file_batch = str(target_file).replace(
                    ".csv", "-" + process_month + "-" + str(chunk_number) + ".csv"
                )
                df = pd.DataFrame()
                df = pd.concat([df, chunk])
                process_chunk(
                    df,
                    target_file_batch,
                    target_file_name,
                    month_number == 1 and chunk_number == 0,
                    month_number == 1 and chunk_number == 0,
                    output_headers,
                    pipeline_name,
                )
                logging.info(
                    f"Processing chunk #{chunk_number} of file {process_month} completed"
                )
    logging.info(f"Processing {process_month} completed")


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
    include_header: bool,
    truncate_file: bool,
    output_headers: typing.List[str],
    pipeline_name: str,
) -> None:
    if pipeline_name == "tlc_green_trips":
        df["distance_between_service"] = ""
        df["time_between_service"] = ""
    df = format_date_time(df, "pickup_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = format_date_time(df, "dropoff_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = remove_null_rows(df)
    df = df[output_headers]
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, include_header, truncate_file)
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
        df[field_name] = df[field_name].dt.strftime(dt_format)
    return df


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path, index=False)


def append_batch_file(
    batch_file_path: str,
    target_file_path: str,
    include_header: bool,
    truncate_target_file: bool,
) -> None:
    logging.info(
        f"testing: Appending file {batch_file_path} to file {target_file_path} with include_header={include_header} and truncate_target_file={truncate_target_file}"
    )
    data_file = open(batch_file_path, "r")
    if truncate_target_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if not include_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} without header"
        )
        next(data_file)
    else:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with header"
        )
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
        source_years_to_load=os.environ["SOURCE_YEARS_TO_LOAD"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        input_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        output_headers=json.loads(os.environ["OUTPUT_CSV_HEADERS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
