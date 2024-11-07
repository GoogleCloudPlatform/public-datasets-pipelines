# Copyright 2023 Google LLC
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
import re
import typing
import urllib
from datetime import datetime, timedelta
from zipfile import ZipFile

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url: str,
    process_filegroup: str,
    zip_path: str,
    api_key: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_filepath: str,
    project_id: str,
    dataset_id: str,
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path(f"{zip_path}").mkdir(parents=True, exist_ok=True)
    # Grab the list of tables for the respective data group
    if process_filegroup == "DOWNLOAD_ONLY":
        bq_table_list = list_bq_tables(
            project_id, dataset_id, r"([A-Za-z]*)_([0-9]*)_([0-9]*)$"
        )
    else:
        bq_table_list = list_bq_tables(
            project_id, dataset_id, rf"{process_filegroup}_([0-9]*)_([0-9]*)$"
        )
    df_bq_tables_list = pd.DataFrame(bq_table_list, columns=["bq_table_name"])
    df_bq_tables_list["yyyymm"] = df_bq_tables_list.apply(
        lambda x: f"20{x['bq_table_name'][-2:]}-{x['bq_table_name'][-5:-3]}", axis=1
    )
    # Grab the max value for the load month-date.
    most_recent_load = df_bq_tables_list["yyyymm"].max()
    load_datetime = pd.to_datetime(
        f"{most_recent_load[-2:]}/01/{most_recent_load[0:4]} 00:00:00"
    )
    # Add 1 month to obtain the next month-date for processing
    next_month_date = load_datetime + relativedelta(months=1)
    next_month_int = next_month_date.strftime("%Y%m")
    # next_month_file_date = next_month_date.strftime("_%m_%y")
    current_month_int = datetime.today().strftime("%Y%m")
    # while the month to process <= current month, process it
    while next_month_int <= current_month_int:
        if process_filegroup == "DOWNLOAD_ONLY":
            source_file_url = find_source_file(
                source_url=source_url, month_date=next_month_int, api_key=api_key
            )
            zip_file_name = os.path.basename(source_file_url).split("&apiKey")[0]
            zip_file_path = os.path.join(zip_path, zip_file_name)
            download_file(
                source_url=source_file_url,
                source_file=zip_file_path,
            )
            upload_file_to_gcs(
                file_path=zip_file_path,
                gcs_bucket=target_gcs_bucket,
                gcs_path=os.path.join(
                    target_gcs_path, process_filegroup, zip_file_name
                ),
            )
            logging.info(
                f"source_file_url : {source_file_url}  zip_file_path : {zip_file_path}"
            )
        else:
            file_prefix = os.path.basename(source_url).split("~file_date~")[0]
            load_process_filegroup_data(
                process_filegroup=process_filegroup,
                file_prefix=file_prefix,
                zip_path=zip_path,
                month_to_load=next_month_int,
                project_id=project_id,
                dataset_id=dataset_id,
                target_gcs_bucket=target_gcs_bucket,
                target_gcs_path=os.path.join(target_gcs_path, "DOWNLOAD_ONLY"),
                schema_filepath=schema_filepath,
            )
        # Add 1 month to obtain the next month-date for processing
        next_month_date = next_month_date + relativedelta(months=1)
        next_month_int = next_month_date.strftime("%Y%m")
    logging.info(f"{pipeline_name} process completed")


def load_process_filegroup_data(
    process_filegroup: str,
    file_prefix: str,
    zip_path: str,
    month_to_load: str,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_filepath: str,
) -> None:
    logging.info(
        f"Loading filegroup data for {process_filegroup} for month {month_to_load}"
    )
    #  Walk tree in source folder for zipfiles begining date of month after
    #  the most recent load of the process_filegroup data.
    month = month_to_load[-2:]
    year = month_to_load[:4]
    re_file_search = rf"{file_prefix[:-1]}_{month}([0-9][0-9]){year}.zip"
    zip_file_list = fetch_gcs_file_names(
        gcs_bucket=target_gcs_bucket,
        gcs_path=target_gcs_path,
        regex_file_expr=re_file_search,
    )
    zip_file = zip_file_list[0] if zip_file_list else ""
    if zip_file != "":
        if fetch_gcs_file_names(target_gcs_bucket, zip_file):
            source_location_gcs = os.path.join("gs://", target_gcs_bucket, zip_file)
            download_file_gcs(
                project_id=project_id,
                source_location=source_location_gcs,
                destination_folder=zip_path,
            )
            # load the data file
            logging.info(
                f"zip file {os.path.join(zip_path, zip_file)} exists.  Loading..."
            )
            table_id = f"{process_filegroup}_{month}_{year[-2:]}"
            load_source_data(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                process_filegroup=process_filegroup,
                schema_filepath=schema_filepath,
                target_file=os.path.join(zip_path, os.path.basename(zip_file)),
                target_gcs_bucket=target_gcs_bucket,
            )
        else:
            raise (
                f"File gs://{target_gcs_bucket}/{zip_file} does not exist.  Cannot continue."
            )
    else:
        # zip file does not exist
        logging.info(
            f"zip file does not exist for the given month {month_to_load} in path {zip_path}."
        )


def fetch_gcs_file_names(
    gcs_bucket: str, gcs_path: str, regex_file_expr: str = ""
) -> typing.List[str]:
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=gcs_path)
    source_file_names = []
    for blob in blobs:
        path = os.path.dirname(blob.name)
        filename = os.path.basename(blob.name)
        if regex_file_expr == "":
            source_file_names.append(blob.name)
        else:
            re_filter = re.compile(rf"{regex_file_expr}")
            if re_filter.match(filename):
                source_file_names.append(os.path.join(path, filename))
    return source_file_names


