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
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    input_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:
    logging.info(f"{pipeline_name} process started")
    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        chunksize=chunksize,
        source_file=source_file,
        target_file=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=destination_table,
        schema_path=schema_path,
        date_format_list=date_format_list,
        int_cols_list=int_cols_list,
        remove_newlines_cols_list=remove_newlines_cols_list,
        null_rows_list=null_rows_list,
        input_headers=input_headers,
        data_dtypes=data_dtypes,
        rename_headers_list=rename_headers_list,
        reorder_headers_list=reorder_headers_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    input_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:
    download_file_http(source_url, source_file)
    process_source_file(
        source_file=source_file,
        chunksize=chunksize,
        target_file=target_file,
        destination_table=destination_table,
        input_headers=input_headers,
        dtypes=data_dtypes,
        date_format_list=date_format_list,
        int_cols_list=int_cols_list,
        remove_newlines_cols_list=remove_newlines_cols_list,
        null_rows_list=null_rows_list,
        reorder_headers_list=reorder_headers_list,
        rename_headers_list=rename_headers_list,
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
    destination_table: str,
    input_headers: typing.List[str],
    dtypes: dict,
    chunksize: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
) -> None:
    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=0,  # use when the data file does not contain a header
        names=input_headers,
        dtype=dtypes,
        keep_default_na=True,
        na_values=[" "],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            import pdb; pdb.set_trace()
            process_chunk(
                df=df,
                target_file_batch=target_file_batch,
                target_file=target_file,
                destination_table=destination_table,
                include_header=(chunk_number == 0),
                truncate_file=(chunk_number == 0),
                date_format_list=date_format_list,
                int_cols_list=int_cols_list,
                remove_newlines_cols_list=remove_newlines_cols_list,
                null_rows_list=null_rows_list,
                reorder_headers_list=reorder_headers_list,
                rename_headers_list=rename_headers_list,
            )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    destination_table: str,
    include_header: bool,
    truncate_file: bool,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
) -> None:
    logging.info(f"Processing Batch {target_file_batch} started")
    if destination_table == "311_service_requests":
        df = rename_headers(df=df, rename_headers_list=rename_headers_list)
        for col in remove_newlines_cols_list:
            logging.info(f"Removing newlines from {col}")
            df[col] = (
                df[col]
                .replace({r"\s+$": "", r"^\s+": ""}, regex=True)
                .replace(r"\n", " ", regex=True)
            )
        df = filter_null_rows(df, null_rows_list)
        for int_col in int_cols_list:
            df[int_col] = df[int_col].fillna(0).astype("int32")
        df = reorder_headers(df=df, reorder_headers_list=reorder_headers_list)
    elif destination_table == "bikeshare_trips":
        df = rename_headers(df=df, rename_headers_list=rename_headers_list)
        df = filter_null_rows(df, null_rows_list)
        logging.info("Merging date/time into start_time")
        df["start_time"] = df["time"] + " " + df["checkout_time"]
        for dt_col in date_format_list:
            logging.info(f"Converting Date Format {dt_col}")
            df[dt_col] = df[dt_col].apply(
                lambda x: datetime.datetime.strptime(
                    str(x), "%m/%d/%Y %H:%M:%S"
                ).strftime("%Y-%m-%d %H:%M:%S")
            )
        df = reorder_headers(df=df, reorder_headers_list=reorder_headers_list)
    else:
        logging.info("Pipeline Not Recognized.")
        return None
    save_to_new_file(df=df, file_path=str(target_file_batch), sep="|")
    append_batch_file(
        batch_file_path=target_file_batch,
        target_file_path=target_file,
        include_header=include_header,
        truncate_target_file=truncate_file,
    )
    logging.info(f"Processing Batch {target_file_batch} completed")


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    return df.rename(columns=rename_headers_list)


def reorder_headers(
    df: pd.DataFrame, reorder_headers_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Reordering headers..")
    return df[reorder_headers_list]


def filter_null_rows(
    df: pd.DataFrame, null_rows_list: typing.List[str]
) -> pd.DataFrame:
    for col in null_rows_list:
        df = df[df[col] != ""]
    return df


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def download_file_http(
    source_url: str, source_file: pathlib.Path, continue_on_error: bool = False
) -> bool:
    logging.info(f"Downloading {source_url} to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        rtn_status_code = src_file.status_code
        if 400 <= rtn_status_code <= 499:
            logging.info(
                f"Unable to download file {source_url} (error code was {rtn_status_code})"
            )
            return False
        else:
            with open(source_file, "wb") as f:
                for chunk in src_file:
                    f.write(chunk)
            return True
    except requests.exceptions.RequestException as e:
        if e == requests.exceptions.HTTPError:
            err_msg = "A HTTP error occurred."
        elif e == requests.exceptions.Timeout:
            err_msg = "A HTTP timeout error occurred."
        elif e == requests.exceptions.TooManyRedirects:
            err_msg = "Too Many Redirects occurred."
        if not continue_on_error:
            logging.info(f"{err_msg} Unable to obtain {source_url}")
            raise SystemExit(e)
        else:
            logging.info(f"{err_msg} Unable to obtain {source_url}.")
        return False


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
    drop_table: bool = False,
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


def append_batch_file(
    batch_file_path: str,
    target_file_path: str,
    include_header: bool,
    truncate_target_file: bool,
) -> None:
    logging.info(
        f"Appending file {batch_file_path} to file {target_file_path} with include_header={include_header} and truncate_target_file={truncate_target_file}"
    )
    with open(batch_file_path, "r") as data_file:
        if truncate_target_file:
            target_file = open(target_file_path, "w+").close()
        with open(target_file_path, "a+") as target_file:
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
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        destination_table=os.environ.get("DESTINATION_TABLE", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", r"{}")),
        int_cols_list=json.loads(os.environ.get("INT_COLS_LIST", r"[]")),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"{}")),
        remove_newlines_cols_list=json.loads(
            os.environ.get("REMOVE_NEWLINES_COLS_LIST", r"[]")
        ),
        null_rows_list=json.loads(os.environ.get("NULL_ROWS_LIST", r"[]")),
        input_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
    )
