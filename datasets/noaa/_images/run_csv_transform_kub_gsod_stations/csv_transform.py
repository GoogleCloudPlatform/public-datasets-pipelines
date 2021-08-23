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

# CSV transform for: austin_311.311_service_request

# import modules
import datetime
import gzip
import logging
import os
import pathlib
import re
import urllib.request
from ftplib import FTP

import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
):

    # source_url            STRING          -> The full url of the source file to transform
    # ftp_host              STRING          -> The host IP of the ftp file (IP only)
    # ftp_dir               STRING          -> The remote working directory that the FTP file resides in (directory only)
    # ftp_filename          STRING          -> The name of the file to pull from the FTP site
    # source_file           PATHLIB.PATH    -> The (local) path pertaining to the downloaded source file
    # target_file           PATHLIB.PATH    -> The (local) target transformed file + filename
    # target_gcs_bucket     STRING          -> The target GCS bucket to place the output (transformed) file
    # target_gcs_path       STRING          -> The target GCS path ( within the GCS bucket ) to place the output (transformed) file

    # log that process has started
    logging.info(
        "NOAA GSOD Stations By Year process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info(f"starting processing {source_url}")

    if url_is_reachable(source_url):

        logging.info("creating 'files' folder")
        pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

        logging.info(f"Downloading FTP file {source_url} from {ftp_host}")
        download_file_ftp(ftp_host, ftp_dir, ftp_filename, source_file, source_url)

        # append to source_file (exclude first 3 lines of header)
        logging.info(f"Removing unnecessary header in {source_file}")
        os.system(f"tail -n +21 {source_file}.bak > {source_file}.1")
        # os.system(f"cat {source_file}.1 > {source_file}")
        os.system(f"sed '2d' {source_file}.1 > {source_file}")
        os.unlink(str(source_file) + ".bak")
        os.unlink(str(source_file) + ".1")

        # open file as dataframe
        logging.info(f"Opening source file {source_file}")
        colspecs = [
            (0, 6),
            (7, 12),
            (13, 42),
            (43, 45),
            (48, 50),
            (51, 56),
            (57, 64),
            (65, 74),
            (75, 81),
            (82, 90),
            (91, 99),
        ]
        df = pd.read_fwf(str(source_file), colspecs=colspecs)

        # rename the headers
        logging.info(f"Transform: Renaming Headers.. {source_file}")
        df.columns = [
            "usaf",
            "wban",
            "name",
            "country",
            "state",
            "call",
            "lat",
            "lon",
            "elev",
            "begin",
            "end",
        ]

        # remove rows with empty (usaf) data
        df = df[df.usaf != ""]

        # execute reg-ex replacements
        logging.info(f"Transform: Executing Reg Ex.. {source_file}")
        logging.info(f"           Executing Reg Ex.. (lat) {source_file}")
        df["lat"] = df["lat"].astype(str)
        df["lat"][:].replace("^(-[0]+)(.*)", "-$2", regex=True, inplace=True)
        df["lat"][:].replace("^(\\s+)$", "", regex=True, inplace=True)
        df["lat"][:].replace(
            "^(\\+\\d+\\.\\d+[0-9])\\s+", "$1", regex=True, inplace=True
        )
        df["lat"][:].replace("^(-\\d+\\.\\d+[0-9])\\s+", "$1", regex=True, inplace=True)
        df["lat"][:].replace("nan", "", regex=False, inplace=True)

        logging.info(f"           Executing Reg Ex.. (lon) {source_file}")
        df["lon"] = df["lon"].astype(str)
        df["lon"][:].replace("^(-[0]+)(.*)", "-$2", regex=True, inplace=True)
        df["lon"][:].replace("^(\\s+)$", "", regex=True, inplace=True)
        df["lon"][:].replace(
            "^(\\+\\d+\\.\\d+[0-9])\\s+", "$1", regex=True, inplace=True
        )
        df["lon"][:].replace("^(-\\d+\\.\\d+[0-9])\\s+", "$1", regex=True, inplace=True)
        df["lon"][:].replace("nan", "", regex=False, inplace=True)

        logging.info(f"           Executing Reg Ex.. (usaf) {source_file}")
        df["usaf"][:].replace("(\\d{1,})(\\s{1,})$", "$1", regex=True, inplace=True)

        logging.info(f"           Executing Reg Ex.. (name) {source_file}")
        df["name"][:].replace("^\\s{1,}([a-zA-Z]\\D+)", "$1", regex=True, inplace=True)
        df["name"][:].replace("^(\\D+[a-zA-Z])\\s{1,}$", "$1", regex=True, inplace=True)
        df["name"][:].replace("^(\\s+)$", "", regex=True, inplace=True)

        logging.info(f"           Executing Reg Ex.. (call) {source_file}")
        df["call"][:].replace("^(\\s+)$", "", regex=True, inplace=True)
        df["call"][:].replace("^([a-zA-Z]+)\\s+", "$1", regex=True, inplace=True)

        logging.info(f"           Executing Reg Ex.. (elev) {source_file}")
        df["elev"][:].replace("^(\\s+)$", "", regex=True, inplace=True)

        logging.info(f"           Executing Reg Ex.. (state) {source_file}")
        df["state"][:].replace("^(\\s+)$", "", regex=True, inplace=True)

        logging.info(f"           Executing Reg Ex.. (country) {source_file}")
        df["country"][:].replace("^(\\s+)$", "", regex=True, inplace=True)

        logging.info(f"Transform: Saving to output file.. {target_file}")
        df.to_csv(target_file, index=False)

        logging.info(f"completed processing {source_url}")

        # pdb.set_trace()

        logging.info(
            f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
        )
        upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

        # log completion
        logging.info(
            "NOAA GSOD Stations process completed at "
            + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    else:

        # we were unable to reach the url
        logging.info(f"Error: Unable to reach url: {source_url}")
        logging.info("Process failed!")


def replace_value(val):
    if val is None or len(val) == 0:
        return val
    else:
        if val.find("\n") > 0:
            # return val.replace("\n", "")
            return re.sub(r"(^\d):(\d{2}:\d{2})", "0$1:$2", val)
        else:
            return val


def replace_values_regex(df):
    header_names = {"checkout_time"}

    for dt_col in header_names:
        if df[dt_col] is not None:
            if df[dt_col].str.len() > 0:
                df[dt_col] = df[dt_col].apply(replace_value)


def download_file_ftp(
    ftp_host: str,
    ftp_dir: str,
    ftp_filename: str,
    local_file: pathlib.Path,
    source_url: str,
):

    # ftp_host      -> host ip (eg. 123.123.0.1)
    # ftp_dir       -> working directory in ftp host where file is located
    # ftp_filename  -> filename of FTP file to download
    # source_file   -> local file (including path) to create containing ftp content

    logging.info(f"Downloading {source_url} into {local_file}")
    ftp_conn = FTP(ftp_host)
    ftp_conn.login("", "")
    ftp_conn.cwd(ftp_dir)
    # ftp_conn.encoding = 'utf-8'

    try:
        bak_local_file = str(local_file) + ".bak"
        dest_file = open(bak_local_file, "wb")
        ftp_conn.encoding = "utf-8"
        ftp_conn.retrbinary(
            cmd="RETR " + ftp_filename,
            callback=dest_file.write,
            blocksize=1024,
            rest=None,
        )
        ftp_conn.quit()
        dest_file.close()
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")


def gz_decompress(infile, tofile):
    # open infile (gzip file) for read and opfile for write (decompressed)
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        # decompress the file
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        # write the file as decompressed
        tof.write(decom_str)


def url_is_reachable(url):
    # Is the URL reachable?

    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


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

    # source url should contain the year as {year} in the source url eg. "https://my.site.gov/../../data_file_{year}.csv.gz"
    main(
        source_url=os.environ["SOURCE_URL"],
        ftp_host=os.environ["FTP_HOST"],
        ftp_dir=os.environ["FTP_DIR"],
        ftp_filename=os.environ["FTP_FILENAME"],
        source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
