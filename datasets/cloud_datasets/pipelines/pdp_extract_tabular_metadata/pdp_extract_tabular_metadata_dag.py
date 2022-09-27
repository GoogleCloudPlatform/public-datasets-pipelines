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
    "start_date": "2022-08-20",
}


with DAG(
    dag_id="cloud_datasets.pdp_extract_tabular_metadata",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Extract the metadata for tabular datasets
    pdp_extract_tabular_metadata_task = kubernetes_pod.KubernetesPodOperator(
        task_id="pdp_extract_tabular_metadata_task",
        name="pdp_extract_tabular_metadata_task",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cloud_datasets.container_registry.pdp_extract_tabular_metadata_image }}",
        env_vars={
            "SOURCE_PROJECTS_IDS": "{{ var.json.cloud_datasets.pdp_extract_tabular_metadata.source_projects_ids }}",
            "TARGET_PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_DATASET": "{{ var.json.cloud_datasets.pdp_extract_tabular_metadata.target_dataset }}",
            "TABULAR_DATASET_TABLE_NAME": "{{ var.json.cloud_datasets.pdp_extract_tabular_metadata.tabular_dataset_table_name }}",
            "TABLES_TABLE_NAME": "{{ var.json.cloud_datasets.pdp_extract_tabular_metadata.tables_table_name }}",
            "TABLES_FIELDS_TABLE_NAME": "{{ var.json.cloud_datasets.pdp_extract_tabular_metadata.tables_fields_table_name }}",
        },
        resources={"request_memory": "128M", "request_cpu": "200m"},
    )

    pdp_extract_tabular_metadata_task
