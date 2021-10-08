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
import os
import pathlib
import tarfile as tf
import zipfile as zip
from subprocess import PIPE, Popen

import numpy as pd
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url_http: str,
    source_url_gs: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("San Francisco - Bikeshare Trips process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    dest_path = os.path.split(source_file)[0]
    download_url_files_from_list(source_url_http, dest_path)
    download_url_files_from_list(source_url_gs, dest_path)


def download_url_files_from_list(url_list: str, dest_path: str):
    for url in url_list.splitlines():
        url = url.replace('"', '').strip()
        dest_file = dest_path + '/' + os.path.split(url)[1]
        if url.find("http") == 0:
            download_file_http(url, dest_file)
        elif url.find("gs:") == 0:
            download_file_gs(url, dest_file)
        else:
            logging.info(f"invalid URL")
        if (url.find(".zip") > -1 \
            or url.find(".gz") > -1 \
            or url.find(".tar") > -1) \
            and (url.find("http") == 0 \
                or url.find("gs:") == 0):
            unpack_file(dest_file, dest_path)
        else:
            logging.info(f"Parsing {dest_file} for decompression")


    # for src_url_http in source_url_http.splitlines():
    #     src_url_http = src_url_http.replace('"', '').strip()
    #     src_file_http = os.path.split(source_file)[0] + '/' + os.path.split(src_url_http)[1]
    #     download_file_http(src_url_http, src_file_http)
    #     if src_file_http.find(".zip") > -1 \
    #         or src_file_http.find(".gz") > -1 \
    #         or src_file_http.find(".tar") > -1:
    #         unpack_file(src_file_http, os.path.split(source_file)[0])
    #     else:
    #         logging.info(f"Parsing {src_file_http}")

    # for src_url_gs in source_url_gs.splitlines():
    #     src_url_gs = src_url_gs.replace('"', '').strip()
    #     src_file_gs = os.path.split(source_file)[0] + '/' + os.path.split(src_url_http)[1]
    #     download_file_http(src_url_http, src_file_http)
    #     if src_file_http.find(".zip") > -1 \
    #         or src_file_http.find(".gz") > -1 \
    #         or src_file_http.find(".tar") > -1:
    #         unpack_file(src_file_http, os.path.split(source_file)[0])
    #     else:
    #         logging.info(f"Parsing {src_file_http}")


    # import pdb;pdb.set_trace()

    # download_file_gs(source_url, source_file)
    #
    # dtypes = {
    #     "source_file_field_1": np.int_,
    #     "source_file_field_2": np.str_,
    # }
    # parse_dates = [
    #     "source_file_date_field_1",
    #     "source_file_date_field_2",
    # ]

    # chunksz = int(chunksize)

    # logging.info(f"Opening batch file {source_file}")
    # with pd.read_csv(
    #     source_file,                # path to main source file to load in batches
    #     engine="python",
    #     encoding="utf-8",
    #     quotechar='"',              # string separator, typically double-quotes
    #     chunksize=chunksz,          # size of batch data, in no. of records
    #     sep=',',                    # data column separator, typically ","
    #     header=None,                # use when the data file does not contain a header
    #     dtype=dtypes,               # use this when defining column and datatypes as per numpy
    #     parse_dates=parse_dates,
    # ) as reader:
    #     for chunk_number, chunk in enumerate(reader):
    #         logging.info(f"Processing batch {chunk_number}")
    #         target_file_batch = str(target_file).replace(
    #             ".csv", "-" + str(chunk_number) + ".csv"
    #         )
    #         df = pd.DataFrame()
    #         df = pd.concat([df, chunk])
    #         process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    # upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    # logging.info(f"San Francisco - Bikeshare Trips process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = extract_columns(df)
    df = rename_headers(df)
    df = remove_empty_key_rows(df)
    df = strip_whitespace(df)
    df = remove_nan_cols(df)
    df = resolve_date_format(df)
    df = remove_parenthesis_long_lat(df)
    df = generate_location(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not(skip_header))


def extract_columns(df_filedata: pd.DataFrame) -> pd.DataFrame:
    # Example:
    # ZZZ99999999  17.1167  -61.7833 TMAX 1949 1949
    col_ranges = {
        "id": slice(0, 11),             # LENGTH: 12  EXAMPLE ID:  123456789999
        "latitude": slice(12, 20),      # LENGTH:  9  EXAMPLE LAT: -31.0123
        "longitude": slice(21, 30),     # LENGTH: 10  EXAMPLE LON: -31.0123
        "element": slice(31, 35),       # LENGTH:  5  EXAMPLE ELE: ZZZZ
        "firstyear": slice(36, 40),     # LENGTH:  5  EXAMPLE FIRSTYEAR: 1901
        "lastyear": slice(41, 45),      # LENGTH:  5  EXAMPLE LASTYEAR: 1902
    }

    df = pd.DataFrame()

    def get_column(col_val: str, col_name: str) -> str:
        return col_val.strip()[col_ranges[col_name]].strip()

    for col_name in col_ranges.keys():
        df[col_name] = df_filedata["textdata"].apply(get_column, args=(col_name,))

    # remove the incidental header
    df = df[df["id"] != "textdata"]

    return df


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    header_names = {
        "Field 1": "New Name Field 1",
        "Field 2": "New Name Field 2",
    }
    df = df.rename(columns=header_names)

    return df


def remove_empty_key_rows(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Remove rows with empty keys")
    df = df[df["unique_key"] != ""]


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Strip Whitespace")
    ws_fields = [
        "field1",
        "field2",
    ]

    for ws_fld in ws_fields:
        df[ws_fld] = df[ws_fld].apply(lambda x: str(x).strip())

    return df


def remove_nan(dt_str: str) -> int:
    if not dt_str or str(dt_str) == "nan":
        return int()
    else:
        return int(dt_str)


def remove_nan_cols(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving NaN data")
    cols = {
        "count_qualified",
        "existing_installs_count",
        "number_of_panels_n",
        "number_of_panels_s",
        "number_of_panels_e",
        "number_of_panels_w",
        "number_of_panels_f",
        "number_of_panels_median",
        "number_of_panels_total",
    }

    for col in cols:
        df[col] = df[col].apply(remove_nan)

    return df


def resolve_date_format(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving Date Format")
    date_fields = [
        "datefield1",
        "datefield2",
    ]

    for dt_fld in date_fields:
        df[dt_fld] = df[dt_fld].apply(convert_dt_format)

    return df

def convert_dt_format(dt_str: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif (
        dt_str.strip()[2] == "/"
    ):  # if there is a '/' in 3rd position, then we have a date format mm/dd/yyyy
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def remove_parenthesis_long_lat(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Remove parenthesis from latitude and longitude")
    df["latitude"].replace("(", "", regex=False, inplace=True)
    df["latitude"].replace(")", "", regex=False, inplace=True)
    df["longitude"].replace("(", "", regex=False, inplace=True)
    df["longitude"].replace(")", "", regex=False, inplace=True)

    return df


def generate_location(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Generating location data")
    df["center_point"] = (
        "POINT( "
        + df["lng_avg"].map(str)
        + " "
        + df["lat_avg"].map(str)
        + " )"
    )

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[
        [
            "field1",
            "field2",
        ]
    ]

    return df


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


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


def download_file_http(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    src_file = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in src_file:
            f.write(chunk)


def download_file_gs(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    process = Popen(
        ["gsutil", "cp", source_url, source_file], stdout=PIPE, stderr=PIPE
    )
    process.communicate()


def unpack_file(infile: str, dest_path: str, compression_type: str='zip') -> None:
    if compression_type == 'gz':
        to_file = dest_path + "/" + os.path.split(infile)[1]
        logging.info(f"Unpacking {infile} to {to_file}")
        with open(infile, "rb") as inf, open(to_file, "w", encoding="utf8") as tof:
            decom_str = gzip.decompress(inf.read()).decode("utf-8")
            tof.write(decom_str)
    elif compression_type == 'tar':
        logging.info(f"Unpacking {infile} to {dest_path}")
        with tf.open(name=infile, mode='r') as tar:
            tar.extractall(dest_path)
            tar.close()
    elif compression_type == 'zip':
        logging.info(f"Unpacking {infile} to {dest_path}")
        with zip.ZipFile(infile, mode='r') as zipf:
            zipf.extractall(dest_path)
            zipf.close()
    else:
        logging.info(f"{infile} ignored as it is not compressed or is of unknown compression")


def zip_decompress(infile: str, dest_path: str) -> None:
    logging.info(f"Unpacking {infile} to {dest_path}")
    with zip.ZipFile(infile, mode='r') as zipf:
        zipf.extractall(dest_path)
        zipf.close()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url_http=os.environ["SOURCE_URL_HTTP"],
        source_url_gs=os.environ["SOURCE_URL_GS"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
