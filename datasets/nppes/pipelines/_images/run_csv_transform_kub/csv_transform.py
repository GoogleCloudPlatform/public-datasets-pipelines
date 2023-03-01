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
import re
import subprocess
from zipfile import ZipFile

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    source_npi_data_file_regexp: str,
    pipeline_name: str,
) -> None:

    logging.info(
        f"{pipeline_name} load process started at {str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"
    )
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading most recent source file")
    src_url = source_url \
                    .replace("_MM", f"_{str(datetime.datetime.now().strftime('%B'))}") \
                    .replace("_YYYY", f"_{str(datetime.datetime.now().strftime('%Y'))}")
    src_zip_file = f"{os.path.dirname(source_file)}/{os.path.basename(src_url)}"
    if not download_file(src_url, src_zip_file):
        logging.info(f" ... file {src_url} is unavailable")
        one_month_ago = datetime.date.today() - relativedelta(months=1)
        src_url = source_url \
                        .replace("_MM", f"_{one_month_ago.strftime('%B')}") \
                        .replace("_YYYY", f"_{one_month_ago.strftime('%Y')}")
        logging.info(f" ... attempting to download file {src_url} instead ...")
        src_zip_file = f"{os.path.dirname(source_file)}/{os.path.basename(src_url)}"
        download_file(src_url, src_zip_file)

    logging.info(f" ... file {src_url} download complete")
    logging.info(f"Searching for source NPI data file within {src_zip_file}")
    with ZipFile(src_zip_file, 'r') as src_zip:
        listOfFileNames = src_zip.namelist()
        for fileName in listOfFileNames:
            if re.match(rf'{source_npi_data_file_regexp}', fileName):
                logging.info(f"Found data file {fileName}, extracting ...")
                src_zip.extract(fileName, os.path.dirname(target_file))
                target_file = f"{os.path.dirname(target_file)}/{fileName}"
                logging.info("Resolving Date Format")
                # os.system(["sed", "-i", "-r", "-E" "'s/([0-9]{2})\/([0-9]{2})\/([0-9]{4})/\3-\1-\2/g'", target_file], shell=True)
                sed_cmd = "sed -i -r -E 's/([0-9]{2})\/([0-9]{2})\/([0-9]{4})/\\3-\\1-\\2/g'"
                subprocess.call([f"{sed_cmd} {target_file}"], shell=True)
                if os.path.exists(target_file):
                    upload_file_to_gcs(
                        file_path=target_file,
                        target_gcs_bucket=target_gcs_bucket,
                        target_gcs_path=target_gcs_path,
                    )
                table_exists = create_dest_table(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=table_id,
                    schema_filepath=schema_path,
                    bucket_name=target_gcs_bucket,
                    drop_table=False,
                )
                if table_exists:
                    load_data_to_bq(
                        project_id=project_id,
                        dataset_id=dataset_id,
                        table_id=table_id,
                        file_path=target_file,
                        truncate_table=True,
                        field_delimiter=",",
                    )
                else:
                    error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
                    raise ValueError(error_msg)
    logging.info(
        f"{pipeline_name} load process completed at {str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"
    )


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


def download_file(source_url: str, source_file: pathlib.Path) -> bool:
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
        return True
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")
        return False


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
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        source_npi_data_file_regexp=os.environ["SOURCE_NPI_DATA_FILE_REGEXP"],
        pipeline_name=os.environ["PIPELINE_NAME"],
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
    )
