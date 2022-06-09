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

import csv
import datetime
import ftplib
import gzip
import json
import logging
import os
import pathlib
import re
import time
import typing
from urllib.request import Request, urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    ftp_host: str,
    ftp_dir: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    ftp_batch_size: str,
    ftp_batch_sleep_time: str,
    full_data_load: str,
    start_year: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str],
    slice_column_list: dict,
    regex_list: dict,
    rename_headers_list: dict,
    remove_source_file: str,
    delete_target_file: str,
    number_of_header_rows: str,
    int_date_list: typing.List[str],
    gen_location_list: dict,
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        pipeline_name=pipeline_name,
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        ftp_host=ftp_host,
        ftp_dir=ftp_dir,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        drop_dest_table=drop_dest_table,
        input_field_delimiter=input_field_delimiter,
        ftp_batch_size=ftp_batch_size,
        ftp_batch_sleep_time=ftp_batch_sleep_time,
        full_data_load=full_data_load,
        start_year=start_year,
        input_csv_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        reorder_headers_list=reorder_headers_list,
        null_rows_list=null_rows_list,
        date_format_list=date_format_list,
        slice_column_list=slice_column_list,
        regex_list=regex_list,
        rename_headers_list=rename_headers_list,
        remove_source_file=(remove_source_file == "Y"),
        delete_target_file=(delete_target_file == "Y"),
        number_of_header_rows=int(number_of_header_rows),
        int_date_list=int_date_list,
        gen_location_list=gen_location_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    pipeline_name: str,
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    ftp_host: str,
    ftp_dir: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    ftp_batch_size: str,
    ftp_batch_sleep_time: str,
    full_data_load: str,
    start_year: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str],
    slice_column_list: dict,
    regex_list: dict,
    remove_source_file: bool,
    rename_headers_list: dict,
    delete_target_file: bool,
    number_of_header_rows: int,
    int_date_list: typing.List[str],
    gen_location_list: dict,
) -> None:
    if pipeline_name == "GHCND by year":
        if full_data_load == "N":
            start = str(datetime.datetime.now().year - 6)
        else:
            start = start_year
        ftp_batch = 1
        for yr in range(int(start), datetime.datetime.now().year + 1):
            yr_str = str(yr)
            source_zipfile = str.replace(str(source_file), ".csv", f"_{yr_str}.csv.gz")
            source_file_unzipped = str.replace(str(source_zipfile), ".csv.gz", ".csv")
            target_file_year = str.replace(str(target_file), ".csv", f"_{yr_str}.csv")
            destination_table_year = f"{destination_table}_{yr_str}"
            source_url_year = str.replace(source_url, ".csv.gz", f"{yr_str}.csv.gz")
            target_gcs_path_year = str.replace(
                target_gcs_path, ".csv", f"_{yr_str}.csv"
            )
            if ftp_batch == int(ftp_batch_size):
                logging.info("Sleeping...")
                time.sleep(int(ftp_batch_sleep_time))
                ftp_batch = 1
            else:
                ftp_batch += 1
            download_file_ftp(
                ftp_host=ftp_host,
                ftp_dir=ftp_dir,
                ftp_filename=f"{yr_str}.csv.gz",
                local_file=source_zipfile,
                source_url=source_url_year,
            )
            gz_decompress(
                infile=source_zipfile, tofile=source_file_unzipped, delete_zipfile=True
            )
            process_and_load_table(
                source_file=source_file_unzipped,
                target_file=target_file_year,
                pipeline_name=pipeline_name,
                source_url=source_url_year,
                chunksize=chunksize,
                project_id=project_id,
                dataset_id=dataset_id,
                destination_table=destination_table_year,
                target_gcs_bucket=target_gcs_bucket,
                target_gcs_path=target_gcs_path_year,
                schema_path=schema_path,
                drop_dest_table=drop_dest_table,
                input_field_delimiter=input_field_delimiter,
                input_csv_headers=input_csv_headers,
                data_dtypes=data_dtypes,
                reorder_headers_list=reorder_headers_list,
                null_rows_list=null_rows_list,
                date_format_list=date_format_list,
                slice_column_list=slice_column_list,
                regex_list=regex_list,
                rename_headers_list=rename_headers_list,
                remove_source_file=remove_source_file,
                delete_target_file=delete_target_file,
                int_date_list=int_date_list,
                gen_location_list=gen_location_list,
            )
    if pipeline_name in [
        "GHCND countries",
        "GHCND inventory",
        "GHCND states",
        "GHCND stations",
        "GSOD stations",
    ]:
        ftp_filename = os.path.split(source_url)[1]
        download_file_ftp(ftp_host, ftp_dir, ftp_filename, source_file, source_url)
        if number_of_header_rows > 0:
            remove_header_rows(source_file, number_of_header_rows=number_of_header_rows)
        else:
            pass
        process_and_load_table(
            source_file=source_file,
            target_file=target_file,
            pipeline_name=pipeline_name,
            source_url=source_url,
            chunksize=chunksize,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            schema_path=schema_path,
            drop_dest_table=drop_dest_table,
            input_field_delimiter=input_field_delimiter,
            input_csv_headers=input_csv_headers,
            data_dtypes=data_dtypes,
            reorder_headers_list=reorder_headers_list,
            null_rows_list=null_rows_list,
            date_format_list=date_format_list,
            slice_column_list=slice_column_list,
            regex_list=regex_list,
            rename_headers_list=rename_headers_list,
            remove_source_file=remove_source_file,
            delete_target_file=delete_target_file,
            int_date_list=int_date_list,
            gen_location_list=gen_location_list,
        )
    if pipeline_name == "GHCND hurricanes":
        download_file(source_url, source_file)
        if number_of_header_rows > 0:
            remove_header_rows(source_file, number_of_header_rows=number_of_header_rows)
        else:
            pass
        process_and_load_table(
            source_file=source_file,
            target_file=target_file,
            pipeline_name=pipeline_name,
            source_url=source_url,
            chunksize=chunksize,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            schema_path=schema_path,
            drop_dest_table=drop_dest_table,
            input_field_delimiter=input_field_delimiter,
            input_csv_headers=input_csv_headers,
            data_dtypes=data_dtypes,
            reorder_headers_list=reorder_headers_list,
            null_rows_list=null_rows_list,
            date_format_list=date_format_list,
            slice_column_list=slice_column_list,
            regex_list=regex_list,
            rename_headers_list=rename_headers_list,
            remove_source_file=remove_source_file,
            delete_target_file=delete_target_file,
            int_date_list=int_date_list,
            gen_location_list=gen_location_list,
        )
    if pipeline_name == "NOAA lightning strikes by year":
        url_path = os.path.split(source_url)[0]
        file_pattern = str.split(os.path.split(source_url)[1], "*")[0]
        url_list = url_directory_list(f"{url_path}/", file_pattern)
        if full_data_load == "N":
            start = datetime.datetime.now().year - 6
        else:
            start = int(start_year)
        for yr in range(start, datetime.datetime.now().year):
            for url in url_list:
                url_file_name = os.path.split(url)[1]
                if str(url_file_name).find(f"{file_pattern}{yr}") >= 0:
                    source_file_path = os.path.split(source_file)[0]
                    source_file_zipped = f"{source_file_path}/{url_file_name}"
                    source_file_year = str.replace(
                        str(source_file), ".csv", f"_{yr}.csv"
                    )
                    target_file_year = str.replace(
                        str(target_file), ".csv", f"_{yr}.csv"
                    )
                    download_file(url, source_file_zipped)
                    gz_decompress(
                        infile=source_file_zipped,
                        tofile=source_file_year,
                        delete_zipfile=True,
                    )
                    if number_of_header_rows > 0:
                        remove_header_rows(
                            source_file_year,
                            number_of_header_rows=number_of_header_rows,
                        )
                    else:
                        pass
                    if not full_data_load:
                        delete_source_file_data_from_bq(
                            project_id=project_id,
                            dataset_id=dataset_id,
                            table_id=destination_table,
                            source_url=url,
                        )
                    process_and_load_table(
                        source_file=source_file_year,
                        target_file=target_file_year,
                        pipeline_name=pipeline_name,
                        source_url=url,
                        chunksize=chunksize,
                        project_id=project_id,
                        dataset_id=dataset_id,
                        destination_table=destination_table,
                        target_gcs_bucket=target_gcs_bucket,
                        target_gcs_path=target_gcs_path,
                        schema_path=schema_path,
                        drop_dest_table=drop_dest_table,
                        input_field_delimiter=input_field_delimiter,
                        input_csv_headers=input_csv_headers,
                        data_dtypes=data_dtypes,
                        reorder_headers_list=reorder_headers_list,
                        null_rows_list=null_rows_list,
                        date_format_list=date_format_list,
                        slice_column_list=slice_column_list,
                        regex_list=regex_list,
                        rename_headers_list=rename_headers_list,
                        remove_source_file=remove_source_file,
                        delete_target_file=delete_target_file,
                        int_date_list=int_date_list,
                        gen_location_list=gen_location_list,
                    )


