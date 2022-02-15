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
    dag_id="austin_crime.crime",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    austin_crime_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_crime_transform_csv",
        name="crime",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.austin_crime.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '["gs://pdp-feeds-staging/Austin_Crime/Annual_Crime_2014.csv","gs://pdp-feeds-staging/Austin_Crime/Annual_Crime_Dataset_2015.csv","gs://pdp-feeds-staging/Austin_Crime/2016_Annual_Crime_Data.csv"]',
            "SOURCE_FILE": '["files/data1.csv","files/data2.csv","files/data3.csv"]',
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin_crime/crime/data_output.csv",
            "FILE_PATH": "files/",
            "CSV_HEADERS": '["unique_key","address","census_tract","clearance_date","clearance_status","council_district_code","description","district","latitude","longitude","location","location_description","primary_type","timestamp","x_coordinate","y_coordinate","year","zipcode"]',
            "RENAME_MAPPINGS": '{"GO Primary Key" : "unique_key","Council District" : "council_district_code","GO Highest Offense Desc" : "description","Highest NIBRS/UCR Offense Description" : "primary_type","GO Report Date" : "timestamp","GO Location" : "location_description","Clearance Status" : "clearance_status","Clearance Date" : "clearance_date","GO District" : "district","GO Location Zip" : "zipcode","GO Census Tract" : "census_tract","GO X Coordinate" : "x_coordinate","GO Y Coordinate" : "y_coordinate","Location_1" : "temp_address"}',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_austin_crime_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_austin_crime_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/austin_crime/crime/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="austin_crime.crime",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "unique_key",
                "type": "integer",
                "description": "Unique identifier for the record.",
                "mode": "nullable",
            },
            {
                "name": "address",
                "type": "string",
                "description": "Full address where the incident occurred.",
                "mode": "nullable",
            },
            {
                "name": "census_tract",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "clearance_date",
                "type": "timestamp",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "clearance_status",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "council_district_code",
                "type": "integer",
                "description": "Indicates the council district code where the incident occurred.",
                "mode": "nullable",
            },
            {
                "name": "description",
                "type": "string",
                "description": "The subcategory of the primary description.",
                "mode": "nullable",
            },
            {
                "name": "district",
                "type": "string",
                "description": "Indicates the police district where the incident occurred.",
                "mode": "nullable",
            },
            {
                "name": "latitude",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "longitude",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "location",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "location_description",
                "type": "string",
                "description": "Description of the location where the incident occurred.",
                "mode": "nullable",
            },
            {
                "name": "primary_type",
                "type": "string",
                "description": "The primary description of the NIBRS/UCR code.",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Time when the incident occurred. This is sometimes a best estimate.",
                "mode": "nullable",
            },
            {
                "name": "x_coordinate",
                "type": "integer",
                "description": "The x coordinate of the location where the incident occurred",
                "mode": "nullable",
            },
            {
                "name": "y_coordinate",
                "type": "integer",
                "description": "The y coordinate of the location where the incident occurred",
                "mode": "nullable",
            },
            {
                "name": "year",
                "type": "integer",
                "description": "Indicates the year in which the incident occurred.",
                "mode": "nullable",
            },
            {
                "name": "zipcode",
                "type": "string",
                "description": "Indicates the zipcode where the incident occurred.",
                "mode": "nullable",
            },
        ],
    )

    austin_crime_transform_csv >> load_austin_crime_to_bq
