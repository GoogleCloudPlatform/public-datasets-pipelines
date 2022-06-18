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
from google.cloud import bigquery_datatransfer_v1 as dt
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
    # dataset_versions: typing.List[str],
    timeout: int,
):
    client = dt.DataTransferServiceClient()
    request=dt.types.ListTransferConfigsRequest(
        parent=f"projects/{target_project_id}"
    )

    _config = create_transfer_config(
        client=client,
        source_project_id=source_project_id,
        target_project_id=target_project_id,
        dataset_name=dataset_name,
        display_name=f"{dataset_name}-copy",
        service_account=service_account,
    )

    trigger_config(client, _config)

    wait_for_completion(client, request, timeout)


def wait_for_completion(
    client: dt.DataTransferServiceClient,
    running_config: dt.types.TransferConfig,
    timeout: int,
) -> None:
    _start = int(time.time())

    while True:
        # latest_runs = []
        # latest_runs.append(latest_transfer_run(client, running_config))

        # logging.info(f"States: {[str(run.state) for run in latest_runs]}")
        transfer_runs = client.list_transfer_runs(parent=running_config)
        latest_transfer = max(transfer_runs, key=operator.attrgetter("run_time"))
        logging.info(f"States: {str(running_config.state)}")

        # Mark as complete when all runs have succeeded
        if all(str(running_config.state) == "TransferState.SUCCEEDED"):
            return

        # Stop the process when it's longer than the allotted time
        if int(time.time()) - _start > timeout:
            raise TimeoutError

        time.sleep(RETRY_DELAY)


# def latest_transfer_run(
#     client: dt.DataTransferServiceClient,
#     config: dt.types.TransferConfig,
# ) -> dt.types.TransferRun:
#     transfer_runs = client.list_transfer_runs(parent=config)
#     # transfer_runs = client.list_transfer_runs()
#     return max(transfer_runs, key=operator.attrgetter("run_time"))


def create_transfer_config(
    client: dt.DataTransferServiceClient,
    source_project_id: str,
    target_project_id: str,
    dataset_name: str,
    display_name: str,
    service_account: str,
) -> dt.types.TransferConfig:
    transfer_config = dt.TransferConfig(
        destination_dataset_id=dataset_name,
        display_name=display_name,
        data_source_id="cross_region_copy",
        dataset_region="US",
        params={
            "source_project_id": source_project_id,
            "source_dataset_id": dataset_name,
        },
        schedule_options=dt.ScheduleOptions(
            disable_auto_scheduling=True
        ),
    )

    request = dt.types.CreateTransferConfigRequest(
        parent=client.common_project_path(target_project_id),
        transfer_config=transfer_config,
        service_account_name=service_account,
    )

    return client.create_transfer_config(request=request)


def trigger_config(
    client: dt.DataTransferServiceClient,
    config: dt.types.TransferConfig,
) -> None:
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * pow(10, 9))

    try:
        client.start_manual_transfer_runs(
            request=dt.types.StartManualTransferRunsRequest(
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
        # dataset_versions=json.loads(os.environ["DATASET_VERSIONS"]),
        timeout=int(os.getenv("TIMEOUT", 1200)),
    )