def process_and_load_table(
    source_file: str,
    target_file: str,
    pipeline_name: str,
    source_url: str,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    input_field_delimiter: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str],
    slice_column_list: dict,
    regex_list: dict,
    rename_headers_list: dict,
    remove_source_file: bool,
    delete_target_file: bool,
    int_date_list: typing.List[str],
    gen_location_list: dict,
    encoding: str = "utf-8",
) -> None:
    process_source_file(
        source_url=source_url,
        source_file=source_file,
        pipeline_name=pipeline_name,
        chunksize=chunksize,
        input_csv_headers=input_csv_headers,
        data_dtypes=data_dtypes,
        target_file=target_file,
        reorder_headers_list=reorder_headers_list,
        null_rows_list=null_rows_list,
        date_format_list=date_format_list,
        input_field_delimiter=input_field_delimiter,
        slice_column_list=slice_column_list,
        regex_list=regex_list,
        rename_headers_list=rename_headers_list,
        remove_source_file=remove_source_file,
        int_date_list=int_date_list,
        gen_location_list=gen_location_list,
        encoding=encoding,
    )
    if os.path.exists(target_file):
        upload_file_to_gcs(
            file_path=target_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
        if drop_dest_table == "Y":
            drop_table = True
        else:
            drop_table = False
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
            drop_table=drop_table,
        )
        if table_exists:
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=destination_table,
                file_path=target_file,
                truncate_table=True,
                field_delimiter="|",
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
        if delete_target_file:
            logging.info(f"Removing target file {target_file}")
            os.remove(target_file)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def process_source_file(
    source_file: str,
    chunksize: str,
    input_csv_headers: str,
    pipeline_name: str,
    data_dtypes: str,
    source_url: str,
    target_file: str,
    reorder_headers_list: typing.List[str],
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str],
    input_field_delimiter: str,
    slice_column_list: dict,
    regex_list: dict,
    rename_headers_list: dict,
    int_date_list: typing.List[str],
    gen_location_list: dict,
    encoding: str = "utf8",
    remove_source_file: bool = False,
) -> None:
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512 << 10)
    csv.register_dialect(
        "TabDialect", quotechar='"', delimiter=input_field_delimiter, strict=True
    )
    with open(source_file, encoding=encoding, mode="r") as reader:
        data = []
        chunk_number = 1
        for index, line in enumerate(
            csv.reader((line.replace("\0", "") for line in reader), "TabDialect"), 0
        ):
            data.append(line)
            if index % int(chunksize) == 0 and index > 0:
                process_dataframe_chunk(
                    data=data,
                    pipeline_name=pipeline_name,
                    input_csv_headers=input_csv_headers,
                    data_dtypes=data_dtypes,
                    source_url=source_url,
                    target_file=target_file,
                    chunk_number=chunk_number,
                    reorder_headers_list=reorder_headers_list,
                    date_format_list=date_format_list,
                    null_rows_list=null_rows_list,
                    slice_column_list=slice_column_list,
                    regex_list=regex_list,
                    rename_headers_list=rename_headers_list,
                    int_date_list=int_date_list,
                    gen_location_list=gen_location_list,
                )
                data = []
                chunk_number += 1

        if data:
            process_dataframe_chunk(
                data=data,
                pipeline_name=pipeline_name,
                input_csv_headers=input_csv_headers,
                data_dtypes=data_dtypes,
                source_url=source_url,
                target_file=target_file,
                chunk_number=chunk_number,
                reorder_headers_list=reorder_headers_list,
                date_format_list=date_format_list,
                null_rows_list=null_rows_list,
                slice_column_list=slice_column_list,
                regex_list=regex_list,
                rename_headers_list=rename_headers_list,
                int_date_list=int_date_list,
                gen_location_list=gen_location_list,
            )
        if remove_source_file:
            os.remove(source_file)


