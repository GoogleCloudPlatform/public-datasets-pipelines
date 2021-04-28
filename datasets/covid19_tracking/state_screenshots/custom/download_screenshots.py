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
from multiprocessing.pool import ThreadPool

import requests

CPU_FRACTION = 0.5
WORKER_THREADS = max(int(os.cpu_count() * CPU_FRACTION), 1)


def download_item(source_target: typing.Tuple[str, pathlib.Path]):
    """ThreadPool.imap_unordered accepts tuples as arguments to the callable"""
    source_url, download_path = source_target
    if not os.path.exists(download_path):
        r = requests.get(source_url, stream=True)
        if r.status_code == 200:
            with open(download_path, "wb") as f:
                for chunk in r:
                    f.write(chunk)


def download_parallel(source_targets: typing.List[typing.Tuple[str, pathlib.Path]]):
    ThreadPool(WORKER_THREADS).imap_unordered(download_item, source_targets)


def main(csv_path: pathlib.Path, source_column: str, download_prefix: str):
    with open(csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        download_dir = pathlib.Path(download_prefix)

        row_num = 0
        source_targets = []
        for row in csv_reader:
            # Example:
            # https://covidtracking.com/screenshots/AL/AL-20210307-230802.png
            source_url = row[source_column]
            state, filename = row[source_column].split("/")[-2:]

            (download_dir / state).mkdir(parents=True, exist_ok=True)
            source_targets.append((source_url, download_dir / state / filename))

            row_num += 1
            if row_num % WORKER_THREADS == 0:
                download_parallel(source_targets)
                source_targets = []

        download_parallel(source_targets)


if __name__ == "__main__":
    assert os.environ["CSV_PATH"]
    assert os.environ["SOURCE_COLUMN"]
    assert os.environ["DOWNLOAD_PREFIX"]
    main(
        csv_path=pathlib.Path(os.environ["CSV_PATH"]).expanduser(),
        source_column=os.environ["SOURCE_COLUMN"],
        download_prefix=os.environ["DOWNLOAD_PREFIX"],
    )
