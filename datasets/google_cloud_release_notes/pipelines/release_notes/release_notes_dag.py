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
from airflow.providers.google.cloud.operators import kubernetes_engine

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
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-google-cloud-release-notes",
            "initial_node_count": 2,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Copy GCP release notes dataset
    copy_bq_dataset = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_bq_dataset",
        startup_timeout_seconds=1000,
        name="copy_bq_dataset",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-cloud-release-notes",
        image_pull_policy="Always",
        image="{{ var.json.google_cloud_release_notes.container_registry.copy_bq_dataset }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.google_cloud_release_notes.source_project_id }}",
            "SOURCE_BQ_DATASET": "{{ var.json.google_cloud_release_notes.source_bq_dataset }}",
            "TARGET_PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_BQ_DATASET": "google_cloud_release_notes",
            "SERVICE_ACCOUNT": "{{ var.json.google_cloud_release_notes.service_account }}",
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-google-cloud-release-notes",
    )

    create_cluster >> copy_bq_dataset >> delete_cluster
