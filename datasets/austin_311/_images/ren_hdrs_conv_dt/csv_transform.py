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


# import csv
import os
import pathlib
import typing
import vaex
from datetime import datetime


def main(source_path: pathlib.Path, target_path: pathlib.Path):
    with open(source_path) as csv_source:
        csv_reader = csv.reader(csv_source, delimiter=",")
        headers = parse_headers(next(csv_reader))

        with open(target_path, "w") as csv_target:
            csv_writer = csv.writer(csv_target, delimiter=",")
            csv_writer.writerow(headers)

            for row in csv_reader:
                csv_writer.writerow(parse_row(row))


def parse_headers(raw_headers: typing.List[str]) -> typing.List[str]:
    headers = []
    for raw_header in raw_headers:
        if raw_header == "City or County?":
            raw_header = "city_or_county"
        headers.append(raw_header.lower())
    return headers


def parse_row(raw_row: list) -> list:
    row = []
    for idx, val in enumerate(raw_row):
        if idx == 0:  # index 0 is the `Date` field with format `YYYYMMDD`
            val = str(datetime.strptime(val, "%Y%m%d").date())

        if idx >= 4:  # values that should be numeric start at the 4th column
            if val == "N/A" or val.startswith("<") or val.startswith("~"):
                val = ""
            elif "," in val:  # convert integers represented as strings: "1,234"
                val = int(val.replace(",", ""))
            elif val == "7/1":  # a row for Idaho has a string value "7/1"
                val = 7

        row.append(val)
    return row


if __name__ == "__main__":
    assert os.environ["SOURCE_CSV"]
    assert os.environ["TARGET_CSV"]
    main(
        source_path=pathlib.Path(os.environ["SOURCE_CSV"]).expanduser(),
        target_path=pathlib.Path(os.environ["TARGET_CSV"]).expanduser(),
    )
