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

# import fnmatch
import json
import logging
import os
import pathlib
import typing
import zipfile as zip

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
    data_names: typing.List[str],
    data_dtypes: dict,
) -> None:

    logging.info(
        "Food and Drug Administration (FDA) - Food Enforcement process started"
    )

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    dest_path = os.path.split(source_file)[0]
    source_zip_file = dest_path + "/" + os.path.split(source_url)[1]
    source_json_file = source_zip_file.replace(".zip", "")

    download_file_http(source_url, source_zip_file, False)
    unpack_file(source_zip_file, dest_path, "zip")
    convert_json_to_csv(source_json_file, source_file)

    process_source_file(
        source_file,
        target_file,
        data_names,
        data_dtypes,
        int(chunksize),  # , key_list=[]
    )

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        "Food and Drug Administration (FDA) - Food Enforcement process completed"
    )


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
        sep="|",  # data column separator, typically ","
        header=None,  # use when the data file does not contain a header
        names=names,
        skiprows=1,
        dtype=dtypes,
        keep_default_na=True,
        na_values=[" "]
        # parse_dates=["start_date", "end_date"],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df,
                target_file_batch,
                target_file,
                (not chunk_number == 0),  # , key_list
            )


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = trim_whitespace(df)
    date_col_list = [
        "center_classification_date",
        "report_date",
        "termination_date",
        "recall_initiation_date",
    ]
    df = resolve_date_format(df, date_col_list, "%Y%m%d", "%Y-%m-%d", True)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def resolve_date_format(
    df: pd.DataFrame,
    date_col_list: list,
    from_format: str,
    to_format: str = "%Y-%m-%d %H:%M:%S",
    is_date: bool = False,
) -> pd.DataFrame:
    logging.info("Resolving Date Format")
    for col in date_col_list:
        logging.info(f"Resolving datetime on {col}")
        df[col] = df[col].apply(
            lambda x: convert_dt_format(str(x), from_format, to_format, is_date)
        )

    return df


def convert_dt_format(
    dt_str: str, from_format: str, to_format: str, is_date: bool
) -> str:
    rtnval = "<initial_value>"
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        rtnval = ""
    elif len(dt_str.strip()) == 10:
        # if there is no time format
        rtnval = dt_str + " 00:00:00"
    elif (
        is_date
    ):  # and from_format == "%Y%m%d" and to_format == "%Y-%m-%d") or (len(dt_str.strip()) == 8):
        # if there is only a date in YYYYMMDD format then add dashes
        rtnval = (
            dt_str.strip()[:4] + "-" + dt_str.strip()[4:6] + "-" + dt_str.strip()[6:8]
        )
    elif len(dt_str.strip().split(" ")[1]) == 8:
        # if format of time portion is 00:00:00 then use 00:00 format
        dt_str = dt_str[:-3]
        rtnval = datetime.datetime.strptime(dt_str, from_format).strftime(to_format)
    elif (len(dt_str.strip().split("-")[0]) == 4) and (
        len(from_format.strip().split("/")[0]) == 2
    ):
        # if the format of the date portion of the data is in YYYY-MM-DD format
        # and from_format is in MM-DD-YYYY then resolve this by modifying the from_format
        # to use the YYYY-MM-DD.  This resolves mixed date formats in files
        from_format = "%Y-%m-%d " + from_format.strip().split(" ")[1]
    else:
        dt_str = "<blank>"

    # return datetime.datetime.strptime(dt_str, from_format).strftime("%Y-%m-%d %H:%M:%S")
    return rtnval


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Trimming whitespace")
    for col in df.columns:
        col_dtype = df[col].dtype
        if col_dtype == "object":
            logging.info(f"Trimming whitespace on {col}")
            df[col] = df[col].apply(lambda x: str(x).strip())

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Re-ordering Headers")
    df = df[
        [
            "classification",
            "center_classification_date",
            "report_date",
            "postal_code",
            "termination_date",
            "recall_initiation_date",
            "recall_number",
            "city",
            "event_id",
            "distribution_pattern",
            "recalling_firm",
            "voluntary_mandated",
            "state",
            "reason_for_recall",
            "initial_firm_notification",
            "status",
            "product_type",
            "country",
            "product_description",
            "code_info",
            "address_1",
            "address_2",
            "product_quantity",
            "more_code_info",
        ]
    ]

    return df


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


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


def download_file_http(
    source_url: str, source_file: pathlib.Path, continue_on_error: bool = False
) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        with open(source_file, "wb") as f:
            for chunk in src_file:
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        if e == requests.exceptions.HTTPError:
            err_msg = "A HTTP error occurred."
        elif e == requests.exceptions.Timeout:
            err_msg = "A HTTP timeout error occurred."
        elif e == requests.exceptions.TooManyRedirects:
            err_msg = "Too Many Redirects occurred."
        if not continue_on_error:
            logging.info(f"{err_msg} Unable to obtain {source_url}")
            raise SystemExit(e)
        else:
            logging.info(
                f"{err_msg} Unable to obtain {source_url}. Continuing execution."
            )


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


def convert_json_to_csv(source_file_json: str, source_file_csv: str) -> None:
    logging.info(f"Converting JSON file {source_file_json} to {source_file_csv}")
    f = open(
        source_file_json.strip(),
    )
    json_data = json.load(f)
    df = pd.DataFrame(json_data["results"])
    df.to_csv(source_file_csv, index=False, sep="|", quotechar='"', encoding="utf-8")


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
        data_names=json.loads(os.environ["DATA_NAMES"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
    )
