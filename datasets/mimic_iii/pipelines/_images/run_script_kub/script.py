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
import operator
import os
import time

from google.api_core.exceptions import ResourceExhausted
from google.cloud import bigquery_datatransfer_v1
from google.protobuf.timestamp_pb2 import Timestamp

RETRY_DELAY = 10


class TimeoutError(Exception):
    """Raised when the BQ transfer jobs haven't all finished within the allotted time"""

    pass


def main(
    source_project_id: str,
    source_bq_dataset: str,
    target_project_id: str,
    target_bq_dataset: str,
    timeout: int,
):
    client = bigquery_datatransfer_v1.DataTransferServiceClient()
    transfer_config_name = f"{source_project_id}-{source_bq_dataset}-copy"
    existing_config = find_existing_config(
        client, target_project_id, transfer_config_name
    )
    if not existing_config:
        existing_config = create_transfer_config(
            client,
            source_project_id,
            source_bq_dataset,
            target_project_id,
            target_bq_dataset,
            transfer_config_name,
        )
    trigger_config(client, existing_config)
    wait_for_completion(client, existing_config, timeout)


def find_existing_config(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    gcp_project: str,
    transfer_config_name: str,
) -> bigquery_datatransfer_v1.types.TransferConfig:
    all_transfer_configs = client.list_transfer_configs(
        request=bigquery_datatransfer_v1.types.ListTransferConfigsRequest(
            parent=f"projects/{gcp_project}"
        )
    )
    return next(
        (
            config
            for config in all_transfer_configs
            if config.display_name == transfer_config_name
        ),
        None,
    )


def wait_for_completion(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    running_config: bigquery_datatransfer_v1.types.TransferConfig,
    timeout: int,
) -> None:
    _start = int(time.time())
    while True:
        latest_runs = []
        latest_runs.append(latest_transfer_run(client, running_config))
        logging.info(f"States: {[str(run.state) for run in latest_runs]}")
        # Mark as complete when all runs have succeeded
        if all([str(run.state) == "TransferState.SUCCEEDED" for run in latest_runs]):
            return
        # Stop the process when it's longer than the allotted time
        if int(time.time()) - _start > timeout:
            raise TimeoutError
        time.sleep(RETRY_DELAY)


def latest_transfer_run(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    config: bigquery_datatransfer_v1.types.TransferConfig,
) -> bigquery_datatransfer_v1.types.TransferRun:
    transfer_runs = client.list_transfer_runs(parent=config.name)
    return max(transfer_runs, key=operator.attrgetter("run_time"))


def create_transfer_config(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    source_project_id: str,
    source_dataset_id: str,
    target_project_id: str,
    target_dataset_id: str,
    display_name: str,
) -> bigquery_datatransfer_v1.types.TransferConfig:
    transfer_config = bigquery_datatransfer_v1.TransferConfig(
        destination_dataset_id=target_dataset_id,
        display_name=display_name,
        data_source_id="cross_region_copy",
        dataset_region="US",
        params={
            "overwrite_destination_table": True,
            "source_project_id": source_project_id,
            "source_dataset_id": source_dataset_id,
        },
        schedule_options=bigquery_datatransfer_v1.ScheduleOptions(
            disable_auto_scheduling=True
        ),
    )
    request = bigquery_datatransfer_v1.types.CreateTransferConfigRequest(
        parent=client.common_project_path(target_project_id),
        transfer_config=transfer_config,
    )
    return client.create_transfer_config(request=request)


def trigger_config(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    config: bigquery_datatransfer_v1.types.TransferConfig,
) -> None:
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * pow(10, 9))
    try:
        client.start_manual_transfer_runs(
            request=bigquery_datatransfer_v1.types.StartManualTransferRunsRequest(
                parent=config.name,
                requested_run_time=Timestamp(seconds=seconds, nanos=nanos),
            )
        )
    except ResourceExhausted:
        logging.info(
            f"Transfer job is currently running for config ({config.display_name}) {config.name}."
        )
        return


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_project_id=os.environ["SOURCE_PROJECT_ID"],
        source_bq_dataset=os.environ["SOURCE_BQ_DATASET"],
        target_project_id=os.environ["TARGET_PROJECT_ID"],
        target_bq_dataset=os.environ["TARGET_BQ_DATASET"],
        timeout=int(os.getenv("TIMEOUT", 1200)),
    )
