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
    "start_date": "2022-08-23",
}


with DAG(
    dag_id="mimic_iii.mimic_iii",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run python script in kubernetes pod.
    copy_bq_dataset = kubernetes_pod.KubernetesPodOperator(
        task_id="copy_bq_dataset",
        name="copy_bq_dataset",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.mimic_iii.container_registry.run_script_kub }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.mimic_iii.source_project_id }}",
            "SOURCE_BQ_DATASET": "{{ var.json.mimic_iii.source_bq_dataset }}",
            "TARGET_PROJECT_ID": "{{ var.json.mimic_iii.target_project_id }}",
            "TARGET_BQ_DATASET": "{{ var.json.mimic_iii.target_bq_dataset }}",
        },
    )

    copy_bq_dataset