def download_file_gcs(
    project_id: str,
    source_location: str,
    destination_folder: str,
    filename_override: str = "",
) -> None:
    object_name = os.path.basename(source_location)
    if filename_override == "":
        dest_object = f"{destination_folder}/{object_name}"
    else:
        dest_object = f"{destination_folder}/{filename_override}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def load_source_data(
    project_id: str,
    dataset_id: str,
    table_id: str,
    process_filegroup: str,
    schema_filepath: str,
    target_file: str,
    target_gcs_bucket: str,
) -> None:
    if process_filegroup == "rxncuichange":
        member_path = "rrf/RXNCUICHANGES.RRF"
    else:
        member_path = f"rrf/{str.upper(process_filegroup)}.RRF"
    with ZipFile(target_file, "r") as zip_file:
        zip_file.extract(member=member_path, path=os.path.dirname(target_file))
    extracted_member_path = os.path.join(os.path.dirname(target_file), member_path)
    if os.path.isfile(extracted_member_path):
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            schema_filepath=f"{schema_filepath}/{str.lower(process_filegroup)}_schema.json",
            bucket_name=target_gcs_bucket,
        )
        if table_exists:
            # extract the source data file from the source zip file
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                file_path=extracted_member_path,
                truncate_table=True,
                skip_leading_rows=0,
                field_delimiter="|",
                ignore_unknown_values=True,
            )
        os.unlink(extracted_member_path)
    else:
        logging.info(
            f"Warning: Source file {extracted_member_path} does not exist.  Skipping."
        )


def list_bq_tables(
    project_id: str, dataset_id: str, regex_filter: str = ""
) -> typing.List[str]:
    client = bigquery.Client(project=project_id)
    tables = client.list_tables(dataset_id)
    table_list = []
    for table in tables:
        if regex_filter == "":
            table_list += [table.table_id]
        else:
            re_filter = re.compile(regex_filter)
            if re_filter.match(table.table_id):
                table_list += [table.table_id]
    return table_list


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_filepath: str,
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
                f"Table {table_ref} currently does not exist.  Attempting to create table from filepath {schema_filepath}."
            )
        )
        file_name = os.path.split(schema_filepath)[1]
        file_path = os.path.split(schema_filepath)[0]
        if check_gcs_file_exists(schema_filepath, bucket_name):
            schema = create_table_schema([], bucket_name, schema_filepath)
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)
            logging.info(f"Table {table_ref} was created".format(table_id))
            table_exists = True
        else:
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


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
    skip_leading_rows: int = 0,
    field_delimiter: str = "|",
    ignore_unknown_values: bool = False,
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
    if skip_leading_rows > 0:
        job_config.skip_leading_rows = skip_leading_rows
    job_config.ignore_unknown_values = ignore_unknown_values
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} completed"
    )


def table_exists(project_id: str, dataset_id: str, table_name: str) -> bool:
    client = bigquery.Client(project=project_id)
    tables = client.list_tables(dataset_id)
    found_table = False
    for tbl in tables:
        if tbl.table_id == table_name:
            found_table = True
    return found_table


def find_source_file(
    source_url: str, month_date: datetime, api_key: str  # yyyymm
) -> str:
    file_date_str = f"{month_date[:4]}-{month_date[-2:]}-01"
    file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
    last_day_of_month = int(
        datetime.strftime((file_date + relativedelta(day=31)), "%d")
    )
    day_of_month_counter = 1
    file_found = False
    while day_of_month_counter <= last_day_of_month:
        # file_date = datetime.strptime(datetime.strptime(file_date_str, "%Y-%m-%d"), "%m%d%Y")
        file_date_mdy = datetime.strftime(file_date, "%m%d%Y")
        src_url = source_url.replace("~file_date~", file_date_mdy).replace(
            "~api_key~", api_key
        )
        file_found = http_file_exists(src_url)
        if file_found:
            logging.info(f"Source file found: {file_date}")
            return src_url
        else:
            file_date = file_date + timedelta(days=1)
    return ""


def http_file_exists(source_url: str) -> bool:
    req = urllib.request.Request(source_url, method="HEAD")
    file = urllib.request.urlopen(req)
    response_type = file.headers["Content-Type"]
    if response_type == "text/html; charset=iso-8859-1":
        return False
    else:
        return True


def download_file(
    source_url: str, source_file: pathlib.Path, continue_on_error: bool = False
) -> bool:
    logging.info(f"Downloading source file to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        rtn_status_code = src_file.status_code
        if 400 <= rtn_status_code <= 499:
            logging.info(
                f"Unable to download file source file (error code was {rtn_status_code})"
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
            logging.info(f"{err_msg} Unable to obtain source_file from url")
            raise SystemExit(e)
        else:
            logging.info(
                f"{err_msg} Unable to obtain source_file from url.  Continuing."
            )
        return False


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if skip_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
        )
        next(data_file)
    else:
        logging.info(f"Appending batch file {batch_file_path} to {target_file_path}")
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=os.environ.get("SOURCE_URL", ""),
        process_filegroup=os.environ.get("PROCESS_FILEGROUP", ""),
        zip_path=os.environ.get("ZIP_PATH", ""),
        api_key=os.environ.get("API_KEY", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
    )
