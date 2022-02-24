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

import logging
import os
import pathlib

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("Sunroof solar potential started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file_gs(source_url, source_file)

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=chunksz,  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("Sunroof solar potential process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = rename_headers(df)
    df = remove_nan_cols(df)
    df = generate_location(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if skip_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
        )
        next(data_file)
    else:
        logging.info(f"Appending batch file {batch_file_path} to {target_file_path}")
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


def generate_location(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Generating location data")
    df["center_point"] = (
        "POINT( " + df["lng_avg"].map(str) + " " + df["lat_avg"].map(str) + " )"
    )

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[
        [
            "region_name",
            "state_name",
            "lat_max",
            "lat_min",
            "lng_max",
            "lng_min",
            "lat_avg",
            "lng_avg",
            "yearly_sunlight_kwh_kw_threshold_avg",
            "count_qualified",
            "percent_covered",
            "percent_qualified",
            "number_of_panels_n",
            "number_of_panels_s",
            "number_of_panels_e",
            "number_of_panels_w",
            "number_of_panels_f",
            "number_of_panels_median",
            "number_of_panels_total",
            "kw_median",
            "kw_total",
            "yearly_sunlight_kwh_n",
            "yearly_sunlight_kwh_s",
            "yearly_sunlight_kwh_e",
            "yearly_sunlight_kwh_w",
            "yearly_sunlight_kwh_f",
            "yearly_sunlight_kwh_median",
            "yearly_sunlight_kwh_total",
            "install_size_kw_buckets",
            "carbon_offset_metric_tons",
            "existing_installs_count",
            "center_point",
        ]
    ]

    return df


def remove_nan(dt_str: str) -> int:
    if not dt_str or str(dt_str) == "nan":
        return int()
    else:
        return int(dt_str)


def remove_nan_cols(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolve NaN data")
    cols = {
        "count_qualified",
        "existing_installs_count",
        "number_of_panels_n",
        "number_of_panels_s",
        "number_of_panels_e",
        "number_of_panels_w",
        "number_of_panels_f",
        "number_of_panels_median",
        "number_of_panels_total",
    }

    for col in cols:
        df[col] = df[col].apply(remove_nan)

    return df


def rename_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Renaming columns")
    header_names = {"install_size_kw_buckets_json": "install_size_kw_buckets"}
    df = df.rename(columns=header_names)

    return df


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path, index=False)


def download_file_gs(source_url: str, source_file: pathlib.Path) -> None:
    with open(source_file, "wb+") as file_obj:
        storage.Client().download_blob_to_file(source_url, file_obj)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
