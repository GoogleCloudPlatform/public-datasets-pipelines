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


import csv
import os
import pathlib
import typing
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
