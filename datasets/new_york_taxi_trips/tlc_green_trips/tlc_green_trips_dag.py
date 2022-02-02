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
    dag_id="new_york_taxi_trips.tlc_green_trips",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="transform_csv",
        startup_timeout_seconds=600,
        name="load_tlc_green_trips",
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
        image="{{ var.json.new_york_taxi_trips.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_",
            "SOURCE_YEARS_TO_LOAD": "{{ var.json.new_york_taxi_trips.container_registry.green_trips_years_to_load }}",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "1500000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york_taxi_trips/tlc_green_trips/data_output.csv",
            "PIPELINE_NAME": "tlc_green_trips",
            "INPUT_CSV_HEADERS": '["vendor_id", "pickup_datetime", "dropoff_datetime", "store_and_fwd_flag", "rate_code",\n "pickup_location_id", "dropoff_location_id", "passenger_count", "trip_distance", "fare_amount",\n "extra", "mta_tax", "tip_amount", "tolls_amount", "ehail_fee",\n "imp_surcharge", "total_amount", "payment_type", "trip_type", "congestion_surcharge" ]',
            "DATA_DTYPES": '{ "vendor_id": "str",\n  "pickup_datetime": "datetime64[ns]",\n  "dropoff_datetime": "datetime64[ns]",\n  "store_and_fwd_flag": "str",\n  "rate_code": "str",\n  "pickup_location_id": "str",\n  "dropoff_location_id": "str",\n  "passenger_count": "str",\n  "trip_distance": "float64",\n  "fare_amount": "float64",\n  "extra": "float64",\n  "mta_tax": "float64",\n  "tip_amount": "float64",\n  "tolls_amount": "float64",\n  "ehail_fee": "float64",\n  "imp_surcharge": "float64",\n  "total_amount": "float64",\n  "payment_type": "str",\n  "trip_type": "str",\n  "congestion_surcharge": "float64" }',
            "OUTPUT_CSV_HEADERS": '[ "vendor_id", "pickup_datetime", "dropoff_datetime", "store_and_fwd_flag", "rate_code",\n  "passenger_count", "trip_distance", "fare_amount", "extra", "mta_tax",\n  "tip_amount", "tolls_amount", "ehail_fee", "total_amount", "payment_type",\n  "distance_between_service", "time_between_service", "trip_type", "imp_surcharge", "pickup_location_id",\n  "dropoff_location_id" ]',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_0 = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq_year_0",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_0_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_0_destination_table }}",
        schema_object="schema/new_york_taxi_trips/tlc_green_trips/green_trips_schema.json",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_1 = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq_year_minus_1",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_1_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_1_destination_table }}",
        schema_object="schema/new_york_taxi_trips/tlc_green_trips/green_trips_schema.json",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_2 = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq_year_minus_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_2_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_2_destination_table }}",
        schema_object="schema/new_york_taxi_trips/tlc_green_trips/green_trips_schema.json",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_3 = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq_year_minus_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_3_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_3_destination_table }}",
        schema_object="schema/new_york_taxi_trips/tlc_green_trips/green_trips_schema.json",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq_year_minus_4 = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq_year_minus_4",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_4_source_file }}",
        destination_project_dataset_table="{{ var.json.new_york_taxi_trips.container_registry.green_trips_year_minus_4_destination_table }}",
        schema_object="schema/new_york_taxi_trips/tlc_green_trips/green_trips_schema.json",
        source_format="CSV",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    transform_csv >> load_to_bq_year_0 >> load_to_bq_year_minus_1 >> load_to_bq_year_minus_2 >> load_to_bq_year_minus_3 >> load_to_bq_year_minus_4
