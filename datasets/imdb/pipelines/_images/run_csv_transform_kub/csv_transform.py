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
import math
import os
import pathlib
import tarfile
import typing

import pandas as pd
import requests
from google.cloud import storage

TEST_TRAIN = ["test", "train"]
NEG_POS_UNSUP = ["neg", "pos", "unsup"]
REVIEW_COLS = ["review", "split", "label", "id_tag", "path", "reviewer_rating"]


def main(
    source_gcs_bucket: str,
    source_gcs_object: str,
    source_url: dict,
    source_file: dict,
    extract_here: pathlib.Path,
    target_csv_file: pathlib.Path,
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
    logging.info(f"Creating './files' folder under {os.getcwd()}")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    logging.info(
        f"Downloading data from {source_url['title_link']} to {source_file['title_data']}."
    )
    download_gzfile(source_url["title_link"], source_file["title_data"])
    logging.info("Downloading Completed.")

    logging.info(
        f"Downloading data from gs://{source_gcs_bucket}/{source_gcs_object} to {source_file['user_review_data']}"
    )
    download_blob(source_gcs_bucket, source_gcs_object, source_file["user_review_data"])
    logging.info("Downloading Completed.")

    logging.info(f"Extracting tar.gz file to -> {extract_here}.")
    extract_tar(source_file["user_review_data"], extract_here)
    logging.info(f"Successfully extracted tar file to -> {extract_here}.")

    logging.info("Started creating Dataframe for reviews(data).")
    df_reviews = create_dataframe(extract_here)
    logging.info("Successfully Created Dataframe and assigned to variable df_reviews.")

    df = add_movie_title(df_reviews, source_file["title_data"])
    logging.info("Successfully created final Dataframe.")

    logging.info("Started cleaning html tags from the user review.")
    clean_html_tags(df, "review")
    logging.info("Cleaning html tags completed.")

    logging.info(
        'Changing "label" column data from  ["neg", "pos", "unsup"] --> ["Negative", "Positive", "Unsupervised"].'
    )
    change_label(df, "label")
    logging.info('Successfully replaced "label" column data.')

    logging.info("Renaming headers")
    rename_headers(df, rename_mappings)

    logging.info(f"Saving to output file to ... {target_csv_file}")
    try:
        save_to_newfile(df, target_csv_file, headers)
        logging.info("Successfully saved.")
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    upload_file_to_gcs(target_csv_file, target_gcs_bucket, target_gcs_path)
    logging.info("Successfully uploaded file to gcs bucket.")

    logging.info(
        f"IMDb Dataset {pipeline_name} pipeline process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def download_gzfile(source_url: str, source_file: str):
    logging.info(f"Downloading data from {source_url}...")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
    else:
        logging.info(f"Couldn't download {source_url}: {res.text}")
    logging.info(f"Downloaded {source_url} into {source_file}")


def download_blob(source_gcs_bucket: str, source_gcs_object: str, target_file: str):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(source_gcs_bucket)
    blob = bucket.blob(source_gcs_object)
    blob.download_to_filename(target_file)


def extract_tar(source_file: pathlib.Path, extract_here: pathlib.Path):
    if "tar.gz" in source_file:
        with tarfile.open(str(source_file), "r") as tar_fb:
            tar_fb.extractall(extract_here)


def get_id_rating(file: str, index: int):
    if "unsup" in file and index == 1:
        return math.nan
    return int(file.split("/")[-1].split(".")[0].split("_")[index])


def allign_data(file: str):
    review = open(file).read()
    split = str(file).split("/")[2]
    label = file.split("/")[-2]
    review_path = file
    id_tag = get_id_rating(file, 0)
    reviewer_rating = get_id_rating(file, 1)
    return [review, split, label, id_tag, review_path, reviewer_rating]


def add_movie_url(parent: str, child: str, df: pd.DataFrame, id_tag: str):
    urls = []
    try:
        with open(f"./files/aclImdb/{parent}/urls_{child}.txt") as fb:
            urls.extend(fb.read().splitlines())
        urls = [url.replace("usercomments", "") for url in urls]
        movie_title_dict = dict(enumerate(urls))
        return df[id_tag].map(movie_title_dict, na_action=None)
    except FileNotFoundError as e:
        logging.info(f"\t\t{e}.")


def add_movie_id(df: pd.DataFrame, column: str, index: int):
    return df[column].apply(lambda row: row.split("/")[index])


def create_dataframe(extract_here: pathlib.Path):
    df_reviews = pd.DataFrame(columns=REVIEW_COLS)
    for parent in TEST_TRAIN:
        for child in NEG_POS_UNSUP:
            if parent == "test" and child == "unsup":
                break
            path = f"{extract_here}/aclImdb/{parent}/{child}/"
            csv_files = list(glob.glob(path + "*.txt"))
            logging.info(
                f"\tCreating Dataframe by reading files from {parent}-->{child}."
            )
            df_child = pd.DataFrame(
                [allign_data(file) for file in csv_files], columns=REVIEW_COLS
            )
            logging.info("\tAdding movie_url column")
            df_child["movie_url"] = add_movie_url(parent, child, df_child, "id_tag")
            logging.info("\tAdding movie_id column")
            df_child["movie_id"] = add_movie_id(df_child, "movie_url", -2)
            logging.info(
                f"\tTrying to concatenating main dataframe & child dataframe for {parent}-->{child} (folder)."
            )
            df_reviews = pd.concat([df_reviews, df_child], ignore_index=True)
            logging.info("\tChild Dataframe concatenated with main Dataframe df")
    return df_reviews


def add_movie_title(df: pd.DataFrame, source_url_path: str):
    logging.info("Started creating Dataframe for title_basics(data).")
    logging.info(
        f"\tCreating Dataframe(df_title_basics) for movie_id and title by reading ./files/{(source_url_path).split('/')[-1]}."
    )
    df_title_basics = pd.read_csv(
        str(source_url_path),
        sep="\t",
        compression="gzip",
        usecols=["tconst", "primaryTitle"],
    )
    logging.info(
        "\tRenaming Dataframe(df_title_basics) columns from ['tconst', 'primaryTitle'] -> ['movie_id', 'title']."
    )
    df_title_basics.rename(
        columns={"tconst": "movie_id", "primaryTitle": "title"}, inplace=True
    )
    logging.info(
        "Merging two Dataframes(df_reviews & df_title_basics) by using left-join and assigned to variable df"
    )
    df = pd.merge(df, df_title_basics, how="left")
    return df


def clean_html_tags(df: pd.DataFrame, review: str) -> None:
    df[review].replace(to_replace="<{1,}.{0,4}>", value="", regex=True, inplace=True)


def change_label(df: pd.DataFrame, label: str) -> None:
    df[label].replace(
        {"neg": "Negative", "pos": "Positive", "unsup": "Unsupervised"}, inplace=True
    )


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    df.rename(columns=rename_mappings, inplace=True)


def save_to_newfile(
    df: pd.DataFrame, target_csv_file: pathlib.Path, headers: typing.List[str]
) -> None:
    df.to_csv(str(target_csv_file), header=True, index=False, columns=headers)


def upload_file_to_gcs(
    target_csv_file: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_csv_file)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_gcs_bucket=os.environ.get("SOURCE_GCS_BUCKET"),
        source_gcs_object=os.environ.get("SOURCE_GCS_OBJECT"),
        source_url=json.loads(os.environ.get("SOURCE_URL")),
        source_file=json.loads(os.environ.get("SOURCE_FILE")),
        extract_here=pathlib.Path(os.environ.get("EXTRACT_HERE")).expanduser(),
        target_csv_file=pathlib.Path(os.environ.get("TARGET_CSV_FILE")).expanduser(),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET"),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH"),
        headers=json.loads(os.environ.get("CSV_HEADERS")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS")),
        pipeline_name=os.environ.get("PIPELINE_NAME"),
    )
