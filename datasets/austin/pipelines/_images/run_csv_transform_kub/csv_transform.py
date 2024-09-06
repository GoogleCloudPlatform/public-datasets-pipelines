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
import math
import os
import pathlib
import typing

import pandas as pd
from google.cloud import storage


def main(
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    input_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:
    """
    Description:
        Main process function
    Args:
        pipeline_name: Name of the pipeline being executed.
        source_url: GCS bucket used to acquire the source file.
        chunksize: Number of rows in the source file to chunk when processing.
        source_file: Local path to download the source file to for prrocessing.
        target_gcs_bucket: GCS Bucket used to manage source and output files.
        target_gcs_path: GCS Bucket Path to write the target batch files to for later loading.
        project_id: GCP Project ID used to access the bucket containing the staged source file.
        date_format_list: List of tuples pertaining to the following metadata:
            field/column: Column containing the date field to transform the date value formats within.
            in_format: Format of the dates in the source file.
            out_format: Format of the dates to write to.  Typically "%Y-%m-%d %H:%M:%S"
        int_cols_list: List of columns to convert values to integers when transforming to output data.
        remove_newlines_cols_list: List of columns to replace all newlines in with spaces.
        null_rows_list: List of columns that are filtered out if the rows contain nulls in those columns.
            Typically to prevent null index violation on required fields such as a unique key.
        input_headers: Defines the names of the columns in the source file in ordinal position.
        data_dtypes: Defines the datatypes of each source file column in its ordinal position.
        rename_headers_list: Dictionary list specifying columns to convert headers to during the column renaming process.
        reorder_headers_list: List of columns in the new ordinal position to use in order to write the output file.
    """
    logging.info(f"{pipeline_name} process started")
    logging.info("creating 'files' folder")
    pathlib.Path(f"./{os.path.dirname(source_file)}").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        pipeline_name=pipeline_name,
        source_url=source_url,
        chunksize=chunksize,
        source_file=source_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        project_id=project_id,
        date_format_list=date_format_list,
        int_cols_list=int_cols_list,
        remove_newlines_cols_list=remove_newlines_cols_list,
        null_rows_list=null_rows_list,
        input_headers=input_headers,
        data_dtypes=data_dtypes,
        rename_headers_list=rename_headers_list,
        reorder_headers_list=reorder_headers_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    source_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    input_headers: typing.List[str],
    data_dtypes: dict,
    rename_headers_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:
    """
    Description:
        Stage the source file locally and execute the transform process.
    """
    download_file_gcs(
        project_id=project_id,
        source_location=source_url,
        destination_folder=os.path.dirname(source_file),
    )
    process_source_file(
        pipeline_name=pipeline_name,
        source_file=source_file,
        chunksize=chunksize,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        input_headers=input_headers,
        dtypes=data_dtypes,
        date_format_list=date_format_list,
        int_cols_list=int_cols_list,
        remove_newlines_cols_list=remove_newlines_cols_list,
        null_rows_list=null_rows_list,
        reorder_headers_list=reorder_headers_list,
        rename_headers_list=rename_headers_list,
    )


def download_file_gcs(
    project_id: str, source_location: str, destination_folder: str
) -> None:
    """
    Description:
        Download a file from GCS to local storage.
    """
    object_name = os.path.basename(source_location)
    dest_object = f"{destination_folder}/{object_name}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def process_source_file(
    pipeline_name: str,
    source_file: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    dtypes: dict,
    chunksize: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
) -> None:
    """
    Description:
        Process the source file.
    """
    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=1,  # use when the data file does not contain a header
        names=input_headers,
        dtype=dtypes,
        keep_default_na=True,
        na_values=[" "],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file = str(source_file).replace("source.csv", "output.csv")
            target_file_batch = str(target_file).replace(
                ".csv", f"-{str(chunk_number).zfill(10)}.csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df=df,
                pipeline_name=pipeline_name,
                target_file_batch=target_file_batch,
                target_gcs_bucket=target_gcs_bucket,
                target_gcs_path=target_gcs_path,
                date_format_list=date_format_list,
                int_cols_list=int_cols_list,
                remove_newlines_cols_list=remove_newlines_cols_list,
                null_rows_list=null_rows_list,
                reorder_headers_list=reorder_headers_list,
                rename_headers_list=rename_headers_list,
            )


