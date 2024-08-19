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

import pandas as pd


def main(
    source_bucket: str,
    source_object: str,
    chunksize: str,
    csv_headers: list,
    data_dtypes: list,
) -> None:
    logging.info("Hacker News process started at ")
    gcs_datafile = f"gs://{source_bucket}/{source_object}"
    logging.info(f"Reading and processing source file from {gcs_datafile}.")
    for i, chunk in enumerate(
        pd.read_csv(
            gcs_datafile,
            chunksize=int(chunksize),
            names=csv_headers,
            skiprows=1,
            dtype=data_dtypes,
        )
    ):
        batch_num_pad = str(i + 1).zfill(10)
        batch_path = os.path.join(os.path.dirname(gcs_datafile), "batch")
        batch_filename = "hacker_news"
        batch_fullpath = os.path.join(
            batch_path, f"{batch_filename}_{batch_num_pad}.csv"
        )
        logging.info(
            f"Processing chunk #{batch_num_pad} and writing to {batch_fullpath}"
        )
        chunk = chunk.replace("\n", "", regex=True)
        chunk = chunk.replace("\r", "", regex=True)
        chunk.to_csv(batch_fullpath, index=False)
    logging.info(
        f'Chicago Taxi Trips Dataset pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_bucket=os.environ.get("SOURCE_GCS_BUCKET", ""),
        source_object=os.environ.get("SOURCE_GCS_OBJECT", ""),
        chunksize=os.environ.get("CHUNKSIZE", "1000000"),
        csv_headers=json.loads(os.environ["CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
    )
