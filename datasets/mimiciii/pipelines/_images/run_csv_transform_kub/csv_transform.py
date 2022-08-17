import logging
import os

from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_project, destination_project, source_dataset, destination_dataset, gcs_bucket
):
    logging.info(
        "Fetching the source tables from bq. Each pipeline will be undergoing ETL"
    )
    source_table_names = fetch_source_tables(source_project, source_dataset)

    logging.info(
        "All of the following script will be executed for each table from the list of source tables."
    )
    for each_table in source_table_names:
        logging.info(
            "========================================== START ================================================"
        )
        pipeline_name = each_table
        table_id = each_table
        execute_pipeline(
            source_project,
            destination_project,
            source_dataset,
            destination_dataset,
            gcs_bucket,
            pipeline_name,
            table_id,
        )
        logging.info(f"Finished ETL for ---> {pipeline_name}")
        print()


def fetch_source_tables(source_project, source_dataset):
    client = bigquery.Client()
    bqtables = client.list_tables(f"{source_project}.{source_dataset}")
    tables = []
    for table in bqtables:
        tables.append(table.table_id)
    return tables


def execute_pipeline(
    source_project,
    destination_project,
    source_dataset,
    destination_dataset,
    gcs_bucket,
    pipeline_name,
    table_id,
):
    logging.info(f"ETL started for {pipeline_name} ---->")

    logging.info("Exporting table.")
    destination = f"gs://{gcs_bucket}/data/mimicIII/{table_id}.csv"
    client = bigquery.Client()
    dataset_ref = bigquery.DatasetReference(source_project, source_dataset)
    table_ref = dataset_ref.table(table_id)
    extract_job = client.extract_table(table_ref, destination, location="US")
    logging.info(extract_job.result())
    source_blob = destination

    logging.info("Fetching schema")
    table = client.get_table(f"{source_project}.{source_dataset}.{table_id}")
    schema_list = table.schema

    if source_blob:
        table_exists = create_dest_table(
            project_id=destination_project,
            dataset_id=destination_dataset,
            table_id=table_id,
            gcs_bucket=gcs_bucket,
            schema_filepath=schema_list,
            drop_table=True,
        )
        if table_exists:
            load_data_to_bq(
                project_id=destination_project,
                dataset_id=destination_dataset,
                table_id=table_id,
                gcs_bucket=gcs_bucket,
                source_gcs_path=source_blob,
                truncate_table=True,
                field_delimiter="|",
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {destination_project}.{destination_dataset}.{table_id} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(f"Informational: The data file {source_blob} is unavailable")


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
            schema = schema_filepath
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)
            logging.info(f"Table {table_id} was created")
            table_exists = True
        else:
            logging.info(f"Schema {schema_filepath} not found")
            table_exists = False
    else:
        table_exists = True
    return table_exists


def load_data_to_bq(
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
        skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV
    )
    job = client.load_table_from_uri(
        source_gcs_path,
        table_ref,
        job_config=job_config,
    )
    logging.info(job.result())
    logging.info("Loading table completed")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_project=os.environ.get("SOURCE_PROJECT"),
        destination_project=os.environ.get("DESTINATION_PROJECT"),
        source_dataset=os.environ.get("SOURCE_DATASET"),
        destination_dataset=os.environ.get("DESTINATION_DATASET"),
        gcs_bucket=os.environ.get("GCS_BUCKET"),
    )
