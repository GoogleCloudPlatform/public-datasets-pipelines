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
    source_url_stations_json: str,
    source_url_status_json: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    transform_list: typing.List[str],
    data_dtypes: typing.List[str],
    null_rows_list: typing.List[str],
    parse_dates_list: dict,
    rename_headers_list: dict,
    reorder_headers_list: typing.List[str],
    output_headers_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
    remove_whitespace_list: typing.List[str],
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    successful_completion = execute_pipeline(
                                source_url=source_url,
                                source_url_stations_json=source_url_stations_json,
                                source_url_status_json=source_url_status_json,
                                source_file=source_file,
                                target_file=target_file,
                                project_id=project_id,
                                dataset_id=dataset_id,
                                destination_table=table_id,
                                chunksize=chunksize,
                                target_gcs_bucket=target_gcs_bucket,
                                target_gcs_path=target_gcs_path,
                                schema_path=schema_path,
                                transform_list=transform_list,
                                data_dtypes=data_dtypes,
                                null_rows_list=null_rows_list,
                                parse_dates_list=parse_dates_list,
                                rename_headers_list=rename_headers_list,
                                output_headers_list=output_headers_list,
                                datetime_fieldlist=datetime_fieldlist,
                                resolve_datatypes_list=resolve_datatypes_list,
                                normalize_data_list=normalize_data_list,
                                boolean_datapoints_list=boolean_datapoints_list,
                                remove_whitespace_list=remove_whitespace_list,
                                regex_list=regex_list,
                                crash_field_list=crash_field_list,
                                date_format_list=date_format_list,
                                reorder_headers_list=reorder_headers_list
                            )
    if successful_completion:
        logging.info(f"{pipeline_name} process completed")
    else:
        logging.info(f"{pipeline_name} process was unknown and failed")


def execute_pipeline(
    source_url: str,
    source_url_stations_json: str,
    source_url_status_json: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    transform_list: typing.List[str],
    data_dtypes: typing.List[str],
    parse_dates_list: dict,
    null_rows_list: typing.List[str],
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    reorder_headers_list: typing.List[str],
    regex_list: typing.List[typing.List],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
    remove_whitespace_list: typing.List[str],
) -> bool:
    if destination_table not in [
                                "311_service_requests",
                                "citibike_stations",
                                "nypd_mv_collisions",
                                "tree_census_1995"
    ]:
        logging.info("Unknown pipeline")
        return False
    else:
        sep = ","
        if destination_table == "311_service_requests":
            # download_file(source_url, source_file)
            pass
        elif destination_table == "citibike_stations":
            download_and_merge_source_files(
                source_url_stations_json=source_url_stations_json,
                source_url_status_json=source_url_status_json,
                source_file=source_file,
                resolve_datatypes_list=resolve_datatypes_list,
                normalize_data_list=normalize_data_list,
                boolean_datapoints_list=boolean_datapoints_list
            )
            sep = "|"
        elif destination_table == "nypd_mv_collisions":
            download_file(source_url, source_file)
        elif destination_table == "tree_census_1995":
            download_file(source_url=source_url, source_file=source_file)
        process_source_file(
            source_file=source_file,
            target_file=target_file,
            chunksize=chunksize,
            data_dtypes=data_dtypes,
            parse_dates_list=parse_dates_list,
            null_rows_list=null_rows_list,
            rename_headers_list=rename_headers_list,
            output_headers_list=output_headers_list,
            destination_table=destination_table,
            normalize_data_list=normalize_data_list,
            boolean_datapoints_list=boolean_datapoints_list,
            transform_list=transform_list,
            reorder_headers_list=output_headers_list,
            datetime_fieldlist=datetime_fieldlist,
            resolve_datatypes_list=resolve_datatypes_list,
            regex_list=regex_list,
            remove_whitespace_list=remove_whitespace_list,
            crash_field_list=crash_field_list,
            date_format_list=date_format_list,
            sep=sep
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
                )
            else:
                error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
                raise ValueError(error_msg)
        else:
            logging.info(
                f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
            )
        return True


def download_and_merge_source_files(
    source_url_stations_json: str,
    source_url_status_json: str,
    source_file: str,
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str]
) -> None:
    source_file_stations_csv = str(source_file).replace(".csv", "") + "_stations.csv"
    source_file_stations_json = str(source_file).replace(".csv", "") + "_stations"
    source_file_status_csv = str(source_file).replace(".csv", "") + "_status.csv"
    source_file_status_json = str(source_file).replace(".csv", "") + "_status"
    download_file_json(
        source_url_stations_json, source_file_stations_json, source_file_stations_csv
    )
    download_file_json(
        source_url_status_json, source_file_status_json, source_file_status_csv
    )
    df_stations = pd.read_csv(
        source_file_stations_csv, engine="python", encoding="utf-8", quotechar='"'
    )
    df_status = pd.read_csv(
        source_file_status_csv, engine="python", encoding="utf-8", quotechar='"'
    )
    logging.info("Merging files")
    df = df_stations.merge(df_status, left_on="station_id", right_on="station_id")
    df = clean_data_points(
        df,
        resolve_datatypes_list=resolve_datatypes_list,
        normalize_data_list=normalize_data_list,
        boolean_datapoints_list=boolean_datapoints_list,
    )
    save_to_new_file(df, source_file)


