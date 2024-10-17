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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="london_bicycles.london_bicycles",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 0 * * 6",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    stations_csv_transform = kubernetes_pod.KubernetesPodOperator(
        task_id="stations_csv_transform",
        startup_timeout_seconds=600,
        name="london_bicycle_stations",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.london_bicycles.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{\n  "stations": "https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml"\n}',
            "SOURCE_FILE": "./files/livecyclehireupdates.xml",
            "REQUIRED_COLS": '[\n  "id",\n  "installed",\n  "lat",\n  "locked",\n  "long",\n  "name",\n  "nbBikes",\n  "nbDocks",\n  "nbEmptyDocks",\n  "temporary",\n  "terminalName",\n  "installDate",\n  "removalDate"\n]',
            "RENAME_MAPPINGS": '{\n  "id": "id",\n  "installed": "installed",\n  "lat": "latitude",\n  "locked": "locked",\n  "long": "longitude",\n  "name": "name",\n  "nbBikes": "bikes_count",\n  "nbDocks": "docks_count",\n  "nbEmptyDocks": "nbEmptyDocks",\n  "temporary": "temporary",\n  "terminalName": "terminal_name",\n  "installDate": "install_date",\n  "removalDate": "removal_date"\n}',
            "DATE_COLS": '[\n  "installDate",\n  "removalDate"\n]',
            "INTEGER_COLS": '[\n  "id",\n  "nbBikes",\n  "nbDocks",\n  "nbEmptyDocks",\n  "terminalName"\n]',
            "FLOAT_COLS": '[\n  "lat",\n  "long"\n]',
            "STRING_COLS": '[\n  "installed",\n  "locked",\n  "name",\n  "temporary"\n]',
            "OUTPUT_FILE": "./files/cycle_stations_data_output.csv",
            "GCS_BUCKET": "{{ var.json.london_bicycles.storage_bucket }}",
            "TARGET_GCS_PATH": "data/london_bicycles/cycle_stations_data_output.csv",
            "PIPELINE": "London Cycle Stations Dataset",
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_cycle_stations_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_cycle_stations_to_bq",
        bucket="{{ var.json.london_bicycles.storage_bucket }}",
        source_objects=["data/london_bicycles/cycle_stations_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="london_bicycles.cycle_stations",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "id", "type": "integer", "mode": "nullable"},
            {"name": "installed", "type": "boolean", "mode": "nullable"},
            {"name": "latitude", "type": "float", "mode": "nullable"},
            {"name": "locked", "type": "string", "mode": "nullable"},
            {"name": "longitude", "type": "float", "mode": "nullable"},
            {"name": "name", "type": "string", "mode": "nullable"},
            {"name": "bikes_count", "type": "integer", "mode": "nullable"},
            {"name": "docks_count", "type": "integer", "mode": "nullable"},
            {"name": "nbEmptyDocks", "type": "integer", "mode": "nullable"},
            {"name": "temporary", "type": "boolean", "mode": "nullable"},
            {"name": "terminal_name", "type": "string", "mode": "nullable"},
            {"name": "install_date", "type": "date", "mode": "nullable"},
            {"name": "removal_date", "type": "date", "mode": "nullable"},
        ],
    )

    # Run CSV transform within kubernetes pod
    trips_csv_transform = kubernetes_pod.KubernetesPodOperator(
        task_id="trips_csv_transform",
        startup_timeout_seconds=600,
        name="london_bicycle_trips",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.london_bicycles.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{\n  "trips": "gs://london-cycling-data"\n}',
            "SOURCE_FILE": "./files/journey.csv",
            "LOAD_START_DATE_FLOOR": "{{ var.json.london_bicycles.cycle_hire.load_start_date_floor }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "london_bicycles",
            "TABLE_ID": "cycle_hire",
            "RENAME_MAPPINGS": '{\n  "Rental Id": "rental_id",\n  "Duration_Seconds": "duration_str",\n  "Duration": "duration_str",\n  "Bike Id": "bike_id",\n  "End Date": "end_date",\n  "EndStation Id": "end_station_id",\n  "End Station Id": "end_station_id",\n  "EndStation Name": "end_station_name",\n  "End Station Name": "end_station_name",\n  "Start Date": "start_date",\n  "StartStation Id": "start_station_id",\n  "Start Station Id": "start_station_id",\n  "StartStation Name": "start_station_name",\n  "Start Station Name": "start_station_name",\n  "Number": "rental_id",\n  "Start date": "start_date",\n  "Start station number": "start_station_id",\n  "Start station": "start_station_name",\n  "End date": "end_date",\n  "End station number": "end_station_id",\n  "End station": "end_station_name",\n  "Bike number": "bike_id",\n  "Bike model": "bike_model",\n  "Total duration": "duration_str",\n  "Total duration (ms)": "duration_ms"\n}',
            "OUTPUT_FILE": "./files/cycle_trips_data_output.csv",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SCHEMA_PATH": "data/london_bicycles/schema/cycle_hire_schema.json",
            "DATA_DTYPES": '{\n  "rental_id": "int32",\n  "duration_str": "int32",\n  "duration_ms": "int32",\n  "bike_id": "int32",\n  "bike_model": "str",\n  "end_date": "datetime64",\n  "end_station_id": "int32",\n  "end_station_name": "str",\n  "start_date": "datetime64",\n  "start_station_id": "int32",\n  "start_station_name": "str",\n  "end_station_logical_terminal": "int32",\n  "start_station_logical_terminal": "int32",\n  "end_station_priority_id": "int32"\n}',
            "OUTPUT_CSV_HEADERS": '[\n  "rental_id",\n  "duration",\n  "duration_ms",\n  "bike_id",\n  "bike_model",\n  "end_date",\n  "end_station_id",\n  "end_station_name",\n  "start_date",\n  "start_station_id",\n  "start_station_name",\n  "end_station_logical_terminal",\n  "start_station_logical_terminal",\n  "end_station_priority_id"\n]',
            "PIPELINE": "London Cycle Trips Dataset",
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    stations_csv_transform >> load_cycle_stations_to_bq >> trips_csv_transform
