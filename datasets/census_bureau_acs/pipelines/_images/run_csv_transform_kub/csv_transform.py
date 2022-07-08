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
import sys
import typing

import numpy as np
import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    pipeline_name: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    year_report: str,
    api_naming_convention: str,
    geography: str,
    report_level: str,
    concat_col_list: typing.List[str],
    data_dtypes: str,
    rename_mappings_list: dict,
    input_csv_headers: typing.List[str],
    output_csv_headers: typing.List[str],
) -> None:
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    logging.info(f"{pipeline_name} process started")
    execute_pipeline(
        source_file=source_file,
        chunksize=chunksize,
        report_level=report_level,
        year_report=year_report,
        api_naming_convention=api_naming_convention,
        source_url=source_url,
        data_dtypes=data_dtypes,
        rename_mappings_list=rename_mappings_list,
        geography=geography,
        concat_col_list=concat_col_list,
        input_csv_headers=input_csv_headers,
        output_csv_headers=output_csv_headers,
        target_file=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        schema_path=schema_path,
    )
    logging.info(f"{pipeline_name} --> ETL process completed")


def execute_pipeline(
    source_file: str,
    chunksize: str,
    report_level: str,
    year_report: str,
    api_naming_convention: str,
    source_url: str,
    data_dtypes: dict,
    rename_mappings_list: dict,
    geography: str,
    concat_col_list: typing.List[str],
    input_csv_headers: typing.List[str],
    output_csv_headers: typing.List[str],
    target_file: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_path: str,
) -> None:
    json_obj_group_id = open("group_ids.json")
    group_id = json.load(json_obj_group_id)
    json_obj_state_code = open("state_codes.json")
    state_code = json.load(json_obj_state_code)
    logging.info("Extracting the data from API and loading into dataframe...")
    if report_level == "national_level":
        df = extract_data_and_convert_to_df_national_level(
            group_id, year_report, api_naming_convention, source_url, destination_table
        )
    elif report_level == "state_level":
        df = extract_data_and_convert_to_df_state_level(
            group_id,
            state_code,
            year_report,
            api_naming_convention,
            source_url,
            destination_table,
        )
    save_to_new_file(df, source_file, sep=",")
    process_source_file(
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        input_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        geography=geography,
        rename_mappings_list=rename_mappings_list,
        concat_col_list=concat_col_list,
        input_csv_headers=input_csv_headers,
        output_csv_headers=output_csv_headers,
        group_id=group_id,
        state_code=state_code,
    )
    if os.path.exists(target_file):
        upload_file_to_gcs(
            file_path=target_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            project_id=project_id,
        )
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
            drop_table="N",
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
    input_headers: str,
    data_dtypes: dict,
    geography: str,
    rename_mappings_list: dict,
    concat_col_list: typing.List[str],
    input_csv_headers: typing.List[str],
    output_csv_headers: typing.List[str],
    group_id: str,
    state_code: str,
) -> None:
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512 << 10)
    csv.register_dialect("TabDialect", quotechar='"', delimiter=",", strict=True)
    with open(source_file) as reader:
        data = []
        chunk_number = 1
        for index, line in enumerate(csv.reader(reader, "TabDialect"), 0):
            data.append(line)
            if index % int(chunksize) == 0 and index > 0:
                process_dataframe_chunk(
                    data=data,
                    input_headers=input_headers,
                    target_file=target_file,
                    chunk_number=chunk_number,
                    data_dtypes=data_dtypes,
                    geography=geography,
                    rename_mappings_list=rename_mappings_list,
                    concat_col_list=concat_col_list,
                    input_csv_headers=input_csv_headers,
                    output_csv_headers=output_csv_headers,
                    group_id=group_id,
                    state_code=state_code,
                )
                data = []
                chunk_number += 1
        if index % int(chunksize) != 0 and index > 0:
            process_dataframe_chunk(
                data=data,
                input_headers=input_headers,
                target_file=target_file,
                chunk_number=chunk_number,
                data_dtypes=data_dtypes,
                geography=geography,
                rename_mappings_list=rename_mappings_list,
                concat_col_list=concat_col_list,
                input_csv_headers=input_csv_headers,
                output_csv_headers=output_csv_headers,
                group_id=group_id,
                state_code=state_code,
            )
    dfcolumns = list(target_df.columns)
    i = 0
    while i < (len(output_csv_headers)):
        if output_csv_headers[i] not in dfcolumns:
            output_csv_headers.pop(i)
            i -= 1
        i += 1
    logging.info("Reordering headers...")
    final_df = target_df[output_csv_headers]
    save_to_new_file(final_df, target_file, sep="|")
    print("final df -->")
    print(final_df)
    print("Opening final file  -->")
    print(pd.read_csv(target_file, sep="|"))