def process_dataframe_chunk(
    data: typing.List[str],
    pipeline_name: str,
    input_csv_headers: typing.List[str],
    data_dtypes: dict,
    source_url: str,
    target_file: str,
    chunk_number: int,
    reorder_headers_list: typing.List[str],
    date_format_list: typing.List[str],
    null_rows_list: typing.List[str],
    slice_column_list: dict,
    regex_list: dict,
    rename_headers_list: dict,
    int_date_list: typing.List[str],
    gen_location_list: dict,
) -> None:
    logging.info(f"Processing chunk #{chunk_number}")
    df = pd.DataFrame(data, columns=input_csv_headers)
    set_df_datatypes(df, data_dtypes)
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        source_url=source_url,
        target_file_batch=target_file_batch,
        target_file=target_file,
        skip_header=(not chunk_number == 1),
        pipeline_name=pipeline_name,
        reorder_headers_list=reorder_headers_list,
        date_format_list=date_format_list,
        null_rows_list=null_rows_list,
        slice_column_list=slice_column_list,
        regex_list=regex_list,
        rename_headers_list=rename_headers_list,
        int_date_list=int_date_list,
        gen_location_list=gen_location_list,
    )


def set_df_datatypes(df: pd.DataFrame, data_dtypes: dict) -> pd.DataFrame:
    logging.info("Setting data types")
    for key, item in data_dtypes.items():
        df[key] = df[key].astype(item)
    return df