def process_chunk(
    df: pd.DataFrame,
    pipeline_name: str,
    target_file_batch: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    date_format_list: typing.List[str],
    int_cols_list: typing.List[str],
    remove_newlines_cols_list: typing.List[str],
    null_rows_list: typing.List[str],
    reorder_headers_list: typing.List[str],
    rename_headers_list: dict,
) -> None:
    """
    Description:
        For each chunk of source data, process and transform.
        The data chunks are then written to transformed output files and posted to the GCS batch folder for loading
    """
    logging.info(f"Processing Batch {target_file_batch} started")
    if pipeline_name == "Austin 311 Service Requests By Year":
        df = rename_headers(df=df, rename_headers_list=rename_headers_list)
        for col in remove_newlines_cols_list:
            logging.info(f"Removing newlines from {col}")
            df[col] = (
                df[col]
                .replace({r"\s+$": "", r"^\s+": ""}, regex=True)
                .replace(r"\n", " ", regex=True)
            )
        df = filter_null_rows(df, null_rows_list)
        for int_col in int_cols_list:
            df[int_col] = df[int_col].fillna(0).astype("int32")
        df = format_date_time(df=df, date_format_list=date_format_list)
        df = reorder_headers(df=df, reorder_headers_list=reorder_headers_list)
    elif pipeline_name == "Austin Bikeshare Stations":
        df = rename_headers(df=df, rename_headers_list=rename_headers_list)
        df = format_date_time(df=df, date_format_list=date_format_list)
        df = filter_null_rows(df, null_rows_list)
        df["city_asset_number"] = df["city_asset_number"].apply(
            convert_to_integer_string
        )
        df["number_of_docks"] = df["number_of_docks"].apply(convert_to_integer_string)
        df["footprint_length"] = df["footprint_length"].apply(convert_to_integer_string)
        df["council_district"] = df["council_district"].apply(convert_to_integer_string)
        df["footprint_width"] = df["footprint_width"].apply(resolve_nan)
        df["location"] = df["location"].apply(
            lambda x: "" if not str(x) else f"POINT{x.replace(',', '')}"
        )
        df = reorder_headers(df=df, reorder_headers_list=reorder_headers_list)
    elif pipeline_name == "Austin Bikeshare Trips":
        df = rename_headers(df=df, rename_headers_list=rename_headers_list)
        df = filter_null_rows(df, null_rows_list)
        logging.info("Merging date/time into start_time")
        df["start_time"] = df["time"] + " " + df["checkout_time"]
        df = format_date_time(df=df, date_format_list=date_format_list)
        df = reorder_headers(df=df, reorder_headers_list=reorder_headers_list)
    else:
        logging.info("Pipeline Not Recognized.")
        return None
    save_to_new_file(df=df, file_path=str(target_file_batch), sep="|")
    # Free up memory from the pandas dataframe
    del df
    # write batch file to GCS bucket for loading, removing the local batch file copy as clean-up.
    upload_file_to_gcs(
        file_path=str(target_file_batch),
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=os.path.join(
            target_gcs_path, os.path.basename(str(target_file_batch))
        ),
        remove_file=True,
    )
    logging.info(f"Processing Batch {target_file_batch} completed")


def resolve_nan(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(input)
    return str_val.replace("None", "")


def convert_to_integer_string(input: typing.Union[str, float]) -> str:
    str_val = ""
    if not input or (str(input) == "nan"):
        str_val = ""
    else:
        str_val = str(int(float(input)))
    return str_val


def format_date_time(
    df: pd.DataFrame, date_format_list: typing.List[typing.List]
) -> pd.DataFrame:
    """
    Description:
        Format date/time values in a column within a DataFrame.
    """
    logging.info("Formatting Date/time values")
    for dt_list_item in date_format_list:
        col_nm = dt_list_item[0]
        in_fmt = dt_list_item[1]
        out_fmt = dt_list_item[2]
        logging.info(f"Converting Date Format {col_nm}")
        df[col_nm] = df[col_nm].apply(
            lambda x: ""
            if (not str(x) or str(x) == "nan")
            else datetime.datetime.strptime(str(x), in_fmt).strftime(out_fmt)
        )
    return df


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    """
    Description:
        Rename the headers of columns within a dataframe.
    """
    logging.info("Renaming Headers")
    return df.rename(columns=rename_headers_list)


def reorder_headers(
    df: pd.DataFrame, reorder_headers_list: typing.List[str]
) -> pd.DataFrame:
    """
    Description:
        Reorder the DataFrame columns/headers.
    """
    logging.info("Reordering headers..")
    return df[reorder_headers_list]


def filter_null_rows(
    df: pd.DataFrame, null_rows_list: typing.List[str]
) -> pd.DataFrame:
    """
    Description:
        Filter out rows in the DataFrame where the value of the specified column is null.
    """
    for col in null_rows_list:
        df = df[df[col] != ""]
    return df


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    """
    Description:
        Write the DataFrame to a pipe-delimited file.
    """
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def upload_file_to_gcs(
    file_path: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    remove_file: bool = False,
) -> None:
    """
    Description:
        Upload the file to GCS.
    """
    if os.path.exists(file_path):
        storage_client = storage.Client()
        bucket = storage_client.bucket(target_gcs_bucket)
        blob = bucket.blob(target_gcs_path)
        blob.upload_from_filename(file_path)
        if remove_file:
            os.unlink(file_path)
    else:
        logging.info(
            f"Cannot upload file to gs://{target_gcs_bucket}/{target_gcs_path} as it does not exist."
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", r"{}")),
        int_cols_list=json.loads(os.environ.get("INT_COLS_LIST", r"[]")),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"{}")),
        remove_newlines_cols_list=json.loads(
            os.environ.get("REMOVE_NEWLINES_COLS_LIST", r"[]")
        ),
        null_rows_list=json.loads(os.environ.get("NULL_ROWS_LIST", r"[]")),
        input_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
    )
