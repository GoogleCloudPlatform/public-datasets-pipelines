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
import gzip
import logging
import os
import pathlib
from ftplib import FTP

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    # source_url            STRING          -> The full url of the source file to transform
    # ftp_host              STRING          -> The host IP of the ftp file (IP only)
    # ftp_dir               STRING          -> The remote working directory that the FTP file resides in (directory only)
    # ftp_filename          STRING          -> The name of the file to pull from the FTP site
    # source_file           PATHLIB.PATH    -> The (local) path pertaining to the downloaded source file
    # target_file           PATHLIB.PATH    -> The (local) target transformed file + filename
    # target_gcs_bucket     STRING          -> The target GCS bucket to place the output (transformed) file
    # target_gcs_path       STRING          -> The target GCS path ( within the GCS bucket ) to place the output (transformed) file

    logging.info("NOAA - GHCND By Year process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_source_file(source_url, source_file, ftp_host, ftp_dir, ftp_filename)

    names = ["id", "date", "element", "value", "mflag", "qflag", "sflag", "time"]

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=chunksz,
        header=None,
        names=names,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("NOAA - GHCND By Year process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = reorder_headers(df)
    df = filter_null_rows(df)
    df = source_convert_date_formats(df)
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


def download_source_file(
    source_url: str, source_file: str, ftp_host: str, ftp_dir: str, ftp_filename
) -> None:
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    source_file_zipped = str(source_file) + ".gz"
    download_file_ftp(ftp_host, ftp_dir, ftp_filename, source_file_zipped, source_url)
    gz_decompress(source_file_zipped, source_file)


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[["id", "date", "element", "value", "mflag", "qflag", "sflag", "time"]]
    return df


def gz_decompress(infile: str, tofile: str) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def filter_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Removing rows with blank id's..")
    df = df[df.id != ""]
    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or dt_str == "nan":
        return str(dt_str)
    else:
        return str(
            datetime.datetime.strptime(str(dt_str), "%Y%m%d")
            .date()
            .strftime("%Y-%m-%d")
        )


def source_convert_date_formats(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Converting Date Format..")
    df["date"] = df["date"].apply(convert_dt_format)
    return df


def save_to_new_file(df, file_path) -> None:
    logging.info(f"Saving to target file.. {file_path}")
    df.to_csv(file_path, float_format="%.0f", index=False)


def download_file_ftp(
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    local_file: pathlib.Path,
    source_url: str,
) -> None:

    # ftp_host      -> host ip (eg. 123.123.0.1)
    # ftp_dir       -> working directory in ftp host where file is located
    # ftp_filename  -> filename of FTP file to download
    # source_file   -> local file (including path) to create containing ftp content

    logging.info(f"Downloading {source_url} into {local_file}")
    ftp_conn = FTP(ftp_host)
    ftp_conn.login("", "")
    ftp_conn.cwd(ftp_dir)
    ftp_conn.encoding = "utf-8"

    dest_file = open(local_file, "wb")
    ftp_conn.encoding = "utf-8"
    ftp_conn.retrbinary(
        cmd=f"RETR {ftp_filename}",
        callback=dest_file.write,
        blocksize=1024,
        rest=None,
    )
    ftp_conn.quit()
    dest_file.close()


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        ftp_host=os.environ["FTP_HOST"],
        ftp_dir=os.environ["FTP_DIR"],
        ftp_filename=os.environ["FTP_FILENAME"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
