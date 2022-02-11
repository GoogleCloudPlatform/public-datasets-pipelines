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


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    transform_list: typing.List[str],
    regex_list: typing.List[typing.List],
    logging_english_name: str,
    reorder_headers_list: typing.List[str],
    new_column_list: typing.List[str],
    rename_headers_list: dict,
    date_format_list: dict,
) -> None:

    logging.info(f"{logging_english_name} started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    dest_path = os.path.split(source_file)[0]
    source_file_zipped = dest_path + "/" + os.path.basename(source_url)
    download_file(source_url, source_file_zipped)
    zip_decompress(source_file_zipped, dest_path)
    source_file_unzipped = (
        dest_path + "/" + os.path.basename(source_url).replace(".zip", "")
    )
    os.unlink(source_file_zipped)
    convert_json_file_to_csv(source_file_unzipped, source_file)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
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
                transform_list=transform_list,
                rename_headers_list=rename_headers_list,
                regex_list=regex_list,
                date_format_list=date_format_list,
                new_column_list=new_column_list,
                reorder_headers_list=reorder_headers_list,
            )

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(f"{logging_english_name} completed")


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    src_file = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in src_file:
            f.write(chunk)


def zip_decompress(infile: str, destpath: str = "./files") -> None:
    logging.info(f"Decompressing {infile}")
    with ZipFile(file=infile, mode="r", allowZip64=True) as zip:
        zip.extractall(path=destpath)


def convert_json_file_to_csv(json_file: str, csv_dest_file: str):
    logging.info(f"Converting JSON file {json_file} to CSV format {csv_dest_file}")
    file_ref = open(
        json_file.strip(),
    )
    json_data = json.load(file_ref)
    df = pd.DataFrame(json_data["results"])
    df = normalize_column_data(df, "openfda")
    df.to_csv(csv_dest_file, index=False)


def normalize_column_data(df: pd.DataFrame, flatten_column: str) -> pd.DataFrame:
    df_norm = pd.json_normalize(df[flatten_column])
    for col in df_norm.columns:
        new_col_name = f"{flatten_column}_{col}"
        df_norm.columns = df_norm.columns.str.replace(col, new_col_name)
    df = df.merge(df_norm, how="left", left_index=True, right_index=True)
    return df


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    transform_list: list,
    rename_headers_list: dict,
    regex_list: dict,
    new_column_list: dict,
    date_format_list: list,
    reorder_headers_list: list,
) -> None:
    for transform in transform_list:
        if transform == "rename_headers":
            df = rename_headers(df, rename_headers_list)
        elif transform == "replace_regex":
            df = replace_regex(df, regex_list)
        elif transform == "add_column":
            df = add_column(df, new_column_list)
        elif transform == "convert_date_format":
            df = resolve_date_format(df, date_format_list)
        elif transform == "trim_whitespace":
            df = trim_whitespace(df)
        elif transform == "reorder_headers":
            df = reorder_headers(df, reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def rename_headers(df: pd.DataFrame, header_list: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    header_names = header_list
    df.rename(columns=header_names)
    return df


def replace_regex(df: pd.DataFrame, regex_list: dict) -> pd.DataFrame:
    for regex_item in regex_list:
        field_name = regex_item[0]
        search_expr = regex_item[1][0]
        replace_expr = regex_item[1][1]
        logging.info(f"Replacing data via regex on field {field_name}")
        df[field_name].replace(search_expr, replace_expr, regex=True, inplace=True)
    return df


def add_column(df: pd.DataFrame, new_column_list: list) -> pd.DataFrame:
    for col in new_column_list:
        logging.info(f"Adding column {col}")
        df[col] = ""
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


def reorder_headers(df: pd.DataFrame, headers_list: list) -> pd.DataFrame:
    logging.info("Reordering Headers")
    df = df[headers_list]
    return df


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtypes == "object":
            df[col] = df[col].apply(lambda x: str(x).strip())
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
        transform_list=json.loads(os.environ["TRANSFORM_LIST"]),
        regex_list=json.loads(os.environ["REGEX_LIST"]),
        logging_english_name=os.environ["LOGGING_ENGLISH_NAME"],
        reorder_headers_list=json.loads(os.environ["REORDER_HEADERS_LIST"]),
        new_column_list=json.loads(os.environ["NEW_COLUMN_LIST"]),
        rename_headers_list=json.loads(os.environ["RENAME_HEADERS_LIST"]),
        date_format_list=json.loads(os.environ["DATE_FORMAT_LIST"]),
    )
