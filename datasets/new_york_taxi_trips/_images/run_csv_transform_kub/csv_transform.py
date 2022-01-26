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
import math
import os
import pathlib
import typing
from datetime import datetime, timedelta

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
    integer_string_col: typing.List[str],
) -> None:
    logging.info("New York taxi trips - green trips process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    start_date_year = int(
        datetime.strftime((datetime.now() + timedelta(days=-1825)), "%Y")
    )
    current_year = int(datetime.strftime(datetime.now(), "%Y"))
    for year_data in range(start_date_year, (current_year + 1)):
        for month_data in range(1, 13):
            process_month = str(year_data) + "-" + str(month_data).zfill(2)
            print(process_month)
            source_url_to_process = source_url + process_month + ".csv"
            successful_download = download_file(source_url_to_process, source_file)
            if successful_download:
                with pd.read_csv(
                    source_file,
                    engine="python",
                    encoding="utf-8",
                    quotechar='"',
                    chunksize=int(chunksize),
                ) as reader:
                    for chunk_number, chunk in enumerate(reader):
                        logging.info(f"Processing batch {chunk_number}")
                        target_file_batch = str(target_file).replace(
                            ".csv", "-" + str(chunk_number) + ".csv"
                        )
                        df = pd.DataFrame()
                        df = pd.concat([df, chunk])
                        process_chunk(
                            df,
                            target_file_batch,
                            target_file,
                            (not chunk_number == 0),
                            headers,
                            rename_mappings,
                            pipeline_name,
                            integer_string_col,
                        )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
    logging.info("New York taxi trips - green trips process completed")


def download_file(source_url: str, source_file: pathlib.Path) -> bool:
    logging.info(f"Downloading {source_url} into {source_file}")
    success = False
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            if chunk.find((b"<Code>NoSuchKey</Code>")):
                # return fail if the file contains no-such-key
                success = False
                break
            else:
                f.write(chunk)
                success = True
    if success:
        logging.info(f"Download {source_url} to {source_file} complete.")
    else:
        logging.info(f"Unable to download {source_url} to {source_file} at this time.  The URL may not exist.")
    return success


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
    integer_string_col: typing.List[str],
) -> None:
    df = rename_headers(df, rename_mappings)
    df = remove_null_rows(df)

    if pipeline_name == "ny_green_trips":
        df["distance_between_service"] = ""
        df["time_between_service"] = ""
        df = format_date_time(df, "pickup_datetime", "strptime", "%Y-%m-%d %H:%M:%S")
        df = format_date_time(df, "dropoff_datetime", "strptime", "%Y-%m-%d %H:%M:%S")
    df = format_date_time(df, "pickup_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = format_date_time(df, "dropoff_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = convert_values_to_integer_string(df, integer_string_col)
    df = df[headers]
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing Batch {target_file_batch} completed")


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info(" Renaming headers...")
    df.rename(columns=rename_mappings, inplace=True)
    return df


def remove_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Transform: Removing Null rows... ")
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


def convert_values_to_integer_string(
    df: pd.DataFrame, integer_string_col: typing.List
) -> None:
    logging.info("Transform: Converting to integers..")
    for cols in integer_string_col:
        df[cols] = df[cols].apply(convert_to_integer_string)
    return df


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    if not input or (math.isnan(input)):
        return ""
    return str(int(round(input, 0)))


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
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        integer_string_col=json.loads(os.environ["INTEGER_STRING_COL"]),
    )
