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
from airflow.contrib.operators import gcs_to_bq
from airflow.operators import bash_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-05-01",
}


with DAG(
    dag_id="ml_datasets.iris",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:
    download_csv_file = bash_operator.BashOperator(
        task_id="download_csv_file",
        bash_command="mkdir -p $airflow_data_folder/ml_datasets/iris\ncurl -o $airflow_data_folder/ml_dataset/iris/data-source-{{ ds }}.csv -L $csv_source_url\n",
        env={
            "csv_source_url": "https://www.openml.org/data/get_csv/61/dataset_61_iris.csv",
            "airflow_data_folder": "{{ var.json.shared.airflow_data_folder }}",
        },
    )

    # Run a custom Python script
    transform_csv = bash_operator.BashOperator(
        task_id="transform_csv",
        bash_command="SOURCE_CSV=$airflow_data_folder/ml_dataset/iris/data-source-{{ ds }}.csv TARGET_CSV=$airflow_data_folder/ml_dataset/iris/transformed-data-{{ ds }}.csv python $airflow_home/dags/$dataset/$pipeline/custom/transform_csv.py\n",
        env={
            "airflow_home": "{{ var.json.shared.airflow_home }}",
            "airflow_data_folder": "{{ var.json.shared.airflow_data_folder }}",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/ml_datasets/iris/transformed-data-{{ ds }}.csv"],
        source_format="CSV",
        destination_project_dataset_table="ml_datasets.iris",
        skip_leading_rows=1,
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

    download_csv_file >> transform_csv >> load_to_bq
