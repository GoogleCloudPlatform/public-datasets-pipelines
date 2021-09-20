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

# import modules
import datetime
import logging
import os
import pathlib
import subprocess

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info("San Francisco - Film Locations process started")

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file, engine="python", encoding="utf-8", quotechar='"', chunksize=chunksz
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            logging.info(f"Processing batch {chunk_number}")
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            processChunk(df, target_file_batch)
            logging.info(f"Appending batch {chunk_number} to {target_file}")
            if chunk_number == 0:
                subprocess.run(["cp", target_file_batch, target_file])
            else:
                subprocess.check_call(f"sed -i '1d' {target_file_batch}", shell=True)
                subprocess.check_call(
                    f"cat {target_file_batch} >> {target_file}", shell=True
                )
            subprocess.run(["rm", target_file_batch])

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("San Francisco - Film Locations process completed")


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def processChunk(df: pd.DataFrame, target_file_batch: str) -> None:

    logging.info(f"Transformation Process Starting")

    logging.info(f"Renaming Headers")
    rename_headers(df)

    logging.info("Trimming Whitespace")
    df["distributor"] = df["distributor"].apply(lambda x: str(x).strip())
    df["director"] = df["director"].apply(lambda x: str(x).strip())
    df["actor_2"] = df["actor_2"].apply(lambda x: str(x).strip())

    logging.info("Reordering headers..")
    df = df[
        [
            "title",
            "release_year",
            "locations",
            "fun_facts",
            "production_company",
            "distributor",
            "director",
            "writer",
            "actor_1",
            "actor_2",
            "actor_3"
        ]
    ]

    logging.info(f"Saving to target file.. {target_file_batch}")

    try:
        save_to_new_file(df, file_path=str(target_file_batch))
    except Exception as e:
        logging.error(f"Error saving to target file: {e}.")

    logging.info(f"Saved transformed source data to target file .. {target_file_batch}")


def convert_dt_format(dt_str: str) -> str:
    if not dt_str or dt_str == "nan":
        return str("")
    else:
        return str(datetime.datetime.strptime(str(dt_str), "%m/%d/%Y %H:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"))


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "Title": "title",
        "Release Year": "release_year",
        "Locations": "locations",
        "Fun Facts": "fun_facts",
        "Production Company": "production_company",
        "Distributor": "distributor",
        "Director": "director",
        "Writer": "writer",
        "Actor 1": "actor_1",
        "Actor 2": "actor_2",
        "Actor 3": "actor_3"
    }

    df = df.rename(columns=header_names, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path) -> None:
    df.to_csv(file_path, index=False)


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
