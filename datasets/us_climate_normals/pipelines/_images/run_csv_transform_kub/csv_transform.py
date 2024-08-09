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

import datetime
import json
import logging
import os
import pathlib
import re
import subprocess
import typing

import airflow.providers.google.cloud.transfers.gcs_to_bigquery as gcs2bq
import google.api_core.exceptions as google_api_exceptions
import pandas as pd
from airflow import DAG
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound


def main(
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    table_prefix: str,
    source_local_folder_root: str,
    pipeline_name: str,
    root_gcs_folder: str,
    root_pipeline_gs_folder: str,
    folders_list: typing.List[str],
) -> None:
    logging.info(f"{pipeline_name} process started")
    source_local_schema_folder = f"{source_local_folder_root}/schema"
    for fldr in folders_list:
        if fldr == "":
            folder_to_process = f"{root_gcs_folder}/{root_pipeline_gs_folder}/access"
        else:
            folder_to_process = (
                f"{root_gcs_folder}/{root_pipeline_gs_folder}/{fldr}/access"
            )
        file_prefix = distinct_file_prefixes(
            project_id, target_gcs_bucket, folder_to_process, "csv"
        )
        for prefix in file_prefix:
            logging.info(f"Processing {prefix} files in {fldr} folder ...")
            logging.info(f"prefix={prefix} folder_to_process={folder_to_process}")
            if not prefix_files_exist(target_gcs_bucket, prefix, folder_to_process):
                logging.info(
                    f" ... No files exist with {prefix} prefix in folder {folder_to_process}.  Skipping."
                )
            else:
                first_file_path = return_first_file_for_prefix(
                    target_gcs_bucket, prefix, folder_to_process
                )
                if fldr == "":
                    fldr_ident = "access"
                else:
                    fldr_ident = str.replace(fldr, "/", "")
                destination_table = (
                    f'{table_prefix}_{prefix}_{fldr_ident.replace("-", "_")}'
                )
                schema_filepath_gcs_path = (
                    f"{root_gcs_folder}/schema/{root_pipeline_gs_folder}"
                )
                output_schema_file = f"{source_local_schema_folder}/{root_pipeline_gs_folder}/{destination_table}_schema.json"
                schema_file_path = (
                    f"{schema_filepath_gcs_path}/{os.path.basename(output_schema_file)}"
                )
                local_file_path = f"{source_local_folder_root}/{root_pipeline_gs_folder}/{fldr}/{os.path.basename(first_file_path)}"
                create_schema_and_table(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    destination_table=destination_table,
                    target_gcs_bucket=target_gcs_bucket,
                    output_schema_file=output_schema_file,
                    gcs_file_path=first_file_path,
                    local_file_path=local_file_path,
                    schema_filepath_gcs_path=schema_file_path,
                )
                prefix_file_list = list_of_files_prefix(
                    project_id=project_id,
                    gcs_bucket=target_gcs_bucket,
                    gcs_file_path=folder_to_process,
                    prefix=prefix,
                )
                truncate_tables_for_prefix(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_name_prefix=destination_table,
                )
                for filename in prefix_file_list:
                    print(f" ... {filename}")
                    local_source_folder = os.path.split(local_file_path)[0]
                    local_file_path = f"{local_source_folder}/{filename}"
                    if fldr_ident != "access":
                        fldr_ident += "/access"
                    source_file_gcs_full_path = f"gs://{target_gcs_bucket}/{root_gcs_folder}/{root_pipeline_gs_folder}/{fldr_ident}/{filename}"
                    download_file_gcs(
                        project_id=project_id,
                        source_location=source_file_gcs_full_path,
                        destination_folder=local_source_folder,
                    )
                    load_data_gcs_to_bq(
                        project_id=project_id,
                        dataset_id=dataset_id,
                        table_id=destination_table,
                        source_bucket=target_gcs_bucket,
                        output_schema_file=output_schema_file,
                        schema_filepath=schema_file_path,
                        gcs_file_path=source_file_gcs_full_path,
                        local_file_path=local_file_path,
                        field_delimiter=",",
                        truncate_load=(
                            os.path.basename(filename)
                            == os.path.basename(first_file_path)
                        ),
                    )
    logging.info(f"{pipeline_name} process completed")


def truncate_tables_for_prefix(
    project_id: str, dataset_id: str, table_name_prefix: str
) -> None:
    client = bigquery.Client(project=project_id)
    tables = client.list_tables(dataset_id)
    for table in tables:
        if table.table_id.startswith(table_name_prefix):
            truncate_table(
                project_id=project_id, dataset_id=dataset_id, table_id=table.table_id
            )


