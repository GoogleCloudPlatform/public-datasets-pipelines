import gzip
import json
import logging
import os
import pathlib
import shutil
import subprocess
import typing
import zipfile
from zipfile import ZipFile

from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage


def main(
    download_path: str,
    source_gcs_key: str,
    source_gcs_path: str,
    destination_gcs_path: str,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    schema_filepath: str,
    table_id: str,
    chunk_size: int,
) -> None:
    archive_name = f"{download_path}/data_{table_id}.zip"
    zip_path = os.path.dirname(archive_name)
    unzip_path = f"{zip_path}/{table_id}"
    logging.info(f"zip_path = {zip_path}, unzip_path = {unzip_path}")
    logging.info(f"Removing folder {unzip_path} if it exists")
    shutil.rmtree(unzip_path, ignore_errors=True)
    logging.info(f"Creating folder {unzip_path}")
    pathlib.Path(unzip_path).mkdir(parents=True, exist_ok=True)
    logging.info(f"Creating archive {archive_name}")
    with ZipFile(archive_name, "w"):
        pass
    compress_source_files(
        source_gcs_key=source_gcs_key,
        source_gcs_path=source_gcs_path,
        archive_name=archive_name,
        download_path=download_path,
        project_id=project_id,
        table_id=table_id,
        target_gcs_bucket=target_gcs_bucket,
    )
    upload_file_to_gcs(
        file_path=archive_name,
        target_gcs_bucket=target_gcs_bucket,
        target_gcs_path=f"{destination_gcs_path}/{ os.path.basename(archive_name) }",
    )
    generate_load_batch_data_file(
        input_zip=archive_name,
        project_id=project_id,
        dataset_id=dataset_id,
        target_gcs_bucket=target_gcs_bucket,
        schema_path=schema_filepath,
        table_id=table_id,
        chunk_size=chunk_size,
    )


def compress_source_files(
    source_gcs_key: str,
    source_gcs_path: str,
    archive_name: str,
    download_path: str,
    project_id: str,
    table_id: str,
    target_gcs_bucket: str,
) -> None:
    source_file_names = fetch_gcs_file_names(
        source_gcs_key, source_gcs_path, target_gcs_bucket
    )
    file_ordinal = 0
    for filepath in source_file_names:
        if file_ordinal == 0 or (file_ordinal % 25 == 0):
            logging.info(
                f"Compressing {file_ordinal} files so far, working on it :) ..."
            )
        staged_file = f"{download_path}/{table_id}_{ str(file_ordinal).zfill(15) }.csv"
        download_file_gcs(
            project_id=project_id,
            source_location=f"gs://{target_gcs_bucket}/{filepath}",
            destination_folder=download_path,
            filename_override=os.path.basename(staged_file),
        )
        cmd = f"sed -i '1d' {staged_file}"
        subprocess.check_call(cmd, shell=True)
        append_datafile_to_zipfile(
            zipfile_archive_name=archive_name, append_data_file=staged_file
        )
        os.remove(staged_file)
        file_ordinal += 1


def generate_load_batch_data_file(
    input_zip: str,
    project_id: str,
    dataset_id: str,
    target_gcs_bucket: str,
    schema_path: str,
    table_id: str,
    chunk_size: int,
) -> None:
    zip_path = os.path.dirname(input_zip)
    unzip_path = f"{zip_path}/{table_id}"
    batch_number = 1
    with ZipFile(input_zip, "r") as src_zip:
        listOfFileNames = src_zip.namelist()
        lastFileName = str("".join(sorted(listOfFileNames)[-1:])).strip()
        for fileName in sorted(listOfFileNames):
            unzip_fileName = f"{unzip_path}/{fileName}"
            cmd = f"unzip -p {input_zip} {fileName} > {unzip_fileName}"
            subprocess.run(cmd, shell=True)
            batch_file = f"{unzip_path}/data_batch_{str(batch_number).zfill(15)}.csv"
            number_lines_batch_file = count_lines_file(batch_file)
            number_lines_data_file = count_lines_file(unzip_fileName)
            #  if (this is the last file in the zipfile)
            #     or ( wc-l batch_load_filename + wc -l fileName ) > chunk_size
            if (fileName == lastFileName) or (
                number_lines_batch_file + number_lines_data_file >= chunk_size
            ):
                append_file_to_batchfile(
                    batch_file=batch_file,
                    file_to_append=unzip_fileName,
                    remove_file=True,
                )
                load_source_file_to_bq(
                    target_file=batch_file,
                    target_gcs_bucket=target_gcs_bucket,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    table_id=table_id,
                    schema_path=schema_path,
                    truncate_table=((batch_number == 1)),
                    field_delimiter=",",
                )
                if os.path.exists(batch_file):
                    os.remove(batch_file)
                batch_number += 1
                if fileName != lastFileName:
                    logging.info(f"Processing batch #{batch_number}")
            else:
                append_file_to_batchfile(
                    batch_file=batch_file,
                    file_to_append=unzip_fileName,
                    remove_file=True,
                )


