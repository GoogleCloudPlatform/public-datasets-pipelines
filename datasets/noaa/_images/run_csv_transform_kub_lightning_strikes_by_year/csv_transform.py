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

import gzip
import logging
import os
import pathlib
import urllib.request

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

    logging.info("NOAA Lightning Strikes By Year process started")

    if url_is_reachable(source_url):

        logging.info("creating 'files' folder")
        pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

        source_file_zipped = str(source_file) + ".gz"
        source_file_unzipped = str(source_file) + ".1"

        logging.info(f"Downloading source file {source_url}")
        download_file(source_url, source_file_zipped)

        logging.info(f"Decompressing {source_file_unzipped}")
        gz_decompress(source_file_zipped, source_file_unzipped)

        logging.info(f"Removing unnecessary header in {source_file_unzipped}")
        os.system(f"echo 'DATE,LONGITUDE,LATITUDE,TOTAL_COUNT' > {source_file}")
        os.system(f"tail -n +4 {source_file_unzipped} >> {source_file}")
        os.unlink(source_file_unzipped)
        os.unlink(source_file_zipped)

        logging.info(f"Opening source file {source_file}")
        df = pd.read_csv(str(source_file))

        logging.info(f"Transform: Renaming Headers.. {source_file}")
        df.columns = ["day_int", "centerlon", "centerlat", "number_of_strikes"]

        logging.info(f"Converting datetime format in {source_file}")
        df["day"] = (
            pd.to_datetime(
                (df["day_int"][:].astype("string") + "000000"), "raise", False, True
            ).astype(str)
            + " 00:00:00"
        )

        df["center_point"] = (
            "POINT("
            + df["centerlon"][:].astype("string")
            + " "
            + df["centerlat"][:].astype("string")
            + ")"
        )

        logging.info(f"Reordering columns in {source_file}")
        df = df[["day", "number_of_strikes", "center_point"]]

        logging.info(f"Transform: Saving to output file.. {target_file}")
        df.to_csv(target_file, index=False)

        logging.info(f"completed processing {source_url}")
        logging.info(
            f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

        logging.info("NOAA Lightning Strikes By Year process completed")

    else:

        logging.info(f"Error: Unable to reach url: {source_url}")
        logging.info("Process failed!")


def gz_decompress(infile: str, tofile: str) -> None:
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def url_is_reachable(url: str) -> bool:

    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


def download_file(source_url: str, source_file: pathlib.Path) -> None:
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

    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
