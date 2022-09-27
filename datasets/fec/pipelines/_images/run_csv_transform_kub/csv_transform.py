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
import json
import logging
import os
import pathlib
import typing
from zipfile import ZipFile

import pandas as pd
import requests
from google.cloud import storage


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
            dtype=object,
            index_col=False,
        )
        df.columns = csv_headers

        logging.info(f"Transforming {source_file}... ")
        if "candidate_20" in pipeline_name:
            logging.info("Transform: Trimming white spaces in headers... ")
            df = df.rename(columns=lambda x: x.strip())

        elif "candidate_committe_20" in pipeline_name:
            pass

        elif "committee_20" in pipeline_name:
            df.drop(df[df["cmte_id"] == "C00622357"].index, inplace=True)

        elif "committee_contributions_20" in pipeline_name:
            df["transaction_dt"] = df["transaction_dt"].astype(str)
            date_for_length(df, "transaction_dt")
            df = resolve_date_format(df, "transaction_dt", pipeline_name)

        elif "other_committee_tx_20" in pipeline_name:
            df["transaction_dt"] = df["transaction_dt"].astype(str)
            date_for_length(df, "transaction_dt")
            df = resolve_date_format(df, "transaction_dt", pipeline_name)

        elif "opex" in pipeline_name:
            df = df.drop(columns=df.columns[-1], axis=1)
            df["transaction_dt"] = df["transaction_dt"].astype(str)
            date_for_length(df, "transaction_dt")
            df = resolve_date_format(df, "transaction_dt", pipeline_name)

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
        download_blob(source_bucket, source_object, source_file)

        process_source_file(
            source_file, target_file, chunksize, csv_headers, pipeline_name
        )

        logging.info(
            f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def process_source_file(
    source_file: str,
    target_file: str,
    chunksize: str,
    csv_headers: typing.List[str],
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
        for index, line in enumerate(csv.reader(reader, "TabDialect"), 0):
            data.append(line)
            if int(index) % int(chunksize) == 0 and int(index) > 0:

                process_dataframe_chunk(
                    data,
                    target_file,
                    chunk_number,
                    pipeline_name,
                )
                data = []
                chunk_number += 1

        if data:
            process_dataframe_chunk(
                data,
                target_file,
                chunk_number,
                pipeline_name,
            )


def process_dataframe_chunk(
    data: typing.List[str],
    target_file: str,
    chunk_number: int,
    pipeline_name: str,
) -> None:
    data = list([char.split("|") for item in data for char in item])
    df = pd.DataFrame(
        data,
        columns=[
            "cmte_id",
            "amndt_ind",
            "rpt_tp",
            "transaction_pgi",
            "image_num",
            "transaction_tp",
            "entity_tp",
            "name",
            "city",
            "state",
            "zip_code",
            "employer",
            "occupation",
            "transaction_dt",
            "transaction_amt",
            "other_id",
            "tran_id",
            "file_num",
            "memo_cd",
            "memo_text",
            "sub_id",
        ],
    )
    target_file_batch = str(target_file).replace(
        ".csv", "-" + str(chunk_number) + ".csv"
    )
    process_chunk(
        df=df,
        target_file_batch=target_file_batch,
        target_file=target_file,
        pipeline_name=pipeline_name,
        skip_header=(not chunk_number == 1),
    )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    pipeline_name: str,
    skip_header: bool,
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df["image_num"] = df["image_num"].astype(str)
    df["transaction_dt"] = df["transaction_dt"].astype(str)
    convert_string_to_int(df, "image_num")
    fill_null_values(df, "sub_id")
    date_for_length(df, "transaction_dt")
    df = resolve_date_format(df, "transaction_dt", pipeline_name)
    df = df.rename(columns=lambda x: x.strip())
    save_to_new_file(df, file_path=str(target_file_batch), sep=",")
    append_batch_file(target_file_batch, target_file, skip_header)
    logging.info(f"Processing batch file {target_file_batch} completed")


def save_to_new_file(df: pd.DataFrame, file_path: str, sep: str = ",") -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False, sep=",")


def append_batch_file(
    target_file_batch: str, target_file: str, skip_header: bool
) -> None:

    with open(target_file_batch, "r") as data_file:
        with open(target_file, "a+") as target_file:
            if skip_header:
                logging.info(
                    f"Appending batch file {target_file_batch} to {target_file} with skipheader..."
                )
                next(data_file)
            else:
                logging.info(
                    f"Appending batch file {target_file_batch} to {target_file}"
                )
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


def fill_null_values(df: pd.DataFrame, field_name: str):
    df[field_name] = df[field_name].fillna(0)


def convert_string_to_int(df: pd.DataFrame, field_name: str):
    df[field_name] = pd.to_numeric(df[field_name], errors="coerce")
    df[field_name] = df[field_name].apply(lambda x: "%.0f" % x)
    df[field_name] = df[field_name].fillna(0)
    df[field_name] = df[field_name].replace({"nan": 0})


def date_for_length(df: pd.DataFrame, field_name: str):
    date_list = df[field_name].values
    new_date_list = []
    for item in date_list:
        if item != "NaN" and len(item) >= 6 and len(item) <= 8:
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
            item = ""
            new_date_list.append(item)
        else:
            item = ""
            new_date_list.append(item)
    df[field_name] = new_date_list
    return df[field_name]


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


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
        csv_headers=json.loads(os.environ["CSV_HEADERS"]),
        chunksize=os.environ.get("CHUNKSIZE", ""),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
    )
