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
#       Kiosk ID                            integer         255                             ""
#       Kiosk Name                          string          255                             ""
#       Kiosk Status                        string          255                             ""
#       Address                             string          512                             ""
#       Alternate Name                      string          255                             ""
#       City Asset Number                   integer         255                             ""
#       Property Type                       string          11/23/2020 01:41:21 PM          ""
#       Number of Docks                     integer         11/23/2020 01:41:21 PM          ""
#       Power Type                          string          11/23/2020 01:41:21 PM          ""
#       Footprint Length                    integer         11/23/2020 01:41:21 PM          ""
#       Footprint Width                     float           255                             ""
#       Notes                               string          255                             ""
#       Council District                    integer         255                             ""
#       Modified Date                       datetime        255                             ""


import datetime
import logging
import math
import os
import pathlib

# import numpy as np
import requests
import vaex
from google.cloud import storage

# import math
# import pdb


# import typing


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
):

    logging.info(
        "Austin bikeshare stations process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    # open the input file
    logging.info(f"Opening file {source_file}")
    df = vaex.open(str(source_file))

    # steps in the pipeline
    logging.info(f"Transforming.. {source_file}")

    logging.info(f"Transform: Rename columns.. {source_file}")
    rename_headers(df)
    # df['city_asset_number'] = df.city_asset_number.astype('int')
    # df["number_of_docks"] = df.number_of_docks.astype('int')
    # df["footprint_length"] = df.footprint_length.astype('int')
    # df["council_district"] = df.council_district.astype('int')

    logging.info(f"Transform: Converting date values.. {source_file}")
    convert_values(df)

    filter_null_rows(df)

    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "station_id",
            "name",
            "status",
            "address",
            "alternate_name",
            "city_asset_number",
            "property_type",
            "number_of_docks",
            "power_type",
            "footprint_length",
            "footprint_width",
            "notes",
            "council_district",
            "modified_date",
        ]
    ]

    # df.fillna("")

    # convert data type format to integer
    df["city_asset_number"] = df["city_asset_number"].apply(convert_to_int)
    df["number_of_docks"] = df["number_of_docks"].apply(convert_to_int)
    df["footprint_length"] = df["footprint_length"].apply(convert_to_int)
    df["council_district"] = df["council_district"].apply(convert_to_int)

    # convert data type format to float
    df["footprint_width"] = df["footprint_width"].apply(resolve_nan)

    # pdb.set_trace()

    # save to output file
    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    # upload to GCS
    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        "Austin bikeshare stations process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def resolve_nan(input: str) -> str:
    str_val = ""
    if input == "" or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(input)
    return str_val.replace("None", "")


def convert_to_int(input: str) -> str:
    str_val = ""
    if input == "" or (math.isnan(input)):
        str_val = ""
    else:
        str_val = str(int(round(input, 0)))
    return str_val


def rename_headers(df):
    header_names = {
        "Kiosk ID": "station_id",
        "Kiosk Name": "name",
        "Kiosk Status": "status",
        "Address": "address",
        "Alternate Name": "alternate_name",
        "City Asset Number": "city_asset_number",
        "Property Type": "property_type",
        "Number of Docks": "number_of_docks",
        "Power Type": "power_type",
        "Footprint Length": "footprint_length",
        "Footprint Width": "footprint_width",
        "Notes": "notes",
        "Council District": "council_district",
        "Modified Date": "modified_date",
    }

    for old_name, new_name in header_names.items():
        df.rename(old_name, new_name)


def convert_dt_format(dt_str):
    # Old format: MM/dd/yyyy hh:mm:ss aa
    # New format: yyyy-MM-dd HH:mm:ss
    if dt_str is None or len(dt_str) == 0:
        return dt_str
    else:
        return datetime.datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime(
            "%Y-%m-%d %H:%M:%S"
        )


def convert_values(df):
    dt_cols = ["modified_date"]

    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)

    # int_cols = ["city_asset_number"]
    # for int_col in int_cols:
    #     df[int_col] = df[int_col].astype('Int64')


def filter_null_rows(df):
    df = df[df.station_id != ""]


def save_to_new_file(df, file_path):
    df.export_csv(file_path)


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