def truncate_table_if_exists(project_id: str, dataset_id: str, table_id: str) -> None:
    pass
    if table_exists(project_id, dataset_id, table_id):
        truncate_table(project_id=project_id, dataset_id=dataset_id, table_id=table_id)
    else:
        pass


def truncate_table(project_id: str, dataset_id: str, table_id: str):
    logging.info(f" ... Truncating table {project_id}.{dataset_id}.{table_id}")
    client = bigquery.Client(project=project_id)
    query = f"""
        TRUNCATE TABLE {project_id}.{dataset_id}.{table_id}
    """
    job_config = bigquery.QueryJobConfig()
    client.query(query, job_config=job_config)


def list_of_files_prefix(
    project_id: str, gcs_bucket: str, gcs_file_path: str, prefix: str
) -> typing.List[str]:
    # p = re.compile(
    #     f"^{prefix}([0-9]*)*\\.csv"
    # )  # make sure the file has a numeric digit directly after the prefix e.g. USW0001109.csv where USW is the prefix
    storage_client = storage.Client(project_id)
    bucket_file_list_blob = storage_client.list_blobs(
        gcs_bucket, prefix=f"{gcs_file_path}/", delimiter="/"
    )
    bucket_file_list_iter = list(bucket_file_list_blob)
    bucket_file_list = [
        str(item).split(",")[1].strip() for item in bucket_file_list_iter
    ]
    df = pd.DataFrame(bucket_file_list, columns=["filename"])
    df["filename"] = df["filename"].apply(
        lambda x, prefix: filter_to_prefix_list(prefix, os.path.basename(x)),
        args=[prefix],
    )
    df = df[df["filename"] != ""]
    df = df[df["filename"].notnull()]
    df = sorted(df["filename"].unique())
    return df


def filter_to_prefix_list(prefix: str, filename: str) -> str:
    reg_expr = f"^{prefix}([0-9]*)*\\.csv"
    filenm = re.match(reg_expr, filename)
    if filenm:
        return filenm.group(0)
    else:
        return None


def distinct_file_prefixes(
    project_id: str,
    gcs_bucket: str,
    filepath: str,
    file_ext: str,
) -> typing.List[str]:
    storage_client = storage.Client(project_id)
    bucket_file_list_blob = storage_client.list_blobs(
        gcs_bucket, prefix=f"{filepath}/", delimiter="/"
    )
    bucket_file_list_iter = list(bucket_file_list_blob)
    bucket_file_list = [
        str(item).split(",")[1].strip() for item in bucket_file_list_iter
    ]
    df = pd.DataFrame(bucket_file_list, columns=["filename"])
    df["filename"] = df["filename"].apply(
        lambda x: re.match(
            "^[a-zA-Z]*", os.path.basename(x).split(f".{file_ext}")[0]
        ).group(0)
    )
    df = df[df["filename"] != ""]
    df = sorted(df["filename"].unique())
    return df


def create_schema_and_table(
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    output_schema_file: str,
    gcs_file_path: str,
    local_file_path: str,
    schema_filepath_gcs_path: str,
) -> None:
    logging.info(
        f"creating schema and table ... destination_table={destination_table} target_gcs_bucket={target_gcs_bucket} output_schema_file={output_schema_file} file_path={gcs_file_path} schema_filepath_gcs_path={schema_filepath_gcs_path} "
    )
    table_already_exists = table_exists(project_id, dataset_id, destination_table)
    source_file_exists = gcs_file_exists(
        bucket=target_gcs_bucket, file_path=output_schema_file
    )
    if not table_already_exists:
        if not source_file_exists:
            generate_schema_file_from_gcs_source_file(
                project_id=project_id,
                gcs_file_path=gcs_file_path,
                local_file_path=local_file_path,
                output_schema_file=output_schema_file,
                schema_filepath_bucket=target_gcs_bucket,
                schema_filepath_gcs_path=schema_filepath_gcs_path,
                input_sep=",",
            )
        create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_filepath_gcs_path,
            bucket_name=target_gcs_bucket,
        )


def gcs_file_exists(bucket: str, file_path: str) -> bool:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    return storage.Blob(bucket=bucket, name=file_path).exists(storage_client)


def prefix_files_exist(gcs_bucket: str, prefix: str, folder_to_process: str) -> bool:
    command = f"gsutil ls gs://{gcs_bucket}/{folder_to_process}/* |grep '\\.csv'"
    files = sorted(str(subprocess.check_output(command, shell=True)).split("\\n"))
    return len(files) > 0


