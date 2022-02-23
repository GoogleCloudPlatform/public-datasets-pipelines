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

import pandas as pd
import requests
<<<<<<< HEAD
from google.cloud import bigquery, storage
=======
from google.cloud import storage
>>>>>>> upstream/main


def main(
    source_url: str,
    start_year: int,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
<<<<<<< HEAD
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:
    logging.info("Pipeline process started")
=======
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    data_names: typing.List[str],
    data_dtypes: dict,
) -> None:

    logging.info("Pipeline process started")

>>>>>>> upstream/main
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    dest_path = os.path.split(source_file)[0]
    end_year = datetime.datetime.today().year - 2
    download_url_files_from_year_range(
        source_url, start_year, end_year, dest_path, True, False
    )
    st_year = datetime.datetime.today().year - 1
    end_year = datetime.datetime.today().year
    download_url_files_from_year_range(
        source_url, st_year, end_year, dest_path, True, True
    )
    file_group_wildcard = os.path.split(source_url)[1].replace("_YEAR_ITERATOR.zip", "")
    source = concatenate_files(source_file, dest_path, file_group_wildcard, False, ",")
<<<<<<< HEAD
    process_source_file(source, target_file, input_headers, data_dtypes, output_headers, int(chunksize))
    if os.path.exists(target_file):
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
        create_dest_table(
            project_id, dataset_id, table_id, schema_path, target_gcs_bucket
        )
        load_data_to_bq(project_id, dataset_id, table_id, target_file)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data was available."
        )
    logging.info("Pipeline process completed")


def load_data_to_bq(
    project_id: str, dataset_id: str, table_id: str, file_path: str
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1  # ignore the header
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} completed"
    )


=======

    process_source_file(source, target_file, data_names, data_dtypes, int(chunksize))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("Pipeline process completed")


>>>>>>> upstream/main
def download_url_files_from_year_range(
    source_url: str,
    start_year: int,
    end_year: int,
    dest_path: str,
    remove_file: bool = False,
    continue_on_error: bool = False,
<<<<<<< HEAD
) -> None:
    for yr in range(start_year, end_year + 1, 1):
        src_url = source_url.replace("YEAR_ITERATOR", str(yr))
        dest_file = dest_path + "/source_" + os.path.split(src_url)[1]
        file_exists = download_file_http(src_url, dest_file, continue_on_error)
        if file_exists:
            unpack_file(dest_file, dest_path, "zip")
            if remove_file:
                os.remove(dest_file)
=======
):
    for yr in range(start_year, end_year + 1, 1):
        src_url = source_url.replace("YEAR_ITERATOR", str(yr))
        dest_file = dest_path + "/source_" + os.path.split(src_url)[1]
        download_file_http(src_url, dest_file, continue_on_error)
        unpack_file(dest_file, dest_path, "zip")
        if remove_file:
            os.remove(dest_file)
>>>>>>> upstream/main


def download_file_http(
    source_url: str, source_file: pathlib.Path, continue_on_error: bool = False
<<<<<<< HEAD
) -> bool:
    logging.info(f"Downloading {source_url} to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        rtn_status_code = src_file.status_code
        if 400 <= rtn_status_code <= 499:
            logging.info(
                f"Unable to download file {source_url} (error code was {rtn_status_code})"
            )
            return False
        else:
            with open(source_file, "wb") as f:
                for chunk in src_file:
                    f.write(chunk)
            return True
=======
) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    try:
        src_file = requests.get(source_url, stream=True)
        with open(source_file, "wb") as f:
            for chunk in src_file:
                f.write(chunk)
>>>>>>> upstream/main
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
<<<<<<< HEAD
            logging.info(f"{err_msg} Unable to obtain {source_url}.")
        return False
=======
            logging.info(
                f"{err_msg} Unable to obtain {source_url}. Continuing execution."
            )
>>>>>>> upstream/main


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


