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
    dag_id="austin.bikeshare_trips",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    austin_bikeshare_trips_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="austin_bikeshare_trips_transform_csv",
        name="bikeshare_trips",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.austin_bikeshare_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.austintexas.gov/api/views/tyfh-5r8s/rows.csv",
            "SOURCE_FILE": "/custom/data.csv",
            "TARGET_FILE": "/custom/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin_bikeshare_trips/bikeshare_trips/data_output.csv",
        },
        resources={"limit_memory": "8G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_austin_bikeshare_trips_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_austin_bikeshare_trips_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/austin_bikeshare_trips/bikeshare_trips/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="austin_bikeshare_trips.bikeshare_trips",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "trip_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "subscriber_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "bikeid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "start_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "start_station_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "start_station_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "end_station_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "end_station_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "duration_minutes", "type": "INTEGER", "mode": "NULLABLE"},
        ],
    )

    austin_bikeshare_trips_transform_csv >> load_austin_bikeshare_trips_to_bq
