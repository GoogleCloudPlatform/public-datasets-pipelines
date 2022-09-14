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
import logging
import math
import os
import pathlib
import subprocess
import typing

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url_gcs: str,
    source_file_batch_length: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_root_path: str,
    target_gcs_source_path: str,
    target_gcs_unpack_path: str,
    target_gcs_load_path: str,
    project_id: str,
    dataset_id: str,
    table_id: str
) -> None:
    # number_source_files = count_files_in_gcs_bucket(
    #     project_id = project_id,
    #     source_gcs_folder_path = source_url_gcs,
    #     file_type="gz"
    # )
    # if number_source_files % source_file_batch_length > 0:
    #     number_file_batches = (int(number_source_files / source_file_batch_length)) + 1
    # else:
    #     number_file_batches = (int(number_source_files / source_file_batch_length))
    df_filelist = populate_df_gcs_filenames_in_bucket(
        project_id=project_id,
        source_gcs_folder_path=source_url_gcs,
        source_file_batch_length=source_file_batch_length,
        file_type = ".tar.gz"
    )
    import pdb; pdb.set_trace()

def populate_df_gcs_filenames_in_bucket(
    project_id: str,
    source_gcs_folder_path: str,
    source_file_batch_length: int,
    file_type: str
) -> pd.DataFrame:
    logging.info("Collecting list of files to process ...")
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_gcs_folder_path, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    df_filelist = pd.DataFrame(columns=["pathname", "guid", "batchnumber"])
    file_counter = 0
    batch_number = 0
    # import pdb; pdb.set_trace()
    for blob in bucket.list_blobs(): #bucket, prefix="/"):
        filename = str(blob).split(",")[1].strip()
        # import pdb; pdb.set_trace()
        if filename.find(f"{file_type}") > 0 or file_type == "":
            path = f"{source_gcs_folder_path}/{filename}"
            guid = filename.replace(f"{file_type}", "")
            if file_counter % int(source_file_batch_length) == 0:
                batch_number += 1
                logging.info(f"Generating metadata for batch {batch_number} file #{file_counter}")
            df_filelist.loc[len(df_filelist)] = [ path, guid, batch_number ]
            # logging.info(f"{filename}  {path} {guid} {batch_number}")
            # import pdb; pdb.set_trace()
            file_counter += 1
    return df_filelist


def count_files_in_gcs_bucket(
    project_id: str,
    source_gcs_folder_path: str,
    file_type: str
) -> int:
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_gcs_folder_path, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name, prefix="/")
    cnt_files = 0
    for blob in bucket.list_blobs(bucket):
        if os.path.basename(blob).find("{file_type}") > 0 or file_type == "":
            cnt_files += 1
    return cnt_files


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



    # logging.info(f"Downloading file {source_url}")
    # download_file(source_url, source_file)

    # with pd.read_csv(
    #     source_file,
    #     chunksize=int(chunk_size),
    # ) as reader:
    #     for chunk_number, chunk in enumerate(reader):
    #         logging.info(f"Processing batch {chunk_number}")
    #         target_file_batch = str(target_file).replace(
    #             ".csv", "-" + str(chunk_number) + ".csv"
    #         )
    #         df = pd.DataFrame()
    #         df = pd.concat([df, chunk])

    #         logging.info(f"Transforming {source_file} ...")

    #         logging.info(f"Transform: Rename columns {source_file} ...")
    #         rename_headers(df)

    #         logging.info("Transform: Converting date format.. ")
    #         convert_values(df)

    #         logging.info("Transform: Removing null values.. ")
    #         filter_null_rows(df)

    #         logging.info("Transform: Converting to integers..")
    #         convert_values_to_integer_string(df)

    #         logging.info("Transform: Converting to float..")
    #         removing_nan_values(df)

    #         logging.info("Transform: Reordering headers..")
    #         df = df[
    #             [
    #                 "unique_key",
    #                 "case_number",
    #                 "date",
    #                 "block",
    #                 "iucr",
    #                 "primary_type",
    #                 "description",
    #                 "location_description",
    #                 "arrest",
    #                 "domestic",
    #                 "beat",
    #                 "district",
    #                 "ward",
    #                 "community_area",
    #                 "fbi_code",
    #                 "x_coordinate",
    #                 "y_coordinate",
    #                 "year",
    #                 "updated_on",
    #                 "latitude",
    #                 "longitude",
    #                 "location",
    #             ]
    #         ]

    #         process_chunk(df, target_file_batch)

    #         logging.info(f"Appending batch {chunk_number} to {target_file}")
    #         if chunk_number == 0:
    #             subprocess.run(["cp", target_file_batch, target_file])
    #         else:
    #             subprocess.check_call(f"sed -i '1d' {target_file_batch}", shell=True)
    #             subprocess.check_call(
    #                 f"cat {target_file_batch} >> {target_file}", shell=True
    #             )
    #         subprocess.run(["rm", target_file_batch])

    # logging.info(
    #     f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    # )
    # upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    # logging.info(
    #     "Chicago crime process completed at "
    #     + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # )


