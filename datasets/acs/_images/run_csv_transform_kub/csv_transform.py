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
import json
import logging
import math
import os
import pathlib
import typing

import pandas as pd
import requests
from google.cloud import storage


def main(
    # source_url: str,
    # source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    # headers: typing.List[str],
    # rename_mappings: dict,
    # pipeline_name: str,
) -> None:

    logging.info(
        f"ACS process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    geography = {
    "B25001001":"housing_units",
    "B25003001":"occupied_housing_units",
    "B25003003":"housing_units_renter_occupied"
    }

    state_code = {
	"01": "Alabama",
	"02": "Alaska",
	"04": "Arizona",
	"05": "Arkansas",
	"06": "California",
	"08": "Colorado",
	"09": "Connecticut",
	"10": "Delaware",
	"11": "District of Columbia",
	"12": "Florida",
	"13": "Georgia",
	"15": "Hawaii",
	"16": "Idaho",
	"17": "Illinois",
	"18": "Indiana",
	"19": "Iowa",
	"20": "Kansas",
	"21": "Kentucky",
	"22": "Louisiana",
	"23": "Maine",
	"24": "Maryland",
	"25": "Massachusetts",
	"26": "Michigan",
	"27": "Minnesota",
	"28": "Mississippi",
	"29": "Missouri",
	"30": "Montana",
	"31": "Nebraska",
	"32": "Nevada",
	"33": "New Hampshire",
	"34": "New Jersey",
	"35": "New Mexico",
	"36": "New York",
	"37": "North Carolina",
	"38": "North Dakota",
	"39": "Ohio",
	"40": "Oklahoma",
	"41": "Oregon",
	"42": "Pennsylvania",
	"44": "Rhode Island",
	"45": "South Carolina",
	"46": "South Dakota",
	"47": "Tennessee",
	"48": "Texas",
	"49": "Utah",
	"50": "Vermont",
	"51": "Virginia",
	"53": "Washington",
	"54": "West Virginia",
	"55": "Wisconsin",
	"56": "Wyoming",
	"60": "American Samoa",
	"66": "Guam",
	"69": "Commonwealth of the Northern Mariana Islands",
	"72": "Puerto Rico",
	"78": "United States Virgin Islands"
    }

    logging.info("Extracting the data from API and loading into dataframe...")
    df=extract_data_and_convert_to_df(geography,state_code)

    logging.info("Replacing values...")
    df = df.replace({"geography":geography})

    rename_mappings ={
    0:"name",
    1:"KPI_Value",
    2:"state",
    3:"county",
    4:"tract",
    "geography":"KPI_Name"
    }

    logging.info("Renaming headers...")
    rename_headers(df, rename_mappings)

    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        f"ACS process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def extract_data_and_convert_to_df(geography: dict,state_code: dict) -> pd.DataFrame:
    list_temp = []
    for key in geography :
        for sc in state_code :
            logging.info(f'reading data from API for KPI {key}...')
            logging.info(f'reading the content of the API for state {sc}...')
            source_url = 'https://api.census.gov/data/2019/acs/acs5?get=NAME,'+key[0:6]+'_'+key[6:]+'E&for=tract:*&in=state:'+sc+'&key=550e53635053be51754b09b5e9f5009c94aa0586'
            r = requests.get(source_url, stream=True)
            if r.status_code == 200:
                text= r.json()
                frame = pd.DataFrame(text)
                frame = frame.iloc[1: , :]
                frame['geography'] = key
                list_temp.append(frame)
    logging.info('creating the dataframe...')
    df = pd.concat(list_temp)
    return df


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        # source_url=os.environ["SOURCE_URL"],
        # source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        # headers=json.loads(os.environ["CSV_HEADERS"]),
        # rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        # pipeline_name=os.environ["PIPELINE_NAME"],
    )
