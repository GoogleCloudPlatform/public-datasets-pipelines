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
from google.cloud import storage, bigquery


def main(
    pipeline_name: str,
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    data_dtypes: typing.List[str],
    parse_dates: dict,
    rename_headers_list: dict,
    output_headers_list: typing.List[str]
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        chunksize=chunksize,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        data_dtypes=data_dtypes,
        parse_dates=parse_dates,
        rename_headers_list=rename_headers_list,
        output_headers_list=output_headers_list)
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    data_dtypes: typing.List[str],
    parse_dates: dict,
    rename_headers_list: dict,
    output_headers_list: typing.List[str]
) -> None:
    download_file(
        source_url,
        source_file
    )
    process_source_file(
        source_file,
        target_file,
        chunksize,
        data_dtypes,
        parse_dates,
        rename_headers_list,
        output_headers_list
    )
    if os.path.exists(target_file):
        upload_file_to_gcs(
            target_file=target_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path
        )
        create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            schema_path=schema_path,
            target_gcs_bucket=target_gcs_bucket
        )
        load_data_to_bq(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            target_file=target_file
        )
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data was available for year {year_number}.  Continuing."
        )



def process_source_file(
        source_file: str,
        target_file: str,
        chunksize: str,
        data_dtypes: dict,
        parse_dates_list: typing.List[str],
        rename_headers_list: dict,
        output_headers_list: typing.List[str]
) -> None:
    logging.info(f"Processing file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),
        dtype=data_dtypes,
        parse_dates=parse_dates_list,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
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
                            rename_headers_list=rename_headers_list,
                            parse_dates_list=parse_dates_list,
                            reorder_headers_list=output_headers_list
                        )


def load_data_to_bq(
    project_id: str, dataset_id: str, table_id: str, file_path: str
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = "|"
    job_config.skip_leading_rows = 1  # ignore the header
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} completed"
    )


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_filepath: list,
    bucket_name: str,
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    success = False
    try:
        table_exists_id = client.get_table(table_ref).table_id
        logging.info(f"Table {table_exists_id} currently exists.")
        success = True
    except NotFound:
        logging.info(
            (
                f"Table {table_ref} currently does not exist.  Attempting to create table."
            )
        )
        schema = create_table_schema([], bucket_name, schema_filepath)
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Table {table_ref} was created".format(table_id))
        success = True
    return success


def create_table_schema(
    schema_structure: list, bucket_name: str = "", schema_filepath: str = ""
) -> list:
    logging.info(f"Defining table schema... {bucket_name} ... {schema_filepath}")
    schema = []
    if not (schema_filepath):
        schema_struct = schema_structure
    else:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(schema_filepath)
        schema_struct = json.loads(blob.download_as_string(client=None))
    for schema_field in schema_struct:
        fld_name = schema_field["name"]
        fld_type = schema_field["type"]
        try:
            fld_descr = schema_field["description"]
        except KeyError:
            fld_descr = ""
        fld_mode = schema_field["mode"]
        schema.append(
            bigquery.SchemaField(
                name=fld_name, field_type=fld_type, mode=fld_mode, description=fld_descr
            )
        )
    return schema


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
        logging.info("file truncated")
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


def process_chunk(
        df: pd.DataFrame,
        target_file_batch: str,
        target_file: str,
        skip_header: bool,
        rename_headers_list: dict,
        parse_dates_list: typing.List[str],
        reorder_headers_list: typing.List[str]
) -> None:
    df = rename_headers(df, rename_headers_list)
    df = remove_null_rows(df)
    df = resolve_date_format(df, parse_dates_list)
    df = reorder_headers(df, reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def remove_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Removing rows with empty keys")
    df = df[df["unique_key"] != ""]
    return df


def reorder_headers(df: pd.DataFrame, headers: typing.List[str]) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[ headers ]
    return df


def resolve_date_format(df: pd.DataFrame, parse_dates: typing.List[str]) -> pd.DataFrame:
    logging.info("Resolve Date Format")
    for dt_fld in parse_dates:
        df[dt_fld] = df[dt_fld].apply(convert_dt_format)
    return df


def convert_dt_format(dt_str: str) -> str:
    logging.info(f"Converting column {dt_str} format")
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif (
        dt_str.strip()[2] == "/"
    ):  # if there is a '/' in 3rd position, then we have a date format mm/dd/yyyy
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def rename_headers(df: pd.DataFrame,
                   header_names: dict
) -> pd.DataFrame:
    logging.info("Renaming Headers")
    df = df.rename(columns=header_names)
    return df


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, seperator=sep)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading file {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


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
        pipeline_name=os.environ["PIPELINE_NAME"],
        source_url=os.environ["SOURCE_URL"],
        chunksize=os.environ["CHUNKSIZE"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        schema_path=os.environ["SCHEMA_PATH"],
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        parse_dates=json.loads(os.environ["PARSE_DATES"]),
        rename_headers_list=json.loads(os.environ["RENAME_HEADERS"]),
        output_headers_list=json.loads(os.environ["OUTPUT_CSV_HEADERS"])
    )
