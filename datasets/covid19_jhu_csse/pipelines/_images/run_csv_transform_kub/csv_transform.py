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
    add_header,
) -> None:
    source_file_names = fetch_gcs_file_names(source_gcs_path, gcs_bucket)
    for each_file in source_file_names:
        pipeline_name = each_file
        table_id = each_file[:-4]
        logging.info(f"Started Extraction and Load process for {pipeline_name} --->")
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
            add_header,
        )
        logging.info(f"Finished process for {pipeline_name}")
        print()


def fetch_gcs_file_names(source_gcs_path, gcs_bucket):
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=source_gcs_path)
    source_file_names = []
    for blob in blobs:
        if blob.name.endswith(".csv"):
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
    add_header,
):
    logging.info(f"ETL started for {pipeline_name}")
    pipeline_name = download_file(
        download_path, source_gcs_path, gcs_bucket, pipeline_name
    )
    if check_file(download_path, pipeline_name):
        schema_fields, final_filename = transform_file(
            download_path, pipeline_name, rename_mappings, add_header
        )
        schema_dict = prepare_schema_dict(table_id, schema_fields, {})
        prepare_upload_schema_file(
            download_path,
            gcs_bucket,
            destination_gcs_path,
            schema_filepath,
            schema_dict,
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
                schema_dict=schema_dict,
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


def transform_file(download_path, pipeline_name, rename_mappings, add_header):
    df = pd.read_csv(download_path + pipeline_name)
    logging.info("Transforming file")
    rename_headers(df, rename_mappings)
    rename_date_headers(df, rename_mappings)
    add_location_header(df, add_header)
    reorder_headers(df, add_header)
    final_filename = save_to_file(df, download_path, pipeline_name)
    return list(df.columns), final_filename


def save_to_file(df, download_path, pipeline_name):
    filename_prefix = "final_"
    filename = download_path + filename_prefix + pipeline_name
    df.to_csv(filename, index=False)
    return filename


def reorder_headers(df, add_header):
    logging.info("Reordering headers")
    col = df.pop(add_header)
    df.insert(4, col.name, col)


def add_location_header(df, add_header):
    logging.info("Adding a new column by concatenating 2")
    df[add_header] = (
        "POINT(" + df["latitude"].astype(str) + " " + df["longitude"].astype(str) + ")"
    )


def rename_date_headers(df, rename_mappings):
    logging.info("Make date headers BigQuery friendly")
    cols = list(df.columns)
    date_cols = []
    for i in cols:
        if i not in list(rename_mappings.values()):
            date_cols.append(i)
    date_dict = {}
    for date in date_cols:
        date_dict[date] = "_" + date.replace("/", "_")
    rename_headers(df, date_dict)


def rename_headers(df, rename_mappings):
    logging.info("Rename the headers")
    df.rename(columns=rename_mappings, inplace=True)


def prepare_schema_dict(table_id, schema_fields, schema_dict):
    schema_dict[table_id] = []
    for i in schema_fields:
        schema_dict[table_id].append({"name": i, "type": "STRING", "mode": "NULLABLE"})
    return schema_dict


def prepare_upload_schema_file(
    download_path, gcs_bucket, destination_gcs_path, schema_filepath, schema_dict
):
    logging.info("Preparing schema file")
    with open(download_path + schema_filepath, "w") as file:
        json.dump(schema_dict, file)
    logging.info("Uploading schema file to GCS")
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    destination_gcs_path = destination_gcs_path[:22]
    blob = bucket.blob(destination_gcs_path + schema_filepath)
    blob.upload_from_filename(download_path + schema_filepath)


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
    schema_dict,
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
            schema = create_table_schema(schema_dict, table_id)
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


def create_table_schema(schema_dict, table_id) -> list:
    logging.info("Defining table schema")
    schema = []
    for schema_field in schema_dict[table_id]:
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


def upload_transformed_file(
    destination_gcs_path, gcs_bucket, final_filename, pipeline_name
):
    logging.info("Uploading file to GCS")
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(destination_gcs_path + pipeline_name)
    blob.upload_from_filename(final_filename)


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
        skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV
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
        add_header=os.environ.get("ADD_HEADER"),
    )
