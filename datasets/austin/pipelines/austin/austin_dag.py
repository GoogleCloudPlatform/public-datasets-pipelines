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

    # Fetch data gcs - gcs
    austin_bs_stations_source_data_to_gcs = bash.BashOperator(
        task_id="austin_bs_stations_source_data_to_gcs",
        bash_command="curl https://data.austintexas.gov/api/views/qd73-bsdg/rows.csv | gsutil cp - gs://{{ var.value.composer_bucket }}/data/austin/austin_bs_stations_source.csv\n",
    )

    # Run CSV transform within kubernetes pod
    austin_bs_stations_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_bs_stations_process",
        name="austin_bs_stations_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_bs_stations_source.csv",
            "SOURCE_FILE": "files/austin_bs_stations_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/bikeshare_stations_batch",
            "PIPELINE_NAME": "Austin Bikeshare Stations",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATE_FORMAT_LIST": '[\n  ["modified_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
            "NULL_ROWS_LIST": '[\n  "station_id"\n]',
            "INPUT_CSV_HEADERS": '[\n  "Kiosk ID",\n  "Kiosk Name",\n  "Kiosk Status",\n  "Location",\n  "Address",\n  "Alternate Name",\n  "City Asset Number",\n  "Property Type",\n  "Number of Docks",\n  "Power Type",\n  "Footprint Length",\n  "Footprint Width",\n  "Notes",\n  "Council District",\n  "Image",\n  "Modified Date"\n]',
            "DATA_DTYPES": '{\n  "station_id": "str",\n  "name": "str",\n  "status": "str",\n  "location": "str",\n  "address": "str",\n  "alternate_name": "str",\n  "city_asset_number": "str",\n  "property_type": "str",\n  "number_of_docks": "str",\n  "power_type": "str",\n  "footprint_length": "str",\n  "footprint_width": "str",\n  "notes": "str",\n  "council_district": "str",\n  "image": "str",\n  "modified_date": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Kiosk ID": "station_id",\n  "Kiosk Name": "name",\n  "Kiosk Status": "status",\n  "Location": "location",\n  "Address": "address",\n  "Alternate Name": "alternate_name",\n  "City Asset Number": "city_asset_number",\n  "Property Type": "property_type",\n  "Number of Docks": "number_of_docks",\n  "Power Type": "power_type",\n  "Footprint Length": "footprint_length",\n  "Footprint Width": "footprint_width",\n  "Notes": "notes",\n  "Council District": "council_district",\n  "Image": "image",\n  "Modified Date": "modified_date"\n}',
            "REORDER_HEADERS_LIST": '[\n  "station_id",\n  "name",\n  "status",\n  "location",\n  "address",\n  "alternate_name",\n  "city_asset_number",\n  "property_type",\n  "number_of_docks",\n  "power_type",\n  "footprint_length",\n  "footprint_width",\n  "notes",\n  "council_district",\n  "image",\n  "modified_date"\n]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_bs_stations = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_bs_stations",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/austin/bikeshare_stations_batch/austin_bs_stations_output-*.csv"
        ],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="austin_bikeshare.bikeshare_stations",
        skip_leading_rows=1,
        ignore_unknown_values=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_object="data/austin/schema/austin_bikeshare_stations_schema.json",
    )

    # Fetch data gcs - crime
    austin_crime_source_data_to_gcs = bash.BashOperator(
        task_id="austin_crime_source_data_to_gcs",
        bash_command="gsutil cp gs://pdp-feeds-staging/Austin_Crime/Annual_Crime_2014.csv gs://{{ var.value.composer_bucket }}/data/austin/austin_crime/austin_crime_2014_source.csv ; gsutil cp gs://pdp-feeds-staging/Austin_Crime/Annual_Crime_Dataset_2015.csv gs://{{ var.value.composer_bucket }}/data/austin/austin_crime/austin_crime_2015_source.csv ; gsutil cp gs://pdp-feeds-staging/Austin_Crime/2016_Annual_Crime_Data.csv gs://{{ var.value.composer_bucket }}/data/austin/austin_crime/austin_crime_2016_source.csv ;",
    )

    # Run CSV transform within kubernetes pod
    austin_crime_2014_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_crime_2014_process",
        name="austin_crime_2014_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_crime/austin_crime_2014_source.csv",
            "SOURCE_FILE": "files/austin_crime_2014_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/crime_batch",
            "PIPELINE_NAME": "Austin Crime 2014",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "INPUT_CSV_HEADERS": '[\n  "GO Primary Key",\n  "Council District",\n  "GO Highest Offense Desc",\n  "Highest NIBRS/UCR Offense Description",\n  "GO Report Date",\n  "GO Location",\n  "Clearance Status",\n  "Clearance Date",\n  "GO District",\n  "GO Location Zip",\n  "GO Census Tract",\n  "GO X Coordinate",\n  "GO Y Coordinate",\n  "Location_1"\n]',
            "REORDER_HEADERS_LIST": '[\n  "unique_key",\n  "address",\n  "census_tract",\n  "clearance_date",\n  "clearance_status",\n  "council_district_code",\n  "description",\n  "district",\n  "latitude",\n  "longitude",\n  "location",\n  "location_description",\n  "primary_type",\n  "timestamp",\n  "x_coordinate",\n  "y_coordinate",\n  "year",\n  "zipcode"\n]',
            "RENAME_HEADERS_LIST": '{\n  "GO Primary Key": "unique_key",\n  "Council District": "council_district_code",\n  "GO Highest Offense Desc": "description",\n  "Highest NIBRS/UCR Offense Description": "primary_type",\n  "GO Report Date": "timestamp",\n  "GO Location": "location_description",\n  "Clearance Status": "clearance_status",\n  "Clearance Date": "clearance_date",\n  "GO District": "district",\n  "GO Location Zip": "zipcode",\n  "GO Census Tract": "census_tract",\n  "GO X Coordinate": "x_coordinate",\n  "GO Y Coordinate": "y_coordinate",\n  "Location_1": "temp_address"\n}',
            "DATE_FORMAT_LIST": '[\n  ["timestamp", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"],\n  ["clearance_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
        },
    )

    # Run CSV transform within kubernetes pod
    austin_crime_2015_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_crime_2015_process",
        name="austin_crime_2015_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_crime/austin_crime_2015_source.csv",
            "SOURCE_FILE": "files/austin_crime_2015_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/crime_batch",
            "PIPELINE_NAME": "Austin Crime 2015",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "INPUT_CSV_HEADERS": '[\n  "GO Primary Key",\n  "Council District",\n  "GO Highest Offense Desc",\n  "Highest NIBRS/UCR Offense Description",\n  "GO Report Date",\n  "GO Location",\n  "Clearance Status",\n  "Clearance Date",\n  "GO District",\n  "GO Location Zip",\n  "GO Census Tract",\n  "GO X Coordinate",\n  "GO Y Coordinate"\n]',
            "REORDER_HEADERS_LIST": '[\n  "unique_key",\n  "address",\n  "census_tract",\n  "clearance_date",\n  "clearance_status",\n  "council_district_code",\n  "description",\n  "district",\n  "latitude",\n  "longitude",\n  "location",\n  "location_description",\n  "primary_type",\n  "timestamp",\n  "x_coordinate",\n  "y_coordinate",\n  "year",\n  "zipcode"\n]',
            "RENAME_HEADERS_LIST": '{\n  "GO Primary Key": "unique_key",\n  "Council District": "council_district_code",\n  "GO Highest Offense Desc": "description",\n  "Highest NIBRS/UCR Offense Description": "primary_type",\n  "GO Report Date": "timestamp",\n  "GO Location": "location_description",\n  "Clearance Status": "clearance_status",\n  "Clearance Date": "clearance_date",\n  "GO District": "district",\n  "GO Location Zip": "zipcode",\n  "GO Census Tract": "census_tract",\n  "GO X Coordinate": "x_coordinate",\n  "GO Y Coordinate": "y_coordinate",\n  "Location_1": "temp_address"\n}',
            "DATE_FORMAT_LIST": '[\n  ["timestamp", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"],\n  ["clearance_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
        },
    )

    # Run CSV transform within kubernetes pod
    austin_crime_2016_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_crime_2016_process",
        name="austin_crime_2016_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_crime/austin_crime_2016_source.csv",
            "SOURCE_FILE": "files/austin_crime_2016_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/crime_batch",
            "PIPELINE_NAME": "Austin Crime 2016",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "INPUT_CSV_HEADERS": '[\n  "GO Primary Key",\n  "Council District",\n  "GO Highest Offense Desc",\n  "Highest NIBRS/UCR Offense Description",\n  "GO Report Date",\n  "GO Location",\n  "Clearance Status",\n  "Clearance Date",\n  "GO District",\n  "GO Location Zip",\n  "GO Census Tract",\n  "GO X Coordinate",\n  "GO Y Coordinate"\n]',
            "RENAME_HEADERS_LIST": '{\n  "GO Primary Key": "unique_key",\n  "Council District": "council_district_code",\n  "GO Highest Offense Desc": "description",\n  "Highest NIBRS/UCR Offense Description": "primary_type",\n  "GO Report Date": "timestamp",\n  "GO Location": "location_description",\n  "Clearance Status": "clearance_status",\n  "Clearance Date": "clearance_date",\n  "GO District": "district",\n  "GO Location Zip": "zipcode",\n  "GO Census Tract": "census_tract",\n  "GO X Coordinate": "x_coordinate",\n  "GO Y Coordinate": "y_coordinate",\n  "Location_1": "address"\n}',
            "REORDER_HEADERS_LIST": '[\n  "unique_key",\n  "address",\n  "census_tract",\n  "clearance_date",\n  "clearance_status",\n  "council_district_code",\n  "description",\n  "district",\n  "latitude",\n  "longitude",\n  "location",\n  "location_description",\n  "primary_type",\n  "timestamp",\n  "x_coordinate",\n  "y_coordinate",\n  "year",\n  "zipcode"\n]',
            "DATE_FORMAT_LIST": '[\n  ["timestamp", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"],\n  ["clearance_date", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_austin_crime = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_austin_crime",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/austin/crime_batch/austin_crime_2014_output-*.csv",
            "data/austin/crime_batch/austin_crime_2015_output-*.csv",
            "data/austin/crime_batch/austin_crime_2016_output-*.csv",
        ],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="austin_crime.crime",
        skip_leading_rows=1,
        ignore_unknown_values=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_object="data/austin/schema/austin_crime_schema.json",
    )

    # Fetch data austin waste
    austin_waste_source_data_to_gcs = bash.BashOperator(
        task_id="austin_waste_source_data_to_gcs",
        bash_command="curl https://data.austintexas.gov/api/views/mbnu-4wq9/rows.csv | gsutil cp - gs://{{ var.value.composer_bucket }}/data/austin/austin_waste/austin_waste_source.csv\n",
    )

    # Run CSV transform within kubernetes pod
    austin_waste_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_waste_process",
        name="austin_waste_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_waste/austin_waste_source.csv",
            "SOURCE_FILE": "files/austin_waste_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/waste_batch",
            "PIPELINE_NAME": "Austin Waste",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "INPUT_CSV_HEADERS": '[\n  "Report Date",\n  "Load Type",\n  "Load Time",\n  "Load Weight",\n  "Dropoff Site",\n  "Route Type",\n  "Route Number",\n  "Load ID"\n]',
            "RENAME_HEADERS_LIST": '{\n  "Load ID": "load_id",\n  "Report Date": "report_date",\n  "Load Type": "load_type",\n  "Load Time": "load_time",\n  "Load Weight": "load_weight",\n  "Dropoff Site": "dropoff_site",\n  "Route Type": "route_type",\n  "Route Number": "route_number"\n}',
            "REORDER_HEADERS_LIST": '[\n  "load_id",\n  "report_date",\n  "load_type",\n  "load_time",\n  "load_weight",\n  "dropoff_site",\n  "route_type",\n  "route_number"\n]',
            "DATE_FORMAT_LIST": '[\n  ["report_date", "%m/%d/%Y", "%Y-%m-%d"],\n  ["load_time", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_austin_waste = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_austin_waste",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/austin/waste_batch/*.csv"],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="austin_waste.waste_and_diversion",
        skip_leading_rows=1,
        ignore_unknown_values=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_object="data/austin/schema/austin_waste_and_diversion_schema.json",
    )

    [
        austin_waste_source_data_to_gcs
        >> austin_waste_process
        >> load_full_to_bq_austin_waste
    ], [
        austin_311_source_data_to_gcs
        >> austin_311_process
        >> load_full_to_bq_austin_311
    ], [
        austin_crime_source_data_to_gcs
        >> [
            austin_crime_2014_process,
            austin_crime_2015_process,
            austin_crime_2016_process,
        ]
        >> load_full_to_bq_austin_crime
    ], [
        austin_bs_trips_source_data_to_gcs
        >> austin_bs_trips_process
        >> load_full_to_bq_bs_trips
    ], [
        austin_bs_stations_source_data_to_gcs
        >> austin_bs_stations_process
        >> load_full_to_bq_bs_stations
    ]
