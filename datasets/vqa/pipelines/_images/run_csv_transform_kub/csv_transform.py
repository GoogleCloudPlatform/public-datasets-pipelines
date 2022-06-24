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
from shutil import move
import subprocess
import time
import typing
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url: typing.List[typing.List[str]],
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    remove_source_file: str,
    delete_target_file: str,
    reorder_headers_list: typing.List[str],
    detail_data_headers_list: typing.List[str]
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        pipeline_name=pipeline_name,
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        chunksize=chunksize,
        project_id=project_id,
        dataset_id=dataset_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_path=schema_path,
        drop_dest_table=drop_dest_table,
        remove_source_file=(remove_source_file == "Y"),
        delete_target_file=(delete_target_file == "Y"),
        reorder_headers_list=reorder_headers_list,
        detail_data_headers_list=detail_data_headers_list
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    pipeline_name: str,
    source_url: typing.List[typing.List[str]],
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    drop_dest_table: str,
    remove_source_file: bool,
    delete_target_file: bool,
    reorder_headers_list: typing.List[str],
    detail_data_headers_list: typing.List[str]
) -> None:
    for subtask, url, table_name, src_filename in source_url:
        logging.info(f"... Executing Load Process for {subtask}")
        source_zipfile = str.replace(str(source_file), ".csv", f"{table_name}.zip")
        root_path = os.path.split(source_zipfile)[0]
        target_file_path_main = str.replace(
            str(target_file), ".csv", f"_{table_name}.csv"
        )
        download_file(url, source_zipfile)
        zip_decompress(source_zipfile, root_path, False)
        if pipeline_name == "Load Annotations":
            file_counter = 0
            for src in src_filename:
                logging.info(f"    ... Processing file {root_path}/{src}")
                data = json.load(open(f"{root_path}/{src}"))
                df = pd.json_normalize(data)
                df = rename_headers(df)
                df_annot = pd.DataFrame()
                df_annot["annot_norm"] = df["annotations"].apply(
                    lambda x: pd.json_normalize(x)
                )
                df = df[reorder_headers_list]
                target_file_path_annot = str.replace(
                    str(target_file), ".csv", f"_{table_name}_annot.csv"
                )
                df = add_metadata_cols(df, url)
                save_to_new_file(
                    df,
                    target_file_path_main,
                    sep="|",
                    include_headers=(file_counter == 0)
                )
                file_counter += 1
                df_annot = add_metadata_cols(df_annot, url)
                save_to_new_file(
                    df_annot["annot_norm"][0][:][detail_data_headers_list],
                    target_file_path_annot,
                    sep="|",
                    include_headers=(file_counter == 0)
                )
        else:
            pass
        if pipeline_name == "Load Questions":
            file_counter = 0
            for src in src_filename:
                logging.info(f"    ... Processing file {root_path}/{src}")
                data = json.load(open(f"{root_path}/{src}"))
                df = pd.json_normalize(data)
                df = rename_headers(df)
                df_quest = pd.DataFrame()
                df_quest["questions"] = df["questions"].apply(
                    lambda x: pd.json_normalize(x)
                )
                df = df[reorder_headers_list]
                target_file_path_quest = str.replace(
                    str(target_file), ".csv", f"_{table_name}_quest.csv"
                )
                df = add_metadata_cols(df, url)
                save_to_new_file(df, target_file_path_main, include_headers=(file_counter == 0))
                df_quest = add_metadata_cols(df_quest, url)
                save_to_new_file(
                    df_quest["questions"][0][:][detail_data_headers_list],
                    target_file_path_quest,
                    sep="|",
                    include_headers=(file_counter == 0)
                )
                file_counter += 1
        else:
            pass
        if pipeline_name == "Load Complementary Pairs":
            file_counter = 0
            for src in src_filename:
                logging.info(f"    ... Processing file {root_path}/{src}")
                target_file_path_pairs = target_file.replace(".csv", "_{table_name}_pairs.csv")
                if convert_comp_pairs_file_to_csv(src, target_file_path_pairs) != "":
                    logging.info(f"        ... {target_file_path_pairs} was created.")
                else:
                    logging.info(f"        ... {target_file_path_pairs} was not created.")



