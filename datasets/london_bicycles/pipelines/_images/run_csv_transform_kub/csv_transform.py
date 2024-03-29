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
import json
import logging
import os
import pathlib
import re
import typing
from xml.etree import ElementTree

import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_url: dict,
    source_file: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    load_start_date_floor: str,
    required_cols: typing.List[str],
    rename_mappings: dict,
    date_cols: typing.List[str],
    integer_cols: typing.List[str],
    float_cols: typing.List[str],
    string_cols: typing.List[str],
    output_file: str,
    data_dtypes: dict,
    output_csv_headers: typing.List[str],
    gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    # page_refresh_dummy_element: str,
    pipeline: str,
) -> None:
    logging.info(
        f'{pipeline} pipeline process started at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )
    source_folder = os.path.split(source_file)[0]
    pathlib.Path(source_folder).mkdir(parents=True, exist_ok=True)
    if pipeline == "London Cycle Stations Dataset":
        process_cycle_stations(
            source_url=source_url,
            source_file=source_file,
            source_folder=source_folder,
            required_cols=required_cols,
            rename_mappings=rename_mappings,
            date_cols=date_cols,
            integer_cols=integer_cols,
            float_cols=float_cols,
            string_cols=string_cols,
            output_file=output_file,
            gcs_bucket=gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
    elif pipeline == "London Cycle Trips Dataset":
        process_cycle_hire(
            source_url=source_url,
            source_file=source_file,
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            load_start_date_floor=load_start_date_floor,
            rename_mappings=rename_mappings,
            output_file=output_file,
            data_dtypes=data_dtypes,
            output_csv_headers=output_csv_headers,
            gcs_bucket=gcs_bucket,
            schema_path=schema_path,
        )
    logging.info(
        f'{pipeline} pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


def process_cycle_hire(
    source_url: dict,
    source_file: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    load_start_date_floor: str,
    rename_mappings: dict,
    output_file: str,
    data_dtypes: dict,
    output_csv_headers: typing.List[str],
    gcs_bucket: str,
    schema_path: str,
):
    files_list = list_files_in_gcs_bucket(
        source_gcs_bucket=source_url["trips"].replace("gs://", ""), source_gcs_path=""
    )
    extract_list = [s for s in files_list if "JourneyDataExtract" in s]
    df_extract_list = pd.DataFrame(extract_list, columns=["source_file_name"])
    df_extract_list["id"] = df_extract_list["source_file_name"].apply(
        lambda x: os.path.basename(str(x)).split("JourneyDataExtract")[0]
    )
    df_extract_list["date_from_extr"] = df_extract_list["source_file_name"].apply(
        lambda x: int(
            clean_date(
                os.path.basename(str(x))
                .split("JourneyDataExtract")[1]
                .replace(".csv", "")
                .replace(".xlsx", "")
                .split("-")[0]
            )
        )
    )
    df_extract_list["date_to_extr"] = df_extract_list["source_file_name"].apply(
        lambda x: int(
            clean_date(
                os.path.basename(str(x))
                .split("JourneyDataExtract")[1]
                .replace(".csv", "")
                .replace(".xlsx", "")
                .split("-")[1]
            )
        )
    )
    df_extract_list = df_extract_list.sort_values(by=["date_to_extr"], ascending=True)
    df_extract_list = df_extract_list.loc[
        (df_extract_list["date_from_extr"] > int(load_start_date_floor))
    ]
    df_extract_list["bq_start_date_from"] = df_extract_list["date_from_extr"].apply(
        lambda x: f"{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}"
    )
    df_extract_list["bq_start_date_to"] = df_extract_list["date_to_extr"].apply(
        lambda x: f"{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}"
    )
    for download_file_name in df_extract_list["source_file_name"]:
        bq_start_date_from = str(
            df_extract_list.loc[
                (df_extract_list["source_file_name"] == download_file_name)
            ]["bq_start_date_from"]
        ).split("    ")[1][0:10]
        bq_start_date_to = str(
            df_extract_list.loc[
                (df_extract_list["source_file_name"] == download_file_name)
            ]["bq_start_date_to"]
        ).split("    ")[1][0:10]
        number_rows = count_number_rows_between_date(
            project_id=project_id,
            dataset_id=dataset_id,
            table_name=table_id,
            start_date_from=bq_start_date_from,
            start_date_to=bq_start_date_to,
        )
        if number_rows == -1:
            create_dest_table(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                schema_filepath=schema_path,
                bucket_name=gcs_bucket,
            )
            number_rows = 0
        if number_rows == 0:
            source_location = f"{source_url['trips']}/{download_file_name}"
            destination_folder = os.path.dirname(source_file)
            destination_filename = (
                f"{destination_folder}/{os.path.basename(download_file_name)}"
            )
            download_file_gcs(
                project_id=project_id,
                source_location=source_location,
                destination_folder=destination_folder,
            )
            df_journey = pd.read_csv(
                destination_filename, sep=",", quotechar='"', dtype=data_dtypes
            )
            df_journey = rename_headers(df_journey, rename_mappings)
            df_journey["duration_str"] = df_journey["duration_str"].astype(
                "Int32", errors="ignore"
            )
            df_journey["bike_id"] = df_journey["bike_id"].astype(
                "Int32", errors="ignore"
            )
            df_journey["start_station_id"] = df_journey["start_station_id"].astype(
                "Int32", errors="ignore"
            )
            if "end_station_id" not in df_journey.columns:
                df_journey["end_station_id"] = ""
            else:
                pass
            df_journey["end_station_id"] = df_journey["end_station_id"].astype(
                "Int32", errors="ignore"
            )
            if "duration_ms" in df_journey.columns:
                df_journey["duration_str"] = df_journey["duration_ms"].apply(
                    lambda x: x if pd.isnull(x) else round(x / 1000)
                )
            else:
                df_journey["duration_ms"] = df_journey["duration_str"].apply(
                    lambda x: x if pd.isnull(x) else round(x * 1000)
                )
            if "bike_model" not in df_journey.columns:
                df_journey["bike_model"] = ""
            else:
                pass
            df_journey["start_date"] = df_journey["start_date"].apply(
                lambda x: x if len(str(x)) < 1 else f"{x}:00"
            )
            df_journey["start_date"] = df_journey["start_date"].apply(
                lambda x: fix_date(x)
            )
            df_journey["end_date"] = df_journey["end_date"].apply(
                lambda x: x if len(str(x)) < 1 else f"{x}:00"
            )
            df_journey["end_date"] = df_journey["end_date"].apply(lambda x: fix_date(x))
            df_journey["rental_id"] = df_journey["rental_id"].apply(
                lambda x: re.sub(r"\W+", "", str(x))
            )
            df_journey["duration_str"] = df_journey["duration_str"].apply(
                lambda x: re.sub(r"\W+", "", str(x))
            )
            df_journey["duration_ms"] = df_journey["duration_ms"].apply(
                lambda x: re.sub(r"\W+", "", str(x))
            )
            df_journey["bike_id"] = df_journey["bike_id"].apply(
                lambda x: re.sub(r"\W+", "", str(x))
            )
            df_journey["start_station_id"] = df_journey["start_station_id"].apply(
                lambda x: re.sub(r"\W+", "", str(x))
            )
            df_journey["end_station_id"] = df_journey["end_station_id"].apply(
                lambda x: re.sub(r"\W+", "", str(x))
            )
            df_journey["end_station_logical_terminal"] = ""
            df_journey["start_station_logical_terminal"] = ""
            df_journey["end_station_priority_id"] = ""
            df_journey.rename(columns={"duration_str": "duration"}, inplace=True)
            df_journey[output_csv_headers].to_csv(
                output_file, sep="|", quotechar='"', index=False
            )
            if os.path.exists(output_file):
                load_data_to_bq(
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=table_id,
                    file_path=output_file,
                    truncate_table=False,
                    field_delimiter="|",
                )
                os.unlink(destination_filename)
                os.unlink(output_file)
            else:
                logging.info(
                    f"Informational: The data file {output_file} was not generated because no data file was available.  Continuing."
                )
        else:
            logging.info(f"Datafile {download_file_name} already loaded.  Skipping.")


def fix_date(dt_val: str) -> str:
    if dt_val == "nan:00":
        rtn_val = ""
    elif dt_val.find("/") == -1:
        rtn_val = dt_val
    else:
        rtn_val = datetime.datetime.strptime(dt_val, "%d/%m/%Y %H:%M:%S").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    # import pdb; pdb.set_trace()
    return rtn_val


def process_cycle_stations(
    source_url: dict,
    source_file: str,
    source_folder: str,
    required_cols: typing.List[str],
    rename_mappings: dict,
    date_cols: typing.List[str],
    integer_cols: typing.List[str],
    float_cols: typing.List[str],
    string_cols: typing.List[str],
    output_file: str,
    gcs_bucket: str,
    target_gcs_path: str,
):
    for src_url in source_url:
        src_file_name = os.path.basename(source_url[src_url])
        dest_file = f"{source_folder}/{src_file_name}"
        download_file(source_url[src_url], dest_file)
        process_xml(
            source_file,
            output_file,
            required_cols,
            rename_mappings,
            date_cols,
            integer_cols,
            float_cols,
            string_cols,
        )
        upload_file_to_gcs(output_file, gcs_bucket, target_gcs_path)


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


def field_exists(
    project_id: str, dataset_id: str, table_name: str, field_name: str
) -> bool:
    if table_exists(project_id, dataset_id, table_name):
        client = bigquery.Client(project=project_id)
        table_ref = f"{dataset_id}.{table_name}"
        tbl_schema = client.get_table(table_ref).schema
        found_field = False
        for field in tbl_schema:
            if field.name == field_name:
                found_field = True
        return found_field
    else:
        return False


def count_number_rows_between_date(
    project_id: str,
    dataset_id: str,
    table_name: str,
    start_date_from: str,
    start_date_to: str,
) -> int:
    check_field_exists = field_exists(project_id, dataset_id, table_name, "start_date")
    if check_field_exists:
        client = bigquery.Client(project=project_id)
        query = f"""
            SELECT count(1) AS number_of_rows
            FROM {dataset_id}.{table_name}
            WHERE start_date between '{start_date_from}' and '{start_date_to}'
        """
        job_config = bigquery.QueryJobConfig()
        query_job = client.query(query, job_config=job_config)
        for row in query_job.result():
            count_rows = row.number_of_rows
        return int(count_rows)
    else:
        return -1


def download_file_gcs(
    project_id: str, source_location: str, destination_folder: str
) -> None:
    logging.info(f"Downloading file {source_location} to folder {destination_folder}")
    object_name = os.path.basename(source_location)
    dest_object = f"{destination_folder}/{object_name}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def list_files_in_gcs_bucket(source_gcs_bucket: str, source_gcs_path: str) -> list:
    client = storage.Client()
    bucket = client.get_bucket(source_gcs_bucket)
    files = bucket.list_blobs(prefix=source_gcs_path)
    file_list = []
    for file in files:
        file = str(file.name).replace(source_gcs_path, "")
        file_list.append(file)
    return file_list


def clean_date(datestr: str) -> str:
    datestr = datestr.strip()
    if len(datestr) < 9:
        datestr = f"{datestr[:-2]}20{datestr[-2:]}"
    if datestr[:-4][-3].isnumeric:
        if datestr[:-4][-2:] == "Fe":
            datestr = f"{datestr[:-6]}Feb{datestr[-4:]}"
    if len(datestr) == 9:
        datestr = datetime.datetime.strptime(datestr, "%d%b%Y").strftime("%Y%m%d")
    else:
        datestr = datetime.datetime.strptime(datestr, "%d%B%Y").strftime("%Y%m%d")
    return datestr


def download_file(source_url: str, source_file: str) -> None:
    logging.info(f"Downloading data from {source_url} to {source_file} .")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
    else:
        logging.info(f"Couldn't download {source_url}: {res.text}")
    logging.info(f"Downloaded data from {source_url} into {source_file}")


def get_data_dict(
    row_tag: ElementTree.Element,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
) -> dict:
    row_data = {}
    for col in row_tag:
        if col.tag in date_cols:
            row_data[col.tag] = parse_date(col.text)
        elif col.tag in integer_cols:
            row_data[col.tag] = int(col.text)
        elif col.tag in float_cols:
            row_data[col.tag] = float(col.text)
        elif col.tag in string_cols:
            row_data[col.tag] = col.text
    return row_data


def parse_date(date: str) -> datetime.datetime.date:
    if not date:
        return None
    date = datetime.datetime.fromtimestamp(int(date) / 1000)
    return date.date()


def process_xml(
    source_file: str,
    output_file: str,
    required_cols: list,
    rename_mappings: dict,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
) -> None:
    logging.info("Process started for converting .xml to .csv")
    xml_data = ElementTree.parse(source_file)
    root_tag = xml_data.getroot()
    row_tags = list(root_tag)
    logging.info(f"Opening {output_file} in 'w'(write) mode")
    with open(output_file, mode="w") as fb:
        logging.info(
            f"Creating csv writer(DictWriter) object with fieldnames={required_cols}"
        )
        writer = csv.DictWriter(fb, fieldnames=required_cols)
        logging.info(
            f"Writing headers(Renamed Headers) {rename_mappings} to {output_file}"
        )
        writer.writerow(rename_mappings)
        logging.info(f"Reading all xml tags and writing to {output_file}")
        for idx, row_tag in enumerate(row_tags, start=1):
            if not (idx % 100):
                logging.info(
                    f"\t{idx} rows of data cleaned and writing/appending to {output_file}"
                )
            row_entry = get_data_dict(
                row_tag, date_cols, integer_cols, float_cols, string_cols
            )
            writer.writerow(row_entry)
        logging.info(
            f"\t{idx} rows of data cleaned and writing/appending to {output_file}"
        )
    logging.info("Process completed for converting .xml to .csv")


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    return df.rename(columns=rename_headers_list)


def upload_file_to_gcs(
    target_csv_file: str, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_csv_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_url=json.loads(os.environ.get("SOURCE_URL", "")),
        source_file=os.environ.get("SOURCE_FILE", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        load_start_date_floor=os.environ.get("LOAD_START_DATE_FLOOR", ""),
        required_cols=json.loads(os.environ.get("REQUIRED_COLS", "[]")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS", "{}")),
        output_file=os.environ.get("OUTPUT_FILE", ""),
        date_cols=json.loads(os.environ.get("DATE_COLS", "[]")),
        integer_cols=json.loads(os.environ.get("INTEGER_COLS", "[]")),
        float_cols=json.loads(os.environ.get("FLOAT_COLS", "[]")),
        string_cols=json.loads(os.environ.get("STRING_COLS", "[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", "{}")),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        output_csv_headers=json.loads(os.environ.get("OUTPUT_CSV_HEADERS", "[]")),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        pipeline=os.environ.get("PIPELINE", ""),
    )
