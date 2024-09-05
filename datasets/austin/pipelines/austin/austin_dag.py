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
from airflow.operators import bash
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="austin.austin",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="3 10 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - 311
    austin_311_source_data_to_gcs = bash.BashOperator(
        task_id="austin_311_source_data_to_gcs",
        bash_command="curl https://data.austintexas.gov/api/views/xwdj-i9he/rows.csv | gsutil cp - gs://{{ var.value.composer_bucket }}/data/austin/austin_311_service_requests_source.csv\n",
    )

    # Run CSV transform within kubernetes pod
    austin_311_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_311_process",
        name="austin_311_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Austin 311 Service Requests By Year",
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_311_service_requests_source.csv",
            "CHUNKSIZE": "50000",
            "SOURCE_FILE": "files/austin_311_service_requests_source.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/311_batch",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATE_FORMAT_LIST": '[\n  ["status_change_date", "%m/%d/%Y %I:%M:%S %p","%Y-%m-%d %H:%M:%S"],\n  ["created_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"],\n  ["last_update_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"],\n  ["close_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
            "INT_COLS_LIST": '[\n  "council_district_code"\n]',
            "REMOVE_NEWLINES_COLS_LIST": '[\n  "location"\n]',
            "NULL_ROWS_LIST": '[\n  "unique_key"\n]',
            "INPUT_CSV_HEADERS": '[\n  "Service Request (SR) Number",\n  "SR Description",\n  "Method Received",\n  "SR Status",\n  "Status Change Date",\n  "Created Date",\n  "Last Update Date",\n  "Close Date",\n  "SR Location",\n  "Street Number",\n  "Street Name",\n  "City",\n  "Zip Code",\n  "County",\n  "State Plane X Coordinate",\n  "State Plane Y Coordinate",\n  "Latitude Coordinate",\n  "Longitude Coordinate",\n  "(Latitude.Longitude)",\n  "Council District",\n  "Map Page",\n  "Map Tile"\n]',
            "DATA_DTYPES": '{\n  "Service Request (SR) Number": "str",\n  "SR Description": "str",\n  "Method Received": "str",\n  "SR Status": "str",\n  "Status Change Date": "str",\n  "Created Date": "str",\n  "Last Update Date": "str",\n  "Close Date": "str",\n  "SR Location": "str",\n  "Street Number": "str",\n  "Street Name": "str",\n  "City": "str",\n  "Zip Code": "str",\n  "County": "str",\n  "State Plane X Coordinate": "str",\n  "State Plane Y Coordinate": "str",\n  "Latitude Coordinate": "str",\n  "Longitude Coordinate": "str",\n  "(Latitude.Longitude)": "str",\n  "Council District": "str",\n  "Map Page": "str",\n  "Map Tile": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Service Request (SR) Number": "unique_key",\n  "SR Description": "complaint_description",\n  "Method Received": "source",\n  "SR Status": "status",\n  "Status Change Date": "status_change_date",\n  "Created Date": "created_date",\n  "Last Update Date": "last_update_date",\n  "Close Date": "close_date",\n  "SR Location": "incident_address",\n  "Street Number": "street_number",\n  "Street Name": "street_name",\n  "City": "city",\n  "Zip Code": "incident_zip",\n  "County": "county",\n  "State Plane X Coordinate": "state_plane_x_coordinate",\n  "State Plane Y Coordinate": "state_plane_y_coordinate",\n  "Latitude Coordinate": "latitude",\n  "Longitude Coordinate": "longitude",\n  "(Latitude.Longitude)": "location",\n  "Council District": "council_district_code",\n  "Map Page": "map_page",\n  "Map Tile": "map_tile"\n}',
            "REORDER_HEADERS_LIST": '[\n  "unique_key",\n  "complaint_description",\n  "source",\n  "status",\n  "status_change_date",\n  "created_date",\n  "last_update_date",\n  "close_date",\n  "incident_address",\n  "street_number",\n  "street_name",\n  "city",\n  "incident_zip",\n  "county",\n  "state_plane_x_coordinate",\n  "state_plane_y_coordinate",\n  "latitude",\n  "longitude",\n  "location",\n  "council_district_code",\n  "map_page",\n  "map_tile"\n]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_austin_311 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_austin_311",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/austin/311_batch/austin_311_service_requests_output-*.csv"
        ],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="austin_311.311_service_requests",
        skip_leading_rows=1,
        ignore_unknown_values=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_object="data/austin/schema/austin_311_service_requests_schema.json",
    )

    # Fetch data gcs - gcs
    austin_bs_trips_source_data_to_gcs = bash.BashOperator(
        task_id="austin_bs_trips_source_data_to_gcs",
        bash_command="curl https://data.austintexas.gov/api/views/tyfh-5r8s/rows.csv | gsutil cp - gs://{{ var.value.composer_bucket }}/data/austin/austin_bs_trips_source.csv\n",
    )

    # Run CSV transform within kubernetes pod
    austin_bs_trips_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_bs_trips_process",
        name="austin_bs_trips_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_bs_trips_source.csv",
            "SOURCE_FILE": "files/austin_bs_trips_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/bikeshare_trips_batch",
            "PIPELINE_NAME": "Austin Bikeshare Trips",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATE_FORMAT_LIST": '[\n  ["start_time", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]\n]',
            "NULL_ROWS_LIST": '[\n  "trip_id"\n]',
            "INPUT_CSV_HEADERS": '[\n  "Trip ID",\n  "Membership Type",\n  "Bicycle ID",\n  "Bike Type",\n  "Checkout Datetime",\n  "Checkout Date",\n  "Checkout Time",\n  "Checkout Kiosk ID",\n  "Checkout Kiosk",\n  "Return Kiosk ID",\n  "Return Kiosk",\n  "Trip Duration Minutes",\n  "Month",\n  "Year"\n]',
            "DATA_DTYPES": '{\n  "Trip ID": "str",\n  "Membership Type": "str",\n  "Bicycle ID": "str",\n  "Bike Type": "str",\n  "Checkout Date": "str",\n  "Checkout Time": "str",\n  "Checkout Kiosk ID": "str",\n  "Checkout Kiosk": "str",\n  "Return Kiosk ID": "str",\n  "Return Kiosk": "str",\n  "Trip Duration Minutes": "str",\n  "Month": "str",\n  "Year": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Trip ID": "trip_id",\n  "Membership Type": "subscriber_type",\n  "Bicycle ID": "bikeid",\n  "Bike Type": "bike_type",\n  "Checkout Date": "time",\n  "Checkout Kiosk ID": "start_station_id",\n  "Checkout Kiosk": "start_station_name",\n  "Return Kiosk ID": "end_station_id",\n  "Return Kiosk": "end_station_name",\n  "Trip Duration Minutes": "duration_minutes",\n  "Checkout Time": "checkout_time",\n  "Month": "month",\n  "Year": "year"\n}',
            "REORDER_HEADERS_LIST": '[\n  "trip_id",\n  "subscriber_type",\n  "bikeid",\n  "bike_type",\n  "start_time",\n  "start_station_id",\n  "start_station_name",\n  "end_station_id",\n  "end_station_name",\n  "duration_minutes"\n]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_bs_trips = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_bs_trips",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/austin/bikeshare_trips_batch/austin_bs_trips_output-*.csv"
        ],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="austin_bikeshare.bikeshare_trips",
        skip_leading_rows=1,
        ignore_unknown_values=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_object="data/austin/schema/austin_bikeshare_trips_schema.json",
    )

    [
        austin_311_source_data_to_gcs
        >> austin_311_process
        >> load_full_to_bq_austin_311
    ], [
        austin_bs_trips_source_data_to_gcs
        >> austin_bs_trips_process
        >> load_full_to_bq_bs_trips
    ]
