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
from zipfile import ZipFile

import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_url: str,
    pipeline_name: str,
    source_file: pathlib.Path,
    source_file_unzipped: str,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    rename_mappings: dict,
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_file=source_file,
        source_file_unzipped=source_file_unzipped,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        schema_path=schema_path,
        chunksize=chunksize,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        input_headers=input_headers,
        rename_mappings=rename_mappings,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    source_file_unzipped: str,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    rename_mappings: dict,
) -> None:
    if destination_table == "tract_outcomes":
        source_zipfile = str.replace(str(source_file), ".csv", ".zip")
        source_file_path = source_file.parent
        download_file(source_url=source_url, source_file=source_zipfile)
        zip_decompress(
            infile=source_zipfile, topath=source_file_path, remove_zipfile=True
        )
        os.rename(source_file_unzipped, target_file)
    else:
        download_file(source_url, source_file)
        process_source_file(
            source_file=source_file,
            target_file=target_file,
            chunksize=chunksize,
            input_headers=input_headers,
            rename_mappings=rename_mappings,
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
        )
        if table_exists:
            if destination_table == "tract_outcomes":
                load_data_to_bq(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=destination_table,
                    file_path=target_file,
                    truncate_table=True,
                    field_delimiter=",",
                )
            else:
                load_data_to_bq(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=destination_table,
                    file_path=target_file,
                    truncate_table=True,
                    field_delimiter="|",
                )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def process_source_file(
    source_file: str,
    target_file: str,
    chunksize: str,
    input_headers: typing.List[str],
    rename_mappings: dict,
) -> None:
    logging.info(f"Opening source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=0,  # use when the data file does not contain a header
        names=input_headers,
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
                target_file_batch=target_file_batch,
                target_file=target_file,
                skip_header=(not chunk_number == 0),
                rename_headers_list=rename_mappings,
            )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    rename_headers_list: list,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = rename_headers(df, rename_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch), sep="|")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


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
    logging.info(f"Downloading file {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def zip_decompress(infile: str, topath: str, remove_zipfile: bool = False) -> None:
    logging.info(f"Decompressing {infile} to {topath}")
    with ZipFile(infile, "r") as zip:
        zip.extractall(topath)
    if remove_zipfile:
        os.unlink(infile)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Renaming Headers")
    df.rename(columns=rename_mappings, inplace=True)
    return df


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
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    table_exists = False
    try:
        table = client.get_table(table_ref)
        table_exists_id = table.table_id
        logging.info(f"Table {table_exists_id} currently exists.")
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


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, float_format="%.0f", index=False, sep=sep)


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
        pipeline_name=os.environ["PIPELINE_NAME"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        source_file_unzipped=pathlib.Path(
            os.environ["SOURCE_FILE_UNZIPPED"]
        ).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        schema_path=os.environ["SCHEMA_PATH"],
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        input_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
    )
