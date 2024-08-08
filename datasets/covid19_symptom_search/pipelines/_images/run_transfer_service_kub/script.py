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
from datetime import datetime

from google.cloud import storage_transfer


def main(
    project_id: str,
    description: str,
    source_bucket: str,
    sink_bucket: str,
    gcs_path: str,
):
    print(gcs_path)
    client = storage_transfer.StorageTransferServiceClient()
    one_time_schedule = {"day": now.day, "month": now.month, "year": now.year}
    transfer_job_request = storage_transfer.CreateTransferJobRequest(
        {
            "transfer_job": {
                "project_id": project_id,
                "description": description,
                "status": storage_transfer.TransferJob.Status.ENABLED,
                "schedule": {
                    "schedule_start_date": one_time_schedule,
                    "schedule_end_date": one_time_schedule,
                },
                "transfer_spec": {
                    "gcs_data_source": {
                        "bucket_name": source_bucket,
                    },
                    "gcs_data_sink": {"bucket_name": sink_bucket, "path": gcs_path},
                    "transfer_options": {
                        "delete_objects_from_source_after_transfer": False
                    },
                },
            }
        }
    )
    result = client.create_transfer_job(transfer_job_request)
    print(f"Created transferJob: {result.name}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    now = datetime.utcnow()
    print("Start =>")
    main(
        project_id=os.environ.get("PROJECT_ID"),
        description="Storage Transfer job",
        source_bucket=os.environ.get("SOURCE_BUCKET"),
        sink_bucket=os.environ.get("SINK_BUCKET"),
        gcs_path=os.environ.get("GCS_PATH"),
    )
