# Copyright 2022 Google LLC
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
import json
import logging
import os
import pathlib
import typing

import pandas as pd
from google.cloud import storage


def main(
    source_gcs_bucket: str,
    source_gcs_object: str,
    source_file: pathlib.Path,
    columns: typing.List[str],
    target_csv_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    logging.info(
        "Multilingual Spoken Words Corpus - MLCommons Association Dataset process started "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info("Creating './files/' folder.")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_blob(source_gcs_bucket, source_gcs_object, source_file)
    logging.info("Reading json file")
    meta_data = json.load(open(source_file))
    logging.info("Getting all existed languages")
    lang_abbr = get_lang_abbr(meta_data)
    logging.info("Creating empty dataframe")
    df = pd.DataFrame(columns=columns)
    write_to_file(df, target_csv_file, "w")
    logging.info("Creating dataframe ")
    create_dataframe(lang_abbr, meta_data, columns, target_csv_file)
    upload_file_to_gcs(target_csv_file, target_gcs_bucket, target_gcs_path)
    logging.info(
        "Multilingual Spoken Words Corpus - MLCommons Association Dataset process completed "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def download_blob(
    source_gcs_bucket: str, source_gcs_object: str, target_file: pathlib.Path
) -> None:
    """Downloads a blob from the bucket."""
    logging.info(
        f"Downloading data from gs://{source_gcs_bucket}/{source_gcs_object} to {target_file} ..."
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(source_gcs_bucket)
    blob = bucket.blob(source_gcs_object)
    blob.download_to_filename(str(target_file))
    logging.info("Downloading Completed.")


def create_dataframe(
    lang_abbr: str,
    meta_data: dict,
    columns: typing.List[str],
    target_csv_file: pathlib.Path,
) -> None:
    for idx, kv_pair in enumerate(lang_abbr.items()):
        abbr, language = kv_pair
        logging.info(f"\t\t\t{idx + 1} out of {len(lang_abbr)} languages.")
        logging.info(
            f"Process started for creating dataframe for {abbr} - {language} language."
        )
        num_of_words = get_num_of_words(meta_data, abbr)
        logging.info(f"\tCreating temporary datafame for all {num_of_words} words\n")
        temp_dataframe(
            meta_data, abbr, columns, num_of_words, language, target_csv_file
        )


def temp_dataframe(
    meta_data: dict,
    abbr: str,
    columns: typing.List[str],
    num_of_words: int,
    language: str,
    target_csv_file: pathlib.Path,
) -> None:
    for word, count in get_lang_words_count(meta_data, abbr).items():
        temp = pd.DataFrame(columns=columns)
        lang_word_filenames = get_lang_word_filenames(meta_data, abbr, word)
        temp["filenames"] = lang_word_filenames
        temp["lang_abbr"] = [abbr] * count
        temp["word"] = [word] * count
        temp["word_count"] = [count] * count
        temp["number_of_words"] = [num_of_words] * count
        temp["language"] = [language] * count
        write_to_file(temp, str(target_csv_file), mode="a")


def get_lang_abbr(meta_data: dict, key: str = "language") -> dict:
    lang_abbr = {}
    for abbr in meta_data.keys():
        if isinstance(meta_data[abbr], dict):
            lang_abbr[abbr] = meta_data[abbr].get(key, {})
    return lang_abbr


def get_num_of_words(meta_data: dict, abbr: str, key: str = "number_of_words") -> int:
    return meta_data[abbr].get(key, 0)


def get_lang_words_count(meta_data: dict, abbr: str, key: str = "wordcounts") -> int:
    return meta_data[abbr].get(key, 0)


def get_lang_word_filenames(
    meta_data: dict, abbr: str, word: str, key: str = "filenames"
) -> typing.List[str]:
    return meta_data[abbr][key].get(word, [])


def write_to_file(
    df: pd.DataFrame, target_csv_file: pathlib.Path, mode: str = "w"
) -> None:
    if mode == "w":
        logging.info("Writing data to csv...")
        df.to_csv(str(target_csv_file), index=False)
    else:
        df.to_csv(str(target_csv_file), mode=mode, index=False, header=False)


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
        source_file=pathlib.Path(os.environ.get("SOURCE_FILE", "")).expanduser(),
        columns=json.loads(os.environ.get("COLUMNS", "[]")),
        target_csv_file=pathlib.Path(
            os.environ.get("TARGET_CSV_FILE", "")
        ).expanduser(),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
    )
