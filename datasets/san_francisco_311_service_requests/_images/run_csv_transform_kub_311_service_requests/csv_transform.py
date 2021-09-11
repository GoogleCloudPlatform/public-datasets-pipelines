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

# import modules
import datetime
import logging
import os
import pathlib

import pdb
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info(f"San Francisco - 311 Service Requests process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"downloading file {source_url}")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(source_file)

    logging.info(f"Transformation Process Starting.. {source_file}")

    logging.info(f"Transform: Renaming Headers.. {source_file}")
    rename_headers(df)

    df = df[ df["unique_key"] != ""]

    df["incident_address"] = df["incident_address"].strip()

    pdb.set_trace()

    df["latitude"].str.replace("(", "").replace(")", "")
    df["longitude"].str.replace("(", "").replace(")", "")

    df["created_date"] = df["created_date"].apply(convert_dt_format)

    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "field1",
            "field2",
        ]
    ]

    logging.info(f"Transformation Process complete .. {source_file}")

    logging.info(f"Saving to output file.. {target_file}")

    try:
        save_to_new_file(df, file_path=str(target_file), index=False)
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(f"San Francisco - 311 Service Requests process completed")


def convert_dt_format(dt_str: str) -> str:
    if dt_str is None or len(str(dt_str)) == 0 or str(dt_str) == "nan":
        return str(dt_str)
    else:
        return str(datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"))


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "CaseID": "unique_key",
        "Opened": "created_date",
        "Closed": "closed_date",
        "Updated": "solution_action_updated_date",
        "Status": "status",
        "Status Notes": "status_notes",
        "Responsible Agency": "agency_name",
        "Category": "category",
        "Request Type": "complaint_type",
        "Request Details": "descriptor",
        "Address": "incident_address",
        "Supervisor District": "supervisor_district",
        "Neighborhood": "neighborhood",
        "Point": "location",
        "Source": "source",
        "Media URL": "media_url",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Police District": "police_district",
    }

    df = df.rename(columns=header_names, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path)


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
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
