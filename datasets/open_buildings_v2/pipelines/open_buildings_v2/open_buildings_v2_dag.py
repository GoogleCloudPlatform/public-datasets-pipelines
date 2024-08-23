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
    "start_date": "2022-12-19",
}


with DAG(
    dag_id="open_buildings_v2.open_buildings_v2",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil -m cp -R gs://open-buildings-data/v2/polygons_s2_level_4_gzip gs://{{ var.value.composer_bucket }}/data/open_buildings_v2/source_files/",
    )

    # Unzip data
    bash_unzip = bash.BashOperator(
        task_id="bash_unzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/open_buildings_v2/source_files/polygons_s2_level_4_gzip/* ;",
    )

    # EL within the kubernetes pod
    kub_gcs_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="kub_gcs_to_bq",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.open_buildings_v2.container_registry.run_script_kub }}",
        env_vars={
            "SOURCE_GCS_PATH": "data/open_buildings_v2/source_files/polygons_s2_level_4_gzip/",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "open_buildings_v2",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SCHEMA_FILEPATH": "schema.json",
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    bash_gcs_to_gcs >> bash_unzip >> kub_gcs_to_bq
