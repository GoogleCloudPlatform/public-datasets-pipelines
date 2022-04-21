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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="ml_datasets.iris",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    iris_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="iris_transform_csv",
        startup_timeout_seconds=600,
        name="iris",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.ml_datasets.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.openml.org/data/get_csv/61/dataset_61_iris.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/ml_datasets/iris/data_output.csv",
            "PIPELINE_NAME": "iris",
            "CSV_HEADERS": '["sepal_length","sepal_width","petal_length","petal_width","species"]',
            "RENAME_MAPPINGS": '{"sepallength": "sepal_length","sepalwidth": "sepal_width","petallength": "petal_length","petalwidth": "petal_width","class": "species"}',
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_iris_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_iris_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ml_datasets/iris/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ml_datasets.iris",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "sepal_length",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "sepal_width",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "petal_length",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "petal_width",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "species",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
        ],
    )

    iris_transform_csv >> load_iris_to_bq
