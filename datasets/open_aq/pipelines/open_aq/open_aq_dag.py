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
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="open_aq.open_aq",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "open-aq",
            "initial_node_count": 1,
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

    # Run Open Air Quality load processes
    open_aq = kubernetes_engine.GKEStartPodOperator(
        task_id="open_aq",
        name="openaq.open_aq",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="open-aq",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.open_aq.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Open Air Quality",
            "SOURCE_URL": '{\n  "cities": "https://api.openaq.org/v2/cities?limit=100000&page=1&offset=0&sort=asc&order_by=city",\n  "countries": "https://api.openaq.org/v2/countries?limit=100000&page=1&offset=0&sort=asc&order_by=country",\n  "locations": "https://api.openaq.org/v2/locations?limit=100&page=1&offset=0&sort=desc&radius=1000&order_by=lastUpdated&dumpRaw=false"\n}',
            "ENGLISH_TRANSLATION_COL_LIST": '{\n  "cities": [ "city" ],\n  "countries": [ "name" ],\n  "locations": [ "city", "name", "country" ]\n}',
            "SOURCE_FILE": "files/data.json",
            "TARGET_FILE": "files/data_output.json",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "openaq",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/open_aq/.json",
            "SCHEMA_PATH": "data/open_aq/schema/openaq_schema.json",
            "DROP_DEST_TABLE": "N",
            "DATE_FORMAT_LIST": '[\n  ["firstUpdated", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S" ],\n  ["lastUpdated", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S" ]\n]',
        },
        resources={"request_ephemeral_storage": "10G", "limit_cpu": "3"},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="open-aq",
    )

    create_cluster >> open_aq >> delete_cluster
