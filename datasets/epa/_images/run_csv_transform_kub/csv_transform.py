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
import fnmatch
import json
import logging
import os
import pathlib
import typing
import zipfile as zip

# import numpy
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    start_year: int,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    data_names: typing.List[str],
    data_dtypes: dict
) -> None:

    logging.info("Annual Summaries process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    dest_path = os.path.split(source_file)[0]
    end_year = (datetime.datetime.today().year - 2)
    download_url_files_from_year_range(source_url, start_year, end_year, dest_path, True, False)
    st_year = (datetime.datetime.today().year - 1)
    end_year = (datetime.datetime.today().year)
    download_url_files_from_year_range(source_url, st_year, end_year, dest_path, True, True)
    file_group_wildcard = os.path.split(source_url)[1].replace("_~year~.zip", "")
    source = concatenate_files(source_file, dest_path, file_group_wildcard, False, ",")
    target = source.replace(".csv", "_output.csv")

    key_list = ["state_code", "county_code", "site_num", "sample_duration", "pollutant_standard", "metric_used", "method_name", "address", "date_of_last_change"]
    process_source_file(
        source,
        target,
        data_names,
        # {},
        data_dtypes,
        int(chunksize),
        key_list
    )

    # trip_data_filepath = str(target_file).replace(".csv", "_trip_data.csv")
    # logging.info(f"Opening {trip_data_filepath}")
    # df_trip_data = pd.read_csv(
    #     trip_data_filepath,
    #     engine="python",
    #     encoding="utf-8",
    #     quotechar='"',  # string separator, typically double-quotes
    #     sep="|",  # data column separator, typically ","
    # )

    # tripdata_filepath = str(target_file).replace(".csv", "_tripdata.csv")
    # logging.info(f"Opening {tripdata_filepath}")
    # df_tripdata = pd.read_csv(
    #     tripdata_filepath,
    #     engine="python",
    #     encoding="utf-8",
    #     quotechar='"',  # string separator, typically double-quotes
    #     sep="|",  # data column separator, typically ","
    # )

    # logging.info("Dropping duplicate rows")
    # df = df_trip_data
    # df.drop_duplicates(
    #     subset=["key_val"], keep="last", inplace=True, ignore_index=False
    # )
    # df_tripdata.drop_duplicates(
    #     subset=["key_val"], keep="last", inplace=True, ignore_index=False
    # )

    # logging.info("Populating empty trip-id values")
    # df_tripdata["trip_id"] = df_tripdata["key_val"].str.replace("-", "")

    # logging.info("Creating indexes")
    # df.set_index("key", inplace=True)
    # df_tripdata.set_index("key", inplace=True)

    # logging.info("Merging data")
    # df = df.append(df_tripdata, sort=True)

    # logging.info("Creating subscriber_type_new")
    # df["subscriber_type_new"] = df.apply(
    #     lambda x: str(x.subscription_type)
    #     if not str(x.subscriber_type)
    #     else str(x.subscriber_type),
    #     axis=1,
    # )
    # df = df.drop(columns=["subscriber_type"])

    # logging.info("Resolving datatypes")
    # df["member_birth_year"] = df["member_birth_year"].fillna(0).astype(int)

    # df = rename_headers_output_file(df)
    # df = reorder_headers(df)

    # save_to_new_file(df, target_file, ",")
    # upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("Annual Summaries process completed")


def download_url_files_from_year_range(source_url: str, start_year: int, end_year: int, dest_path: str, remove_file: bool=False, continue_on_error: bool=False):
    # for yr in range(start_year, (datetime.datetime.today().year - 1), 1):
    for yr in range(start_year, end_year + 1, 1):
        src_url = source_url.replace("~year~", str(yr))
        dest_file = dest_path + "/source_" + os.path.split(src_url)[1]
        download_file_http(src_url, dest_file)
        unpack_file(dest_file, dest_path, "zip")
        if remove_file :
            os.remove(dest_file)


def download_file_http(source_url: str, source_file: pathlib.Path, continue_on_error: bool=False) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        with open(source_file, "wb") as f:
            for chunk in src_file:
                f.write(chunk)
    except:
        if not continue_on_error:
            logging.info(f"Unable to obtain {source_url}")
        else:
            logging.info(f"Unable to obtain {source_url}. Continuing execution.")


def process_source_file(
    source_file: str, target_file: str, names: list, dtypes: dict, chunksize: int, key_list: list
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
        keep_default_na=True,
        na_values=[' ']
        # parse_dates=["start_date", "end_date"],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0), key_list)


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool, key_list: list
) -> None:
    df = resolve_date_format(df, "%Y-%m-%d %H:%M")
    # df = add_key(df, key_list)
    save_to_new_file(df, file_path=str(target_file_batch), sep=",")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def add_key(df: pd.DataFrame, key_list: list) -> pd.DataFrame:
    logging.info(f"Adding key column(s) {key_list}")
    df["key"] = ""
    for key in key_list:
        df["key"] = df.apply(
            lambda x: str(x[key])
            if not str(x["key"])
            else str(x["key"]) + "-" + str(x[key]),
            axis=1,
        )
    df["key_val"] = df["key"]

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers output file")
    df = df[
        [
            "trip_id",
            "duration_sec",
            "start_date",
            "start_station_name",
            "start_station_id",
            "end_date",
            "end_station_name",
            "end_station_id",
            "bike_number",
            "zip_code",
            "subscriber_type",
            "subscription_type",
            "start_station_latitude",
            "start_station_longitude",
            "end_station_latitude",
            "end_station_longitude",
            "member_birth_year",
            "member_gender",
            "bike_share_for_all_trip",
            "start_station_geom",
            "end_station_geom",
        ]
    ]

    return df


def concatenate_files(
    target_file_path: str, dest_path: str, file_group_wildcard: str, incl_file_source_path: bool=False, separator: str=","
) -> str:
    target_file_dir = os.path.split(str(target_file_path))[0]
    target_file_path = str(target_file_path).replace(".csv", "_" + file_group_wildcard + ".csv")
    logging.info(f"Concatenating files {target_file_dir}/*{file_group_wildcard}")
    if os.path.isfile(target_file_path):
        os.unlink(target_file_path)
    for src_file_path in sorted(
        fnmatch.filter(os.listdir(dest_path), "*" + file_group_wildcard + "*")
    ):
        src_file_path = dest_path + "/" + src_file_path
        with open(src_file_path, "r") as src_file:
            with open(target_file_path, "a+") as target_file:
                next(src_file)
                logging.info(
                    f"Reading from file {src_file_path}, writing to file {target_file_path}"
                )
                for line in src_file:
                    if incl_file_source_path:
                        line = (
                            '"' + os.path.split(src_file_path)[1].strip() + '"' + separator + line
                        )  # include the file source
                    else:
                        line = (
                            line
                        )
                    target_file.write(line)

    return target_file_path


def listdirs(rootdir: str) -> list:
    rtn_list = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            rtn_list.append(d)
            for elem in listdirs(d):
                rtn_list.append(elem)
    return rtn_list


def resolve_date_format(
    df: pd.DataFrame, from_format: str
) -> pd.DataFrame:
    logging.info("Resolving Date Format")
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
	        logging.info(f"Resolving datetime on {col}")
	        df[col] = df[col].apply(lambda x: convert_dt_format(str(x), from_format))

    return df


def convert_dt_format(dt_str: str, from_format: str) -> str:
	# rtnval = ""
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        rtnval = ""
    elif len(dt_str.strip()) == 10:
        # if there is no time format
        rtnval = dt_str + ' 00:00:00'
    elif len(dt_str.strip().split(" ")[1]) == 8:
        # if format of time portion is 00:00:00 then use 00:00 format
        dt_str = dt_str[:-3]
        rtnval = datetime.datetime.strptime(dt_str, from_format).strftime("%Y-%m-%d %H:%M:%S")
    elif (len(dt_str.strip().split("-")[0]) == 4) and (
            len(from_format.strip().split("/")[0]) == 2
        ):
            # if the format of the date portion of the data is in YYYY-MM-DD format
            # and from_format is in MM-DD-YYYY then resolve this by modifying the from_format
            # to use the YYYY-MM-DD.  This resolves mixed date formats in files
            from_format = "%Y-%m-%d " + from_format.strip().split(" ")[1]
    else:
	    dt_str = ""

    # return datetime.datetime.strptime(dt_str, from_format).strftime("%Y-%m-%d %H:%M:%S")
    return rtnval


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


def unpack_file(infile: str, dest_path: str, compression_type: str = "zip") -> None:
    if os.path.exists(infile):
        if compression_type == "zip":
            logging.info(f"Unpacking {infile} to {dest_path}")
            with zip.ZipFile(infile, mode="r") as zipf:
                zipf.extractall(dest_path)
                zipf.close()
        else:
            logging.info(
                f"{infile} ignored as it is not compressed or is of unknown compression"
        )
    else:
        logging.info(f"{infile} not unpacked because it does not exist.")


def zip_decompress(infile: str, dest_path: str) -> None:
    logging.info(f"Unpacking {infile} to {dest_path}")
    with zip.ZipFile(infile, mode="r") as zipf:
        zipf.extractall(dest_path)
        zipf.close()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        start_year=int(os.environ["START_YEAR"]),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        data_names=json.loads(os.environ["DATA_NAMES"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
    )
