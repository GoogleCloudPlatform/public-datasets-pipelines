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

import gzip
import logging
import os
import pathlib

import numpy as np
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
):

    logging.info("NOAA Lightning Strikes By Year process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    source_file_zipped = str(source_file) + ".gz"
    download_file(source_url, source_file_zipped)
    gz_decompress(source_file_zipped, source_file)
    os.unlink(source_file_zipped)

    dtypes = {
        "DATE": np.str_,
        "LONGITUDE": np.float_,
        "LATITUDE": np.float_,
        "TOTAL_COUNT": np.int_,
    }

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=chunksz,  # size of batch data, in no. of records
        skiprows=3,
        sep=",",  # data column separator, typically ","
        header=None,  # use when the data file does not contain a header
        dtype=dtypes,  # use this when defining column and datatypes as per numpy
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("NOAA Lightning Strikes By Year process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = rename_headers(df)
    df = convert_date_from_int(df)
    df = generating_location(df)
    df = reorder_header(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


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


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Renaming Headers")
    df.columns = ["day_int", "centerlon", "centerlat", "number_of_strikes"]

    return df


def convert_date_from_int(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Converting dates from integers")
    df["day"] = (
        pd.to_datetime(
            (df["day_int"][:].astype("string") + "000000"), "raise", False, True
        ).astype("string")
        + " 00:00:00"
    )

    return df


def generating_location(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Generating location data")
    df["center_point"] = (
        "POINT("
        + df["centerlon"][:].astype("string")
        + " "
        + df["centerlat"][:].astype("string")
        + ")"
    )

    return df


def reorder_header(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering columns")
    df = df[["day", "number_of_strikes", "center_point"]]

    return df


def gz_decompress(infile: str, tofile: str) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