def convert_comp_pairs_file_to_csv(src_json: str, destination_csv: str) -> str:
    subprocess.check_call(f"sed -i -e 's/\], \[/\n/g' {src_json}")
    subprocess.check_call(f"sed -i -e 's/,/\|/g' {src_json}")
    subprocess.check_call(f"sed -i -e 's/\[//g' {src_json}")
    subprocess.check_call(f"sed -i -e 's/\]//g' {src_json}")
    subprocess.check_call(f"sed -i -e 's/ //g' {src_json}")
    subprocess.check_call(f"echo 'question_id_1|question_id_2' > {destination_csv}")
    subprocess.check_call(f"cat {src_json} >> {destination_csv}")
    if os.path.exists(destination_csv):
        return destination_csv
    else:
        return ""


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def zip_decompress(infile: str, topath: str, remove_zipfile: bool = False) -> None:
    logging.info(f"Decompressing {infile} to {topath}")
    with ZipFile(infile, "r") as zip:
        zip.extractall(topath)
    if remove_zipfile:
        os.unlink(infile)


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        new_col_name = str.replace(str(col), ".", "_")
        df.rename(columns={col: new_col_name}, inplace=True)
    return df


def save_to_new_file(
    df: pd.DataFrame, file_path: str, sep: str = "|", include_headers: bool = True
) -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(
        file_path,
        index=False,
        sep=sep,
        header=include_headers,
        mode=("w+" if include_headers else "a"),
    )


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


def add_metadata_cols(df: pd.DataFrame, source_url: str) -> pd.DataFrame:
    logging.info("Adding metadata columns")
    df["source_url"] = source_url
    df["etl_timestamp"] = pd.to_datetime(
        datetime.datetime.now(), format="%Y-%m-%d %H:%M:%S", infer_datetime_format=True
    )
    return df


# def process_and_load_table(
#     source_file: str,
#     target_file: str,
#     pipeline_name: str,
#     source_url: str,
#     chunksize: str,
#     project_id: str,
#     dataset_id: str,
#     destination_table: str,
#     target_gcs_bucket: str,
#     target_gcs_path: str,
#     schema_path: str,
#     drop_dest_table: str,
#     input_field_delimiter: str,
#     input_csv_headers: typing.List[str],
#     data_dtypes: dict,
#     reorder_headers_list: typing.List[str],
#     null_rows_list: typing.List[str],
#     date_format_list: typing.List[str],
#     slice_column_list: dict,
#     regex_list: dict,
#     rename_headers_list: dict,
#     remove_source_file: bool,
#     delete_target_file: bool,
#     int_date_list: typing.List[str],
#     gen_location_list: dict,
#     encoding: str = "utf-8",
# ) -> None:
#     process_source_file(
#         source_url=source_url,
#         source_file=source_file,
#         pipeline_name=pipeline_name,
#         chunksize=chunksize,
#         input_csv_headers=input_csv_headers,
#         data_dtypes=data_dtypes,
#         target_file=target_file,
#         reorder_headers_list=reorder_headers_list,
#         null_rows_list=null_rows_list,
#         date_format_list=date_format_list,
#         input_field_delimiter=input_field_delimiter,
#         slice_column_list=slice_column_list,
#         regex_list=regex_list,
#         rename_headers_list=rename_headers_list,
#         remove_source_file=remove_source_file,
#         int_date_list=int_date_list,
#         gen_location_list=gen_location_list,
#         encoding=encoding,
#     )
#     if os.path.exists(target_file):
#         upload_file_to_gcs(
#             file_path=target_file,
#             target_gcs_bucket=target_gcs_bucket,
#             target_gcs_path=target_gcs_path,
#         )
#         if drop_dest_table == "Y":
#             drop_table = True
#         else:
#             drop_table = False
#         table_exists = create_dest_table(
#             project_id=project_id,
#             dataset_id=dataset_id,
#             table_id=destination_table,
#             schema_filepath=schema_path,
#             bucket_name=target_gcs_bucket,
#             drop_table=drop_table,
#         )
#         if table_exists:
#             load_data_to_bq(
#                 project_id=project_id,
#                 dataset_id=dataset_id,
#                 table_id=destination_table,
#                 file_path=target_file,
#                 truncate_table=True,
#                 field_delimiter="|",
#             )
#         else:
#             error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
#             raise ValueError(error_msg)
#         if delete_target_file:
#             logging.info(f"Removing target file {target_file}")
#             os.remove(target_file)
#     else:
#         logging.info(
#             f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
#         )


