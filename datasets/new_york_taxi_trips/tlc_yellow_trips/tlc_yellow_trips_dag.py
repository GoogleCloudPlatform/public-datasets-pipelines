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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

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
            "name": "new-york-taxi-trips--tlc-yellow-trips",
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
    transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv",
        startup_timeout_seconds=600,
        name="load_tlc_yellow_trips",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york-taxi-trips--tlc-yellow-trips",
        image_pull_policy="Always",
        image="{{ var.json.new_york_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_source_url }}",
            "SOURCE_YEARS_TO_LOAD": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_years_to_load }}",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_chunk_size }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_target_gcs_path }}",
            "PIPELINE_NAME": "tlc_yellow_trips",
            "INPUT_CSV_HEADERS": '[ "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count", "trip_distance",\n  "rate_code", "store_and_fwd_flag", "pickup_location_id", "dropoff_location_id",\n  "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount",\n  "tolls_amount", "imp_surcharge", "total_amount", "congestion_surcharge" ]',
            "DATA_DTYPES": '{ "vendor_id": "str",\n  "pickup_datetime": "datetime64[ns]",\n  "dropoff_datetime": "datetime64[ns]",\n  "passenger_count": "str",\n  "trip_distance": "float64",\n  "rate_code": "str",\n  "store_and_fwd_flag": "str",\n  "pickup_location_id": "str",\n  "dropoff_location_id": "str",\n  "payment_type": "str",\n  "fare_amount": "float64",\n  "extra": "float64",\n  "mta_tax": "float64",\n  "tip_amount": "float64",\n  "tolls_amount": "float64",\n  "imp_surcharge": "float64",\n  "total_amount": "float64",\n  "congestion_surcharge": "float64" }',
            "OUTPUT_CSV_HEADERS": '[ "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count", "trip_distance",\n  "rate_code", "store_and_fwd_flag", "payment_type", "fare_amount", "extra",\n  "mta_tax", "tip_amount", "tolls_amount", "imp_surcharge", "total_amount",\n  "pickup_location_id", "dropoff_location_id" ]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_0 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq_year_0",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_0_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_0_destination_table }}",
        schema_object="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_schema_path }}",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_1 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq_year_minus_1",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_1_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_1_destination_table }}",
        schema_object="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_schema_path }}",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq_year_minus_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_2_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_2_destination_table }}",
        schema_object="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_schema_path }}",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq_year_minus_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_3_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_3_destination_table }}",
        schema_object="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_schema_path }}",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_4 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq_year_minus_4",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_4_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_year_minus_4_destination_table }}",
        schema_object="{{ var.json.new_york_taxi_trips.container_registry.yellow_trips_schema_path }}",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="new-york-taxi-trips--tlc-yellow-trips",
    )

    create_cluster >> transform_csv
    transform_csv >> load_to_bq_year_0 >> load_to_bq_year_minus_1 >> load_to_bq_year_minus_2 >> load_to_bq_year_minus_3 >> load_to_bq_year_minus_4
    load_to_bq_year_minus_4 >> delete_cluster
