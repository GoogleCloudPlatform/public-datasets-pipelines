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

# import modules
import datetime
import fnmatch
import logging
import os
import pathlib
import re
import shutil
import zipfile as zip

import numpy as np
import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info(f"International Database (Country Names - Midyear Population, by Age and Sex) Delivery process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file_gs(source_url, source_file)

    data_names = [
        "source_file",
        "trip_id",
        "duration_sec",
        "start_date",
        "start_station_name",
        "start_station_terminal",
        "end_date",
        "end_station_name",
        "end_station_terminal",
        "bike_number",
        "subscription_type",
        "zip_code",
    ]

    data_dtypes = {
        "source_file": np.str_,
        "trip_id": np.int_,
        "duration_sec": np.int_,
        "start_date": np.str_,
        "start_station_name": np.str_,
        "start_station_terminal": np.int_,
        "end_date": np.str_,
        "end_station_name": np.str_,
        "end_station_terminal": np.str_,
        "bike_number": np.int_,
        "subscription_type": np.str_,
        "zip_code": np.str_,
    }

    process_source_file(
        str(source_file).replace(".csv", "_trip_data.csv"),
        str(target_file).replace(".csv", "_trip_data.csv"),
        data_names,
        data_dtypes,
        int(chunksize),
    )

    tripdata_filepath = str(target_file).replace(".csv", "_tripdata.csv")
    logging.info(f"Opening {tripdata_filepath}")
    df = pd.read_csv(
        tripdata_filepath,
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        sep="|",  # data column separator, typically ","
    )

    df.drop_duplicates(
        subset=["key_val"], keep="last", inplace=True, ignore_index=False
    )

    save_to_new_file(df, target_file, ",")
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(f"International Database (Country Names - Midyear Population, by Age and Sex) Delivery process completed")


def process_source_file(
    source_file: str, target_file: str, names: list, dtypes: dict, chunksize: int
) -> None:
    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=chunksize,  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=None,  # use when the data file does not contain a header
        names=names,
        dtype=dtypes,
        parse_dates=["start_date", "end_date"],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))


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


def add_key(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Adding key column")
    df["start_date_str"] = df["start_date"].apply(
        lambda x: re.sub("[^0-9.]", "", str(x))
    )
    df["key"] = df.apply(
        lambda x: str(x.start_date_str) + "-" + str(x.bike_number), axis=1
    )
    df["key_val"] = df["key"].replace("-", "")

    return df

def pool_files(src_dir: str, dest_dir: str, file_group_wildcard: str):
    logging.info(f"Pooling files *{file_group_wildcard}")
    if len(fnmatch.filter(os.listdir(src_dir), "*" + file_group_wildcard)) > 0:
        for src_file in fnmatch.filter(os.listdir(src_dir), "*" + file_group_wildcard):
            logging.info(f"Copying {src_dir}/{src_file} -> {dest_dir}/{src_file}")
            shutil.copyfile(f"{src_dir}/{src_file}", f"{dest_dir}/{src_file}")


def concatenate_files(
    target_file_path: str, dest_path: str, file_group_wildcard: str
) -> None:
    target_file_dir = os.path.split(str(target_file_path))[0]
    target_file_path = str(target_file_path).replace(".csv", "_" + file_group_wildcard)
    logging.info(f"Concatenating files {target_file_dir}/*{file_group_wildcard}")
    if os.path.isfile(target_file_path):
        os.unlink(target_file_path)
    for src_file_path in sorted(
        fnmatch.filter(os.listdir(dest_path), "*" + file_group_wildcard)
    ):
        src_file_path = dest_path + "/" + src_file_path
        with open(src_file_path, "r") as src_file:
            with open(target_file_path, "a+") as target_file:
                next(src_file)
                logging.info(
                    f"Reading from file {src_file_path}, writing to file {target_file_path}"
                )
                for line in src_file:
                    line = (
                        os.path.split(src_file_path)[1] + "," + line
                    )  # include the file source
                    target_file.write(line)


def listdirs(rootdir: str) -> list:
    rtn_list = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            rtn_list.append(d)
            for elem in listdirs(d):
                rtn_list.append(elem)
    return rtn_list


def download_url_files_from_list(url_list: str, dest_path: str):
    for url in url_list.split(","):
        url = url.replace('"', "").strip()
        dest_file = dest_path + "/" + os.path.split(url)[1]
        download_file_http(url, dest_file)
        if (
            url.find(".zip") > -1 or url.find(".gz") > -1 or url.find(".tar") > -1
        ) and (url.find("http") == 0 or url.find("gs:") == 0):
            unpack_file(dest_file, dest_path)
        else:
            logging.info(f"Parsing {dest_file} for decompression")


def resolve_date_format(
    df: pd.DataFrame, from_format: str, date_fields: list = []
) -> pd.DataFrame:
    logging.info("Resolving Date Format")
    for dt_fld in date_fields:
        df[dt_fld] = df[dt_fld].apply(lambda x: convert_dt_format(x, from_format))

    return df


def convert_dt_format(dt_str: str, from_format: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        dt_str = ""
    if len(dt_str.strip().split(" ")[1]) == 8:
        # if format of time portion is 00:00:00 then use 00:00 format
        dt_str = dt_str[:-3]
    if (len(dt_str.strip().split("-")[0]) == 4) and (
        len(from_format.strip().split("/")[0]) == 2
    ):
        # if the format of the date portion of the data is in YYYY-MM-DD format
        # and from_format is in MM-DD-YYYY then resolve this by modifying the from_format
        # to use the YYYY-MM-DD.  This resolves mixed date formats in files
        from_format = "%Y-%m-%d " + from_format.strip().split(" ")[1]

    return datetime.datetime.strptime(dt_str, from_format).strftime("%Y-%m-%d %H:%M:%S")


def location(longitude: str, latitude: str) -> str:
    if not longitude or not latitude:
        return ""
    else:
        return "POINT( " + longitude + " " + latitude + " )"


def generate_location(
    df: pd.DataFrame, geom_col: str, long_col: str, lat_col: str
) -> pd.DataFrame:
    logging.info(f"Generating location data column {geom_col}")
    df[geom_col] = df[[long_col, lat_col]].apply(
        lambda x, lat_col, long_col: location(str(x[long_col]), str(x[lat_col])),
        args=(lat_col, long_col),
        axis=1,
    )

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


def save_to_new_file(df, file_path, sep="|") -> None:
    logging.info(f"Saving to file {file_path} separator='{sep}'")
    df.to_csv(file_path, sep=sep, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info("Uploading to GCS {gcs_bucket} in {gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


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
        "nan_field_1",
        "nan_field_2",
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


def download_file_gs(source_url: str, source_file: pathlib.Path) -> None:
    with open(source_file, "wb+") as file_obj:
        storage.Client().download_blob_to_file(source_url, file_obj)


def remove_parenthesis_long_lat(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Remove parenthesis from latitude and longitude")
    df["latitude"].replace("(", "", regex=False, inplace=True)
    df["latitude"].replace(")", "", regex=False, inplace=True)
    df["longitude"].replace("(", "", regex=False, inplace=True)
    df["longitude"].replace(")", "", regex=False, inplace=True)

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


def gz_decompress(infile: str, tofile: str) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


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
