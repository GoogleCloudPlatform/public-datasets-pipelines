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


from airflow import DAG
from airflow.providers.google.cloud.operators import cloud_storage_transfer_service

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-12-01",
}


with DAG(
    dag_id="mlcommons.mswc",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a GCS to GCS operation using Google resources
    copy_gcs_bucket = (
        cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
            task_id="copy_gcs_bucket",
            timeout=43200,
            retries=0,
            wait=True,
            project_id="bigquery-public-data",
            source_bucket="{{ var.json.mlcommons.mswc.source_bucket }}",
            destination_bucket="{{ var.json.mlcommons.mswc.destination_bucket}}",
            google_impersonation_chain="{{ var.json.mlcommons.mswc.service_account }}",
        )
    )

    copy_gcs_bucket
