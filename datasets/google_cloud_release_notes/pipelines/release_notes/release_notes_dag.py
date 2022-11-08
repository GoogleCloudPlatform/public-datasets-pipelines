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


from airflow import DAG
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-08-05",
}


with DAG(
    dag_id="google_cloud_release_notes.release_notes",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 5 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy GCP release notes dataset
    copy_bq_dataset = kubernetes_pod.KubernetesPodOperator(
        task_id="copy_bq_dataset",
        name="copy_bq_dataset",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.google_cloud_release_notes.container_registry.copy_bq_dataset }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.google_cloud_release_notes.source_project_id }}",
            "SOURCE_BQ_DATASET": "{{ var.json.google_cloud_release_notes.source_bq_dataset }}",
            "TARGET_PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_BQ_DATASET": "google_cloud_release_notes",
            "SERVICE_ACCOUNT": "{{ var.json.google_cloud_release_notes.service_account }}",
        },
        resources={"request_memory": "128M", "request_cpu": "200m"},
    )

    copy_bq_dataset
