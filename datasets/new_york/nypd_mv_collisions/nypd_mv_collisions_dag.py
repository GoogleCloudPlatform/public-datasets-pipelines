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
    dag_id="new_york.nypd_mv_collisions",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="nypd_mv_collisions",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_nypd_mv_collisions }}",
        env_vars={
            "SOURCE_URL": "https://nycopendata.socrata.com/api/views/h9gi-nx95/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "150000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york/nypd_mv_collisions/data_output.csv",
            "ENGLISH_PIPELINE_NAME": "New York - NYPD Motor Vehicle Collisions",
            "SOURCE_DTYPES": '{\n  "CRASH DATE": "str",\n  "CRASH TIME": "str",\n  "BOROUGH": "str",\n  "ZIP CODE": "str",\n  "LATITUDE": "float64",\n  "LONGITUDE": "float64",\n  "LOCATION": "str",\n  "ON STREET NAME": "str",\n  "CROSS STREET NAME": "str",\n  "OFF STREET NAME": "str",\n  "NUMBER OF PERSONS INJURED": "str",\n  "NUMBER OF PERSONS KILLED" : "str",\n  "NUMBER OF PEDESTRIANS INJURED" : "str",\n  "NUMBER OF PEDESTRIANS KILLED" : "str",\n  "NUMBER OF CYCLIST INJURED" : "str",\n  "NUMBER OF CYCLIST KILLED" : "str",\n  "NUMBER OF MOTORIST INJURED" : "str",\n  "NUMBER OF MOTORIST KILLED" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 1" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 2" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 3" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 4" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 5" : "str",\n  "COLLISION_ID": "int64",\n  "VEHICLE TYPE CODE 1" : "str",\n  "VEHICLE TYPE CODE 2" : "str",\n  "VEHICLE TYPE CODE 3" : "str",\n  "VEHICLE TYPE CODE 4" : "str",\n  "VEHICLE TYPE CODE 5": "str"\n}',
            "TRANSFORM_LIST": '[ "replace_regex", "add_crash_timestamp", "convert_date_format", "rename_headers", "resolve_datatypes", "reorder_headers" ]',
            "REGEX_LIST": '[\n  [ "OFF STREET NAME", "\\\\n", " " ]\n]',
            "DATE_FORMAT_LIST": '[\n  ["timestamp", "%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]\n]',
            "CRASH_FIELD_LIST": '[ [ "timestamp", "CRASH DATE", "CRASH TIME" ] ]',
            "RENAME_HEADERS_LIST": '{\n  "BOROUGH": "borough",\n  "CONTRIBUTING FACTOR VEHICLE 1": "contributing_factor_vehicle_1",\n  "CONTRIBUTING FACTOR VEHICLE 2": "contributing_factor_vehicle_2",\n  "CONTRIBUTING FACTOR VEHICLE 3": "contributing_factor_vehicle_3",\n  "CONTRIBUTING FACTOR VEHICLE 4": "contributing_factor_vehicle_4",\n  "CONTRIBUTING FACTOR VEHICLE 5": "contributing_factor_vehicle_5",\n  "CROSS STREET NAME": "cross_street_name",\n  "LATITUDE": "latitude",\n  "LONGITUDE": "longitude",\n  "LOCATION": "location",\n  "NUMBER OF CYCLIST INJURED": "number_of_cyclist_injured",\n  "NUMBER OF CYCLIST KILLED": "number_of_cyclist_killed",\n  "NUMBER OF MOTORIST INJURED": "number_of_motorist_injured",\n  "NUMBER OF MOTORIST KILLED": "number_of_motorist_killed",\n  "NUMBER OF PEDESTRIANS INJURED": "number_of_pedestrians_injured",\n  "NUMBER OF PEDESTRIANS KILLED": "number_of_pedestrians_killed",\n  "NUMBER OF PERSONS INJURED": "number_of_persons_injured",\n  "NUMBER OF PERSONS KILLED": "number_of_persons_killed",\n  "OFF STREET NAME": "off_street_name",\n  "ON STREET NAME": "on_street_name",\n  "COLLISION_ID": "unique_key",\n  "VEHICLE TYPE CODE 1": "vehicle_type_code1",\n  "VEHICLE TYPE CODE 2": "vehicle_type_code2",\n  "VEHICLE TYPE CODE 3": "vehicle_type_code_3",\n  "VEHICLE TYPE CODE 4": "vehicle_type_code_4",\n  "VEHICLE TYPE CODE 5": "vehicle_type_code_5",\n  "ZIP CODE": "zip_code"\n}',
            "REORDER_HEADERS_LIST": '[\n  "borough",\n  "contributing_factor_vehicle_1",\n  "contributing_factor_vehicle_2",\n  "contributing_factor_vehicle_3",\n  "contributing_factor_vehicle_4",\n  "contributing_factor_vehicle_5",\n  "cross_street_name",\n  "timestamp",\n  "latitude",\n  "longitude",\n  "location",\n  "number_of_cyclist_injured",\n  "number_of_cyclist_killed",\n  "number_of_motorist_injured",\n  "number_of_motorist_killed",\n  "number_of_pedestrians_injured",\n  "number_of_pedestrians_killed",\n  "number_of_persons_injured",\n  "number_of_persons_killed",\n  "off_street_name",\n  "on_street_name",\n  "unique_key",\n  "vehicle_type_code1",\n  "vehicle_type_code2",\n  "vehicle_type_code_3",\n  "vehicle_type_code_4",\n  "vehicle_type_code_5",\n  "zip_code"\n]',
        },
        resources={"limit_memory": "4G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/new_york/nypd_mv_collisions/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.new_york.container_registry.nypd_mv_collisions_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "borough",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "contributing_factor_vehicle_1",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "contributing_factor_vehicle_2",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "contributing_factor_vehicle_3",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "contributing_factor_vehicle_4",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "contributing_factor_vehicle_5",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "cross_street_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "timestamp",
                "type": "DATETIME",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "latitude",
                "type": "FLOAT",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "longitude",
                "type": "FLOAT",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "location",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_cyclist_injured",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_cyclist_killed",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_motorist_injured",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_motorist_killed",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_pedestrians_injured",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_pedestrians_killed",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_persons_injured",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_persons_killed",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "off_street_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "on_street_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "unique_key",
                "type": "INTEGER",
                "description": "",
                "mode": "required",
            },
            {
                "name": "vehicle_type_code1",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "vehicle_type_code2",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "vehicle_type_code_3",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "vehicle_type_code_4",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "vehicle_type_code_5",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "zip_code",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
