import json
import logging
import os

import pandas as pd
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    download_path,
    source_gcs_key,
    source_gcs_path,
    destination_gcs_path,
    project_id,
    dataset_id,
    gcs_bucket,
    schema_filepath,
    table_id,
) -> None:
    source_file_names = fetch_gcs_file_names(
        source_gcs_key, source_gcs_path, gcs_bucket
    )
    final_df = ""
    for filepath in source_file_names:
        each_file = filepath.split("/")[-1]
        pipeline_name = each_file
        logging.info(f"Started Extraction and Load process for {pipeline_name} --->")
        final_df = execute_pipeline(
            download_path=download_path,
            source_gcs_path=filepath,
            gcs_bucket=gcs_bucket,
            pipeline_name=pipeline_name,
            final_df=final_df,
        )
        print()
    schema_fields = rectify_header_names(list(final_df.columns))
    schema_dict = prepare_schema_dict(table_id, schema_fields, {})
    prepare_upload_schema_file(
        download_path,
        gcs_bucket,
        destination_gcs_path,
        schema_filepath,
        schema_dict,
    )
    filepath, filename = save_to_file(final_df, download_path)
    upload_transformed_file(destination_gcs_path, gcs_bucket, filepath, filename)
    client = storage.Client()
    blob = client.list_blobs(gcs_bucket, prefix=destination_gcs_path + filename)
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
                pipeline_name=filename,
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


def fetch_gcs_file_names(source_gcs_key, source_gcs_path, gcs_bucket):
    source_file_names = []
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=source_gcs_path)
    for blob in blobs:
        path = blob.name.split("/")
        if (
            blob.name.endswith("csv")
            and path[-3] == source_gcs_key[0]
            and path[-2] == source_gcs_key[1]
        ):
            source_file_names.append(blob.name)
    logging.info(f"{len(source_file_names)} tables to be loaded in bq")
    return source_file_names


def rectify_header_names(schema_fields):
    bq_fields = []
    for i in list(schema_fields):
        i = i.lower()
        if ord(i[0]) < 97 or ord(i[0]) > 122 or i[0].isdigit():
            i = "_" + i
        char = list(i)
        for j in char:
            if (
                ord(j) < 97 or ord(j) > 122
            ):  # anything other than alphabets, digits and underscore
                if not j.isdigit():
                    if j != "_":
                        i = i.replace(j, "_")
        bq_fields.append(i)
    return bq_fields


def execute_pipeline(
    download_path, source_gcs_path, gcs_bucket, pipeline_name, final_df
):
    logging.info(f"ETL started for {pipeline_name}")
    pipeline_name = download_file(
        download_path, source_gcs_path, gcs_bucket, pipeline_name
    )
    if check_file(download_path, pipeline_name):
        final_df = transform_file(download_path, pipeline_name, final_df)
    else:
        logging.info(f"File {pipeline_name} empty/corrupted")
    return final_df


def check_file(download_path, pipeline_name):
    logging.info("Check for empty file")
    with open(download_path + pipeline_name) as f:
        return f.read()


def transform_file(download_path, pipeline_name, final_df):
    if not len(final_df):
        logging.info("Framing the target dataframe")
        final_df = pd.read_csv(download_path + pipeline_name)
    else:
        df = pd.read_csv(download_path + pipeline_name)
        logging.info("Concatenating")
        final_df = pd.concat([final_df, df], axis=0)
        del df  # saving memory
    logging.info("Removing the file once loaded in df")
    os.remove(download_path + pipeline_name)
    return final_df


def save_to_file(df, download_path):
    filename_ = "final_output.csv"
    filepath = download_path + filename_
    df.to_csv(filepath, index=False)
    return filepath, filename_


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
    destination_gcs_path = destination_gcs_path
    blob = bucket.blob(destination_gcs_path + schema_filepath)
    blob.upload_from_filename(download_path + schema_filepath)


def download_file(download_path, source_gcs_path, gcs_bucket, pipeline_name):
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(source_gcs_path)
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


def upload_transformed_file(destination_gcs_path, gcs_bucket, filepath, filename):
    logging.info("Uploading file to GCS")
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(destination_gcs_path + filename)
    blob.upload_from_filename(filepath)


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
        source_gcs_key=json.loads(os.environ.get("SOURCE_GCS_KEY")),
        source_gcs_path=os.environ.get("SOURCE_GCS_PATH"),
        destination_gcs_path=os.environ.get("DESTINATION_GCS_PATH"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        gcs_bucket=os.environ.get("GCS_BUCKET"),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH"),
        table_id=os.environ.get("TABLE_ID"),
    )
