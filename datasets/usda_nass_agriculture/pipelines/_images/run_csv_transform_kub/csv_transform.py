import json
import logging
import os

import pandas as pd
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    download_path,
    source_gcs_path,
    destination_gcs_path,
    project_id,
    dataset_id,
    gcs_bucket,
    schema_filepath,
    rename_mappings,
    headers,
) -> None:
    source_file_names = fetch_gcs_file_names(source_gcs_path, gcs_bucket)
    for each_file in source_file_names:
        pipeline_name = each_file
        table_id = each_file[:-4]
        logging.info(f"Started Extraction and Load process for {pipeline_name} ---->")
        if pipeline_name.startswith("environmental"):
            continue
        execute_pipeline(
            download_path,
            source_gcs_path,
            destination_gcs_path,
            project_id,
            dataset_id,
            gcs_bucket,
            pipeline_name,
            table_id,
            schema_filepath,
            rename_mappings,
            headers,
        )
        logging.info(f"Finished process for {pipeline_name}...")
        print()


def fetch_gcs_file_names(source_gcs_path, gcs_bucket):
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=source_gcs_path)
    source_file_names = []
    for blob in blobs:
        if blob.name.endswith(".txt"):
            source_file_names.append(blob.name.split("/")[-1])
    logging.info(f"{len(source_file_names)} tables to be loaded in bq")
    return source_file_names


def execute_pipeline(
    download_path,
    source_gcs_path,
    destination_gcs_path,
    project_id,
    dataset_id,
    gcs_bucket,
    pipeline_name,
    table_id,
    schema_filepath,
    rename_mappings,
    headers,
):
    logging.info(f"ETL started for {pipeline_name}")
    pipeline_name = download_file(
        download_path, source_gcs_path, gcs_bucket, pipeline_name
    )
    if check_file(download_path, pipeline_name):
        final_filename = transform_file(
            download_path, pipeline_name, rename_mappings, headers
        )
        upload_transformed_file(
            destination_gcs_path, gcs_bucket, final_filename, pipeline_name
        )
        client = storage.Client()
        blob = client.list_blobs(
            gcs_bucket, prefix=destination_gcs_path + pipeline_name
        )
        if blob:
            table_exists = create_dest_table(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                schema_filepath=schema_filepath,
                drop_table=True,
            )
            if table_exists:
                load_data_to_bq(
                    pipeline_name=pipeline_name,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=table_id,
                    gcs_bucket=gcs_bucket,
                    source_gcs_path=destination_gcs_path,
                )
            else:
                error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{table_id} does not exist and/or could not be created."
                raise ValueError(error_msg)
        else:
            logging.info(f"Informational: The data file {blob} is unavailable")
    else:
        logging.info(f"File {pipeline_name} empty/corrupted")


def check_file(download_path, pipeline_name):
    with open(download_path + pipeline_name) as f:
        return f.read()


def transform_file(download_path, pipeline_name, rename_mappings, headers):
    logging.info("Transforming file")
    with pd.read_csv(
        download_path + pipeline_name,
        sep="\t",
        encoding_errors="ignore",
        chunksize=1000000,
    ) as reader:
        logging.info("Deleting source file to avoid space consumption.")
        os.remove(download_path + pipeline_name)
        for df in reader:
            logging.info("Processing chunk df")
            rename_headers(df, rename_mappings)
            reorder_headers(df, headers)
            final_filename = save_to_file(df, download_path, pipeline_name)
    return final_filename


def save_to_file(df, download_path, pipeline_name):
    filename = download_path + pipeline_name[:-4] + ".csv"
    df.to_csv(filename, index=False, header=False, mode="a")
    return filename


def reorder_headers(df, headers):
    logging.info("Reordering headers")
    df = df[headers]


def rename_headers(df, rename_mappings):
    logging.info("Rename the headers")
    df.rename(columns=rename_mappings, inplace=True)


def download_file(download_path, source_gcs_path, gcs_bucket, pipeline_name):
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(source_gcs_path + pipeline_name)
    blob.download_to_filename(download_path + pipeline_name)
    logging.info(f"Finished downloading {pipeline_name}")
    return pipeline_name


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
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
        schema_dict = json.load(f)
    for line_field in schema_dict:
        fld_name = line_field["name"]
        fld_type = line_field["type"]
        try:
            fld_descr = line_field["description"]
        except KeyError:
            fld_descr = ""
        fld_mode = line_field["mode"]
        schema.append(
            bigquery.SchemaField(
                name=fld_name, field_type=fld_type, mode=fld_mode, description=fld_descr
            )
        )
    return schema


def upload_transformed_file(
    destination_gcs_path, gcs_bucket, final_filename, pipeline_name
):
    logging.info("Uploading file to GCS")
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(destination_gcs_path + pipeline_name[:-4] + ".csv")
    blob.upload_from_filename(final_filename)
    logging.info("Deleting file post upload")
    os.remove(final_filename)


def load_data_to_bq(
    pipeline_name: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    gcs_bucket: str,
    source_gcs_path: str,
) -> None:
    logging.info(
        f"Loading output data from {source_gcs_path} into {project_id}.{dataset_id}.{table_id} ...."
    )
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=0, source_format=bigquery.SourceFormat.CSV
    )
    job = client.load_table_from_uri(
        f"gs://{gcs_bucket}/{source_gcs_path}{pipeline_name}",
        table_ref,
        job_config=job_config,
    )
    logging.info(job.result())
    logging.info("Loading table completed")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        download_path=os.environ.get("DOWNLOAD_PATH", ""),
        source_gcs_path=os.environ.get("SOURCE_GCS_PATH"),
        destination_gcs_path=os.environ.get("DESTINATION_GCS_PATH"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        gcs_bucket=os.environ.get("GCS_BUCKET"),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH"),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS")),
        headers=json.loads(os.environ.get("HEADERS")),
    )
