# Copyright 2024 Google LLC
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
import shutil
from datetime import datetime

import json_stream
import pandas as pd
from google.cloud import storage
from google.cloud.storage.fileio import BlobReader
from json_stream.dump import JSONStreamEncoder, default


def main(
    source_bucket: str,
    source_object: str,
    target_bucket: str,
    target_local_dir: str,
    chunk_size: str,
) -> None:
    logging.info(
        f"HACKER NEWS process started at { str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) }"
    )
    success = stream_split_source_file(
        source_bucket=source_bucket,
        source_object=source_object,
        target_bucket=target_bucket,
        # target_object=target_object,
        target_local_dir=target_local_dir,
        chunk_size=int(chunk_size),
    )
    if success:
        logging.info(
            f"HACKER NEWS process completed at { str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) }"
        )
    else:
        logging.info(
            f"HACKER NEWS process failed at { str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) }"
        )


def stream_split_source_file(
    source_bucket: str,
    source_object: str,
    target_bucket: str,
    target_local_dir: str,
    chunk_size: int = 100000,
) -> bool:
    # Create Cloud Storage client
    storage_client = storage.Client()
    # Create a reference to the bucket
    bucket = storage_client.bucket(source_bucket)
    # source_file_path = os.path.join(source_gcs_dir, file_name)
    # Create a reference to the file in the bucket
    blob = bucket.blob(source_object)
    # Create a file-like object to read from without loading the whole file in memory
    reader = BlobReader(blob)
    # local folder to stage the data files in
    batch_file_target_dir = os.path.join(target_local_dir, "batch")
    # Create output directory
    if os.path.exists(batch_file_target_dir) and os.path.isdir(batch_file_target_dir):
        shutil.rmtree(batch_file_target_dir)
    pathlib.Path(batch_file_target_dir).mkdir(parents=True)
    # Count the number of records so that we know when the end of the streamed source data section is
    total_records = count_source_file_records(source_bucket, source_object, chunk_size)
    # Open the data stream
    data = json_stream.load(reader)
    # Obtain the section containing the data to process and load
    items = data["v0"]["item"]
    # Counter pertaining to cumulative number of source records read
    count = 1
    # Batch row counter
    row_count = 0
    # File number counter
    file_num = 1

    for id, item in items.items():
        local_batch_file_name = os.path.join(
            batch_file_target_dir, f"hn_processed_{str(file_num).zfill(10)}.json"
        )
        if row_count == 0:
            logging.info(
                f"Processed {count} rows - Creating batch file {local_batch_file_name}..."
            )
            if os.path.isfile(local_batch_file_name):
                # Remove the [local] batch JSON file if it exists
                os.remove(local_batch_file_name)
            with open(local_batch_file_name, "w") as outfile:
                outfile.write('{"data": [\n')
        if (count + 1) == total_records:
            # if we are processing the last record
            with open(local_batch_file_name, "a") as outfile:
                outfile.write(json.dumps(item, default=default) + "\n] }")
        else:
            if count % chunk_size != 0:
                # if we are appending a row from within a batch
                with open(local_batch_file_name, "a") as outfile:
                    if (count + 1) % chunk_size == 0:
                        outfile.write(json.dumps(item, default=default) + "\n")
                    else:
                        outfile.write(json.dumps(item, default=default) + ",\n")
            else:
                # if we are processing the last item in a batch
                if os.path.isfile(local_batch_file_name):
                    # Close-up the batch file write process
                    close_batch_file_write(
                        local_batch_file_name=local_batch_file_name,
                        target_bucket=target_bucket,
                        source_object=source_object,
                    )
                    row_count = -1
                file_num = file_num + 1
        count = count + 1
        row_count = row_count + 1
    logging.info(f" ... processed {count} rows")


