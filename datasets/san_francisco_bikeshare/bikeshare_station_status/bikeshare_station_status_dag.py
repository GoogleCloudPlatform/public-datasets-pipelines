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
    dag_id="san_francisco_bikeshare.bikeshare_station_status",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="bikeshare_station_status",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_station_status }}",
        env_vars={
            "SOURCE_URL_JSON": "https://gbfs.baywheels.com/gbfs/en/station_status",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_bikeshare/bikeshare_station_status/data_output.csv",
            "LOGGING_ENGLISH_NAME": "San francisco bikeshare station status",
            "TRANSFORM_LIST": '[ "rename_headers", "filter_empty_data", "reorder_headers" ]',
            "REORDER_HEADERS": '[ "station_id", "num_bikes_available", "num_bikes_disabled", "num_docks_available", "num_docks_disabled",\n  "is_installed", "is_renting", "is_returning", "last_reported", "num_ebikes_available",\n  "eightd_has_available_keys" ]',
            "RENAME_HEADERS": '{ "data.stations.eightd_has_available_keys": "eightd_has_available_keys",\n  "data.stations.is_installed": "is_installed", "data.stations.is_renting": "is_renting",\n  "data.stations.is_returning": "is_returning", "data.stations.last_reported": "last_reported",\n  "data.stations.num_bikes_available": "num_bikes_available", "data.stations.num_bikes_disabled": "num_bikes_disabled",\n  "data.stations.num_docks_available": "num_docks_available", "data.stations.num_docks_disabled": "num_docks_disabled",\n  "data.stations.num_ebikes_available": "num_ebikes_available", "data.stations.station_id": "station_id" }',
            "GEOM_FIELD_LIST": "[ [ ] ]",
            "JSON_NODE_NAME": "stations",
            "FIELD_TYPE_LIST": "[ [ ] ]",
            "FILTER_ROWS_LIST": '[ [ "station_id", "num_bikes_available", "num_docks_available", "is_installed", "is_renting",\n    "is_returning", "last_reported" ] ]',
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/san_francisco_bikeshare/bikeshare_station_status/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_station_status_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "station_id",
                "type": "INTEGER",
                "description": "Unique identifier of a station",
                "mode": "REQUIRED",
            },
            {
                "name": "num_bikes_available",
                "type": "INTEGER",
                "description": "Number of bikes available for rental",
                "mode": "REQUIRED",
            },
            {
                "name": "num_bikes_disabled",
                "type": "INTEGER",
                "description": "Number of disabled bikes at the station. Vendors who do not want to publicize the number of disabled bikes or docks in their system can opt to omit station capacity (in station_information), num_bikes_disabled and num_docks_disabled. If station capacity is published then broken docks/bikes can be inferred (though not specifically whether the decreased capacity is a broken bike or dock)",
                "mode": "NULLABLE",
            },
            {
                "name": "num_docks_available",
                "type": "INTEGER",
                "description": "Number of docks accepting bike returns",
                "mode": "REQUIRED",
            },
            {
                "name": "num_docks_disabled",
                "type": "INTEGER",
                "description": "Number of empty but disabled dock points at the station. This value remains as part of the spec as it is possibly useful during development",
                "mode": "NULLABLE",
            },
            {
                "name": "is_installed",
                "type": "BOOLEAN",
                "description": "1/0 boolean - is the station currently on the street",
                "mode": "REQUIRED",
            },
            {
                "name": "is_renting",
                "type": "BOOLEAN",
                "description": "1/0 boolean - is the station currently renting bikes (even if the station is empty, if it is set to allow rentals this value should be 1)",
                "mode": "REQUIRED",
            },
            {
                "name": "is_returning",
                "type": "BOOLEAN",
                "description": "1/0 boolean - is the station accepting bike returns (if a station is full but would allow a return if it was not full then this value should be 1)",
                "mode": "REQUIRED",
            },
            {
                "name": "last_reported",
                "type": "INTEGER",
                "description": "Integer POSIX timestamp indicating the last time this station reported its status to the backend",
                "mode": "REQUIRED",
            },
            {
                "name": "num_ebikes_available",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "eightd_has_available_keys",
                "type": "BOOLEAN",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
