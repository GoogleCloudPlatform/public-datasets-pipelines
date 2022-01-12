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
    dag_id="new_york_taxi_trips.tlc_green_trips_2018",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    tlc_green_trips_2018_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="tlc_green_trips_2018_transform_csv",
        startup_timeout_seconds=600,
        name="tlc_green_trips_2018",
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
            "SOURCE_URL": "https://data.cityofnewyork.us/api/views/w7fs-fd9i/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "1000000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york_taxi_trips/tlc_green_trips_2018/data_output.csv",
            "PIPELINE_NAME": "tlc_green_trips_2018",
            "CSV_HEADERS": '["vendor_id","pickup_datetime","dropoff_datetime","store_and_fwd_flag","rate_code","passenger_count","trip_distance","fare_amount","extra","mta_tax","tip_amount","tolls_amount","ehail_fee","total_amount","payment_type","distance_between_service","time_between_service","trip_type","imp_surcharge","pickup_location_id","dropoff_location_id"]',
            "RENAME_MAPPINGS": '{"VendorID":"vendor_id","lpep_pickup_datetime":"pickup_datetime","lpep_dropoff_datetime":"dropoff_datetime","RatecodeID":"rate_code","improvement_surcharge":"imp_surcharge","DOLocationID":"dropoff_location_id","PULocationID":"pickup_location_id"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_tlc_green_trips_2018_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_tlc_green_trips_2018_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/new_york_taxi_trips/tlc_green_trips_2018/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="new_york_taxi_trips.tlc_green_trips_2018",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "vendor_id",
                "type": "string",
                "description": "A code indicating the LPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.",
                "mode": "required",
            },
            {
                "name": "pickup_datetime",
                "type": "datetime",
                "description": "The date and time when the meter was engaged",
                "mode": "nullable",
            },
            {
                "name": "dropoff_datetime",
                "type": "datetime",
                "description": "The date and time when the meter was disengaged",
                "mode": "nullable",
            },
            {
                "name": "store_and_fwd_flag",
                "type": "string",
                "description": "This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server. Y= store and forward trip N= not a store and forward trip",
                "mode": "nullable",
            },
            {
                "name": "rate_code",
                "type": "string",
                "description": "The final rate code in effect at the end of the trip. 1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride",
                "mode": "nullable",
            },
            {
                "name": "passenger_count",
                "type": "integer",
                "description": "The number of passengers in the vehicle. This is a driver-entered value.",
                "mode": "nullable",
            },
            {
                "name": "trip_distance",
                "type": "NUMERIC",
                "description": "The elapsed trip distance in miles reported by the taximeter.",
                "mode": "nullable",
            },
            {
                "name": "fare_amount",
                "type": "NUMERIC",
                "description": "The time-and-distance fare calculated by the meter",
                "mode": "nullable",
            },
            {
                "name": "extra",
                "type": "NUMERIC",
                "description": "Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges",
                "mode": "nullable",
            },
            {
                "name": "mta_tax",
                "type": "NUMERIC",
                "description": "$0.50 MTA tax that is automatically triggered based on the metered rate in use",
                "mode": "nullable",
            },
            {
                "name": "tip_amount",
                "type": "NUMERIC",
                "description": "Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.",
                "mode": "nullable",
            },
            {
                "name": "tolls_amount",
                "type": "NUMERIC",
                "description": "Total amount of all tolls paid in trip.",
                "mode": "nullable",
            },
            {
                "name": "ehail_fee",
                "type": "NUMERIC",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "total_amount",
                "type": "NUMERIC",
                "description": "The total amount charged to passengers. Does not include cash tips.",
                "mode": "nullable",
            },
            {
                "name": "payment_type",
                "type": "string",
                "description": "A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip",
                "mode": "nullable",
            },
            {
                "name": "distance_between_service",
                "type": "NUMERIC",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "time_between_service",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "trip_type",
                "type": "string",
                "description": "A code indicating whether the trip was a street-hail or a dispatch that is automatically assigned based on the metered rate in use but can be altered by the driver. 1= Street-hail 2= Dispatch",
                "mode": "nullable",
            },
            {
                "name": "imp_surcharge",
                "type": "NUMERIC",
                "description": "$0.30 improvement surcharge assessed on hailed trips at the flag drop. The improvement surcharge began being levied in 2015.",
                "mode": "nullable",
            },
            {
                "name": "pickup_location_id",
                "type": "string",
                "description": "TLC Taxi Zone in which the taximeter was engaged",
                "mode": "nullable",
            },
            {
                "name": "dropoff_location_id",
                "type": "string",
                "description": "TLC Taxi Zone in which the taximeter was disengaged",
                "mode": "nullable",
            },
        ],
    )

    tlc_green_trips_2018_transform_csv >> load_tlc_green_trips_2018_to_bq
