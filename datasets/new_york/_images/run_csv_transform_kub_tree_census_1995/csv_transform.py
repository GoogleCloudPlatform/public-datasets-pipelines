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

# CSV transform for: austin_311.311_service_request

# import modules
import datetime
import logging
import os
import pathlib

# import numpy as np
import re

import pandas as pd
import requests

# import csv
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
):

    logging.info(
        "New York Tree Census 1995 process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    # open the input file
    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(source_file)

    # steps in the pipeline
    logging.info(f"Transformation Process Starting.. {source_file}")

    # rename the headers
    logging.info(f"Transform: Renaming Headers.. {source_file}")
    rename_headers(df)

    # trim whitespace
    df["Spc_Latin"] = df["Spc_Latin"].str.strip()

    # reorder headers in output
    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "RecordId",
            "Address",
            "House_Number",
            "Street",
            "Postcode_Original",
            "Community Board_Original",
            "Site",
            "Species",
            "Diameter",
            "Condition",
            "Wires",
            "Sidewalk_Condition",
            "Support_Structure",
            "Borough",
            "X",
            "Y",
            "Longitude",
            "Latitude",
            "CB_New",
            "Zip_New",
            "CensusTract_2010",
            "CensusBlock_2010",
            "NTA_2010",
            "SegmentID",
            "Spc_Common",
            "Spc_Latin",
            "Location",
        ]
    ]

    # steps in the pipeline
    logging.info(f"Transformation Process complete .. {source_file}")

    # save to output file
    logging.info(f"Saving to output file.. {target_file}")

    try:
        # save_to_new_file(df, file_path=str(target_file))
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    # log completion
    logging.info(
        "New York Tree Census 1995 process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def convert_dt_format(date_str, time_str):
    #  date_str, time_str
    # 10/26/2014,13:12:00
    return str(datetime.datetime.strptime(date_str, "%m/%d/%Y").date()) + " " + time_str


def rename_headers(df):
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

    # for old_name, new_name in header_names.items():
    df.rename(columns=header_names)


def replace_value(val):
    if val is None or len(val) == 0:
        return val
    else:
        if val.find("\n") > 0:
            # return val.replace("\n", "")
            return re.sub(r"(^\d):(\d{2}:\d{2})", "0$1:$2", val)
        else:
            return val


def replace_values_regex(df):
    header_names = {"checkout_time"}

    for dt_col in header_names:
        if df[dt_col] is not None:
            if df[dt_col].str.len() > 0:
                df[dt_col] = df[dt_col].apply(replace_value)


def filter_null_rows(df):
    df = df[df.trip_id != ""]


def save_to_new_file(df, file_path):
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path):
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
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
