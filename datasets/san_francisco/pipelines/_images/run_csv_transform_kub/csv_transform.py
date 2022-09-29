# Copyright 2022 Google LLC
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

import fnmatch
import json
import logging
import os
import pathlib
import re
import shutil
import typing
import zipfile as zip
from datetime import datetime

import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    source_url: str,
    source_url_dict: dict,
    source_url_list: typing.List[str],
    pipeline_name: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    drop_dest_table: str,
    schema_path: str,
    header_row_ordinal: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    trip_data_names: typing.List[str],
    trip_data_dtypes: dict,
    tripdata_names: typing.List[str],
    tripdata_dtypes: dict,
    rename_headers_tripdata: dict,
    rename_headers_list: dict,
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    date_format_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:

    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        source_url=source_url,
        source_url_dict=source_url_dict,
        source_url_list=source_url_list,
        source_file=source_file,
        target_file=target_file,
        project_id=project_id,
        dataset_id=dataset_id,
        destination_table=table_id,
        drop_dest_table=drop_dest_table,
        schema_path=schema_path,
        chunksize=chunksize,
        header_row_ordinal=header_row_ordinal,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        input_headers=input_headers,
        data_dtypes=data_dtypes,
        trip_data_names=trip_data_names,
        trip_data_dtypes=trip_data_dtypes,
        tripdata_names=tripdata_names,
        tripdata_dtypes=tripdata_dtypes,
        rename_headers_tripdata=rename_headers_tripdata,
        rename_headers_list=rename_headers_list,
        empty_key_list=empty_key_list,
        gen_location_list=gen_location_list,
        resolve_datatypes_list=resolve_datatypes_list,
        remove_paren_list=remove_paren_list,
        strip_newlines_list=strip_newlines_list,
        strip_whitespace_list=strip_whitespace_list,
        date_format_list=date_format_list,
        reorder_headers_list=reorder_headers_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    source_url: str,
    source_url_dict: dict,
    source_url_list: typing.List[str],
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    drop_dest_table: str,
    schema_path: str,
    chunksize: str,
    header_row_ordinal: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    trip_data_names: typing.List[str],
    trip_data_dtypes: dict,
    tripdata_names: typing.List[str],
    tripdata_dtypes: dict,
    rename_headers_tripdata: dict,
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    date_format_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:
    if (
        destination_table == "311_service_requests"
        or destination_table == "film_locations"
        or destination_table == "sffd_service_calls"
        or destination_table == "street_trees"
    ):
        download_file(source_url, source_file)
    elif destination_table == "calendar":
        process_sf_calendar(
            source_url_dict=source_url_dict,
            target_file=target_file,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            drop_dest_table=drop_dest_table,
            schema_path=schema_path,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            rename_headers_list=rename_headers_list,
            reorder_headers_list=reorder_headers_list,
        )
        return None
    elif destination_table == "routes":
        process_sf_muni_routes(
            source_url_dict=source_url_dict,
            target_file=target_file,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            drop_dest_table=drop_dest_table,
            schema_path=schema_path,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            reorder_headers_list=reorder_headers_list,
        )
        return None
    elif destination_table == "shapes":
        process_sf_muni_shapes(
            source_url_dict=source_url_dict,
            target_file=target_file,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            drop_dest_table=drop_dest_table,
            schema_path=schema_path,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            rename_headers_list=rename_headers_list,
            reorder_headers_list=reorder_headers_list,
        )
        return None
    elif destination_table == "stops":
        process_sf_muni_stops(
            source_url_dict=source_url_dict,
            target_file=target_file,
            project_id=project_id,
            dataset_id=dataset_id,
            destination_table=destination_table,
            drop_dest_table=drop_dest_table,
            schema_path=schema_path,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
            reorder_headers_list=reorder_headers_list,
        )
        return None
    elif destination_table == "sfpd_incidents":
        download_file_http(
            source_url=source_url_dict["sfpd_incidents"], source_file=source_file
        )
    elif destination_table == "bikeshare_station_info":
        source_url_json = f"{source_url}.json"
        source_file_json = str(source_file).replace(".csv", "") + "_stations.json"
        download_file_json(source_url_json, source_file_json, source_file, "stations")
    elif destination_table == "bikeshare_station_status":
        source_url_json = f"{source_url}.json"
        source_file_json = str(source_file).replace(".csv", "") + "_status.json"
        download_file_json(source_url_json, source_file_json, source_file, "stations")
    if destination_table == "bikeshare_trips":
        dest_path = os.path.split(source_file)[0]
        download_url_files_from_list(source_url_list, dest_path)
        stage_input_files(dest_path, source_file)
        process_source_file(
            source_file=str(source_file).replace(".csv", "_trip_data.csv"),
            target_file=str(target_file).replace(".csv", "_trip_data.csv"),
            chunksize=int(chunksize),
            input_headers=trip_data_names,
            data_dtypes=trip_data_dtypes,
            destination_table=destination_table,
            rename_headers_list=rename_headers_list,
            empty_key_list=empty_key_list,
            gen_location_list=gen_location_list,
            resolve_datatypes_list=resolve_datatypes_list,
            remove_paren_list=remove_paren_list,
            strip_newlines_list=strip_newlines_list,
            strip_whitespace_list=strip_whitespace_list,
            date_format_list=date_format_list,
            reorder_headers_list=reorder_headers_list,
            header_row_ordinal=None,
        )
        process_source_file(
            source_file=str(source_file).replace(".csv", "_tripdata.csv"),
            target_file=str(target_file).replace(".csv", "_tripdata.csv"),
            chunksize=int(chunksize),
            input_headers=tripdata_names,
            data_dtypes=tripdata_dtypes,
            destination_table=destination_table,
            rename_headers_list=rename_headers_tripdata,
            empty_key_list=empty_key_list,
            gen_location_list=gen_location_list,
            resolve_datatypes_list=resolve_datatypes_list,
            remove_paren_list=remove_paren_list,
            strip_newlines_list=strip_newlines_list,
            strip_whitespace_list=strip_whitespace_list,
            date_format_list=date_format_list,
            reorder_headers_list=reorder_headers_list,
            header_row_ordinal=None,
        )
        handle_tripdata(
            target_file=target_file,
            resolve_datatypes_list=resolve_datatypes_list,
            rename_headers_list=rename_headers_list,
            reorder_headers_list=reorder_headers_list,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
    else:
        process_source_file(
            source_file=source_file,
            target_file=target_file,
            chunksize=chunksize,
            header_row_ordinal=header_row_ordinal,
            input_headers=input_headers,
            data_dtypes=data_dtypes,
            destination_table=destination_table,
            rename_headers_list=rename_headers_list,
            empty_key_list=empty_key_list,
            gen_location_list=gen_location_list,
            resolve_datatypes_list=resolve_datatypes_list,
            remove_paren_list=remove_paren_list,
            strip_newlines_list=strip_newlines_list,
            strip_whitespace_list=strip_whitespace_list,
            date_format_list=date_format_list,
            reorder_headers_list=reorder_headers_list,
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
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def process_sf_calendar(
    source_url_dict: dict,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    drop_dest_table: str,
    schema_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    rename_headers_list: typing.List[str],
    reorder_headers_list: typing.List[str],
) -> None:
    df_calendar = gcs_to_df(
        project_id=project_id,
        source_file_gcs_path=source_url_dict["calendar"],
        target_file_path=str(target_file),
    )
    df_calendar_attributes = gcs_to_df(
        project_id=project_id,
        source_file_gcs_path=source_url_dict["calendar_attributes"],
        target_file_path=str(target_file),
    )
    df_calendar_dates = gcs_to_df(
        project_id=project_id,
        source_file_gcs_path=source_url_dict["calendar_dates"],
        target_file_path=str(target_file),
    )
    df = df_calendar.merge(
        df_calendar_attributes,
        how="inner",
        on=None,
        left_on="service_id",
        right_on="service_id",
        sort=True,
        suffixes=("_calendar", "_attributes"),
        copy=True,
        indicator=False,
        validate=None,
    )
    df = df.merge(
        df_calendar_dates,
        how="inner",
        on=None,
        left_on="service_id",
        right_on="service_id",
        sort=True,
        suffixes=("_calendar", "_dates"),
        copy=True,
        indicator=False,
        validate=None,
    )
    df["monday_str"] = df["monday"].apply(lambda x: "False" if x == 0 else "True")
    df["tuesday_str"] = df["tuesday"].apply(lambda x: "False" if x == 0 else "True")
    df["wednesday_str"] = df["wednesday"].apply(lambda x: "False" if x == 0 else "True")
    df["thursday_str"] = df["thursday"].apply(lambda x: "False" if x == 0 else "True")
    df["friday_str"] = df["friday"].apply(lambda x: "False" if x == 0 else "True")
    df["saturday_str"] = df["saturday"].apply(lambda x: "False" if x == 0 else "True")
    df["sunday_str"] = df["sunday"].apply(lambda x: "False" if x == 0 else "True")
    df["exception_type_str"] = df["exception_type"].apply(
        lambda x: "True" if x == 1 else "False"
    )
    df = df[
        [
            "service_id",
            "start_date",
            "end_date",
            "service_description",
            "date",
            "exception_type_str",
            "monday_str",
            "tuesday_str",
            "wednesday_str",
            "thursday_str",
            "friday_str",
            "saturday_str",
            "sunday_str",
        ]
    ]
    df = rename_headers(df=df, rename_headers_list=rename_headers_list)
    df["exceptions"] = df["exceptions"].apply(
        lambda x: f"{str(x).strip()[:4]}-{str(x).strip()[4:6]}-{str(x).strip()[6:8]}"
    )
    df = reorder_headers(df=df, output_headers_list=reorder_headers_list)
    save_to_new_file(df=df, file_path=target_file, sep="|")
    upload_file_to_gcs(
        file_path=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
    )
    drop_table = drop_dest_table == "Y"
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


def process_sf_muni_routes(
    source_url_dict: dict,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    drop_dest_table: str,
    schema_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    reorder_headers_list: typing.List[str],
) -> None:
    df_routes = gcs_to_df(
        project_id=project_id,
        source_file_gcs_path=source_url_dict["routes"],
        target_file_path=str(target_file),
    )
    df_routes = reorder_headers(df=df_routes, output_headers_list=reorder_headers_list)
    save_to_new_file(df=df_routes, file_path=target_file, sep="|")
    upload_file_to_gcs(
        file_path=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
    )
    drop_table = drop_dest_table == "Y"
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


def process_sf_muni_shapes(
    source_url_dict: dict,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    drop_dest_table: str,
    schema_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    rename_headers_list: typing.List[str],
    reorder_headers_list: typing.List[str],
) -> None:
    df_shapes = gcs_to_df(
        project_id=project_id,
        source_file_gcs_path=source_url_dict["shapes"],
        target_file_path=str(target_file),
    )
    df_shapes = rename_headers(df=df_shapes, rename_headers_list=rename_headers_list)
    df_shapes["shape_point_geom"] = df_shapes.apply(
        lambda x: create_geometry_columns(x["shape_point_lon"], x["shape_point_lat"]),
        axis=1,
    )
    df_shapes = reorder_headers(df=df_shapes, output_headers_list=reorder_headers_list)
    save_to_new_file(df=df_shapes, file_path=target_file, sep="|")
    upload_file_to_gcs(
        file_path=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
    )
    drop_table = drop_dest_table == "Y"
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


def process_sf_muni_stops(
    source_url_dict: dict,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    drop_dest_table: str,
    schema_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    reorder_headers_list: typing.List[str],
) -> None:
    df_stops = gcs_to_df(
        project_id=project_id,
        source_file_gcs_path=source_url_dict["stops"],
        target_file_path=str(target_file),
    )
    df_stops["stop_geom"] = df_stops.apply(
        lambda x: create_geometry_columns(x["stop_lon"], x["stop_lat"]), axis=1
    )
    df_stops = reorder_headers(df=df_stops, output_headers_list=reorder_headers_list)
    save_to_new_file(df=df_stops, file_path=target_file, sep="|")
    upload_file_to_gcs(
        file_path=target_file,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
    )
    drop_table = drop_dest_table == "Y"
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


def create_geometry_columns(long: float, lat: float) -> pd.DataFrame:
    return f"POINT({str(long)} {str(lat)})".replace("POINT( )", "")


def rename_headers(df: pd.DataFrame, rename_headers_list: dict) -> pd.DataFrame:
    logging.info("Renaming Headers")
    df = df.rename(columns=rename_headers_list)
    return df


def gcs_to_df(
    project_id: str,
    source_file_gcs_path: str,
    target_file_path: str,
    source_file_type: str = "csv",
) -> pd.DataFrame:
    filename = os.path.basename(source_file_gcs_path)
    destination_folder = os.path.split(target_file_path)[0]
    download_file_gcs(
        project_id=project_id,
        source_location=source_file_gcs_path,
        destination_folder=destination_folder,
    )
    if source_file_type == "csv":
        df = pd.read_csv(f"{destination_folder}/{filename}")
    elif source_file_type == "txt":
        df = pd.read_fwf(f"{destination_folder}/{filename}")
    return df


def http_to_df(
    source_url: str, target_file_path: str, source_file_type: str = "csv"
) -> pd.DataFrame:
    filename = os.path.basename(source_url)
    destination_folder = os.path.split(target_file_path)[0]
    download_file_http(
        source_url=source_url, source_file=f"{destination_folder}/{filename}"
    )
    if source_file_type == "csv":
        df = pd.read_csv(f"{destination_folder}/{filename}")
    elif source_file_type == "txt":
        df = pd.read_fwf(f"{destination_folder}/{filename}")
    return df


def download_file_gcs(
    project_id: str, source_location: str, destination_folder: str
) -> None:
    object_name = os.path.basename(source_location)
    dest_object = f"{destination_folder}/{object_name}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def handle_tripdata(
    target_file: str,
    resolve_datatypes_list: dict,
    rename_headers_list: dict,
    reorder_headers_list: typing.List[str],
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> pd.DataFrame:
    logging.info("Compiling target file by merging source data")
    trip_data_filepath = str(target_file).replace(".csv", "_trip_data.csv")
    logging.info(f"Opening {trip_data_filepath}")
    df_trip_data = pd.read_csv(
        trip_data_filepath,
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        sep="|",  # data column separator, typically ","
    )
    tripdata_filepath = str(target_file).replace(".csv", "_tripdata.csv")
    logging.info(f"Opening {tripdata_filepath}")
    df_tripdata = pd.read_csv(
        tripdata_filepath,
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        sep="|",  # data column separator, typically ","
    )
    df_tripdata.drop_duplicates(
        subset=["key_val"], keep="last", inplace=True, ignore_index=False
    )
    df_tripdata["trip_id"] = df_tripdata["key_val"].str.replace("-", "")
    df_tripdata.set_index("key", inplace=True)
    df_trip_data.drop_duplicates(
        subset=["key_val"], keep="last", inplace=True, ignore_index=False
    )
    df_trip_data.set_index("key", inplace=True)
    df = df_trip_data.append(df_tripdata, sort=True)
    df["subscriber_type_new"] = df.apply(
        lambda x: str(x.subscription_type)
        if not str(x.subscriber_type)
        else str(x.subscriber_type),
        axis=1,
    )
    df = df.drop(columns=["subscriber_type"])
    df = resolve_datatypes(df=df, resolve_datatypes_list=resolve_datatypes_list)
    df = rename_headers(df=df, rename_headers_list=rename_headers_list)
    df = reorder_headers(df=df, output_headers_list=reorder_headers_list)
    save_to_new_file(df=df, file_path=target_file, sep="|")
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def listdirs(rootdir: str) -> list:
    rtn_list = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            rtn_list.append(d)
            for elem in listdirs(d):
                rtn_list.append(elem)
    return rtn_list


def download_url_files_from_list(url_list: typing.List[str], dest_path: str) -> None:
    for url in url_list:
        dest_file = dest_path + "/" + os.path.split(url)[1]
        download_file_http(url, dest_file)
        if (
            url.find(".zip") > -1 or url.find(".gz") > -1 or url.find(".tar") > -1
        ) and (url.find("http") == 0 or url.find("gs:") == 0):
            unpack_file(dest_file, dest_path)
        else:
            logging.info(f"Parsing {dest_file} for decompression")


def download_file_http(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    src_file = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in src_file:
            f.write(chunk)


def unpack_file(infile: str, dest_path: str, compression_type: str = "zip") -> None:
    if compression_type == "zip":
        logging.info(f"Unpacking {infile} to {dest_path}")
        zip_decompress(infile=infile, dest_path=dest_path)
    else:
        logging.info(
            f"{infile} ignored as it is not compressed or is of unknown compression"
        )


def zip_decompress(infile: str, dest_path: str) -> None:
    logging.info(f"Unpacking {infile} to {dest_path}")
    with zip.ZipFile(infile, mode="r") as zipf:
        zipf.extractall(dest_path)
        zipf.close()


def stage_input_files(dest_dir: str, target_file_path: str) -> None:
    logging.info("Staging input files")
    for src_dir in listdirs(dest_dir):
        logging.info("-------------------------------------------------------------")
        pool_files(src_dir, dest_dir, "tripdata.csv")
        pool_files(src_dir, dest_dir, "trip_data.csv")
    concatenate_files(target_file_path, dest_dir, "tripdata.csv")
    concatenate_files(target_file_path, dest_dir, "trip_data.csv")


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


def process_source_file(
    source_file: str,
    target_file: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    destination_table: str,
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    date_format_list: dict,
    reorder_headers_list: typing.List[str],
    header_row_ordinal: str = "0",
    field_separator: str = ",",
) -> None:
    logging.info(f"Opening source file {source_file}")
    if header_row_ordinal is None or header_row_ordinal == "None":
        with pd.read_csv(
            source_file,
            engine="python",
            encoding="utf-8",
            quotechar='"',
            chunksize=int(chunksize),  # size of batch data, in no. of records
            sep=field_separator,  # data column separator, typically ","
            names=input_headers,
            dtype=data_dtypes,
            keep_default_na=True,
            na_values=[" "],
        ) as reader:
            for chunk_number, chunk in enumerate(reader):
                target_file_batch = str(target_file).replace(
                    ".csv", "-" + str(chunk_number) + ".csv"
                )
                df = pd.DataFrame()
                df = pd.concat([df, chunk])
                process_chunk(
                    df=df,
                    target_file_batch=target_file_batch,
                    target_file=target_file,
                    skip_header=(not chunk_number == 0),
                    destination_table=destination_table,
                    rename_headers_list=rename_headers_list,
                    empty_key_list=empty_key_list,
                    gen_location_list=gen_location_list,
                    resolve_datatypes_list=resolve_datatypes_list,
                    remove_paren_list=remove_paren_list,
                    strip_newlines_list=strip_newlines_list,
                    strip_whitespace_list=strip_whitespace_list,
                    date_format_list=date_format_list,
                    reorder_headers_list=reorder_headers_list,
                )
    else:
        header = int(header_row_ordinal)
        if data_dtypes != "[]":
            with pd.read_csv(
                source_file,
                engine="python",
                encoding="utf-8",
                quotechar='"',
                chunksize=int(chunksize),  # size of batch data, in no. of records
                sep=field_separator,  # data column separator, typically ","
                header=header,  # use when the data file does not contain a header
                dtype=data_dtypes,
                keep_default_na=True,
                na_values=[" "],
            ) as reader:
                for chunk_number, chunk in enumerate(reader):
                    target_file_batch = str(target_file).replace(
                        ".csv", "-" + str(chunk_number) + ".csv"
                    )
                    df = pd.DataFrame()
                    df = pd.concat([df, chunk])
                    process_chunk(
                        df=df,
                        target_file_batch=target_file_batch,
                        target_file=target_file,
                        skip_header=(not chunk_number == 0),
                        destination_table=destination_table,
                        rename_headers_list=rename_headers_list,
                        empty_key_list=empty_key_list,
                        gen_location_list=gen_location_list,
                        resolve_datatypes_list=resolve_datatypes_list,
                        remove_paren_list=remove_paren_list,
                        strip_newlines_list=strip_newlines_list,
                        strip_whitespace_list=strip_whitespace_list,
                        date_format_list=date_format_list,
                        reorder_headers_list=reorder_headers_list,
                    )
        else:
            with pd.read_csv(
                source_file,
                engine="python",
                encoding="utf-8",
                quotechar='"',
                chunksize=int(chunksize),  # size of batch data, in no. of records
                sep=field_separator,  # data column separator, typically ","
                header=header,  # use when the data file does not contain a header
                keep_default_na=True,
                na_values=[" "],
            ) as reader:
                for chunk_number, chunk in enumerate(reader):
                    target_file_batch = str(target_file).replace(
                        ".csv", "-" + str(chunk_number) + ".csv"
                    )
                    df = pd.DataFrame()
                    df = pd.concat([df, chunk])
                    process_chunk(
                        df=df,
                        target_file_batch=target_file_batch,
                        target_file=target_file,
                        skip_header=(not chunk_number == 0),
                        destination_table=destination_table,
                        rename_headers_list=rename_headers_list,
                        empty_key_list=empty_key_list,
                        gen_location_list=gen_location_list,
                        resolve_datatypes_list=resolve_datatypes_list,
                        remove_paren_list=remove_paren_list,
                        strip_newlines_list=strip_newlines_list,
                        strip_whitespace_list=strip_whitespace_list,
                        date_format_list=date_format_list,
                        reorder_headers_list=reorder_headers_list,
                    )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
    destination_table: str,
    rename_headers_list: typing.List[str],
    empty_key_list: typing.List[str],
    gen_location_list: dict,
    resolve_datatypes_list: dict,
    remove_paren_list: typing.List[str],
    strip_whitespace_list: typing.List[str],
    strip_newlines_list: typing.List[str],
    date_format_list: dict,
    reorder_headers_list: typing.List[str],
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    if destination_table == "311_service_requests":
        df = rename_headers(df, rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = resolve_datatypes(df, resolve_datatypes_list)
        df = remove_parenthesis_long_lat(df, remove_paren_list)
        df = strip_whitespace(df, strip_whitespace_list)
        df = strip_newlines(df, strip_newlines_list)
        df = resolve_date_format(df, date_format_list)
        df = reorder_headers(df, reorder_headers_list)
    elif destination_table == "sffd_service_calls":
        df = rename_headers(df, rename_headers_list)
        df = strip_whitespace(df, strip_whitespace_list)
        df = strip_newlines(df, strip_newlines_list)
        df = extract_latitude_from_geom(df, "location_geom", "latitude")
        df = extract_longitude_from_geom(df, "location_geom", "longitude")
        df = resolve_date_format(df, date_format_list)
        df = reorder_headers(df, reorder_headers_list)
    elif destination_table == "street_trees":
        df = rename_headers(df, rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = resolve_date_format(df, date_format_list)
        df = reorder_headers(df, reorder_headers_list)
    elif destination_table == "sfpd_incidents":
        df = rename_headers(df=df, rename_headers_list=rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = resolve_date_format(df, date_format_list)
        df["timestamp"] = df.apply(
            lambda x: datetime.strftime(
                datetime.strptime(
                    (x["Date"][:10] + " " + x["Time"] + ":00"), "%Y-%m-%d %H:%M:%S"
                ),
                "%Y-%m-%d %H:%M:%S",
            ),
            axis=1,
        )
        df = reorder_headers(df, reorder_headers_list)
    elif destination_table == "bikeshare_station_info":
        df = rename_headers(df, rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = generate_location(df, gen_location_list)
        df = resolve_datatypes(df, resolve_datatypes_list)
        df = reorder_headers(df, reorder_headers_list)
    elif destination_table == "bikeshare_station_status":
        df = rename_headers(df, rename_headers_list)
        df = remove_empty_key_rows(df, empty_key_list)
        df = reorder_headers(df, reorder_headers_list)
    elif destination_table == "bikeshare_trips":
        if str(target_file).find("_trip_data.csv") > -1:
            df = resolve_date_format(df, date_format_list)
        if str(target_file).find("_tripdata.csv") > -1:
            df = resolve_date_format(df, date_format_list)
            df = generate_location(df, gen_location_list)
        df = add_key(df)
    elif destination_table == "film_locations":
        df = rename_headers(df, rename_headers_list)
        df = strip_whitespace(df, strip_whitespace_list)
        df = strip_newlines(df, strip_newlines_list)
        df = reorder_headers(df, reorder_headers_list)
    else:
        pass
    save_to_new_file(df, file_path=str(target_file_batch), sep="|")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


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


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading file {source_file} from {source_url}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def download_file_json(
    source_url: str,
    source_file_json: pathlib.Path,
    source_file_csv: pathlib.Path,
    subnode_name: str,
) -> None:
    logging.info(f"Downloading file {source_url}.json.")
    r = requests.get(source_url, stream=True)
    with open(f"{source_file_json}.json", "wb") as f:
        for chunk in r:
            f.write(chunk)
    df = pd.read_json(f"{source_file_json}.json")["data"][subnode_name]
    df = pd.DataFrame(df)
    df.to_csv(source_file_csv, index=False)


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
        schema_struct = json.loads(blob.download_as_string(client=None))
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


def remove_empty_key_rows(
    df: pd.DataFrame, empty_key_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Removing rows with empty keys")
    for key_field in empty_key_list:
        df = df[df[key_field] != ""]
    return df


def resolve_datatypes(df: pd.DataFrame, resolve_datatypes_list: dict) -> pd.DataFrame:
    logging.info("Resolving datatypes")
    for key, value in resolve_datatypes_list.items():
        if str.lower(value[0:2]) == "int":
            df[key] = df[key].fillna(0).astype(value)
        else:
            df[key] = df[key].astype(value)
    return df


def remove_parenthesis_long_lat(
    df: pd.DataFrame, remove_paren_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Removing parenthesis from geographic fields")
    for paren_fld in remove_paren_list:
        df[paren_fld].replace("(", "", regex=False, inplace=True)
        df[paren_fld].replace(")", "", regex=False, inplace=True)
    return df


def extract_longitude_from_geom(
    df: pd.DataFrame,
    geom_field_name: str,
    lon_field_name: str,
) -> str:
    logging.info(f"Extracting longitude field {lon_field_name} from {geom_field_name}")
    df[lon_field_name] = df[geom_field_name].apply(
        lambda x: str(x).replace("POINT (", "").replace(")", "").split(" ", 1)[0]
        if str(x) != ""
        else "POINT (  )"
    )
    return df


def extract_latitude_from_geom(
    df: pd.DataFrame,
    geom_field_name: str,
    lat_field_name: str,
) -> str:
    logging.info(f"Extracting latitude field {lat_field_name} from {geom_field_name}")
    df[lat_field_name] = df[geom_field_name].apply(
        lambda x: str(x).replace("POINT (", "").replace(")", "").split(" ", 1)[-1]
        if str(x) != ""
        else "POINT (  )"
    )
    return df


def generate_location(df: pd.DataFrame, gen_location_list: dict) -> pd.DataFrame:
    logging.info("Generating location data")
    for key, values in gen_location_list.items():
        logging.info(f"Generating location data for field {key}")
        df[key] = (
            "POINT("
            + df[values[0]][:].astype("string")
            + " "
            + df[values[1]][:].astype("string")
            + ")"
        )
    return df


def strip_whitespace(
    df: pd.DataFrame, strip_whitespace_list: typing.List[str]
) -> pd.DataFrame:
    for ws_fld in strip_whitespace_list:
        logging.info(f"Stripping whitespaces in column {ws_fld}")
        df[ws_fld] = df[ws_fld].apply(lambda x: str(x).strip())
    return df


def strip_newlines(
    df: pd.DataFrame, strip_newlines_list: typing.List[str]
) -> pd.DataFrame:
    for ws_fld in strip_newlines_list:
        logging.info(f"Stripping newlines in column {ws_fld}")
        df[ws_fld] = df[ws_fld].str.replace(r"\n", "", regex=True)
        df[ws_fld] = df[ws_fld].str.replace(r"\r", "", regex=True)
    return df


def resolve_date_format(
    df: pd.DataFrame,
    date_format_list: dict,
) -> pd.DataFrame:
    logging.info("Resolving date formats")
    for dt_fld in date_format_list.items():
        logging.info(f"Resolving date formats in field {dt_fld}")
        df[dt_fld[0]] = df[dt_fld[0]].apply(convert_dt_format, to_format=dt_fld[1])
    return df


def convert_dt_format(dt_str: str, to_format: str = '"%Y-%m-%d %H:%M:%S"') -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    else:
        if to_format.find(" ") > 0:
            # Date and Time
            return str(
                pd.to_datetime(
                    dt_str, format=f"{to_format}", infer_datetime_format=True
                )
            )
        else:
            # Date Only
            return str(
                pd.to_datetime(
                    dt_str, format=f"{to_format}", infer_datetime_format=True
                ).date()
            )


def reorder_headers(
    df: pd.DataFrame, output_headers_list: typing.List[str]
) -> pd.DataFrame:
    logging.info("Re-ordering Headers")
    return df[output_headers_list]


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
        source_url=os.environ.get("SOURCE_URL", ""),
        source_url_dict=json.loads(os.environ.get("SOURCE_URL_DICT", r"{}")),
        source_url_list=json.loads(os.environ.get("SOURCE_URL_LIST", r"[]")),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        chunksize=os.environ.get("CHUNKSIZE", "100000"),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        table_id=os.environ.get("TABLE_ID", ""),
        drop_dest_table=os.environ.get("DROP_DEST_TABLE", "N"),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        header_row_ordinal=os.environ.get("HEADER_ROW_ORDINAL", "None"),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        input_headers=json.loads(os.environ.get("INPUT_CSV_HEADERS", r"[]")),
        data_dtypes=json.loads(os.environ.get("DATA_DTYPES", r"{}")),
        rename_headers_list=json.loads(os.environ.get("RENAME_HEADERS_LIST", r"{}")),
        trip_data_names=json.loads(os.environ.get("TRIP_DATA_NAMES", r"[]")),
        trip_data_dtypes=json.loads(os.environ.get("TRIP_DATA_DTYPES", r"{}")),
        tripdata_names=json.loads(os.environ.get("TRIPDATA_NAMES", r"[]")),
        tripdata_dtypes=json.loads(os.environ.get("TRIPDATA_DTYPES", r"{}")),
        rename_headers_tripdata=json.loads(
            os.environ.get("RENAME_HEADERS_TRIPDATA", r"{}")
        ),
        empty_key_list=json.loads(os.environ.get("EMPTY_KEY_LIST", r"[]")),
        gen_location_list=json.loads(os.environ.get("GEN_LOCATION_LIST", r"{}")),
        resolve_datatypes_list=json.loads(
            os.environ.get("RESOLVE_DATATYPES_LIST", r"{}")
        ),
        remove_paren_list=json.loads(os.environ.get("REMOVE_PAREN_LIST", r"[]")),
        strip_newlines_list=json.loads(os.environ.get("STRIP_NEWLINES_LIST", r"[]")),
        strip_whitespace_list=json.loads(
            os.environ.get("STRIP_WHITESPACE_LIST", r"[]")
        ),
        date_format_list=json.loads(os.environ.get("DATE_FORMAT_LIST", r"[]")),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
    )
