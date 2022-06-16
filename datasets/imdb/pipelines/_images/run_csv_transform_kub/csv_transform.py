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

import datetime
import glob
import json
import logging
import os
import pathlib
import tarfile
import typing

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    extract_here: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
) -> None:
    logging.info(
        f"IMDb Dataset {pipeline_name} pipeline process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Downloading tar file ...")
    download_tarfile(source_url, source_file)
    logging.info("Downloading Completed.")

    logging.info(f"Extracting tar file to {extract_here}.")
    extract_tar(source_file, extract_here)
    logging.info(f"Successfully extracted tar file to {extract_here}.")

    logging.info("Started creating Dataframe.")
    df = create_dataframe(extract_here, headers)
    logging.info("Successfully Created Dataframe and assigned to variable df.")

    logging.info("Started cleaning html tags from the user review.")
    clean_html_tags(df)
    logging.info("Cleaning html tags completed.")

    logging.info(
        'Changing "label" column data from  ["neg", "pos"] -->  ["Negative", "Positive"].'
    )
    change_label(df)
    logging.info('Successfully replaced "label" column data.')

    logging.info("Renaming headers")
    rename_headers(df, rename_mappings)

    logging.info(f"Saving to output file... {target_file}")
    try:
        save_to_new_file(df, target_file)
        logging.info("Successfully saved.")
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)
    logging.info("Successfully uploaded file to gcs bucket.")

    logging.info(
        f"IMDb Dataset {pipeline_name} pipeline process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def download_tarfile(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Creating 'files' folder under {os.getcwd()}")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    logging.info(f"Downloading file from {source_url}...")
    logging.info(f"Downloading {source_url} into {source_file}")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {res.text}")


def extract_tar(source_file: pathlib.Path, extract_here: pathlib.Path):
    with tarfile.open(str(source_file), "r") as tar_fb:
        tar_fb.extractall(extract_here)


def create_dataframe(
    extract_here: pathlib.Path, headers: typing.List[str]
) -> pd.DataFrame:
    df = pd.DataFrame(columns=headers)
    for parent in ["train", "test"]:
        for child in ["pos", "neg"]:
            path = f"{extract_here}/aclImdb/{parent}/{child}/"
            csv_files = list(glob.glob(path + "*.txt"))
            logging.info(
                f"\tCreating Dataframe from by reading fila from {parent}-->{child}."
            )
            df_child = pd.DataFrame(
                [[open(file).read(), file.split("/")[-2]] for file in csv_files],
                columns=headers,
            )
            logging.info(
                f"\tSuccessfully created Dataframe(Child Dataframe) for {parent}-->{child}."
            )
            logging.info(
                f"\tTrying to concatenating main dataframe & child dataframe for {parent}-->{child}."
            )
            df = pd.concat([df, df_child], ignore_index=True)
            logging.info("\tChild Dataframe concatenated with main Dataframe df")
    return df


def clean_html_tags(df: pd.DataFrame) -> None:
    df.review.replace(to_replace="<{1,}.{0,4}>", value="", regex=True, inplace=True)


def change_label(df: pd.DataFrame) -> None:
    df.label.replace({"neg": "Negative", "pos": "Positive"}, inplace=True)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, target_file: pathlib.Path) -> None:
    df.to_csv(str(target_file), header=True, index=False)


def upload_file_to_gcs(
    target_file: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_file)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        extract_here=pathlib.Path(os.environ["EXTRACT_HERE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
    )