# def process_source_file(
#     source_file: str,
#     chunksize: str,
#     input_csv_headers: str,
#     pipeline_name: str,
#     data_dtypes: str,
#     source_url: str,
#     target_file: str,
#     reorder_headers_list: typing.List[str],
#     null_rows_list: typing.List[str],
#     date_format_list: typing.List[str],
#     input_field_delimiter: str,
#     slice_column_list: dict,
#     regex_list: dict,
#     rename_headers_list: dict,
#     int_date_list: typing.List[str],
#     gen_location_list: dict,
#     encoding: str = "utf8",
#     remove_source_file: bool = False,
# ) -> None:
#     logging.info(f"Opening source file {source_file}")
#     csv.field_size_limit(512 << 10)
#     csv.register_dialect(
#         "TabDialect", quotechar='"', delimiter=input_field_delimiter, strict=True
#     )
#     with open(source_file, encoding=encoding, mode="r") as reader:
#         data = []
#         chunk_number = 1
#         for index, line in enumerate(
#             csv.reader((line.replace("\0", "") for line in reader), "TabDialect"), 0
#         ):
#             data.append(line)
#             if index % int(chunksize) == 0 and index > 0:
#                 process_dataframe_chunk(
#                     data=data,
#                     pipeline_name=pipeline_name,
#                     input_csv_headers=input_csv_headers,
#                     data_dtypes=data_dtypes,
#                     source_url=source_url,
#                     target_file=target_file,
#                     chunk_number=chunk_number,
#                     reorder_headers_list=reorder_headers_list,
#                     date_format_list=date_format_list,
#                     null_rows_list=null_rows_list,
#                     slice_column_list=slice_column_list,
#                     regex_list=regex_list,
#                     rename_headers_list=rename_headers_list,
#                     int_date_list=int_date_list,
#                     gen_location_list=gen_location_list,
#                 )
#                 data = []
#                 chunk_number += 1

#         if data:
#             process_dataframe_chunk(
#                 data=data,
#                 pipeline_name=pipeline_name,
#                 input_csv_headers=input_csv_headers,
#                 data_dtypes=data_dtypes,
#                 source_url=source_url,
#                 target_file=target_file,
#                 chunk_number=chunk_number,
#                 reorder_headers_list=reorder_headers_list,
#                 date_format_list=date_format_list,
#                 null_rows_list=null_rows_list,
#                 slice_column_list=slice_column_list,
#                 regex_list=regex_list,
#                 rename_headers_list=rename_headers_list,
#                 int_date_list=int_date_list,
#                 gen_location_list=gen_location_list,
#             )
#         if remove_source_file:
#             os.remove(source_file)


