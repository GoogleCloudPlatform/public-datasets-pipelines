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
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="gnomad.copy_gcs_bucket",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a GCS to GCS operation using Google resources
    gnomad_gcs_bucket_transfer = (
        cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
            task_id="gnomad_gcs_bucket_transfer",
            timeout=43200,
            retries=0,
            wait=True,
            project_id="bigquery-public-data",
            source_bucket="gnomad-public-requester-pays",
            destination_bucket="gcp-public-data--gnomad",
            google_impersonation_chain="{{ var.json.gnomad.service_account }}",
            transfer_options={"deleteObjectsUniqueInSink": False},
        )
    )

    gnomad_gcs_bucket_transfer
