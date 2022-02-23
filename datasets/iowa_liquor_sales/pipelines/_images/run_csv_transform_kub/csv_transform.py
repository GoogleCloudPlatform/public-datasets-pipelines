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
import subprocess
from datetime import datetime

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
    logging.info(" Sales pipeline process started")
    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    chunksz = int(chunksize)
    logging.info(f"Reading csv file {source_url}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=chunksz,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            processChunk(df, target_file_batch)

            logging.info(f"Appending batch {chunk_number} to {target_file}")
            if chunk_number == 0:
                subprocess.run(["cp", target_file_batch, target_file])
            else:
                subprocess.check_call(f"sed -i '1d' {target_file_batch}", shell=True)
                subprocess.check_call(
                    f"cat {target_file_batch} >> {target_file}", shell=True
                )
            subprocess.run(["rm", target_file_batch])

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def processChunk(df: pd.DataFrame, target_file_batch: str) -> None:

    logging.info("Renaming Headers")
    rename_headers(df)

    logging.info("Convert Date Format")
    df["date"] = df["date"].apply(convert_dt_format)

    logging.info("Reordering headers..")
    df = df[
        [
            "invoice_and_item_number",
            "date",
            "store_number",
            "store_name",
            "address",
            "city",
            "zip_code",
            "store_location",
            "county_number",
            "county",
            "category",
            "category_name",
            "vendor_number",
            "vendor_name",
            "item_number",
            "item_description",
            "pack",
            "bottle_volume_ml",
            "state_bottle_cost",
            "state_bottle_retail",
            "bottles_sold",
            "sale_dollars",
            "volume_sold_liters",
            "volume_sold_gallons",
        ]
    ]

    df["county_number"] = df["county_number"].astype("Int64")

    logging.info(f"Saving to output file.. {target_file_batch}")
    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    logging.info("..Done!")


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "Invoice/Item Number": "invoice_and_item_number",
        "Date": "date",
        "Store Number": "store_number",
        "Store Name": "store_name",
        "Address": "address",
        "City": "city",
        "Zip Code": "zip_code",
        "Store Location": "store_location",
        "County Number": "county_number",
        "County": "county",
        "Category": "category",
        "Category Name": "category_name",
        "Vendor Number": "vendor_number",
        "Vendor Name": "vendor_name",
        "Item Number": "item_number",
        "Item Description": "item_description",
        "Pack": "pack",
        "Bottle Volume (ml)": "bottle_volume_ml",
        "State Bottle Cost": "state_bottle_cost",
        "State Bottle Retail": "state_bottle_retail",
        "Bottles Sold": "bottles_sold",
        "Sale (Dollars)": "sale_dollars",
        "Volume Sold (Liters)": "volume_sold_liters",
        "Volume Sold (Gallons)": "volume_sold_gallons",
    }
    df = df.rename(columns=header_names, inplace=True)


def convert_dt_format(dt_str: str) -> str:
    if dt_str is None or len(dt_str) == 0:
        return dt_str
    else:
        if len(dt_str) == 10:
            return datetime.strptime(dt_str, "%m/%d/%Y").strftime("%Y-%m-%d")


def save_to_new_file(df, file_path) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} into {source_file}")
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