# def process_dataframe_chunk(
#     data: typing.List[str],
#     pipeline_name: str,
#     input_csv_headers: typing.List[str],
#     data_dtypes: dict,
#     source_url: str,
#     target_file: str,
#     chunk_number: int,
#     reorder_headers_list: typing.List[str],
#     date_format_list: typing.List[str],
#     null_rows_list: typing.List[str],
#     slice_column_list: dict,
#     regex_list: dict,
#     rename_headers_list: dict,
#     int_date_list: typing.List[str],
#     gen_location_list: dict,
# ) -> None:
#     logging.info(f"Processing chunk #{chunk_number}")
#     df = pd.DataFrame(data, columns=input_csv_headers)
#     set_df_datatypes(df, data_dtypes)
#     target_file_batch = str(target_file).replace(
#         ".csv", "-" + str(chunk_number) + ".csv"
#     )
#     process_chunk(
#         df=df,
#         source_url=source_url,
#         target_file_batch=target_file_batch,
#         target_file=target_file,
#         skip_header=(not chunk_number == 1),
#         pipeline_name=pipeline_name,
#         reorder_headers_list=reorder_headers_list,
#         date_format_list=date_format_list,
#         null_rows_list=null_rows_list,
#         slice_column_list=slice_column_list,
#         regex_list=regex_list,
#         rename_headers_list=rename_headers_list,
#         int_date_list=int_date_list,
#         gen_location_list=gen_location_list,
#     )


# def set_df_datatypes(df: pd.DataFrame, data_dtypes: dict) -> pd.DataFrame:
#     logging.info("Setting data types")
#     for key, item in data_dtypes.items():
#         df[key] = df[key].astype(item)
#     return df


# def process_chunk(
#     df: pd.DataFrame,
#     source_url: str,
#     target_file_batch: str,
#     target_file: str,
#     skip_header: bool,
#     pipeline_name: str,
#     reorder_headers_list: dict,
#     null_rows_list: typing.List[str],
#     date_format_list: typing.List[str],
#     slice_column_list: dict,
#     regex_list: dict,
#     rename_headers_list: dict,
#     int_date_list: typing.List[str],
#     gen_location_list: dict,
# ) -> None:
#     if pipeline_name == "GHCND by year":
#         df = filter_null_rows(df, null_rows_list=null_rows_list)
#         df = add_metadata_cols(df, source_url=source_url)
#         df = source_convert_date_formats(df, date_format_list=date_format_list)
#         df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
#     if pipeline_name in [
#         "GHCND countries",
#         "GHCND inventory",
#         "GHCND states",
#         "GHCND stations",
#     ]:
#         df = slice_column(df, slice_column_list)
#         df = add_metadata_cols(df, source_url=source_url)
#         df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
#     if pipeline_name == "GSOD stations":
#         df = slice_column(df, slice_column_list)
#         df = filter_null_rows(df, null_rows_list=null_rows_list)
#         df = add_metadata_cols(df, source_url=source_url)
#         df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
#         df["lat"] = df["lat"].astype(str)
#         df["lon"] = df["lon"].astype(str)
#         df = apply_regex(df, regex_list)
#     if pipeline_name == "GHCND hurricanes":
#         df.columns = df.columns.str.lower()
#         df = rename_headers(df, rename_headers_list=rename_headers_list)
#         df = add_metadata_cols(df, source_url=source_url)
#         df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
#     if pipeline_name == "NOAA lightning strikes by year":
#         df.columns = df.columns.str.lower()
#         df = rename_headers(df, rename_headers_list=rename_headers_list)
#         df = convert_date_from_int(df, int_date_list=int_date_list)
#         df = generate_location(df, gen_location_list=gen_location_list)
#         df = add_metadata_cols(df, source_url=source_url)
#         df = reorder_headers(df, reorder_headers_list=reorder_headers_list)
#     save_to_new_file(df, file_path=str(target_file_batch))
#     append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


# def convert_date_from_int(df: pd.DataFrame, int_date_list: dict) -> pd.DataFrame:
#     logging.info("Converting dates from integers")
#     for key, values in int_date_list.items():
#         dt_col = key
#         dt_int_col = values
#         df[dt_col] = (
#             pd.to_datetime(
#                 (df[dt_int_col][:].astype("string") + "000000"), "raise", False, True
#             ).astype("string")
#             + " 00:00:00"
#         )
#     return df


