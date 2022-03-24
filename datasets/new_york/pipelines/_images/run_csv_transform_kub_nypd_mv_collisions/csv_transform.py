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
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    data_dtypes: dict,
    schema_path: str,
    transform_list: typing.List[str],
    resolve_datatypes_list: dict,
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        data_dtypes=data_dtypes,
        schema_path=schema_path,
        resolve_datatypes_list=resolve_datatypes_list,
        transform_list=transform_list,
        reorder_headers_list=reorder_headers_list,
        rename_headers_list=rename_headers_list,
        regex_list=regex_list,
        crash_field_list=crash_field_list,
        date_format_list=date_format_list
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    data_dtypes: dict,
    schema_path: str,
    resolve_datatypes_list: dict,
    transform_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:
    download_file(source_url, source_file)
    process_source_file(
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        source_dtypes=data_dtypes,
        resolve_datatypes_list=resolve_datatypes_list,
        transform_list=transform_list,
        reorder_headers_list=reorder_headers_list,
        rename_headers_list=rename_headers_list,
        regex_list=regex_list,
        crash_field_list=crash_field_list,
        date_format_list=date_format_list,
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
                truncate_table=True
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
    truncate_table: bool
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
        table_exists_id = client.get_table(table_ref).table_id
        logging.info(f"Table {table_exists_id} currently exists.")
        table_exists = True
    except NotFound:
        logging.info(
            (
                f"Table {table_ref} currently does not exist.  Attempting to create table."
            )
        )
        try:
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
        except Exception as e:
            logging.info(f"Unable to create table. {e}")
            table_exists = False
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
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    source_dtypes: dict,
    resolve_datatypes_list: dict,
    transform_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:
    logging.info(f"Opening source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        sep=",",
        dtype=source_dtypes,
        chunksize=int(chunksize),
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
                resolve_datatypes_list=resolve_datatypes_list,
                transform_list=transform_list,
                reorder_headers_list=reorder_headers_list,
                rename_headers_list=rename_headers_list,
                regex_list=regex_list,
                crash_field_list=crash_field_list,
                date_format_list=date_format_list,
            )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    resolve_datatypes_list: dict,
    transform_list: list,
    reorder_headers_list: list,
    rename_headers_list: list,
    regex_list: list,
    crash_field_list: list,
    date_format_list: list,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    for transform in transform_list:
        if transform == "replace_regex":
            df = replace_regex(df, regex_list)
        elif transform == "add_crash_timestamp":
            for fld in crash_field_list:
                new_crash_field = fld[0]
                crash_date_field = fld[1]
                crash_time_field = fld[2]
                df[new_crash_field] = ""
                df = add_crash_timestamp(
                    df, new_crash_field, crash_date_field, crash_time_field
                )
        elif transform == "convert_date_format":
            df = resolve_date_format(df, date_format_list)
        elif transform == "resolve_datatypes":
            df = resolve_datatypes(df, resolve_datatypes_list)
        elif transform == "rename_headers":
            df = rename_headers(df, rename_headers_list)
        elif transform == "reorder_headers":
            df = reorder_headers(df, reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def resolve_datatypes(
    df: pd.DataFrame,
    resolve_datatypes_list: dict
) -> pd.DataFrame:
    logging.info("Resolving column datatypes")
    df = df.astype(resolve_datatypes_list, errors="ignore")
    return df


def reorder_headers(
    df: pd.DataFrame,
    headers_list: list
) -> pd.DataFrame:
    logging.info("Reordering Headers")
    df = df[headers_list]
    return df


def rename_headers(df: pd.DataFrame, header_list: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    header_names = header_list
    df.rename(columns=header_names, inplace=True)
    return df


def replace_regex(
    df: pd.DataFrame,
    regex_list: dict
) -> pd.DataFrame:
    for regex_item in regex_list:
        field_name = regex_item[0]
        search_expr = regex_item[1]
        replace_expr = regex_item[2]
        logging.info(
            f"Replacing data via regex on field {field_name} '{field_name}' '{search_expr}' '{replace_expr}'"
        )
        df[field_name] = df[field_name].replace(
            r"" + search_expr, replace_expr, regex=True
        )
    return df


def resolve_date_format(
    df: pd.DataFrame,
    date_fields: list = []
) -> pd.DataFrame:
    for dt_fld in date_fields:
        field_name = dt_fld[0]
        logging.info(f"Resolving date format in column {field_name}")
        from_format = dt_fld[1]
        to_format = dt_fld[2]
        df[field_name] = df[field_name].apply(
            lambda x: convert_dt_format(str(x), from_format, to_format)
        )
    return df


def convert_dt_format(
    dt_str: str,
    from_format: str,
    to_format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        dt_str = ""
        return dt_str
    else:
        if from_format == "%Y%m%d":
            year = dt_str[0:4]
            month = dt_str[4:6]
            day = dt_str[6:8]
            dt_str = f"{year}-{month}-{day} 00:00:00"
            from_format = "%Y-%m-%d %H:%M:%S"
        elif len(dt_str.strip().split(" ")[1]) == 8:
            # if format of time portion is 00:00:00 then use 00:00 format
            dt_str = dt_str[:-3]
        elif (len(dt_str.strip().split("-")[0]) == 4) and (
            len(from_format.strip().split("/")[0]) == 2
        ):
            # if the format of the date portion of the data is in YYYY-MM-DD format
            # and from_format is in MM-DD-YYYY then resolve this by modifying the from_format
            # to use the YYYY-MM-DD.  This resolves mixed date formats in files
            from_format = "%Y-%m-%d " + from_format.strip().split(" ")[1]
        return datetime.datetime.strptime(dt_str, from_format).strftime(to_format)


def add_crash_timestamp(
    df: pd.DataFrame,
    new_crash_field: str,
    crash_date_field: str,
    crash_time_field: str
) -> pd.DataFrame:
    logging.info(
        f"add_crash_timestamp '{new_crash_field}' '{crash_date_field}' '{crash_time_field}'"
    )
    df[new_crash_field] = df.apply(
        lambda x, crash_date_field, crash_time_field: crash_timestamp(
            x["" + crash_date_field], x["" + crash_time_field]
        ),
        args=[crash_date_field, crash_time_field],
        axis=1,
    )
    return df


def crash_timestamp(
    crash_date: str,
    crash_time: str
) -> str:
    # if crash time format is H:MM then convert to HH:MM:SS
    if len(crash_time) == 4:
        crash_time = f"0{crash_time}:00"
    return f"{crash_date} {crash_time}"


def save_to_new_file(
    df: pd.DataFrame,
    file_path: str,
    sep: str = "|"
) -> None:
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
            data_file.close()
            target_file.close()
            if os.path.exists(batch_file_path):
                os.remove(batch_file_path)


def download_file(
    source_url: str,
    source_file: pathlib.Path
) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def upload_file_to_gcs(
    file_path: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str
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
        source_url=os.environ["SOURCE_URL"],
        chunksize=os.environ["CHUNKSIZE"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        schema_path=os.environ["SCHEMA_PATH"],
        resolve_datatypes_list=json.loads(os.environ["RESOLVE_DATATYPES_LIST"]),
        transform_list=json.loads(os.environ["TRANSFORM_LIST"]),
        reorder_headers_list=json.loads(os.environ["REORDER_HEADERS_LIST"]),
        rename_headers_list=json.loads(os.environ["RENAME_HEADERS_LIST"]),
        regex_list=json.loads(os.environ["REGEX_LIST"]),
        crash_field_list=json.loads(os.environ["CRASH_FIELD_LIST"]),
        date_format_list=json.loads(os.environ["DATE_FORMAT_LIST"]),
    )
