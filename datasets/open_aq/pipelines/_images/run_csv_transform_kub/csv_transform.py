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

import csv
import datetime
import json
import logging
import os
import pathlib
import re
import sys
import time
import typing
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import requests
from google.api_core.exceptions import NotFound, BadRequest
from google.cloud import bigquery, storage
import sh


def main(
    pipeline_name: str,
    source_url: dict,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    date_format_list: typing.List[typing.List[str]]
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        pipeline_name=pipeline_name,
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        drop_dest_table=drop_dest_table,
        date_format_list=date_format_list
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    pipeline_name: str,
    source_url: dict,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    date_format_list: typing.List[typing.List[str]]
) -> None:
    for url_key, url in source_url.items():
        logging.info(f"Processing table: {url_key} at url: {url}")
        src_file = str.replace(str(source_file), ".json", f"_{url_key}.json")
        params = {
                    "format": "json"
                }
        response = requests.get(url, headers={"accept": "application/json"}, params=params)
        data = response.json() #convert to json
        df = pd.DataFrame.from_dict(data["results"]) #convert json to dataframe
        df = source_convert_date_formats(df, date_format_list=date_format_list)
        # df["firstUpdated"] = df["firstUpdated"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S"))
        # df["lastUpdated"] = df["lastUpdated"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S"))
        df = add_metadata_cols(df=df, source_url=url)
        target_json_file = str(target_file).replace(".json", f"_{url_key}.json")
        logging.info(f"Writing output file to {target_json_file}")
        df.to_json(target_json_file, orient="split")
        if os.path.exists(target_json_file):
            upload_file_to_gcs(
            file_path=target_json_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
        if drop_dest_table == "Y":
            drop_table = True
        else:
            drop_table = False
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=url_key,
            schema_filepath=schema_path.replace("_schema.json", f"_{url_key}_schema.json"),
            bucket_name=target_gcs_bucket,
            drop_table=drop_table,
        )
        if table_exists:
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=url_key,
                file_path=target_json_file,
                truncate_table=True,
                source_url=url,
                field_delimiter="|",
                source_file_type = "json"
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{url_key} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )
    import pdb; pdb.set_trace()


def download_file_http(
    source_url: str,
    source_file: pathlib.Path,
    continue_on_error: bool = False,
    quiet_mode: bool = False,
    no_of_retries: int = 5,
) -> bool:
    for retries in (0, no_of_retries):
        if not download_file_http_exec(
            source_url=source_url,
            source_file=source_file,
            continue_on_error=continue_on_error,
            quiet_mode=quiet_mode,
        ):
            logging.info(
                f"Unable to download file {source_url}.  Retry {retries} of {no_of_retries}"
            )
            time.sleep(3)
        else:
            return True
    return False


def download_file_http_exec(
    source_url: str,
    source_file: pathlib.Path,
    continue_on_error: bool = False,
    quiet_mode: bool = False,
) -> bool:
    if not quiet_mode:
        logging.info(f"Downloading {source_url} to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        rtn_status_code = src_file.status_code
        if 400 <= rtn_status_code <= 499:
            logging.info(
                f"Unable to download file {source_url} (error code was {rtn_status_code})"
            )
            return False
        else:
            with open(source_file, "wb") as f:
                for chunk in src_file:
                    f.write(chunk)
            return True
    except requests.exceptions.RequestException as e:
        if e == requests.exceptions.HTTPError:
            err_msg = "A HTTP error occurred."
        elif e == requests.exceptions.Timeout:
            err_msg = "A HTTP timeout error occurred."
        elif e == requests.exceptions.TooManyRedirects:
            err_msg = "Too Many Redirects occurred."
        if not continue_on_error:
            logging.info(f"{err_msg} Unable to obtain {source_url}")
            raise SystemExit(e)
        else:
            logging.info(f"{err_msg} Unable to obtain {source_url}.")
        return False


def set_df_datatypes(df: pd.DataFrame, data_dtypes: dict) -> pd.DataFrame:
    logging.info("Setting data types")
    for key, item in data_dtypes.items():
        df[key] = df[key].astype(item)
    return df


def add_metadata_cols(df: pd.DataFrame, source_url: str) -> pd.DataFrame:
    logging.info("Adding metadata columns")
    df["source_url"] = source_url
    df["etl_timestamp"] = pd.to_datetime(
        datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S", infer_datetime_format=True
    )
    return df


def convert_dt_format(
    dt_str: str, from_format: str = "%Y%m%d", to_format: str = "%Y-%m-%d"
) -> str:
    if not dt_str or dt_str.lower() == "nan":
        return dt_str
    else:
        return str(datetime.datetime.strptime(dt_str, from_format).strftime(to_format))


def source_convert_date_formats(
    df: pd.DataFrame,
    date_format_list: typing.List[typing.List[str]],
) -> pd.DataFrame:
    logging.info("Converting Date Format..")
    for fld, from_format, to_format in date_format_list:
        df[fld] = df[fld].apply(
            lambda x, from_format, to_format: convert_dt_format(
                x, from_format, to_format
            ),
            args=(from_format, to_format),
        )
    return df


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
    source_url: str = "",
    field_delimiter: str = "|",
    quotechar: str = '"',
    source_file_type: str = "csv"
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    if source_file_type == "csv":
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.skip_leading_rows = 1  # ignore the header
        job_config.field_delimiter = field_delimiter
        job_config.allow_quoted_newlines = True
        job_config.quote_character = quotechar
    elif source_file_type == "avro":
        job_config.source_format = bigquery.SourceFormat.AVRO
    elif source_file_type == "datastore_backup":
        job_config.source_format = bigquery.SourceFormat.DATASTORE_BACKUP
    elif source_file_type == "json":
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        print(job_config.source_format)
    elif source_file_type == "orc":
        job_config.source_format = bigquery.SourceFormat.ORC
    elif source_file_type == "parquet":
        job_config.source_format = bigquery.SourceFormat.PARQUET
    if truncate_table:
        job_config.write_disposition = "WRITE_TRUNCATE"
    else:
        if source_url == "":
            pass
        else:
            delete_source_file_data_from_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                source_url=source_url,
            )
        job_config.write_disposition = "WRITE_APPEND"
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    try:
        job.result()
    except BadRequest as ex:
        logging.info("an error occurred ...")
        import pdb; pdb.set_trace()
        for err in ex.errors:
            logging.info(err)
        raise
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


def delete_source_file_data_from_bq(
    project_id: str, dataset_id: str, table_id: str, source_url: str
) -> None:
    logging.info(
        f"Deleting data from {project_id}.{dataset_id}.{table_id} where source_url = '{source_url}'"
    )
    client = bigquery.Client()
    query = f"""
        DELETE
        FROM {project_id}.{dataset_id}.{table_id}
        WHERE source_url = '@source_url'
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
            bigquery.ScalarQueryParameter("dataset_id", "STRING", dataset_id),
            bigquery.ScalarQueryParameter("table_id", "STRING", table_id),
            bigquery.ScalarQueryParameter("source_url", "STRING", source_url),
        ]
    )
    query_job = client.query(query, job_config=job_config)  # Make an API request.
    query_job.result()


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
        schema_struct = json.loads(blob.download_as_bytes(client=None))
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


def save_to_new_file(
    df: pd.DataFrame, file_path: str, sep: str = "|", quotechar: str = '"'
) -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep, quotechar=quotechar)


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
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=json.loads(os.environ.get("SOURCE_URL", r"{}")),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        drop_dest_table=os.environ.get("DROP_DEST_TABLE", ""),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"[]"))
    )
