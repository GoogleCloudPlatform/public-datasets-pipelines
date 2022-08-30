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
import logging
import os
import pathlib
import typing
from zipfile import ZipFile

import pandas as pd
import requests
from google.cloud import storage

# from numpy import source


def main(
    source_bucket: str,
    source_object: str,
    source_url: str,
    source_file_zip_file: pathlib.Path,
    source_file_path: pathlib.Path,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    csv_headers: typing.List[str],
    # rename_mappings: dict,
    chunksize: str,
    pipeline_name: str,
) -> None:

    logging.info(
        f"FEC{pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    if "individuals" not in pipeline_name:
        logging.info(f"Downloading file from {source_url}...")
        download_file(source_url, source_file_zip_file)
        unzip_file(source_file_zip_file, source_file_path)

        logging.info(f"Opening file {source_file}...")
        df = pd.read_table(
            source_file,
            sep="|",
            header=None,
            names=csv_headers,
            dtype=object,
            index_col=False,
        )

        logging.info(f"Transforming {source_file}... ")

        # logging.info("Transform: Rename columns... ")
        # rename_headers(df, rename_mappings)

        if "candidate_20" in pipeline_name:
            logging.info("Transform: Trimming white spaces in headers... ")
            df = df.rename(columns=lambda x: x.strip())

        elif "committee_20" in pipeline_name:
            df.drop(df[df["cmte_id"] == "C00622357"].index, inplace=True)

        elif "committee_contributions_20" in pipeline_name:
            df["transaction_dt"] = df["transaction_dt"].astype(str)
            # df["transaction_dt"] = df["transaction_dt"].str[:-2]
            date_for_length(df, "transaction_dt")
            df = resolve_date_format(df, "transaction_dt", pipeline_name)

        elif "other_committee_tx_20" in pipeline_name:
            df["transaction_dt"] = df["transaction_dt"].astype(str)
            # df["transaction_dt"] = df["transaction_dt"].str[:-2]
            date_for_length(df, "transaction_dt")
            df = resolve_date_format(df, "transaction_dt", pipeline_name)

        elif "opex" in pipeline_name:
            df["transaction_dt"] = df["transaction_dt"].astype(str)
            # df["transaction_dt"] = df["transaction_dt"].str[:-2]
            date_for_length(df, "transaction_dt")
            df = resolve_date_format(df, "transaction_dt", pipeline_name)

        # elif pipeline_name == "individuals_":
        #     df["transaction_dt"] = df["transaction_dt"].astype(str)
        #     #df["transaction_dt"] = df["transaction_dt"].str[:-2]
        #     date_for_length(df, "transaction_dt")
        #     df = resolve_date_format(df, "transaction_dt", pipeline_name)
        #     df = df.rename(columns=lambda x: x.strip())

        else:
            pass

        logging.info(f"Saving to output file.. {target_file}")
        try:
            save_to_new_file(df, file_path=str(target_file))
        except Exception as e:
            logging.error(f"Error saving output file: {e}.")

        logging.info(
            f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

        logging.info(
            f"FEC {pipeline_name} process completed at "
            + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
    else:
        logging.info(f"Downloading file gs://{source_bucket}/{source_object}")
        # download_blob(source_bucket, source_object, source_file)

        process_source_file(source_file, target_file, chunksize, pipeline_name)

        logging.info(
            f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

        logging.info(
            f"FEC {pipeline_name} process completed at "
            + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )


def process_source_file(
    source_file: str,
    target_file: str,
    chunksize: str,
    pipeline_name: str,
) -> None:
    logging.info(f"Opening source file {source_file}")
    csv.field_size_limit(512 << 10)
    csv.register_dialect("TabDialect", quotechar='"', delimiter="\t", strict=True)
    with open(
        source_file,
    ) as reader:
        data = []
        chunk_number = 1
        print("process_source_file is good")
        for index, line in enumerate(csv.reader(reader, "TabDialect"), 0):
            data.append(line)
            if index % int(chunksize) == 0 and index > 0:
                process_dataframe_chunk(
                    data,
                    target_file,
                    chunk_number,
                    source_file,
                    pipeline_name,
                )
                data = []
                chunk_number += 1

        if data:
            process_dataframe_chunk(
                data,
                target_file,
                chunk_number,
                source_file,
                pipeline_name,
            )


def process_dataframe_chunk(
    data: typing.List[str],
    target_file: str,
    chunk_number: int,
    csv_headers: list,
    pipeline_name: str,
) -> None:
    print("coming into process_dataframe_chunk")
    # print(data)
    for item in data:
        for char in item:
            char = char.split("|")
    print(data)
    df = pd.DataFrame(data, columns=csv_headers)
    print(df.head())
    print("prblm is with batch")
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        target_file_batch=target_file_batch,
        target_file=target_file,
        pipeline_name=pipeline_name,
    )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    pipeline_name: str,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df["transaction_dt"] = df["transaction_dt"].astype(str)
    date_for_length(df, "transaction_dt")
    df = resolve_date_format(df, "transaction_dt", pipeline_name)
    df = df.rename(columns=lambda x: x.strip())
    save_to_new_file(df, file_path=str(target_file_batch), sep=",")
    append_batch_file(target_file_batch, target_file)
    logging.info(f"Processing batch file {target_file_batch} completed")


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = ",") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=",")


def append_batch_file(target_file_batch: str, target_file: str) -> None:

    with open(target_file_batch, "r") as data_file:
        with open(target_file, "a+") as target_file:
            logging.info(f"Appending batch file {target_file_batch} to {target_file}")
            target_file.write(data_file.read())
            if os.path.exists(target_file_batch):
                os.remove(target_file_batch)


def download_blob(bucket, object, target_file):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(object)
    blob.download_to_filename(target_file)


def resolve_date_format(
    df: pd.DataFrame,
    field_name: str,
    pipeline: str,
) -> pd.DataFrame:
    if "opex" not in pipeline:
        logging.info("Resolving date formats")
        df[field_name] = df[field_name].apply(convert_dt_format)
        return df
    else:
        logging.info("Resolving date formats")
        df[field_name] = df[field_name].apply(convert_dt_format_opex)
        return df


def convert_dt_format(dt_str: str) -> str:
    if (
        not dt_str
        or str(dt_str).lower() == "nan"
        or str(dt_str).lower() == "nat"
        or dt_str == "-"
    ):
        return ""
    else:
        return str(
            datetime.datetime.strftime(
                datetime.datetime.strptime(dt_str, "%m%d%Y"), "%Y-%m-%d"
            )
        )


def convert_dt_format_opex(dt_str: str) -> str:
    if (
        not dt_str
        or str(dt_str).lower() == "nan"
        or str(dt_str).lower() == "nat"
        or dt_str == "-"
    ):
        return ""
    else:
        return str(
            datetime.datetime.strftime(
                datetime.datetime.strptime(dt_str, "%m/%d/%Y"), "%Y-%m-%d"
            )
        )


def date_for_length(df: pd.DataFrame, field_name: str):
    date_list = df[field_name].values
    new_date_list = []
    for item in date_list:
        if item != "NaN" and len(item) >= 6:
            if len(item) == 7:
                item = "0" + item
                new_date_list.append(item)
            elif len(item) == 6:
                item = "0" + item[0:1] + "0" + item[1:]
                new_date_list.append(item)
            else:
                new_date_list.append(item)
                continue
        elif len(item) < 6:
            item = "NaN"
            new_date_list.append(item)
        else:
            new_date_list.append(item)
    df[field_name] = new_date_list
    return df[field_name]


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


# def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
#     df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file_zip_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file_zip_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file_zip_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def unzip_file(
    source_file_zip_file: pathlib.Path, source_file_path: pathlib.Path
) -> None:
    logging.info(f"Unzipping {source_file_zip_file}")
    with ZipFile(source_file_zip_file, "r") as zipObj:
        zipObj.extractall(source_file_path)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_bucket=os.environ.get("SOURCE_GCS_BUCKET", ""),
        source_object=os.environ.get("SOURCE_GCS_OBJECT", ""),
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        source_file_zip_file=os.environ.get("SOURCE_FILE_ZIP_FILE", ""),
        source_file_path=os.environ.get("SOURCE_FILE_PATH", ""),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        csv_headers=os.environ.get("CSV_HEADERS", ""),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
    )
