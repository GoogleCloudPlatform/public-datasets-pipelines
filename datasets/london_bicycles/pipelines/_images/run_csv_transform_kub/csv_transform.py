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
import datetime
import json
import logging
import os
import pathlib
from xml.etree import ElementTree

import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: str,
    required_cols: list,
    rename_mappings: dict,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
    output_file: str,
    gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    logging.info(
        f'London Cycle Stations Dataset pipeline process started at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file(source_url, source_file)
    process_xml(
        source_file,
        output_file,
        required_cols,
        rename_mappings,
        date_cols,
        integer_cols,
        float_cols,
        string_cols,
    )
    upload_file_to_gcs(output_file, gcs_bucket, target_gcs_path)
    logging.info(
        f'London Cycle Stations Dataset pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


def download_file(source_url: str, source_file: str) -> None:
    logging.info(f"Downloading data from {source_url} to {source_file} .")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
    else:
        logging.info(f"Couldn't download {source_url}: {res.text}")
    logging.info(f"Downloaded data from {source_url} into {source_file}")


def get_data_dict(
    row_tag: ElementTree.Element,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
) -> dict:
    row_data = {}
    for col in row_tag:
        if col.tag in date_cols:
            row_data[col.tag] = parse_date(col.text)
        elif col.tag in integer_cols:
            row_data[col.tag] = int(col.text)
        elif col.tag in float_cols:
            row_data[col.tag] = float(col.text)
        elif col.tag in string_cols:
            row_data[col.tag] = col.text
    return row_data


def parse_date(date: str) -> datetime.datetime.date:
    if not date:
        return None
    date = datetime.datetime.fromtimestamp(int(date) / 1000)
    return date.date()


def process_xml(
    source_file: str,
    output_file: str,
    required_cols: list,
    rename_mappings: dict,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
) -> None:
    logging.info("Process started for converting .xml to .csv")
    xml_data = ElementTree.parse(source_file)
    root_tag = xml_data.getroot()
    row_tags = list(root_tag)
    logging.info(f"Opening {output_file} in 'w'(write) mode")
    with open(output_file, mode="w") as fb:
        logging.info(
            f"Creating csv writer(DictWriter) object with fieldnames={required_cols}"
        )
        writer = csv.DictWriter(fb, fieldnames=required_cols)
        logging.info(
            f"Writing headers(Renamed Headers) {rename_mappings} to {output_file}"
        )
        writer.writerow(rename_mappings)
        logging.info(f"Reading all xml tags and writing to {output_file}")
        for idx, row_tag in enumerate(row_tags, start=1):
            if not (idx % 100):
                logging.info(
                    f"\t{idx} rows of data cleaned and writing/appending to {output_file}"
                )
            row_entry = get_data_dict(
                row_tag, date_cols, integer_cols, float_cols, string_cols
            )
            writer.writerow(row_entry)
        logging.info(
            f"\t{idx} rows of data cleaned and writing/appending to {output_file}"
        )
    logging.info("Process completed for converting .xml to .csv")


def upload_file_to_gcs(
    target_csv_file: str, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_csv_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_url=os.environ.get("SOURCE_URL", ""),
        source_file=os.environ.get("SOURCE_FILE", ""),
        required_cols=json.loads(os.environ.get("REQUIRED_COLS", "[]")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS", "{}")),
        date_cols=json.loads(os.environ.get("DATE_COLS", "[]")),
        integer_cols=json.loads(os.environ.get("INTEGER_COLS", "[]")),
        float_cols=json.loads(os.environ.get("FLOAT_COLS", "[]")),
        string_cols=json.loads(os.environ.get("STRING_COLS", "[]")),
        output_file=os.environ.get("OUTPUT_FILE", ""),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
    )