def process_chunk(
    df: pd.DataFrame,
    source_url: str,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    pipeline_name: str,
    reorder_headers_list: dict,
    null_rows_list: typing.List[str],
    date_format_list: typing.List[str],
    slice_column_list: dict,
    regex_list: dict,
    rename_headers_list: dict,
    int_date_list: typing.List[str],
    gen_location_list: dict,
) -> None:
    if pipeline_name == "GHCND by year":
        df = filter_null_rows(df, null_rows_list=null_rows_list)
        df = add_metadata_cols(df, source_url=source_url)
        df = source_convert_date_formats(df, date_format_list=date_format_list)
        df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
    if pipeline_name in [
        "GHCND countries",
        "GHCND inventory",
        "GHCND states",
        "GHCND stations",
    ]:
        df = slice_column(df, slice_column_list)
        df = add_metadata_cols(df, source_url=source_url)
        df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
    if pipeline_name == "GSOD stations":
        df = slice_column(df, slice_column_list)
        df = filter_null_rows(df, null_rows_list=null_rows_list)
        df = add_metadata_cols(df, source_url=source_url)
        df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
        df["lat"] = df["lat"].astype(str)
        df["lon"] = df["lon"].astype(str)
        df = apply_regex(df, regex_list)
    if pipeline_name == "GHCND hurricanes":
        df.columns = df.columns.str.lower()
        df = rename_headers(df, rename_headers_list=rename_headers_list)
        df = add_metadata_cols(df, source_url=source_url)
        df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
    if pipeline_name == "NOAA lightning strikes by year":
        df.columns = df.columns.str.lower()
        df = rename_headers(df, rename_headers_list=rename_headers_list)
        df = convert_date_from_int(df, int_date_list=int_date_list)
        df = generate_location(df, gen_location_list=gen_location_list)
        df = add_metadata_cols(df, source_url=source_url)
        df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def convert_date_from_int(df: pd.DataFrame, int_date_list: dict) -> pd.DataFrame:
    logging.info("Converting dates from integers")
    for key, values in int_date_list.items():
        dt_col = key
        dt_int_col = values
        df[dt_col] = (
            pd.to_datetime(
                (df[dt_int_col][:].astype("string") + "000000"), "raise", False, True
            ).astype("string")
            + " 00:00:00"
        )
    return df


