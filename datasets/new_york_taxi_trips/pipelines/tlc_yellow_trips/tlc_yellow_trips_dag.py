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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="new_york_taxi_trips.tlc_yellow_trips",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "new-york-taxi-trips",
            "initial_node_count": 1,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-8",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_and_load_data = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_and_load_data",
        startup_timeout_seconds=600,
        name="load_tlc_yellow_trips",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york-taxi-trips",
        image_pull_policy="Always",
        image="{{ var.json.new_york_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_source_url }}",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "DATA_FILE_YEAR_FIELD": "data_file_year",
            "DATA_FILE_MONTH_FIELD": "data_file_month",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_dataset_id }}",
            "TABLE_ID": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_table_id }}",
            "SCHEMA_PATH": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_schema_path }}",
            "CHUNKSIZE": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_chunk_size }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_target_gcs_path }}",
            "PIPELINE_NAME": "tlc_yellow_trips",
            "INPUT_CSV_HEADERS": '[ "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count", "trip_distance",\n  "rate_code", "store_and_fwd_flag", "pickup_location_id", "dropoff_location_id",\n  "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount",\n  "tolls_amount", "imp_surcharge", "total_amount", "congestion_surcharge" ]',
            "DATA_DTYPES": '{ "vendor_id": "str",\n  "pickup_datetime": "datetime64[ns]",\n  "dropoff_datetime": "datetime64[ns]",\n  "passenger_count": "str",\n  "trip_distance": "float64",\n  "rate_code": "str",\n  "store_and_fwd_flag": "str",\n  "pickup_location_id": "str",\n  "dropoff_location_id": "str",\n  "payment_type": "str",\n  "fare_amount": "float64",\n  "extra": "float64",\n  "mta_tax": "float64",\n  "tip_amount": "float64",\n  "tolls_amount": "float64",\n  "imp_surcharge": "float64",\n  "total_amount": "float64",\n  "congestion_surcharge": "float64" }',
            "OUTPUT_CSV_HEADERS": '[ "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count", "trip_distance",\n  "rate_code", "store_and_fwd_flag", "payment_type", "fare_amount", "extra",\n  "mta_tax", "tip_amount", "tolls_amount", "imp_surcharge", "total_amount",\n  "pickup_location_id", "dropoff_location_id", "data_file_year", "data_file_month" ]',
        },
    )

    create_cluster >> transform_csv_and_load_data