def count_lines_file(input_file: str) -> int:
    cmd = f"wc -l {input_file}"
    returnval = (
        str(subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout)
        .split("\n")[0]
        .split(" ")[0]
    )  # .strip()
    if returnval == "":
        return 0
    else:
        return int(returnval)


def append_file_to_batchfile(
    batch_file: str, file_to_append: str, remove_file: bool = True
) -> None:
    cmd = f"cat {file_to_append} >> {batch_file}"
    subprocess.run(cmd, shell=True)
    number_lines_batch_file = count_lines_file(batch_file)
    number_lines_data_file = count_lines_file(file_to_append)
    logging.info(
        f" ... Appended file { os.path.basename(file_to_append) } ( {number_lines_data_file} rows ) to batch file { os.path.basename(batch_file) } ( {number_lines_batch_file} rows )"
    )
    if remove_file:
        os.remove(file_to_append)


def load_source_file_to_bq(
    target_file: str,
    target_gcs_bucket: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_path: str,
    truncate_table: bool,
    field_delimiter: str,
):
    if os.path.exists(target_file):
        number_lines_batch_file = count_lines_file(target_file)
        logging.info(
            f"Loading batch file {target_file} into table {table_id} with {number_lines_batch_file} rows. truncate table: { str(truncate_table) }"
        )
        table_exists = create_dest_table(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            schema_filepath=schema_path,
            bucket_name=target_gcs_bucket,
            drop_table=False,
        )
        if table_exists:
            load_data_to_bq(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                file_path=target_file,
                truncate_table=truncate_table,
                field_delimiter=field_delimiter,
            )
            os.remove(target_file)
        else:
            error_msg = f"Error: Data was not loaded because the destination table {project_id}.{dataset_id}.{table_id} does not exist and/or could not be created."
            raise ValueError(error_msg)


def gz_decompress(infile: str, tofile: str, delete_zipfile: bool = False) -> None:
    logging.info(f"Decompressing {infile}")
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)
    if delete_zipfile:
        os.remove(infile)


def append_datafile_to_zipfile(
    zipfile_archive_name: str, append_data_file: str
) -> None:
    with zipfile.ZipFile(zipfile_archive_name, "a", zipfile.ZIP_DEFLATED) as my_zip:
        my_zip.write(append_data_file, os.path.basename(append_data_file))


def fetch_gcs_file_names(
    source_gcs_key, source_gcs_path, gcs_bucket
) -> typing.List[str]:
    source_file_names = []
    client = storage.Client()
    blobs = client.list_blobs(gcs_bucket, prefix=source_gcs_path)
    for blob in blobs:
        path = blob.name.split("/")
        if (
            blob.name.endswith("csv")
            and path[-3] == source_gcs_key[0]
            and path[-2] == source_gcs_key[1]
        ):
            source_file_names.append(blob.name)
    logging.info(f"{len(source_file_names)} tables to be loaded in bq")
    return source_file_names


def download_file_gcs(
    project_id: str,
    source_location: str,
    destination_folder: str,
    filename_override: str = "",
) -> None:
    object_name = os.path.basename(source_location)
    if filename_override == "":
        dest_object = f"{destination_folder}/{object_name}"
    else:
        dest_object = f"{destination_folder}/{filename_override}"
    storage_client = storage.Client(project_id)
    bucket_name = str.split(source_location, "gs://")[1].split("/")[0]
    bucket = storage_client.bucket(bucket_name)
    source_object_path = str.split(source_location, f"gs://{bucket_name}/")[1]
    blob = bucket.blob(source_object_path)
    blob.download_to_filename(dest_object)


def create_dest_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema_filepath: list,
    bucket_name: str,
    drop_table: bool = False,
) -> bool:
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
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
    job_config.autodetect = False
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()


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
        download_path=os.environ.get("DOWNLOAD_PATH", ""),
        source_gcs_key=json.loads(os.environ.get("SOURCE_GCS_KEY")),
        source_gcs_path=os.environ.get("SOURCE_GCS_PATH"),
        destination_gcs_path=os.environ.get("DESTINATION_GCS_PATH"),
        project_id=os.environ.get("PROJECT_ID"),
        dataset_id=os.environ.get("DATASET_ID"),
        target_gcs_bucket=os.environ.get("GCS_BUCKET"),
        schema_filepath=os.environ.get("SCHEMA_FILEPATH"),
        table_id=os.environ.get("TABLE_ID"),
        chunk_size=int(os.environ.get("CHUNK_SIZE")),
    )
