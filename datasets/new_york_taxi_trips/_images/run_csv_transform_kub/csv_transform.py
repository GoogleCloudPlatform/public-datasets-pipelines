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

import json
import logging
import os
import pathlib
import typing
from datetime import datetime

import pandas as pd
import requests
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    pipeline_name: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:
    logging.info(f"New York taxi trips - {pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url,
        str(source_file),
        str(target_file),
        project_id,
        dataset_id,
        table_id,
        schema_path,
        chunksize,
        target_gcs_bucket,
        target_gcs_path,
        pipeline_name,
        input_headers,
        data_dtypes,
        output_headers,
    )
    logging.info(f"New York taxi trips - {pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_file: str,
    target_file: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    pipeline_name: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:
    for year_number in range(datetime.now().year, (datetime.now().year - 6), -1):
        target_file_name = str.replace(target_file, ".csv", f"_{year_number}.csv")
        process_year_data(
            source_url,
            int(year_number),
            source_file,
            target_file,
            target_file_name,
            project_id,
            dataset_id,
            table_id,
            schema_path,
            chunksize,
            target_gcs_bucket,
            target_gcs_path,
            pipeline_name,
            input_headers,
            data_dtypes,
            output_headers,
        )


def process_year_data(
    source_url: str,
    year_number: int,
    source_file: str,
    target_file: str,
    target_file_name: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    pipeline_name: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:
    logging.info(f"Processing year {year_number}")
    destination_table = f"{table_id}_{year_number}"
    year_data_available = False
    for month_number in range(1, 13):
        month_data_available = process_month(
            source_url,
            year_number,
            month_number,
            source_file,
            target_file,
            target_file_name,
            chunksize,
            input_headers,
            data_dtypes,
            output_headers,
            pipeline_name,
        )
        if month_data_available:
            year_data_available = True
        else:
            pass
    if os.path.exists(target_file_name) and year_data_available:
        upload_file_to_gcs(
            target_file_name,
            target_gcs_bucket,
            str(target_gcs_path).replace(".csv", f"_{year_number}.csv"),
        )
        create_dest_table(
            project_id, dataset_id, destination_table, schema_path, target_gcs_bucket
        )
        load_data_to_bq(project_id, dataset_id, destination_table, target_file_name)
    else:
        logging.info(
            f"Informational: The data file {target_file_name} was not generated because no data was available for year {year_number}.  Continuing."
        )
    logging.info(f"Processing year {year_number} completed")


def load_data_to_bq(
    project_id: str, dataset_id: str, table_id: str, file_path: str
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
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
    success = False
    try:
        table_exists_id = client.get_table(table_ref).table_id
        logging.info(f"Table {table_exists_id} currently exists.")
        success = True
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
        success = True
    return success


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


def process_month(
    source_url: str,
    year_number: int,
    month_number: int,
    source_file: str,
    target_file: str,
    target_file_name: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
    pipeline_name: str,
) -> None:
    process_month = str(year_number) + "-" + str(month_number).zfill(2)
    logging.info(f"Processing {process_month} started")
    source_url_to_process = f"{source_url}{process_month}.csv"
    source_file_to_process = str(source_file).replace(".csv", f"_{process_month}.csv")
    successful_download = download_file(source_url_to_process, source_file_to_process)
    if successful_download:
        with pd.read_csv(
            source_file_to_process,
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
                    f"Processing chunk #{chunk_number} of file {process_month} started"
                )
                target_file_batch = str(target_file).replace(
                    ".csv", f"-{process_month}-{chunk_number}.csv"
                )
                df = pd.DataFrame()
                df = pd.concat([df, chunk])
                process_chunk(
                    df,
                    target_file_batch,
                    target_file_name,
                    month_number == 1 and chunk_number == 0,
                    month_number == 1 and chunk_number == 0,
                    output_headers,
                    pipeline_name,
                )
                logging.info(
                    f"Processing chunk #{chunk_number} of file {process_month} completed"
                )
    logging.info(f"Processing {process_month} completed")
    return successful_download


def download_file(source_url: str, source_file: pathlib.Path) -> bool:
    logging.info(f"Downloading {source_url} into {source_file}")
    success = True
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)
    # if the file contains the string "<Code>NoSuchKey</Code>" then the url returned
    # that it could not locate the respective file
    if open(source_file, "rb").read().find(b"<Code>NoSuchKey</Code>") > -1:
        success = False
    if success:
        logging.info(f"Download {source_url} to {source_file} complete.")
    else:
        logging.info(
            f"Unable to download {source_url} to {source_file} at this time.  The URL may not exist."
        )
    return success


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    include_header: bool,
    truncate_file: bool,
    output_headers: typing.List[str],
    pipeline_name: str,
) -> None:
    if pipeline_name == "tlc_green_trips":
        df["distance_between_service"] = ""
        df["time_between_service"] = ""
    df = format_date_time(df, "pickup_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = format_date_time(df, "dropoff_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = remove_null_rows(df)
    df = df[output_headers]
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, include_header, truncate_file)
    logging.info(f"Processing Batch {target_file_batch} completed")


def remove_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Removing Null rows... ")
    df = df.dropna(axis=0, subset=["vendor_id"])
    return df


def format_date_time(
    df: pd.DataFrame, field_name: str, str_pf_time: str, dt_format: str
) -> pd.DataFrame:
    if str_pf_time == "strptime":
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from datetime to {dt_format}  "
        )
        df[field_name] = df[field_name].apply(lambda x: datetime.strptime(x, dt_format))
    else:
        logging.info(
            f"Transform: Formatting datetime for field {field_name} from {dt_format} to datetime "
        )
        df[field_name] = df[field_name].dt.strftime(dt_format)
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
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        schema_path=os.environ["SCHEMA_PATH"],
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        pipeline_name=os.environ["PIPELINE_NAME"],
        input_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        output_headers=json.loads(os.environ["OUTPUT_CSV_HEADERS"]),
    )
