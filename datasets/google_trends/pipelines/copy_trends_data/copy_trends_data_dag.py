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
    "start_date": "2022-03-22",
}


with DAG(
    dag_id="google_trends.copy_trends_data",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 2 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy Google Trends dataset
    copy_bq_datasets = kubernetes_pod.KubernetesPodOperator(
        task_id="copy_bq_datasets",
        name="copy_bq_datasets",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.google_trends.container_registry.copy_bq_datasets }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.google_trends.source_project_id }}",
            "SOURCE_BQ_DATASET": "{{ var.json.google_trends.source_bq_dataset }}",
            "TARGET_PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_BQ_DATASET": "{{ var.json.google_trends.target_bq_dataset }}",
            "EXPECTED_TABLES": '["top_terms", "top_rising_terms", "international_top_terms", "international_top_rising_terms"]',
            "SERVICE_ACCOUNT": "{{ var.json.google_trends.service_account }}",
        },
    )

    copy_bq_datasets
