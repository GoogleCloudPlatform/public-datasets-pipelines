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

    curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logging.info(
        f"NOAA Lightning Strikes By Year process started at {curr_dtm}"
    )

    if url_is_reachable(source_url):

        source_file_zipped = str(source_file) + ".gz"
        source_file_unzipped = str(source_file) + ".1"

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Downloading source file {source_url} at {curr_dtm}")
        download_file(source_url, source_file_zipped)

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Decompressing {source_file_unzipped} at {curr_dtm}")
        gz_decompress(source_file_zipped, source_file_unzipped)

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Removing unnecessary header in {source_file_unzipped} at {curr_dtm}")
        os.system(f"echo 'DATE,LONGITUDE,LATITUDE,TOTAL_COUNT' > {source_file}")
        os.system(f"tail -n +4 {source_file_unzipped} >> {source_file}")
        os.unlink(source_file_unzipped)
        os.unlink(source_file_zipped)

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Opening source file {source_file} at {curr_dtm}")
        df = pd.read_csv(str(source_file))

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Transform: Renaming Headers.. {source_file} at {curr_dtm}")
        df.columns = ["day_int", "centerlon", "centerlat", "number_of_strikes"]

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Converting datetime format in {source_file} at {curr_dtm}")
        df["day"] = pd.to_datetime(
            (df["day_int"][:].astype("string")), "raise", False, True
        )

        logging.info(f"Adding geography column in {source_file} at {curr_dtm}")
        df["center_point"] = (
            "POINT("
            + df["centerlon"][:].astype("string")
            + " "
            + df["centerlat"][:].astype("string")
            + ")"
        )

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Reordering columns in {source_file} at {curr_dtm}")
        df = df[["day", "number_of_strikes", "center_point"]]

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Transform: Saving to output file.. {target_file} at {curr_dtm}")
        df.to_csv(target_file, index=False)

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"completed processing {source_url} at {curr_dtm}")

        logging.info(
            f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path} at {curr_dtm}"
        )
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(
            f"NOAA Lightning Strikes By Year process completed at {curr_dtm}"
        )

    else:

        curr_dtm = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info(f"Error: Unable to reach url: {source_url} at {curr_dtm}")
        logging.info("Process failed!")


def gz_decompress(infile: str, tofile: str) -> None:
    # open infile (gzip file) for read and opfile for write (decompressed)
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        # decompress the file
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        # write the file as decompressed
        tof.write(decom_str)


def url_is_reachable(url: str) -> str:
    # Is the URL reachable?

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

    # source url should contain the year as {year} in the source url eg. "https://my.site.gov/../../data_file_{year}.csv.gz"
    main(
        source_url=os.environ["SOURCE_URL"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
