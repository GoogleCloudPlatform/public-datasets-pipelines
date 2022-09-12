import csv
import json
import logging
import os
import typing

import pandas as pd
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_gcs_path: str,
    destination_gcs_path: str,
    project_id: str,
    dataset_id: str,
    gcs_bucket: str,
    schema_filepath: str,
    header: typing.List[str],
) -> None:
    logging.info("Getting the names of the source files")
    source_file_names = fetch_gcs_file_names(source_gcs_path, gcs_bucket)
    for each_file in source_file_names:
        pipeline_name = each_file
        table_id = each_file
        logging.info(f"Started ETL process for {pipeline_name}")
        execute_pipeline(
            source_gcs_path,
            destination_gcs_path,
            project_id,
            dataset_id,
            gcs_bucket,
            pipeline_name,
            table_id,
            schema_filepath,
            header,
        )
        logging.info(f"Finished process for {pipeline_name} ------>")
        logging.info("------ NEXT PIPELINE ------")
    logging.info("Finished the entire process for all the pipelines.")


def fetch_gcs_file_names(source_gcs_path: str, gcs_bucket: str) -> list:
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=source_gcs_path)
    source_file_names = []
    for blob in blobs:
        if blob.name.split("/")[-1]:
            source_file_names.append(blob.name.split("/")[-1])
    logging.info(f"{len(source_file_names)} tables to be loaded in bq")
    return source_file_names


def execute_pipeline(
    source_gcs_path: str,
    destination_gcs_path: str,
    project_id: str,
    dataset_id: str,
    gcs_bucket: str,
    pipeline_name: str,
    table_id: str,
    schema_filepath: str,
    header: typing.List[str],
):
    if pipeline_name.endswith(".xlsx"):
        table_id = table_id[:-5].lower()
        logging.info(f"Downloading and transforming {pipeline_name}")
        upload_file = transform_xlsx(gcs_bucket, source_gcs_path, pipeline_name)
    elif pipeline_name.endswith(".csv"):
        table_id = table_id[:-4].lower()
        logging.info(f"Downloading and transforming {pipeline_name}")
        upload_file = transform_csv(gcs_bucket, source_gcs_path, pipeline_name, header)
    pipeline_name = upload_file
    blob = None
    if upload_file:
        logging.info("Uploading final file to gcs")
        upload_file_to_gcs(gcs_bucket, destination_gcs_path, upload_file=upload_file)
        source_gcs_path = destination_gcs_path
        client = storage.Client()
        blob = client.list_blobs(gcs_bucket, prefix=source_gcs_path + pipeline_name)
    if blob:
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            gcs_bucket=gcs_bucket,
            schema_filepath=schema_filepath,
            drop_table=True,
        )
        if table_exists:
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                gcs_bucket=gcs_bucket,
                source_gcs_path=source_gcs_path,
                truncate_table=True,
                field_delimiter="|",
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{table_id} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(f"Informational: The data file {blob} is unavailable")


def upload_file_to_gcs(gcs_bucket: str, destination_gcs_path: str, upload_file: str):
    gcs_upload_file = upload_file.lower()
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(destination_gcs_path + "/" + gcs_upload_file)
    blob.upload_from_filename(upload_file)
    logging.info(f"Completed uploading {upload_file} to gcs")


def transform_xlsx(gcs_bucket: str, source_gcs_path: str, pipeline_name: str) -> str:
    download_file(gcs_bucket, source_gcs_path, pipeline_name)
    try:
        df = pd.read_excel(pipeline_name)
        upload_file = f"{pipeline_name[:-5]}.csv"
        upload_file = upload_file.lower()
        df.to_csv(upload_file, index=False, sep=",")
    except ValueError:
        logging.info(f"{pipeline_name} file is corrupted, skipping and moving ahead.")
        return None
    logging.info("Completed transforming file.")
    if upload_file:
        return upload_file


def transform_csv(
    gcs_bucket: str, source_gcs_path: str, pipeline_name: str, header: typing.List[str]
) -> str:
    download_file(gcs_bucket, source_gcs_path, pipeline_name)
    if pipeline_name == "NCEI_NEFSC_PAD_metadata.csv":
        data = []
        with open(pipeline_name) as f:
            content = csv.reader(f)
            for row in content:
                while row[-1] == "":
                    row.pop()
                if "MULTIPOINT" in row[-1]:
                    temp = row.pop()
                    row.extend(temp.split(","))
                data.append(row)
        data[0] = header
        upload_file = f"_{pipeline_name[:-4]}.csv"
        upload_file = upload_file.lower()
        with open(upload_file, "w", newline="") as f:
            content = csv.writer(f)
            for row in data:
                content.writerow(row)
        df = pd.read_csv(upload_file)
        upload_file = upload_file[1:]
        df.to_csv(
            upload_file, index=False
        )  # Ensures column number consistency by padding blank fields
    else:
        upload_file = pipeline_name
        logging.info("No transformations required. Moving ahead.")
        return upload_file
    logging.info("Completed transforming file.")
    return upload_file.lower()


def download_file(gcs_bucket: str, source_gcs_path: str, pipeline_name: str):
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(source_gcs_path + "/" + pipeline_name)
    blob.download_to_filename(pipeline_name)
    logging.info("Completed downloading file.")


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    gcs_bucket: str,
    schema_filepath: str,
    drop_table: bool,
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_id} if it doesn't already exist")
    client = bigquery.Client()
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
            f"Table {table_ref} currently does not exist.  Attempting to create table."
        )
        if schema_filepath:
            schema = create_table_schema(schema_filepath, table_id)
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)
            logging.info(f"Table {table_id} was created")
            table_exists = True
        else:
            logging.info(f"Schema {schema_filepath} file not found")
            table_exists = False
    else:
        table_exists = True
    return table_exists


def create_table_schema(schema_filepath: str, table_id: str) -> list:
    logging.info("Defining table schema")
    schema = []
    with open(schema_filepath) as f:
        sc = f.read()
    schema_struct = json.loads(sc)
    for table_field in schema_struct:
        if table_field == table_id:
            for schema_field in schema_struct[table_field]:
                fld_name = schema_field["name"]
                fld_type = schema_field["type"]
                try:
                    fld_descr = schema_field["description"]
                except KeyError:
                    fld_descr = ""
                fld_mode = schema_field["mode"]
                schema.append(
                    bigquery.SchemaField(
                        name=fld_name,
                        field_type=fld_type,
                        mode=fld_mode,
                        description=fld_descr,
                    )
                )
    return schema


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    gcs_bucket: str,
    source_gcs_path: str,
    truncate_table: bool,
    field_delimiter: str = "|",
) -> None:
    logging.info(f"Loading output data from {source_gcs_path} into {table_id}")
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV
    )
    job = client.load_table_from_uri(
        f"gs://{gcs_bucket}/{source_gcs_path}/{table_id}.csv",
        table_ref,
        job_config=job_config,
    )
    logging.info(job.result())
    logging.info("Loading table completed")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_gcs_path=os.environ.get("SOURCE_GCS_PATH"),
        destination_gcs_path=os.environ.get("DESTINATION_GCS_PATH"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        gcs_bucket=os.environ.get("GCS_BUCKET"),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH", ""),
        header=json.loads(os.environ.get("HEADER")),
    )
