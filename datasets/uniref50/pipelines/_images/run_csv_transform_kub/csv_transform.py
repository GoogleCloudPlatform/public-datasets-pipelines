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
import json
import logging
import os
import pathlib

from Bio import SeqIO
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_gcs_bucket: str,
    source_gcs_object: str,
    source_file: pathlib.Path,
    batch_file: str,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_gcs_bucket=source_gcs_bucket,
        source_gcs_object=source_gcs_object,
        source_file=source_file,
        batch_file=batch_file,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        schema_path=schema_path,
        chunksize=chunksize,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_gcs_bucket: str,
    source_gcs_object: str,
    source_file: pathlib.Path,
    batch_file: str,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    download_blob(source_gcs_bucket, source_gcs_object, source_file)
    process_source_file(
        source_file=source_file,
        batch_file=batch_file,
        target_file=target_file,
        chunksize=chunksize,
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
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=destination_table,
                file_path=target_file,
                truncate_table=False,
                field_delimiter=",",
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def download_blob(source_gcs_bucket: str, source_gcs_object: str, source_file: str):
    """Downloads a blob from the bucket."""
    logging.info(
        f"Downloading data from gs://{source_gcs_bucket}/{source_gcs_object} to {source_file} ..."
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(source_gcs_bucket)
    blob = bucket.blob(source_gcs_object)
    blob.download_to_filename(source_file)
    logging.info("Downloading Completed.")


def process_source_file(
    source_file: str,
    batch_file: str,
    target_file: str,
    chunksize: str,
) -> None:
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512 << 10)
    csv.register_dialect("TabDialect", quotechar='"', delimiter=",", strict=True)
    append_header_data(
        batch_file,
        headers_list=[
            "ClusterID",
            "RepID",
            "TaxID",
            "Sequence",
            "ClusterName",
            "Organism",
            "Size",
        ],
    )
    fasta_sequences = SeqIO.parse(open(source_file), "fasta")
    logging.info(f"Finished opening source file {source_file}")
    row_position = 0
    for fasta in fasta_sequences:
        description, sequence = str(fasta.description), str(fasta.seq)
        description_list = description.split(" ")
        row_list = []
        string = ""
        append_row_list(description_list, sequence, row_list)
        description_list = [" {0}".format(elem) for elem in description_list]
        iteration_list = iter(description_list[1:])
        iteration_string = ""
        for item in description_list:
            try:
                iteration_string = next(iteration_list)
                if " n=" in iteration_string:
                    string = string + item
                    row_list.append(string.lstrip())
                    string = ""
                elif " n=" in item:
                    string = string + item
                    row_list.append(string.lstrip()[2:])
                    string = ""
                else:
                    string = string + item
            except StopIteration:
                string = string + item
                row_list.append(string.lstrip()[4:])

        write_batch_file(batch_file, row_list)
        row_position = row_position + 1
        if row_position % int(chunksize) == 0 and row_position > 0:
            process_chunk(
                batch_file=batch_file,
                target_file=target_file,
            )
            row_position = 0

    if row_position != 0:
        process_chunk(
            batch_file=batch_file,
            target_file=target_file,
        )


def append_row_list(description_list: list, sequence: str, row_list: list) -> None:
    row_list.append(description_list.pop(0))
    row_list.append(description_list.pop()[6:])
    row_list.append(description_list.pop()[6:])
    row_list.append(str(sequence))
    return row_list


def write_batch_file(batch_file: str, row_list: list) -> None:
    with open(
        batch_file,
        "a",
    ) as rowobj:
        row_append = csv.writer(rowobj)
        row_append.writerow(row_list)


def process_chunk(
    batch_file: str,
    target_file: str,
) -> None:
    logging.info("Processing batch file")
    target_file_batch = batch_file
    append_batch_file(target_file_batch, target_file)
    logging.info(f"Processing batch file {target_file_batch} completed")


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


def append_header_data(batch_file: str, headers_list: list) -> None:
    with open(batch_file, "w") as headerobj:
        header_write = csv.writer(headerobj)
        header_write.writerow(headers_list)


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


def append_batch_file(target_file_batch: str, target_file: str) -> None:

    with open(target_file_batch, "r") as data_file:
        with open(target_file, "a+") as _target_file:
            logging.info(f"Appending batch file {target_file_batch} to {target_file}")
            logging.info(f"Size of target file is {os.path.getsize(target_file_batch)}")
            logging.info(f"Size of target file is {os.path.getsize(target_file)}")
            _target_file.write(data_file.read())
            if os.path.exists(target_file_batch):
                os.remove(target_file_batch)


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
        source_gcs_object=os.environ.get("SOURCE_GCS_OBJECT"),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE")).expanduser(),
        batch_file=os.environ.get("BATCH_FILE"),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE"),
        target_gcs_bucket=os.environ.get(
            "TARGET_GCS_BUCKET",
        ),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        table_id=os.environ["TABLE_ID"],
        schema_path=os.environ["SCHEMA_PATH"],
    )
