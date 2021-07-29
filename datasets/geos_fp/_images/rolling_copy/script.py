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
import subprocess
import typing
from datetime import date, timedelta

import bs4
import requests
from google.cloud import storage

# The manifest file contains a list of files already downloaded for a given date
MANIFEST_FILE = "manifest.txt"


def main(
    base_url: str,
    dt: date,
    download_dir: pathlib.Path,
    target_bucket: str,
    batch_size: int,
) -> None:
    # Get date prefix, e.g. Y2021/M01/D01, and create directories for them
    date_prefix = _date_prefix(dt)
    (download_dir / date_prefix).mkdir(parents=True, exist_ok=True)

    # Generate a set of all .nc4 files from the specified url and date
    all_files = get_all_files(base_url, date_prefix)

    stored_files = get_stored_files(target_bucket, date_prefix, download_dir)

    # Files present in the source webpage but not yet stored on GCS
    unstored_files = all_files - stored_files

    download_and_store_new_files(
        download_dir, date_prefix, unstored_files, batch_size, target_bucket
    )


def _date_prefix(dt: date) -> typing.List[str]:
    # Generates URL paths to folders containing the .nc4 files, for example
    # https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das/Y2021/M01/D01/
    # => Y2021/M01/D01
    return f"Y{dt.year}/M{dt.month:0>2}/D{dt.day:0>2}"


def get_all_files(base_url: str, date_prefix: str) -> typing.Set[str]:
    all_files = set()
    url = f"{base_url}/{date_prefix}"
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f"Scraping .nc4 files in {url}")
        webpage = bs4.BeautifulSoup(response.text, "html.parser")
        all_files.update(scrape(date_prefix, webpage))
    else:
        logging.warning(f"The following URL doesn't exist, will try again later: {url}")
    return all_files


def get_stored_files(
    bucket_name: str, date_prefix: str, download_dir: pathlib.Path
) -> typing.Set[str]:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    gcs_object = f"{date_prefix}/{MANIFEST_FILE}"
    local_object = download_dir / MANIFEST_FILE

    if storage.Blob(bucket=bucket, name=gcs_object).exists(storage_client):
        logging.info(f"Manifest file found at gs://{bucket_name}/{gcs_object}")
        blob = bucket.blob(gcs_object)
        blob.download_to_filename(str(local_object))
    else:
        local_object.touch()

    with open(local_object) as f:
        return set(f.read().splitlines())


def scrape(source_path: str, webpage: bs4.BeautifulSoup) -> typing.List[str]:
    file_paths = []

    # Go through all the URLs in the page and collect the ones ending in ".nc4"
    for a_tag in webpage.find_all("a"):

        # The `href` property is the filename,
        # e.g. GEOS.fp.asm.inst1_2d_smp_Nx.20210101_1700.V01.nc4
        if a_tag.get("href") and a_tag["href"].endswith(".nc4"):
            file_paths.append(f"{source_path}/{a_tag['href']}")

    return file_paths


def download_and_store_new_files(
    download_dir: pathlib.Path,
    date_prefix: str,
    new_files: typing.Set[str],
    batch_size: int,
    target_bucket: str,
) -> None:
    """In batches, download files from the source to the local filesystem
    and upload them to the GCS target bucket
    """
    total_files = len(new_files)
    logging.info(f"Downloading {total_files} files.")
    for n, batch in enumerate(batches(list(new_files), batch_size=batch_size), 1):
        logging.info(
            f"Processing batch {n}: {(n - 1) * batch_size + 1} to {min(total_files, n * batch_size)}"
        )
        download_batch(batch, download_dir)
        move_dir_contents_to_gcs(download_dir, target_bucket, date_prefix)
        update_manifest_file(batch, download_dir, target_bucket, date_prefix)


def download_batch(batch: typing.List[str], download_dir: pathlib.Path) -> None:
    for file_path in batch:
        logging.info(f"Downloading file to {download_dir}/{file_path}")
        subprocess.check_call(
            [
                "wget",
                f"{os.environ['BASE_URL']}/{file_path}",
                "-O",
                f"{download_dir}/{file_path}",
                "-nv",
            ]
        )


def move_dir_contents_to_gcs(
    dir_: pathlib.Path, target_bucket: str, date_prefix: str
) -> None:
    subprocess.check_call(
        [
            "gsutil",
            "-m",
            "-o",
            "GSUtil:parallel_composite_upload_threshold=250M",
            "cp",
            f"{dir_}/{date_prefix}/*.nc4",
            f"gs://{target_bucket}/{date_prefix}",
        ]
    )
    delete_dir_contents(dir_ / date_prefix)


def delete_dir_contents(dir_to_delete: pathlib.Path) -> None:
    """Delete directory contents, but not the dir itself. This is useful for keeping
    date dirs such as Y2021/M07/D12 intact for the next batch of files to use.
    """
    [f.unlink() for f in dir_to_delete.glob("*") if f.is_file()]


def update_manifest_file(
    paths: typing.Set[str],
    download_dir: pathlib.Path,
    target_bucket: str,
    date_prefix: str,
) -> None:
    manifest_path = download_dir / MANIFEST_FILE
    with open(manifest_path, "a") as f:
        f.write("\n".join(paths))
        f.write("\n")
    subprocess.check_call(
        [
            "gsutil",
            "cp",
            str(manifest_path),
            f"gs://{target_bucket}/{date_prefix}/{MANIFEST_FILE}",
        ]
    )


def batches(file_paths: typing.List[str], batch_size: int):
    for i in range(0, len(file_paths), batch_size):
        yield file_paths[i : i + batch_size]


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    assert os.environ["BASE_URL"]
    assert os.environ["TODAY_DIFF"]
    assert os.environ["DOWNLOAD_DIR"]
    assert os.environ["TARGET_BUCKET"]

    main(
        base_url=os.environ["BASE_URL"],
        dt=(date.today() - timedelta(days=int(os.environ["TODAY_DIFF"]))),
        download_dir=pathlib.Path(os.environ["DOWNLOAD_DIR"]).expanduser(),
        target_bucket=os.environ["TARGET_BUCKET"],
        batch_size=int(os.getenv("BATCH_SIZE", 10)),
    )