def return_first_file_for_prefix(
    gcs_bucket: str, prefix: str, folder_to_process: str
) -> str:
    command = f"gsutil ls gs://{gcs_bucket}/{folder_to_process}/{prefix}* |grep '.csv'"
    files = sorted(str(subprocess.check_output(command, shell=True)).split("\\n"))
    df = pd.DataFrame(files, columns=["filename"])
    df = df[df["filename"] != "'"]
    return str(sorted(df["filename"])[0]).replace("b'gs://", "gs://")


def extract_header_from_gcs_file(
    project_id: str,
    gcs_file_path: str,
    local_file_path: str,
    sep: str = ",",
) -> typing.List[str]:
    download_file_gcs(
        project_id=project_id,
        source_location=gcs_file_path,
        destination_folder=os.path.split(local_file_path)[0],
    )
    with open(local_file_path) as f:
        first_line = f.readline()
    return first_line.replace("-", "_").split(sep)


def generate_schema_file_from_gcs_source_file(
    project_id: str,
    gcs_file_path: str,
    local_file_path: str,
    output_schema_file: str,
    schema_filepath_bucket: str = "",
    schema_filepath_gcs_path: str = "",
    input_sep: str = ",",
) -> None:
    header = extract_header_from_gcs_file(
        project_id=project_id,
        gcs_file_path=gcs_file_path,
        local_file_path=local_file_path,
        sep=input_sep,
    )
    schema_content = "[\n"
    for fld in header:
        data_type = ""
        fld = fld.replace('"', "").strip()
        if fld in ("LATITUDE", "LONGITUDE", "ELEVATION"):
            data_type = "FLOAT"
        elif fld[len(fld) - 11 :] == "_ATTRIBUTES" or fld in (
            "STATION",
            "DATE",
            "NAME",
        ):
            data_type = "STRING"
        elif fld.find("flag") > -1:
            data_type = "STRING"
        elif data_type == "":
            data_type = "FLOAT"
        schema_content += f'  {{\n    "name": "{fld}",\n    "type": "{data_type}",\n    "mode": "NULLABLE",\n    "description": ""\n  }},\n'
    schema_content = schema_content[:-3]
    schema_content += "  }\n]\n"
    schema_file_pathname = os.path.dirname(output_schema_file)
    pathlib.Path(schema_file_pathname).mkdir(parents=True, exist_ok=True)
    with open(output_schema_file, "w+") as schema_file:
        schema_file.write(schema_content)
    upload_file_to_gcs(
        file_path=output_schema_file,
        target_gcs_bucket=schema_filepath_bucket,
        target_gcs_path=schema_filepath_gcs_path,
    )


def table_exists(project_id: str, dataset_id: str, table_name: str) -> bool:
    client = bigquery.Client(project=project_id)
    tables = client.list_tables(dataset_id)
    found_table = False
    for tbl in tables:
        if tbl.table_id == table_name:
            found_table = True
    return found_table


def load_data_gcs_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    source_bucket: str,
    schema_filepath: str,
    gcs_file_path: str,
    local_file_path: str,
    output_schema_file: str,
    field_delimiter: str,
    truncate_load: bool = False,
) -> None:
    if truncate_load:
        logging.info(
            f"Loading data from {local_file_path} into {project_id}.{dataset_id}.{table_id} (with truncate table) started"
        )
    else:
        logging.info(
            f"Loading data from {local_file_path} into {project_id}.{dataset_id}.{table_id} (with append data) started"
        )
    if truncate_load:
        write_disposition = "WRITE_TRUNCATE"
    else:
        write_disposition = "WRITE_APPEND"
    default_args = {
        "owner": "default_user",
        "start_date": datetime.datetime.now() - datetime.timedelta(days=2),
        "depends_on_past": False,
        "retries": 5,
        "retry_delay": datetime.timedelta(minutes=1),
    }
    gcs_file_path = gcs_file_path.replace(f"gs://{source_bucket}/", "")
    try:
        with DAG("tempDAG", default_args=default_args) as dag:
            if not truncate_load:
                load_data = gcs2bq.GCSToBigQueryOperator(
                    dag=dag,
                    task_id="load_source_data",
                    bucket=source_bucket,
                    source_objects=[gcs_file_path],
                    field_delimiter=field_delimiter,
                    destination_project_dataset_table=f"us_climate_normals.{table_id}",
                    skip_leading_rows=1,
                    schema_object=schema_filepath,
                    write_disposition=f"{write_disposition}",
                )
            else:
                load_data = gcs2bq.GCSToBigQueryOperator(
                    dag=dag,
                    task_id="load_source_data",
                    bucket=source_bucket,
                    source_objects=[gcs_file_path],
                    field_delimiter=field_delimiter,
                    destination_project_dataset_table=f"us_climate_normals.{table_id}",
                    skip_leading_rows=1,
                    schema_object=schema_filepath,
                    write_disposition=f"{write_disposition}",
                )
            load_data.execute("load_source_data")
    except google_api_exceptions.BadRequest:
        load_ext_schema(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            ext_surr_val=1,
            source_bucket=source_bucket,
            gcs_file_path=gcs_file_path,
            local_file_path=local_file_path,
            schema_filepath=schema_filepath,
            output_schema_file=output_schema_file,
            dag=dag,
            write_disposition=write_disposition,
            field_delimiter=field_delimiter,
        )
    logging.info(
        f"Loading data from {gcs_file_path} into {project_id}.{dataset_id}.{table_id} completed"
    )


