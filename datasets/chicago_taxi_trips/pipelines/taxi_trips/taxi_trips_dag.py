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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="chicago_taxi_trips.taxi_trips",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Download Taxi Trips dataset
    prepare_source = kubernetes_pod.KubernetesPodOperator(
        task_id="prepare_source",
        name="taxi_trips",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        image_pull_policy="Always",
        env_vars={
            "SOURCE_URL": "https://data.cityofchicago.org/api/views/wrvz-psew/rows.csv",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CSV_GCS_PATH": "data/chicago_taxi_trips/taxi_trips.csv",
            "CSV_HEADERS": '[\n  "unique_key", "taxi_id", "trip_start_timestamp",\n  "trip_end_timestamp", "trip_seconds", "trip_miles",\n  "pickup_census_tract", "dropoff_census_tract",\n  "pickup_community_area", "dropoff_community_area",\n  "fare", "tips", "tolls", "extras",\n  "trip_total", "payment_type", "company",\n  "pickup_latitude", "pickup_longitude",\n  "pickup_location", "dropoff_latitude",\n  "dropoff_longitude", "dropoff_location"\n]',
            "DATA_DTYPES": '{\n  "unique_key": "str", "taxi_id": "str", "trip_start_timestamp": "str",\n  "trip_end_timestamp": "str", "trip_seconds": "str", "trip_miles": "str",\n  "pickup_census_tract": "str", "dropoff_census_tract": "str",\n  "pickup_community_area": "str", "dropoff_community_area": "str",\n  "fare": "str", "tips": "str", "tolls": "str", "extras": "str",\n  "trip_total": "str", "payment_type": "str", "company": "str",\n  "pickup_latitude": "str", "pickup_longitude": "str",\n  "pickup_location": "str", "dropoff_latitude": "str",\n  "dropoff_longitude": "str", "dropoff_location": "str"\n}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "CHUNKSIZE": "1000000",
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_taxi_trips_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_taxi_trips_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/chicago_taxi_trips/batch/taxi_trips*.csv"],
        source_format="CSV",
        destination_project_dataset_table="chicago_taxi_trips.taxi_trips",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "unique_key",
                "type": "string",
                "mode": "required",
                "description": "Unique identifier for the trip.",
            },
            {
                "name": "taxi_id",
                "type": "string",
                "mode": "required",
                "description": "A unique identifier for the taxi.",
            },
            {
                "name": "trip_start_timestamp",
                "type": "timestamp",
                "mode": "nullable",
                "description": "When the trip started, rounded to the nearest 15 minutes.",
            },
            {
                "name": "trip_end_timestamp",
                "type": "timestamp",
                "mode": "nullable",
                "description": "When the trip ended, rounded to the nearest 15 minutes.",
            },
            {
                "name": "trip_seconds",
                "type": "integer",
                "mode": "nullable",
                "description": "Time of the trip in seconds.",
            },
            {
                "name": "trip_miles",
                "type": "float",
                "mode": "nullable",
                "description": "Distance of the trip in miles.",
            },
            {
                "name": "pickup_census_tract",
                "type": "integer",
                "mode": "nullable",
                "description": "The Census Tract where the trip began. For privacy, this Census Tract is not shown for some trips.",
            },
            {
                "name": "dropoff_census_tract",
                "type": "integer",
                "mode": "nullable",
                "description": "The Census Tract where the trip ended. For privacy, this Census Tract is not shown for some trips.",
            },
            {
                "name": "pickup_community_area",
                "type": "integer",
                "mode": "nullable",
                "description": "The Community Area where the trip began.",
            },
            {
                "name": "dropoff_community_area",
                "type": "integer",
                "mode": "nullable",
                "description": "The Community Area where the trip ended.",
            },
            {
                "name": "fare",
                "type": "float",
                "mode": "nullable",
                "description": "The fare for the trip.",
            },
            {
                "name": "tips",
                "type": "float",
                "mode": "nullable",
                "description": "The tip for the trip. Cash tips generally will not be recorded.",
            },
            {
                "name": "tolls",
                "type": "float",
                "mode": "nullable",
                "description": "The tolls for the trip.",
            },
            {
                "name": "extras",
                "type": "float",
                "mode": "nullable",
                "description": "Extra charges for the trip.",
            },
            {
                "name": "trip_total",
                "type": "float",
                "mode": "nullable",
                "description": "Total cost of the trip, the total of the fare, tips, tolls, and extras.",
            },
            {
                "name": "payment_type",
                "type": "string",
                "mode": "nullable",
                "description": "Type of payment for the trip.",
            },
            {
                "name": "company",
                "type": "string",
                "mode": "nullable",
                "description": "The taxi company.",
            },
            {
                "name": "pickup_latitude",
                "type": "float",
                "mode": "nullable",
                "description": "The latitude of the center of the pickup census tract or the community area if the census tract has been hidden for privacy.",
            },
            {
                "name": "pickup_longitude",
                "type": "float",
                "mode": "nullable",
                "description": "The longitude of the center of the pickup census tract or the community area if the census tract has been hidden for privacy.",
            },
            {
                "name": "pickup_location",
                "type": "string",
                "mode": "nullable",
                "description": "The location of the center of the pickup census tract or the community area if the census tract has been hidden for privacy.",
            },
            {
                "name": "dropoff_latitude",
                "type": "float",
                "mode": "nullable",
                "description": "The latitude of the center of the dropoff census tract or the community area if the census tract has been hidden for privacy.",
            },
            {
                "name": "dropoff_longitude",
                "type": "float",
                "mode": "nullable",
                "description": "The longitude of the center of the dropoff census tract or the community area if the census tract has been hidden for privacy.",
            },
            {
                "name": "dropoff_location",
                "type": "string",
                "mode": "nullable",
                "description": "The location of the center of the dropoff census tract or the community area if the census tract has been hidden for privacy.",
            },
        ],
    )

    prepare_source >> load_taxi_trips_to_bq
