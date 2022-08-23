# Copyright 2022 Google LLC
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
    project_id: str,
    dataset_id: str,
    current_data_table_id: str,
    historical_data_table_id: str,
    data_file_surr_key_field: str,
    dest_folder: str,
    schema_filepath: str,
    source_bucket: str,
    target_gcs_bucket: str,
    dest_current_data_folder_name: str,
    dest_historical_data_folder_name: str,
    source_bucket_current_data_folder_name: str,
    current_data_target_gcs_path: str,
    historical_data_target_gcs_path: str,
    data_root_folder: typing.List[str],
    hist_folders_list: typing.List[str],
    pipeline_name: str,
) -> None:
    logging.info(f"{pipeline_name} process started")
    execute_pipeline(
        project_id = project_id,
        dataset_id = dataset_id,
        current_data_table_id = current_data_table_id,
        historical_data_table_id = historical_data_table_id,
        data_file_surr_key_field = data_file_surr_key_field,
        dest_folder = dest_folder,
        schema_filepath=schema_filepath,
        source_bucket = source_bucket,
        target_gcs_bucket = target_gcs_bucket,
        dest_current_data_folder_name = dest_current_data_folder_name,
        dest_historical_data_folder_name = dest_historical_data_folder_name,
        source_bucket_current_data_folder_name = source_bucket_current_data_folder_name,
        current_data_target_gcs_path = current_data_target_gcs_path,
        historical_data_target_gcs_path = historical_data_target_gcs_path,
        data_root_folder = data_root_folder,
        hist_folders_list = hist_folders_list,
        pipeline_name = pipeline_name,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    project_id: str,
    dataset_id: str,
    current_data_table_id: str,
    historical_data_table_id: str,
    data_file_surr_key_field: str,
    dest_folder: str,
    schema_filepath: str,
    source_bucket: str,
    target_gcs_bucket: str,
    dest_current_data_folder_name: str,
    dest_historical_data_folder_name: str,
    source_bucket_current_data_folder_name: str,
    current_data_target_gcs_path: str,
    historical_data_target_gcs_path: str,
    data_root_folder: typing.List[str],
    hist_folders_list: typing.List[str],
    pipeline_name: str,
) -> None:
    for folder in data_root_folder:
        root_gs_bucket_folder = f"gs://{source_bucket}"
        new_dest_current_data_folder_name = f"{dest_folder}/{folder}/{dest_current_data_folder_name}"
        new_dest_historical_data_folder_name = f"{dest_folder}/{folder}/{dest_historical_data_folder_name}"
        logging.info(f"Creating {new_dest_current_data_folder_name} if it does not exist")
        pathlib.Path(new_dest_current_data_folder_name).mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating {new_dest_historical_data_folder_name} if it does not exist")
        pathlib.Path(new_dest_historical_data_folder_name).mkdir(parents=True, exist_ok=True)
        # import pdb; pdb.set_trace()
        source_gs_folder = f"{root_gs_bucket_folder}/{source_bucket_current_data_folder_name}"
        process_data(
            project_id = project_id,
            dataset_id = dataset_id,
            table_name = current_data_table_id,
            schema_filepath = schema_filepath,
            target_gcs_bucket = target_gcs_bucket,
            data_file_surr_key_field = data_file_surr_key_field,
            source_gs_folder = source_gs_folder,
            dest_folder = new_dest_current_data_folder_name
        )


def download_file_gcs(
    project_id: str,
    source_location: str,
    destination_folder: str
) -> None:
    object_name = os.path.basename(source_location)
    dest_object = f"{destination_folder}/{object_name}"
    logging.info(f"   ... {source_location} -> {dest_object}")
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def download_folder_contents(
    project_id: str,
    source_gcs_folder_path: str,  # eg. "gs://normals/normal-hourly/access"
    destination_folder: str,
    file_type: str = ""
) -> None:
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_gcs_folder_path, "gs://")[1].split("/")[0]
    gcs_folder_path = str.split(source_gcs_folder_path, f"gs://{bucket_name}/")[1]
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f'{gcs_folder_path}')
    for blob in blobs:
        if os.path.splitext(os.path.basename(blob.name))[1] == f".{file_type}" or file_type == "":
            source_location = f"{source_gcs_folder_path}/{os.path.basename(blob.name)}"
            # import pdb; pdb.set_trace()
            download_file_gcs(
                project_id,
                source_location = source_location,
                destination_folder = destination_folder
            )


