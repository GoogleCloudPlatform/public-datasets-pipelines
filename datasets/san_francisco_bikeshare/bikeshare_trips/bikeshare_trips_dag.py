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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="san_francisco_bikeshare.bikeshare_trips",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="bikeshare_trips",
        namespace="default",
        affinity={
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    "values": ["pool-e2-standard-4"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        image_pull_policy="Always",
        image="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_trips }}",
        env_vars={
            "SOURCE_URL_HTTP": '"https://s3.amazonaws.com/fordgobike-data/201803-fordgobike-tripdata.csv.zip",\n"https://s3.amazonaws.com/fordgobike-data/201804-fordgobike-tripdata.csv.zip",\n"https://s3.amazonaws.com/fordgobike-data/201802-fordgobike-tripdata.csv.zip",\n"https://s3.amazonaws.com/fordgobike-data/201801-fordgobike-tripdata.csv.zip",\n"https://s3.amazonaws.com/fordgobike-data/2017-fordgobike-tripdata.csv",\n"https://s3.amazonaws.com/babs-open-data/babs_open_data_year_1.zip",\n"https://s3.amazonaws.com/babs-open-data/babs_open_data_year_2.zip",\n"https://s3.amazonaws.com/babs-open-data/babs_open_data_year_3.zip"\n',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_bikeshare/bikeshare_trips/data_output.csv",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/san_francisco_bikeshare/bikeshare_trips/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_trips_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "trip_id",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Numeric ID of bike trip",
            },
            {
                "name": "duration_sec",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Time of trip in seconds",
            },
            {
                "name": "start_date",
                "type": "TIMESTAMP",
                "mode": "NULLABLE",
                "description": "Start date of trip with date and time, in PST",
            },
            {
                "name": "start_station_name",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "Station name of start station",
            },
            {
                "name": "start_station_id",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Numeric reference for start station",
            },
            {
                "name": "end_date",
                "type": "TIMESTAMP",
                "mode": "NULLABLE",
                "description": "End date of trip with date and time, in PST",
            },
            {
                "name": "end_station_name",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "Station name for end station",
            },
            {
                "name": "end_station_id",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Numeric reference for end station",
            },
            {
                "name": "bike_number",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "ID of bike used",
            },
            {
                "name": "zip_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "Home zip code of subscriber (customers can choose to manually enter zip at kiosk however data is unreliable)",
            },
            {
                "name": "subscriber_type",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "Subscriber = annual or 30-day member; Customer = 24-hour or 3-day member",
            },
            {
                "name": "subscription_type",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "start_station_latitude",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "start_station_longitude",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "end_station_latitude",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "end_station_longitude",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "member_birth_year",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "member_gender",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "bike_share_for_all_trip",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "start_station_geom",
                "type": "GEOGRAPHY",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "end_station_geom",
                "type": "GEOGRAPHY",
                "mode": "NULLABLE",
                "description": "",
            },
        ],
    )

    transform_csv >> load_to_bq
