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
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="us_climate_normals.normals_daily",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 */6 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    load_data_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="load_data_to_bq",
        startup_timeout_seconds=600,
        name="load_us_climate_normals_daily_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "US Climate Normals - Daily",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "us_climate_normals",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TABLE_PREFIX": "normals_daily",
            "SOURCE_LOCAL_FOLDER_ROOT": "files/us_climate_normals",
            "ROOT_GCS_FOLDER": "data/us_climate_normals",
            "ROOT_PIPELINE_GS_FOLDER": "normals-daily",
            "FOLDERS_LIST": '[\n  "",\n  "1981-2010",\n  "1991-2020",\n  "2006-2020"\n]',
        },
        resources={
            "request_memory": "12G",
            "request_cpu": "1",
            "request_ephemeral_storage": "16G",
        },
    )

    load_data_to_bq