def process_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    schema_filepath: str,
    target_gcs_bucket: str,
    data_file_surr_key_field: str,
    source_gs_folder: str,
    dest_folder: str
) -> None:

    # download_folder_contents(
    #     project_id = project_id,
    #     source_gcs_folder_path = source_gs_folder,
    #     destination_folder = dest_folder,
    #     file_type = "csv"
    # )

    # * for each file in {dest_folder}\*.csv:
    for filename in os.listdir(dest_folder):
        filepath = os.path.join(dest_folder, filename)
        if os.path.isfile(filepath):
            process_file(
                filepath=filepath,
                project_id = project_id,
                dataset_id = dataset_id,
                table_name = table_name,
                schema_path = schema_filepath,
                target_gcs_bucket = target_gcs_bucket,
                data_file_surr_key_field = data_file_surr_key_field,
                data_file_surr_key_value = filename
            )

    import pdb; pdb.set_trace()

    # storage_client = storage.Client(project_id)
    # bucket_name = str.split(source_gs_folder, "gs://")[1].split("/")[0]
    # bucket = storage_client.bucket(bucket_name)
    # bucket.list_blobs()
    # download_file_gcs(
    #     project_id = project_id,
    #     source_location = source_gs_folder,
    #     destination_folder = dest_folder
    # )
    #    {source_gs_folder}/*.csv -> dest_folder

def process_file(
    filepath: str,
    project_id: str,
    dataset_id: str,
    table_name: str,
    schema_path: str,
    target_gcs_bucket: str,
    data_file_surr_key_field: str,
    data_file_surr_key_value: int
) -> None:

    logging.info(f"Processing file {filepath} started ...")

    if not table_exists(project_id, dataset_id, table_name):
        # Destination table doesn't exist
        create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_name,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
        )
    # if the table already has data for the file
    if table_already_has_file_data(
        project_id=project_id,
        dataset_id=dataset_id,
        table_name=table_name,
        data_file_surr_key_field=data_file_surr_key_value,
        data_file_surr_key_value=data_file_surr_key_value
    ):
        remove_file_table_data(
            project_id = project_id,
            dataset_id = dataset_id,
            table_name = table_name,
            data_file_surr_key_field = data_file_surr_key_field,
            data_file_surr_key_value = data_file_surr_key_value
        )

    # with pd.read_csv(
    #     filepath,
    #     engine="python",
    #     encoding="utf-8",
    #     quotechar='"',
    #     chunksize=int(chunksize),
    #     sep=",",
    #     names=input_headers,
    #     skiprows=1,
    #     dtype=data_dtypes,
    # ) as reader:
    #     for chunk_number, chunk in enumerate(reader):
    #         logging.info(
    #             f"Processing chunk #{chunk_number} of file {filepath} started"
    #         )
    #         target_file_batch = str(target_file).replace(
    #             ".csv", f"-{chunk_number}.csv"
    #         )
    #         df = pd.DataFrame()
    #         df = pd.concat([df, chunk])
    #         # process_chunk(
    #         #     df,
    #         #     target_file_batch,
    #         #     target_file_name,
    #         #     month_number == 1 and chunk_number == 0,
    #         #     month_number == 1 and chunk_number == 0,
    #         #     output_headers,
    #         #     pipeline_name,
    #         #     year_number,
    #         #     month_number,
    #         # )
    #         logging.info(
    #             f"Processing chunk #{chunk_number} of file {process_year_month} completed"
    #         )
    # if not table_exists(project_id, dataset_id, table_id):
    #     # Destination able doesn't exist
    #     create_dest_table(
    #         project_id=project_id,
    #         dataset_id=dataset_id,
    #         table_id=table_id,
    #         schema_filepath=schema_path,
    #         bucket_name=target_gcs_bucket,
    #     )
    # load_data_to_bq(
    #     project_id=project_id,
    #     dataset_id=dataset_id,
    #     table_id=table_id,
    #     file_path=target_file_name,
    #     field_delimiter="|",
    # )
    # upload_file_to_gcs(
    #     file_path=target_file_name,
    #     target_gcs_bucket=target_gcs_bucket,
    #     target_gcs_path=str(target_gcs_path).replace(
    #         ".csv", f"_{process_year_month}.csv"
    #     ),
    # )
    logging.info(f"Processing file {filepath} completed ...")


    #     * load into df

    #     * transforms:
    #         * format datetime in date fields
    #         * add metadata columns
    #     * rewrite/overwrite file back to original



