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
    dag_id="chicago_crime.crime",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    chicago_crime_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="chicago_crime_transform_csv",
        startup_timeout_seconds=600,
        name="crime",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.chicago_crime.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/chicago_crime/crime/data_output.csv",
        },
        resources={"request_memory": "8G", "request_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_chicago_crime_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_chicago_crime_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/chicago_crime/crime/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="chicago_crime.crime",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "unique_key", "type": "integer", "mode": "required"},
            {"name": "case_number", "type": "string", "mode": "nullable"},
            {"name": "date", "type": "timestamp", "mode": "nullable"},
            {"name": "block", "type": "string", "mode": "nullable"},
            {"name": "iucr", "type": "string", "mode": "nullable"},
            {"name": "primary_type", "type": "string", "mode": "nullable"},
            {"name": "description", "type": "string", "mode": "nullable"},
            {"name": "location_description", "type": "string", "mode": "nullable"},
            {"name": "arrest", "type": "boolean", "mode": "nullable"},
            {"name": "domestic", "type": "boolean", "mode": "nullable"},
            {"name": "beat", "type": "integer", "mode": "nullable"},
            {"name": "district", "type": "integer", "mode": "nullable"},
            {"name": "ward", "type": "integer", "mode": "nullable"},
            {"name": "community_area", "type": "integer", "mode": "nullable"},
            {"name": "fbi_code", "type": "string", "mode": "nullable"},
            {"name": "x_coordinate", "type": "float", "mode": "nullable"},
            {"name": "y_coordinate", "type": "float", "mode": "nullable"},
            {"name": "year", "type": "integer"},
            {"name": "updated_on", "type": "timestamp", "mode": "nullable"},
            {"name": "latitude", "type": "float", "mode": "nullable"},
            {"name": "longitude", "type": "float", "mode": "nullable"},
            {"name": "location", "type": "string", "mode": "nullable"},
        ],
    )

    chicago_crime_transform_csv >> load_chicago_crime_to_bq
