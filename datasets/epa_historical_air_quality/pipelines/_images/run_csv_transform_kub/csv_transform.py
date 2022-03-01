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

import datetime
import json
import logging
import os
import pathlib
import typing
import zipfile as zip

import pandas as pd
import requests
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound


def main(
    source_url: str,
    start_year: int,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    pipeline_name: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:
    logging.info("Pipeline process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    dest_path = os.path.split(source_file)[0]
    execute_pipeline(
        project_id=project_id,
        dataset_id=dataset_id,
        table_name=table_id,
        start_year=start_year,
        year_field_name="date_local",
        source_url=source_url,
        dest_path=dest_path,
        schema_path=schema_path,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        input_headers=input_headers,
        output_headers=output_headers,
        data_dtypes=data_dtypes,
        chunksize=chunksize,
        field_delimiter="|",
    )
    logging.info("Pipeline process completed")


def execute_pipeline(
    project_id: str,
    dataset_id: str,
    table_name: str,
    start_year: str,
    year_field_name: str,
    source_url: str,
    dest_path: str,
    schema_path: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    output_headers: typing.List[str],
    data_dtypes: dict,
    chunksize: str,
    field_delimiter: str,
) -> None:
    create_dest_table(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_name,
        schema_filepath=schema_path,
        bucket_name=target_gcs_bucket,
    )
    end_year = datetime.datetime.today().year - 2
    for yr in range(start_year, end_year + 1, 1):
        process_year_data(
            project_id=project_id,
            dataset_id=dataset_id,
            table_name=table_name,
            year_field_name=year_field_name,
            year=yr,
            continue_on_error=False,
            source_url=source_url,
            dest_path=dest_path,
            input_headers=input_headers,
            output_headers=output_headers,
            data_dtypes=data_dtypes,
            chunksize=chunksize,
            field_delimiter=field_delimiter,
        )
    st_year = datetime.datetime.today().year - 1
    end_year = datetime.datetime.today().year
    for yr in range(st_year, end_year + 1, 1):
        process_year_data(
            project_id=project_id,
            dataset_id=dataset_id,
            table_name=table_name,
            year_field_name=year_field_name,
            year=yr,
            continue_on_error=True,
            source_url=source_url,
            dest_path=dest_path,
            input_headers=input_headers,
            output_headers=output_headers,
            data_dtypes=data_dtypes,
            chunksize=chunksize,
            field_delimiter=field_delimiter,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )


def process_year_data(
    project_id: str,
    dataset_id: str,
    table_name: str,
    year_field_name: str,
    year: str,
    continue_on_error: bool,
    source_url: str,
    dest_path: str,
    input_headers: typing.List[str],
    output_headers: typing.List[str],
    data_dtypes: dict,
    chunksize: str,
    field_delimiter: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    remove_file: bool = True,
):
    logging.info(f"Processing year {year} data.")
    if table_has_year_data(project_id, dataset_id, table_name, year_field_name, year):
        pass
    else:
        src_url = source_url.replace("YEAR_ITERATOR", str(year))
        url_file = os.path.split(src_url)[1]
        url_file_csv = url_file.replace(".zip", ".csv")
        source_file = f"{dest_path}/source_{url_file}"
        source_csv_file = f"{dest_path}/{url_file_csv}"
        target_file = f"{dest_path}/target_{url_file_csv}"
        file_exists = download_file_http(
            source_url=src_url,
            source_file=source_file,
            continue_on_error=continue_on_error,
        )
        if file_exists:
            unpack_file(infile=source_file, dest_path=dest_path, compression_type="zip")
            process_source_file(
                source_file=source_file,
                target_file=target_file,
                input_headers=input_headers,
                output_headers=output_headers,
                dtypes=data_dtypes,
                chunksize=chunksize,
                field_delimiter=field_delimiter,
            )
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_name,
                file_path=target_file,
                field_delimiter=field_delimiter,
            )
            if os.path.exists(target_file):
                upload_file_to_gcs(
                    file_path=target_file,
                    target_gcs_bucket=target_gcs_bucket,
                    target_gcs_path=target_gcs_path,
                )
            if remove_file:
                os.remove(source_file)
                os.remove(source_csv_file)
                os.remove(target_file)
            else:
                pass
        else:
            pass
    logging.info(f"Processing year {year} data completed.")


def table_has_year_data(
    project_id: str, dataset_id: str, table_name: str, year_field_name: str, year: str
) -> bool:
    if (
        number_rows_in_table(project_id, dataset_id, table_name, year_field_name, year)
        > 0
    ):
        return True
    else:
        return False


def number_rows_in_table(
    project_id: str, dataset_id: str, table_name: str, year_field_name: str, year: str
) -> int:
    client = bigquery.Client(project=project_id)
    query = f"""
        SELECT count(1) AS number_of_rows
        FROM {dataset_id}.{table_name}
        WHERE FORMAT_DATE('%Y', {year_field_name}) = '{year}'
    """
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query, job_config=job_config)
    for row in query_job.result():
        count_rows = row.number_of_rows
    return int(count_rows)


def process_source_file(
    source_file: str,
    target_file: str,
    input_headers: typing.List[str],
    output_headers: typing.List[str],
    dtypes: dict,
    chunksize: str,
    field_delimiter: str,
) -> None:
    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=int(chunksize),  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        header=0,  # use when the data file does not contain a header
        names=input_headers,
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
            process_chunk(
                df=df,
                target_file_batch=target_file_batch,
                target_file=target_file,
                include_header=(chunk_number == 0),
                truncate_file=(chunk_number == 0),
                field_delimiter=field_delimiter,
                output_headers=output_headers,
            )


def load_data_to_bq(
    project_id: str,
    dataset_id: str,
    table_id: str,
    file_path: str,
    field_delimiter: str,
) -> None:
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} delim={field_delimiter} started"
    )
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = field_delimiter
    job_config.skip_leading_rows = 1
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(
            file_obj=source_file, destination=table_ref, job_config=job_config
        )
    job.result()
    logging.info(
        f"Loading data from {file_path} into {project_id}.{dataset_id}.{table_id} completed"
    )


def download_file_http(
    source_url: str, source_file: pathlib.Path, continue_on_error: bool = False
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
            logging.info(f"{err_msg} Unable to obtain {source_url}.")
        return False


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


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    include_header: bool,
    truncate_file: bool,
    field_delimiter: str,
    output_headers: typing.List[str],
) -> None:
    df = resolve_date_format(df, "%Y-%m-%d %H:%M")
    df = df[output_headers]
    save_to_new_file(df=df, file_path=str(target_file_batch), sep=field_delimiter)
    append_batch_file(
        batch_file_path=target_file_batch,
        target_file_path=target_file,
        include_header=include_header,
        truncate_target_file=truncate_file,
    )
    logging.info(f"Processing Batch {target_file_batch} completed")


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
    batch_file_path: str,
    target_file_path: str,
    include_header: bool,
    truncate_target_file: bool,
) -> None:
    logging.info(
        f"Appending file {batch_file_path} to file {target_file_path} with include_header={include_header} and truncate_target_file={truncate_target_file}"
    )
    data_file = open(batch_file_path, "r")
    if truncate_target_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if not include_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} without header"
        )
        next(data_file)
    else:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with header"
        )
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
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
        source_url=os.environ["SOURCE_URL"],
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
        pipeline_name=os.environ["PIPELINE_NAME"],
        input_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        output_headers=json.loads(os.environ["OUTPUT_CSV_HEADERS"]),
    )