def generate_location(df: pd.DataFrame, gen_location_list: dict) -> pd.DataFrame:
    logging.info("Generating location data")
    for key, values in gen_location_list.items():
        df[key] = df[[values[0], values[1]]].apply(
            lambda x: f"POINT({x[0]} {x[1]})", axis=1
        )
    return df


def url_directory_list(
    source_url_path: str, file_pattern: str = ""
) -> typing.List[str]:
    rtn_list = []
    url = source_url_path.replace(" ", "%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, "html.parser")
    x = soup.find_all("a")
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ", "%20")
        if file_pattern == "":
            rtn_list.append(url_new)
        else:
            if re.search("" + file_pattern, file_name):
                rtn_list.append(url_new)
            else:
                pass
    return rtn_list


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    df.rename(columns=rename_headers_list, inplace=True)
    return df


def remove_header_rows(source_file: str, number_of_header_rows: int) -> None:
    logging.info(f"Removing header from {source_file}")
    os.system(f"sed -i '1,{number_of_header_rows}d' {source_file} ")


def add_metadata_cols(df: pd.DataFrame, source_url: str) -> pd.DataFrame:
    logging.info("Adding metadata columns")
    df["source_url"] = source_url
    df["etl_timestamp"] = pd.to_datetime(
        datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S", infer_datetime_format=True
    )
    return df


def reorder_headers(
    df: pd.DataFrame, reorder_headers_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Reordering headers..")
    return df[reorder_headers_list]


def gz_decompress(infile: str, tofile: str, delete_zipfile: bool = False) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)
    if delete_zipfile:
        os.remove(infile)


def filter_null_rows(
    df: pd.DataFrame, null_rows_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Removing rows with blank id's..")
    for fld in null_rows_list:
        df = df[df[fld] != ""]
    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or dt_str.lower() == "nan":
        return dt_str
    else:
        return str(
            datetime.datetime.strptime(dt_str, "%Y%m%d").date().strftime("%Y-%m-%d")
        )


def source_convert_date_formats(
    df: pd.DataFrame, date_format_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Converting Date Format..")
    for fld in date_format_list:
        df[fld] = df[fld].apply(convert_dt_format)
    return df


def slice_column(
    df: pd.DataFrame, slice_column_list: dict, pipeline_name: str = ""
) -> pd.DataFrame:
    logging.info("Extracting column data..")
    for key, values in slice_column_list.items():
        src_col = values[0]
        dest_col = key
        start_pos = values[1]
        end_pos = values[2]
        if pipeline_name == "GHCND states":
            if dest_col == "name":
                # Work-around for Alabama - bad data
                df[dest_col] = df[src_col].apply(
                    lambda x: "ALABAMA"
                    if str(x)[0:2] == "AL"
                    else str(x)[int(start_pos) :].strip()
                )
            else:
                if end_pos == "":
                    df[dest_col] = df[src_col].apply(
                        lambda x: str(x)[int(start_pos) :].strip()
                    )
                else:
                    df[dest_col] = df[src_col].apply(
                        lambda x: str(x)[int(start_pos) : int(end_pos)].strip()
                    )
        else:
            if end_pos == "":
                df[dest_col] = df[src_col].apply(
                    lambda x: str(x)[int(start_pos) :].strip()
                )
            else:
                df[dest_col] = df[src_col].apply(
                    lambda x: str(x)[int(start_pos) : int(end_pos)].strip()
                )
    return df


def get_column_country_code(col_val: str) -> str:
    return col_val.strip().split(" ")[0]


def get_column_country_name(col_val: str) -> str:
    len_code = len(str.split(str.strip(col_val), " ")[0])
    strmain1 = str.strip(col_val)
    len_main = len(str.strip(col_val))
    len_out = len_main - len_code
    return str.strip((strmain1[::-1])[0:(len_out)][::-1])


def apply_regex(df: pd.DataFrame, regex_list: dict) -> pd.DataFrame:
    logging.info("Applying RegEx")
    for key, values in regex_list.items():
        regex_expr = values[0]
        replace_expr = values[1]
        isregex = values[2] == "True"
        df[key][:].replace(regex_expr, replace_expr, regex=isregex, inplace=True)
    return df


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    truncate_table: bool,
    field_delimiter: str = "|",
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = field_delimiter
    if truncate_table:
        job_config.write_disposition = "WRITE_TRUNCATE"
    else:
        job_config.write_disposition = "WRITE_APPEND"
    job_config.skip_leading_rows = 1  # ignore the header
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} completed"
    )


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_filepath: list,
    bucket_name: str,
    drop_table: bool = False,
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    table_exists = False
    try:
        table = client.get_table(table_ref)
        table_exists_id = table.table_id
        logging.info(f"Table {table_exists_id} currently exists.")
        if drop_table:
            logging.info("Dropping existing table")
            client.delete_table(table)
            table = None
    except NotFound:
        table = None
    if not table:
        logging.info(
            (
                f"Table {table_ref} currently does not exist.  Attempting to create table."
            )
        )
        if check_gcs_file_exists(schema_filepath, bucket_name):
            schema = create_table_schema([], bucket_name, schema_filepath)
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)
            print(f"Table {table_ref} was created".format(table_id))
            table_exists = True
        else:
            file_name = os.path.split(schema_filepath)[1]
            file_path = os.path.split(schema_filepath)[0]
            logging.info(
                f"Error: Unable to create table {table_ref} because schema file {file_name} does not exist in location {file_path} in bucket {bucket_name}"
            )
            table_exists = False
    else:
        table_exists = True
    return table_exists


