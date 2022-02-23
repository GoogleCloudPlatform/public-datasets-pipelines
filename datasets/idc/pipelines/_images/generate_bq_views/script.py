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

import json
import logging
import os
import pathlib
import typing

from google.cloud import bigquery


def main(
    queries_dir: pathlib.Path,
    gcp_project: str,
    dataset_name: str,
    dataset_versions: typing.List[str],
    current_version: str,
):
    client = bigquery.Client()
    for version in dataset_versions:
        sql_files = [f for f in (queries_dir / version).iterdir() if f.suffix == ".sql"]
        for sql_file in sql_files:
            query = load_query(
                sql_file=sql_file,
                gcp_project=gcp_project,
                dataset=f"{dataset_name}_{version}",
                current_version=current_version,
            )

            client.query(query)


def load_query(
    sql_file: pathlib.Path, gcp_project: str, dataset: str, current_version: str
) -> str:
    query = sql_file.read_text()

    # Replace template variables
    query = query.replace("PROJECT", gcp_project)
    query = query.replace("DATASET", dataset)
    query = query.replace("CURRENT_VERSION", current_version)
    query = f"""
        CREATE OR REPLACE VIEW
            `{gcp_project}.{dataset}.{sql_file.stem}`
        AS (
            {query}
        )
    """

    return query


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        queries_dir=pathlib.Path(os.environ["QUERIES_DIR"]).expanduser(),
        gcp_project=os.environ["GCP_PROJECT"],
        dataset_name=os.environ["DATASET_NAME"],
        dataset_versions=json.loads(os.environ["DATASET_VERSIONS"]),
        current_version=os.environ["CURRENT_VERSION"],
    )
