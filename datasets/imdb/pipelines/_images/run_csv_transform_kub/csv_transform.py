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

import numpy as np
import pandas as pd
import requests
from google.cloud import storage

TEST_TRAIN = ["test", "train"]
NEG_POS_UNSUP = ["neg", "pos", "unsup"]
REVIEW_COLS = ["review", "split", "label", "id_tag", "path", "reviewer_rating"]
LABEL_DICT = {"neg": "Negative", "pos": "Positive", "unsup": "Unsupervised"}
REPLACE_DICT = {"\\N": np.nan}
REPLACE_BINARY_DICT = {"0": 0, "1": 1, "0.0": 0, "1.0": 1, 0.0: 0, 1.0: 1}


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
    table_name: str,
    chunk_size: int,
) -> None:
    logging.info(
        f"IMDb Dataset {pipeline_name} pipeline process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info(f"Creating './files' folder under {os.getcwd()}")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    if pipeline_name == "reviews":
        df = get_reviews(
            source_gcs_bucket, source_gcs_object, source_url, source_file, extract_here
        )
    elif pipeline_name == "interfaces":
        download_gzfile(source_url.get("url", ""), source_file.get("url_data", ""))

    if table_name == "name_basics":
        df = get_name_basics(source_file)
    elif table_name == "title_akas":
        df = get_title_akas(
            source_file, chunk_size, rename_mappings, target_csv_file, headers
        )
    elif table_name == "title_basics":
        df = get_title_basics(source_file)
    elif table_name == "title_crew":
        df = get_title_crew(source_file)
    elif table_name == "title_episode":
        df = get_title_episode(source_file)
    elif table_name == "title_principals":
        df = get_title_principals(
            source_file, chunk_size, rename_mappings, target_csv_file, headers
        )
    elif table_name == "title_ratings":
        df = get_title_ratings(source_file)

    if table_name not in ("title_akas", "title_principals"):
        rename_headers(df, rename_mappings)
        try:
            save_to_newfile(df, target_csv_file, headers)

        except Exception as e:
            logging.error(f"Error saving output file: {e}.")

    upload_file_to_gcs(target_csv_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        f"IMDb Dataset {pipeline_name} pipeline process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def get_reviews(
    source_gcs_bucket: str,
    source_gcs_object: str,
    source_url: dict,
    source_file: dict,
    extract_here: pathlib.Path,
) -> pd.DataFrame:
    download_gzfile(source_url.get("title_link", ""), source_file.get("title_data", ""))
    download_blob(
        source_gcs_bucket, source_gcs_object, source_file.get("user_review_data", "")
    )
    extract_tar(source_file.get("user_review_data", ""), extract_here)
    df_reviews = create_dataframe(extract_here)
    df = add_movie_title(df_reviews, source_file.get("title_data", ""))
    clean_html_tags(df, "review")
    coldata_replace(df, "label", LABEL_DICT)
    return df


def get_name_basics(source_file: dict) -> pd.DataFrame:
    logging.info(f'Reading data from  {source_file.get("url_data", "")}')
    df = pd.read_csv(source_file.get("url_data", ""), sep="\t", compression="gzip")
    for col in df:
        if col in ("birthYear", "deathYear"):
            coldata_replace(df, col, REPLACE_DICT)
            convert_int(df, col, "Int64")
            continue
        elif col in ("knownForTitles"):
            coldata_replace(df, col, REPLACE_DICT)
    return df


def get_title_akas(
    source_file: dict,
    chunk_size: int,
    rename_mappings: dict,
    target_csv_file: pathlib.Path,
    headers: list,
) -> None:
    logging.info(f'Reading data from  {source_file.get("url_data", "")} in chunks')
    df_chunk = pd.read_csv(
        source_file.get("url_data", ""),
        sep="\t",
        compression="gzip",
        chunksize=chunk_size,
    )
    for idx, chunk in enumerate(df_chunk):
        logging.info(f"\t\tStarted cleaning chunk {idx}.")
        chunk_cleaned = chunk_clean_akas(chunk)
        if idx == 0:
            rename_headers(chunk_cleaned, rename_mappings)
            logging.info(f"csv headers are {headers}")
            logging.info(f"Writing data to {target_csv_file}.")
            chunk_cleaned.to_csv(str(target_csv_file), index=False, columns=headers)
        else:
            logging.info(f"Appending data to {target_csv_file}.")
            chunk_cleaned.to_csv(
                str(target_csv_file), index=False, mode="a", header=False
            )
        logging.info(f"{idx} chunk shape {chunk_cleaned.shape}")
    logging.info(f"Successfully created {target_csv_file} file")


def get_title_basics(source_file: dict) -> pd.DataFrame:
    logging.info(f'Reading data from  {source_file.get("url_data", "")}')
    df = pd.read_csv(source_file.get("url_data", ""), sep="\t", compression="gzip")
    df = df[df.isAdult.isin([0, "0", "0.0", 0.0, 1, "1", "1.0", 1.0, "\\N"])]
    for col in df:
        if col in ("isAdult"):
            coldata_replace(df, col, {**REPLACE_BINARY_DICT, **REPLACE_DICT})
            convert_int(df, col, "Int64")
            continue
        elif col in ("startYear", "endYear", "runtimeMinutes"):
            convert_digit(df, col)
            convert_int(df, col, "Int64")
            continue
        elif col in ("genres"):
            coldata_replace(df, col, REPLACE_DICT)

    return df


def get_title_crew(source_file: dict) -> pd.DataFrame:
    logging.info(f'Reading data from  {source_file.get("url_data", "")}')
    df = pd.read_csv(source_file.get("url_data", ""), sep="\t", compression="gzip")
    for col in df:
        coldata_replace(df, col, REPLACE_DICT)
    return df


def get_title_episode(source_file: dict) -> pd.DataFrame:
    logging.info(f'Reading data from  {source_file.get("url_data", "")}')
    df = pd.read_csv(source_file.get("url_data", ""), sep="\t", compression="gzip")
    for col in df:
        if col in ("seasonNumber", "episodeNumber"):
            convert_digit(df, col)
            convert_int(df, col, "Int64")
    return df


def get_title_principals(
    source_file: dict,
    chunk_size: int,
    rename_mappings: dict,
    target_csv_file: pathlib.Path,
    headers: list,
) -> None:
    logging.info(f'Reading data from  {source_file.get("url_data", "")} in chunks')
    df_chunk = pd.read_csv(
        source_file.get("url_data", ""),
        sep="\t",
        compression="gzip",
        chunksize=chunk_size,
    )
    for idx, chunk in enumerate(df_chunk):
        logging.info(f"\t\tStarted cleaning chunk {idx}.")
        chunk_cleaned = chunk_clean_principals(chunk)
        if idx == 0:
            rename_headers(chunk_cleaned, rename_mappings)
            logging.info(f"csv headers are {headers}")
            logging.info(f"Writing data to {target_csv_file}.")
            chunk_cleaned.to_csv(str(target_csv_file), index=False, columns=headers)
        else:
            logging.info(f"Appending data to {target_csv_file}.")
            chunk_cleaned.to_csv(
                str(target_csv_file), index=False, mode="a", header=False
            )
        logging.info(f"{idx} chunk shape {chunk_cleaned.shape}")
    logging.info(f"Successfully created {target_csv_file} file")


def get_title_ratings(source_file: dict) -> pd.DataFrame:
    logging.info(f'Reading data from  {source_file.get("url_data", "")}')
    df = pd.read_csv(source_file.get("url_data", ""), sep="\t", compression="gzip")
    return df


def download_gzfile(source_url: str, source_file: str):
    logging.info(f"Downloading data from {source_url} to {source_file} .")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
    else:
        logging.info(f"Couldn't download {source_url}: {res.text}")
    logging.info(f"Downloaded data from {source_url} into {source_file}")


def download_blob(source_gcs_bucket: str, source_gcs_object: str, target_file: str):
    """Downloads a blob from the bucket."""
    logging.info(
        f"Downloading data from gs://{source_gcs_bucket}/{source_gcs_object} to {target_file} ..."
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(source_gcs_bucket)
    blob = bucket.blob(source_gcs_object)
    blob.download_to_filename(target_file)
    logging.info("Downloading Completed.")


def extract_tar(source_file: pathlib.Path, extract_here: pathlib.Path):
    logging.info(f"Extracting tar.gz file to -> {extract_here}.")
    if "tar.gz" in source_file:
        with tarfile.open(str(source_file), "r") as tar_fb:
            tar_fb.extractall(extract_here)
    logging.info(f"Successfully extracted tar file to -> {extract_here}.")


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
    logging.info("Started creating Dataframe for reviews(data).")
    df_reviews = pd.DataFrame(columns=REVIEW_COLS)
    for parent in TEST_TRAIN:
        for child in NEG_POS_UNSUP:
            if parent == "test" and child == "unsup":
                break
            path = f"{extract_here}/aclImdb/{parent}/{child}/"
            csv_files = list(glob.glob(path + "*.txt"))
            csv_files.sort()
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
    logging.info("Successfully Created Dataframe and assigned to variable df_reviews.")
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
    rename_headers(df_title_basics, {"tconst": "movie_id", "primaryTitle": "title"})
    logging.info(
        "Merging two Dataframes(df_reviews & df_title_basics) by using left-join and assigned to variable df"
    )
    df = pd.merge(df, df_title_basics, how="left")
    logging.info("Successfully created final Dataframe.")
    return df


def clean_html_tags(df: pd.DataFrame, review: str) -> None:
    logging.info("Started cleaning html tags from the user review.")
    df[review].replace(to_replace="<{1,}.{0,4}>", value="", regex=True, inplace=True)
    logging.info("Cleaning html tags completed.")


def replace_unicode(df: pd.DataFrame, col: str, match: str, replace: str) -> None:
    logging.info(
        f"Replacing unicode char in '{col}' replacing '{match}' with '{replace}'."
    )
    df[col] = df[col].apply(lambda data: data.replace(match, replace))


def coldata_replace(df: pd.DataFrame, col: str, replace_dict: dict) -> None:
    logging.info(f"Replacing '{col}' column data with {replace_dict}.")
    df[col].replace(replace_dict, inplace=True)
    logging.info(f"Successfully replaced '{col}' column data.")


def convert_int(df: pd.DataFrame, col: str, dtype: str) -> None:
    logging.info(f"Converting data type to {dtype}")
    df[col] = df[col].astype(dtype)


def convert_digit(df: pd.DataFrame, col: str) -> None:
    logging.info(f"Converting '{col}' data from string(value) to integer(value).")
    df[col] = df[col].apply(lambda data: int(data) if str(data).isdigit() else np.nan)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Renaming headers")
    logging.info(f"\t {list(df.columns)} with {rename_mappings}")
    df.rename(columns=rename_mappings, inplace=True)
    logging.info("Renaming headers completed.")


def convert_str(chunk: pd.DataFrame, col: str, data_type: str) -> pd.DataFrame:
    logging.info(f"Converting datatype of '{col}' column to {data_type}.")
    chunk[col] = chunk[col].apply(data_type)
    return chunk


def clean_data(chunk: pd.DataFrame, col: str, match: str, replace: str) -> None:
    logging.info(
        f"Replacing unicode char in '{col}' replacing '{match}' with '{replace}'."
    )
    chunk[col] = chunk[col].apply(
        lambda x: x if pd.isnull(x) else x.replace(match, replace)
    )


def chunk_clean_akas(chunk: pd.DataFrame) -> pd.DataFrame:
    for col in chunk:
        if col in ("title", "region", "language"):
            coldata_replace(chunk, col, {"\\N": None})
        if col in ("types", "attributes"):
            replace_unicode(chunk, col, "\x02", "&")
            coldata_replace(chunk, col, {"\\N": None})
        if col in ("isOriginalTitle"):
            coldata_replace(
                chunk, col, {"0": False, "1": True, "\\N": None, 0: False, 1: True}
            )
        if col in ("title"):
            clean_data(chunk, col, "\n", "|")
    logging.info(f"Dataframe chunk shape {chunk.shape}")
    return chunk


def chunk_clean_principals(chunk: pd.DataFrame) -> pd.DataFrame:
    for col in chunk:
        if col in ("characters"):
            replace_unicode(chunk, col, "[", "")
            replace_unicode(chunk, col, "]", "")
            replace_unicode(chunk, col, '"', "")
            coldata_replace(chunk, col, {"\\N": None})
        elif col in ("job"):
            coldata_replace(chunk, col, {"\\N": None})
    logging.info(f"Dataframe chunk shape {chunk.shape}")
    return chunk


def save_to_newfile(
    df: pd.DataFrame, target_csv_file: pathlib.Path, headers: typing.List[str]
) -> None:
    logging.info(f"Saving to output file to ... {target_csv_file}")
    df.to_csv(str(target_csv_file), header=True, index=False, columns=headers)
    logging.info("Successfully saved.")


def upload_file_to_gcs(
    target_csv_file: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_csv_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_gcs_bucket=os.environ.get("SOURCE_GCS_BUCKET", ""),
        source_gcs_object=os.environ.get("SOURCE_GCS_OBJECT", ""),
        source_url=json.loads(os.environ.get("SOURCE_URL")),
        source_file=json.loads(os.environ.get("SOURCE_FILE")),
        extract_here=pathlib.Path(os.environ.get("EXTRACT_HERE", "")).expanduser(),
        target_csv_file=pathlib.Path(os.environ.get("TARGET_CSV_FILE")).expanduser(),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET"),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH"),
        headers=json.loads(os.environ.get("CSV_HEADERS")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS")),
        pipeline_name=os.environ.get("PIPELINE_NAME", ""),
        table_name=os.environ.get("TABLE_NAME", ""),
        chunk_size=int(os.environ.get("CHUNK_SIZE", "1000000")),
    )
