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


import json
import logging
import os
import pathlib
import subprocess
import typing
from glob import glob

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    source_folder = os.path.split(source_file)[0]
    download_file(source_url, source_folder)
    concatenate_files(source_folder, source_file)
    process_data(
        source_file, target_file, chunksize, input_headers, data_dtypes, output_headers
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def save_to_new_file(df, file_path):
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading files at {source_url}")
    subprocess.check_call(
        ["gsutil", "-m", "cp", "-r", f"{source_url}", f"{source_file}"]
    )


def concatenate_files(source_folder: str, source_file: str) -> None:
    logging.info("Concatenating files")
    file_number = 1
    for path, subdir, files in os.walk(source_folder + "/FTD"):
        for file in glob(os.path.join(path, "*.csv")):
            resolve_source_data_issues(path, file)
            if file_number == 1:
                append_file(file, source_file, True, True)
            else:
                append_file(file, source_file, False, False)
            file_number = file_number + 1


def resolve_source_data_issues(path: str, file: str) -> None:
    cmd_list = [
        # resolve newlines in quoted text
        f"sed -zi 's/\\n\\\"\\n/\\\"\\n/g' {file}",
        f"sed -zi 's/\\n\\\",,,,,\\n/\\\",,,,,\\n/g' {file}",
        f"sed -i '/^\\\",,,,,/d'  {file}",
        # remove NUL characters
        "sed -i 's/\\x0//g' " + file,
        # remove trailer text from all source files under the source path recursively
        f'find {path} -type f -name "*.csv" -exec sed -i "/Trailer record count/d" {{}} +',
        f'find {path} -type f -name "*.csv" -exec sed -i "/Trailer total quantity of shares/d" {{}} +',
    ]
    logging.info(f"Resolving source data issues on file {file}")
    for cmd in cmd_list:
        logging.info("cmd: " + cmd)
        subprocess.check_call([cmd], shell=True)


def process_data(
    source_file: str,
    target_file: str,
    chunksize: str,
    input_headers: typing.List[str],
    data_dtypes: dict,
    output_headers: typing.List[str],
) -> None:
    logging.info(f"Processing {source_file} started")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=int(chunksize),
        sep=",",
        names=input_headers,
        skiprows=1,
        dtype=data_dtypes,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(
                f"Processing chunk #{chunk_number} of file {source_file} started"
            )
            target_file_batch = str(target_file).replace(".csv", f"-{chunk_number}.csv")
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(
                df,
                target_file_batch,
                target_file,
                chunk_number == 0,
                chunk_number == 0,
                output_headers,
            )
            logging.info(
                f"Processing chunk #{chunk_number} of file {source_file} completed"
            )


def process_chunk(
    df: pd.DataFrame,
    target_file_batch: str,
    target_file: str,
    include_header: bool,
    truncate_file: bool,
    output_headers: typing.List[str],
) -> None:
    logging.info(f"Processing Batch {target_file_batch} started")
    df = search_and_replace_values(df)
    df = reorder_headers(df, output_headers)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_file(target_file_batch, target_file, include_header, truncate_file, True)
    logging.info(f"Processing Batch {target_file_batch} completed")


def append_file(
    batch_file_path: str,
    target_file_path: str,
    include_header: bool,
    truncate_target_file: bool,
    remove_source: bool = False,
) -> None:
    logging.info(
        f"Appending file {batch_file_path} to file {target_file_path} with include_header={include_header} and truncate_target_file={truncate_target_file}"
    )
    with open(batch_file_path, "r") as data_file:
        if truncate_target_file:
            target_file = open(target_file_path, "w+").close()
        with open(target_file_path, "a+") as target_file:
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
            if os.path.exists(batch_file_path) and remove_source:
                os.remove(batch_file_path)


def search_and_replace_values(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Search and replacing values..")
    df.drop(
        df[df.settlement_date.astype(str).str.startswith("Trailer")].index, inplace=True
    )
    df["settlement_date"] = pd.to_datetime(
        df["settlement_date"].astype(str), errors="coerce"
    )
    df["total_shares"] = df["total_shares"].fillna(0).astype(int)
    df = df.replace(
        to_replace={
            "share_price": {'"': ""},
        }
    )
    df = df.replace(
        to_replace={"share_price": {"^.$": "", "\n": ""}, "company_name": {"\n": ""}},
        regex=True,
    )
    return df


def reorder_headers(df: pd.DataFrame, headers: typing.List[str]) -> pd.DataFrame:
    logging.info("Transform: Reordering headers..")
    df = df[headers]
    return df


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
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        input_headers=json.loads(os.environ["INPUT_CSV_HEADERS"]),
        data_dtypes=json.loads(os.environ["DATA_DTYPES"]),
        output_headers=json.loads(os.environ["OUTPUT_CSV_HEADERS"]),
    )
