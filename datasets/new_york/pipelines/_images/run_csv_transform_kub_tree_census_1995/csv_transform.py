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

import logging
import os
import pathlib

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("New York Tree Census 1995 process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file(source_url, source_file)

    chunksz = int(chunksize)

    logging.info(f"Opening source file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        sep=",",
        chunksize=chunksz,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("New York Tree Census 1995 process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    logging.info(f"Processing batch file {target_file_batch}")
    df = rename_headers(df)
    df = remove_whitespace(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))
    logging.info(f"Processing batch file {target_file_batch} completed")


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    header_names = {
        "RecordId": "recordid",
        "Address": "address",
        "House_Number": "house_number",
        "Street": "street",
        "Postcode_Original": "zip_original",
        "Community Board_Original": "cb_original",
        "Site": "site",
        "Species": "species",
        "Diameter": "diameter",
        "Condition": "status",
        "Wires": "wires",
        "Sidewalk_Condition": "sidewalk_condition",
        "Support_Structure": "support_structure",
        "Borough": "borough",
        "X": "x",
        "Y": "y",
        "Longitude": "longitude",
        "Latitude": "latitude",
        "CB_New": "cb_new",
        "Zip_New": "zip_new",
        "CensusTract_2010": "censustract_2010",
        "CensusBlock_2010": "censusblock_2010",
        "NTA_2010": "nta_2010",
        "SegmentID": "segmentid",
        "Spc_Common": "spc_common",
        "Spc_Latin": "spc_latin",
        "Location": "location",
    }

    df.rename(columns=header_names, inplace=True)

    return df


def remove_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    df["spc_latin"] = df["spc_latin"].apply(lambda x: str(x).strip())

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[
        [
            "recordid",
            "address",
            "house_number",
            "street",
            "zip_original",
            "cb_original",
            "site",
            "species",
            "diameter",
            "status",
            "wires",
            "sidewalk_condition",
            "support_structure",
            "borough",
            "x",
            "y",
            "longitude",
            "latitude",
            "cb_new",
            "zip_new",
            "censustract_2010",
            "censusblock_2010",
            "nta_2010",
            "segmentid",
            "spc_common",
            "spc_latin",
            "location",
        ]
    ]

    return df


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if skip_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
        )
        next(data_file)
    else:
        logging.info(f"Appending batch file {batch_file_path} to {target_file_path}")
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
