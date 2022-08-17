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
    "start_date": "2022-08-17",
}


with DAG(
    dag_id="mimiciii.mimiciii",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # ETL within the kubernetes pod
    py_gcs_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="py_gcs_to_bq",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.mimiciii.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_PROJECT": "{{ var.json.mimiciii.source_project }}",
            "DESTINATION_PROJECT": "{{ var.json.mimiciii.destination_project }}",
            "SOURCE_DATASET": "{{ var.json.mimiciii.source_dataset }}",
            "DESTINATION_DATASET": "{{ var.json.mimiciii.destination_dataset }}",
            "GCS_BUCKET": "{{ var.json.mimiciii.gcs_bucket }}",
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    py_gcs_to_bq
