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

import json
import logging
import math
import os
import pathlib
import typing
from datetime import datetime

import pandas as pd
import requests
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound


def main(
    project_id: str,
    dataset_id: str,
    current_data_table_id: str,
    historical_data_table_id: str,
    data_file_surr_key_field: str,
    dest_folder: str,
    schema_filepath: str,
    source_bucket: str,
    target_gcs_bucket: str,
    dest_current_data_folder_name: str,
    dest_historical_data_folder_name: str,
    source_bucket_current_data_folder_name: str,
    current_data_target_gcs_path: str,
    historical_data_target_gcs_path: str,
    data_root_folder: str,
    hist_folders_list: typing.List[str],
    pipeline_name: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    logging.info(f"{pipeline_name} process started")
    execute_pipeline(
        project_id = project_id,
        dataset_id = dataset_id,
        current_data_table_id = current_data_table_id,
        historical_data_table_id = historical_data_table_id,
        data_file_surr_key_field = data_file_surr_key_field,
        dest_folder = dest_folder,
        schema_filepath=schema_filepath,
        source_bucket = source_bucket,
        target_gcs_bucket = target_gcs_bucket,
        dest_current_data_folder_name = dest_current_data_folder_name,
        dest_historical_data_folder_name = dest_historical_data_folder_name,
        source_bucket_current_data_folder_name = source_bucket_current_data_folder_name,
        current_data_target_gcs_path = current_data_target_gcs_path,
        historical_data_target_gcs_path = historical_data_target_gcs_path,
        data_root_folder = data_root_folder,
        hist_folders_list = hist_folders_list,
        chunksize = chunksize,
        input_headers = input_headers,
        data_dtypes = data_dtypes,
        int_col_list = int_col_list
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    project_id: str,
    dataset_id: str,
    current_data_table_id: str,
    historical_data_table_id: str,
    data_file_surr_key_field: str,
    dest_folder: str,
    schema_filepath: str,
    source_bucket: str,
    target_gcs_bucket: str,
    dest_current_data_folder_name: str,
    dest_historical_data_folder_name: str,
    source_bucket_current_data_folder_name: str,
    current_data_target_gcs_path: str,
    historical_data_target_gcs_path: str,
    data_root_folder: typing.List[str],
    hist_folders_list: typing.List[str],
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    root_gs_bucket_folder = f"gs://{source_bucket}"
    source_gs_folder = f"{root_gs_bucket_folder}/{source_bucket_current_data_folder_name}"
    execute_current_data_load(
        project_id=project_id,
        dataset_id=dataset_id,
        current_data_table_id=current_data_table_id,
        data_file_surr_key_field=data_file_surr_key_field,
        dest_folder=dest_folder,
        schema_filepath=schema_filepath,
        source_bucket=source_bucket,
        target_gcs_bucket=target_gcs_bucket,
        dest_current_data_folder_name=dest_current_data_folder_name,
        current_data_target_gcs_path=current_data_target_gcs_path,
        source_gs_folder=source_gs_folder,
        data_root_folder=data_root_folder,
        chunksize=chunksize,
        input_headers=input_headers,
        data_dtypes=data_dtypes,
        int_col_list=int_col_list
    )
    execute_historical_data_load(
        project_id=project_id,
        dataset_id=dataset_id,
        historical_data_table_id=historical_data_table_id,
        data_file_surr_key_field=data_file_surr_key_field,
        dest_folder=dest_folder,
        schema_filepath=schema_filepath,
        target_gcs_bucket=target_gcs_bucket,
        source_gs_folder=source_gs_folder,
        data_root_folder=data_root_folder,
        dest_historical_data_folder_name=dest_historical_data_folder_name,
        historical_data_target_gcs_path=historical_data_target_gcs_path,
        hist_folders_list=hist_folders_list,
        chunksize=chunksize,
        input_headers=input_headers,
        data_dtypes=data_dtypes,
        int_col_list=int_col_list
    )


def execute_current_data_load(
    project_id: str,
    dataset_id: str,
    current_data_table_id: str,
    data_file_surr_key_field: str,
    dest_folder: str,
    schema_filepath: str,
    target_gcs_bucket: str,
    dest_current_data_folder_name: str,
    current_data_target_gcs_path: str,
    source_gs_folder: str,
    data_root_folder: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    for folder in data_root_folder:
        new_dest_current_data_folder_name = f"{dest_folder}/{folder}/{dest_current_data_folder_name}"
        logging.info(f"Creating {new_dest_current_data_folder_name} if it does not exist")
        pathlib.Path(new_dest_current_data_folder_name).mkdir(parents=True, exist_ok=True)
        process_data(
            project_id = project_id,
            dataset_id = dataset_id,
            table_name = current_data_table_id,
            schema_filepath = schema_filepath,
            target_gcs_bucket = target_gcs_bucket,
            target_gcs_path = current_data_target_gcs_path,
            data_file_surr_key_field = data_file_surr_key_field,
            source_gs_folder = source_gs_folder,
            dest_folder = new_dest_current_data_folder_name,
            chunksize = chunksize,
            input_headers = input_headers,
            data_dtypes = data_dtypes,
            int_col_list = int_col_list
        )


def execute_historical_data_load(
    project_id: str,
    dataset_id: str,
    historical_data_table_id: str,
    data_file_surr_key_field: str,
    dest_folder: str,
    schema_filepath: str,
    target_gcs_bucket: str,
    source_gs_folder: str,
    data_root_folder: str,
    dest_historical_data_folder_name: str,
    historical_data_target_gcs_path: str,
    hist_folders_list: typing.List[str],
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    for folder in hist_folders_list:
        new_dest_historical_data_folder_name = f"{dest_folder}/{data_root_folder}/{dest_historical_data_folder_name}/{folder}"
        logging.info(f"Creating {new_dest_historical_data_folder_name} if it does not exist")
        pathlib.Path(new_dest_historical_data_folder_name).mkdir(parents=True, exist_ok=True)
        process_historical_data(
            project_id = project_id,
            dataset_id = dataset_id,
            table_name = historical_data_table_id,
            schema_filepath = schema_filepath,
            target_gcs_bucket = target_gcs_bucket,
            target_gcs_path = historical_data_target_gcs_path,
            hist_folders_list=hist_folders_list,
            data_file_surr_key_field = data_file_surr_key_field,
            source_gs_folder = source_gs_folder,
            dest_folder = new_dest_historical_data_folder_name,
            chunksize = chunksize,
            input_headers = input_headers,
            data_dtypes = data_dtypes,
            int_col_list = int_col_list
        )


def download_file_gcs(
    project_id: str,
    source_location: str,
    destination_folder: str
) -> None:
    object_name = os.path.basename(source_location)
    dest_object = f"{destination_folder}/{object_name}"
    logging.info(f"   ... {source_location} -> {dest_object}")
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def download_folder_contents(
    project_id: str,
    source_gcs_folder_path: str,  # eg. "gs://normals/normal-hourly/access"
    destination_folder: str,
    file_type: str = ""
) -> None:
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_gcs_folder_path, "gs://")[1].split("/")[0]
    gcs_folder_path = str.split(source_gcs_folder_path, f"gs://{bucket_name}/")[1]
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f'{gcs_folder_path}')
    for blob in blobs:
        if os.path.splitext(os.path.basename(blob.name))[1] == f".{file_type}" or file_type == "":
            source_location = f"{source_gcs_folder_path}/{os.path.basename(blob.name)}"
            download_file_gcs(
                project_id,
                source_location = source_location,
                destination_folder = destination_folder
            )


def process_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    schema_filepath: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    data_file_surr_key_field: str,
    source_gs_folder: str,
    dest_folder: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    download_folder_contents(
        project_id = project_id,
        source_gcs_folder_path = source_gs_folder,
        destination_folder = dest_folder,
        file_type = "csv"
    )
    for filename in sorted(os.listdir(dest_folder)):
        filepath = os.path.join(dest_folder, filename)
        if os.path.isfile(filepath) and filepath.endswith(".csv"):
            process_file(
                filepath=filepath,
                project_id = project_id,
                dataset_id = dataset_id,
                table_name = table_name,
                schema_path = schema_filepath,
                source_gs_folder=source_gs_folder,
                target_gcs_bucket = target_gcs_bucket,
                target_gcs_path = target_gcs_path,
                data_file_surr_key_field = data_file_surr_key_field,
                data_file_surr_key_value = f'{source_gs_folder.replace("gs://normals", "")}/{filename}',
                chunksize = chunksize,
                input_headers = input_headers,
                data_dtypes = data_dtypes,
                int_col_list = int_col_list
            )


def process_file(
    filepath: str,
    project_id: str,
    dataset_id: str,
    table_name: str,
    schema_path: str,
    source_gs_folder: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    data_file_surr_key_field: str,
    data_file_surr_key_value: int,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    logging.info(f"Processing file {filepath} started ...")
    if not table_exists(project_id, dataset_id, table_name):
        # Destination table doesn't exist
        create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_name,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
        )
    # if the table already has data for the file
    if table_already_has_file_data(
        project_id=project_id,
        dataset_id=dataset_id,
        table_name=table_name,
        data_file_surr_key_field=data_file_surr_key_value,
        data_file_surr_key_value=data_file_surr_key_value
    ):
        remove_file_table_data(
            project_id = project_id,
            dataset_id = dataset_id,
            table_name = table_name,
            data_file_surr_key_field = data_file_surr_key_field,
            data_file_surr_key_value = data_file_surr_key_value
        )
    etl_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with pd.read_csv(
        filepath,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),
        sep=",",
        names=input_headers,
        skiprows=1,
        dtype=data_dtypes,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(
                f"Processing chunk #{chunk_number} of file {filepath} started"
            )
            target_file_batch = str(filepath).replace(
                ".csv", f"-{chunk_number}.csv"
            )
            target_file = str(filepath).replace(
                ".csv", f"_load_file.csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df=df,
                target_file_batch=target_file_batch,
                target_file=target_file,
                include_header=(chunk_number == 0),
                truncate_file=(chunk_number == 0),
                output_headers=input_headers,
                data_file_surr_key_field=data_file_surr_key_field,
                data_file_surr_key_value=f'{source_gs_folder.replace("gs://normals", "")}/{os.path.basename(filepath)}',
                etl_timestamp=etl_timestamp,
                int_col_list=int_col_list
            )
            logging.info(
                f"Processing chunk #{chunk_number} of file {filepath} completed"
            )
    os.unlink(filepath)
    os.rename(target_file, filepath)
    load_data_to_bq(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_name,
        file_path=filepath,
        field_delimiter="|",
    )
    upload_file_to_gcs(
        file_path=filepath,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path
    )
    logging.info(f"Processing file {filepath} completed ...")


def process_historical_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    schema_filepath: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    hist_folders_list: typing.List[str],
    data_file_surr_key_field: str,
    source_gs_folder: str,
    dest_folder: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    int_col_list: typing.List[str]
) -> None:
    for fldr in hist_folders_list:
        source_gs_folder = source_gs_folder.replace('/access', f'/{fldr}/access')
        logging.info(f"Creating {dest_folder} if it does not exist")
        pathlib.Path(f"{dest_folder}").mkdir(parents=True, exist_ok=True)
        process_data(
            project_id=project_id,
            dataset_id=dataset_id,
            table_name=table_name,
            schema_filepath=schema_filepath,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            data_file_surr_key_field=data_file_surr_key_field,
            source_gs_folder=source_gs_folder,
            dest_folder=f"{dest_folder}",
            chunksize=chunksize,
            input_headers=input_headers,
            data_dtypes=data_dtypes,
            int_col_list=int_col_list
        )


def table_already_has_file_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    data_file_surr_key_field: str,
    data_file_surr_key_value: int
) -> bool:
    check_field_exists = field_exists(
        project_id, dataset_id, table_name, data_file_surr_key_field
    )
    if check_field_exists:
        client = bigquery.Client(project=project_id)
        query = f"""
            SELECT count(1) AS number_of_rows
              FROM {dataset_id}.{table_name}
             WHERE {data_file_surr_key_field} = '{data_file_surr_key_value}'
        """
        job_config = bigquery.QueryJobConfig()
        query_job = client.query(query, job_config=job_config)
        for row in query_job.result():
            count_rows = row.number_of_rows
        if int(count_rows) > 0:
            return True
        else:
            return False
    else:
        return None


