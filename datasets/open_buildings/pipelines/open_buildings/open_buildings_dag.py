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
from airflow.operators import bash
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-08-12",
}


with DAG(
    dag_id="open_buildings.open_buildings",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Unzip data
    bash_gunzip = bash.BashOperator(
        task_id="bash_gunzip",
        bash_command="gunzip -v /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/*",
    )

    # ETL within the kubernetes pod
    py_gcs_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="py_gcs_to_bq",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.open_buildings.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_PATH": "{{ var.json.open_buildings.source_gcs_path }}",
            "PROJECT_ID": "{{ var.json.open_buildings.project_id }}",
            "DATASET_ID": "{{ var.json.open_buildings.dataset_id }}",
            "GCS_BUCKET": "{{ var.json.open_buildings.gcs_bucket }}",
            "SCHEMA_FILEPATH": "schema.json",
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    bash_gunzip >> py_gcs_to_bq