def download_file_json(
    source_url: str, source_file_json: pathlib.Path, source_file_csv: pathlib.Path
) -> None:
    logging.info(f"Downloading file {source_url}.json.")
    r = requests.get(source_url + ".json", stream=True)
    with open(source_file_json + ".json", "wb") as f:
        for chunk in r:
            f.write(chunk)
    df = pd.read_json(source_file_json + ".json")["data"]["stations"]
    df = pd.DataFrame(df)
    df.to_csv(source_file_csv, index=False)


def clean_data_points(
    df: pd.DataFrame,
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> pd.DataFrame:
    df = resolve_datatypes(df, resolve_datatypes_list)
    df = normalize_data(df, normalize_data_list)
    df = resolve_boolean_datapoints(df, boolean_datapoints_list)
    return df


def resolve_datatypes(df: pd.DataFrame, resolve_datatypes_list: dict) -> pd.DataFrame:
    for column, datatype in resolve_datatypes_list.items():
        logging.info(f"Resolving datatype for column {column} to {datatype}")
        if datatype in ('Int64', 'Float'):
            df[column] = df[column].fillna(0).astype(datatype)
        else:
            df[column] = df[column].astype(datatype)
    return df


def normalize_data(
    df: pd.DataFrame, normalize_data_list: typing.List[str]
) -> pd.DataFrame:
    for column in normalize_data_list:
        logging.info(f"Normalizing data in column {column}")
        # Data is in list format in this column.
        # Therefore remove square brackets and single quotes
        df[column] = (
            str(pd.Series(df[column])[0])
            .replace("[", "")
            .replace("'", "")
            .replace("]", "")
        )
    return df


def resolve_boolean_datapoints(
    df: pd.DataFrame, boolean_datapoints_list: typing.List[str]
) -> pd.DataFrame:
    for column in boolean_datapoints_list:
        logging.info(f"Resolving boolean datapoints in column {column}")
        df[column] = df[column].apply(lambda x: "True" if x == "0" else "False")
    return df


def process_source_file(
    source_file: str,
    target_file: str,
    destination_table: str,
    chunksize: str,
    data_dtypes: dict,
    parse_dates_list: typing.List[str],
    null_rows_list: typing.List[str],
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    transform_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    regex_list: typing.List[typing.List],
    remove_whitespace_list: typing.List[str],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
    sep: str = ","
) -> None:
    logging.info(f"Processing file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),
        dtype=data_dtypes,
        parse_dates=parse_dates_list,
        sep = sep
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df=df,
                target_file_batch=target_file_batch,
                target_file=target_file,
                destination_table=destination_table,
                skip_header=(not chunk_number == 0),
                rename_headers_list=rename_headers_list,
                null_rows_list=null_rows_list,
                parse_dates_list=parse_dates_list,
                reorder_headers_list=reorder_headers_list,
                # normalize_data_list=normalize_data_list,
                # boolean_datapoints_list=boolean_datapoints_list,
                transform_list=transform_list,
                output_headers_list=output_headers_list,
                datetime_fieldlist=datetime_fieldlist,
                resolve_datatypes_list=resolve_datatypes_list,
                regex_list=regex_list,
                remove_whitespace_list=remove_whitespace_list,
                crash_field_list=crash_field_list,
                date_format_list=date_format_list,
            )


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
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
        table = client.get_table(table_ref)
        table_exists_id = table.table_id
        logging.info(f"Table {table_exists_id} currently exists.")
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


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    destination_table: str,
    skip_header: bool,
    transform_list: typing.List[str],
    rename_headers_list: dict,
    output_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    parse_dates_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    # normalize_data_list: typing.List[str],
    # boolean_datapoints_list: typing.List[str],
    datetime_fieldlist: typing.List[str],
    resolve_datatypes_list: dict,
    regex_list: typing.List[typing.List],
    remove_whitespace_list: typing.List[str],
    crash_field_list: typing.List[typing.List],
    date_format_list: typing.List[typing.List],
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    if destination_table == "311_service_requests":
        df = resolve_date_format(df, parse_dates_list)
        df = rename_headers(df, rename_headers_list)
        df = remove_null_rows(df, null_rows_list)
        df = reorder_headers(df, reorder_headers_list)
    if destination_table == "citibike_stations":
        df = convert_datetime_from_int(df, datetime_fieldlist)
        df = rename_headers(df, rename_headers_list)
        df = reorder_headers(df, output_headers_list)
    if destination_table == "nypd_mv_collisions":
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
    if destination_table == "tree_census_1995":
        df = rename_headers(df, rename_headers_list)
        df = remove_whitespace(df, remove_whitespace_list)
        df = reorder_headers(df, reorder_headers_list)
    if not df.empty:
        save_to_new_file(df, file_path=str(target_file_batch))
        append_batch_file(
            batch_file_path=target_file_batch,
            target_file_path=target_file,
            skip_header=skip_header,
            truncate_file=not (skip_header),
        )
    logging.info(f"Processing batch file {target_file_batch} completed")


def add_crash_timestamp(
    df: pd.DataFrame, new_crash_field: str, crash_date_field: str, crash_time_field: str
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


def remove_whitespace(
    df: pd.DataFrame, remove_whitespace_list: typing.List[str]
) -> pd.DataFrame:
    for column in remove_whitespace_list:
        logging.info(f"Removing whitespace in column {column}..")
        df[column] = df[column].apply(lambda x: str(x).strip())
    return df


def replace_regex(df: pd.DataFrame, regex_list: dict) -> pd.DataFrame:
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


def convert_datetime_from_int(
    df: pd.DataFrame, datetime_columns_list: typing.List[str]
) -> pd.DataFrame:
    for column in datetime_columns_list:
        logging.info(f"Converting Datetime column {column}")
        df[column] = df[column].astype(str).astype(int).apply(datetime_from_int)
    return df


def datetime_from_int(dt_int: int) -> str:
    return datetime.datetime.fromtimestamp(dt_int).strftime("%Y-%m-%d %H:%M:%S")


def clean_data_points(
    df: pd.DataFrame,
    resolve_datatypes_list: dict,
    normalize_data_list: typing.List[str],
    boolean_datapoints_list: typing.List[str],
) -> pd.DataFrame:
    df = resolve_datatypes(df, resolve_datatypes_list)
    df = normalize_data(df, normalize_data_list)
    df = resolve_boolean_datapoints(df, boolean_datapoints_list)
    return df


def remove_null_rows(
    df: pd.DataFrame, null_rows_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Removing rows with empty keys")
    for column in null_rows_list:
        df = df[df[column] != ""]
    return df


def reorder_headers(df: pd.DataFrame, output_headers: typing.List[str]) -> pd.DataFrame:
    logging.info("Reordering headers..")
    return df[output_headers]


def resolve_date_format(
    df: pd.DataFrame, parse_dates: typing.List[str]
) -> pd.DataFrame:
    for dt_fld in parse_dates:
        logging.info(f"Resolving date format in column {dt_fld}")
        df[dt_fld] = df[dt_fld].apply(convert_dt_format)
    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif (
        str(dt_str).strip()[2] == "/"
    ):  # if there is a '/' in 3rd position, then we have a date format mm/dd/yyyy
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def rename_headers(df: pd.DataFrame, header_names: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    df = df.rename(columns=header_names)
    return df


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


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
        chunksize=os.environ.get("CHUNKSIZE", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", "{}")),
        null_rows_list=json.loads(os.environ.get("NULL_ROWS_LIST", "[]")),
        parse_dates_list=json.loads(os.environ.get("PARSE_DATES", "{}")),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", "{}")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", "[]")),
        output_headers_list=json.loads(os.environ.get("OUTPUT_CSV_HEADERS", "[]")),
        source_url_stations_json=os.environ.get("SOURCE_URL_STATIONS_JSON", ""),
        source_url_status_json=os.environ.get("SOURCE_URL_STATUS_JSON", ""),
        transform_list=json.loads(os.environ.get("TRANSFORM_LIST", "[]")),
        datetime_fieldlist=json.loads(os.environ.get("DATETIME_FIELDLIST", "[]")),
        resolve_datatypes_list=json.loads(os.environ.get("RESOLVE_DATATYPES_LIST", "{}")),
        normalize_data_list=json.loads(os.environ.get("NORMALIZE_DATA_LIST", "[]")),
        boolean_datapoints_list=json.loads(os.environ.get("BOOLEAN_DATAPOINTS_LIST", "[]")),
        remove_whitespace_list=json.loads(os.environ.get("REMOVE_WHITESPACE_LIST", "[]")),
        regex_list=json.loads(os.environ.get("REGEX_LIST", "[]")),
        crash_field_list=json.loads(os.environ.get("CRASH_FIELD_LIST", "[]")),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", "[]")),
    )
