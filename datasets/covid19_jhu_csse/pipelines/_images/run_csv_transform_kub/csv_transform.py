import json
import logging
import os

from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage

download_path="/usr/local/google/home/nnoel/Downloads/csv_transform_dump/"
schema_dict={}
def main(source_gcs_path, destination_gcs_path, project_id, dataset_id, gcs_bucket, schema_filepath) -> None:
    source_file_names = fetch_gcs_file_names(source_gcs_path, gcs_bucket)
    for each_file in source_file_names:
        pipeline_name = each_file
        table_id = each_file[:-5].replace(".","_")
        logging.info(f"Started Extraction and Load process for {pipeline_name} --->")
        execute_pipeline(
            source_gcs_path,
            destination_gcs_path,
            project_id,
            dataset_id,
            gcs_bucket,
            pipeline_name,
            table_id,
            schema_filepath,
        )
        logging.info(f"Finished process for {pipeline_name}")
        print()
        # break


def fetch_gcs_file_names(source_gcs_path, gcs_bucket):
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=source_gcs_path)
    source_file_names = []
    for blob in blobs:
        if blob.name.endswith(".json"):
            source_file_names.append(blob.name.split("/")[-1])
    logging.info(f"{len(source_file_names)} tables to be loaded in bq")
    return source_file_names


def execute_pipeline(
    source_gcs_path,
    destination_gcs_path,
    project_id,
    dataset_id,
    gcs_bucket,                        #pipeline name has the extension, table_id doesnt
    pipeline_name,
    table_id,
    schema_filepath,
):
    logging.info(f"ETL started for {pipeline_name}")
    pipeline_name=download_file(source_gcs_path, gcs_bucket, pipeline_name)
    table_id=replace_hyphen(table_id)
    if check_file(pipeline_name):
        schema_fields=transform_file(pipeline_name)
        prepare_schema_dict(pipeline_name, schema_fields, schema_dict)
        upload_transformed_file(destination_gcs_path, gcs_bucket, pipeline_name)
        client = storage.Client()
        blob = client.list_blobs(gcs_bucket, prefix=source_gcs_path + pipeline_name)
        if blob:
            table_exists = create_dest_table(
                pipeline_name=pipeline_name,
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                gcs_bucket=gcs_bucket,
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
                    truncate_table=True,
                    field_delimiter="|",
                )
            else:
                error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{table_id} does not exist and/or could not be created."
                raise ValueError(error_msg)
        else:
            logging.info(f"Informational: The data file {blob} is unavailable")
    else:
        logging.info(f"File {pipeline_name} empty/corrupted")


def check_file(pipeline_name):
    with open(download_path+pipeline_name) as f:
        return f.read()

def transform_file(pipeline_name):
    logging.info("Fetching schema from the file itself.")
    schema_fields=get_schema_fields(pipeline_name)
    logging.info("Transforming file")
    with open(download_path+pipeline_name, "r+") as f:
        # file_data=json.load(f)
        for row in f:
            for field in schema_fields:
                if not json.loads(row).get(field):
                    json.loads(row)[field]=''
                    # file_data[pipeline_name].append({field:''})
        
    return schema_fields


def get_schema_fields(pipeline_name):
    max_no_cols=0
    with open(download_path+pipeline_name) as f:
        for row in f:
            num_of_cols=len(json.loads(row).keys())
            if num_of_cols>max_no_cols:
                max_no_cols=num_of_cols
                row_with_schema=row
    return list(json.loads(row_with_schema).keys())

def prepare_schema_dict(pipeline_name, schema_fields, schema_dict):    # '{pipeline_name:[{},{}],pipeline_name:[{},{}]}'
    schema_dict[pipeline_name]=[]
    for i in schema_fields:
        schema_dict[pipeline_name].append({"name": i,"type": "STRING","mode": "NULLABLE"})
    # return schema_dict


def replace_hyphen(x):
    return x.replace("-","_")


def download_file(source_gcs_path, gcs_bucket, pipeline_name):
    client=storage.Client()
    bucket=client.bucket(gcs_bucket)
    blob=bucket.blob(source_gcs_path+pipeline_name)
    # blob.download_to_filename(pipeline_name)
    pipeline_name=replace_hyphen(pipeline_name)
    pipeline_name=pipeline_name.replace(".","_",1)
    blob.download_to_filename(download_path+pipeline_name)
    logging.info(f"Finished downloading {pipeline_name}")
    return pipeline_name

def create_dest_table(
    pipeline_name: str,
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
            schema = create_table_schema(schema_filepath, schema_dict, pipeline_name)
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


def create_table_schema(schema_filepath, schema_dict, pipeline_name) -> list:
    logging.info("Defining table schema")
    schema = []
    # with open(schema_filepath) as f:
    #     sc = f.read()
    # schema_struct = json.loads(sc)

    for schema_field in schema_dict[pipeline_name]:
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

def upload_transformed_file(destination_gcs_path, gcs_bucket, pipeline_name):
    logging.info("Uploading file to GCS")
    client=storage.Client()
    bucket=client.bucket(gcs_bucket)
    blob=bucket.blob(destination_gcs_path+pipeline_name)
    blob.upload_from_filename(download_path+pipeline_name)


def load_data_to_bq(
    pipeline_name: str,
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
    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)
    job = client.load_table_from_uri(
        f"gs://{gcs_bucket}/{source_gcs_path}{table_id}.json",
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
        schema_filepath=os.environ.get("SCHEMA_FILEPATH"),
        # download_path=os.environ.get("DOWNLOAD_PATH")
    )