def concatenate_files(
    target_file_path: str,
    dest_path: str,
    file_group_wildcard: str,
    incl_file_source_path: bool = False,
    separator: str = ",",
    delete_src_file: bool = True,
) -> str:
    target_file_dir = os.path.split(str(target_file_path))[0]
    target_file_path = str(target_file_path).replace(
        ".csv", "_" + file_group_wildcard + ".csv"
    )
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
                            '"'
                            + os.path.split(src_file_path)[1].strip()
                            + '"'
                            + separator
                            + line
                        )  # include the file source
                    else:
                        line = line
                    target_file.write(line)
        if os.path.isfile(src_file_path) and delete_src_file:
            os.unlink(src_file_path)

    return target_file_path


<<<<<<< HEAD
def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_filepath: list,
    bucket_name: str,
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logging.info(f"Attempting to create table {table_ref} if it doesn't already exist")
    client = bigquery.Client()
    success = False
    try:
        table_exists_id = client.get_table(table_ref).table_id
        logging.info(f"Table {table_exists_id} currently exists.")
        success = True
    except NotFound:
        logging.info(
            (
                f"Table {table_ref} currently does not exist.  Attempting to create table."
            )
        )
        schema = create_table_schema([], bucket_name, schema_filepath)
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Table {table_ref} was created".format(table_id))
        success = True
    return success


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


def process_source_file(
    source_file: str,
    target_file: str,
    input_headers: list,
    dtypes: dict,
    chunksize: str
=======
def process_source_file(
    source_file: str, target_file: str, names: list, dtypes: dict, chunksize: int
>>>>>>> upstream/main
) -> None:
    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
<<<<<<< HEAD
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=None,  # use when the data file does not contain a header
        names=input_headers,
=======
        chunksize=chunksize,  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=None,  # use when the data file does not contain a header
        names=names,
>>>>>>> upstream/main
        dtype=dtypes,
        keep_default_na=True,
        na_values=[" "],
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
<<<<<<< HEAD
            process_chunk(df,
                          target_file_batch,
                          target_file,
                          (not chunk_number == 0)
            )
=======
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))
>>>>>>> upstream/main


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    skip_header: bool,
) -> None:
    df = resolve_date_format(df, "%Y-%m-%d %H:%M")
    save_to_new_file(df, file_path=str(target_file_batch), sep=",")
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def resolve_date_format(df: pd.DataFrame, from_format: str) -> pd.DataFrame:
    logging.info("Resolving Date Format")
    for col in df.columns:
        if df[col].dtype == "datetime64[ns]":
            logging.info(f"Resolving datetime on {col}")
            df[col] = df[col].apply(lambda x: convert_dt_format(str(x), from_format))

    return df


def convert_dt_format(dt_str: str, from_format: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        rtnval = ""
    elif len(dt_str.strip()) == 10:
        # if there is no time format
        rtnval = dt_str + " 00:00:00"
    elif len(dt_str.strip().split(" ")[1]) == 8:
        # if format of time portion is 00:00:00 then use 00:00 format
        dt_str = dt_str[:-3]
        rtnval = datetime.datetime.strptime(dt_str, from_format).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif (len(dt_str.strip().split("-")[0]) == 4) and (
        len(from_format.strip().split("/")[0]) == 2
    ):
        # if the format of the date portion of the data is in YYYY-MM-DD format
        # and from_format is in MM-DD-YYYY then resolve this by modifying the from_format
        # to use the YYYY-MM-DD.  This resolves mixed date formats in files
        from_format = "%Y-%m-%d " + from_format.strip().split(" ")[1]
    else:
        dt_str = ""

    return rtnval


def save_to_new_file(df, file_path, sep="|") -> None:
    logging.info(f"Saving to file {file_path} separator='{sep}'")
    df.to_csv(file_path, sep=sep, index=False)


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


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info(f"Uploading to GCS {gcs_bucket} in {gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
<<<<<<< HEAD
        start_year=int(os.environ["START_YEAR"]),
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        project_id=os.environ["PROJECT_ID"],
        dataset_id=os.environ["DATASET_ID"],
        table_id=os.environ["TABLE_ID"],
        schema_path=os.environ["SCHEMA_PATH"],
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        input_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        output_headers=json.loads(os.environ["OUTPUT_CSV_HEADERS"]),
=======
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        start_year=int(os.environ["START_YEAR"]),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        data_names=json.loads(os.environ["DATA_NAMES"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
>>>>>>> upstream/main
    )