def load_ext_schema(
    project_id: str,
    dataset_id: str,
    table_id: str,
    ext_surr_val: int,
    source_bucket: str,
    gcs_file_path: str,
    local_file_path: str,
    schema_filepath: str,
    output_schema_file: str,
    dag: DAG,
    write_disposition: str,
    field_delimiter: str = ",",
) -> None:
    ext = f"ext_{str(ext_surr_val).zfill(3)}"
    destination_table = f"{table_id}_{ext}"
    schema_file_path = schema_filepath.replace("_schema.json", f"_{ext}_schema.json")
    output_schema_file_ext = output_schema_file.replace(
        "_schema.json", f"_{ext}_schema.json"
    )
    task_id = f"load_{destination_table}"
    full_gcs_file_path = f"gs://{source_bucket}/{gcs_file_path}"
    try:
        print("*** SCHEMA DIFFERENT FROM TABLE - CREATING ADDITIONAL TABLE ***")
        if not table_exists(project_id, dataset_id, destination_table):
            create_schema_and_table(
                project_id=project_id,
                dataset_id=dataset_id,
                destination_table=destination_table,
                target_gcs_bucket=source_bucket,
                output_schema_file=output_schema_file_ext,
                gcs_file_path=full_gcs_file_path,
                local_file_path=local_file_path,
                schema_filepath_gcs_path=schema_file_path,
            )
        load_data = gcs2bq.GCSToBigQueryOperator(
            dag=dag,
            task_id=task_id,
            bucket=source_bucket,
            source_objects=[gcs_file_path],
            field_delimiter=field_delimiter,
            allow_quoted_newlines=True,
            quote_character='"',
            destination_project_dataset_table=f"us_climate_normals.{destination_table}",
            skip_leading_rows=1,
            schema_object=schema_file_path,
            write_disposition=f"{write_disposition}",
            autodetect=False,
        )
        load_data.execute(task_id)
    except google_api_exceptions.BadRequest:
        if ext_surr_val < 999:
            load_ext_schema(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                ext_surr_val=(ext_surr_val + 1),
                source_bucket=source_bucket,
                gcs_file_path=gcs_file_path,
                local_file_path=local_file_path,
                schema_filepath=schema_file_path,
                output_schema_file=output_schema_file,
                dag=dag,
                write_disposition=write_disposition,
                field_delimiter=field_delimiter,
            )
        else:
            raise ("Error: Total number of extension schemas exceeded.")


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


def download_file_gcs(
    project_id: str, source_location: str, destination_folder: str
) -> None:
    pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)
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
    source_gcs_folder_path: str,
    destination_folder: str,
    file_type: str = "",
) -> None:
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_gcs_folder_path, "gs://")[1].split("/")[0]
    gcs_folder_path = str.split(source_gcs_folder_path, f"gs://{bucket_name}/")[1]
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f"{gcs_folder_path}")
    for blob in blobs:
        if (
            os.path.splitext(os.path.basename(blob.name))[1] == f".{file_type}"
            or file_type == ""
        ):
            source_location = f"{source_gcs_folder_path}/{os.path.basename(blob.name)}"
            download_file_gcs(
                project_id,
                source_location=source_location,
                destination_folder=destination_folder,
            )


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
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        table_prefix=os.environ.get("TABLE_PREFIX", ""),
        source_local_folder_root=os.environ.get("SOURCE_LOCAL_FOLDER_ROOT", ""),
        root_gcs_folder=os.environ.get("ROOT_GCS_FOLDER", ""),
        root_pipeline_gs_folder=os.environ.get("ROOT_PIPELINE_GS_FOLDER", ""),
        folders_list=json.loads(os.environ.get("FOLDERS_LIST", r"[]")),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
    )
