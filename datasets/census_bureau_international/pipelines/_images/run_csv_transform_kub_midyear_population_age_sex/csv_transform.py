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

import pandas as pd
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    logging.info(
        "International Database (Country Names - Midyear Population, by Age and Sex) Delivery process started"
    )

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    df_pop = obtain_source_data(
        source_url, source_file, ["country_code", "year"], "_pop_data.csv", 0, ","
    )
    df_country = obtain_source_data(
        source_url, source_file, ["country_code"], "_country_data.csv", 1, ","
    )

    df = pd.merge(
        df_pop,
        df_country,
        left_on="country_code",
        right_on="country_code",
        how="left",
    )

    df = resolve_sex(df)
    df = reorder_headers(df)

    save_to_new_file(df, target_file, ",")
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        "International Database (Country Names - Midyear Population, by Age and Sex) Delivery process completed"
    )


def resolve_sex(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Resolving gender data point")
    df = df.replace(to_replace={"sex": {2: "Male", 3: "Female"}})

    return df


def obtain_source_data(
    source_url: str,
    source_file: str,
    key_list: list,
    file_suffix: str,
    path_ordinal: int,
    separator: str = ",",
) -> pd.DataFrame:
    source_data_filepath = str(source_file).replace(".csv", file_suffix)
    download_file_gs(
        source_url.split(",")[path_ordinal].replace('"', "").strip(),
        source_data_filepath,
    )
    df = pd.read_csv(
        source_data_filepath,
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        sep=",",  # data column separator, typically ","
    )
    df = add_key(df, key_list)
    df.drop_duplicates(subset=["key"], keep="last", inplace=True, ignore_index=False)

    return df


def download_file_gs(source_url: str, source_file: pathlib.Path) -> None:
    logging.info(f"Downloading {source_url} to {source_file}")
    with open(source_file, "wb+") as file_obj:
        storage.Client().download_blob_to_file(source_url, file_obj)


def add_key(df: pd.DataFrame, key_list: list) -> pd.DataFrame:
    logging.info(f"Adding key column(s) {key_list}")
    df["key"] = ""
    for key in key_list:
        df["key"] = df.apply(
            lambda x: str(x[key])
            if not str(x["key"])
            else str(x["key"]) + "-" + str(x[key]),
            axis=1,
        )
    df["key_val"] = df["key"]

    return df


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[
        [
            "country_code",
            "country_name",
            "year",
            "sex",
            "max_age",
            "population_age_0",
            "population_age_1",
            "population_age_2",
            "population_age_3",
            "population_age_4",
            "population_age_5",
            "population_age_6",
            "population_age_7",
            "population_age_8",
            "population_age_9",
            "population_age_10",
            "population_age_11",
            "population_age_12",
            "population_age_13",
            "population_age_14",
            "population_age_15",
            "population_age_16",
            "population_age_17",
            "population_age_18",
            "population_age_19",
            "population_age_20",
            "population_age_21",
            "population_age_22",
            "population_age_23",
            "population_age_24",
            "population_age_25",
            "population_age_26",
            "population_age_27",
            "population_age_28",
            "population_age_29",
            "population_age_30",
            "population_age_31",
            "population_age_32",
            "population_age_33",
            "population_age_34",
            "population_age_35",
            "population_age_36",
            "population_age_37",
            "population_age_38",
            "population_age_39",
            "population_age_40",
            "population_age_41",
            "population_age_42",
            "population_age_43",
            "population_age_44",
            "population_age_45",
            "population_age_46",
            "population_age_47",
            "population_age_48",
            "population_age_49",
            "population_age_50",
            "population_age_51",
            "population_age_52",
            "population_age_53",
            "population_age_54",
            "population_age_55",
            "population_age_56",
            "population_age_57",
            "population_age_58",
            "population_age_59",
            "population_age_60",
            "population_age_61",
            "population_age_62",
            "population_age_63",
            "population_age_64",
            "population_age_65",
            "population_age_66",
            "population_age_67",
            "population_age_68",
            "population_age_69",
            "population_age_70",
            "population_age_71",
            "population_age_72",
            "population_age_73",
            "population_age_74",
            "population_age_75",
            "population_age_76",
            "population_age_77",
            "population_age_78",
            "population_age_79",
            "population_age_80",
            "population_age_81",
            "population_age_82",
            "population_age_83",
            "population_age_84",
            "population_age_85",
            "population_age_86",
            "population_age_87",
            "population_age_88",
            "population_age_89",
            "population_age_90",
            "population_age_91",
            "population_age_92",
            "population_age_93",
            "population_age_94",
            "population_age_95",
            "population_age_96",
            "population_age_97",
            "population_age_98",
            "population_age_99",
            "population_age_100",
        ]
    ]

    return df


def save_to_new_file(df, file_path, sep="|") -> None:
    logging.info(f"Saving to file {file_path} separator='{sep}'")
    df.to_csv(file_path, sep=sep, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    logging.info(f"Uploading to GCS {gcs_bucket} in {gcs_path}")
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
