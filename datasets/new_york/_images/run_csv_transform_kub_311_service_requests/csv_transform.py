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
import subprocess

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

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"downloading file {source_url}")
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

    logging.info("New York - 311 Service Requests process completed")


def processChunk(df: pd.DataFrame, target_file_batch: str) -> None:

    logging.info("Renaming Headers")
    rename_headers(df)

    logging.info("Remove rows with empty keys")
    df = df[df["unique_key"] != ""]

    logging.info("Convert Date Format")
    df["created_date"] = df["created_date"].apply(convert_dt_format)
    df["closed_date"] = df["closed_date"].apply(convert_dt_format)
    df["due_date"] = df["due_date"].apply(convert_dt_format)
    df["resolution_action_updated_date"] = df["resolution_action_updated_date"].apply(
        convert_dt_format
    )

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

    logging.info(f"    Saving to target file.. {target_file_batch}")

    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving to target file: {e}.")

    logging.info(f"Saved transformed source data to target file .. {target_file_batch}")


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat":
        return ""
    elif dt_str.strip()[3] == "/":
        return datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return str(dt_str)


def rename_headers(df: pd.DataFrame) -> None:
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

    df = df.rename(columns=header_names, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


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
