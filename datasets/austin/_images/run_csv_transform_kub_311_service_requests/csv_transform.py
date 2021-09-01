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
#
#       Column Name                         Type            Length / Format                 Description
#
#       Service Request (SR) Number         String          255                             "The service request tracking number."
#       SR Type Code                        String          255
#       SR Description                      String          255
#       Owning Department                   String          512                             "Owning department of SR type."
#       Method Received                     String          255                             "Contact method SR was received from.  \n\nMass entry requests are submitted by dept. in groups after work is completed."
#       SR Status                           String          255                             "SR status.  Duplicate statuses indicate that issue had previously been reported recently."
#       Status Change Date                  Date            11/23/2020 01:41:21 PM          "Date of last SR status change.  Status changes occur when SR moves from one status to another.  I.E. new to open, open to closed."
#       Created Date                        Date            11/23/2020 01:41:21 PM          "Date SR was created."
#       Last Update Date                    Date            11/23/2020 01:41:21 PM          "Date SR was updated.  Last date SR received updates.  Updates may include creation, status changes, or changes to data in SR."
#       Close Date                          Date            11/23/2020 01:41:21 PM          "Date SR was closed."
#       SR Location                         String          255                             "Service location of SR."
#       Street Number                       String          255                             "Parsed location information.  Street number."
#       Street Name                         String          255                             "Parsed location information.  Street name."
#       City                                String          255                             "Parsed location information.  City."
#       Zip Code                            String          255                             "Parsed location information.  Zip code."
#       County                              String          255                             "Parsed location information.  County."
#       State Plane X Coordinate            String          255                             "State plane X coordinate."
#       State Plane Y Coordinate            String          255                             "State plane Y coordinate."
#       Latitude Coordinate                 Number                                          "SR location latitude coordinate."
#       Longitude Coordinate                Number                                          "SR location latitude coordinate."
#       (Latitude.Longitude)                Location                                        "SR location latitude and longitude coordinates."
#       Council District                    Number                                          "Council district corresponding to SR location.  Locations outside of the City of Austin jurisdiction will not have a council district."
#       Map Page                            String          255                             "SR location corresponding map page."
#       Map Tile                            String          255                             "SR location corresponding map page."


import datetime
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
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("Austin 311 Service Requests By Year process started")

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    logging.info(f"Opening file {source_file}")
    df = pd.read_csv(str(source_file))

    logging.info(f"Transforming.. {source_file}")
    rename_headers(df)
    convert_values(df)
    delete_newlines_from_column(df, col_name="location")
    filter_null_rows(df)

    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")
    logging.info("..Done!")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "Service Request (SR) Number": "unique_key",
        "SR Type Code": "complaint_type",
        "SR Description": "complaint_description",
        "Owning Department": "owning_department",
        "Method Received": "source",
        "SR Status": "status",
        "Status Change Date": "status_change_date",
        "Created Date": "created_date",
        "Last Update Date": "last_update_date",
        "Close Date": "close_date",
        "SR Location": "incident_address",
        "Street Number": "street_number",
        "Street Name": "street_name",
        "City": "city",
        "Zip Code": "incident_zip",
        "County": "county",
        "State Plane X Coordinate": "state_plane_x_coordinate",
        "State Plane Y Coordinate": "state_plane_y_coordinate",
        "Latitude Coordinate": "latitude",
        "Longitude Coordinate": "longitude",
        "(Latitude.Longitude)": "location",
        "Council District": "council_district_code",
        "Map Page": "map_page",
        "Map Tile": "map_tile",
    }

    for old_name, new_name in header_names.items():
        df.rename(old_name, new_name)


def convert_dt_format(dt_str: str) -> str:
    if str(dt_str).strip()[3:3] == "/":
        return datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif (
        dt_str is None
        or len(str(dt_str)) == 0
        or str(dt_str).lower() == "nan"
        or str(dt_str).lower() == "nat"
    ):
        return ""
    else:
        return str(dt_str)


def convert_values(df: pd.DataFrame) -> None:
    dt_cols = [
        "status_change_date",
        "created_date",
        "last_update_date",
        "close_date",
    ]

    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)

    int_cols = ["council_district_code"]
    for int_col in int_cols:
        df[int_col] = df[int_col].astype("int32")


def delete_newlines(val: str) -> str:
    if val is None or len(val) == 0:
        return val
    else:
        if val.find("\n") > 0:
            return val.replace("\n", "")
        else:
            return val


def delete_newlines_from_column(df: pd.DataFrame, col_name: str) -> None:
    if df[col_name] is not None & df[col_name].str.len() > 0:
        df[col_name] = df[col_name].apply(delete_newlines)


def filter_null_rows(df: pd.DataFrame) -> None:
    df = df[df.unique_key != ""]


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.export_csv(file_path)


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
