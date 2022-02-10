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
import operator
import os
import time
import typing

from google.api_core.exceptions import ResourceExhausted
from google.cloud import bigquery_datatransfer_v1
from google.protobuf.timestamp_pb2 import Timestamp

RETRY_DELAY = 10


class TimeoutError(Exception):
    """Raised when the BQ transfer jobs haven't all finished within the allotted time"""

    pass


def main(
    source_project_id: str,
    target_project_id: str,
    service_account: str,
    dataset_name: str,
    dataset_versions: typing.List[str],
    timeout: int,
):
    client = bigquery_datatransfer_v1.DataTransferServiceClient()
    transfer_config_prefix = f"{dataset_name}-copy"
    transfer_configs = client.list_transfer_configs(
        request=bigquery_datatransfer_v1.types.ListTransferConfigsRequest(
            parent=f"projects/{target_project_id}"
        )
    )

    existing_configs = [
        config
        for config in transfer_configs
        if config.display_name.startswith(transfer_config_prefix)
    ]

    _running_configs = []
    for version in dataset_versions:
        dataset_id = f"{dataset_name}_{version}"
        display_name = f"{transfer_config_prefix}-{version}"

        _config = next(
            (
                config
                for config in existing_configs
                if config.display_name == display_name
            ),
            None,
        )
        if not _config:
            _config = create_transfer_config(
                client,
                source_project_id,
                target_project_id,
                dataset_id,
                display_name,
                service_account,
            )

        trigger_config(client, _config)
        _running_configs.append(_config)

    wait_for_completion(client, _running_configs, timeout)


def wait_for_completion(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    running_configs: typing.List[bigquery_datatransfer_v1.types.TransferConfig],
    timeout: int,
) -> None:
    _start = int(time.time())

    while True:
        latest_runs = []
        for config in running_configs:
            latest_runs.append(latest_transfer_run(client, config))

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
    target_project_id: str,
    dataset_id: str,
    display_name: str,
    service_account: str,
) -> bigquery_datatransfer_v1.types.TransferConfig:
    transfer_config = bigquery_datatransfer_v1.TransferConfig(
        destination_dataset_id=dataset_id,
        display_name=display_name,
        data_source_id="cross_region_copy",
        dataset_region="US",
        params={
            "source_project_id": source_project_id,
            "source_dataset_id": dataset_id,
        },
        schedule_options=bigquery_datatransfer_v1.ScheduleOptions(
            disable_auto_scheduling=True
        ),
    )

    request = bigquery_datatransfer_v1.types.CreateTransferConfigRequest(
        parent=client.common_project_path(target_project_id),
        transfer_config=transfer_config,
        service_account_name=service_account,
    )

    return client.create_transfer_config(request=request)


def trigger_config(
    client: bigquery_datatransfer_v1.DataTransferServiceClient,
    config: bigquery_datatransfer_v1.types.TransferConfig,
) -> None:
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)

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
        target_project_id=os.environ["TARGET_PROJECT_ID"],
        service_account=os.environ["SERVICE_ACCOUNT"],
        dataset_name=os.environ["DATASET_NAME"],
        dataset_versions=json.loads(os.environ["DATASET_VERSIONS"]),
        timeout=int(os.getenv("TIMEOUT", 1200)),
    )
