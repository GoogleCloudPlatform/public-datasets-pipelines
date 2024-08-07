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
import subprocess

import pandas as pd


def main(
    source_url: str,
    gcs_bucket: str,
    csv_headers: list,
    csv_gcs_path: str,
    non_na_columns: list,
    data_dtypes: dict,
    chunksize: int,
) -> None:
    logging.info(
        f'Chicago Taxi Trips Dataset pipeline process started at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )
    # Stage the datafile
    gcs_datafile = f"gs://{gcs_bucket}/{csv_gcs_path}"
    logging.info(f"Downloading source file from {source_url}.")
    cmd = f"wget -q -O - {source_url} |gcloud storage cp - {gcs_datafile}"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    ps.communicate()
    logging.info(f"Reading and processing source file from {gcs_datafile}.")
    file_batch_nbr = 1
    batch_filename = f"./output/taxi_trips_{str.zfill(str(file_batch_nbr), 10)}"
    for i, chunk in enumerate(
        pd.read_csv(
            gcs_datafile,
            chunksize=chunksize,
            names=csv_headers,
            skiprows=1,
            dtype=data_dtypes,
        )
    ):
        batch_num_pad = str(i + 1).zfill(10)
        batch_path = os.path.join(os.path.dirname(gcs_datafile), "batch")
        batch_filename = "taxi_trips_"
        batch_fullpath = os.path.join(
            batch_path, f"{batch_filename}{batch_num_pad}.csv"
        )
        logging.info(f"Processing chunk #{batch_num_pad} and writing to {batch_fullpath}")
        chunk.dropna(subset=non_na_columns, inplace=True)
        chunk["trip_start_timestamp"] = pd.to_datetime(
            chunk["trip_start_timestamp"], format="%m/%d/%Y %I:%M:%S %p"
        )
        chunk["trip_end_timestamp"] = pd.to_datetime(
            chunk["trip_end_timestamp"], format="%m/%d/%Y %I:%M:%S %p"
        )
        chunk.to_csv(batch_fullpath, index=False)
    logging.info(
        f'Chicago Taxi Trips Dataset pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_url=os.environ.get("SOURCE_URL", ""),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        csv_gcs_path=os.environ.get("CSV_GCS_PATH", ""),
        csv_headers=json.loads(os.environ.get("CSV_HEADERS", "{}")),
        non_na_columns=json.loads(os.environ.get("NON_NA_COLUMNS", "[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", "{}")),
        chunksize=int(os.environ.get("CHUNKSIZE", "1000000")),
    )
