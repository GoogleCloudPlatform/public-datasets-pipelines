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

FACILITY_CATEGORY = (
    "nursing_homes",
    "assisted_living",
    "uncategorized_ltc_facilities",
    "other_care_facilities",
)

FACILITY_COLS = (
    "resident_positives",
    "probable_resident_positives",
    "resident_deaths",
    "probable_resident_deaths",
    "staff_positives",
    "probable_staff_positives",
    "staff_deaths",
    "probable_staff_deaths",
    "resident_staff_positives",
    "probable_res_staff_positives",
    "resident_staff_deaths",
    "probable_res_staff_deaths",
    "number_of_facilities_with_outbreak",
)


def main(source_path: pathlib.Path, target_path: pathlib.Path):
    with open(source_path) as csv_source:
        csv_reader = csv.reader(csv_source, delimiter=",")

        # Skip the unnecessary first line in the raw CSV
        next(csv_reader)

        # The 2nd line contains the raw CSV headers
        raw_headers = next(csv_reader)
        headers, skip_col_indices = parse_headers(raw_headers)

        with open(target_path, "w") as csv_target:
            csv_writer = csv.writer(csv_target, delimiter=",")
            csv_writer.writerow(headers)

            for row in csv_reader:
                csv_writer.writerow(parse_row(row, skip_col_indices))


def parse_headers(raw_headers: list) -> typing.Tuple[list, set]:
    headers = []
    skip_col_indices = set()

    for idx, col in enumerate(raw_headers):
        if not col:
            skip_col_indices.add(idx)
            continue

        col = col.lower().replace(" ", "_").replace("/", "_")

        # Start prepending the column names with facility categories,
        # iterating through all facility columns per category
        if col == "resident_positives":
            for prefix in FACILITY_CATEGORY:
                for suffix in FACILITY_COLS:
                    headers.append(f"{prefix}_{suffix}")
            break
        else:
            headers.append(col)

    return headers, skip_col_indices


def parse_row(raw_row: list, skip_col_indices: set) -> list:
    row = []
    for idx, val in enumerate(raw_row):
        if idx in skip_col_indices:
            continue

        if idx == 0:  # index 0 is the date with raw format `YYYYMMDD`
            val = str(datetime.strptime(val, "%Y%m%d").date())

        row.append(val)
    return row


if __name__ == "__main__":
    assert os.environ["SOURCE_CSV"]
    assert os.environ["TARGET_CSV"]
    main(
        source_path=pathlib.Path(os.environ["SOURCE_CSV"]).expanduser(),
        target_path=pathlib.Path(os.environ["TARGET_CSV"]).expanduser(),
    )
