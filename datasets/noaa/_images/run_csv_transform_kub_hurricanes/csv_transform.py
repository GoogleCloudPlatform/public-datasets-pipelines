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

import numpy as np
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    source_file: pathlib.Path,
    target_file: pathlib.Path,
    chunksize: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:

    # source_url            STRING          -> The full url of the source file to transform
    # source_file           PATHLIB.PATH    -> The (local) path pertaining to the downloaded source file
    # target_file           PATHLIB.PATH    -> The (local) target transformed file + filename
    # chunksize             INT (STRING)    -> The number of records to import per each batch, reduces memory consumption
    # target_gcs_bucket     STRING          -> The target GCS bucket to place the output (transformed) file
    # target_gcs_path       STRING          -> The target GCS path ( within the GCS bucket ) to place the output (transformed) file

    logging.info("NOAA - Hurricanes process started")

    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)
    download_file(source_url, source_file)

    names = [
        "sid",
        "season",
        "number",
        "basin",
        "subbasin",
        "name",
        "iso_time",
        "nature",
        "lat",
        "lon",
        "wmo_wind",
        "wmo_pres",
        "wmo_agency",
        "track_type",
        "dist2land",
        "landfall",
        "iflag",
        "usa_agency",
        "usa_atcf_id",
        "usa_lat",
        "usa_lon",
        "usa_record",
        "usa_status",
        "usa_wind",
        "usa_pres",
        "usa_sshs",
        "usa_r34_ne",
        "usa_r34_se",
        "usa_r34_sw",
        "usa_r34_nw",
        "usa_r50_ne",
        "usa_r50_se",
        "usa_r50_sw",
        "usa_r50_nw",
        "usa_r64_ne",
        "usa_r64_se",
        "usa_r64_sw",
        "usa_r64_nw",
        "usa_poci",
        "usa_roci",
        "usa_rmw",
        "usa_eye",
        "tokyo_lat",
        "tokyo_lon",
        "tokyo_grade",
        "tokyo_wind",
        "tokyo_pres",
        "tokyo_r50_dir",
        "tokyo_r50_long",
        "tokyo_r50_short",
        "tokyo_r30_dir",
        "tokyo_r30_long",
        "tokyo_r30_short",
        "tokyo_land",
        "cma_lat",
        "cma_lon",
        "cma_cat",
        "cma_wind",
        "cma_pres",
        "hko_lat",
        "hko_lon",
        "hko_cat",
        "hko_wind",
        "hko_pres",
        "newdelhi_lat",
        "newdelhi_lon",
        "newdelhi_grade",
        "newdelhi_wind",
        "newdelhi_pres",
        "newdelhi_ci",
        "newdelhi_dp",
        "newdelhi_poci",
        "reunion_lat",
        "reunion_lon",
        "reunion_type",
        "reunion_wind",
        "reunion_pres",
        "reunion_tnum",
        "reunion_ci",
        "reunion_rmw",
        "reunion_r34_ne",
        "reunion_r34_se",
        "reunion_r34_sw",
        "reunion_r34_nw",
        "reunion_r50_ne",
        "reunion_r50_se",
        "reunion_r50_sw",
        "reunion_r50_nw",
        "reunion_r64_ne",
        "reunion_r64_se",
        "reunion_r64_sw",
        "reunion_r64_nw",
        "bom_lat",
        "bom_lon",
        "bom_type",
        "bom_wind",
        "bom_pres",
        "bom_tnum",
        "bom_ci",
        "bom_rmw",
        "bom_r34_ne",
        "bom_r34_se",
        "bom_r34_sw",
        "bom_r34_nw",
        "bom_r50_ne",
        "bom_r50_se",
        "bom_r50_sw",
        "bom_r50_nw",
        "bom_r64_ne",
        "bom_r64_se",
        "bom_r64_sw",
        "bom_r64_nw",
        "bom_roci",
        "bom_poci",
        "bom_eye",
        "bom_pos_method",
        "bom_pres_method",
        "nadi_lat",
        "nadi_lon",
        "nadi_cat",
        "nadi_wind",
        "nadi_pres",
        "wellington_lat",
        "wellington_lon",
        "wellington_wind",
        "wellington_pres",
        "ds824_lat",
        "ds824_lon",
        "ds824_stage",
        "ds824_wind",
        "ds824_pres",
        "td9636_lat",
        "td9636_lon",
        "td9636_stage",
        "td9636_wind",
        "td9636_pres",
        "td9635_lat",
        "td9635_lon",
        "td9635_wind",
        "td9635_pres",
        "td9635_roci",
        "neumann_lat",
        "neumann_lon",
        "neumann_class",
        "neumann_wind",
        "neumann_pres",
        "mlc_lat",
        "mlc_lon",
        "mlc_class",
        "mlc_wind",
        "mlc_pres",
        "usa_gust",
        "bom_gust",
        "bom_gust_per",
        "reunion_gust",
        "reunion_gust_per",
        "usa_seahgt",
        "usa_searad_ne",
        "usa_searad_se",
        "usa_searad_sw",
        "usa_searad_nw",
        "storm_speed",
        "storm_dir",
    ]

    dtypes = {"textdata": np.str_}

    chunksz = int(chunksize)

    logging.info(f"Opening batch file {source_file}")
    with pd.read_csv(
        source_file,  # path to main source file to load in batches
        engine="python",
        encoding="utf-8",
        quotechar='"',  # string separator, typically double-quotes
        chunksize=chunksz,  # size of batch data, in no. of records
        sep=",",  # data column separator, typically ","
        skiprows=2,  # skip the informational text
        header=None,  # use when the data file does not contain a header
        names=names,
        dtype=dtypes,
    ) as reader:
        for chunk_number, chunk in enumerate(reader):
            target_file_batch = str(target_file).replace(
                ".csv", "-" + str(chunk_number) + ".csv"
            )
            df = pd.DataFrame()
            df = pd.concat([df, chunk])
            process_chunk(df, target_file_batch, target_file, (not chunk_number == 0))

    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info("NOAA - Hurricanes process completed")


