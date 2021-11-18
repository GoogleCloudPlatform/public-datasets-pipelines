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
from datetime import datetime

from google.cloud import bigquery_datatransfer_v1

# from airflow.contrib.operators.gcs_to_gcs import (
#     GoogleCloudStorageToGoogleCloudStorageOperator,
# )


def main(
    source_project_id: str,
    source_dataset_list: list,
    target_project_id: str,
    user_id: str,
) -> None:

    logging.info("IDC data migration process started")

    transfer_bq_data(
        source_project_id,
        source_dataset_list,
        target_project_id,
        user_id,
        copy_display_name="copy executing...",
    )

    logging.info("IDC data migration process completed")


def transfer_bq_data(
    source_project_id: str,
    source_dataset_list: list,
    target_project_id: str,
    user_id: str,
):
    # transfer_config = ""
    logging.info(
        f"Creating transfer config for {source_project_id}.[{source_dataset_list}] -> {target_project_id}"
    )
    client = bigquery_datatransfer_v1.DataTransferServiceClient()
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    DATASETS = source_dataset_list

    for dataset in DATASETS:
        transfer_config = bigquery_datatransfer_v1.TransferConfig(
            destination_dataset_id=dataset,
            display_name=f"transfer-{dataset}-{timestamp}",
            data_source_id="cross_region_copy",
            dataset_region="US",
            schedule="0 0 1 * *",  # First day of month
            params={
                "source_project_id": source_project_id,
                "source_dataset_id": dataset,
                "overwrite_destination_table": "true",
            },
        )

        request = bigquery_datatransfer_v1.types.CreateTransferConfigRequest(
            parent=client.common_project_path("bigquery-public-data-dev"),
            transfer_config=transfer_config,
            service_account_name=user_id,
        )

        client.create_transfer_config(
            request=request,
        )

        logging.info(f"Created transfer config {transfer_config.name}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_project_id=os.environ["SOURCE_PROJECT_ID"],
        source_dataset_list=json.loads(os.environ["SOURCE_DATASET_LIST"]),
        target_project_id=os.environ["TARGET_PROJECT_ID"],
        user_id=os.environ["USER_ID"],
    )