# def generate_location(df: pd.DataFrame, gen_location_list: dict) -> pd.DataFrame:
#     logging.info("Generating location data")
#     for key, values in gen_location_list.items():
#         df[key] = df[[values[0], values[1]]].apply(
#             lambda x: f"POINT({x[0]} {x[1]})", axis=1
#         )
#     return df


# def url_directory_list(
#     source_url_path: str, file_pattern: str = ""
# ) -> typing.List[str]:
#     rtn_list = []
#     url = source_url_path.replace(" ", "%20")
#     req = Request(url)
#     a = urlopen(req).read()
#     soup = BeautifulSoup(a, "html.parser")
#     x = soup.find_all("a")
#     for i in x:
#         file_name = i.extract().get_text()
#         url_new = url + file_name
#         url_new = url_new.replace(" ", "%20")
#         if file_pattern == "":
#             rtn_list.append(url_new)
#         else:
#             if re.search("" + file_pattern, file_name):
#                 rtn_list.append(url_new)
#             else:
#                 pass
#     return rtn_list


# def remove_header_rows(source_file: str, number_of_header_rows: int) -> None:
#     logging.info(f"Removing header from {source_file}")
#     os.system(f"sed -i '1,{number_of_header_rows}d' {source_file} ")


# def reorder_headers(
#     df: pd.DataFrame, reorder_headers_list: typing.List[str]
# ) -> pd.DataFrame:
#     logging.info("Reordering headers..")
#     return df[reorder_headers_list]


# def gz_decompress(infile: str, tofile: str, delete_zipfile: bool = False) -> None:
#     logging.info(f"Decompressing {infile}")
#     with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
#         decom_str = gzip.decompress(inf.read()).decode("utf-8")
#         tof.write(decom_str)
#     if delete_zipfile:
#         os.remove(infile)


# def filter_null_rows(
#     df: pd.DataFrame, null_rows_list: typing.List[str]
# ) -> pd.DataFrame:
#     logging.info("Removing rows with blank id's..")
#     for fld in null_rows_list:
#         df = df[df[fld] != ""]
#     return df


# def convert_dt_format(dt_str: str) -> str:
#     if not dt_str or dt_str.lower() == "nan":
#         return dt_str
#     else:
#         return str(
#             datetime.datetime.strptime(dt_str, "%Y%m%d").date().strftime("%Y-%m-%d")
#         )


# def source_convert_date_formats(
#     df: pd.DataFrame, date_format_list: typing.List[str]
# ) -> pd.DataFrame:
#     logging.info("Converting Date Format..")
#     for fld in date_format_list:
#         df[fld] = df[fld].apply(convert_dt_format)
#     return df


# def slice_column(
#     df: pd.DataFrame, slice_column_list: dict, pipeline_name: str = ""
# ) -> pd.DataFrame:
#     logging.info("Extracting column data..")
#     for key, values in slice_column_list.items():
#         src_col = values[0]
#         dest_col = key
#         start_pos = values[1]
#         end_pos = values[2]
#         if pipeline_name == "GHCND states":
#             if dest_col == "name":
#                 # Work-around for Alabama - bad data
#                 df[dest_col] = df[src_col].apply(
#                     lambda x: "ALABAMA"
#                     if str(x)[0:2] == "AL"
#                     else str(x)[int(start_pos) :].strip()
#                 )
#             else:
#                 if end_pos == "":
#                     df[dest_col] = df[src_col].apply(
#                         lambda x: str(x)[int(start_pos) :].strip()
#                     )
#                 else:
#                     df[dest_col] = df[src_col].apply(
#                         lambda x: str(x)[int(start_pos) : int(end_pos)].strip()
#                     )
#         else:
#             if end_pos == "":
#                 df[dest_col] = df[src_col].apply(
#                     lambda x: str(x)[int(start_pos) :].strip()
#                 )
#             else:
#                 df[dest_col] = df[src_col].apply(
#                     lambda x: str(x)[int(start_pos) : int(end_pos)].strip()
#                 )
#     return df


