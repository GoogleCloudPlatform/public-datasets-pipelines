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
import tempfile
import typing
from datetime import date, datetime, timedelta

import bs4
import requests
from google.cloud import storage


def main(
    base_url: str,
    today: date,
    download_dir: pathlib.Path,
    target_bucket: str,
    manifest_path: pathlib.Path,
    days_rolling: int,
    batch_size: int,
) -> None:
    # Collects all paths that span the last N days rolling.
    # Example path: Y2021/M01/D01
    source_paths = folder_paths_last_n_days(today, n_days=days_rolling)
    create_local_dirs(download_dir, source_paths)

    new_paths = set()
    for source_path in source_paths:
        url = f"{base_url}/{source_path}"

        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"Scraping .nc4 files in {url}")
            webpage = bs4.BeautifulSoup(response.text, "html.parser")
            new_paths.update(scrape(source_path, webpage))
        else:
            logging.warning(
                f"The following URL doesn't exist, will try again later: {url}"
            )

    old_paths = get_old_paths(target_bucket, manifest_path)
    for_download = urls_to_download(old_paths, new_paths)

    copy_new_files(download_dir, for_download, manifest_path, batch_size, target_bucket)
    remove_old_files_from_gcs(
        download_dir, base_url, urls_to_delete(old_paths, new_paths)
    )
    update_manifest_file(new_paths, manifest_path, target_bucket)


def folder_paths_last_n_days(today: date, n_days: int) -> typing.List[str]:
    dates = [today - timedelta(days=n) for n in range(n_days)]

    # Generates URLs to folders containing the .nc4 files, for example
    # https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das/Y2021/M01/D01/
    return [f"Y{dt.year}/M{dt.month:0>2}/D{dt.day:0>2}" for dt in dates]


def create_local_dirs(
    download_dir: pathlib.Path, source_paths: typing.List[str]
) -> None:
    for source_path in source_paths:
        (download_dir / source_path).mkdir(parents=True, exist_ok=True)


def scrape(source_path: str, webpage: bs4.BeautifulSoup) -> typing.List[str]:
    file_paths = []

    # Finds all URLs that end with ".nc4"
    for a_tag in webpage.find_all("a"):

        # The `href` property is the filename,
        # e.g. GEOS.fp.asm.inst1_2d_smp_Nx.20210101_1700.V01.nc4
        if a_tag.get("href") and a_tag["href"].endswith(".nc4"):
            file_paths.append(f"{source_path}/{a_tag['href']}")

    return file_paths


def get_old_paths(bucket_name: str, manifest_path: pathlib.Path) -> typing.Set[str]:
    name = "manifest.txt"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    if storage.Blob(bucket=bucket, name=name).exists(storage_client):
        logging.info(f"Manifest file found at gs://{bucket_name}/{name}")
        blob = bucket.blob(name)
        blob.download_to_filename(str(manifest_path))
        return set(manifest_path.read_text().split("\n"))
    else:
        manifest_path.touch()
        return set()


def download_item(parent_dir: pathlib.Path, file_path: str) -> None:
    r = requests.get(f"{os.environ['BASE_URL']}/{file_path}", stream=True)
    if r.status_code == 200:
        with open(parent_dir / file_path, "wb") as f:
            for chunk in r:
                f.write(chunk)
    else:
        logging.warning(f"Couldn't download {file_path}: {r.text}")


def copy_new_files(
    download_dir: pathlib.Path,
    file_paths: typing.List[str],
    manifest_path: pathlib.Path,
    batch_size: int,
    target_bucket: str,
) -> None:
    total_files = len(file_paths)
    logging.info(f"Downloading {total_files} files.")
    for n, batch in enumerate(batches(file_paths, batch_size=batch_size), 1):
        logging.info(
            f"Processing batch {n}: {(n - 1) * batch_size + 1} to {min(total_files, n * batch_size)}"
        )
        copy_batch(batch, download_dir, target_bucket)

        manifest = set(manifest_path.read_text().split("\n"))
        manifest.update(batch)
        update_manifest_file(
            paths=manifest,
            manifest_path=manifest_path,
            target_bucket=target_bucket,
        )


def copy_batch(
    batch: typing.List[str],
    download_dir: pathlib.Path,
    target_bucket: str,
) -> None:
    for file_path in batch:
        download_item(pathlib.Path(download_dir), file_path)
    move_contents_to_gcs(pathlib.Path(download_dir), target_bucket)


def move_contents_to_gcs(dir: pathlib.Path, target_bucket: str) -> None:
    subprocess.check_call(
        ["gsutil", "-m", "mv", "-r", f"{dir}/", f"gs://{target_bucket}"]
    )


def remove_old_files_from_gcs(
    download_dir: pathlib.Path, base_url: str, file_paths: typing.List[str]
) -> None:
    logging.info(f"Deleting {len(file_paths)} files.")

    if not file_paths:
        return

    # Save the urls in a temporary text file, so we can pass it into gsutil
    # with the `-m` option to perform parallel deletions.
    with tempfile.NamedTemporaryFile(dir=download_dir, mode="w") as tmp_file:
        tmp_file.write(
            "\n".join([f"{base_url}/{file_path}" for file_path in file_paths])
        )

        ps = subprocess.Popen(["cat", tmp_file], stdout=subprocess.PIPE)
        subprocess.check_output(["gsutil", "-m", "rm", "-I"], stdin=ps.stdout)
        ps.wait()


def update_manifest_file(
    paths: typing.Set[str], manifest_path: pathlib.Path, target_bucket: str
) -> None:
    with open(manifest_path, "w") as file_:
        file_.write("\n".join(paths))
    subprocess.check_call(["gsutil", "cp", manifest_path, f"gs://{target_bucket}"])


def urls_to_download(
    old_urls: typing.Set[str], new_urls: typing.Set[str]
) -> typing.Set[str]:
    urls = []
    for new_url in new_urls:
        if new_url not in old_urls:
            urls.append(new_url)
    return urls


def urls_to_delete(
    old_urls: typing.Set[str], new_urls: typing.Set[str]
) -> typing.Set[str]:
    urls = []
    for old_url in old_urls:
        if old_url not in new_urls:
            urls.append(old_url)
    return urls


def batches(file_paths: typing.List[str], batch_size: int):
    for i in range(0, len(file_paths), batch_size):
        yield file_paths[i : i + batch_size]


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    assert os.environ["TODAY"]
    assert os.environ["BASE_URL"]
    assert os.environ["DOWNLOAD_DIR"]
    assert os.environ["TARGET_BUCKET"]
    assert os.environ["MANIFEST_PATH"]

    main(
        base_url=os.environ["BASE_URL"],
        today=datetime.strptime(os.environ["TODAY"], "%Y-%m-%d").date(),
        download_dir=pathlib.Path(os.environ["DOWNLOAD_DIR"]).expanduser(),
        manifest_path=pathlib.Path(os.environ["MANIFEST_PATH"]).expanduser(),
        target_bucket=os.environ["TARGET_BUCKET"],
        days_rolling=int(os.getenv("DAYS_ROLLING", 10)),
        batch_size=int(os.getenv("BATCH_SIZE", 100)),
    )
