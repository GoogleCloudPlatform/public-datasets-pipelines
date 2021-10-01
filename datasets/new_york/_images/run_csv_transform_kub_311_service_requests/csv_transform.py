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

import datetime
import logging
import os
import pathlib

import numpy as np
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

    logging.info("New York 311 Service Requests process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file(source_url, source_file)

    chunksz = int(chunksize)

    dtypes = {
        "Unique Key": np.int_,
        "Created Date": np.str_,
        "Closed Date": np.str_,
        "Agency": np.str_,
        "Agency Name": np.str_,
        "Complaint Type": np.str_,
        "Descriptor": np.str_,
        "Location Type": np.str_,
        "Incident Zip": np.str_,
        "Incident Address": np.str_,
        "Street Name": np.str_,
        "Cross Street 1": np.str_,
        "Cross Street 2": np.str_,
        "Intersection Street 1": np.str_,
        "Intersection Street 2": np.str_,
        "Address Type": np.str_,
        "City": np.str_,
        "Landmark": np.str_,
        "Facility Type": np.str_,
        "Status": np.str_,
        "Due Date": np.str_,
        "Resolution Description": np.str_,
        "Resolution Action Updated Date": np.str_,
        "Community Board": np.str_,
        "BBL": np.str_,
        "Borough": np.str_,
        "X Coordinate (State Plane)": np.str_,
        "Y Coordinate (State Plane)": np.str_,
        "Open Data Channel Type": np.str_,
        "Park Facility Name": np.str_,
        "Park Borough": np.str_,
        "Vehicle Type": np.str_,
        "Taxi Company Borough": np.str_,
        "Taxi Pick Up Location": np.str_,
        "Bridge Highway Name": np.str_,
        "Bridge Highway Direction": np.str_,
        "Road Ramp": np.str_,
        "Bridge Highway Segment": np.str_,
        "Latitude": np.float64,
        "Longitude": np.float64,
        "Location": np.str_,
    }
    parse_dates = [
        "Created Date",
        "Closed Date",
        "Due Date",
        "Resolution Action Updated Date",
    ]

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,
        engine="python",
        encoding="utf-8",
        quotechar='"',
        chunksize=chunksz,
        dtype=dtypes,
        parse_dates=parse_dates,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("New York - 311 Service Requests process completed")


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
        logging.info("file truncated")
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


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = rename_headers(df)
    logging.info("Remove rows with empty keys")
    df = df[df["unique_key"] != ""]
    df = resolve_date_format(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[
        [
            "unique_key",
            "created_date",
            "closed_date",
            "agency",
            "agency_name",
            "complaint_type",
            "descriptor",
            "location_type",
            "incident_zip",
            "incident_address",
            "street_name",
            "cross_street_1",
            "cross_street_2",
            "intersection_street_1",
            "intersection_street_2",
            "address_type",
            "city",
            "landmark",
            "facility_type",
            "status",
            "due_date",
            "resolution_description",
            "resolution_action_updated_date",
            "community_board",
            "borough",
            "x_coordinate",
            "y_coordinate",
            "park_facility_name",
            "park_borough",
            "bbl",
            "open_data_channel_type",
            "vehicle_type",
            "taxi_company_borough",
            "taxi_pickup_location",
            "bridge_highway_name",
            "bridge_highway_direction",
            "road_ramp",
            "bridge_highway_segment",
            "latitude",
            "longitude",
            "location",
        ]
    ]
    return df


def resolve_date_format(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolve Date Format")
    date_fields = [
        "created_date",
        "closed_date",
        "due_date",
        "resolution_action_updated_date",
    ]

    for dt_fld in date_fields:
        df[dt_fld] = df[dt_fld].apply(convert_dt_format)

    return df


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif (
        dt_str.strip()[2] == "/"
    ):  # if there is a '/' in 3rd position, then we have a date format mm/dd/yyyy
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Renaming Headers")
    header_names = {
        "Unique Key": "unique_key",
        "Created Date": "created_date",
        "Closed Date": "closed_date",
        "Agency": "agency",
        "Agency Name": "agency_name",
        "Complaint Type": "complaint_type",
        "Descriptor": "descriptor",
        "Location Type": "location_type",
        "Incident Zip": "incident_zip",
        "Incident Address": "incident_address",
        "Street Name": "street_name",
        "Cross Street 1": "cross_street_1",
        "Cross Street 2": "cross_street_2",
        "Intersection Street 1": "intersection_street_1",
        "Intersection Street 2": "intersection_street_2",
        "Address Type": "address_type",
        "City": "city",
        "Landmark": "landmark",
        "Facility Type": "facility_type",
        "Status": "status",
        "Due Date": "due_date",
        "Resolution Description": "resolution_description",
        "Resolution Action Updated Date": "resolution_action_updated_date",
        "Community Board": "community_board",
        "Open Data Channel Type": "open_data_channel_type",
        "Borough": "borough",
        "X Coordinate (State Plane)": "x_coordinate",
        "Y Coordinate (State Plane)": "y_coordinate",
        "Park Facility Name": "park_facility_name",
        "Park Borough": "park_borough",
        "Vehicle Type": "vehicle_type",
        "Taxi Company Borough": "taxi_company_borough",
        "Taxi Pick Up Location": "taxi_pickup_location",
        "Bridge Highway Name": "bridge_highway_name",
        "Bridge Highway Direction": "bridge_highway_direction",
        "Road Ramp": "road_ramp",
        "Bridge Highway Segment": "bridge_highway_segment",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Location": "location",
        "BBL": "bbl",
    }

    df = df.rename(columns=header_names)

    return df


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    logging.info(f"Saving data to target file.. {file_path} ...")
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading file {source_url}")
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info(f"Uploading output file to.. gs://{gcs_bucket}/{gcs_path}")
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
