# Copyright 2022 Google LLC
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

    # Run New York 311 Service Requests Pipeline
    sf_311_service_requests = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_311_service_requests",
        name="sf_311_service_requests",
        startup_timeout_seconds=600,
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco 311 Service Requests",
            "SOURCE_URL": "https://data.sfgov.org/api/views/vw6y-z8j6/rows.csv",
            "CHUNKSIZE": "1000000",
            "SOURCE_FILE": "files/data_311_service_requests.csv",
            "TARGET_FILE": "files/data_output_311_service_requests.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_311",
            "TABLE_ID": "311_service_requests",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/311_service_requests/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_311_service_requests_schema.json",
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
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Municipal Calendar Pipeline
    sf_calendar = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_calendar",
        name="calendar",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Municipal Calendar",
            "SOURCE_URL_DICT": '{\n  "calendar": "gs://pdp-feeds-staging/SF_Muni/GTFSTransitData_SF/calendar.csv",\n  "calendar_attributes": "gs://pdp-feeds-staging/SF_Muni/GTFSTransitData_SF/calendar_attributes.csv",\n  "calendar_dates": "gs://pdp-feeds-staging/SF_Muni/GTFSTransitData_SF/calendar_dates.csv"\n}',
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_municipal_calendar.csv",
            "TARGET_FILE": "files/data_output_municipal_calendar.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_transit_muni",
            "TABLE_ID": "calendar",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/transit_municipal_calendar/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_calendar_schema.json",
            "REORDER_HEADERS_LIST": '[\n  "service_id", "service_desc",\n  "monday", "tuesday", "wednesday",\n  "thursday", "friday", "saturday", "sunday",\n  "exceptions", "exception_type"\n]',
            "RENAME_HEADERS_LIST": '{\n    "monday_str": "monday",\n    "tuesday_str": "tuesday",\n    "wednesday_str": "wednesday",\n    "thursday_str": "thursday",\n    "friday_str": "friday",\n    "saturday_str": "saturday",\n    "sunday_str": "sunday",\n    "service_description": "service_desc",\n    "date": "exceptions",\n    "exception_type_str": "exception_type"\n}',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Municipal Routes Pipeline
    sf_muni_routes = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_muni_routes",
        name="muni_routes",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Municipal Routes",
            "SOURCE_URL_DICT": '{\n  "routes": "gs://pdp-feeds-staging/SF_Muni/GTFSTransitData_SF/routes.txt"\n}',
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_municipal_routes.csv",
            "TARGET_FILE": "files/data_output_municipal_routes.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_transit_muni",
            "TABLE_ID": "routes",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/transit_municipal_routes/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_muni_routes_schema.json",
            "REORDER_HEADERS_LIST": '[\n  "route_id",\n  "route_short_name",\n  "route_long_name",\n  "route_type"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Municipal Shapes Pipeline
    sf_muni_shapes = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_muni_shapes",
        name="muni_shapes",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Municipal Shapes",
            "SOURCE_URL_DICT": '{\n  "shapes": "gs://pdp-feeds-staging/SF_Muni/GTFSTransitData_SF/shapes.txt"\n}',
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_municipal_shapes.csv",
            "TARGET_FILE": "files/data_output_municipal_shapes.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_transit_muni",
            "TABLE_ID": "shapes",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/transit_municipal_shapes/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_muni_shapes_schema.json",
            "RENAME_HEADERS_LIST": '{\n  "shape_pt_lon": "shape_point_lon",\n  "shape_pt_lat": "shape_point_lat",\n  "shape_pt_sequence": "shape_point_sequence",\n  "shape_dist_traveled": "shape_distance_traveled"\n}',
            "REORDER_HEADERS_LIST": '[\n  "shape_id",\n  "shape_point_sequence",\n  "shape_point_lat",\n  "shape_point_lon",\n  "shape_point_geom",\n  "shape_distance_traveled"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Municipal Stops Pipeline
    sf_muni_stops = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_muni_stops",
        name="muni_stops",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Municipal Stops",
            "SOURCE_URL_DICT": '{\n  "stops": "gs://pdp-feeds-staging/SF_Muni/GTFSTransitData_SF/stops.txt"\n}',
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_municipal_stops.csv",
            "TARGET_FILE": "files/data_output_municipal_stops.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_transit_muni",
            "TABLE_ID": "stops",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/transit_municipal_stops/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_muni_stops_schema.json",
            "REORDER_HEADERS_LIST": '[\n  "stop_id",\n  "stop_name",\n  "stop_lat",\n  "stop_lon",\n  "stop_geom"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Police Department Incidents Pipeline
    sfpd_incidents = kubernetes_pod.KubernetesPodOperator(
        task_id="sfpd_incidents",
        name="sfpd_incidents",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Police Department Incidents",
            "SOURCE_URL_DICT": '{\n  "sfpd_incidents": "https://data.sfgov.org/api/views/tmnf-yvry/rows.csv"\n}',
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_sfpd_incidents.csv",
            "TARGET_FILE": "files/data_output_sfpd_incidents.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_sfpd_incidents",
            "TABLE_ID": "sfpd_incidents",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/sfpd_incidents/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_sfpd_incidents_schema.json",
            "HEADER_ROW_ORDINAL": "0",
            "EMPTY_KEY_LIST": '[\n  "unique_key"\n]',
            "DATE_FORMAT_LIST": '{\n  "Date": "%Y-%m-%d %H:%M:%S"\n}',
            "RENAME_HEADERS_LIST": '{\n  "IncidntNum": "unique_key",\n  "Category": "category",\n  "Descript": "descript",\n  "DayOfWeek": "dayofweek",\n  "PdDistrict": "pddistrict",\n  "Resolution": "resolution",\n  "Address": "address",\n  "X": "longitude",\n  "Y": "latitude",\n  "Location": "location",\n  "PdId": "pdid",\n  "Date": "Date",\n  "Time": "Time"\n}',
            "REORDER_HEADERS_LIST": '[\n  "unique_key",\n  "category",\n  "descript",\n  "dayofweek",\n  "pddistrict",\n  "resolution",\n  "address",\n  "longitude",\n  "latitude",\n  "location",\n  "pdid",\n  "timestamp"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Bikeshare Stations Pipeline
    sf_bikeshare_stations = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_bikeshare_stations",
        name="bikeshare_stations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Bikeshare Stations",
            "SOURCE_URL": "https://gbfs.baywheels.com/gbfs/fr/station_information",
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_bikeshare_station_info.csv",
            "TARGET_FILE": "files/data_output_bikeshare_station_info.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_bikeshare",
            "TABLE_ID": "bikeshare_station_info",
            "DROP_DEST_TABLE": "Y",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/bikeshare_stations/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_bikeshare_station_info_schema.json",
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
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Bikeshare Status Pipeline
    sf_bikeshare_status = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_bikeshare_status",
        name="bikeshare_status",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Bikeshare Station Status",
            "SOURCE_URL": "https://gbfs.baywheels.com/gbfs/en/station_status",
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_bikeshare_status.csv",
            "TARGET_FILE": "files/data_output_bikeshare_status.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_bikeshare",
            "TABLE_ID": "bikeshare_station_status",
            "DROP_DEST_TABLE": "Y",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/bikeshare_status/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_bikeshare_station_status_schema.json",
            "HEADER_ROW_ORDINAL": "0",
            "RENAME_HEADERS_LIST": '{\n  "data.stations.eightd_has_available_keys": "eightd_has_available_keys",\n  "data.stations.is_installed": "is_installed",\n  "data.stations.is_renting": "is_renting",\n  "data.stations.is_returning": "is_returning",\n  "data.stations.last_reported": "last_reported",\n  "data.stations.num_bikes_available": "num_bikes_available",\n  "data.stations.num_bikes_disabled": "num_bikes_disabled",\n  "data.stations.num_docks_available": "num_docks_available",\n  "data.stations.num_docks_disabled": "num_docks_disabled",\n  "data.stations.num_ebikes_available": "num_ebikes_available",\n  "data.stations.station_id": "station_id"\n}',
            "EMPTY_KEY_LIST": '[\n  "station_id",\n  "num_bikes_available",\n  "num_docks_available",\n  "is_installed",\n  "is_renting",\n  "is_returning",\n  "last_reported"\n]',
            "REORDER_HEADERS_LIST": '[\n  "station_id",\n  "num_bikes_available",\n  "num_bikes_disabled",\n  "num_docks_available",\n  "num_docks_disabled",\n  "is_installed",\n  "is_renting",\n  "is_returning",\n  "last_reported",\n  "num_ebikes_available",\n  "eightd_has_available_keys"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Bikeshare Trips Pipeline
    sf_bikeshare_trips = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_bikeshare_trips",
        name="sf_bikeshare_trips",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Bikeshare Trips",
            "SOURCE_URL_LIST": '[\n  "https://s3.amazonaws.com/fordgobike-data/201803-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/201804-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/201802-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/201801-fordgobike-tripdata.csv.zip",\n  "https://s3.amazonaws.com/fordgobike-data/2017-fordgobike-tripdata.csv",\n  "https://s3.amazonaws.com/babs-open-data/babs_open_data_year_1.zip",\n  "https://s3.amazonaws.com/babs-open-data/babs_open_data_year_2.zip",\n  "https://s3.amazonaws.com/babs-open-data/babs_open_data_year_3.zip"\n]',
            "CHUNKSIZE": "1000000",
            "SOURCE_FILE": "files/data_bikeshare_trips.csv",
            "TARGET_FILE": "files/data_output_bikeshare_trips.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_bikeshare",
            "TABLE_ID": "bikeshare_trips",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/bikeshare_trips/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_bikeshare_trips_schema.json",
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
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Film Locations Pipeline
    sf_film_locations = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_film_locations",
        name="sf_film_locations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Film Locations",
            "SOURCE_URL": "https://data.sfgov.org/api/views/yitu-d5am/rows.csv",
            "CHUNKSIZE": "1000000",
            "SOURCE_FILE": "files/data_film_locations.csv",
            "TARGET_FILE": "files/data_output_film_locations.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_film_locations",
            "TABLE_ID": "film_locations",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/film_locations/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_film_locations_schema.json",
            "HEADER_ROW_ORDINAL": "0",
            "RENAME_HEADERS_LIST": '{\n  "Title": "title",\n  "Release Year": "release_year",\n  "Locations": "locations",\n  "Fun Facts": "fun_facts",\n  "Production Company": "production_company",\n  "Distributor": "distributor",\n  "Director": "director",\n  "Writer": "writer",\n  "Actor 1": "actor_1",\n  "Actor 2": "actor_2",\n  "Actor 3": "actor_3"\n}',
            "STRIP_WHITESPACE_LIST": '[\n  "distributor",\n  "director",\n  "actor_2"\n]',
            "STRIP_NEWLINES_LIST": '[\n  "production_company",\n  "fun_facts"\n]',
            "REORDER_HEADERS_LIST": '[\n  "title",\n  "release_year",\n  "locations",\n  "fun_facts",\n  "production_company",\n  "distributor",\n  "director",\n  "writer",\n  "actor_1",\n  "actor_2",\n  "actor_3"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Fire Department Service Calls Pipeline
    sffd_service_calls = kubernetes_pod.KubernetesPodOperator(
        task_id="sffd_service_calls",
        name="sffd_service_calls",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Fire Department Service Calls",
            "SOURCE_URL": "https://data.sfgov.org/api/views/nuek-vuh3/rows.csv",
            "CHUNKSIZE": "1000000",
            "SOURCE_FILE": "files/data_sffd_service_calls.csv",
            "TARGET_FILE": "files/data_output_sffd_service_calls.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_sffd_service_calls",
            "TABLE_ID": "sffd_service_calls",
            "DROP_DEST_TABLE": "Y",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/sffd_service_calls/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_sffd_service_calls_schema.json",
            "HEADER_ROW_ORDINAL": "0",
            "INPUT_CSV_HEADERS": '[\n  "Call Number",\n  "Unit ID",\n  "Incident Number",\n  "Call Type",\n  "Call Date",\n  "Watch Date",\n  "Received DtTm",\n  "Entry DtTm",\n  "Dispatch DtTm",\n  "Response DtTm",\n  "On Scene DtTm",\n  "Transport DtTm",\n  "Hospital DtTm",\n  "Call Final Disposition",\n  "Available DtTm",\n  "Address",\n  "City",\n  "Zipcode of Incident",\n  "Battalion",\n  "Station Area",\n  "Box",\n  "Original Priority",\n  "Priority",\n  "Final Priority",\n  "ALS Unit",\n  "Call Type Group",\n  "Number of Alarms",\n  "Unit Type",\n  "Unit sequence in call dispatch",\n  "Fire Prevention District",\n  "Supervisor District",\n  "Neighborhooods - Analysis Boundaries",\n  "RowID",\n  "case_location"\n]',
            "DATA_DTYPES": '{\n  "Call Number": "int64",\n  "Unit ID": "str",\n  "Incident Number": "int64",\n  "Call Type": "str",\n  "Call Date": "str",\n  "Watch Date": "str",\n  "Received DtTm": "str",\n  "Entry DtTm": "str",\n  "Dispatch DtTm": "str",\n  "Response DtTm": "str",\n  "On Scene DtTm": "str",\n  "Transport DtTm": "str",\n  "Hospital DtTm": "str",\n  "Call Final Disposition": "str",\n  "Available DtTm": "str",\n  "Address": "str",\n  "City": "str",\n  "Zipcode of Incident": "str",\n  "Battalion": "str",\n  "Station Area": "str",\n  "Box": "str",\n  "Original Priority": "str",\n  "Priority": "str",\n  "Final Priority": "int64",\n  "ALS Unit": "str",\n  "Call Type Group": "str",\n  "Number of Alarms": "str",\n  "Unit Type": "str",\n  "Unit sequence in call dispatch": "str",\n  "Fire Prevention District": "str",\n  "Supervisor District": "str",\n  "Neighborhooods - Analysis Boundaries": "str",\n  "RowID": "str",\n  "case_location": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Call Number": "call_number",\n  "Unit ID": "unit_id",\n  "Incident Number": "incident_number",\n  "Call Type": "call_type",\n  "Call Date": "call_date",\n  "Watch Date": "watch_date",\n  "Received DtTm": "received_timestamp",\n  "Entry DtTm": "entry_timestamp",\n  "Dispatch DtTm": "dispatch_timestamp",\n  "Response DtTm": "response_timestamp",\n  "On Scene DtTm": "on_scene_timestamp",\n  "Transport DtTm": "transport_timestamp",\n  "Hospital DtTm": "hospital_timestamp",\n  "Call Final Disposition": "call_final_disposition",\n  "Available DtTm": "available_timestamp",\n  "Address": "address",\n  "City": "city",\n  "Zipcode of Incident": "zipcode_of_incident",\n  "Battalion": "battalion",\n  "Station Area": "station_area",\n  "Box": "box",\n  "Original Priority": "original_priority",\n  "Priority": "priority",\n  "Final Priority": "final_priority",\n  "ALS Unit": "als_unit",\n  "Call Type Group": "call_type_group",\n  "Number of Alarms": "number_of_alarms",\n  "Unit Type": "unit_type",\n  "Unit sequence in call dispatch": "unit_sequence_in_call_dispatch",\n  "Fire Prevention District": "fire_prevention_district",\n  "Supervisor District": "supervisor_district",\n  "Neighborhooods - Analysis Boundaries": "neighborhood_name",\n  "RowID": "row_id",\n  "case_location": "location_geom"\n}',
            "DATE_FORMAT_LIST": '{\n  "call_date": "%Y-%m-%d",\n  "watch_date": "%Y-%m-%d",\n  "available_timestamp": "%Y-%m-%d %H:%M:%S",\n  "dispatch_timestamp": "%Y-%m-%d %H:%M:%S",\n  "entry_timestamp": "%Y-%m-%d %H:%M:%S",\n  "on_scene_timestamp": "%Y-%m-%d %H:%M:%S",\n  "received_timestamp": "%Y-%m-%d %H:%M:%S",\n  "response_timestamp": "%Y-%m-%d %H:%M:%S",\n  "transport_timestamp": "%Y-%m-%d %H:%M:%S",\n  "hospital_timestamp": "%Y-%m-%d %H:%M:%S"\n}',
            "REORDER_HEADERS_LIST": '[\n  "call_number",\n  "unit_id",\n  "incident_number",\n  "call_type",\n  "call_date",\n  "watch_date",\n  "received_timestamp",\n  "entry_timestamp",\n  "dispatch_timestamp",\n  "response_timestamp",\n  "on_scene_timestamp",\n  "transport_timestamp",\n  "hospital_timestamp",\n  "call_final_disposition",\n  "available_timestamp",\n  "address",\n  "city",\n  "zipcode_of_incident",\n  "battalion",\n  "station_area",\n  "box",\n  "original_priority",\n  "priority",\n  "final_priority",\n  "als_unit",\n  "call_type_group",\n  "number_of_alarms",\n  "unit_type",\n  "unit_sequence_in_call_dispatch",\n  "fire_prevention_district",\n  "supervisor_district",\n  "row_id",\n  "latitude",\n  "longitude",\n  "neighborhood_name",\n  "location_geom"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run San Francisco Street Trees Pipeline
    sf_street_trees = kubernetes_pod.KubernetesPodOperator(
        task_id="sf_street_trees",
        name="sf_street_trees",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "San Francisco Street Trees",
            "SOURCE_URL": "https://data.sfgov.org/api/views/tkzw-k3nq/rows.csv",
            "CHUNKSIZE": "1000000",
            "SOURCE_FILE": "files/data_sf_street_trees.csv",
            "TARGET_FILE": "files/data_output_sf_street_trees.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "san_francisco_trees",
            "TABLE_ID": "street_trees",
            "DROP_DEST_TABLE": "N",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco/sf_street_trees/data_output.csv",
            "SCHEMA_PATH": "data/san_francisco/schema/sf_street_trees_schema.json",
            "HEADER_ROW_ORDINAL": "0",
            "INPUT_CSV_HEADERS": '[\n  "TreeID",\n  "qLegalStatus",\n  "qSpecies",\n  "qAddress",\n  "SiteOrder",\n  "qSiteInfo",\n  "PlantType",\n  "qCaretaker",\n  "qCareAssistant",\n  "PlantDate",\n  "DBH",\n  "PlotSize",\n  "PermitNotes",\n  "XCoord",\n  "YCoord",\n  "Latitude",\n  "Longitude",\n  "Location"\n]',
            "DATA_DTYPES": '{\n  "TreeID": "int64",\n  "qLegalStatus": "str",\n  "qSpecies": "str",\n  "qAddress": "str",\n  "SiteOrder": "str",\n  "qSiteInfo": "str",\n  "PlantType": "str",\n  "qCaretaker": "str",\n  "qCareAssistant": "str",\n  "PlantDate": "str",\n  "DBH": "str",\n  "PlotSize": "str",\n  "PermitNotes": "str",\n  "XCoord": "float64",\n  "YCoord": "float64",\n  "Latitude": "float64",\n  "Longitude": "float64",\n  "Location": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "TreeID" : "tree_id",\n  "qLegalStatus" : "legal_status",\n  "qSpecies" : "species",\n  "qAddress" : "address",\n  "SiteOrder" : "site_order",\n  "qSiteInfo" : "site_info",\n  "PlantType" : "plant_type",\n  "qCaretaker" : "care_taker",\n  "qCareAssistant" : "care_assistant",\n  "PlantDate" : "plant_date",\n  "DBH" : "dbh",\n  "PlotSize" : "plot_size",\n  "PermitNotes" : "permit_notes",\n  "XCoord" : "x_coordinate",\n  "YCoord" : "y_coordinate",\n  "Latitude" : "latitude",\n  "Longitude" : "longitude",\n  "Location" : "location"\n}',
            "DATE_FORMAT_LIST": '{\n  "plant_date": "%Y-%m-%d %H:%M:%S"\n}',
            "EMPTY_KEY_LIST": '[\n  "tree_id"\n]',
            "REORDER_HEADERS_LIST": '[\n  "tree_id",\n  "legal_status",\n  "species",\n  "address",\n  "site_order",\n  "site_info",\n  "plant_type",\n  "care_taker",\n  "care_assistant",\n  "plant_date",\n  "dbh",\n  "plot_size",\n  "permit_notes",\n  "x_coordinate",\n  "y_coordinate",\n  "latitude",\n  "longitude",\n  "location"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    (
        [sf_bikeshare_stations, sf_bikeshare_status, sf_film_locations, sf_street_trees]
        >> sf_bikeshare_trips
        >> [sf_calendar, sf_muni_routes, sf_muni_shapes, sf_muni_stops]
        >> sffd_service_calls
        >> sfpd_incidents
        >> sf_311_service_requests
    )
