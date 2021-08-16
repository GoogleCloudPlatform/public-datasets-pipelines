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

# CSV transform for: covid19_italy.data_by_region

import datetime
import logging
import os
import pathlib

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
):

    logging.info(
        "Covid-19 Italy (By Region) process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    logging.info(f"Downloading file {source_url}")
    download_file(source_url, source_file)

    # open the input file
    logging.info(f"Opening file {source_file}")

    df = pd.read_csv(str(source_file))

    # steps in the pipeline
    logging.info(f"Transformation Process Starting.. {source_file}")

    # rename the headers
    logging.info(f"Transform: Renaming Headers.. {source_file}")
    rename_headers(df)

    # create location_geom
    logging.info(f"Transform: Creating Geometry Column.. {source_file}")
    df["location_geom"] = (
        "POINT("
        + df["longitude"].astype(str).replace("nan", "")
        + " "
        + df["latitude"].astype(str).replace("nan", "")
        + ")"
    )

    # replace blank POINT( ) valye with blank
    df.location_geom = df.location_geom.replace("POINT( )", "")

    # reorder headers in output
    logging.info("Transform: Reordering headers..")
    df = df[
        [
            "date",
            "country",
            "region_code",
            "region_name",
            "latitude",
            "longitude",
            "location_geom",
            "hospitalized_patients_symptoms",
            "hospitalized_patients_intensive_care",
            "total_hospitalized_patients",
            "home_confinement_cases",
            "total_current_confirmed_cases",
            "new_current_confirmed_cases",
            "new_total_confirmed_cases",
            "recovered",
            "deaths",
            "total_confirmed_cases",
            "tests_performed",
            "note",
        ]
    ]

    # steps in the pipeline
    logging.info(f"Transformation Process complete .. {source_file}")

    # save to output file
    logging.info(f"Saving to output file.. {target_file}")

    try:
        # save_to_new_file(df, file_path=str(target_file))
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    # log completion
    logging.info(
        "Covid-19 Italy (By Region) process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def convert_dt_format(date_str, time_str):
    #  date_str, time_str
    # 10/26/2014,13:12:00
    return str(datetime.datetime.strptime(date_str, "%m/%d/%Y").date()) + " " + time_str


def rename_headers(df):
    header_names = {
        "data": "date",
        "stato": "country",
        "codice_regione": "region_code",
        "denominazione_regione": "region_name",
        "lat": "latitude",
        "long": "longitude",
        "ricoverati_con_sintomi": "hospitalized_patients_symptoms",
        "terapia_intensiva": "hospitalized_patients_intensive_care",
        "totale_ospedalizzati": "total_hospitalized_patients",
        "isolamento_domiciliare": "home_confinement_cases",
        "totale_positivi": "total_current_confirmed_cases",
        "variazione_totale_positivi": "new_current_confirmed_cases",
        "nuovi_positivi": "new_total_confirmed_cases",
        "note": "note",
        "dimessi_guariti": "recovered",
        "totale_casi": "total_confirmed_cases",
        "tamponi": "tests_performed",
        "deceduti": "deaths",
    }

    df = df.rename(columns=header_names, inplace=True)


def save_to_new_file(df, file_path):
    df.to_csv(file_path, float_format="%.0f", index=False)


def download_file(source_url: str, source_file: pathlib.Path):
    logging.info(f"Downloading {source_url} into {source_file}")
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(source_file, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.error(f"Couldn't download {source_url}: {r.text}")


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    # if os.environ["PIPELINE"] == 'data_by_region':
    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