def process_chunk(df: pd.DataFrame, target_file_batch: str) -> None:

    logging.info(f"Saving to output file.. {target_file_batch}")
    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    logging.info("..Done!")


def resolve_nan(input: typing.Union[str, float]) -> str:
    if not input or (math.isnan(input)):
        return ""
    return str(input).replace("None", "")


def removing_nan_values(df: pd.DataFrame) -> None:
    cols = ["x_coordinate", "y_coordinate", "latitude", "longitude"]
    for cols in cols:
        df[cols] = df[cols].apply(resolve_nan)


def convert_to_integer_string(input: typing.Union[str, float]) -> str:

    if not input or (math.isnan(input)):
        return ""
    return str(int(round(input, 0)))


def convert_values_to_integer_string(df: pd.DataFrame) -> None:
    cols = ["unique_key", "beat", "district", "ward", "community_area", "year"]

    for cols in cols:
        df[cols] = df[cols].apply(convert_to_integer_string)


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "ID": "unique_key",
        "Case Number": "case_number",
        "Date": "date",
        "Block": "block",
        "IUCR": "iucr",
        "Primary Type": "primary_type",
        "Description": "description",
        "Location Description": "location_description",
        "Arrest": "arrest",
        "Domestic": "domestic",
        "Beat": "beat",
        "District": "district",
        "Ward": "ward",
        "Community Area": "community_area",
        "FBI Code": "fbi_code",
        "X Coordinate": "x_coordinate",
        "Y Coordinate": "y_coordinate",
        "Year": "year",
        "Updated On": "updated_on",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Location": "location",
    }

    df.rename(columns=header_names, inplace=True)


def convert_dt_format(dt_str: str) -> str:
    # Old format: MM/dd/yyyy hh:mm:ss aa
    # New format: yyyy-MM-dd HH:mm:ss
    if not dt_str:
        return dt_str
    else:
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )


def convert_values(df: pd.DataFrame) -> None:
    dt_cols = ["date", "updated_on"]

    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)


def filter_null_rows(df: pd.DataFrame) -> None:
    df = df[df.unique_key != ""]


def save_to_new_file(df: pd.DataFrame, file_path: pathlib.Path) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url_gcs=os.environ.get("SOURCE_URL_GCS", ""),
        source_file_batch_length=os.environ.get("SOURCE_FILE_BATCH_LENGTH", "1000"),
        chunksize=os.environ.get("CHUNKSIZE", "500000"),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_root_path=os.environ.get("TARGET_GCS_ROOT_PATH", "data/trafficvision"),
        target_gcs_source_path=os.environ.get("TARGET_GCS_SOURCE_FOLDER", "files"),
        target_gcs_unpack_path=os.environ.get("TARGET_GCS_UNPACK_FOLDER", "unpack"),
        target_gcs_load_path=os.environ.get("TARGET_GCS_LOAD_FOLDER", "load_files"),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", "")
    )
