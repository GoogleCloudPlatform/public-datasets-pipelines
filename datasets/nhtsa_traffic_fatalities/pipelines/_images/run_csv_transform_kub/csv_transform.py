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
import json
import logging
import os
import pathlib
import typing
import zipfile as zip
from datetime import date


import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    source_zipfile_extracted: str,
    source_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    start_year: str,
    end_year: str,
    drop_dest_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    input_csv_headers: typing.List[str],
    input_dtypes: dict,
    rename_mappings_list: dict
) -> None:
    logging.info(f"{pipeline_name} process started")
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    process_year = int(start_year)
    todays_date = date.today()
    current_year = todays_date.year
    # max_year = 2020
    max_year = int(end_year)
    for processing_year in range(process_year, max_year+1):
        # source_url = source_url.replace("<<YEAR>>", str(processing_year))
        source_url = build_source_url(source_url,processing_year)
        source_file = str.replace(str(source_file),".zip", f"_{processing_year}.zip")
        execute_pipeline(
            source_url=source_url,
            source_file=source_file,
            source_zipfile_extracted=source_zipfile_extracted,
            chunksize=chunksize,
            rename_mappings_list=rename_mappings_list,
            input_dtypes=input_dtypes,
            input_csv_headers=input_csv_headers,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            process_year=processing_year,
            drop_dest_table=drop_dest_table,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            schema_path=schema_path,
            pipeline_name=pipeline_name
        )
        logging.info(f"{pipeline_name}_{processing_year} process completed")


def build_source_url(
    source_url:str,
    process_year: int
)-> str:
    source_url ="https://www.nhtsa.gov/file-downloads/download?p=nhtsa/downloads/FARS/<<YEAR>>/National/FARS<<YEAR>>NationalCSV.zip"
    source_url_parts =source_url.split("<<YEAR>>")
    processing_year = str(process_year)
    Final_URL = source_url_parts[0]+processing_year+source_url_parts[1]+processing_year+source_url_parts[2]
    return Final_URL

def execute_pipeline(
    source_url: str,
    source_file: pathlib.Path,
    source_zipfile_extracted: str,
    chunksize: str,
    rename_mappings_list: dict,
    input_dtypes: dict,
    input_csv_headers: typing.List[str],
    project_id: str,
    dataset_id: str,
    destination_table: str,
    process_year: int,
    drop_dest_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    pipeline_name: str
) -> None:
    download_file(source_url, source_file)
    source_file_path = os.path.split(source_file)[0]
    source_file_unzip_dir = f"{source_file_path}/{process_year}"
    source_file_extracted = f"{source_file_unzip_dir}/{source_zipfile_extracted}"
    target_file = source_file_extracted.replace(".csv", "_output.csv")
    df = process_source_file(
        source_file=source_file,
        source_file_unzip_dir=source_file_unzip_dir,
        source_file_extracted=source_file_extracted,
        target_file=target_file,
        chunksize=chunksize,
        field_separator=",",
        rename_mappings_list=rename_mappings_list,
        input_dtypes=input_dtypes,
        input_csv_headers=input_csv_headers
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
        destination_table = (pipeline_name.split('-')[1]).lower()+f"_{process_year}"
        # f"destination_table_{process_year}"
        # eg. "accident_" & "2015" = "accident_2015"
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
    source_file_unzip_dir: str,
    source_file_extracted: str,
    target_file: str,
    chunksize: str,
    field_separator: str,
    rename_mappings_list: dict,
    input_dtypes: dict,
    input_csv_headers: typing.List[str]
) -> pd.DataFrame:
    unpack_file(source_file, source_file_unzip_dir, "zip")
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512<<10)
    csv.register_dialect(
        'TabDialect',
        quotechar='"',
        delimiter=field_separator,
        strict=True
    )
    with open(
        source_file_extracted, encoding="cp1252"
    ) as reader:
        data = []
        chunk_number = 1
        next(reader)
        for index, line in enumerate(csv.reader(reader, 'TabDialect'), 0):
            data.append(line)
            if (index % int(chunksize) == 0 and index > 0):
                process_dataframe_chunk(
                    data=data,
                    input_csv_headers=input_csv_headers,
                    input_dtypes=input_dtypes,
                    target_file=target_file,
                    chunk_number=chunk_number,
                    rename_mappings_list=rename_mappings_list
                )
                data = []
                chunk_number += 1
        if index % int(chunksize) != 0 and index > 0:
            process_dataframe_chunk(
                data=data,
                input_csv_headers=input_csv_headers,
                input_dtypes=input_dtypes,
                target_file=target_file,
                chunk_number=chunk_number,
                rename_mappings_list=rename_mappings_list
            )


def process_dataframe_chunk(
    data: typing.List[str],
    input_csv_headers: typing.List[str],
    input_dtypes: dict,
    target_file: str,
    chunk_number: int,
    rename_mappings_list: dict
) -> None:
    df = pd.DataFrame(
                data,
                columns=input_csv_headers
            )
    set_df_datatypes(df, input_dtypes)
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        target_file_batch=target_file_batch,
        target_file=target_file,
        skip_header=(not chunk_number == 1),
        rename_headers_list=rename_mappings_list
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
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    rename_headers_list: dict
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = rename_headers(df, rename_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch), sep="|")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def unpack_file(infile: str, dest_path: str, compression_type: str = "zip") -> None:
    if compression_type == "zip":
        logging.info(f"Unpacking {infile} to {dest_path}")
        zip_decompress(infile=infile, dest_path=dest_path)
    else:
        logging.info(
            f"{infile} ignored as it is not compressed or is of unknown compression"
        )


def zip_decompress(infile: str, dest_path: str) -> None:
    with zip.ZipFile(infile, mode="r") as zipf:
        zipf.extractall(dest_path)
        for fileame in os.listdir(dest_path):
            # file_ext = fileame.split('.')[1]
            # if file_ext == 'CSV':
            file_name, file_extension = os.path.splitext(fileame)
            os.rename(os.path.join(dest_path, fileame), os.path.join(dest_path, file_name.lower() + file_extension.lower()))


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


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Renaming headers..")
    df.rename(columns=rename_mappings, inplace=True)
    return df


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, float_format="%.0f", index=False, sep=sep)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


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
        source_url=os.environ["SOURCE_URL"],
        chunksize=os.environ["CHUNKSIZE"],
        source_zipfile_extracted=os.environ["SOURCE_ZIPFILE_EXTRACTED"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        # target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        destination_table=os.environ["TABLE_ID"],
        start_year=os.environ["START_YEAR"],
        end_year=os.environ["END_YEAR"],
        drop_dest_table=os.environ["DROP_DEST_TABLE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        schema_path=os.environ["SCHEMA_PATH"],
        input_dtypes=json.loads(os.environ["INPUT_DTYPES"]),
        input_csv_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        rename_mappings_list=json.loads(os.environ["RENAME_MAPPINGS_LIST"]),
    )
