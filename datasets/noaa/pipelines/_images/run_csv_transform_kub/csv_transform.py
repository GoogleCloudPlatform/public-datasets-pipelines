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

import csv
import datetime
import ftplib
import gzip
import json
import logging
import os
import pathlib
import time
import typing


import pandas as pd
# import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    full_data_load: str,
    start_year: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    output_csv_headers: typing.List[str],
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str]
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        pipeline_name=pipeline_name,
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        ftp_host=ftp_host,
        ftp_dir=ftp_dir,
        ftp_filename=ftp_filename,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        drop_dest_table=drop_dest_table,
        input_field_delimiter=input_field_delimiter,
        full_data_load=full_data_load,
        start_year=start_year,
        input_csv_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        output_csv_headers=output_csv_headers,
        reorder_headers_list=reorder_headers_list,
        null_rows_list=null_rows_list,
        date_format_list=date_format_list
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    pipeline_name: str,
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    full_data_load: str,
    start_year: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    output_csv_headers: typing.List[str],
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str]
) -> None:
    if pipeline_name == "GHCND by year":
        if full_data_load == "N":
            start_year = str(datetime.datetime.now().year - 6)
        else:
            pass
        for yr in range(int(start_year), datetime.datetime.now().year + 1):
            yr_str = str(yr)
            source_zipfile=str.replace(str(source_file), ".csv", f"_{yr_str}.csv.gz")
            source_file_unzipped=str.replace(str(source_zipfile), ".csv.gz", ".csv")
            target_file_year=str.replace(str(target_file), ".csv", f"_{yr_str}.csv")
            destination_table_year=f"{destination_table}_{yr_str}"
            source_url_year=str.replace(source_url, ".csv.gz", f"{yr_str}.csv.gz")
            target_gcs_path_year=str.replace(target_gcs_path, ".csv", f"_{yr_str}.csv")
            download_file_ftp(
                ftp_host=ftp_host,
                ftp_dir=ftp_dir,
                ftp_filename=f"{yr_str}.csv.gz",
                local_file=source_zipfile,
                source_url=source_url_year
            )
            gz_decompress(
                infile=source_zipfile,
                tofile=source_file_unzipped
            )
            process_and_load_table(
                source_file=source_file_unzipped,
                target_file=target_file_year,
                pipeline_name=pipeline_name,
                source_url=source_url_year,
                chunksize=chunksize,
                project_id=project_id,
                dataset_id=dataset_id,
                destination_table=destination_table_year,
                target_gcs_bucket=target_gcs_bucket,
                target_gcs_path=target_gcs_path_year,
                schema_path=schema_path,
                drop_dest_table=drop_dest_table,
                input_field_delimiter=input_field_delimiter,
                input_csv_headers=input_csv_headers,
                data_dtypes=data_dtypes,
                reorder_headers_list=reorder_headers_list,
                null_rows_list=null_rows_list,
                date_format_list=date_format_list
            )

def process_and_load_table(
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str]
) -> None:
    process_source_file(
        source_url=source_url,
        source_file=source_file,
        pipeline_name=pipeline_name,
        chunksize=chunksize,
        input_csv_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        target_file=target_file,
        reorder_headers_list=reorder_headers_list,
        null_rows_list=null_rows_list,
        date_format_list=date_format_list,
        input_field_delimiter=input_field_delimiter,
        destination_table=destination_table
    )
    if os.path.exists(target_file):
        upload_file_to_gcs(
            file_path=target_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
        if drop_dest_table == "Y":
            drop_table = True
        else:
            drop_table = False
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
            drop_table=drop_table,
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
    chunksize: str,
    input_csv_headers: str,
    pipeline_name: str,
    data_dtypes: str,
    source_url: str,
    target_file: str,
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str],
    input_field_delimiter: str,
    destination_table: str
) -> None:
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512<<10)
    csv.register_dialect(
        'TabDialect',
        quotechar='"',
        delimiter=input_field_delimiter,
        strict=True
    )
    with open(
        source_file
    ) as reader:
        data = []
        chunk_number = 1
        for index, line in enumerate(csv.reader(reader, 'TabDialect'), 0):
            data.append(line)
            if (index % int(chunksize) == 0 and index > 0):
                process_dataframe_chunk(
                    data=data,
                    pipeline_name=pipeline_name,
                    input_csv_headers=input_csv_headers,
                    data_dtypes=data_dtypes,
                    source_url=source_url,
                    target_file=target_file,
                    chunk_number=chunk_number,
                    reorder_headers_list=reorder_headers_list,
                    date_format_list=date_format_list,
                    null_rows_list=null_rows_list,
                    destination_table=destination_table
                )
                data = []
                chunk_number += 1

        if index % int(chunksize) != 0 and index > 0:
            process_dataframe_chunk(
                data=data,
                pipeline_name=pipeline_name,
                input_csv_headers=input_csv_headers,
                data_dtypes=data_dtypes,
                source_url=source_url,
                target_file=target_file,
                chunk_number=chunk_number,
                reorder_headers_list=reorder_headers_list,
                date_format_list=date_format_list,
                null_rows_list=null_rows_list,
                destination_table=destination_table
            )