# def get_column_country_code(col_val: str) -> str:
#     return col_val.strip().split(" ")[0]


# def get_column_country_name(col_val: str) -> str:
#     len_code = len(str.split(str.strip(col_val), " ")[0])
#     strmain1 = str.strip(col_val)
#     len_main = len(str.strip(col_val))
#     len_out = len_main - len_code
#     return str.strip((strmain1[::-1])[0:(len_out)][::-1])


# def apply_regex(df: pd.DataFrame, regex_list: dict) -> pd.DataFrame:
#     logging.info("Applying RegEx")
#     for key, values in regex_list.items():
#         regex_expr = values[0]
#         replace_expr = values[1]
#         isregex = values[2] == "True"
#         df[key][:].replace(regex_expr, replace_expr, regex=isregex, inplace=True)
#     return df


# def load_data_to_bq(
#     project_id: str,
#     dataset_id: str,
#     table_id: str,
#     file_path: str,
#     truncate_table: bool,
#     field_delimiter: str = "|",
# ) -> None:
#     logging.info(
#         f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
#     )
#     client = bigquery.Client(project=project_id)
#     table_ref = client.dataset(dataset_id).table(table_id)
#     job_config = bigquery.LoadJobConfig()
#     job_config.source_format = bigquery.SourceFormat.CSV
#     job_config.field_delimiter = field_delimiter
#     if truncate_table:
#         job_config.write_disposition = "WRITE_TRUNCATE"
#     else:
#         job_config.write_disposition = "WRITE_APPEND"
#     job_config.skip_leading_rows = 1  # ignore the header
#     job_config.autodetect = False
#     with open(file_path, "rb") as source_file:
#         job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
#     job.result()
#     logging.info(
#         f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} completed"
#     )


# def create_dest_table(
#     project_id: str,
#     dataset_id: str,
#     table_id: str,
#     schema_filepath: list,
#     bucket_name: str,
#     drop_table: bool = False,
# ) -> bool:
#     table_ref = f"{project_id}.{dataset_id}.{table_id}"
#     logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
#     client = bigquery.Client()
#     table_exists = False
#     try:
#         table = client.get_table(table_ref)
#         table_exists_id = table.table_id
#         logging.info(f"Table {table_exists_id} currently exists.")
#         if drop_table:
#             logging.info("Dropping existing table")
#             client.delete_table(table)
#             table = None
#     except NotFound:
#         table = None
#     if not table:
#         logging.info(
#             (
#                 f"Table {table_ref} currently does not exist.  Attempting to create table."
#             )
#         )
#         if check_gcs_file_exists(schema_filepath, bucket_name):
#             schema = create_table_schema([], bucket_name, schema_filepath)
#             table = bigquery.Table(table_ref, schema=schema)
#             client.create_table(table)
#             print(f"Table {table_ref} was created".format(table_id))
#             table_exists = True
#         else:
#             file_name = os.path.split(schema_filepath)[1]
#             file_path = os.path.split(schema_filepath)[0]
#             logging.info(
#                 f"Error: Unable to create table {table_ref} because schema file {file_name} does not exist in location {file_path} in bucket {bucket_name}"
#             )
#             table_exists = False
#     else:
#         table_exists = True
#     return table_exists


# def check_gcs_file_exists(file_path: str, bucket_name: str) -> bool:
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     exists = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)
#     return exists


# def delete_source_file_data_from_bq(
#     project_id: str, dataset_id: str, table_id: str, source_url: str
# ) -> None:
#     logging.info(
#         f"Deleting data from {project_id}.{dataset_id}.{table_id} where source_url = '{source_url}'"
#     )
#     client = bigquery.Client()
#     query = f"""
#         DELETE
#         FROM {project_id}.{dataset_id}.{table_id}
#         WHERE source_url = '@source_url'
#     """
#     job_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
#             bigquery.ScalarQueryParameter("dataset_id", "STRING", dataset_id),
#             bigquery.ScalarQueryParameter("table_id", "STRING", table_id),
#             bigquery.ScalarQueryParameter("source_url", "STRING", source_url),
#         ]
#     )
#     query_job = client.query(query, job_config=job_config)  # Make an API request.
#     query_job.result()


