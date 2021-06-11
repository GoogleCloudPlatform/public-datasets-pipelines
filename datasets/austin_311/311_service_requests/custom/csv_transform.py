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

# transform descriptions:
#
#   * Load the CSV
#   * Rename Headers
        # drag_indicator                      unique_key
        # --------------                      ----------
        # Service Request (SR) Number         drag_indicator
        # SR Type Code                        complaint_type
        # SR Description                      complaint_description
        # Owning Department                   owning_department
        # Method Received                     source
        # SR Status                           status
        # Status Change Date                  status_change_date
        # Created Date                        created_date
        # Last Update Date                    last_update_date
        # Close Date                          close_date
        # SR Location                         incident_address
        # Street Number                       street_number
        # Street Name                         street_name
        # City                                city
        # Zip Code                            incident_zip
        # County                              county
        # State Plane X Coordinate            state_plane_x_coordinate
        # State Plane Y Coordinate            state_plane_y_coordinate
        # Latitude Coordinate                 latitude
        # Longitude Coordinate                longitude
        # (Latitude.Longitude)                location
        # Council District                    council_district_code
        # Map Page                            map_page
        # Map Tile                            map_tile

import vaex
from datetime import datetime
import os
import pathlib
# import typing


def main(source_file: pathlib.Path, target_file: pathlib.Path):
    df = vaex.open(str(source_file))

    # steps in the pipeline

    rename_headers(df)
    
    convert_dt_values(df)
    
    delete_newlines_from_column(df, col_name="location")
    
    filter_null_rows(df)
    
    save_to_new_file(df, file_path=str(target_file))


def rename_headers(df):
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


def convert_dt_format(dt_str):
    # Old format: MM/dd/yyyy hh:mm:ss aa
    # New format: yyyy-MM-dd HH:mm:ss
    if dt_str is None or len(dt_str) == 0:
        return dt_str
    else:
        return datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S")

def convert_dt_values(df):
    dt_cols = [
        "status_change_date",
        "created_date",
        "last_update_date",
        "close_date",
    ]

    for dt_col in dt_cols:
        df[dt_col] = df[dt_col].apply(convert_dt_format)


def delete_newlines(val):
    if val is None or len(val) == 0:
        return val
    else:
        if(val.find("\n") > 0):
            return val.replace("\n", "")
        else:
            return val


def delete_newlines_from_column(df, col_name):
    if df[col_name] is not None:
        if df[col_name].str.len() > 0:
            df[col_name] = df[col_name].apply(delete_newlines)


def filter_null_rows(df):
    df = df[df.unique_key != ""]


def save_to_new_file(df, file_path):
    df.export_csv(file_path)

if __name__ == "__main__":
    main(
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
    )
