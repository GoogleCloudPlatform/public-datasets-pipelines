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

import requests
from google.cloud import storage


def main(csv_path: pathlib.Path, source_column: str, target_column: str):
    gcs_client = storage.Client()
    with open(csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            source_url = row[source_column]
            gcs_bucket, gcs_path = decompose_gcs_uri(row[target_column])

            stream_http_to_gcs(gcs_client, source_url, gcs_bucket, gcs_path)


def decompose_gcs_uri(gcs_uri: str) -> typing.Tuple[str, str]:
    gcs_bucket, gcs_path = gcs_uri.replace("gs://", "").split("/", 1)
    return gcs_bucket, gcs_path


def stream_http_to_gcs(
    client: storage.Client, source_url: str, gcs_bucket: str, gcs_path: str
):
    response = requests.get(source_url)
    bucket = client.get_bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_string(response.content, content_type="image/png")


if __name__ == "__main__":
    assert os.environ["CSV_PATH"]
    assert os.environ["SOURCE_COLUMN"]
    assert os.environ["TARGET_COLUMN"]
    main(
        csv_path=pathlib.Path(os.environ["CSV_PATH"]).expanduser(),
        source_column=os.environ["SOURCE_COLUMN"],
        target_column=os.environ["TARGET_COLUMN"],
    )
