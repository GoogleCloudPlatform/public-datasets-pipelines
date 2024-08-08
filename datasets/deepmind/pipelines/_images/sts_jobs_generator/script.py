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


import logging
import os
import time
import typing

from google.cloud import storage, storage_transfer

POLL_INTERVAL_INC = 60
POLL_INTERVAL_MAX = 600


def main(
    manifest_bucket: str,
    manifest_prefix: str,
    source_bucket: str,
    destination_bucket: str,
    gcp_project: str,
) -> None:
    manifest_files = get_manifest_files(manifest_bucket, manifest_prefix)
    _operations = []
    for manifest in manifest_files:
        _operation = create_transfer_job(
            manifest_bucket=manifest_bucket,
            manifest=manifest,
            source_bucket=source_bucket,
            destination_bucket=destination_bucket,
            gcp_project=gcp_project,
        )
        _operations.append(_operation)

    poll_interval = 0
    while True:
        logging.info("Checking transfer job statuses..")

        _done = [op.done() for op in _operations]
        if all(_done):
            # Break the loop when all transfers are done
            logging.info(f"All {len(_done)} transfer jobs complete.")
            break
        else:
            # If transfers are still running, wait some time and poll again
            poll_interval = min(poll_interval + POLL_INTERVAL_INC, POLL_INTERVAL_MAX)
            logging.info(
                f"Transfer jobs completed: {_done.count(True)}/{len(_done)} (next check in {poll_interval} seconds)"
            )

        time.sleep(poll_interval)


def get_manifest_files(bucket: str, prefix: str) -> typing.List[storage.blob.Blob]:
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket, prefix=f"{prefix}/", delimiter="/")
    blobs = list(blobs)
    logging.info(f"Found {len(blobs)} manifest files:")
    for blob in blobs:
        logging.info(f"- {blob.name}")
    return blobs


def create_transfer_job(
    manifest_bucket: str,
    manifest: storage.blob.Blob,
    source_bucket: str,
    destination_bucket: str,
    gcp_project: str,
):
    # Create a client
    client = storage_transfer.StorageTransferServiceClient()

    job_name = f"transferJobs/deepmind-afdb-{manifest.name.split('/')[-1].replace('.csv', '')}-{time.time_ns() // 1_000_000}"
    logging.info(f"Creating transfer job {job_name}")

    # Initialize request argument(s)
    request = {
        "transfer_job": {
            "name": job_name,
            "project_id": gcp_project,
            "status": storage_transfer.TransferJob.Status.ENABLED,
            "transfer_spec": {
                "gcs_data_source": {
                    "bucket_name": source_bucket,
                },
                "gcs_data_sink": {"bucket_name": destination_bucket},
                "transfer_options": {"overwrite_when": "DIFFERENT"},
                "transfer_manifest": {
                    "location": f"gs://{manifest_bucket}/{manifest.name}"
                },
            },
        }
    }

    client.create_transfer_job(request=request)
    logging.info(f"Created transfer job {job_name}")

    logging.info(f"Running transfer job {job_name}")
    request = storage_transfer.RunTransferJobRequest(
        job_name=job_name, project_id=gcp_project
    )

    operation = client.run_transfer_job(request=request)
    return operation


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        manifest_bucket=os.environ["MANIFEST_BUCKET"],
        manifest_prefix=os.environ["MANIFEST_PREFIX"],
        source_bucket=os.environ["SOURCE_BUCKET"],
        destination_bucket=os.environ["DESTINATION_BUCKET"],
        gcp_project=os.environ["GCP_PROJECT"],
    )