def remove_file_table_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    data_file_surr_key_field: str,
    data_file_surr_key_value: int
) -> bool:
    check_field_exists = field_exists(
        project_id, dataset_id, table_name, data_file_surr_key_field
    )
    if check_field_exists:
        try:
            client = bigquery.Client(project=project_id)
            query = f"""
                DELETE
                FROM {dataset_id}.{table_name}
                WHERE {data_file_surr_key_field} = '{data_file_surr_key_value}'
            """
            query_job = client.query(query)  # API request
            query_job.result()
        except Exception as e:
            logging.info(e)
            return False
    else:
        return None


def table_exists(project_id: str, dataset_id: str, table_name: str) -> bool:
    client = bigquery.Client(project=project_id)
    tables = client.list_tables(dataset_id)
    found_table = False
    for tbl in tables:
        if tbl.table_id == table_name:
            found_table = True
    return found_table


def field_exists(
    project_id: str, dataset_id: str, table_name: str, field_name: str
) -> bool:
    if table_exists(project_id, dataset_id, table_name):
        client = bigquery.Client(project=project_id)
        table_ref = f"{dataset_id}.{table_name}"
        tbl_schema = client.get_table(table_ref).schema
        found_field = False
        for field in tbl_schema:
            if field.name == field_name:
                found_field = True
        return found_field
    else:
        return False


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
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
) -> None:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    try:
        table_exists_id = client.get_table(table_ref).table_id
        logging.info(f"Table {table_exists_id} currently exists.")
    except NotFound:
        logging.info(
            (
                f"Table {table_ref} currently does not exist.  Attempting to create table."
            )
        )
        schema = create_table_schema([], bucket_name, schema_filepath)
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Table {table_ref} was created".format(table_id))


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


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    include_header: bool,
    truncate_file: bool,
    output_headers: typing.List[str],
    data_file_surr_key_field: str,
    data_file_surr_key_value: str,
    etl_timestamp: str,
    int_col_list: typing.List[str]
) -> None:
    logging.info(" ... reordering columns")
    df = df[output_headers]
    logging.info(" ... formatting integer columns")
    df = format_int_columns(df, int_col_list)
    logging.info(" ... appending metadata")
    df["etl_timestamp"] = etl_timestamp
    df[data_file_surr_key_field] = data_file_surr_key_value
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, include_header, truncate_file)
    logging.info(f"Processing Batch {target_file_batch} completed")


