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
    transform_csv_ny_311_service_requests = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_ny_311_service_requests",
        name="311_service_requests",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_ny_311_service_requests }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.new_york.ny_311_service_requests.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.new_york.ny_311_service_requests.source_url }}",
            "CHUNKSIZE": "{{ var.json.new_york.ny_311_service_requests.chunksize }}",
            "SOURCE_FILE": "files/data_{{ var.json.new_york.ny_311_service_requests.dataset_id }}_{{ var.json.new_york.ny_311_service_requests.destination_table }}.csv",
            "TARGET_FILE": "files/data_output_{{ var.json.new_york.ny_311_service_requests.dataset_id }}_{{ var.json.new_york.ny_311_service_requests.destination_table }}.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.new_york.ny_311_service_requests.dataset_id }}",
            "TABLE_ID": "{{ var.json.new_york.ny_311_service_requests.destination_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york.ny_311_service_requests.target_path }}",
            "SCHEMA_PATH": "{{ var.json.new_york.ny_311_service_requests.schema_path }}",
            "DATA_DTYPES": '{\n  "Unique Key": "int",\n  "Created Date": "str",\n  "Closed Date": "str",\n  "Agency": "str",\n  "Agency Name": "str",\n  "Complaint Type": "str",\n  "Descriptor": "str",\n  "Location Type": "str",\n  "Incident Zip": "str",\n  "Incident Address": "str",\n  "Street Name": "str",\n  "Cross Street 1": "str",\n  "Cross Street 2": "str",\n  "Intersection Street 1": "str",\n  "Intersection Street 2": "str",\n  "Address Type": "str",\n  "City": "str",\n  "Landmark": "str",\n  "Facility Type": "str",\n  "Status": "str",\n  "Due Date": "str",\n  "Resolution Description": "str",\n  "Resolution Action Updated Date": "str",\n  "Community Board": "str",\n  "BBL": "str",\n  "Borough": "str",\n  "X Coordinate (State Plane)": "str",\n  "Y Coordinate (State Plane)": "str",\n  "Open Data Channel Type": "str",\n  "Park Facility Name": "str",\n  "Park Borough": "str",\n  "Vehicle Type": "str",\n  "Taxi Company Borough": "str",\n  "Taxi Pick Up Location": "str",\n  "Bridge Highway Name": "str",\n  "Bridge Highway Direction": "str",\n  "Road Ramp": "str",\n  "Bridge Highway Segment": "str",\n  "Latitude": "float64",\n  "Longitude": "float64",\n  "Location": "str"\n}',
            "PARSE_DATES": '[\n  "Created Date",\n  "Closed Date",\n  "Due Date",\n  "Resolution Action Updated Date"\n]',
            "NULL_ROWS_LIST": '[\n  "unique_key"\n]',
            "RENAME_HEADERS": '{\n  "Unique Key": "unique_key",\n  "Created Date": "created_date",\n  "Closed Date": "closed_date",\n  "Agency": "agency",\n  "Agency Name": "agency_name",\n  "Complaint Type": "complaint_type",\n  "Descriptor": "descriptor",\n  "Location Type": "location_type",\n  "Incident Zip": "incident_zip",\n  "Incident Address": "incident_address",\n  "Street Name": "street_name",\n  "Cross Street 1": "cross_street_1",\n  "Cross Street 2": "cross_street_2",\n  "Intersection Street 1": "intersection_street_1",\n  "Intersection Street 2": "intersection_street_2",\n  "Address Type": "address_type",\n  "City": "city",\n  "Landmark": "landmark",\n  "Facility Type": "facility_type",\n  "Status": "status",\n  "Due Date": "due_date",\n  "Resolution Description": "resolution_description",\n  "Resolution Action Updated Date": "resolution_action_updated_date",\n  "Community Board": "community_board",\n  "Open Data Channel Type": "open_data_channel_type",\n  "Borough": "borough",\n  "X Coordinate (State Plane)": "x_coordinate",\n  "Y Coordinate (State Plane)": "y_coordinate",\n  "Park Facility Name": "park_facility_name",\n  "Park Borough": "park_borough",\n  "Vehicle Type": "vehicle_type",\n  "Taxi Company Borough": "taxi_company_borough",\n  "Taxi Pick Up Location": "taxi_pickup_location",\n  "Bridge Highway Name": "bridge_highway_name",\n  "Bridge Highway Direction": "bridge_highway_direction",\n  "Road Ramp": "road_ramp",\n  "Bridge Highway Segment": "bridge_highway_segment",\n  "Latitude": "latitude",\n  "Longitude": "longitude",\n  "Location": "location",\n  "BBL": "bbl"\n}',
            "OUTPUT_CSV_HEADERS": '[\n  "unique_key",\n  "created_date",\n  "closed_date",\n  "agency",\n  "agency_name",\n  "complaint_type",\n  "descriptor",\n  "location_type",\n  "incident_zip",\n  "incident_address",\n  "street_name",\n  "cross_street_1",\n  "cross_street_2",\n  "intersection_street_1",\n  "intersection_street_2",\n  "address_type",\n  "city",\n  "landmark",\n  "facility_type",\n  "status",\n  "due_date",\n  "resolution_description",\n  "resolution_action_updated_date",\n  "community_board",\n  "borough",\n  "x_coordinate",\n  "y_coordinate",\n  "park_facility_name",\n  "park_borough",\n  "bbl",\n  "open_data_channel_type",\n  "vehicle_type",\n  "taxi_company_borough",\n  "taxi_pickup_location",\n  "bridge_highway_name",\n  "bridge_highway_direction",\n  "road_ramp",\n  "bridge_highway_segment",\n  "latitude",\n  "longitude",\n  "location"\n]',
        },
        resources={"request_ephemeral_storage": "32G", "limit_cpu": "3"},
    )

    # Run New York Citibike Stations Pipeline
    transform_csv_ny_citibike_stations = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_ny_citibike_stations",
        name="citibike_stations",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_citibike_stations }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.new_york.citibike_stations.pipeline_name }}",
            "SOURCE_URL_STATIONS_JSON": "{{ var.json.new_york.citibike_stations.source_url_stations }}",
            "SOURCE_URL_STATUS_JSON": "{{ var.json.new_york.citibike_stations.source_url_status }}",
            "CHUNKSIZE": "{{ var.json.new_york.citibike_stations.chunksize }}",
            "SOURCE_FILE": "files/data_{{ var.json.new_york.citibike_stations.dataset_id }}_{{ var.json.new_york.citibike_stations.destination_table }}.csv",
            "TARGET_FILE": "files/data_output_{{ var.json.new_york.citibike_stations.dataset_id }}_{{ var.json.new_york.citibike_stations.destination_table }}.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.new_york.citibike_stations.dataset_id }}",
            "TABLE_ID": "{{ var.json.new_york.citibike_stations.destination_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york.citibike_stations.target_path }}",
            "SCHEMA_PATH": "{{ var.json.new_york.citibike_stations.schema_path }}",
            "DATA_DTYPES": '{\n  "rental_uris": "str",\n  "lat": "float64",\n  "eightd_station_services": "str",\n  "legacy_id_x": "int64",\n  "short_name": "str",\n  "external_id": "str",\n  "station_id": "int64",\n  "rental_methods": "str",\n  "station_type": "str",\n  "short_name": "str",\n  "eightd_has_key_dispenser": "bool",\n  "electric_bike_surcharge_waiver": "bool",\n  "lon": "float64",\n  "has_kiosk": "bool",\n  "capacity": "int64",\n  "region_id": "int64",\n  "is_installed": "bool",\n  "num_docks_available": "int64",\n  "num_docks_disabled": "int64",\n  "num_bikes_disabled": "int64",\n  "num_bikes_available": "int64",\n  "station_status": "str",\n  "last_reported": "int64",\n  "eightd_has_available_keys": "bool",\n  "num_ebikes_available": "int64",\n  "is_returning": "int64",\n  "is_renting": "int64",\n  "legacy_id_y": "int64",\n  "valet": "str",\n  "eightd_active_station_services": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "lat": "latitude",\n  "lon": "longitude"\n}',
            "BOOLEAN_DATAPOINTS": '[\n  "eightd_has_key_dispenser",\n  "is_installed",\n  "is_renting",\n  "is_returning"\n]',
            "DATETIME_FIELDLIST": '[\n  "last_reported"\n]',
            "RESOLVE_DATATYPES_LIST": '{\n  "station_id": "Int64",\n  "region_id": "Int64",\n  "rental_methods": "string"\n}',
            "NORMALIZE_DATA_LIST": '[\n  "rental_methods"\n]',
            "INPUT_CSV_HEADERS": '[\n  "rental_uris",\n  "lat",\n  "eightd_station_services",\n  "legacy_id_x",\n  "short_name",\n  "external_id",\n  "station_id",\n  "rental_methods",\n  "station_type",\n  "short_name",\n  "eightd_has_key_dispenser",\n  "electric_bike_surcharge_waiver",\n  "lon",\n  "has_kiosk",\n  "capacity",\n  "region_id",\n  "is_installed",\n  "num_docks_available",\n  "num_docks_disabled",\n  "num_bikes_disabled",\n  "num_bikes_available",\n  "station_status",\n  "last_reported",\n  "eightd_has_available_keys",\n  "num_ebikes_available",\n  "is_returning",\n  "is_renting",\n  "legacy_id_y",\n  "valet",\n  "eightd_active_station_services"\n]',
            "OUTPUT_CSV_HEADERS": '[\n  "station_id",\n  "name",\n  "short_name",\n  "latitude",\n  "longitude",\n  "region_id",\n  "rental_methods",\n  "capacity",\n  "eightd_has_key_dispenser",\n  "num_bikes_available",\n  "num_bikes_disabled",\n  "num_docks_available",\n  "num_docks_disabled",\n  "is_installed",\n  "is_renting",\n  "is_returning",\n  "eightd_has_available_keys",\n  "last_reported"\n]',
        },
        resources={"request_ephemeral_storage": "16G", "limit_cpu": "3"},
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
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_nypd_mv_collisions }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.new_york.nypd_mv_collisions.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.new_york.nypd_mv_collisions.source_url }}",
            "CHUNKSIZE": "{{ var.json.new_york.nypd_mv_collisions.chunksize }}",
            "SOURCE_FILE": "files/data_{{ var.json.new_york.nypd_mv_collisions.dataset_id }}_{{ var.json.new_york.nypd_mv_collisions.destination_table }}.csv",
            "TARGET_FILE": "files/data_output_{{ var.json.new_york.nypd_mv_collisions.dataset_id }}_{{ var.json.new_york.nypd_mv_collisions.destination_table }}.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.new_york.nypd_mv_collisions.dataset_id }}",
            "TABLE_ID": "{{ var.json.new_york.nypd_mv_collisions.destination_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york.nypd_mv_collisions.target_path }}",
            "SCHEMA_PATH": "{{ var.json.new_york.nypd_mv_collisions.schema_path }}",
            "DATA_DTYPES": '{\n  "CRASH DATE": "str",\n  "CRASH TIME": "str",\n  "BOROUGH": "str",\n  "ZIP CODE": "str",\n  "LATITUDE": "float64",\n  "LONGITUDE": "float64",\n  "LOCATION": "str",\n  "ON STREET NAME": "str",\n  "CROSS STREET NAME": "str",\n  "OFF STREET NAME": "str",\n  "NUMBER OF PERSONS INJURED": "str",\n  "NUMBER OF PERSONS KILLED" : "str",\n  "NUMBER OF PEDESTRIANS INJURED" : "str",\n  "NUMBER OF PEDESTRIANS KILLED" : "str",\n  "NUMBER OF CYCLIST INJURED" : "str",\n  "NUMBER OF CYCLIST KILLED" : "str",\n  "NUMBER OF MOTORIST INJURED" : "str",\n  "NUMBER OF MOTORIST KILLED" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 1" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 2" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 3" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 4" : "str",\n  "CONTRIBUTING FACTOR VEHICLE 5" : "str",\n  "COLLISION_ID": "int64",\n  "VEHICLE TYPE CODE 1" : "str",\n  "VEHICLE TYPE CODE 2" : "str",\n  "VEHICLE TYPE CODE 3" : "str",\n  "VEHICLE TYPE CODE 4" : "str",\n  "VEHICLE TYPE CODE 5": "str"\n}',
            "RESOLVE_DATATYPES_LIST": '{\n  "latitude": "float64",\n  "longitude": "float64",\n  "number_of_cyclist_injured": "int64",\n  "number_of_cyclist_killed": "int64",\n  "number_of_motorist_injured": "int64",\n  "number_of_motorist_killed": "int64",\n  "number_of_pedestrians_injured": "int64",\n  "number_of_pedestrians_killed": "int64",\n  "number_of_persons_injured": "int64",\n  "number_of_persons_killed": "int64"\n}',
            "TRANSFORM_LIST": '[ "replace_regex", "add_crash_timestamp", "convert_date_format", "rename_headers", "resolve_datatypes", "reorder_headers" ]',
            "REGEX_LIST": '[\n  [ "OFF STREET NAME", "\\\\n", " " ]\n]',
            "DATE_FORMAT_LIST": '[\n  ["timestamp", "%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]\n]',
            "CRASH_FIELD_LIST": '[ [ "timestamp", "CRASH DATE", "CRASH TIME" ] ]',
            "RENAME_HEADERS_LIST": '{\n  "BOROUGH": "borough",\n  "CONTRIBUTING FACTOR VEHICLE 1": "contributing_factor_vehicle_1",\n  "CONTRIBUTING FACTOR VEHICLE 2": "contributing_factor_vehicle_2",\n  "CONTRIBUTING FACTOR VEHICLE 3": "contributing_factor_vehicle_3",\n  "CONTRIBUTING FACTOR VEHICLE 4": "contributing_factor_vehicle_4",\n  "CONTRIBUTING FACTOR VEHICLE 5": "contributing_factor_vehicle_5",\n  "CROSS STREET NAME": "cross_street_name",\n  "LATITUDE": "latitude",\n  "LONGITUDE": "longitude",\n  "LOCATION": "location",\n  "NUMBER OF CYCLIST INJURED": "number_of_cyclist_injured",\n  "NUMBER OF CYCLIST KILLED": "number_of_cyclist_killed",\n  "NUMBER OF MOTORIST INJURED": "number_of_motorist_injured",\n  "NUMBER OF MOTORIST KILLED": "number_of_motorist_killed",\n  "NUMBER OF PEDESTRIANS INJURED": "number_of_pedestrians_injured",\n  "NUMBER OF PEDESTRIANS KILLED": "number_of_pedestrians_killed",\n  "NUMBER OF PERSONS INJURED": "number_of_persons_injured",\n  "NUMBER OF PERSONS KILLED": "number_of_persons_killed",\n  "OFF STREET NAME": "off_street_name",\n  "ON STREET NAME": "on_street_name",\n  "COLLISION_ID": "unique_key",\n  "VEHICLE TYPE CODE 1": "vehicle_type_code1",\n  "VEHICLE TYPE CODE 2": "vehicle_type_code2",\n  "VEHICLE TYPE CODE 3": "vehicle_type_code_3",\n  "VEHICLE TYPE CODE 4": "vehicle_type_code_4",\n  "VEHICLE TYPE CODE 5": "vehicle_type_code_5",\n  "ZIP CODE": "zip_code"\n}',
            "REORDER_HEADERS_LIST": '[\n  "borough",\n  "contributing_factor_vehicle_1",\n  "contributing_factor_vehicle_2",\n  "contributing_factor_vehicle_3",\n  "contributing_factor_vehicle_4",\n  "contributing_factor_vehicle_5",\n  "cross_street_name",\n  "timestamp",\n  "latitude",\n  "longitude",\n  "location",\n  "number_of_cyclist_injured",\n  "number_of_cyclist_killed",\n  "number_of_motorist_injured",\n  "number_of_motorist_killed",\n  "number_of_pedestrians_injured",\n  "number_of_pedestrians_killed",\n  "number_of_persons_injured",\n  "number_of_persons_killed",\n  "off_street_name",\n  "on_street_name",\n  "unique_key",\n  "vehicle_type_code1",\n  "vehicle_type_code2",\n  "vehicle_type_code_3",\n  "vehicle_type_code_4",\n  "vehicle_type_code_5",\n  "zip_code"\n]',
        },
        resources={"request_ephemeral_storage": "16G", "limit_cpu": "3"},
    )

    # Run New York Tree Census 1995 Pipeline
    transform_csv_ny_tree_census_1995 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_ny_tree_census_1995",
        name="tree_census_1995",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_tree_census_1995 }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.new_york.tree_census_1995.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.new_york.tree_census_1995.source_url }}",
            "CHUNKSIZE": "{{ var.json.new_york.tree_census_1995.chunksize }}",
            "SOURCE_FILE": "files/data_{{ var.json.new_york.tree_census_1995.dataset_id }}_{{ var.json.new_york.tree_census_1995.destination_table }}.csv",
            "TARGET_FILE": "files/data_output_{{ var.json.new_york.tree_census_1995.dataset_id }}_{{ var.json.new_york.tree_census_1995.destination_table }}.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.new_york.tree_census_1995.dataset_id }}",
            "TABLE_ID": "{{ var.json.new_york.tree_census_1995.destination_table }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york.tree_census_1995.target_path }}",
            "SCHEMA_PATH": "{{ var.json.new_york.tree_census_1995.schema_path }}",
            "RENAME_HEADERS_LIST": '{\n  "RecordId": "recordid",\n  "Address": "address",\n  "House_Number": "house_number",\n  "Street": "street",\n  "Postcode_Original": "zip_original",\n  "Community Board_Original": "cb_original",\n  "Site": "site",\n  "Species": "species",\n  "Diameter": "diameter",\n  "Condition": "status",\n  "Wires": "wires",\n  "Sidewalk_Condition": "sidewalk_condition",\n  "Support_Structure": "support_structure",\n  "Borough": "borough",\n  "X": "x",\n  "Y": "y",\n  "Longitude": "longitude",\n  "Latitude": "latitude",\n  "CB_New": "cb_new",\n  "Zip_New": "zip_new",\n  "CensusTract_2010": "censustract_2010",\n  "CensusBlock_2010": "censusblock_2010",\n  "NTA_2010": "nta_2010",\n  "SegmentID": "segmentid",\n  "Spc_Common": "spc_common",\n  "Spc_Latin": "spc_latin",\n  "Location": "location"\n}',
            "REMOVE_WHITESPACE_LIST": '[\n  "spc_latin"\n]',
            "REORDER_HEADERS_LIST": '[\n  "recordid",\n  "address",\n  "house_number",\n  "street",\n  "zip_original",\n  "cb_original",\n  "site",\n  "species",\n  "diameter",\n  "status",\n  "wires",\n  "sidewalk_condition",\n  "support_structure",\n  "borough",\n  "x",\n  "y",\n  "longitude",\n  "latitude",\n  "cb_new",\n  "zip_new",\n  "censustract_2010",\n  "censusblock_2010",\n  "nta_2010",\n  "segmentid",\n  "spc_common",\n  "spc_latin",\n  "location"\n]',
        },
        resources={"request_ephemeral_storage": "16G", "limit_cpu": "3"},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="new-york",
    )

    (
        create_cluster
        >> [
            transform_csv_nypd_mv_collisions,
            transform_csv_ny_citibike_stations,
            transform_csv_ny_tree_census_1995,
            transform_csv_ny_311_service_requests,
        ]
        >> delete_cluster
    )