# def process_year_data(
#     source_url: str,
#     year_number: int,
#     source_file: str,
#     target_file: str,
#     project_id: str,
#     dataset_id: str,
#     table_id: str,
#     data_file_year_field: str,
#     data_file_month_field: str,
#     schema_path: str,
#     chunksize: str,
#     target_gcs_bucket: str,
#     target_gcs_path: str,
#     pipeline_name: str,
#     input_headers: typing.List[str],
#     data_dtypes: dict,
#     output_headers: typing.List[str],
# ) -> None:
#     logging.info(f"Processing year {year_number}")
#     destination_table = f"{table_id}_{year_number}"
#     for month_number in range(1, 13):
#         padded_month = str(month_number).zfill(2)
#         process_year_month = f"{year_number}-{padded_month}"
#         logging.info(f"Processing month {process_year_month}")
#         month_data_already_loaded = table_has_month_data(
#             project_id=project_id,
#             dataset_id=dataset_id,
#             table_name=destination_table,
#             data_file_year_field=data_file_year_field,
#             year_number=year_number,
#             data_file_month_field=data_file_month_field,
#             month_number=month_number,
#         )
#         if month_data_already_loaded:
#             logging.info(f"{process_year_month} data is already loaded. Skipping.")
#         else:
#             target_file_name = str.replace(
#                 target_file, ".csv", f"_{year_number}-{month_number}.csv"
#             )
#             process_month(
#                 source_url=source_url,
#                 year_number=year_number,
#                 month_number=month_number,
#                 source_file=source_file,
#                 target_file=target_file,
#                 project_id=project_id,
#                 dataset_id=dataset_id,
#                 table_id=destination_table,
#                 target_file_name=target_file_name,
#                 schema_path=schema_path,
#                 chunksize=chunksize,
#                 target_gcs_bucket=target_gcs_bucket,
#                 target_gcs_path=target_gcs_path,
#                 input_headers=input_headers,
#                 data_dtypes=data_dtypes,
#                 output_headers=output_headers,
#                 pipeline_name=pipeline_name,
#             )
#     logging.info(f"Processing year {year_number} completed")


def table_already_has_file_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    data_file_surr_key_field: str,
    data_file_surr_key_value: int
) -> bool:
    check_field_exists = field_exists(
        project_id, dataset_id, table_name, data_file_surr_key_field
    )
    if check_field_exists:
        client = bigquery.Client(project=project_id)
        query = f"""
            SELECT count(1) AS number_of_rows
              FROM {dataset_id}.{table_name}
             WHERE {data_file_surr_key_field} = '{data_file_surr_key_value}'
        """
        job_config = bigquery.QueryJobConfig()
        query_job = client.query(query, job_config=job_config)
        for row in query_job.result():
            count_rows = row.number_of_rows
        if int(count_rows) > 0:
            return True
        else:
            return False
    else:
        return None


def remove_file_table_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    data_file_surr_key_field: str,
    data_file_surr_key_value: int
) -> bool:
    check_field_exists = field_exists(
        project_id, dataset_id, table_name, data_file_surr_key_field
    )
    if check_field_exists:
        try:
            client = bigquery.Client(project=project_id)
            query = f"""
                DELETE
                FROM {dataset_id}.{table_name}
                WHERE {data_file_surr_key_field} = '{data_file_surr_key_value}'
            """
            query_job = client.query(query)  # API request
            query_job.result()
        except Exception as e:
            logging.info(e)
            return False
    else:
        return None


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


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    field_delimiter: str,
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = field_delimiter
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
) -> None:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    try:
        table_exists_id = client.get_table(table_ref).table_id
        logging.info(f"Table {table_exists_id} currently exists.")
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