def close_batch_file_write(
    local_batch_file_name: str, target_bucket: str, source_object: str
):
    with open(local_batch_file_name, "a") as outfile:
        outfile.write("] }")
    # Target location for the new batch file in GCS
    target_bucket_file = os.path.join(
        os.path.dirname(source_object), "batch", os.path.basename(local_batch_file_name)
    )
    # Convert and fix the data from JSON to csv
    target_file_batch_csv = convert_json_file_to_csv(local_batch_file_name)
    target_bucket_file = os.path.join(
        os.path.dirname(source_object), "batch", os.path.basename(target_file_batch_csv)
    )
    if os.path.isfile(local_batch_file_name):
        # Remove the [local] batch JSON file if it exists
        os.remove(local_batch_file_name)
    # Upload the new CSV batch file to GCS
    upload_file_to_gcs(
        file_path=target_file_batch_csv,
        gcs_bucket=target_bucket,
        gcs_path=target_bucket_file,
    )
    if os.path.isfile(target_file_batch_csv):
        # Remove the [local] batch csv file if it exists
        os.remove(target_file_batch_csv)


def count_source_file_records(
    source_bucket: str, source_object: str, chunk_size: int = 100000
) -> int:
    logging.info(
        f"Counting number of records in gs://{ os.path.join(source_bucket, source_object)} ..."
    )
    # Create Cloud Storage client
    storage_client = storage.Client()
    # Create a reference to the bucket
    bucket = storage_client.bucket(source_bucket)
    # source_file_path = os.path.join(source_gcs_dir, file_name)
    # Create a reference to the file in the bucket
    blob = bucket.blob(source_object)
    # Create a file-like object to read from without loading the whole file in memory
    reader = BlobReader(blob)
    # Connect to the stream
    data = json_stream.load(reader)
    items = data["v0"]["item"]
    total_count = 0
    # Read and count data records
    for id, item in items.items():
        total_count += 1
        if total_count % chunk_size == 0:
            logging.info(f" ... found {total_count} records")
    logging.info(f" ... found {total_count} total records")
    logging.info(datetime.now())
    return total_count


def convert_json_file_to_csv(source_json_file: str) -> str:
    target_file_batch_csv = source_json_file.replace(".json", ".csv")
    if os.path.isfile(target_file_batch_csv):
        # Remove the [local] batch csv file if it exists
        os.remove(target_file_batch_csv)
    with open(source_json_file, "r") as source_json:
        data = json.load(source_json)
        df = pd.json_normalize(data["data"], max_level=0)
        df["time"] = df["time"].astype("Int64")
        df["time"] = df["time"].astype("str")
        df["time"] = df["time"].apply(lambda x: "" if x == "<NA>" else x)
        df["timestamp"] = df["time"].apply(
            lambda x: (
                ""
                if x == ""
                else f"{datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
        )
        df["descendants"] = df["descendants"].astype("Int64")
        df["descendants"] = df["descendants"].astype("str")
        df["descendants"] = df["descendants"].apply(lambda x: "" if x == "<NA>" else x)
        df["score"] = df["score"].astype("Int64")
        df["score"] = df["score"].astype("str")
        df["score"] = df["score"].apply(lambda x: "" if x == "<NA>" else x)
        df["parent"] = df["parent"].astype("Int64")
        df["parent"] = df["parent"].astype("str")
        df["parent"] = df["parent"].apply(lambda x: "" if x == "<NA>" else x)
        df["ranking"] = ""
        df["text"] = df["text"].replace(r"\n", " ", regex=True)
        df["text"] = df["text"].replace(r"\r", " ", regex=True)
        df["text"] = df["text"].replace(r"\x00", "", regex=True)
        df["title"] = df["title"].replace(r"\n", " ", regex=True)
        df["title"] = df["title"].replace(r"\r", " ", regex=True)
        df["title"] = df["title"].replace(r"\x00", "", regex=True)
        df = df[
            [
                "title",
                "url",
                "text",
                "dead",
                "by",
                "score",
                "time",
                "timestamp",
                "type",
                "id",
                "parent",
                "descendants",
                "ranking",
                "deleted",
            ]
        ]
        save_to_new_file(df, file_path=str(target_file_batch_csv), sep="|")
        # Release the dataframe memory
        del df
    return str(target_file_batch_csv)


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = ",") -> None:
    df.to_csv(file_path, index=False, sep=sep)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_bucket=os.environ.get("SOURCE_BUCKET", ""),
        source_object=os.environ.get("SOURCE_OBJECT", ""),
        target_bucket=os.environ.get("TARGET_BUCKET", ""),
        target_local_dir=os.environ.get("TARGET_LOCAL_DIR", ""),
        chunk_size=os.environ.get("CHUNK_SIZE", ""),
    )
