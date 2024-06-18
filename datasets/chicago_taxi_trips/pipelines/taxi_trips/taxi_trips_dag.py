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
from airflow.operators import bash
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.operators import kubernetes_engine
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
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "chicago-taxi-trips",
            "initial_node_count": 2,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Download Taxi Trips dataset
    prepare_source = kubernetes_engine.GKEStartPodOperator(
        task_id="prepare_source",
        name="taxi_trips",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="chicago-taxi-trips",
        namespace="default",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        image_pull_policy="Always",
        env_vars={
            "SOURCE_URL": "https://data.cityofchicago.org/api/views/wrvz-psew/rows.csv?accessType=DOWNLOAD&bom=true",
            "SOURCE_FILE": "./files/taxi_trips.csv",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CSV_GCS_PATH": "data/chicago_taxi_trips/taxi_trips.csv",
            "PIPELINE": "download_source",
        },
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="chicago-taxi-trips",
    )

    # Split Taxi Trips dataset into multiple files.
    split_source_file = bash.BashOperator(
        task_id="split_source_file",
        bash_command='rm -rf $split_files\nmkdir -p $split_files\ntail -n +2 $source_file | split --verbose -d -l 2700000 - --filter=\u0027sh -c "{ head -n1 $source_file; cat; } \u003e $FILE"\u0027 $split_files/split_file_\nrm -rf $output\n',
        env={
            "source_file": "/home/airflow/gcs/data/chicago_taxi_trips/taxi_trips.csv",
            "split_files": "/home/airflow/gcs/data/chicago_taxi_trips/split_files",
            "output": "/home/airflow/gcs/data/chicago_taxi_trips/output",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_1 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv_1",
        startup_timeout_seconds=600,
        name="taxi_trips_1",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT_FOLDER": "data/chicago_taxi_trips/split_files",
            "RENAME_MAPPINGS": '{"Trip ID": "unique_key", "Taxi ID": "taxi_id", "Trip Start Timestamp": "trip_start_timestamp", "Trip End Timestamp": "trip_end_timestamp", "Trip Seconds": "trip_seconds", "Trip Miles": "trip_miles", "Pickup Census Tract": "pickup_census_tract", "Dropoff Census Tract": "dropoff_census_tract", "Pickup Community Area": "pickup_community_area", "Dropoff Community Area": "dropoff_community_area", "Fare": "fare", "Tips": "tips", "Tolls": "tolls", "Extras": "extras", "Trip Total": "trip_total", "Payment Type": "payment_type", "Company": "company", "Pickup Centroid Latitude": "pickup_latitude", "Pickup Centroid Longitude": "pickup_longitude", "Pickup Centroid Location": "pickup_location", "Dropoff Centroid Latitude": "dropoff_latitude", "Dropoff Centroid Longitude": "dropoff_longitude", "Dropoff Centroid  Location": "dropoff_location"}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "OUTPUT_OBJECT_FOLDER": "data/chicago_taxi_trips/output",
            "DATA_TYPES": '{"Trip Seconds": "Int64", "Pickup Census Tract": "Int64", "Dropoff Census Tract": "Int64","Pickup Community Area": "Int64","Dropoff Community Area": "Int64"}',
            "DATE_COLS": '["Trip Start Timestamp", "Trip End Timestamp"]',
            "BATCH_COUNT": "1",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "2",
            "request_ephemeral_storage": "3G",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_2 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv_2",
        startup_timeout_seconds=600,
        name="taxi_trips_2",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT_FOLDER": "data/chicago_taxi_trips/split_files",
            "RENAME_MAPPINGS": '{"Trip ID": "unique_key", "Taxi ID": "taxi_id", "Trip Start Timestamp": "trip_start_timestamp", "Trip End Timestamp": "trip_end_timestamp", "Trip Seconds": "trip_seconds", "Trip Miles": "trip_miles", "Pickup Census Tract": "pickup_census_tract", "Dropoff Census Tract": "dropoff_census_tract", "Pickup Community Area": "pickup_community_area", "Dropoff Community Area": "dropoff_community_area", "Fare": "fare", "Tips": "tips", "Tolls": "tolls", "Extras": "extras", "Trip Total": "trip_total", "Payment Type": "payment_type", "Company": "company", "Pickup Centroid Latitude": "pickup_latitude", "Pickup Centroid Longitude": "pickup_longitude", "Pickup Centroid Location": "pickup_location", "Dropoff Centroid Latitude": "dropoff_latitude", "Dropoff Centroid Longitude": "dropoff_longitude", "Dropoff Centroid  Location": "dropoff_location"}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "OUTPUT_OBJECT_FOLDER": "data/chicago_taxi_trips/output",
            "DATA_TYPES": '{"Trip Seconds": "Int64", "Pickup Census Tract": "Int64", "Dropoff Census Tract": "Int64","Pickup Community Area": "Int64","Dropoff Community Area": "Int64"}',
            "DATE_COLS": '["Trip Start Timestamp", "Trip End Timestamp"]',
            "BATCH_COUNT": "2",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "2",
            "request_ephemeral_storage": "3G",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_3 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv_3",
        startup_timeout_seconds=600,
        name="taxi_trips_3",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT_FOLDER": "data/chicago_taxi_trips/split_files",
            "RENAME_MAPPINGS": '{"Trip ID": "unique_key", "Taxi ID": "taxi_id", "Trip Start Timestamp": "trip_start_timestamp", "Trip End Timestamp": "trip_end_timestamp", "Trip Seconds": "trip_seconds", "Trip Miles": "trip_miles", "Pickup Census Tract": "pickup_census_tract", "Dropoff Census Tract": "dropoff_census_tract", "Pickup Community Area": "pickup_community_area", "Dropoff Community Area": "dropoff_community_area", "Fare": "fare", "Tips": "tips", "Tolls": "tolls", "Extras": "extras", "Trip Total": "trip_total", "Payment Type": "payment_type", "Company": "company", "Pickup Centroid Latitude": "pickup_latitude", "Pickup Centroid Longitude": "pickup_longitude", "Pickup Centroid Location": "pickup_location", "Dropoff Centroid Latitude": "dropoff_latitude", "Dropoff Centroid Longitude": "dropoff_longitude", "Dropoff Centroid  Location": "dropoff_location"}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "OUTPUT_OBJECT_FOLDER": "data/chicago_taxi_trips/output",
            "DATA_TYPES": '{"Trip Seconds": "Int64", "Pickup Census Tract": "Int64", "Dropoff Census Tract": "Int64","Pickup Community Area": "Int64","Dropoff Community Area": "Int64"}',
            "DATE_COLS": '["Trip Start Timestamp", "Trip End Timestamp"]',
            "BATCH_COUNT": "3",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "2",
            "request_ephemeral_storage": "3G",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_4 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv_4",
        startup_timeout_seconds=600,
        name="taxi_trips_4",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT_FOLDER": "data/chicago_taxi_trips/split_files",
            "RENAME_MAPPINGS": '{"Trip ID": "unique_key", "Taxi ID": "taxi_id", "Trip Start Timestamp": "trip_start_timestamp", "Trip End Timestamp": "trip_end_timestamp", "Trip Seconds": "trip_seconds", "Trip Miles": "trip_miles", "Pickup Census Tract": "pickup_census_tract", "Dropoff Census Tract": "dropoff_census_tract", "Pickup Community Area": "pickup_community_area", "Dropoff Community Area": "dropoff_community_area", "Fare": "fare", "Tips": "tips", "Tolls": "tolls", "Extras": "extras", "Trip Total": "trip_total", "Payment Type": "payment_type", "Company": "company", "Pickup Centroid Latitude": "pickup_latitude", "Pickup Centroid Longitude": "pickup_longitude", "Pickup Centroid Location": "pickup_location", "Dropoff Centroid Latitude": "dropoff_latitude", "Dropoff Centroid Longitude": "dropoff_longitude", "Dropoff Centroid  Location": "dropoff_location"}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "OUTPUT_OBJECT_FOLDER": "data/chicago_taxi_trips/output",
            "DATA_TYPES": '{"Trip Seconds": "Int64", "Pickup Census Tract": "Int64", "Dropoff Census Tract": "Int64","Pickup Community Area": "Int64","Dropoff Community Area": "Int64"}',
            "DATE_COLS": '["Trip Start Timestamp", "Trip End Timestamp"]',
            "BATCH_COUNT": "4",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "2",
            "request_ephemeral_storage": "3G",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_5 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv_5",
        startup_timeout_seconds=600,
        name="taxi_trips_5",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT_FOLDER": "data/chicago_taxi_trips/split_files",
            "RENAME_MAPPINGS": '{"Trip ID": "unique_key", "Taxi ID": "taxi_id", "Trip Start Timestamp": "trip_start_timestamp", "Trip End Timestamp": "trip_end_timestamp", "Trip Seconds": "trip_seconds", "Trip Miles": "trip_miles", "Pickup Census Tract": "pickup_census_tract", "Dropoff Census Tract": "dropoff_census_tract", "Pickup Community Area": "pickup_community_area", "Dropoff Community Area": "dropoff_community_area", "Fare": "fare", "Tips": "tips", "Tolls": "tolls", "Extras": "extras", "Trip Total": "trip_total", "Payment Type": "payment_type", "Company": "company", "Pickup Centroid Latitude": "pickup_latitude", "Pickup Centroid Longitude": "pickup_longitude", "Pickup Centroid Location": "pickup_location", "Dropoff Centroid Latitude": "dropoff_latitude", "Dropoff Centroid Longitude": "dropoff_longitude", "Dropoff Centroid  Location": "dropoff_location"}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "OUTPUT_OBJECT_FOLDER": "data/chicago_taxi_trips/output",
            "DATA_TYPES": '{"Trip Seconds": "Int64", "Pickup Census Tract": "Int64", "Dropoff Census Tract": "Int64","Pickup Community Area": "Int64","Dropoff Community Area": "Int64"}',
            "DATE_COLS": '["Trip Start Timestamp", "Trip End Timestamp"]',
            "BATCH_COUNT": "5",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "2",
            "request_ephemeral_storage": "3G",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_6 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv_6",
        startup_timeout_seconds=600,
        name="taxi_trips_6",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT_FOLDER": "data/chicago_taxi_trips/split_files",
            "RENAME_MAPPINGS": '{"Trip ID": "unique_key", "Taxi ID": "taxi_id", "Trip Start Timestamp": "trip_start_timestamp", "Trip End Timestamp": "trip_end_timestamp", "Trip Seconds": "trip_seconds", "Trip Miles": "trip_miles", "Pickup Census Tract": "pickup_census_tract", "Dropoff Census Tract": "dropoff_census_tract", "Pickup Community Area": "pickup_community_area", "Dropoff Community Area": "dropoff_community_area", "Fare": "fare", "Tips": "tips", "Tolls": "tolls", "Extras": "extras", "Trip Total": "trip_total", "Payment Type": "payment_type", "Company": "company", "Pickup Centroid Latitude": "pickup_latitude", "Pickup Centroid Longitude": "pickup_longitude", "Pickup Centroid Location": "pickup_location", "Dropoff Centroid Latitude": "dropoff_latitude", "Dropoff Centroid Longitude": "dropoff_longitude", "Dropoff Centroid  Location": "dropoff_location"}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "OUTPUT_OBJECT_FOLDER": "data/chicago_taxi_trips/output",
            "DATA_TYPES": '{"Trip Seconds": "Int64", "Pickup Census Tract": "Int64", "Dropoff Census Tract": "Int64","Pickup Community Area": "Int64","Dropoff Community Area": "Int64"}',
            "DATE_COLS": '["Trip Start Timestamp", "Trip End Timestamp"]',
            "BATCH_COUNT": "6",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "2",
            "request_ephemeral_storage": "3G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_taxi_trips_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_taxi_trips_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/chicago_taxi_trips/output/*"],
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

    create_cluster >> prepare_source >> [delete_cluster, split_source_file]
    (
        split_source_file
        >> [
            transform_csv_1,
            transform_csv_2,
            transform_csv_3,
            transform_csv_4,
            transform_csv_5,
            transform_csv_6,
        ]
        >> load_taxi_trips_to_bq
    )
