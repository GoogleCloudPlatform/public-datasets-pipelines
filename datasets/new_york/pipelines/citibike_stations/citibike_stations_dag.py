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
    dag_id="new_york.citibike_stations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="citibike_stations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_citibike_stations }}",
        env_vars={
            "SOURCE_URL_STATIONS_JSON": "https://gbfs.citibikenyc.com/gbfs/en/station_information",
            "SOURCE_URL_STATUS_JSON": "https://gbfs.citibikenyc.com/gbfs/en/station_status",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york/citibike_stations/data_output.csv",
        },
        resources={"limit_memory": "4G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/new_york/citibike_stations/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="new_york.citibike_stations",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "station_id",
                "type": "INTEGER",
                "description": "Unique identifier of a station.",
                "mode": "REQUIRED",
            },
            {
                "name": "name",
                "type": "STRING",
                "description": "Public name of the station.",
                "mode": "NULLABLE",
            },
            {
                "name": "short_name",
                "type": "STRING",
                "description": "Short name or other type of identifier, as used by the data publisher.",
                "mode": "NULLABLE",
            },
            {
                "name": "latitude",
                "type": "FLOAT",
                "description": "The latitude of station. The field value must be a valid WGS 84 latitude in decimal degrees format.",
                "mode": "NULLABLE",
            },
            {
                "name": "longitude",
                "type": "FLOAT",
                "description": "The longitude of station. The field value must be a valid WGS 84 latitude in decimal degrees format.",
                "mode": "NULLABLE",
            },
            {
                "name": "region_id",
                "type": "INTEGER",
                "description": "ID of the region where station is located.",
                "mode": "NULLABLE",
            },
            {
                "name": "rental_methods",
                "type": "STRING",
                "description": "Array of enumerables containing the payment methods accepted at this station.",
                "mode": "NULLABLE",
            },
            {
                "name": "capacity",
                "type": "INTEGER",
                "description": "ANumber of total docking points installed at this station, both available and unavailable.",
                "mode": "NULLABLE",
            },
            {
                "name": "eightd_has_key_dispenser",
                "type": "BOOLEAN",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "num_bikes_available",
                "type": "INTEGER",
                "description": "Number of bikes available for rental.",
                "mode": "NULLABLE",
            },
            {
                "name": "num_bikes_disabled",
                "type": "INTEGER",
                "description": "Number of disabled bikes at the station.",
                "mode": "NULLABLE",
            },
            {
                "name": "num_docks_available",
                "type": "INTEGER",
                "description": "Number of docks accepting bike returns.",
                "mode": "NULLABLE",
            },
            {
                "name": "num_docks_disabled",
                "type": "INTEGER",
                "description": "Number of empty but disabled dock points at the station.",
                "mode": "NULLABLE",
            },
            {
                "name": "is_installed",
                "type": "BOOLEAN",
                "description": "Is the station currently on the street?",
                "mode": "NULLABLE",
            },
            {
                "name": "is_renting",
                "type": "BOOLEAN",
                "description": "Is the station currently renting bikes?",
                "mode": "NULLABLE",
            },
            {
                "name": "is_returning",
                "type": "BOOLEAN",
                "description": "Is the station accepting bike returns?",
                "mode": "NULLABLE",
            },
            {
                "name": "eightd_has_available_keys",
                "type": "BOOLEAN",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "last_reported",
                "type": "TIMESTAMP",
                "description": "Timestamp indicating the last time this station reported its status to the backend, in NYC local time.",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