def check_gcs_file_exists(file_path: str, bucket_name: str) -> bool:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    exists = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)
    return exists


def delete_source_file_data_from_bq(
    project_id: str, dataset_id: str, table_id: str, source_url: str
) -> None:
    logging.info(
        f"Deleting data from {project_id}.{dataset_id}.{table_id} where source_url = '{source_url}'"
    )
    client = bigquery.Client()
    query = f"""
        DELETE
        FROM {project_id}.{dataset_id}.{table_id}
        WHERE source_url = '@source_url'
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
            bigquery.ScalarQueryParameter("dataset_id", "STRING", dataset_id),
            bigquery.ScalarQueryParameter("table_id", "STRING", table_id),
            bigquery.ScalarQueryParameter("source_url", "STRING", source_url),
        ]
    )
    query_job = client.query(query, job_config=job_config)  # Make an API request.
    query_job.result()


def create_table_schema(
    schema_structure: list, bucket_name: str = "", schema_filepath: str = ""
) -> list:
    logging.info(f"Defining table schema... {bucket_name} ... {schema_filepath}")
    schema = []
    if not (schema_filepath):
        schema_struct = schema_structure
    else:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(schema_filepath)
        schema_struct = json.loads(blob.download_as_bytes(client=None))
    for schema_field in schema_struct:
        fld_name = schema_field["name"]
        fld_type = schema_field["type"]
        try:
            fld_descr = schema_field["description"]
        except KeyError:
            fld_descr = ""
        fld_mode = schema_field["mode"]
        schema.append(
            bigquery.SchemaField(
                name=fld_name, field_type=fld_type, mode=fld_mode, description=fld_descr
            )
        )
    return schema


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = "|") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=sep)


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    with open(batch_file_path, "r") as data_file:
        if truncate_file:
            target_file = open(target_file_path, "w+").close()
        with open(target_file_path, "a+") as target_file:
            if skip_header:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
                )
                next(data_file)
            else:
                logging.info(
                    f"Appending batch file {batch_file_path} to {target_file_path}"
                )
            target_file.write(data_file.read())
            if os.path.exists(batch_file_path):
                os.remove(batch_file_path)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def download_file_ftp(
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    local_file: pathlib.Path,
    source_url: str,
) -> None:
    logging.info(f"Downloading {source_url} into {local_file}")
    for retry in range(1, 3):
        if not download_file_ftp_single_try(
            ftp_host, ftp_dir, ftp_filename, local_file
        ):
            logging.info(f"FTP file download failed.  Retrying #{retry} in 60 seconds")
            time.sleep(60)
        else:
            break


def download_file_ftp_single_try(
    ftp_host: str, ftp_dir: str, ftp_filename: str, local_file: pathlib.Path
) -> bool:
    # try:
    with ftplib.FTP(ftp_host, timeout=60) as ftp_conn:
        ftp_conn.login("", "")
        ftp_conn.cwd(ftp_dir)
        ftp_conn.encoding = "utf-8"
        with open(local_file, "wb") as dest_file:
            ftp_conn.retrbinary("RETR %s" % ftp_filename, dest_file.write)
        ftp_conn.quit()
        return True
    # except:
    #     return True


def upload_file_to_gcs(
    file_path: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    if os.path.exists(file_path):
        logging.info(
            f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket(target_gcs_bucket)
        blob = bucket.blob(target_gcs_path)
        blob.upload_from_filename(file_path)
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
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", "100000"),
        ftp_host=os.environ.get("FTP_HOST", ""),
        ftp_dir=os.environ.get("FTP_DIR", ""),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        drop_dest_table=os.environ.get("DROP_DEST_TABLE", "N"),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        input_field_delimiter=os.environ.get("INPUT_FIELD_DELIMITER", "N"),
        ftp_batch_size=os.environ.get("FTP_BATCH_SIZE", "20"),
        ftp_batch_sleep_time=os.environ.get("FTP_BATCH_SLEEP_TIME", "30"),
        full_data_load=os.environ.get("FULL_DATA_LOAD", "N"),
        start_year=os.environ.get("START_YEAR", ""),
        input_csv_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
        null_rows_list=json.loads(os.environ.get("NULL_ROWS_LIST", r"[]")),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"[]")),
        slice_column_list=json.loads(os.environ.get("SLICE_COLUMN_LIST", r"{}")),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", r"{}")),
        remove_source_file=os.environ.get("REMOVE_SOURCE_FILE", "N"),
        delete_target_file=os.environ.get("DELETE_TARGET_FILE", "N"),
        number_of_header_rows=os.environ.get("NUMBER_OF_HEADER_ROWS", "0"),
        regex_list=json.loads(os.environ.get("REGEX_LIST", r"{}")),
        int_date_list=json.loads(os.environ.get("INT_DATE_LIST", r"[]")),
        gen_location_list=json.loads(os.environ.get("GEN_LOCATION_LIST", r"{}")),
    )
