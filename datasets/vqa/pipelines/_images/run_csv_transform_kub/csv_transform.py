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

import io
import json
import logging
import os
import pathlib
import typing
from datetime import datetime
from zipfile import ZipFile

import pandas as pd
import requests
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    pipeline_name: str,
    source_url: typing.List[typing.List[str]],
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    load_file_list: dict,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_path: str,
    schema_detail_data_path: str,
    drop_dest_table: str,
    remove_source_file: str,
    delete_target_file: str,
    reorder_headers_list: typing.List[str],
    detail_data_headers_list: typing.List[str],
) -> None:
    logging.info(f"{pipeline_name} process started")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    execute_pipeline(
        pipeline_name=pipeline_name,
        source_url=source_url,
        source_file=source_file,
        target_file=target_file,
        load_file_list=load_file_list,
        project_id=project_id,
        dataset_id=dataset_id,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=target_gcs_path,
        schema_filepath=schema_path,
        schema_detail_data_filepath=schema_detail_data_path,
        drop_dest_table=drop_dest_table,
        remove_source_file=(remove_source_file == "Y"),
        delete_target_file=(delete_target_file == "Y"),
        reorder_headers_list=reorder_headers_list,
        detail_data_headers_list=detail_data_headers_list,
    )
    logging.info(f"{pipeline_name} process completed")


def execute_pipeline(
    pipeline_name: str,
    source_url: typing.List[typing.List[str]],
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    load_file_list: typing.List[dict],
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    schema_filepath: str,
    schema_detail_data_filepath: str,
    drop_dest_table: str,
    remove_source_file: bool,
    delete_target_file: bool,
    reorder_headers_list: typing.List[str],
    detail_data_headers_list: typing.List[str],
) -> None:
    if "Extract " in pipeline_name:
        for subtask, url, table_name, schema_filepath, schema_detail_data_filepath, src_filename in source_url:
            logging.info(f"... Executing Extraction Process for {subtask}")
            source_zipfile = str.replace(str(source_file), ".csv", f"{table_name}.zip")
            root_path = os.path.split(source_zipfile)[0]
            target_file_path_main = str.replace(
                str(target_file), ".csv", f"_{table_name}.csv"
            )
            download_file(url, source_zipfile)
            zip_decompress(source_zipfile, root_path, False)
            if pipeline_name == "Extract Annotations":
                normalize_tag_source = "annotations"
                normalize_tag_dest="annot_norm"
                target_file_path_detail = str.replace(
                    str(target_file), ".csv", f"_{table_name}_{normalize_tag_dest}.csv"
                )
                extract_transform_file(
                    url=url,
                    src_filename=src_filename,
                    target_file_path_main=target_file_path_main,
                    target_file_path_detail=target_file_path_detail,
                    root_path=root_path,
                    reorder_headers_list=reorder_headers_list,
                    detail_data_headers_list=detail_data_headers_list,
                    normalize_tag_source=normalize_tag_source
                )
                load_target_file(
                    target_file=target_file_path_main,
                    target_gcs_bucket=target_gcs_bucket,
                    target_gcs_path=target_gcs_path,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    destination_table=table_name,
                    schema_filepath=schema_filepath,
                    source_url=url
                )
                load_target_file(
                    target_file=target_file_path_detail,
                    target_gcs_bucket=target_gcs_bucket,
                    target_gcs_path=target_gcs_path,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    destination_table=f"{table_name}_detail",
                    schema_filepath=schema_detail_data_filepath,
                    source_url=url
                )
            elif pipeline_name == "Extract Questions":
                normalize_tag_source = "questions"
                normalize_tag_dest="questions"
                target_file_path_detail = str.replace(
                    str(target_file), ".csv", f"_{table_name}_{normalize_tag_dest}.csv"
                )
                extract_transform_file(
                    url=url,
                    src_filename=src_filename,
                    target_file_path_main=target_file_path_main,
                    target_file_path_detail=target_file_path_detail,
                    root_path=root_path,
                    reorder_headers_list=reorder_headers_list,
                    detail_data_headers_list=detail_data_headers_list,
                    normalize_tag_source=normalize_tag_source
                )
                load_target_file(
                    target_file=target_file_path_main,
                    target_gcs_bucket=target_gcs_bucket,
                    target_gcs_path=target_gcs_path,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    destination_table=table_name,
                    schema_filepath=schema_filepath,
                    source_url=url
                )
                load_target_file(
                    target_file=target_file_path_detail,
                    target_gcs_bucket=target_gcs_bucket,
                    target_gcs_path=target_gcs_path,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    destination_table=f"{table_name}_detail",
                    schema_filepath=schema_detail_data_filepath,
                    source_url=url
                )
            elif pipeline_name == "Extract Complementary Pairs":
                for src in src_filename:
                    logging.info(f"    ... Processing file {root_path}/{src}")
                    target_file_path_pairs = str.replace( str(target_file), ".csv", f"_{table_name}_pairs.csv")
                    if (
                        convert_comp_pairs_file_to_csv(f"{root_path}/{src}", target_file_path_pairs, url)
                        != ""
                    ):
                        logging.info(
                            f"        ... {target_file_path_pairs} was created."
                        )
                    else:
                        logging.info(
                            f"        ... {target_file_path_pairs} was not created."
                        )
                    # import pdb; pdb.set_trace()
                    load_target_file(
                        target_file=target_file_path_pairs,
                        target_gcs_bucket=target_gcs_bucket,
                        target_gcs_path=target_gcs_path,
                        project_id=project_id,
                        dataset_id=dataset_id,
                        destination_table=f"{table_name}",
                        schema_filepath=schema_filepath,
                        source_url=url
                    )
            else:
                pass
    else:
        pass
    if pipeline_name == "Load Images":
        for subtask, url, dest_gcs_bucket, dest_gcs_path in source_url:
            source_zipfile_filename = os.path.split(url)[1]
            dest_zipfile_path = os.path.split(source_file)[0]
            source_zipfile = f"{dest_zipfile_path}/{source_zipfile_filename}"
            download_file(url, source_zipfile)
            upload_file_to_gcs(
                file_path=source_zipfile,
                target_gcs_bucket=dest_gcs_bucket,
                target_gcs_path=dest_gcs_path,
            )
            zip_extract_in_gcs(dest_gcs_bucket, f"{dest_gcs_path}/{source_zipfile_filename}")

