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
    dag_id="san_francisco.san_francisco",
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
            "name": "san-francisco",
            "initial_node_count": 4,
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

    # Run New York 311 Service Requests Pipeline
    sf_311_service_requests = kubernetes_engine.GKEStartPodOperator(
        task_id="sf_311_service_requests",
        name="sf_311_service_requests",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sf_311_service_requests.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.san_francisco.sf_311_service_requests.source_url }}",
            "CHUNKSIZE": "{{ var.json.san_francisco.sf_311_service_requests.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sf_311_service_requests.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sf_311_service_requests.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sf_311_service_requests.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sf_311_service_requests.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sf_311_service_requests.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sf_311_service_requests.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sf_311_service_requests.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "INPUT_CSV_HEADERS": '[\n  "CaseID",\n  "Opened",\n  "Closed",\n  "Updated",\n  "Status",\n  "Status Notes",\n  "Responsible Agency",\n  "Category",\n  "Request Type",\n  "Request Details",\n  "Address",\n  "Supervisor District",\n  "Neighborhood",\n  "Point",\n  "Source",\n  "Media URL",\n  "Latitude",\n  "Longitude",\n  "Police District"\n]',
            "RENAME_HEADERS_LIST": '{\n  "CaseID": "unique_key",\n  "Opened": "created_date",\n  "Closed": "closed_date",\n  "Updated": "resolution_action_updated_date",\n  "Status": "status",\n  "Status Notes": "status_notes",\n  "Responsible Agency": "agency_name",\n  "Category": "category",\n  "Request Type": "complaint_type",\n  "Request Details": "descriptor",\n  "Address": "incident_address",\n  "Supervisor District": "supervisor_district",\n  "Neighborhood": "neighborhood",\n  "Point": "location",\n  "Source": "source",\n  "Media URL": "media_url",\n  "Latitude": "latitude",\n  "Longitude": "longitude",\n  "Police District": "police_district"\n}',
            "EMPTY_KEY_LIST": '[\n  "unique_key"\n]',
            "RESOLVE_DATATYPES_LIST": '{\n  "supervisor_district": "Int64"\n}',
            "REMOVE_PAREN_LIST": '[\n  "latitude",\n  "longitude"\n]',
            "STRIP_NEWLINES_LIST": '[\n  "status_notes",\n  "descriptor"\n]',
            "STRIP_WHITESPACE_LIST": '[\n  "incident_address"\n]',
            "DATE_FORMAT_LIST": '{\n  "created_date": "%Y-%m-%d %H:%M:%S",\n  "closed_date": "%Y-%m-%d %H:%M:%S",\n  "resolution_action_updated_date": "%Y-%m-%d %H:%M:%S"\n}',
            "REORDER_HEADERS_LIST": '[\n    "unique_key",\n    "created_date",\n    "closed_date",\n    "resolution_action_updated_date",\n    "status",\n    "status_notes",\n    "agency_name",\n    "category",\n    "complaint_type",\n    "descriptor",\n    "incident_address",\n    "supervisor_district",\n    "neighborhood",\n    "location",\n    "source",\n    "media_url",\n    "latitude",\n    "longitude",\n    "police_district"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Run San Francisco Bikeshare Stations Pipeline
    sf_bikeshare_stations = kubernetes_engine.GKEStartPodOperator(
        task_id="sf_bikeshare_stations",
        name="bikeshare_stations",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sf_bikeshare_stations.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.san_francisco.sf_bikeshare_stations.source_url }}",
            "CHUNKSIZE": "{{ var.json.san_francisco.sf_bikeshare_stations.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sf_bikeshare_stations.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sf_bikeshare_stations.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sf_bikeshare_stations.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sf_bikeshare_stations.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sf_bikeshare_stations.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sf_bikeshare_stations.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sf_bikeshare_stations.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "RENAME_HEADERS_LIST": '{\n  "data.stations.station_id": "station_id",\n  "data.stations.name": "name",\n  "data.stations.short_name": "short_name",\n  "data.stations.lat": "lat",\n  "data.stations.lon": "lon",\n  "data.stations.region_id": "region_id",\n  "data.stations.rental_methods": "rental_methods",\n  "data.stations.capacity": "capacity",\n  "data.stations.eightd_has_key_dispenser": "eightd_has_key_dispenser",\n  "data.stations.has_kiosk": "has_kiosk",\n  "data.stations.external_id": "external_id"\n}',
            "EMPTY_KEY_LIST": '[\n  "station_id",\n  "name",\n  "lat",\n  "lon"\n]',
            "GEN_LOCATION_LIST": '{\n  "station_geom": [ "lon", "lat" ]\n}',
            "RESOLVE_DATATYPES_LIST": '{\n  "region_id": "Int64"\n}',
            "REMOVE_PAREN_LIST": '[\n  "latitude",\n  "longitude"\n]',
            "STRIP_WHITESPACE_LIST": '[\n  "incident_address"\n]',
            "DATE_FORMAT_LIST": '{\n  "created_date": "%Y-%m-%d %H:%M:%S",\n  "closed_date": "%Y-%m-%d %H:%M:%S",\n  "resolution_action_updated_date": "%Y-%m-%d %H:%M:%S"\n}',
            "REORDER_HEADERS_LIST": '[\n  "station_id",\n  "name",\n  "short_name",\n  "lat",\n  "lon",\n  "region_id",\n  "rental_methods",\n  "capacity",\n  "external_id",\n  "eightd_has_key_dispenser",\n  "has_kiosk",\n  "station_geom"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Run San Francisco Bikeshare Status Pipeline
    sf_bikeshare_status = kubernetes_engine.GKEStartPodOperator(
        task_id="sf_bikeshare_status",
        name="bikeshare_status",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sf_bikeshare_status.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.san_francisco.sf_bikeshare_status.source_url }}",
            "CHUNKSIZE": "{{ var.json.san_francisco.sf_bikeshare_status.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sf_bikeshare_status.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sf_bikeshare_status.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sf_bikeshare_status.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sf_bikeshare_status.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sf_bikeshare_status.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sf_bikeshare_status.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sf_bikeshare_status.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "RENAME_HEADERS_LIST": '{\n  "data.stations.eightd_has_available_keys": "eightd_has_available_keys",\n  "data.stations.is_installed": "is_installed",\n  "data.stations.is_renting": "is_renting",\n  "data.stations.is_returning": "is_returning",\n  "data.stations.last_reported": "last_reported",\n  "data.stations.num_bikes_available": "num_bikes_available",\n  "data.stations.num_bikes_disabled": "num_bikes_disabled",\n  "data.stations.num_docks_available": "num_docks_available",\n  "data.stations.num_docks_disabled": "num_docks_disabled",\n  "data.stations.num_ebikes_available": "num_ebikes_available",\n  "data.stations.station_id": "station_id"\n}',
            "EMPTY_KEY_LIST": '[\n  "station_id",\n  "num_bikes_available",\n  "num_docks_available",\n  "is_installed",\n  "is_renting",\n  "is_returning",\n  "last_reported"\n]',
            "REORDER_HEADERS_LIST": '[\n  "station_id",\n  "num_bikes_available",\n  "num_bikes_disabled",\n  "num_docks_available",\n  "num_docks_disabled",\n  "is_installed",\n  "is_renting",\n  "is_returning",\n  "last_reported",\n  "num_ebikes_available",\n  "eightd_has_available_keys"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Run San Francisco Bikeshare Trips Pipeline
    sf_bikeshare_trips = kubernetes_engine.GKEStartPodOperator(
        task_id="sf_bikeshare_trips",
        name="sf_bikeshare_trips",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sf_bikeshare_trips.pipeline_name }}",
            "SOURCE_URL_LIST": '[\n  "https://s3.amazonaws.com/fordgobike-data/201803-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/201804-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/201802-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/201801-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/2017-fordgobike-tripdata.csv",\n  "https://s3.amazonaws.com/babs-open-data/babs_open_data_year_1.zip",\n  "https://s3.amazonaws.com/babs-open-data/babs_open_data_year_2.zip",\n  "https://s3.amazonaws.com/babs-open-data/babs_open_data_year_3.zip"\n]',
            "CHUNKSIZE": "{{ var.json.san_francisco.sf_bikeshare_trips.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sf_bikeshare_trips.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sf_bikeshare_trips.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sf_bikeshare_trips.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sf_bikeshare_trips.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sf_bikeshare_trips.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sf_bikeshare_trips.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sf_bikeshare_trips.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "TRIP_DATA_NAMES": '[\n  "source_file",\n  "trip_id",\n  "duration_sec",\n  "start_date",\n  "start_station_name",\n  "start_station_terminal",\n  "end_date",\n  "end_station_name",\n  "end_station_terminal",\n  "bike_number",\n  "subscription_type",\n  "zip_code"\n]',
            "TRIP_DATA_DTYPES": '{\n  "source_file": "str",\n  "trip_id": "str",\n  "duration_sec": "str",\n  "start_date": "str",\n  "start_station_name": "str",\n  "start_station_terminal": "str",\n  "end_date": "str",\n  "end_station_name": "str",\n  "end_station_terminal": "str",\n  "bike_number": "str",\n  "subscription_type": "str",\n  "zip_code": "str"\n}',
            "TRIPDATA_NAMES": '[\n  "source_file",\n  "duration_sec",\n  "start_date",\n  "end_date",\n  "start_station_terminal",\n  "start_station_name",\n  "start_station_latitude",\n  "start_station_longitude",\n  "end_station_terminal",\n  "end_station_name",\n  "end_station_latitude",\n  "end_station_longitude",\n  "bike_number",\n  "subscriber_type",\n  "member_birth_year",\n  "member_gender",\n  "bike_share_for_all_trip"\n]',
            "TRIPDATA_DTYPES": '{\n    "source_file": "str",\n    "duration_sec": "int",\n    "start_date": "str",\n    "end_date": "str",\n    "start_station_terminal": "int",\n    "start_station_name": "str",\n    "start_station_latitude": "float",\n    "start_station_longitude": "float",\n    "end_station_terminal": "int",\n    "end_station_name": "str",\n    "end_station_latitude": "float",\n    "end_station_longitude": "float",\n    "bike_number": "int",\n    "subscriber_type": "str",\n    "member_birth_year": "str",\n    "member_gender": "str",\n    "bike_share_for_all_trip": "str"\n}',
            "RENAME_HEADERS_TRIPDATA": '{\n  "duration_sec": "Duration",\n  "start_time": "Start Date",\n  "start_station_name": "Start Station",\n  "start_station_id": "Start Terminal",\n  "end_time": "End Date",\n  "end_station_name": "End Station",\n  "end_station_id": "End Terminal",\n  "bike_id": "Bike #",\n  "user_type": "Subscription Type",\n  "start_station_latitude": "start_station_latitude",\n  "start_station_longitude": "start_station_longitude",\n  "end_station_latitude": "end_station_latitude",\n  "end_station_longitude": "end_station_longitude",\n  "member_birth_year": "member_birth_year",\n  "member_gender": "member_gender",\n  "bike_share_for_all_trip": "bike_share_for_all_trip"\n}',
            "RENAME_HEADERS_LIST": '{\n  "trip_id": "trip_id",\n  "duration_sec": "duration_sec",\n  "start_date": "start_date",\n  "start_station_name": "start_station_name",\n  "start_station_terminal": "start_station_id",\n  "end_date": "end_date",\n  "end_station_name": "end_station_name",\n  "end_station_terminal": "end_station_id",\n  "bike_number": "bike_number",\n  "zip_code": "zip_code",\n  "subscriber_type_new": "subscriber_type",\n  "subscription_type": "subscription_type",\n  "start_station_latitude": "start_station_latitude",\n  "start_station_longitude": "start_station_longitude",\n  "end_station_latitude": "end_station_latitude",\n  "end_station_longitude": "end_station_longitude",\n  "member_birth_year": "member_birth_year",\n  "member_gender": "member_gender",\n  "bike_share_for_all_trip": "bike_share_for_all_trip",\n  "start_station_geom": "start_station_geom",\n  "end_station_geom": "end_station_geom"\n}',
            "RESOLVE_DATATYPES_LIST": '{\n  "member_birth_year": "Int64"\n}',
            "DATE_FORMAT_LIST": '{\n  "start_date": "%Y-%m-%d %H:%M:%S",\n  "end_date": "%Y-%m-%d %H:%M:%S"\n}',
            "GEN_LOCATION_LIST": '{\n  "start_station_geom": [ "start_station_longitude", "start_station_latitude" ],\n  "end_station_geom": [ "end_station_longitude", "end_station_latitude" ]\n}',
            "REORDER_HEADERS_LIST": '[\n  "trip_id",\n  "duration_sec",\n  "start_date",\n  "start_station_name",\n  "start_station_id",\n  "end_date",\n  "end_station_name",\n  "end_station_id",\n  "bike_number",\n  "zip_code",\n  "subscriber_type",\n  "subscription_type",\n  "start_station_latitude",\n  "start_station_longitude",\n  "end_station_latitude",\n  "end_station_longitude",\n  "member_birth_year",\n  "member_gender",\n  "bike_share_for_all_trip",\n  "start_station_geom",\n  "end_station_geom"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Run San Francisco Film Locations Pipeline
    sf_film_locations = kubernetes_engine.GKEStartPodOperator(
        task_id="sf_film_locations",
        name="sf_film_locations",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sf_film_locations.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.san_francisco.sf_film_locations.source_url }}",
            "CHUNKSIZE": "{{ var.json.san_francisco.sf_film_locations.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sf_film_locations.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sf_film_locations.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sf_film_locations.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sf_film_locations.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sf_film_locations.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sf_film_locations.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sf_film_locations.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "RENAME_HEADERS_LIST": '{\n  "Title": "title",\n  "Release Year": "release_year",\n  "Locations": "locations",\n  "Fun Facts": "fun_facts",\n  "Production Company": "production_company",\n  "Distributor": "distributor",\n  "Director": "director",\n  "Writer": "writer",\n  "Actor 1": "actor_1",\n  "Actor 2": "actor_2",\n  "Actor 3": "actor_3"\n}',
            "STRIP_WHITESPACE_LIST": '[\n  "distributor",\n  "director",\n  "actor_2"\n]',
            "STRIP_NEWLINES_LIST": '[\n  "production_company",\n  "fun_facts"\n]',
            "REORDER_HEADERS_LIST": '[\n  "title",\n  "release_year",\n  "locations",\n  "fun_facts",\n  "production_company",\n  "distributor",\n  "director",\n  "writer",\n  "actor_1",\n  "actor_2",\n  "actor_3"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Run San Francisco Fire Department Service Calls Pipeline
    sffd_service_calls = kubernetes_engine.GKEStartPodOperator(
        task_id="sffd_service_calls",
        name="sffd_service_calls",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sffd_service_calls.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.san_francisco.sffd_service_calls.source_url }}",
            "CHUNKSIZE": "{{ var.json.san_francisco.sffd_service_calls.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sffd_service_calls.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sffd_service_calls.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sffd_service_calls.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sffd_service_calls.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sffd_service_calls.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sffd_service_calls.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sffd_service_calls.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "INPUT_CSV_HEADERS": '[\n  "Call Number",\n  "Unit ID",\n  "Incident Number",\n  "Call Type",\n  "Call Date",\n  "Watch Date",\n  "Received DtTm",\n  "Entry DtTm",\n  "Dispatch DtTm",\n  "Response DtTm",\n  "On Scene DtTm",\n  "Transport DtTm",\n  "Hospital DtTm",\n  "Call Final Disposition",\n  "Available DtTm",\n  "Address",\n  "City",\n  "Zipcode of Incident",\n  "Battalion",\n  "Station Area",\n  "Box",\n  "Original Priority",\n  "Priority",\n  "Final Priority",\n  "ALS Unit",\n  "Call Type Group",\n  "Number of Alarms",\n  "Unit Type",\n  "Unit sequence in call dispatch",\n  "Fire Prevention District",\n  "Supervisor District",\n  "Neighborhooods - Analysis Boundaries",\n  "RowID",\n  "case_location"\n]',
            "DATA_DTYPES": '{\n  "Call Number": "int64",\n  "Unit ID": "str",\n  "Incident Number": "int64",\n  "Call Type": "str",\n  "Call Date": "str",\n  "Watch Date": "str",\n  "Received DtTm": "str",\n  "Entry DtTm": "str",\n  "Dispatch DtTm": "str",\n  "Response DtTm": "str",\n  "On Scene DtTm": "str",\n  "Transport DtTm": "str",\n  "Hospital DtTm": "str",\n  "Call Final Disposition": "str",\n  "Available DtTm": "str",\n  "Address": "str",\n  "City": "str",\n  "Zipcode of Incident": "str",\n  "Battalion": "str",\n  "Station Area": "str",\n  "Box": "str",\n  "Original Priority": "str",\n  "Priority": "str",\n  "Final Priority": "int64",\n  "ALS Unit": "str",\n  "Call Type Group": "str",\n  "Number of Alarms": "str",\n  "Unit Type": "str",\n  "Unit sequence in call dispatch": "str",\n  "Fire Prevention District": "str",\n  "Supervisor District": "str",\n  "Neighborhooods - Analysis Boundaries": "str",\n  "RowID": "str",\n  "case_location": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Call Number": "call_number",\n  "Unit ID": "unit_id",\n  "Incident Number": "incident_number",\n  "Call Type": "call_type",\n  "Call Date": "call_date",\n  "Watch Date": "watch_date",\n  "Received DtTm": "received_timestamp",\n  "Entry DtTm": "entry_timestamp",\n  "Dispatch DtTm": "dispatch_timestamp",\n  "Response DtTm": "response_timestamp",\n  "On Scene DtTm": "on_scene_timestamp",\n  "Transport DtTm": "transport_timestamp",\n  "Hospital DtTm": "hospital_timestamp",\n  "Call Final Disposition": "call_final_disposition",\n  "Available DtTm": "available_timestamp",\n  "Address": "address",\n  "City": "city",\n  "Zipcode of Incident": "zipcode_of_incident",\n  "Battalion": "battalion",\n  "Station Area": "station_area",\n  "Box": "box",\n  "Original Priority": "original_priority",\n  "Priority": "priority",\n  "Final Priority": "final_priority",\n  "ALS Unit": "als_unit",\n  "Call Type Group": "call_type_group",\n  "Number of Alarms": "number_of_alarms",\n  "Unit Type": "unit_type",\n  "Unit sequence in call dispatch": "unit_sequence_in_call_dispatch",\n  "Fire Prevention District": "fire_prevention_district",\n  "Supervisor District": "supervisor_district",\n  "Neighborhooods - Analysis Boundaries": "neighborhood_name",\n  "RowID": "row_id",\n  "case_location": "location_geom"\n}',
            "DATE_FORMAT_LIST": '{\n  "call_date": "%Y-%m-%d",\n  "watch_date": "%Y-%m-%d",\n  "available_timestamp": "%Y-%m-%d %H:%M:%S",\n  "dispatch_timestamp": "%Y-%m-%d %H:%M:%S",\n  "entry_timestamp": "%Y-%m-%d %H:%M:%S",\n  "on_scene_timestamp": "%Y-%m-%d %H:%M:%S",\n  "received_timestamp": "%Y-%m-%d %H:%M:%S",\n  "response_timestamp": "%Y-%m-%d %H:%M:%S",\n  "transport_timestamp": "%Y-%m-%d %H:%M:%S",\n  "hospital_timestamp": "%Y-%m-%d %H:%M:%S"\n}',
            "REORDER_HEADERS_LIST": '[\n  "call_number",\n  "unit_id",\n  "incident_number",\n  "call_type",\n  "call_date",\n  "watch_date",\n  "received_timestamp",\n  "entry_timestamp",\n  "dispatch_timestamp",\n  "response_timestamp",\n  "on_scene_timestamp",\n  "transport_timestamp",\n  "hospital_timestamp",\n  "call_final_disposition",\n  "available_timestamp",\n  "address",\n  "city",\n  "zipcode_of_incident",\n  "battalion",\n  "station_area",\n  "box",\n  "original_priority",\n  "priority",\n  "final_priority",\n  "als_unit",\n  "call_type_group",\n  "number_of_alarms",\n  "unit_type",\n  "unit_sequence_in_call_dispatch",\n  "fire_prevention_district",\n  "supervisor_district",\n  "row_id",\n  "latitude",\n  "longitude",\n  "neighborhood_name",\n  "location_geom"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Run San Francisco Street Trees Pipeline
    sf_street_trees = kubernetes_engine.GKEStartPodOperator(
        task_id="sf_street_trees",
        name="sf_street_trees",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="san-francisco",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.san_francisco.sf_street_trees.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.san_francisco.sf_street_trees.source_url }}",
            "CHUNKSIZE": "{{ var.json.san_francisco.sf_street_trees.chunksize }}",
            "SOURCE_FILE": "{{ var.json.san_francisco.sf_street_trees.source_file }}",
            "TARGET_FILE": "{{ var.json.san_francisco.sf_street_trees.target_file }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.san_francisco.sf_street_trees.dataset_id }}",
            "TABLE_ID": "{{ var.json.san_francisco.sf_street_trees.destination_table }}",
            "DROP_DEST_TABLE": "{{ var.json.san_francisco.sf_street_trees.drop_dest_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.san_francisco.sf_street_trees.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.san_francisco.sf_street_trees.schema_path }}",
            "HEADER_ROW_ORDINAL": "0",
            "INPUT_CSV_HEADERS": '[\n  "TreeID",\n  "qLegalStatus",\n  "qSpecies",\n  "qAddress",\n  "SiteOrder",\n  "qSiteInfo",\n  "PlantType",\n  "qCaretaker",\n  "qCareAssistant",\n  "PlantDate",\n  "DBH",\n  "PlotSize",\n  "PermitNotes",\n  "XCoord",\n  "YCoord",\n  "Latitude",\n  "Longitude",\n  "Location"\n]',
            "DATA_DTYPES": '{\n  "TreeID": "int64",\n  "qLegalStatus": "str",\n  "qSpecies": "str",\n  "qAddress": "str",\n  "SiteOrder": "str",\n  "qSiteInfo": "str",\n  "PlantType": "str",\n  "qCaretaker": "str",\n  "qCareAssistant": "str",\n  "PlantDate": "str",\n  "DBH": "str",\n  "PlotSize": "str",\n  "PermitNotes": "str",\n  "XCoord": "float64",\n  "YCoord": "float64",\n  "Latitude": "float64",\n  "Longitude": "float64",\n  "Location": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "TreeID" : "tree_id",\n  "qLegalStatus" : "legal_status",\n  "qSpecies" : "species",\n  "qAddress" : "address",\n  "SiteOrder" : "site_order",\n  "qSiteInfo" : "site_info",\n  "PlantType" : "plant_type",\n  "qCaretaker" : "care_taker",\n  "qCareAssistant" : "care_assistant",\n  "PlantDate" : "plant_date",\n  "DBH" : "dbh",\n  "PlotSize" : "plot_size",\n  "PermitNotes" : "permit_notes",\n  "XCoord" : "x_coordinate",\n  "YCoord" : "y_coordinate",\n  "Latitude" : "latitude",\n  "Longitude" : "longitude",\n  "Location" : "location"\n}',
            "DATE_FORMAT_LIST": '{\n  "plant_date": "%Y-%m-%d %H:%M:%S"\n}',
            "EMPTY_KEY_LIST": '[\n  "tree_id"\n]',
            "REORDER_HEADERS_LIST": '[\n  "tree_id",\n  "legal_status",\n  "species",\n  "address",\n  "site_order",\n  "site_info",\n  "plant_type",\n  "care_taker",\n  "care_assistant",\n  "plant_date",\n  "dbh",\n  "plot_size",\n  "permit_notes",\n  "x_coordinate",\n  "y_coordinate",\n  "latitude",\n  "longitude",\n  "location"\n]',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="san-francisco",
    )

    (
        create_cluster
        >> [
            sf_311_service_requests,
            sf_bikeshare_stations,
            sf_bikeshare_status,
            sf_bikeshare_trips,
            sf_film_locations,
            sffd_service_calls,
            sf_street_trees,
        ]
        >> delete_cluster
    )
