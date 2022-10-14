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
import typing

import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url_stations_json: str,
    source_url_status_json: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    data_dtypes: dict,
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url_stations_json=source_url_stations_json,
        source_url_status_json=source_url_status_json,
        chunksize=chunksize,
        source_file=source_file,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        data_dtypes=data_dtypes,
        rename_headers_list=rename_headers_list,
        output_headers_list=output_headers_list,
        datetime_fieldlist=datetime_fieldlist,
        resolve_datatypes_list=resolve_datatypes_list,
        normalize_data_list=normalize_data_list,
        boolean_datapoints_list=boolean_datapoints_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url_stations_json: str,
    source_url_status_json: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    data_dtypes: dict,
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> None:
    download_and_merge_source_files(
        source_url_stations_json=source_url_stations_json,
        source_url_status_json=source_url_status_json,
        source_file=source_file,
        resolve_datatypes_list=resolve_datatypes_list,
        normalize_data_list=normalize_data_list,
        boolean_datapoints_list=boolean_datapoints_list,
    )
    process_source_file(
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        data_dtypes=data_dtypes,
        rename_headers_list=rename_headers_list,
        output_headers_list=output_headers_list,
        datetime_fieldlist=datetime_fieldlist,
        resolve_datatypes_list=resolve_datatypes_list,
        normalize_data_list=normalize_data_list,
        boolean_datapoints_list=boolean_datapoints_list,
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
                truncate_table=True,
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = "|"
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


def process_source_file(
    source_file: str,
    target_file: str,
    chunksize: str,
    data_dtypes: dict,
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> None:
    logging.info(f"Processing source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),
        sep="|",
        dtype=data_dtypes,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df=df,
                target_file_batch=target_file_batch,
                target_file=target_file,
                skip_header=(not chunk_number == 0),
                rename_headers_list=rename_headers_list,
                output_headers_list=output_headers_list,
                datetime_fieldlist=datetime_fieldlist,
                resolve_datatypes_list=resolve_datatypes_list,
                normalize_data_list=normalize_data_list,
                boolean_datapoints_list=boolean_datapoints_list,
            )


def download_and_merge_source_files(
    source_url_stations_json: str,
    source_url_status_json: str,
    source_file: str,
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str]
) -> None:
    source_file_stations_csv = str(source_file).replace(".csv", "") + "_stations.csv"
    source_file_stations_json = str(source_file).replace(".csv", "") + "_stations"
    source_file_status_csv = str(source_file).replace(".csv", "") + "_status.csv"
    source_file_status_json = str(source_file).replace(".csv", "") + "_status"
    download_file_json(
        source_url_stations_json, source_file_stations_json, source_file_stations_csv
    )
    download_file_json(
        source_url_status_json, source_file_status_json, source_file_status_csv
    )
    df_stations = pd.read_csv(
        source_file_stations_csv, engine="python", encoding="utf-8", quotechar='"'
    )
    df_status = pd.read_csv(
        source_file_status_csv, engine="python", encoding="utf-8", quotechar='"'
    )
    logging.info("Merging files")
    df = df_stations.merge(df_status, left_on="station_id", right_on="station_id")
    df = clean_data_points(
        df,
        resolve_datatypes_list=resolve_datatypes_list,
        normalize_data_list=normalize_data_list,
        boolean_datapoints_list=boolean_datapoints_list,
    )
    save_to_new_file(df, source_file)


def download_file_json(
    source_url: str, source_file_json: pathlib.Path, source_file_csv: pathlib.Path
) -> None:
    logging.info(f"Downloading file {source_url}.json.")
    r = requests.get(source_url + ".json", stream=True)
    with open(source_file_json + ".json", "wb") as f:
        for chunk in r:
            f.write(chunk)
    df = pd.read_json(source_file_json + ".json")["data"]["stations"]
    df = pd.DataFrame(df)
    df.to_csv(source_file_csv, index=False)


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = convert_datetime_from_int(df, datetime_fieldlist)
    # df = clean_data_points(
    #     df,
    #     resolve_datatypes_list=resolve_datatypes_list,
    #     normalize_data_list=normalize_data_list,
    #     boolean_datapoints_list=boolean_datapoints_list,
    # )
    df = rename_headers(df, rename_headers_list)
    df = reorder_headers(df, output_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(
        batch_file_path=target_file_batch,
        target_file_path=target_file,
        skip_header=skip_header,
        truncate_file=not (skip_header),
    )
    logging.info(f"Processing batch file {target_file_batch} completed")


def convert_datetime_from_int(
    df: pd.DataFrame, datetime_columns_list: typing.List[str]
) -> pd.DataFrame:
    for column in datetime_columns_list:
        logging.info(f"Converting Datetime column {column}")
        df[column] = df[column].astype(str).astype(int).apply(datetime_from_int)
    return df


def datetime_from_int(dt_int: int) -> str:
    return datetime.datetime.fromtimestamp(dt_int).strftime("%Y-%m-%d %H:%M:%S")


def clean_data_points(
    df: pd.DataFrame,
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> pd.DataFrame:
    df = resolve_datatypes(df, resolve_datatypes_list)
    df = normalize_data(df, normalize_data_list)
    df = resolve_boolean_datapoints(df, boolean_datapoints_list)
    return df


def resolve_datatypes(df: pd.DataFrame, resolve_datatypes_list: dict) -> pd.DataFrame:
    for column, datatype in resolve_datatypes_list.items():
        logging.info(f"Resolving datatype for column {column} to {datatype}")
        if datatype in ('Int64', 'Float'):
            df[column] = df[column].fillna(0).astype(datatype)
        else:
            df[column] = df[column].astype(datatype)
    return df


def normalize_data(
    df: pd.DataFrame, normalize_data_list: typing.List[str]
) -> pd.DataFrame:
    for column in normalize_data_list:
        logging.info(f"Normalizing data in column {column}")
        # Data is in list format in this column.
        # Therefore remove square brackets and single quotes
        df[column] = (
            str(pd.Series(df[column])[0])
            .replace("[", "")
            .replace("'", "")
            .replace("]", "")
        )
    return df


def resolve_boolean_datapoints(
    df: pd.DataFrame, boolean_datapoints_list: typing.List[str]
) -> pd.DataFrame:
    for column in boolean_datapoints_list:
        logging.info(f"Resolving boolean datapoints in column {column}")
        df[column] = df[column].apply(lambda x: "True" if x == "0" else "False")
    return df


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    df.rename(columns=rename_headers_list, inplace=True)
    return df


def reorder_headers(
    df: pd.DataFrame, output_headers_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Re-ordering Headers")
    return df[output_headers_list]


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    with open(batch_file_path, "r") as data_file:
        if truncate_file:
            target_file = open(target_file_path, "w+").close()
        with open(target_file_path, "a+") as target_file:
            if skip_header:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
                )
                next(data_file)
            else:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path}"
                )
            target_file.write(data_file.read())
            if os.path.exists(batch_file_path):
                os.remove(batch_file_path)


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
        pipeline_name=os.environ["PIPELINE_NAME"],
        source_url_stations_json=os.environ["SOURCE_URL_STATIONS_JSON"],
        source_url_status_json=os.environ["SOURCE_URL_STATUS_JSON"],
        chunksize=os.environ["CHUNKSIZE"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        schema_path=os.environ["SCHEMA_PATH"],
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        rename_headers_list=json.loads(os.environ["RENAME_HEADERS_LIST"]),
        output_headers_list=json.loads(os.environ["OUTPUT_CSV_HEADERS"]),
        datetime_fieldlist=json.loads(os.environ["DATETIME_FIELDLIST"]),
        resolve_datatypes_list=json.loads(os.environ["RESOLVE_DATATYPES_LIST"]),
        normalize_data_list=json.loads(os.environ["NORMALIZE_DATA_LIST"]),
        boolean_datapoints_list=json.loads(os.environ["BOOLEAN_DATAPOINTS"]),
    )