def extract_transform_file(
    url: str,
    src_filename: str,
    target_file_path_main: str,
    target_file_path_detail: str,
    root_path: str,
    reorder_headers_list: typing.List[str],
    detail_data_headers_list: typing.List[str],
    normalize_tag_source: str #,
    # normalize_tag_dest: str,
) -> bool:
    file_counter = 0
    for src in src_filename:
        logging.info(f"    ... Processing file {root_path}/{src}")
        data = json.load(open(f"{root_path}/{src}"))
        df_main = pd.json_normalize(data)
        df_detail = pd.DataFrame()
        df_detail = df_main[normalize_tag_source].apply(
            lambda x: pd.json_normalize(x)
        )[0][:][detail_data_headers_list]
        df_main = rename_headers(df_main)
        df_main = df_main[reorder_headers_list]
        df_main = add_metadata_cols(df_main, url)
        save_to_new_file(
            df_main, target_file_path_main, sep="|", include_headers=(file_counter == 0)
        )
        if os.path.exists(target_file_path_main):
            logging.info(
                f"        ... Extracted {normalize_tag_source} to {target_file_path_main}"
            )
        df_detail = add_metadata_cols(df_detail, url)
        save_to_new_file(
            df_detail,
            target_file_path_detail,
            sep="|",
            include_headers=(file_counter == 0),
        )
        if os.path.exists(target_file_path_main):
            logging.info(
                f"        ... Extracted {normalize_tag_source} detail data to {target_file_path_detail}"
            )
        file_counter += 1
    if os.path.exists(target_file_path_main) and os.path.exists(
        target_file_path_detail
    ):
        return True
    else:
        return False


def load_target_file(
    target_file: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    project_id: str,
    dataset_id: str,
    destination_table: str,
    schema_filepath: str,
    source_url: str
) -> None:
    if os.path.exists(target_file):
        upload_file_to_gcs(
            file_path=target_file,
            target_gcs_bucket=target_gcs_bucket,
            target_gcs_path=target_gcs_path,
        )
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=destination_table,
            schema_filepath=schema_filepath,
            bucket_name=target_gcs_bucket,
        )
        if table_exists:
            delete_source_file_data_from_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=destination_table,
                source_url=source_url,
            )
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=destination_table,
                file_path=target_file,
                truncate_table=True,
                field_delimiter="|"
            )
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{destination_table} does not exist and/or could not be created."
            raise ValueError(error_msg)
    else:
        logging.info(
            f"Informational: The data file {target_file} was not generated because no data file was available.  Continuing."
        )


