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
    "start_date": "2022-06-10",
}


with DAG(
    dag_id="uniref50.uniref50",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_load_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_load_csv",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "uniref50",
            "DESTINATION_FOLDER": "files",
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_PATH": "data/uniref50/uniref",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "TABLE_ID": "uniref50",
            "CSV_HEADERS": '[\n  "ClusterID",\n  "TaxID",\n  "RepID",\n  "Sequence",\n  "Size",\n  "ClusterName",\n  "Organism"\n]',
            "REORDER_HEADERS_LIST": '[\n  "ClusterID",\n  "RepID",\n  "TaxID",\n  "Sequence",\n  "ClusterName",\n  "Size",\n  "Organism"\n]',
            "FIELD_SEPARATOR": "~",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_ephemeral_storage": "10G",
            "request_memory": "12G",
            "request_cpu": "1",
        },
    )

    transform_load_csv
