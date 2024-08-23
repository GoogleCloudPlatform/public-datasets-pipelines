import json
import logging
import math
import os
import pathlib
import typing

import pandas as pd
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_file_name,
    download_path,
    source_gcs_path,
    destination_gcs_path,
    project_id,
    dataset_id,
    gcs_bucket,
    pipeline_name,
    table_id,
    schema_filepath,
    column_name,
    headers,
    rename_mappings,
) -> None:
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    logging.info(f"Started Extraction and Load process for {pipeline_name} --->")
    execute_pipeline(
        source_file_name,
        download_path,
        source_gcs_path,
        destination_gcs_path,
        project_id,
        dataset_id,
        gcs_bucket,
        pipeline_name,
        table_id,
        schema_filepath,
        column_name,
        headers,
        rename_mappings,
    )
    logging.info(f"Finished process for {pipeline_name}")


def execute_pipeline(
    source_file_name,
    download_path,
    source_gcs_path,
    destination_gcs_path,
    project_id,
    dataset_id,
    gcs_bucket,
    pipeline_name,
    table_id,
    schema_filepath,
    column_name,
    headers,
    rename_mappings,
):
    logging.info(f"ETL started for {source_file_name}")
    logging.info("Downloading file")
    download_file(source_gcs_path, download_path, gcs_bucket, source_file_name)
    logging.info("Transforming file")
    source_file_name = transform_file(
        pipeline_name,
        dataset_id,
        download_path,
        source_file_name,
        column_name,
        headers,
        rename_mappings,
    )
    upload_file_to_gcs(
        gcs_bucket, download_path, source_file_name, destination_gcs_path
    )
    client = storage.Client()
    blob = client.list_blobs(gcs_bucket, prefix=destination_gcs_path + pipeline_name)
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
                source_file_name=source_file_name,
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                gcs_bucket=gcs_bucket,
                source_gcs_path=destination_gcs_path,
                truncate_table=True,
                field_delimiter="|",
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{table_id} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(f"Informational: The data file {blob} is unavailable")


def transform_file(
    pipeline_name,
    dataset_id,
    download_path,
    source_file_name,
    column_name,
    headers,
    rename_mappings,
):
    logging.info(f"Reading file {source_file_name}")
    df = pd.read_csv(download_path + source_file_name, skip_blank_lines=True)
    logging.info(f"Transforming {source_file_name} ... ")
    logging.info(f"Transform: Dropping column {column_name} ...")
    delete_column(df, column_name)
    logging.info(f"Transform: Renaming columns for {source_file_name} ...")
    rename_headers(df, rename_mappings)

    if pipeline_name == "series_time" or pipeline_name == "footnotes":
        logging.info(f"Transform: Extracting year for {source_file_name} ...")
        df["year"] = df["year"].apply(extract_year)

    if pipeline_name == "country_summary":
        logging.info("Transform: Creating a new column ...")
        df["latest_water_withdrawal_data"] = ""

        logging.info("Transform: converting to integer ... ")
        df["latest_industrial_data"] = df["latest_industrial_data"].apply(
            convert_to_integer_string
        )
        df["latest_trade_data"] = df["latest_trade_data"].apply(
            convert_to_integer_string
        )

    logging.info(f"Transform: Reordering headers for {source_file_name} ...")
    df = df[headers]

    logging.info("Saving output file with proper naming convention")
    source_file_name = source_file_name.lower().replace("-", "_")
    try:
        save_to_new_file(df, file_path=download_path + source_file_name)
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    return source_file_name


def delete_column(df: pd.DataFrame, column_name: str) -> None:
    df.drop(column_name, axis=1, inplace=True)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def extract_year(string_val: str) -> str:
    # example : YR2021
    return string_val[-4:]


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(int(round(input, 0)))
    return str_val


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False, sep=",")


def download_file(source_gcs_path, download_path, gcs_bucket, source_file_name):
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(source_gcs_path + source_file_name)
    blob.download_to_filename(download_path + source_file_name)


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    gcs_bucket: str,
    schema_filepath: str,
    drop_table: bool,
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
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


def create_table_schema(schema_filepath, table_id) -> list:
    logging.info("Defining table schema")
    schema = []
    with open(schema_filepath) as f:
        sc = f.read()
    schema_struct = json.loads(sc)
    dataset = table_id
    for schema_field in schema_struct[dataset]:
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
    gcs_bucket, download_path, source_file_name, destination_gcs_path
):
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(destination_gcs_path + source_file_name)
    blob.upload_from_filename(download_path + source_file_name)


def load_data_to_bq(
    source_file_name: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    gcs_bucket: str,
    source_gcs_path: str,
    truncate_table: bool,
    field_delimiter: str = "|",
) -> None:
    logging.info(
        f"Loading output data from {source_gcs_path} into {project_id}.{dataset_id}.{table_id} ...."
    )
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        allow_quoted_newlines=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )
    job = client.load_table_from_uri(
        f"gs://{gcs_bucket}/{source_gcs_path}{source_file_name}",
        table_ref,
        job_config=job_config,
    )
    logging.info(job.result())
    logging.info("Loading table completed")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_file_name=os.environ.get("SOURCE_FILE_NAME"),
        download_path=os.environ.get("DOWNLOAD_PATH"),
        source_gcs_path=os.environ.get("SOURCE_GCS_PATH"),
        destination_gcs_path=os.environ.get("DESTINATION_GCS_PATH"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        gcs_bucket=os.environ.get("GCS_BUCKET"),
        pipeline_name=os.environ.get("PIPELINE_NAME"),
        table_id=os.environ.get("TABLE_ID"),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH"),
        column_name=os.environ.get("COLUMN_NAME"),
        headers=json.loads(os.environ.get("HEADERS")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS")),
    )
