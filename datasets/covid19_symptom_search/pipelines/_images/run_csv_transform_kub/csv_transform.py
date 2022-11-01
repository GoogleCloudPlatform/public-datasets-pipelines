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


from datetime import datetime

from google.cloud import storage_transfer


def bucket_copy(project_id: str, description: str, source_bucket: str,sink_bucket: str, path: str, start_date: datetime):

    client = storage_transfer.StorageTransferServiceClient()

    one_time_schedule = {
        'day': now.day,
        'month': now.month,
        'year': now.year
    }
    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'description': description,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'schedule': {
                'schedule_start_date': one_time_schedule,
                'schedule_end_date': one_time_schedule
            },
            'transfer_spec': {
                'gcs_data_source': {
                    'bucket_name': source_bucket,
                },
                'gcs_data_sink': {
                    'bucket_name': sink_bucket,
                    'path': path
                },
                'transfer_options': {
                    'delete_objects_from_source_after_transfer': False
                }
            }
        }
    })
    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')

now = datetime.utcnow()
print("Start =>")
bucket_copy(project_id = "bigquery-public-data-dev",
    description = "Naveen's test transfer job",
    source_bucket = "covid-st-prod-datasets-bigquery",
    sink_bucket = "us-central1-dev-v2-cd7f5f38-bucket",
    path="data/covid19_symptom_search/",
    start_date=now.date)


