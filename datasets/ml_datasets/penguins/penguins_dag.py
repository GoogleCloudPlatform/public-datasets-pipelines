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

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="ml_datasets.penguins",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    penguins_gcs_to_bq_task = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="penguins_gcs_to_bq_task",
        bucket="cloud-samples-data",
        source_objects=[
            "ai-platform/penguins/penguins.data.csv",
            "ai-platform/penguins/penguins.test.csv",
        ],
        source_format="CSV",
        destination_project_dataset_table="ml_datasets.penguins",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "species", "type": "STRING", "mode": "REQUIRED"},
            {"name": "island", "type": "STRING", "mode": "NULLABLE"},
            {"name": "culmen_length_mm", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "culmen_depth_mm", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "flipper_length_mm", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "body_mass_g", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "sex", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    penguins_gcs_to_bq_task
