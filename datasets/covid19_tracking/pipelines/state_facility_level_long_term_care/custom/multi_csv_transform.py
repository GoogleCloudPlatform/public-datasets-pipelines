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


def main(working_dir: pathlib.Path):
    for raw_csv_filename in csv_files(working_dir):
        with open(working_dir / raw_csv_filename) as csv_source:
            csv_reader = csv.reader(csv_source, delimiter=",")
            headers = parse_headers(next(csv_reader))

            target_filename = raw_csv_filename.replace("raw-", "")
            with open(working_dir / target_filename, "w") as csv_target:
                csv_writer = csv.writer(csv_target, delimiter=",")
                csv_writer.writerow(headers)

                for row in csv_reader:
                    csv_writer.writerow(parse_row(row))


def csv_files(dir_: pathlib.Path) -> typing.List[str]:
    return [
        file.name
        for file in dir_.iterdir()
        if file.name.endswith(".csv") and file.name.startswith("raw")
    ]


def parse_headers(raw_headers: list) -> typing.List[str]:
    headers = []
    for header in raw_headers:
        if header == "date_outreak_closed":  # Fix typo from data source
            header = "date_outbreak_closed"
        headers.append(header)
    return headers


def parse_row(raw_row: list) -> list:
    row = []
    for idx, val in enumerate(raw_row):
        if idx == 0:  # index 0 is the `Date` field with format `YYYYMMDD`
            val = str(datetime.strptime(val, "%Y%m%d").date())
        row.append(val)
    return row


if __name__ == "__main__":
    assert os.environ["WORKING_DIR"]
    main(
        working_dir=pathlib.Path(os.environ["WORKING_DIR"]).expanduser(),
    )
