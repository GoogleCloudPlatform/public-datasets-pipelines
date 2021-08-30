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
import pdb
import subprocess

import numpy as np
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    number_of_batches: int,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(
        f"New York 311 Service Requests process started at {curr_dtm}"
    )

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"creating 'files' folder at {curr_dtm}")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    # curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    # logging.info(f"Downloading {source_url} into {source_file} at {curr_dtm}")
    # download_file(source_url, source_file)

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"Counting lines in input file {source_file} at {curr_dtm}")
    number_lines_source_file = subprocess.run(['wc', '-l', source_file], stdout=subprocess.PIPE)
    number_lines_input_file = int(str(str(number_lines_source_file.stdout).split(" ")[0][2:]).strip()) - 1

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"Calculating chunksize metadata in input file {source_file} at {curr_dtm}")
    chunksize = int((number_lines_input_file - 1) / int(number_of_batches))

    # whole number value (quotient) of dividing size into batches
    number_batches = int(number_lines_input_file / chunksize)

    # add one for any remaining batch data
    if float(number_lines_input_file % chunksize) > 0:
        number_batches = number_batches + 1

    start_line = 2

    for i in range(1, (number_batches+1)):

        batch_line_count = (chunksize - 1)

        if (i == 1):
            start_line = 2
            end_line = start_line + (batch_line_count - 1)
        elif (i > 1):
            start_line = ((i - 1) * chunksize) + 1
            end_line = start_line + batch_line_count


        # batch slice extracted from the source file
        source_file_batch = str(source_file).replace('.csv', '_batch.csv')
        # output generated from processing the source (batch) file
        target_file_batch = str(source_file).replace('.csv', '_batch_targ.csv')

        # logging.info("batch #" + str(i) + " start_line: " + str(start_line) + " batch_line_count: " + str(batch_line_count) + 'end: ' + str(end_line))
        # logging.info("source_file = " + str(source_file))
        # logging.info("source_file_batch = " + str(source_file_batch))

        # extract the header from the source file and use it in the new batch
        curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
        logging.info(f"creating data file for batch #{i} of {number_batches} batches at {curr_dtm}")
        os.system(f'head -n 1 {source_file} > {source_file_batch}')

        curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
        logging.info(f"populating data file for batch #{i} of {number_batches} batches at {curr_dtm}")
        os.system(f"sed -n '{start_line},{end_line}p;" + str(end_line + 1) + f"q' {source_file} >> {source_file_batch}")

        curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
        logging.info(f"processing batch data file #{i} of {number_batches} batches at {curr_dtm}")
        processBatch(source_file_batch, target_file_batch) # process the batch of data

        curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
        logging.info(f"writing batch data to target file for batch #{i} of {number_batches} batches at {curr_dtm}")
        if (i == 1):
            # write the first batch target file to the actual target file
            os.system(f'cp {target_file_batch} {target_file}')
        else:
            os.system(f'tail -n +2 {target_file_batch} >> {target_file}')

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path} at {curr_dtm}")
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    # log completion
    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"New York 311 Service Requests process completed at {curr_dtm}")


    # pdb.set_trace()


def processBatch(batch_file_path: str, target_batch_file: str) -> None:

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"->  Opening batch file at {curr_dtm} .. {batch_file_path}")
    dtypes = {  'Unique Key': np.int_,
                'Created Date': np.str_, # converted to datetime type later. Resolves constraint that pandas cannot import numpy datatype datetime or datetime64
                'Closed Date': np.str_, # converted to datetime type later. Resolves constraint that pandas cannot import numpy datatype datetime or datetime64
                'Agency': np.str_,
                'Agency Name': np.str_,
                'Complaint Type': np.str_,
                'Descriptor': np.str_,
                'Location Type': np.str_,
                'Incident Zip': np.str_,
                'Incident Address': np.str_,
                'Street Name': np.str_,
                'Cross Street 1': np.str_,
                'Cross Street 2': np.str_,
                'Intersection Street 1': np.str_,
                'Intersection Street 2': np.str_,
                'Address Type': np.str_,
                'City': np.str_,
                'Landmark': np.str_,
                'Facility Type': np.str_,
                'Status': np.str_,
                'Due Date': np.str_, # converted to datetime type later. Resolves constraint that pandas cannot import numpy datatype datetime or datetime64
                'Resolution Description': np.str_,
                'Resolution Action Updated Date': np.str_, # converted to datetime type later. Resolves constraint that pandas cannot import numpy datatype datetime or datetime64
                'Community Board': np.str_,
                'BBL': np.str_, # converted to int later due to NA appearing in input file on some rows
                'Borough': np.str_,
                'X Coordinate (State Plane)': np.str_,  # converted to int later due to NA appearing in input file on some rows
                'Y Coordinate (State Plane)': np.str_,  # converted to int later due to NA appearing in input file on some rows
                'Open Data Channel Type': np.str_,
                'Park Facility Name': np.str_,
                'Park Borough': np.str_,
                'Vehicle Type': np.str_,
                'Taxi Company Borough': np.str_,
                'Taxi Pick Up Location': np.str_,
                'Bridge Highway Name': np.str_,
                'Bridge Highway Direction': np.str_,
                'Road Ramp': np.str_,
                'Bridge Highway Segment': np.str_,
                'Latitude': np.float64,
                'Longitude': np.float64,
                'Location': np.str_
        }
    parse_dates = ['Created Date', 'Closed Date', 'Due Date', 'Resolution Action Updated Date']
    df = pd.read_csv(batch_file_path, dtype=dtypes, parse_dates=parse_dates)

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"->  Transformation Process Starting at {curr_dtm} .. {batch_file_path}")

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"->       Transform: Renaming Headers at {curr_dtm} .. {batch_file_path}")
    rename_headers(df)

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"->       Transform: Removing rows with empty Ids at {curr_dtm} .. {batch_file_path}")
    df = df[df["unique_key"] != ""]

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"->       Transform: Converting datetime format at {curr_dtm} .. {batch_file_path}")
    df["created_date"] = df["created_date"].apply(convert_dt_format)
    df["closed_date"] = df["closed_date"].apply(convert_dt_format)
    df["due_date"] = df["due_date"].apply(convert_dt_format)
    df["resolution_action_updated_date"] = df["resolution_action_updated_date"].apply(
        convert_dt_format
    )

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info("->       Transform: Reordering columns at {curr_dtm} ..")
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

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"->  Transformation Process complete at {curr_dtm} .. {batch_file_path}")

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"Saving transformed batch data to output file at {curr_dtm} .. {target_batch_file}")

    try:
        save_to_new_file(df, file_path=str(target_batch_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    curr_dtm = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
    logging.info(f"Saved transformed batch data to output file at {curr_dtm} .. {target_batch_file}")



def convert_dt_format(dt_str: str) -> str:
    if (str(dt_str).strip()[3:3] == '/'):
        return datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif (dt_str is None or len(str(dt_str)) == 0 or str(dt_str).lower() == "nan" or str(dt_str).lower() == "nat"):
	    return ""
    else:
        return str(dt_str)

        # return datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime(
        #     "%Y-%m-%d %H:%M:%S"
        # )


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
        number_of_batches=os.environ["NUMBER_OF_BATCHES"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
