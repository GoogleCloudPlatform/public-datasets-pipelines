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
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    pipeline_name: str,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    remove_source_file: str,
    delete_target_file: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: dict,
    table_description: str,
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        drop_dest_table=drop_dest_table,
        input_field_delimiter=input_field_delimiter,
        remove_source_file=remove_source_file,
        delete_target_file=delete_target_file,
        input_csv_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        rename_headers_list=rename_headers_list,
        table_description=table_description,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    remove_source_file: str,
    delete_target_file: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: dict,
    table_description: str,
) -> None:
    download_file(source_url, source_file)
    process_source_file(
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        input_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        rename_headers_list=rename_headers_list,
        header_row_ordinal="0",
        field_separator=input_field_delimiter,
    )
    if os.path.exists(target_file):
        upload_file_to_gcs(
            file_path=target_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
            drop_table=(drop_dest_table == "Y"),
            table_description=table_description,
        )
        if table_exists:
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=destination_table,
                file_path=target_file,
                truncate_table=True,
                field_delimiter="|",
            )
            if remove_source_file == "Y":
                os.remove(source_file)
            else:
                pass
            if delete_target_file == "Y":
                os.remove(target_file)
            else:
                pass
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def process_source_file(
    source_url: str,
    source_file: str,
    target_file: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: typing.List[str],
    header_row_ordinal: str = "0",
    field_separator: str = ",",
) -> None:
    logging.info(f"Opening source file {source_file}")
    if header_row_ordinal is None or header_row_ordinal == "None":
        with pd.read_csv(
            source_file,
            engine="python",
            encoding="utf-8",
            quotechar='"',
            chunksize=int(chunksize),  # size of batch data, in no. of records
            sep=field_separator,  # data column separator, typically ","
            names=input_headers,
            dtype=data_dtypes,
            keep_default_na=True,
            na_values=[" "],
        ) as reader:
            for chunk_number, chunk in enumerate(reader):
                target_file_batch = str(target_file).replace(
                    ".csv", "-" + str(chunk_number) + ".csv"
                )
                df = pd.DataFrame()
                df = pd.concat([df, chunk])
                process_chunk(
                    df=df,
                    source_url=source_url,
                    target_file_batch=target_file_batch,
                    target_file=target_file,
                    skip_header=(not chunk_number == 0),
                    rename_headers_list=rename_headers_list,
                )
    else:
        header = int(header_row_ordinal)
        if data_dtypes != "[]":
            with pd.read_csv(
                source_file,
                engine="python",
                encoding="utf-8",
                quotechar='"',
                chunksize=int(chunksize),  # size of batch data, in no. of records
                sep=field_separator,  # data column separator, typically ","
                header=header,  # use when the data file does not contain a header
                dtype=data_dtypes,
                keep_default_na=True,
                na_values=[" "],
            ) as reader:
                for chunk_number, chunk in enumerate(reader):
                    target_file_batch = str(target_file).replace(
                        ".csv", "-" + str(chunk_number) + ".csv"
                    )
                    df = pd.DataFrame()
                    df = pd.concat([df, chunk])
                    process_chunk(
                        df=df,
                        source_url=source_url,
                        target_file_batch=target_file_batch,
                        target_file=target_file,
                        skip_header=(not chunk_number == 0),
                        rename_headers_list=rename_headers_list,
                    )
        else:
            with pd.read_csv(
                source_file,
                engine="python",
                encoding="utf-8",
                quotechar='"',
                chunksize=int(chunksize),  # size of batch data, in no. of records
                sep=field_separator,  # data column separator, typically ","
                header=header,  # use when the data file does not contain a header
                keep_default_na=True,
                na_values=[" "],
            ) as reader:
                for chunk_number, chunk in enumerate(reader):
                    target_file_batch = str(target_file).replace(
                        ".csv", "-" + str(chunk_number) + ".csv"
                    )
                    df = pd.DataFrame()
                    df = pd.concat([df, chunk])
                    process_chunk(
                        df=df,
                        source_url=source_url,
                        target_file_batch=target_file_batch,
                        target_file=target_file,
                        skip_header=(not chunk_number == 0),
                        rename_headers_list=rename_headers_list,
                    )


def process_chunk(
    df: pd.DataFrame,
    source_url: str,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    rename_headers_list: typing.List[str],
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = rename_headers(df, rename_headers_list)
    df = add_metadata_cols(df, source_url)
    save_to_new_file(df, file_path=str(target_file_batch), sep="|")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
    field_delimiter: str = "|",
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = field_delimiter
    if truncate_table:
        job_config.write_disposition = "WRITE_TRUNCATE"
    else:
        job_config.write_disposition = "WRITE_APPEND"
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
    drop_table: bool = False,
    table_description="",
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    table_exists = False
    try:
        table = client.get_table(table_ref)
        table_exists_id = table.table_id
        logging.info(f"Table {table_exists_id} currently exists.")
        if drop_table:
            logging.info("Dropping existing table")
            client.delete_table(table)
            table = None
    except NotFound:
        table = None
    if not table:
        logging.info(
            (
                f"Table {table_ref} currently does not exist.  Attempting to create table."
            )
        )
        if check_gcs_file_exists(schema_filepath, bucket_name):
            schema = create_table_schema([], bucket_name, schema_filepath)
            table = bigquery.Table(table_ref, schema=schema)
            table.description = table_description
            client.create_table(table)
            print(f"Table {table_ref} was created".format(table_id))
            table_exists = True
        else:
            file_name = os.path.split(schema_filepath)[1]
            file_path = os.path.split(schema_filepath)[0]
            logging.info(
                f"Error: Unable to create table {table_ref} because schema file {file_name} does not exist in location {file_path} in bucket {bucket_name}"
            )
            table_exists = False
    else:
        table_exists = True
    return table_exists


def check_gcs_file_exists(file_path: str, bucket_name: str) -> bool:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    exists = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)
    return exists


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


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    return df.rename(columns=rename_mappings)


def add_metadata_cols(df: pd.DataFrame, source_url: str) -> pd.DataFrame:
    logging.info("Adding metadata columns")
    df["source_url"] = source_url
    df["etl_timestamp"] = pd.to_datetime(
        datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S", infer_datetime_format=True
    )
    return df


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    with open(batch_file_path, "r") as data_file:
        if truncate_file:
            target_file = open(target_file_path, "w+").close()
        with open(target_file_path, "a+") as target_file:
            if skip_header:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
                )
                next(data_file)
            else:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path}"
                )
            target_file.write(data_file.read())
            if os.path.exists(batch_file_path):
                os.remove(batch_file_path)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


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
        pipeline_name=os.environ["PIPELINE_NAME"],
        chunksize=os.environ["CHUNKSIZE"],
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        schema_path=os.environ["SCHEMA_PATH"],
        drop_dest_table=os.environ["DROP_DEST_TABLE"],
        input_field_delimiter=os.environ["INPUT_FIELD_DELIMITER"],
        remove_source_file=os.environ["REMOVE_SOURCE_FILE"],
        delete_target_file=os.environ["DELETE_TARGET_FILE"],
        input_csv_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", r"{}")),
        table_description=os.environ.get("TABLE_DESCRIPTION", ""),
    )
