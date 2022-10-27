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
import subprocess
import typing
from datetime import datetime

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    download_location: str,
    target_file: str,
    chunksize: str,
    target_gcs_bucket: str,
    source_gcs_path: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict
) -> None:
    source_files=list_files(source_bucket=target_gcs_bucket, source_gcs_path=source_gcs_path)
    file_number=0
    for source_file in source_files:
        download_file(source_url+source_file, download_location+source_file, target_gcs_bucket)
        chunksz = int(chunksize)
        temp_store=target_file
        target_file=target_file+"_"+str(file_number)+".csv"
        logging.info("Reading csv file")
        csvfile=download_location+source_file
        with pd.read_csv(
            csvfile,
            engine="python",
            encoding="utf-8",
            quotechar='"',
            chunksize=chunksz,
        ) as reader:
            for chunk_number, chunk in enumerate(reader):
                logging.info(f"Processing batch {chunk_number}")
                target_file_batch = str(target_file).replace(".csv", "-" + str(chunk_number) + ".csv")
                df = pd.DataFrame()
                df = pd.concat([df, chunk])
                processChunk(df, target_file_batch, headers, rename_mappings)
                logging.info(f"Appending batch {chunk_number} to {target_file}")
                if chunk_number == 0:
                    subprocess.run(["cp", target_file_batch, target_file])
                else:
                    subprocess.check_call(f"sed -i '1d' {target_file_batch}", shell=True)
                    subprocess.check_call(
                        f"cat {target_file_batch} >> {target_file}", shell=True
                    )
                subprocess.run(["rm", target_file_batch])
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path, str(file_number))
        subprocess.run(["rm", target_file])
        logging.info("Proceed to next file, if any =======>")
        print()
        file_number+=1
        target_file=temp_store

def list_files(source_bucket, source_gcs_path):
    client=storage.Client()
    blobs=client.list_blobs(source_bucket,prefix=source_gcs_path+"split")
    files=[]
    for blob in blobs:
        files.append(blob.name.split("/")[-1])
    return files

def processChunk(df: pd.DataFrame, target_file_batch: str, headers, rename_mappings) -> None:
    rename_headers_(df, rename_mappings)
    logging.info("Convert Date Format")
    df["date"] = df["date"].apply(convert_dt_format)
    logging.info("Reordering headers..")
    df = df[headers]
    df["county_number"] = df["county_number"].astype("Int64")
    logging.info(f"Saving to output file.. {target_file_batch}")
    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    logging.info("..Done!")


def rename_headers_(df: pd.DataFrame, rename_mappings) -> None:
    logging.info("Renaming Headers")
    df = df.rename(columns=rename_mappings, inplace=True)


def convert_dt_format(dt_str: str) -> str:
    if dt_str is None or len(dt_str) == 0:
        return dt_str
    else:
        if len(dt_str) == 10:
            return datetime.strptime(dt_str, "%m/%d/%Y").strftime("%Y-%m-%d")


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, download_location: str, source_bucket: str) -> None:
    logging.info("Downloading source file")
    logging.info(f"Downloading {source_url} into {download_location}")
    client=storage.Client()
    bucket=client.bucket(source_bucket)
    blob=bucket.blob(source_url)
    blob.download_to_filename(download_location)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str, file_number: str) -> None:
    logging.info("Uploading output file to gcs")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    filename=gcs_path+file_number+".csv"
    blob = bucket.blob(filename)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        download_location=os.environ["DOWNLOAD_LOCATION"],
        target_file=os.environ["TARGET_FILE"],
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        source_gcs_path=os.environ["SOURCE_GCS_PATH"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"])
    )