def process_chunk(
    df: pd.DataFrame, target_file_batch: str, target_file: str, skip_header: bool
) -> None:
    df = rename_headers(df)
    df = reorder_headers(df)
    save_to_new_file(df, file_path=str(target_file_batch))
    append_batch_file(target_file_batch, target_file, skip_header, not (skip_header))


def append_batch_file(
    batch_file_path: str, target_file_path: str, skip_header: bool, truncate_file: bool
) -> None:
    data_file = open(batch_file_path, "r")
    if truncate_file:
        target_file = open(target_file_path, "w+").close()
    target_file = open(target_file_path, "a+")
    if skip_header:
        logging.info(
            f"Appending batch file {batch_file_path} to {target_file_path} with skip header"
        )
        next(data_file)
    else:
        logging.info(f"Appending batch file {batch_file_path} to {target_file_path}")
    target_file.write(data_file.read())
    data_file.close()
    target_file.close()
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)


def reorder_headers(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Reordering headers..")
    df = df[
        [
            "sid",
            "season",
            "number",
            "basin",
            "subbasin",
            "name",
            "iso_time",
            "nature",
            "latitude",
            "longitude",
            "wmo_wind",
            "wmo_pressure",
            "wmo_agency",
            "track_type",
            "dist2land",
            "landfall",
            "iflag",
            "usa_agency",
            "usa_latitude",
            "usa_longitude",
            "usa_record",
            "usa_status",
            "usa_wind",
            "usa_pressure",
            "usa_sshs",
            "usa_r34_ne",
            "usa_r34_se",
            "usa_r34_sw",
            "usa_r34_nw",
            "usa_r50_ne",
            "usa_r50_se",
            "usa_r50_sw",
            "usa_r50_nw",
            "usa_r64_ne",
            "usa_r64_se",
            "usa_r64_sw",
            "usa_r64_nw",
            "usa_poci",
            "usa_roci",
            "usa_rmw",
            "usa_eye",
            "tokyo_latitude",
            "tokyo_longitude",
            "tokyo_grade",
            "tokyo_wind",
            "tokyo_pressure",
            "tokyo_r50_dir",
            "tokyo_r50_longitude",
            "tokyo_r50_short",
            "tokyo_r30_dir",
            "tokyo_r30_long",
            "tokyo_r30_short",
            "tokyo_land",
            "cma_latitude",
            "cma_longitude",
            "cma_cat",
            "cma_wind",
            "cma_pressure",
            "hko_latitude",
            "hko_longitude",
            "hko_cat",
            "hko_wind",
            "hko_pressure",
            "newdelhi_latitude",
            "newdelhi_longitude",
            "newdelhi_grade",
            "newdelhi_wind",
            "newdelhi_pressure",
            "newdelhi_ci",
            "newdelhi_dp",
            "newdelhi_poci",
            "reunion_latitude",
            "reunion_longitude",
            "reunion_type",
            "reunion_wind",
            "reunion_pressure",
            "reunion_tnum",
            "reunion_ci",
            "reunion_rmw",
            "reunion_r34_ne",
            "reunion_r34_se",
            "reunion_r34_sw",
            "reunion_r34_nw",
            "reunion_r50_ne",
            "reunion_r50_se",
            "reunion_r50_sw",
            "reunion_r50_nw",
            "reunion_r64_ne",
            "reunion_r64_se",
            "reunion_r64_sw",
            "reunion_r64_nw",
            "bom_latitude",
            "bom_longitude",
            "bom_type",
            "bom_wind",
            "bom_pressure",
            "bom_tnum",
            "bom_ci",
            "bom_rmw",
            "bom_r34_ne",
            "bom_r34_se",
            "bom_r34_sw",
            "bom_r34_nw",
            "bom_r50_ne",
            "bom_r50_se",
            "bom_r50_sw",
            "bom_r50_nw",
            "bom_r64_ne",
            "bom_r64_se",
            "bom_r64_sw",
            "bom_r64_nw",
            "bom_roci",
            "bom_poci",
            "bom_eye",
            "bom_pos_method",
            "bom_pressure_method",
            "wellington_latitude",
            "wellington_longitude",
            "wellington_wind",
            "wellington_pressure",
            "nadi_latitude",
            "nadi_longitude",
            "nadi_cat",
            "nadi_wind",
            "nadi_pressure",
            "ds824_latitude",
            "ds824_longitude",
            "ds824_stage",
            "ds824_wind",
            "ds824_pressure",
            "td9636_latitude",
            "td9636_longitude",
            "td9636_stage",
            "td9636_wind",
            "td9636_pressure",
            "td9635_latitude",
            "td9635_longitude",
            "td9635_wind",
            "td9635_pressure",
            "td9635_roci",
            "neumann_latitude",
            "neumann_longitude",
            "neumann_class",
            "neumann_wind",
            "neumann_pressure",
            "mlc_latitude",
            "mlc_longitude",
            "mlc_class",
            "mlc_wind",
            "mlc_pressure",
            "usa_atcf_id",
        ]
    ]

    return df


def rename_headers(df: pd.DataFrame) -> None:
    header_names = {
        "lat": "latitude",
        "lon": "longitude",
        "wmo_pres": "wmo_pressure",
        "usa_lat": "usa_latitude",
        "usa_lon": "usa_longitude",
        "usa_pres": "usa_pressure",
        "tokyo_lat": "tokyo_latitude",
        "tokyo_lon": "tokyo_longitude",
        "tokyo_pres": "tokyo_pressure",
        "tokyo_r50_long": "tokyo_r50_longitude",
        "cma_lat": "cma_latitude",
        "cma_lon": "cma_longitude",
        "cma_pres": "cma_pressure",
        "hko_lat": "hko_latitude",
        "hko_lon": "hko_longitude",
        "hko_pres": "hko_pressure",
        "newdelhi_lat": "newdelhi_latitude",
        "newdelhi_lon": "newdelhi_longitude",
        "newdelhi_pres": "newdelhi_pressure",
        "reunion_lat": "reunion_latitude",
        "reunion_lon": "reunion_longitude",
        "reunion_pres": "reunion_pressure",
        "bom_lat": "bom_latitude",
        "bom_lon": "bom_longitude",
        "bom_pres": "bom_pressure",
        "bom_pres_method": "bom_pressure_method",
        "wellington_lat": "wellington_latitude",
        "wellington_lon": "wellington_longitude",
        "wellington_pres": "wellington_pressure",
        "nadi_lat": "nadi_latitude",
        "nadi_lon": "nadi_longitude",
        "nadi_pres": "nadi_pressure",
        "ds824_lat": "ds824_latitude",
        "ds824_lon": "ds824_longitude",
        "ds824_pres": "ds824_pressure",
        "td9636_lat": "td9636_latitude",
        "td9636_lon": "td9636_longitude",
        "td9636_pres": "td9636_pressure",
        "td9635_lat": "td9635_latitude",
        "td9635_lon": "td9635_longitude",
        "td9635_pres": "td9635_pressure",
        "neumann_lat": "neumann_latitude",
        "neumann_lon": "neumann_longitude",
        "neumann_pres": "neumann_pressure",
        "mlc_lat": "mlc_latitude",
        "mlc_lon": "mlc_longitude",
        "mlc_pres": "mlc_pressure",
    }

    df.columns = df.columns.str.lower()
    df.rename(columns=header_names, inplace=True)

    return df


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def download_file(source_url: str, source_file: pathlib.Path) -> None:
    r = requests.get(source_url, stream=True)
    with open(source_file, "wb") as f:
        for chunk in r:
            f.write(chunk)


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
        chunksize=os.environ["CHUNKSIZE"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
    )
