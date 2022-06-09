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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.operators import cloud_storage_transfer_service

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-11-23",
}


with DAG(
    dag_id="idc.copy_tcia_data",
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
            source_bucket="{{ var.json.idc.source_bucket }}",
            destination_bucket="{{ var.json.idc.destination_bucket}}",
            transfer_options={"deleteObjectsUniqueInSink": False},
        )
    )

    # Transfer IDC Databases
    copy_bq_datasets = kubernetes_pod.KubernetesPodOperator(
        task_id="copy_bq_datasets",
        name="copy_bq_datasets",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.idc.container_registry.copy_bq_datasets }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.idc.source_project_id }}",
            "TARGET_PROJECT_ID": "{{ var.json.idc.target_project_id }}",
            "SERVICE_ACCOUNT": "{{ var.json.idc.service_account }}",
            "DATASET_NAME": "idc",
            "DATASET_VERSIONS": '["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"]',
        },
        resources={"request_memory": "128M", "request_cpu": "200m"},
    )

    # Generate BQ views
    generate_bq_views = kubernetes_pod.KubernetesPodOperator(
        task_id="generate_bq_views",
        name="generate_bq_views",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.idc.container_registry.generate_bq_views }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.idc.source_project_id }}",
            "TARGET_PROJECT_ID": "{{ var.json.idc.target_project_id }}",
            "BQ_DATASETS": '["idc_v1", "idc_v2", "idc_v3", "idc_v4", "idc_v5", "idc_v6", "idc_v7", "idc_v8", "idc_v9", "idc_current"]',
            "SERVICE_ACCOUNT": "{{ var.json.idc.service_account }}",
        },
        resources={"request_memory": "128M", "request_cpu": "200m"},
    )

    copy_gcs_bucket >> copy_bq_datasets >> generate_bq_views
