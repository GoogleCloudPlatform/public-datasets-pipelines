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
    "start_date": "2022-10-31",
}


with DAG(
    dag_id="covid19_symptom_search.covid19_symptom_search",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # ETL within the kubernetes pod
    kub_test = kubernetes_pod.KubernetesPodOperator(
        task_id="kub_test",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.covid19_symptom_search.container_registry.run_csv_transform_kub }}",
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    kub_test