def process_dataframe_chunk(
    data: typing.List[str],
    input_headers: typing.List[str],
    target_file: str,
    chunk_number: int,
    data_dtypes: dict,
    geography: str,
    rename_mappings_list: dict,
    concat_col_list: typing.List[str],
    input_csv_headers: typing.List[str],
    output_csv_headers: typing.List[str],
    group_id: str,
    state_code: str,
) -> None:
    df = pd.DataFrame(data, columns=input_headers)
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        chunk_number=chunk_number,
        target_file_batch=target_file_batch,
        target_file=target_file,
        skip_header=0,
        geography=geography,
        rename_mappings_list=rename_mappings_list,
        concat_col_list=concat_col_list,
        input_csv_headers=input_csv_headers,
        output_csv_headers=output_csv_headers,
        group_id=group_id,
        state_code=state_code,
    )


def set_df_datatypes(df: pd.DataFrame, data_dtypes: dict) -> pd.DataFrame:
    logging.info("Setting data types")
    for key, item in data_dtypes.items():
        df[key] = df[key].astype(item)
    return df


def process_chunk(
    df: pd.DataFrame,
    chunk_number: int,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    geography: str,
    rename_mappings_list: dict,
    concat_col_list: typing.List[str],
    input_csv_headers: typing.List[str],
    output_csv_headers: typing.List[str],
    group_id: str,
    state_code: str,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    logging.info("Replacing values...")
    df = df.replace(to_replace={"KPI_Name": group_id})
    rename_headers(df, rename_mappings_list)
    if geography == "censustract" or geography == "blockgroup":
        df["tract"] = df["tract"].apply(pad_zeroes_to_the_left, args=(6,))
        df["state"] = df["state"].apply(pad_zeroes_to_the_left, args=(2,))
        df["county"] = df["county"].apply(pad_zeroes_to_the_left, args=(3,))
    df = create_geo_id(df, concat_col_list)
    df = pivot_dataframe(df)
    save_to_new_file(df, file_path=str(target_file_batch), sep="|")
    df = append_batch_file(
        df, chunk_number, target_file_batch, target_file, skip_header, not (skip_header)
    )
    logging.info(f"Processing batch file {target_file_batch} completed")


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
    schema_structure: list,
    bucket_name: str = "",
    schema_filepath: str = "",
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
    i = 0
    dfcolumns = list(target_df.columns)
    while i < len(schema_struct):
        if schema_struct[i].get("name") not in dfcolumns:
            schema_struct.pop(i)
            i -= 1
        i += 1
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


def pivot_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Pivoting the dataframe...")
    df = df[["geo_id", "KPI_Name", "KPI_Value"]]
    df = df.pivot_table(
        index="geo_id", columns="KPI_Name", values="KPI_Value", aggfunc=np.sum
    ).reset_index()
    return df


def string_replace(source_url, replace: dict) -> str:
    for k, v in replace.items():
        source_url_new = source_url.replace(k, v)
    return source_url_new


def extract_data_and_convert_to_df_national_level(
    group_id: dict,
    year_report: str,
    api_naming_convention: str,
    source_url: str,
    destination_table: str,
) -> pd.DataFrame:
    list_temp = []
    flag = 0
    for key in group_id:
        logging.info(f"reading data from API for KPI {key}...")
        str1 = source_url.replace("~year_report~", year_report)
        str2 = str1.replace("~group_id~", key[0:-3])
        str3 = str2.replace("~row_position~", key[-3:])
        source_url_new = str3.replace("~api_naming_convention~", api_naming_convention)
        try:
            r = requests.get(source_url_new, stream=True, verify=False, timeout=200)
            if r.status_code == 200:
                logging.info("Data source valid for at least one entity")
                flag = 1
                text = r.json()
                frame = load_nested_list_into_df_without_headers(text)
                frame["KPI_Name"] = key
                list_temp.append(frame)
            elif 400 >= r.status_code <= 499:
                logging.info(r.status_code)
            else:
                logging.info(f"Source url : {source_url_new}")
                logging.info(f"status code : {r.status_code}")
        except OSError as e:
            logging.info(f"error : {e}")
    if flag == 0:
        logging.info(f"Data not available for {destination_table} yet")
        sys.exit(0)
    logging.info("creating the dataframe...")
    df = pd.concat(list_temp)
    return df


def load_nested_list_into_df_without_headers(text: typing.List) -> pd.DataFrame:
    frame = pd.DataFrame(text)
    frame = frame.iloc[1:, :]
    return frame


def extract_data_and_convert_to_df_state_level(
    group_id: dict,
    state_code: dict,
    year_report: str,
    api_naming_convention: str,
    source_url: str,
    destination_table: str,
) -> pd.DataFrame:
    list_temp = []
    flag = 0
    for key in group_id:
        for sc in state_code:
            logging.info(f"reading data from API for KPI {key}...")
            logging.info(f"reading data from API for KPI {sc}...")
            str1 = source_url.replace("~year_report~", year_report)
            str2 = str1.replace("~group_id~", key[0:-3])
            str3 = str2.replace("~row_position~", key[-3:])
            str4 = str3.replace("~api_naming_convention~", api_naming_convention)
            source_url_new = str4.replace("~state_code~", sc)
            try:
                r = requests.get(source_url_new, stream=True, verify=False, timeout=200)
                if r.status_code == 200:
                    logging.info("Data source valid for at least one entity")
                    flag = 1
                    text = r.json()
                    frame = load_nested_list_into_df_without_headers(text)
                    frame["KPI_Name"] = key
                    list_temp.append(frame)
                elif 400 >= r.status_code <= 499:
                    logging.info(r.status_code)
                else:
                    logging.info(f"Source url : {source_url_new}")
                    logging.info(f"status code : {r.status_code}")

            except OSError as e:
                logging.info(f"error : {e}")
    if flag == 0:
        logging.info(f"Data not available for {destination_table} yet")
        sys.exit(0)
    logging.info("creating the dataframe...")
    df = pd.concat(list_temp)
    return df


def create_geo_id(df: pd.DataFrame, concat_col: str) -> pd.DataFrame:
    logging.info("Creating column geo_id...")
    df = df.drop(0, axis=0)
    df["geo_id"] = ""
    for col in concat_col:
        df["geo_id"] = df["geo_id"] + df[col]
    return df


def pad_zeroes_to_the_left(val: str, length: int) -> str:
    if len(str(val)) < length:
        return ("0" * (length - len(str(val)))) + str(val)
    else:
        return str(val)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Renaming headers...")
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = ",") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def append_batch_file(
    df: pd.DataFrame,
    chunk_number: int,
    batch_file_path: str,
    target_file_path: str,
    skip_header: bool,
    truncate_file: bool,
) -> pd.DataFrame:
    global target_df
    truncate_file = True
    with open(batch_file_path, "r") as data_file:
        if truncate_file:
            open(target_file_path, "w+").close()
        with open(target_file_path, "w"):
            if skip_header:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
                )
                next(data_file)
            else:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path}"
                )
            batch_df = pd.read_csv(data_file, sep="|")
            logging.info("Making batch df -- >")
            if chunk_number == 1:
                target_df = batch_df
                target_df.to_csv(target_file_path, index=False, sep="|")
            else:
                batchdfcols = list(batch_df.columns)
                targetdfcols = dict.fromkeys(list(target_df.columns))
                logging.info(f"Removing common columns from batch : {chunk_number}")
                for columns in batchdfcols:
                    if columns in targetdfcols:
                        batch_df.drop(columns, axis=1, inplace=True)
                target_df = pd.concat([target_df, batch_df], axis=1, ignore_index=False)
                target_df.to_csv(target_file_path, index=False, sep="|")
        return target_df


def upload_file_to_gcs(
    file_path: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
) -> None:
    if os.path.exists(file_path):
        logging.info(
            f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        storage_client = storage.Client(project=project_id)
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
        chunksize=os.environ.get("CHUNKSIZE", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        year_report=os.environ.get("YEAR_REPORT", ""),
        api_naming_convention=os.environ.get("API_NAMING_CONVENTION", ""),
        geography=os.environ.get("GEOGRAPHY", ""),
        report_level=os.environ.get("REPORT_LEVEL", ""),
        concat_col_list=json.loads(os.environ.get("CONCAT_COL_LIST", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        rename_mappings_list=json.loads(os.environ.get("RENAME_MAPPINGS_LIST", r"{}")),
        input_csv_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        output_csv_headers=json.loads(os.environ.get("OUTPUT_CSV_HEADERS", r"[]")),
    )