def convert_comp_pairs_file_to_csv(src_json: str, destination_csv: str, source_url: str = "") -> str:
    source_url = str.replace(source_url, "/", "\/")
    etl_timestamp = datetime.today().isoformat().replace('T', ' ')
    command = ( f"sed -i -e 's/\\], \\[/\\n/g' {src_json} "
                f"&& sed -i -e 's/,/\\|/g' {src_json} "
                f"&& sed -i -e 's/\\[//g' {src_json} "
                f"&& sed -i -e 's/\\]//g' {src_json} "
                f"&& sed -i -e 's/ //g' {src_json} "
                f"&& sed -i -e 's/$/|{source_url}/g' {src_json} "
                f"&& sed -i -e 's/$/|{etl_timestamp}/g' {src_json} "
                f"&& echo 'question_id_1|question_id_2|source_url|etl_timestamp' > {destination_csv}"
                f"&& cat {src_json} >> {destination_csv}"
                )
    logging.info(command)
    os.system(command)
    if os.path.exists(destination_csv):
        return destination_csv
    else:
        return ""


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"    ... Downloading {source_url} to {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def zip_decompress(infile: str, topath: str, remove_zipfile: bool = False) -> None:
    logging.info(f"    ... Decompressing {infile} to {topath}")
    with ZipFile(infile, "r") as zip:
        zip.extractall(topath)
    if remove_zipfile:
        os.unlink(infile)


def zip_extract_in_gcs(bucketname: str, zipfilename_with_path: str) -> None:
    logging.info(f"    ... Extracting {zipfilename_with_path} to {bucketname}")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucketname)
    blob = bucket.blob(zipfilename_with_path)
    logging.info("        ... Reading zipfile data")
    zipbytes = io.BytesIO(blob.download_as_string())
    with ZipFile(zipbytes, 'r') as myzip:
        file_count = len(myzip.infolist())
        logging.info(f"            ... Count of files to extract: {file_count} ")
        process_file_counter = 0
        for contentfilename in myzip.namelist():
            # if process_file_counter == 0 or (((process_file_counter / file_count) * 100 ) % 1 == 0):
            progress_bar(process_file_counter, file_count)
        #    import pdb; pdb.set_trace()
            contentfile = myzip.read(contentfilename)
            contentzippath = f"{zipfilename_with_path}/{contentfilename}"
            blob = bucket.blob(contentzippath)
            blob.upload_from_string(contentfile)
            process_file_counter += 1
        import pdb; pdb.set_trace()

# for dir in zip_ref.namelist():
#     if dir.endswith('/'):
#         subdirs_list.append(os.path.basename(os.path.normpath(dir)))

def progress_bar(progress: float, total: float) -> None:
    percent = (100 * (progress / float(total)))
    bar = '*' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}", end="\r")


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        new_col_name = str.replace(str(col), ".", "_")
        df.rename(columns={col: new_col_name}, inplace=True)
    return df


def save_to_new_file(
    df: pd.DataFrame, file_path: str, sep: str = "|", include_headers: bool = True
) -> None:
    logging.info(f"        ... Saving data to target file.. {file_path} ...")
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
    logging.info("        ... Adding metadata columns")
    df["source_url"] = source_url
    df["etl_timestamp"] = pd.to_datetime(
        datetime.now(), format="%Y-%m-%d %H:%M:%S", infer_datetime_format=True
    )
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


def upload_file_to_gcs(
    file_path: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    if os.path.exists(file_path):
        target_path = os.path.split(target_gcs_path)[0]
        filename = os.path.split(file_path)[1]
        target_filepath = f"{target_path}/{filename}"
        logging.info(
            f"Uploading output file to gs://{target_filepath}"
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket(target_gcs_bucket)
        blob = bucket.blob(target_filepath)
        blob.upload_from_filename(file_path)
    else:
        logging.info(
            f"Cannot upload file {file_path} to gs://{target_filepath} as it does not exist."
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        source_url=json.loads(os.environ.get("SOURCE_URL", r"[[]]")),
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        target_file=pathlib.Path(os.environ.get("TARGET_FILE", "")).expanduser(),
        load_file_list=json.loads(os.environ.get("LOAD_FILE_LIST", r"{}")),
        project_id=os.environ.get("PROJECT_ID", ""),
        dataset_id=os.environ.get("DATASET_ID", ""),
        drop_dest_table=os.environ.get("DROP_DEST_TABLE", "N"),
        schema_path=os.environ.get("SCHEMA_PATH", ""),
        schema_detail_data_path=os.environ.get("SCHEMA_DETAIL_DATA_PATH", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        remove_source_file=os.environ.get("REMOVE_SOURCE_FILE", "N"),
        delete_target_file=os.environ.get("DELETE_TARGET_FILE", "N"),
        reorder_headers_list=json.loads(os.environ.get("REORDER_HEADERS_LIST", r"[]")),
        detail_data_headers_list=json.loads(
            os.environ.get("DETAIL_DATA_HEADERS_LIST", r"[]")
        ),
    )
