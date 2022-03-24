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
    dag_id="new_york.new_york",
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
            "name": "new-york",
            "initial_node_count": 1,
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

    # Run New York NYPD MV Collisions Pipeline
    transform_csv_nypd_mv_collisions = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_nypd_mv_collisions",
        name="nypd_mv_collisions",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.nypd_mv_collisions.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.new_york.container_registry.nypd_mv_collisions.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.new_york.container_registry.nypd_mv_collisions.source_url }}",
            "CHUNKSIZE": "{{ var.json.new_york.container_registry.nypd_mv_collisions.chunksize }}",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.new_york.container_registry.nypd_mv_collisions.dataset_id }}",
            "TABLE_ID": "{{ var.json.new_york.container_registry.nypd_mv_collisions.destination_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york.container_registry.nypd_mv_collisions.target_path }}",
            "SCHEMA_PATH": "{{ var.json.new_york.container_registry.nypd_mv_collisions.schema_path }}",
            "DATA_DTYPES": '{\n  "CRASH DATE": "str",\n  "CRASH TIME": "str",\n  "BOROUGH": "str",\n  "ZIP CODE": "str",\n  "LATITUDE": "float64",\n  "LONGITUDE": "float64",\n  "LOCATION": "str",\n  "ON STREET NAME": "str",\n  "CROSS STREET NAME": "str",\n  "OFF STREET NAME": "str",\n  "NUMBER OF PERSONS INJURED": "str",\n  "NUMBER OF PERSONS KILLED" : "str",\n  "NUMBER OF PEDESTRIANS INJURED" : "str",\n  "NUMBER OF PEDESTRIANS KILLED" : "str",\n  "NUMBER OF CYCLIST INJURED" : "str",\n  "NUMBER OF CYCLIST KILLED" : "str",\n  "NUMBER OF MOTORIST INJURED" : "str",\n  "NUMBER OF MOTORIST KILLED" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 1" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 2" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 3" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 4" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 5" : "str",\n  "COLLISION_ID": "int64",\n  "VEHICLE TYPE CODE 1" : "str",\n  "VEHICLE TYPE CODE 2" : "str",\n  "VEHICLE TYPE CODE 3" : "str",\n  "VEHICLE TYPE CODE 4" : "str",\n  "VEHICLE TYPE CODE 5": "str"\n}',
            "RESOLVE_DATATYPES_LIST": '{\n  "latitude": "float64",\n  "longitude": "float64",\n  "number_of_cyclist_injured": "int64",\n  "number_of_cyclist_killed": "int64",\n  "number_of_motorist_injured": "int64",\n  "number_of_motorist_killed": "int64",\n  "number_of_pedestrians_injured": "int64",\n  "number_of_pedestrians_killed": "int64",\n  "number_of_persons_injured": "int64",\n  "number_of_persons_killed": "int64"\n}',
            "TRANSFORM_LIST": '[ "replace_regex", "add_crash_timestamp", "convert_date_format", "rename_headers", "resolve_datatypes", "reorder_headers" ]',
            "REGEX_LIST": '[\n  [ "OFF STREET NAME", "\\\\n", " " ]\n]',
            "DATE_FORMAT_LIST": '[\n  ["timestamp", "%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]\n]',
            "CRASH_FIELD_LIST": '[ [ "timestamp", "CRASH DATE", "CRASH TIME" ] ]',
            "RENAME_HEADERS_LIST": '{\n  "BOROUGH": "borough",\n  "CONTRIBUTING FACTOR VEHICLE 1": "contributing_factor_vehicle_1",\n  "CONTRIBUTING FACTOR VEHICLE 2": "contributing_factor_vehicle_2",\n  "CONTRIBUTING FACTOR VEHICLE 3": "contributing_factor_vehicle_3",\n  "CONTRIBUTING FACTOR VEHICLE 4": "contributing_factor_vehicle_4",\n  "CONTRIBUTING FACTOR VEHICLE 5": "contributing_factor_vehicle_5",\n  "CROSS STREET NAME": "cross_street_name",\n  "LATITUDE": "latitude",\n  "LONGITUDE": "longitude",\n  "LOCATION": "location",\n  "NUMBER OF CYCLIST INJURED": "number_of_cyclist_injured",\n  "NUMBER OF CYCLIST KILLED": "number_of_cyclist_killed",\n  "NUMBER OF MOTORIST INJURED": "number_of_motorist_injured",\n  "NUMBER OF MOTORIST KILLED": "number_of_motorist_killed",\n  "NUMBER OF PEDESTRIANS INJURED": "number_of_pedestrians_injured",\n  "NUMBER OF PEDESTRIANS KILLED": "number_of_pedestrians_killed",\n  "NUMBER OF PERSONS INJURED": "number_of_persons_injured",\n  "NUMBER OF PERSONS KILLED": "number_of_persons_killed",\n  "OFF STREET NAME": "off_street_name",\n  "ON STREET NAME": "on_street_name",\n  "COLLISION_ID": "unique_key",\n  "VEHICLE TYPE CODE 1": "vehicle_type_code1",\n  "VEHICLE TYPE CODE 2": "vehicle_type_code2",\n  "VEHICLE TYPE CODE 3": "vehicle_type_code_3",\n  "VEHICLE TYPE CODE 4": "vehicle_type_code_4",\n  "VEHICLE TYPE CODE 5": "vehicle_type_code_5",\n  "ZIP CODE": "zip_code"\n}',
            "REORDER_HEADERS_LIST": '[\n  "borough",\n  "contributing_factor_vehicle_1",\n  "contributing_factor_vehicle_2",\n  "contributing_factor_vehicle_3",\n  "contributing_factor_vehicle_4",\n  "contributing_factor_vehicle_5",\n  "cross_street_name",\n  "timestamp",\n  "latitude",\n  "longitude",\n  "location",\n  "number_of_cyclist_injured",\n  "number_of_cyclist_killed",\n  "number_of_motorist_injured",\n  "number_of_motorist_killed",\n  "number_of_pedestrians_injured",\n  "number_of_pedestrians_killed",\n  "number_of_persons_injured",\n  "number_of_persons_killed",\n  "off_street_name",\n  "on_street_name",\n  "unique_key",\n  "vehicle_type_code1",\n  "vehicle_type_code2",\n  "vehicle_type_code_3",\n  "vehicle_type_code_4",\n  "vehicle_type_code_5",\n  "zip_code"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="new-york",
    )

    create_cluster >> [transform_csv_nypd_mv_collisions] >> delete_cluster
