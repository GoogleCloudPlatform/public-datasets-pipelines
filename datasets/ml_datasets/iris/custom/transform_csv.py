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
from collections import OrderedDict


def main(source_path: pathlib.Path, target_path: pathlib.Path):
    with open(source_path) as csv_source:
        csv_reader = csv.reader(csv_source, delimiter=",")

        headers = rename_headers(
            next(csv_reader),
            {
                "sepallength": "sepal_length",
                "sepalwidth": "sepal_width",
                "petallength": "petal_length",
                "petalwidth": "petal_width",
                "class": "species",
            },
        )

        with open(target_path, "w") as csv_target:
            csv_writer = csv.writer(csv_target, delimiter=",")
            csv_writer.writerow(headers)

            for row in csv_reader:
                csv_writer.writerow(parse_row(row, headers))


def rename_headers(
    raw_headers: typing.List[str], replacements: dict
) -> typing.List[str]:
    headers = []
    for header in raw_headers:
        if replacements.get(header):
            header = replacements[header]
        headers.append(header.lower())
    return headers


def parse_row(raw_row: list, headers: list) -> list:
    _row = OrderedDict(zip(headers, raw_row))

    # apply transform here
    _row["species"] = _row["species"].replace("Iris-", "").strip()

    return list(_row.values())


if __name__ == "__main__":
    assert os.environ["SOURCE_CSV"]
    assert os.environ["TARGET_CSV"]
    main(
        source_path=pathlib.Path(os.environ["SOURCE_CSV"]).expanduser(),
        target_path=pathlib.Path(os.environ["TARGET_CSV"]).expanduser(),
    )
