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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from google.cloud import bigquery, storage
import json
import logging
import os
import pathlib
import pandas as pd
import re
import requests
import typing
import urllib


def main(
    pipeline_name: str,
    source_url: str,
    process_filegroup: str,
    zip_path: str,
    api_key: str,
    tables_list: typing.List[str],
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_file: str,
    project_id: str,
    dataset_id: str,
) -> None:

    logging.info(f"{pipeline_name} process started")
    pathlib.Path(f"{zip_path}").mkdir(parents=True, exist_ok=True)

    # Grab the list of tables for the respective data group
    # bq_table_list = list_bq_tables(project_id, dataset_id, r"rxnsat_([0-9]*)_([0-9]*)")
    if process_filegroup == "DOWNLOAD_ONLY":
        bq_table_list = list_bq_tables(project_id, dataset_id, r"([A-Za-z]*)_([0-9]*)_([0-9]*)$")
    else:
        bq_table_list = list_bq_tables(project_id, dataset_id, r"{process_filegroup}_([0-9]*)_([0-9]*)$")
    df_bq_tables_list = pd.DataFrame(bq_table_list, columns=["bq_table_name"])
    df_bq_tables_list["yyyymm"] = df_bq_tables_list.apply(
        lambda x: f"20{x['bq_table_name'][-2:]}-{x['bq_table_name'][-5:-3]}", axis=1
    )
    # Grab the max value for the load month-date.
    most_recent_load = df_bq_tables_list['yyyymm'].max()
    load_datetime = pd.to_datetime(f"{most_recent_load[-2:]}/01/{most_recent_load[0:4]} 00:00:00")
    # Add 1 month to obtain the next month-date for processing
    next_month_date = load_datetime + relativedelta(months=1)
    next_month_int = next_month_date.strftime("%Y%m")
    # next_month_file_date = next_month_date.strftime("_%m_%y")
    current_month_int = datetime.today().strftime("%Y%m")
    # while the month to process <= current month, process it
    while next_month_int <= current_month_int:
        if process_filegroup == "DOWNLOAD_ONLY":
            source_file_url = find_source_file(
                source_url = source_url,
                month_date = next_month_int,
                api_key=api_key
            )
            zip_file_name = os.path.basename(source_file_url).split('&apiKey')[0]
            download_file(source_url = source_file_url,
                          source_file = os.path.join(zip_path, zip_file_name))

            import pdb
            pdb.set_trace()

        # else:

        import pdb
        pdb.set_trace()
        # process_and_load()
        # Add 1 month to obtain the next month-date for processing
        next_month_date = load_datetime + relativedelta(months=1)
        next_month_int = int(next_month_date.strftime("%Y%m"))



    # bq_table_list['mmyyyy'] = bq_table_list.apply(lambda x: )
    # extract_month_year(list_tables)
    print(df_bq_tables_list)
    print("--------------------------")
    print(bq_table_list)

    import pdb

    pdb.set_trace()


    # for table in bq_table_list:
    #     [print(f"{key}  {val}") for key, val in table.items()]

    # download_file(source_url, source_file)

    # chunksz = int(chunksize)

    # with pd.read_csv(
    #     source_file, engine="python", encoding="utf-8", quotechar='"', chunksize=chunksz
    # ) as reader:
    #     for chunk_number, chunk in enumerate(reader):
    #         logging.info(f"Processing batch {chunk_number}")
    #         target_file_batch = str(target_file).replace(
    #             ".csv", "-" + str(chunk_number) + ".csv"
    #         )
    #         df = pd.DataFrame()
    #         df = pd.concat([df, chunk])
    #         process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    # upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("San Francisco - Film Locations process completed")


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
    job_config.skip_leading_rows = 1
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
    source_url: str,
    month_date: datetime, #yyyymm
    api_key: str
) -> str:
    file_date_str = f"{month_date[:4]}-{month_date[-2:]}-01"
    file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
    last_day_of_month = int(datetime.strftime((file_date + relativedelta(day=31)), "%d"))
    day_of_month_counter = 1
    file_found = False
    while day_of_month_counter <= last_day_of_month:
        # file_date = datetime.strptime(datetime.strptime(file_date_str, "%Y-%m-%d"), "%m%d%Y")
        file_date_mdy = datetime.strftime(file_date, "%m%d%Y")
        src_url = source_url.replace("~file_date~", file_date_mdy).replace("~api_key~", api_key)
        file_found = http_file_exists(src_url)
        if file_found:
            print(f"Source file found: {file_date}")
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
        tables_list=json.loads(os.environ.get("TABLES_LIST", r"[]")),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        schema_file=os.environ.get("SCHEMA_FILE", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
    )
