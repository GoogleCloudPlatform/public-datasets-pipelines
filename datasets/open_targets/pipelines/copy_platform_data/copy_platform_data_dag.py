# Copyright 2021 Google LLC
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
    "start_date": "2021-04-01",
}


with DAG(
    dag_id="open_targets.copy_platform_data",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Transfer Open Targets Platform Dataset
    copy_bq_datasets = kubernetes_pod.KubernetesPodOperator(
        task_id="copy_bq_datasets",
        name="copy_bq_datasets",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.open_targets.container_registry.copy_bq_datasets }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.open_targets.platform.source_project_id }}",
            "TARGET_PROJECT_ID": "{{ var.json.open_targets.platform.target_project_id }}",
            "SERVICE_ACCOUNT": "{{ var.json.open_targets.service_account }}",
            "TRANSFER_CONFIG_NAME": "open-targets-platform",
            "SOURCE_DATASET_NAME": "{{ var.json.open_targets.platform.source_dataset_name }}",
            "TARGET_DATASET_NAME": "{{ var.json.open_targets.platform.target_dataset_name }}",
        },
        resources={
            "request_memory": "128M",
            "request_cpu": "200m",
            "request_ephemeral_storage": "5G",
        },
    )

    copy_bq_datasets
