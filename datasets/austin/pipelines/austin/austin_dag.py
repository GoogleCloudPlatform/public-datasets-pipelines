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
    dag_id="austin.austin",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    austin_311_service_requests = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_311_service_requests",
        name="austin",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Austin 311 Service Requests By Year",
            "SOURCE_URL": "https://data.austintexas.gov/api/views/xwdj-i9he/rows.csv",
            "CHUNKSIZE": "750000",
            "SOURCE_FILE": "files/data_austin_311_service_requests.csv",
            "TARGET_FILE": "files/data_output_austin_311_service_requests.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin_311/311_service_requests/data_output.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "austin_311",
            "DESTINATION_TABLE": "311_service_requests",
            "SCHEMA_PATH": "data/austin_311/schema/austin_311_service_requests_schema.json",
            "DATE_FORMAT_LIST": '{\n  "status_change_date": "%Y-%m-%d %H:%M:%S",\n  "created_date": "%Y-%m-%d %H:%M:%S",\n  "last_update_date": "%Y-%m-%d %H:%M:%S",\n  "close_date": "%Y-%m-%d %H:%M:%S"\n}',
            "INT_COLS_LIST": '[\n  "council_district_code"\n]',
            "REMOVE_NEWLINES_COLS_LIST": '[\n  "location"\n]',
            "NULL_ROWS_LIST": '[\n  "unique_key"\n]',
            "INPUT_CSV_HEADERS": '[\n  "Service Request (SR) Number",\n  "SR Description",\n  "Method Received",\n  "SR Status",\n  "Status Change Date",\n  "Created Date",\n  "Last Update Date",\n  "Close Date",\n  "SR Location",\n  "Street Number",\n  "Street Name",\n  "City",\n  "Zip Code",\n  "County",\n  "State Plane X Coordinate",\n  "State Plane Y Coordinate",\n  "Latitude Coordinate",\n  "Longitude Coordinate",\n  "(Latitude.Longitude)",\n  "Council District",\n  "Map Page",\n  "Map Tile"\n]',
            "DATA_DTYPES": '{\n  "Service Request (SR) Number": "str",\n  "SR Description": "str",\n  "Method Received": "str",\n  "SR Status": "str",\n  "Status Change Date": "datetime64",\n  "Created Date": "datetime64",\n  "Last Update Date": "datetime64",\n  "Close Date": "datetime64",\n  "SR Location": "str",\n  "Street Number": "str",\n  "Street Name": "str",\n  "City": "str",\n  "Zip Code": "str",\n  "County": "str",\n  "State Plane X Coordinate": "float",\n  "State Plane Y Coordinate": "float",\n  "Latitude Coordinate": "float",\n  "Longitude Coordinate": "float",\n  "(Latitude.Longitude)": "str",\n  "Council District": "str",\n  "Map Page": "str",\n  "Map Tile": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Service Request (SR) Number": "unique_key",\n  "SR Description": "complaint_description",\n  "Method Received": "source",\n  "SR Status": "status",\n  "Status Change Date": "status_change_date",\n  "Created Date": "created_date",\n  "Last Update Date": "last_update_date",\n  "Close Date": "close_date",\n  "SR Location": "incident_address",\n  "Street Number": "street_number",\n  "Street Name": "street_name",\n  "City": "city",\n  "Zip Code": "incident_zip",\n  "County": "county",\n  "State Plane X Coordinate": "state_plane_x_coordinate",\n  "State Plane Y Coordinate": "state_plane_y_coordinate",\n  "Latitude Coordinate": "latitude",\n  "Longitude Coordinate": "longitude",\n  "(Latitude.Longitude)": "location",\n  "Council District": "council_district_code",\n  "Map Page": "map_page",\n  "Map Tile": "map_tile"\n}',
            "REORDER_HEADERS_LIST": '[\n  "unique_key",\n  "complaint_description",\n  "source",\n  "status",\n  "status_change_date",\n  "created_date",\n  "last_update_date",\n  "close_date",\n  "incident_address",\n  "street_number",\n  "street_name",\n  "city",\n  "incident_zip",\n  "county",\n  "state_plane_x_coordinate",\n  "state_plane_y_coordinate",\n  "latitude",\n  "longitude",\n  "location",\n  "council_district_code",\n  "map_page",\n  "map_tile"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run CSV transform within kubernetes pod
    austin_bikeshare_trips = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_bikeshare_trips",
        name="austin_bikeshare_trips",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.austintexas.gov/api/views/tyfh-5r8s/rows.csv",
            "SOURCE_FILE": "files/data_austin_bikeshare_trips.csv",
            "TARGET_FILE": "files/data_output_austin_bikeshare_trips.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin_bikeshare/data_output.csv",
            "PIPELINE_NAME": "Austin Bikeshare Trips",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "austin_bikeshare",
            "DESTINATION_TABLE": "bikeshare_trips",
            "SCHEMA_PATH": "data/austin_bikeshare/schema/austin_bikeshare_trips_schema.json",
            "DATE_FORMAT_LIST": '{\n  "start_time": "%Y-%m-%d %H:%M:%S"\n}',
            "NULL_ROWS_LIST": '[\n  "trip_id"\n]',
            "INPUT_CSV_HEADERS": '[\n  "Trip ID",\n  "Membership Type",\n  "Bicycle ID",\n  "Bike Type",\n  "Checkout Date",\n  "Checkout Time",\n  "Checkout Kiosk ID",\n  "Checkout Kiosk",\n  "Return Kiosk ID",\n  "Return Kiosk",\n  "Trip Duration Minutes",\n  "Month",\n  "Year"\n]',
            "DATA_DTYPES": '{\n  "Trip ID": "str",\n  "Membership Type": "str",\n  "Bicycle ID": "str",\n  "Bike Type": "str",\n  "Checkout Date": "str",\n  "Checkout Time": "str",\n  "Checkout Kiosk ID": "str",\n  "Checkout Kiosk": "str",\n  "Return Kiosk ID": "str",\n  "Return Kiosk": "str",\n  "Trip Duration Minutes": "str",\n  "Month": "str",\n  "Year": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Trip ID": "trip_id",\n  "Membership Type": "subscriber_type",\n  "Bicycle ID": "bikeid",\n  "Checkout Date": "time",\n  "Checkout Kiosk ID": "start_station_id",\n  "Checkout Kiosk": "start_station_name",\n  "Return Kiosk ID": "end_station_id",\n  "Return Kiosk": "end_station_name",\n  "Trip Duration Minutes": "duration_minutes",\n  "Checkout Time": "checkout_time",\n  "Month": "month",\n  "Year": "year"\n}',
            "REORDER_HEADERS_LIST": '[\n  "trip_id",\n  "subscriber_type",\n  "bikeid",\n  "start_time",\n  "start_station_id",\n  "start_station_name",\n  "end_station_id",\n  "end_station_name",\n  "duration_minutes"\n]',
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    [austin_311_service_requests, austin_bikeshare_trips]