# def process_month(
#     source_url: str,
#     year_number: int,
#     month_number: int,
#     source_file: str,
#     target_file: str,
#     project_id: str,
#     dataset_id: str,
#     table_id: str,
#     target_file_name: str,
#     schema_path: str,
#     chunksize: str,
#     target_gcs_bucket: str,
#     target_gcs_path: str,
#     input_headers: typing.List[str],
#     data_dtypes: dict,
#     output_headers: typing.List[str],
#     pipeline_name: str,
# ) -> None:
#     padded_month = str(month_number).zfill(2)
#     process_year_month = f"{year_number}-{padded_month}"
#     source_url_to_process = f"{source_url}{process_year_month}.parquet"
#     source_parquet_file = str(source_file).replace(
#         ".csv", f"_{process_year_month}.parquet"
#     )
#     source_file_to_process = str(source_file).replace(
#         ".csv", f"_{process_year_month}.csv"
#     )
#     successful_download = download_file(source_url_to_process, source_parquet_file)
#     if successful_download:
#         try:
#             df_parquet = pd.read_parquet(source_parquet_file)
#         except BaseException as error:
#             logging.info(f" ... Unable to obtain or read parquet file ... {error}")
#             logging.info(f"Processing {process_year_month} failed")
#         else:
#             df_parquet.to_csv(source_file_to_process, sep="|", index=False)
#             with pd.read_csv(
#                 source_file_to_process,
#                 engine="python",
#                 encoding="utf-8",
#                 quotechar='"',
#                 chunksize=int(chunksize),
#                 sep="|",
#                 names=input_headers,
#                 skiprows=1,
#                 dtype=data_dtypes,
#             ) as reader:
#                 for chunk_number, chunk in enumerate(reader):
#                     logging.info(
#                         f"Processing chunk #{chunk_number} of file {process_year_month} started"
#                     )
#                     target_file_batch = str(target_file).replace(
#                         ".csv", f"-{process_year_month}-{chunk_number}.csv"
#                     )
#                     df = pd.DataFrame()
#                     df = pd.concat([df, chunk])
#                     process_chunk(
#                         df,
#                         target_file_batch,
#                         target_file_name,
#                         month_number == 1 and chunk_number == 0,
#                         month_number == 1 and chunk_number == 0,
#                         output_headers,
#                         pipeline_name,
#                         year_number,
#                         month_number,
#                     )
#                     logging.info(
#                         f"Processing chunk #{chunk_number} of file {process_year_month} completed"
#                     )
#             if not table_exists(project_id, dataset_id, table_id):
#                 # Destination able doesn't exist
#                 create_dest_table(
#                     project_id=project_id,
#                     dataset_id=dataset_id,
#                     table_id=table_id,
#                     schema_filepath=schema_path,
#                     bucket_name=target_gcs_bucket,
#                 )
#             load_data_to_bq(
#                 project_id=project_id,
#                 dataset_id=dataset_id,
#                 table_id=table_id,
#                 file_path=target_file_name,
#                 field_delimiter="|",
#             )
#             upload_file_to_gcs(
#                 file_path=target_file_name,
#                 target_gcs_bucket=target_gcs_bucket,
#                 target_gcs_path=str(target_gcs_path).replace(
#                     ".csv", f"_{process_year_month}.csv"
#                 ),
#             )
#             logging.info(f"Processing {process_year_month} completed")
#     else:
#         logging.info(
#             f"Informational: The data file {target_file_name} was not generated because no data was available for year {year_number}.  Continuing."
#         )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    include_header: bool,
    truncate_file: bool,
    output_headers: typing.List[str],
    pipeline_name: str,
    year_number: int,
    month_number: int,
) -> None:
    if pipeline_name == "tlc_green_trips":
        df["distance_between_service"] = ""
        df["time_between_service"] = ""
    df["data_file_year"] = year_number
    df["data_file_month"] = month_number
    df = format_date_time(df, "pickup_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df = format_date_time(df, "dropoff_datetime", "strftime", "%Y-%m-%d %H:%M:%S")
    df["passenger_count"] = df["passenger_count"].apply(lambda x: str(int(float(str(x)))) if str(x).replace('.', '', 1).isdigit() else "")
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
            f"Uploading output file {file_path} to gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket(target_gcs_bucket)
        blob = bucket.blob(target_gcs_path)
        blob.upload_from_filename(file_path)
    else:
        logging.info(
            f"Cannot upload file {file_path} to gs://{target_gcs_bucket}/{target_gcs_path} as it does not exist."
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        current_data_table_id=os.environ.get("CURRENT_DATA_TABLE_ID", ""),
        historical_data_table_id=os.environ.get("HISTORICAL_DATA_TABLE_ID", ""),
        data_file_surr_key_field=os.environ.get("DATA_FILE_SURR_KEY_FIELD", ""),
        dest_folder=os.environ.get("DEST_FOLDER", ""),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH", ""),
        source_bucket=os.environ.get("SOURCE_BUCKET", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        dest_current_data_folder_name=os.environ.get("DEST_CURRENT_DATA_FOLDER_NAME", ""),
        dest_historical_data_folder_name=os.environ.get("DEST_HISTORICAL_FOLDER_NAME", ""),
        source_bucket_current_data_folder_name=os.environ.get("SOURCE_BUCKET_CURRENT_DATA_FOLDER_NAME", ""),
        current_data_target_gcs_path=os.environ.get("CURRENT_DATA_TARGET_GCS_PATH", ""),
        historical_data_target_gcs_path=os.environ.get("HISTORICAL_DATA_TARGET_GCS_PATH", ""),
        data_root_folder=json.loads(os.environ.get("DATA_ROOT_FOLDER", r"[]")),
        hist_folders_list=json.loads(os.environ.get("HIST_FOLDERS_LIST", r"[]")),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
    )
