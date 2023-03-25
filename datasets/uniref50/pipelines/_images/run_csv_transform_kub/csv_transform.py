# Copyright 2022 Google LLC
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
import gzip
import json
import logging
import os
import pathlib
import pandas as pd
import subprocess
import typing

# from Bio import SeqIO
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_gcs_bucket: str,
    source_gcs_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    destination_folder: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    csv_headers: typing.List[str],
    schema_path: str,
    chunksize: str,
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_gcs_bucket=source_gcs_bucket,
        source_gcs_path=source_gcs_path,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        destination_folder=destination_folder,
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        csv_headers=csv_headers,
        schema_path=schema_path,
        chunksize=chunksize,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_gcs_bucket: str,
    source_gcs_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    destination_folder: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    csv_headers: typing.List[str],
    schema_path: str,
    chunksize: str,
) -> None:
    # find all zipfiles for loading
    logging.info("Processing individual zip files ...")
    # for zip_file in sorted(pathlib.Path(zip_path).glob("x*.csv.gz")):
    for zip_file in sorted(list_gcs_files(project_id, source_gcs_bucket, source_gcs_path, "x", ".txt.gz")):
        source_location = f"gs://{source_gcs_bucket}/{source_gcs_path}/{zip_file}"
        logging.info(f" Downloading, processing and loading source data file {source_location} ...")
        #copy file to pod
        download_file_gcs(
            project_id=project_id,
            source_location=source_location,
            destination_folder=destination_folder
        )
        extracted_chunk = str(zip_file).replace(".gz", "")
        gz_decompress(infile=f"{destination_folder}/{zip_file}", tofile=extracted_chunk, delete_zipfile=True)
        transform_data(
            fileName=extracted_chunk,
            csv_headers=csv_headers
        )
        load_source_file_to_bq(
            target_file=extracted_chunk,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            schema_path=schema_path,
            truncate_table=(
                True if os.path.basename(extracted_chunk) == "x000.csv" else False
            ),
            field_delimiter="|",
        )


def transform_data(
    fileName: str,
    csv_headers: typing.List[str]
) -> None:
    logging.info("Transforms ...")
    logging.info(" ... Transform -> Adding header")
    csv_header = ",".join(str(itm) for itm in csv_headers)
    cmd = f"sed -i '1s/^/{csv_header}\\n/' {fileName}"
    subprocess.run(cmd, shell=True)
    logging.info(" ... Transform -> Cleaning Organism Data Column")
    df = pd.read_csv(fileName, sep="|")
    df["Organism"] = df["Organism"].apply(lambda x: x.replace("-", "\n"))
    df.to_csv(fileName, sep="|", index=False)
    logging.info("Transforms completed")


def list_gcs_files(
    project_id: str,
    source_gcs_bucket: str,
    source_gcs_path: str,
    file_prefix: str,
    file_suffix: str
) -> typing.List[str]:
    storage_client = storage.Client(project_id)
    blobs = list(storage_client.list_blobs(source_gcs_bucket, prefix=source_gcs_path, fields="items(name)"))
    blob_names = [blob_name.name[len(source_gcs_path):] for blob_name in blobs if blob_name.name != source_gcs_path]
    bucket_files = sorted(blob_names)
    rtn_list = []
    for bucket_file in bucket_files:
        if bucket_file[:(len(file_prefix)+1)] == f"/{file_prefix}" \
            and bucket_file[-(len(file_suffix)):] == file_suffix:
                rtn_list += [bucket_file[1:]]
    return rtn_list


def download_file_gcs(
    project_id: str,
    source_location: str,
    destination_folder: str,
    filename_override: str = "",
) -> None:
    object_name = os.path.basename(source_location)
    if filename_override == "":
        dest_object = f"{destination_folder}/{object_name}"
    else:
        dest_object = f"{destination_folder}/{filename_override}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def gz_decompress(infile: str, tofile: str, delete_zipfile: bool = False) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)
    if delete_zipfile:
        os.remove(infile)


def check_gcs_file_exists(file_path: str, bucket_name: str) -> bool:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    exists = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)
    return exists


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
    field_delimiter: str,
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
        table = True
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
        pipeline_name=os.environ.get("PIPELINE_NAME"),
        source_gcs_bucket=os.environ.get("SOURCE_GCS_BUCKET"),
        source_gcs_path=os.environ.get("SOURCE_GCS_PATH"),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET"),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH"),
        destination_folder=os.environ.get("DESTINATION_FOLDER"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        table_id=os.environ["TABLE_ID"],
        csv_headers=json.loads(os.environ.get("CSV_HEADERS", r"[]")),
        schema_path=os.environ["SCHEMA_PATH"],
        chunksize=os.environ.get("CHUNKSIZE"),
    )