def process_dataframe_chunk(
    data: typing.List[str],
    pipeline_name: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    source_url: str,
    target_file: str,
    chunk_number: int,
    reorder_headers_list: typing.List[str],
    date_format_list: typing.List[str],
    null_rows_list: typing.List[str],
    destination_table: str
) -> None:
    logging.info(f"Processing chunk #{chunk_number}")
    df = pd.DataFrame(
                data,
                columns=input_csv_headers
            )
    set_df_datatypes(df, data_dtypes)
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        source_url=source_url,
        target_file_batch=target_file_batch,
        target_file=target_file,
        skip_header=(not chunk_number == 1),
        pipeline_name=pipeline_name,
        reorder_headers_list=reorder_headers_list,
        date_format_list=date_format_list,
        null_rows_list=null_rows_list
    )


def set_df_datatypes(
    df: pd.DataFrame,
    data_dtypes: dict
) -> pd.DataFrame:
    logging.info("Setting data types")
    for key, item in data_dtypes.items():
        df[key] = df[key].astype(item)
    return df


def process_chunk(
    df: pd.DataFrame,
    source_url: str,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    pipeline_name: str,
    reorder_headers_list: dict,
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str]
) -> None:
    if pipeline_name == "GHCND by year":
        df = filter_null_rows(df, null_rows_list=null_rows_list)
        df = add_metadata_cols(df, source_url=source_url)
        df = source_convert_date_formats(df, date_format_list=date_format_list)
        df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def add_metadata_cols(
    df: pd.DataFrame,
    source_url: str
) -> pd.DataFrame:
    logging.info("Adding metadata columns")
    df["source_url"] = source_url
    df["etl_timestamp"] = pd.to_datetime( datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S", infer_datetime_format=True )
    return df

def reorder_headers(
    df: pd.DataFrame,
    reorder_headers_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Reordering headers..")
    return df[reorder_headers_list]


def gz_decompress(infile: str, tofile: str) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def filter_null_rows(df: pd.DataFrame, null_rows_list: typing.List[str]) -> pd.DataFrame:
    logging.info("Removing rows with blank id's..")
    for fld in null_rows_list:
        df = df[df[fld] != ""]
    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or dt_str == "nan":
        return str(dt_str)
    else:
        return str(
            datetime.datetime.strptime(str(dt_str), "%Y%m%d")
            .date()
            .strftime("%Y-%m-%d")
        )


def source_convert_date_formats(
    df: pd.DataFrame,
    date_format_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Converting Date Format..")
    for fld in date_format_list:
        df[fld] = df[fld].apply(convert_dt_format)
    return df


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
        schema_struct = json.loads(blob.download_as_bytes(client=None))
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


def download_file_ftp(
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    local_file: pathlib.Path,
    source_url: str,
) -> None:
    logging.info(f"Downloading {source_url} into {local_file}")
    ftp_conn = ftplib.FTP(ftp_host, timeout=60)
    ftp_conn.login("", "")
    ftp_conn.cwd(ftp_dir)
    ftp_conn.encoding = "utf-8"
    with open(local_file ,'wb') as dest_file:
        ftp_conn.retrbinary('RETR %s' % ftp_filename, dest_file.write)
    ftp_conn.quit()


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
        chunksize=os.environ.get("CHUNKSIZE", "100000"),
        ftp_host=os.environ.get("FTP_HOST", ""),
        ftp_dir=os.environ.get("FTP_DIR", ""),
        ftp_filename=os.environ.get("FTP_FILENAME", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        drop_dest_table=os.environ.get("DROP_DEST_TABLE", "N"),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        input_field_delimiter=os.environ.get("INPUT_FIELD_DELIMITER", "N"),
        full_data_load=os.environ.get("FULL_DATA_LOAD", "N"),
        start_year=os.environ.get("START_YEAR", ""),
        input_csv_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        output_csv_headers=json.loads(os.environ.get("OUTPUT_CSV_HEADERS", r"[]")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
        null_rows_list=json.loads(os.environ.get("NULL_ROWS_LIST", r"[]")),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"[]"))
    )
