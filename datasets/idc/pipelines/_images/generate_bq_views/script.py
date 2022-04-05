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
import typing

import google.api_core
import google.auth
import google.auth.impersonated_credentials
from google.cloud import bigquery

BQ_OAUTH_SCOPE = "https://www.googleapis.com/auth/bigquery"


def main(
    source_project: str,
    target_project: str,
    bq_datasets: typing.List[str],
    service_account: str,
):
    default_creds, pid = google.auth.default()
    print(f"Obtained default credentials for the project {pid}")
    credentials = google.auth.impersonated_credentials.Credentials(
        source_credentials=default_creds,
        target_principal=service_account,
        target_scopes=[BQ_OAUTH_SCOPE],
    )

    client = bigquery.Client(credentials=credentials)
    for dataset in bq_datasets:
        logging.info(f"Generating views for {dataset}..")
        tables = client.list_tables(f"{source_project}.{dataset}")

        source_views = []
        for table in tables:
            if table.table_type == "TABLE":
                continue
            source_view = client.get_table(
                f"{source_project}.{dataset}.{table.table_id}"
            )
            create_or_update_view(client, source_view, source_project, target_project)
            source_views.append(table.table_id)

        sync_views(client, dataset, source_views, target_project)


def create_or_update_view(
    client: bigquery.Client,
    source_view: bigquery.Table,
    source_project: str,
    target_project: str,
) -> None:
    try:
        target_view = client.get_table(
            f"{target_project}.{source_view.dataset_id}.{source_view.table_id}"
        )
    except google.api_core.exceptions.NotFound:
        target_view = None

    _view = bigquery.Table(
        f"{target_project}.{source_view.dataset_id}.{source_view.table_id}"
    )
    _view.description = source_view.description
    _view.view_query = source_view.view_query.replace(source_project, target_project)

    # Create the view if it doesn't exist. Otherwise, update it.
    if not target_view:
        view = client.create_table(_view)
        logging.info(f"View {view.full_table_id} successfully created.")
    else:
        view = client.update_table(_view, ["view_query", "description"])
        logging.info(f"View {view.full_table_id} successfully updated.")


def sync_views(
    client: bigquery.Client,
    dataset: str,
    source_views: typing.List[str],
    target_project: str,
) -> None:
    """Syncs views between source and target BQ datasets.

    If a view exists in the target dataset but not in the source dataset, that
    view must be deleted from the target dataset.
    """
    target_tables = client.list_tables(f"{target_project}.{dataset}")
    for target_table in target_tables:
        if not target_table.table_type == "VIEW":
            continue
        if target_table.table_id not in source_views:
            logging.info(
                f"Extra view {target_project}.{dataset}.{target_table.table_id} will be deleted."
            )
            client.delete_table(
                f"{target_project}.{dataset}.{target_table.table_id}", not_found_ok=True
            )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_project=os.environ["SOURCE_PROJECT_ID"],
        target_project=os.environ["TARGET_PROJECT_ID"],
        bq_datasets=json.loads(os.environ["BQ_DATASETS"]),
        service_account=os.environ["SERVICE_ACCOUNT"],
    )