def format_int_columns(
    df: pd.DataFrame,
    int_col_list: typing.List[str]
) -> pd.DataFrame:
    for col in int_col_list:
        df[col] = df[col].apply(lambda x: str(int(round(float("0" if math.isnan(x) else str(x))))))
    return df


def save_to_new_file(df, file_path, sep="|") -> None:
    logging.info(f"Saving to file {file_path} separator='{sep}'")
    df.to_csv(file_path, sep=sep, index=False)


def append_batch_file(
    batch_file_path: str,
    target_file_path: str,
    include_header: bool,
    truncate_target_file: bool,
) -> None:
    logging.info(
        f"Appending file {batch_file_path} to file {target_file_path} with include_header={include_header} and truncate_target_file={truncate_target_file}"
    )
    data_file = open(batch_file_path, "r")
    if truncate_target_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if not include_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} without header"
        )
        next(data_file)
    else:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with header"
        )
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


def upload_file_to_gcs(
    file_path: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    if os.path.exists(file_path):
        logging.info(
            f"Uploading output file {file_path} to gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket(target_gcs_bucket)
        blob = bucket.blob(target_gcs_path)
        blob.upload_from_filename(file_path)
    else:
        logging.info(
            f"Cannot upload file {file_path} to gs://{target_gcs_bucket}/{target_gcs_path} as it does not exist."
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        current_data_table_id=os.environ.get("CURRENT_DATA_TABLE_ID", ""),
        historical_data_table_id=os.environ.get("HISTORICAL_DATA_TABLE_ID", ""),
        data_file_surr_key_field=os.environ.get("DATA_FILE_SURR_KEY_FIELD", ""),
        dest_folder=os.environ.get("DEST_FOLDER", ""),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH", ""),
        source_bucket=os.environ.get("SOURCE_BUCKET", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        dest_current_data_folder_name=os.environ.get("DEST_CURRENT_DATA_FOLDER_NAME", ""),
        dest_historical_data_folder_name=os.environ.get("DEST_HISTORICAL_FOLDER_NAME", ""),
        source_bucket_current_data_folder_name=os.environ.get("SOURCE_BUCKET_CURRENT_DATA_FOLDER_NAME", ""),
        current_data_target_gcs_path=os.environ.get("CURRENT_DATA_TARGET_GCS_PATH", ""),
        historical_data_target_gcs_path=os.environ.get("HISTORICAL_DATA_TARGET_GCS_PATH", ""),
        data_root_folder=os.environ.get("DATA_ROOT_FOLDER", ""),
        hist_folders_list=json.loads(os.environ.get("HIST_FOLDERS_LIST", r"[]")),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        input_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        int_col_list=json.loads(os.environ.get("INT_COL_LIST", r"[]")),
    )
