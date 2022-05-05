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
    english_pipeline_name: str,
    source_dtypes: dict,
    transform_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:

    logging.info(f"{english_pipeline_name} process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file(source_url, source_file)

    process_source_file(
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        source_dtypes=source_dtypes,
        transform_list=transform_list,
        reorder_headers_list=reorder_headers_list,
        rename_headers_list=rename_headers_list,
        regex_list=regex_list,
        crash_field_list=crash_field_list,
        date_format_list=date_format_list,
    )

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(f"{english_pipeline_name} process completed")


def process_source_file(
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    source_dtypes: dict,
    transform_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:
    logging.info(f"Opening source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        sep=",",
        dtype=source_dtypes,
        chunksize=int(chunksize),
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df=df,
                target_file_batch=target_file_batch,
                target_file=target_file,
                skip_header=(not chunk_number == 0),
                transform_list=transform_list,
                reorder_headers_list=reorder_headers_list,
                rename_headers_list=rename_headers_list,
                regex_list=regex_list,
                crash_field_list=crash_field_list,
                date_format_list=date_format_list,
            )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    transform_list: list,
    reorder_headers_list: list,
    rename_headers_list: list,
    regex_list: list,
    crash_field_list: list,
    date_format_list: list,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    for transform in transform_list:
        if transform == "replace_regex":
            df = replace_regex(df, regex_list)
        elif transform == "add_crash_timestamp":
            for fld in crash_field_list:
                new_crash_field = fld[0]
                crash_date_field = fld[1]
                crash_time_field = fld[2]
                df[new_crash_field] = ""
                df = add_crash_timestamp(
                    df, new_crash_field, crash_date_field, crash_time_field
                )
        elif transform == "convert_date_format":
            df = resolve_date_format(df, date_format_list)
        elif transform == "resolve_datatypes":
            df = resolve_datatypes(df)  # column_data_types_list)
        elif transform == "rename_headers":
            df = rename_headers(df, rename_headers_list)
        elif transform == "reorder_headers":
            df = reorder_headers(df, reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def resolve_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving column datatypes")
    convert_dict = {
        "latitude": float,
        "longitude": float,
        "number_of_cyclist_injured": int,
        "number_of_cyclist_killed": int,
        "number_of_motorist_injured": int,
        "number_of_motorist_killed": int,
        "number_of_pedestrians_injured": int,
        "number_of_pedestrians_killed": int,
        "number_of_persons_injured": int,
        "number_of_persons_killed": int,
    }
    df = df.astype(convert_dict, errors="ignore")
    return df


def reorder_headers(df: pd.DataFrame, headers_list: list) -> pd.DataFrame:
    logging.info("Reordering Headers")
    import pdb

    pdb.set_trace
    df = df[headers_list]
    return df


def rename_headers(df: pd.DataFrame, header_list: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    header_names = header_list
    df.rename(columns=header_names, inplace=True)
    return df


def replace_regex(df: pd.DataFrame, regex_list: dict) -> pd.DataFrame:
    for regex_item in regex_list:
        field_name = regex_item[0]
        search_expr = regex_item[1]
        replace_expr = regex_item[2]
        logging.info(
            f"Replacing data via regex on field {field_name} '{field_name}' '{search_expr}' '{replace_expr}'"
        )
        df[field_name] = df[field_name].replace(
            r"" + search_expr, replace_expr, regex=True
        )
    return df


def resolve_date_format(df: pd.DataFrame, date_fields: list = []) -> pd.DataFrame:
    logging.info("Resolving Date Format")
    for dt_fld in date_fields:
        field_name = dt_fld[0]
        from_format = dt_fld[1]
        to_format = dt_fld[2]
        df[field_name] = df[field_name].apply(
            lambda x: convert_dt_format(str(x), from_format, to_format)
        )
    return df


def convert_dt_format(
    dt_str: str, from_format: str, to_format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        dt_str = ""
        return dt_str
    else:
        if from_format == "%Y%m%d":
            year = dt_str[0:4]
            month = dt_str[4:6]
            day = dt_str[6:8]
            dt_str = f"{year}-{month}-{day} 00:00:00"
            from_format = "%Y-%m-%d %H:%M:%S"
        elif len(dt_str.strip().split(" ")[1]) == 8:
            # if format of time portion is 00:00:00 then use 00:00 format
            dt_str = dt_str[:-3]
        elif (len(dt_str.strip().split("-")[0]) == 4) and (
            len(from_format.strip().split("/")[0]) == 2
        ):
            # if the format of the date portion of the data is in YYYY-MM-DD format
            # and from_format is in MM-DD-YYYY then resolve this by modifying the from_format
            # to use the YYYY-MM-DD.  This resolves mixed date formats in files
            from_format = "%Y-%m-%d " + from_format.strip().split(" ")[1]
        return datetime.datetime.strptime(dt_str, from_format).strftime(to_format)


def add_crash_timestamp(
    df: pd.DataFrame, new_crash_field: str, crash_date_field: str, crash_time_field: str
) -> pd.DataFrame:
    logging.info(
        f"add_crash_timestamp '{new_crash_field}' '{crash_date_field}' '{crash_time_field}'"
    )
    df[new_crash_field] = df.apply(
        lambda x, crash_date_field, crash_time_field: crash_timestamp(
            x["" + crash_date_field], x["" + crash_time_field]
        ),
        args=[crash_date_field, crash_time_field],
        axis=1,
    )
    return df


def crash_timestamp(crash_date: str, crash_time: str) -> str:
    # if crash time format is H:MM then convert to HH:MM:SS
    if len(crash_time) == 4:
        crash_time = f"0{crash_time}:00"
    return f"{crash_date} {crash_time}"


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
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


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
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
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        english_pipeline_name=os.environ["ENGLISH_PIPELINE_NAME"],
        source_dtypes=json.loads(os.environ["SOURCE_DTYPES"]),
        transform_list=json.loads(os.environ["TRANSFORM_LIST"]),
        reorder_headers_list=json.loads(os.environ["REORDER_HEADERS_LIST"]),
        rename_headers_list=json.loads(os.environ["RENAME_HEADERS_LIST"]),
        regex_list=json.loads(os.environ["REGEX_LIST"]),
        crash_field_list=json.loads(os.environ["CRASH_FIELD_LIST"]),
        date_format_list=json.loads(os.environ["DATE_FORMAT_LIST"]),
    )