# def create_table_schema(
#     schema_structure: list, bucket_name: str = "", schema_filepath: str = ""
# ) -> list:
#     logging.info(f"Defining table schema... {bucket_name} ... {schema_filepath}")
#     schema = []
#     if not (schema_filepath):
#         schema_struct = schema_structure
#     else:
#         storage_client = storage.Client()
#         bucket = storage_client.get_bucket(bucket_name)
#         blob = bucket.blob(schema_filepath)
#         schema_struct = json.loads(blob.download_as_bytes(client=None))
#     for schema_field in schema_struct:
#         fld_name = schema_field["name"]
#         fld_type = schema_field["type"]
#         try:
#             fld_descr = schema_field["description"]
#         except KeyError:
#             fld_descr = ""
#         fld_mode = schema_field["mode"]
#         schema.append(
#             bigquery.SchemaField(
#                 name=fld_name, field_type=fld_type, mode=fld_mode, description=fld_descr
#             )
#         )
#     return schema


# def append_batch_file(
#     batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
# ) -> None:
#     with open(batch_file_path, "r") as data_file:
#         if truncate_file:
#             target_file = open(target_file_path, "w+").close()
#         with open(target_file_path, "a+") as target_file:
#             if skip_header:
#                 logging.info(
#                     f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
#                 )
#                 next(data_file)
#             else:
#                 logging.info(
#                     f"Appending batch file {batch_file_path} to {target_file_path}"
#                 )
#             target_file.write(data_file.read())
#             if os.path.exists(batch_file_path):
#                 os.remove(batch_file_path)


# def download_file_ftp(
#     ftp_host: str,
#     ftp_dir: str,
#     ftp_filename: str,
#     local_file: pathlib.Path,
#     source_url: str,
# ) -> None:
#     logging.info(f"Downloading {source_url} into {local_file}")
#     for retry in range(1, 3):
#         if not download_file_ftp_single_try(
#             ftp_host, ftp_dir, ftp_filename, local_file
#         ):
#             logging.info(f"FTP file download failed.  Retrying #{retry} in 60 seconds")
#             time.sleep(60)
#         else:
#             break


# def download_file_ftp_single_try(
#     ftp_host: str, ftp_dir: str, ftp_filename: str, local_file: pathlib.Path
# ) -> bool:
#     # try:
#     with ftplib.FTP(ftp_host, timeout=60) as ftp_conn:
#         ftp_conn.login("", "")
#         ftp_conn.cwd(ftp_dir)
#         ftp_conn.encoding = "utf-8"
#         with open(local_file, "wb") as dest_file:
#             ftp_conn.retrbinary("RETR %s" % ftp_filename, dest_file.write)
#         ftp_conn.quit()
#         return True
#     # except:
#     #     return True


# def upload_file_to_gcs(
#     file_path: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
# ) -> None:
#     if os.path.exists(file_path):
#         logging.info(
#             f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}"
#         )
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(target_gcs_bucket)
#         blob = bucket.blob(target_gcs_path)
#         blob.upload_from_filename(file_path)
#     else:
#         logging.info(
#             f"Cannot upload file to gs://{target_gcs_bucket}/{target_gcs_path} as it does not exist."
#         )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=json.loads(os.environ.get("SOURCE_URL", r"[[]]")),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", "100000"),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        drop_dest_table=os.environ.get("DROP_DEST_TABLE", "N"),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        remove_source_file=os.environ.get("REMOVE_SOURCE_FILE", "N"),
        delete_target_file=os.environ.get("DELETE_TARGET_FILE", "N"),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
        detail_data_headers_list=json.loads(os.environ.get("DETAIL_DATA_HEADERS_LIST", r"[]"))
    )
