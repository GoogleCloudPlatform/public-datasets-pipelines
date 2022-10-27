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
# import subprocess
import typing

import pandas as pd
import requests
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound


def main(
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    rename_headers_list: dict,
    int_cols_list: typing.List[str],
    date_format_list: dict,
) -> None:
    logging.info(f"{pipeline_name} process started")
    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        chunksize=chunksize,
        source_file=source_file,
        target_file=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=destination_table,
        schema_path=schema_path,
        rename_headers_list=rename_headers_list,
        int_cols_list=int_cols_list,
        date_format_list=date_format_list,
    )
    # download_file_http(source_url, source_file)
    # logging.info(f"Opening batch file {source_file}")
    # with pd.read_csv(
    #     source_file, engine="python", encoding="utf-8", quotechar='"', chunksize=chunksz
    # ) as reader:
    #     for chunk_number, chunk in enumerate(reader):
    #         logging.info(f"Processing batch {chunk_number}")
    #         target_file_batch = str(target_file).replace(
    #             ".csv", "-" + str(chunk_number) + ".csv"
    #         )
    #         df = pd.DataFrame()
    #         df = pd.concat([df, chunk])
    #         processChunk(df, target_file_batch)
    #         logging.info(f"Appending batch {chunk_number} to {target_file}")
    #         if chunk_number == 0:
    #             subprocess.run(["cp", target_file_batch, target_file])
    #         else:
    #             subprocess.check_call(f"sed -i '1d' {target_file_batch}", shell=True)
    #             subprocess.check_call(
    #                 f"cat {target_file_batch} >> {target_file}", shell=True
    #             )
    #         subprocess.run(["rm", target_file_batch])
    # logging.info(
    #     f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    # )
    # upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
    logging.info("Austin 311 Service Requests By Year process completed")


def execute_pipeline(
    source_url: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    rename_headers_list: dict,
    int_cols_list: typing.List[str],
    date_format_list: dict,
) -> None:
    if destination_table == "311_service_requests":
        # download_file_http(source_url, source_file)
        process_source_file(
            source_file=source_file,
            target_file=target_file,
            input_headers=input_headers,
            output_headers=output_headers,
            dtypes=data_dtypes,
            chunksize=chunksize,
            field_delimiter=field_delimiter,
            rename_headers_list=rename_headers_list,
        )
        load_data_to_bq(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_name,
            file_path=target_file,
            field_delimiter=field_delimiter,
            truncate_table=False,
        )
        if os.path.exists(target_file):
            upload_file_to_gcs(
                file_path=target_file,
                target_gcs_bucket=target_gcs_bucket,
                target_gcs_path=target_gcs_path,
            )
        if remove_file:
            os.remove(source_file)
            os.remove(source_csv_file)
            os.remove(target_file)
        else:
            pass
    else:
        pass


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
    table_clustering_field_list: typing.List[str] = [],
    table_description: str = "",
    table_partition_field: str = "",
    table_partition_field_type: str = "",
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
            if table_clustering_field_list:
                logging.info(
                    f"Creating cluster on table ({table_clustering_field_list})"
                )
                table.clustering_fields = table_clustering_field_list
            if table_partition_field:
                logging.info(
                    f"Creating partition on table ({table_partition_field}, {table_partition_field_type})"
                )
                table.partitioning_type = table_partition_field_type
                table.time_partitioning.field = table_partition_field
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


def processChunk(df: pd.DataFrame, target_file_batch: str) -> None:
    logging.info("Transforming.")
    rename_headers(df)
    convert_values(df)
    delete_newlines_from_column(df, col_name="location")
    filter_null_rows(df)
    logging.info("Saving to target file.. {target_file_batch}")
    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving to target file: {e}.")
    logging.info(f"Saved transformed source data to target file .. {target_file_batch}")


def convert_dt_format(dt_str: str) -> str:
    # if the format is %m/%d/%Y then...
    if str(dt_str).strip()[3] == "/":
        return datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    else:
        return str(dt_str)


def convert_values(df: pd.DataFrame) -> None:
    dt_cols = [
        "status_change_date",
        "created_date",
        "last_update_date",
        "close_date",
    ]
    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)
    int_cols = ["council_district_code"]
    for int_col in int_cols:
        df[int_col] = df[int_col].astype("int32")


def delete_newlines(val: str) -> str:
    return val.replace("\n", "")


def delete_newlines_from_column(df: pd.DataFrame, col_name: str) -> None:
    if df[col_name] is not None & df[col_name].str.len() > 0:
        df[col_name] = df[col_name].apply(delete_newlines)


def filter_null_rows(df: pd.DataFrame) -> None:
    df = df[df.unique_key != ""]


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.export_csv(file_path)


def download_file_http(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading file {source_url} to {source_file}")
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
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        rename_headers_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"{}")),
        int_cols_list=json.loads(os.environ.get("INT_COLS_LIST", r"[]")),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"{}")),
    )
