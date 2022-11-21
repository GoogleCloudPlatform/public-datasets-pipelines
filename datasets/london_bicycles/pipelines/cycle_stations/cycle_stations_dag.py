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
    dag_id="london_bicycles.cycle_stations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    csv_transform = kubernetes_pod.KubernetesPodOperator(
        task_id="csv_transform",
        startup_timeout_seconds=600,
        name="cycle_stations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.london_bicycles.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml",
            "SOURCE_FILE": "./files/livecyclehireupdates.xml",
            "REQUIRED_COLS": '["id", "installed", "lat", "locked", "long", "name", "nbBikes", "nbDocks", "nbEmptyDocks", "temporary", "terminalName", "installDate", "removalDate"]',
            "RENAME_MAPPINGS": '{"id": "id", "installed": "installed", "lat": "latitude", "locked": "locked", "long": "longitude", "name": "name", "nbBikes": "bikes_count", "nbDocks": "docks_count", "nbEmptyDocks": "nbEmptyDocks", "temporary": "temporary", "terminalName": "terminal_name", "installDate": "install_date", "removalDate": "removal_date"}',
            "DATE_COLS": '["installDate", "removalDate"]',
            "INTEGER_COLS": '["id", "nbBikes", "nbDocks", "nbEmptyDocks", "terminalName"]',
            "FLOAT_COLS": '["lat", "long"]',
            "STRING_COLS": '["installed","locked", "name", "temporary"]',
            "OUTPUT_FILE": "./files/cycle_stations_data_output.csv",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/london_bicycles/cycle_stations/cycle_stations_data_output.csv",
        },
        resources={"request_memory": "128M", "request_cpu": "128m"},
    )

    # Task to load CSV data to a BigQuery table
    load_cycle_stations_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_cycle_stations_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/london_bicycles/cycle_stations/cycle_stations_data_output.csv"
        ],
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

    csv_transform >> load_cycle_stations_to_bq
