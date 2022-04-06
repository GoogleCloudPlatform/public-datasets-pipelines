# Copyright 2021 Google LLC
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
    source_url: str,
    pipeline_name: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    date_format_list: typing.List[str],
    reorder_headers_list: typing.List[str],
) -> None:

    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        schema_path=schema_path,
        chunksize=chunksize,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        input_headers=input_headers,
        rename_headers_list=rename_headers_list,
        empty_key_list=empty_key_list,
        gen_location_list=gen_location_list,
        resolve_datatypes_list=resolve_datatypes_list,
        remove_paren_list=remove_paren_list,
        strip_newlines_list=strip_newlines_list,
        strip_whitespace_list=strip_whitespace_list,
        date_format_list=date_format_list,
        reorder_headers_list=reorder_headers_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    date_format_list: typing.List[str],
    reorder_headers_list: typing.List[str],
) -> None:
    if destination_table == "bikeshare_station_info":
        source_url_json = f"{source_url}.json"
        source_file_stations_json = str(source_file).replace(".csv", "") + "_stations.json"
        download_file_json(
            source_url_json, source_file_stations_json, source_file, "stations"
        )
    elif destination_table == "311_service_requests":
        download_file(source_url, source_file)
    process_source_file(
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        input_headers=input_headers,
        destination_table=destination_table,
        rename_headers_list=rename_headers_list,
        empty_key_list=empty_key_list,
        gen_location_list=gen_location_list,
        resolve_datatypes_list=resolve_datatypes_list,
        remove_paren_list=remove_paren_list,
        strip_newlines_list=strip_newlines_list,
        strip_whitespace_list=strip_whitespace_list,
        date_format_list=date_format_list,
        reorder_headers_list=reorder_headers_list,
    )
    if os.path.exists(target_file):
        # upload_file_to_gcs(
        #     file_path=target_file,
        #     target_gcs_bucket=target_gcs_bucket,
        #     target_gcs_path=target_gcs_path,
        # )
        if destination_table == "bikeshare_station_info":
            drop_table = True
        else:
            drop_table = False
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
            drop_table=drop_table
        )
        if table_exists:
                load_data_to_bq(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=destination_table,
                    file_path=target_file,
                    truncate_table=True,
                    field_delimiter="|",
                )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def process_source_file(
    source_file: str,
    target_file: str,
    chunksize: str,
    input_headers: typing.List[str],
    destination_table: str,
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    date_format_list: typing.List[str],
    reorder_headers_list: typing.List[str],
) -> None:
    logging.info(f"Opening source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        # header=1,  # use when the data file does not contain a header
        # names=input_headers,
        keep_default_na=True,
        na_values=[" "],
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
                destination_table=destination_table,
                rename_headers_list=rename_headers_list,
                empty_key_list=empty_key_list,
                gen_location_list=gen_location_list,
                resolve_datatypes_list=resolve_datatypes_list,
                remove_paren_list=remove_paren_list,
                strip_newlines_list=strip_newlines_list,
                strip_whitespace_list=strip_whitespace_list,
                date_format_list=date_format_list,
                reorder_headers_list=reorder_headers_list,
            )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    destination_table: str,
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    date_format_list: typing.List[str],
    reorder_headers_list: typing.List[str],
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    if destination_table == "311_service_requests":
        df = rename_headers(df, rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = resolve_datatypes(df, resolve_datatypes_list)
        df = remove_parenthesis_long_lat(df, remove_paren_list)
        df = strip_whitespace(df, strip_whitespace_list)
        df = strip_newlines(df, strip_newlines_list)
        df = resolve_date_format(df, date_format_list)
        df = reorder_headers(df, reorder_headers_list)
    if destination_table == "bikeshare_station_info":
        df = rename_headers(df, rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = generate_location(df, gen_location_list)
        df = resolve_datatypes(df, resolve_datatypes_list)
        df = reorder_headers(df, reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch), sep="|")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading file {source_file} from {source_url}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def download_file_json(
    source_url: str,
    source_file_json: pathlib.Path,
    source_file_csv: pathlib.Path,
    subnode_name: str,
) -> None:
    logging.info(f"Downloading file {source_url}.json.")
    r = requests.get(source_url, stream=True)
    with open(f"{source_file_json}.json", "wb") as f:
        for chunk in r:
            f.write(chunk)
    df = pd.read_json(f"{source_file_json}.json")["data"][subnode_name]
    df = pd.DataFrame(df)
    df.to_csv(source_file_csv, index=False)
    # import pdb; pdb.set_trace()


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
    field_delimiter: str = "|",
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = field_delimiter
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
    drop_table: bool = False
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    table_exists = False
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


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    df.rename(columns=rename_headers_list, inplace=True)
    return df


def remove_empty_key_rows(
    df: pd.DataFrame, empty_key_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Removing rows with empty keys")
    for key_field in empty_key_list:
        df = df[df[key_field] != ""]
    return df


def resolve_datatypes(df: pd.DataFrame, resolve_datatypes_list: dict) -> pd.DataFrame:
    logging.info("Resolving datatypes")
    for key, value in resolve_datatypes_list.items():
        df[key] = df[key].astype(value)
    return df


def remove_parenthesis_long_lat(
    df: pd.DataFrame, remove_paren_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Removing parenthesis from geographic fields")
    for paren_fld in remove_paren_list:
        df[paren_fld].replace("(", "", regex=False, inplace=True)
        df[paren_fld].replace(")", "", regex=False, inplace=True)
    return df


def generate_location(df: pd.DataFrame, gen_location_list: dict) -> pd.DataFrame:
    for key, values in gen_location_list.items():
        df[key] = (
            "POINT("
            + df[values[0]][:].astype("string")
            + " "
            + df[values[1]][:].astype("string")
            + ")"
        )
    return df


def strip_whitespace(
    df: pd.DataFrame, strip_whitespace_list: typing.List[str]
) -> pd.DataFrame:
    for ws_fld in strip_whitespace_list:
        logging.info(f"Stripping whitespaces in column {ws_fld}")
        df[ws_fld] = df[ws_fld].apply(lambda x: str(x).strip())
    return df


def strip_newlines(
    df: pd.DataFrame, strip_newlines_list: typing.List[str]
) -> pd.DataFrame:
    for ws_fld in strip_newlines_list:
        logging.info(f"Stripping newlines in column {ws_fld}")
        df[ws_fld] = df[ws_fld].str.replace(r'\n', '', regex=True)
        df[ws_fld] = df[ws_fld].str.replace(r'\r', '', regex=True)
    return df


def resolve_date_format(
    df: pd.DataFrame, date_format_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Resolving date formats")
    for dt_fld in date_format_list:
        df[dt_fld] = df[dt_fld].apply(convert_dt_format)
    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif (
        dt_str.strip()[2] == "/"
    ):  # if there is a '/' in 3rd position, then we have a date format mm/dd/yyyy
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def reorder_headers(
    df: pd.DataFrame, output_headers_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Re-ordering Headers")
    return df[output_headers_list]


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


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
        source_url=os.environ.get("SOURCE_URL", ""),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", "100000"),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        input_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", r"[]")),
        empty_key_list=json.loads(os.environ.get("EMPTY_KEY_LIST", r"[]")),
        gen_location_list=json.loads(os.environ.get("GEN_LOCATION_LIST", r"{}")),
        resolve_datatypes_list=json.loads(
            os.environ.get("RESOLVE_DATATYPES_LIST", r"{}")
        ),
        remove_paren_list=json.loads(os.environ.get("REMOVE_PAREN_LIST", r"[]")),
        strip_newlines_list=json.loads(
            os.environ.get("STRIP_NEWLINES_LIST", r"[]")
        ),
        strip_whitespace_list=json.loads(
            os.environ.get("STRIP_WHITESPACE_LIST", r"[]")
        ),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"[]")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
    )
