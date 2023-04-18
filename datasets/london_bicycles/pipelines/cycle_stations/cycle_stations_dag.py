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
    dag_id="london_bicycles.cycle_stations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    trips_csv_transform = kubernetes_pod.KubernetesPodOperator(
        task_id="trips_csv_transform",
        startup_timeout_seconds=600,
        name="london_bicycle_trips",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.london_bicycles.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{\n  "trips": "https://cycling.data.tfl.gov.uk"\n}',
            "SOURCE_FILE": "./files/livecyclehireupdates.xml",
            "REQUIRED_COLS": '["id", "installed", "lat", "locked", "long", "name", "nbBikes", "nbDocks", "nbEmptyDocks", "temporary", "terminalName", "installDate", "removalDate"]',
            "RENAME_MAPPINGS": '{"id": "id", "installed": "installed", "lat": "latitude", "locked": "locked", "long": "longitude", "name": "name", "nbBikes": "bikes_count", "nbDocks": "docks_count", "nbEmptyDocks": "nbEmptyDocks", "temporary": "temporary", "terminalName": "terminal_name", "installDate": "install_date", "removalDate": "removal_date"}',
            "DATE_COLS": '["installDate", "removalDate"]',
            "INTEGER_COLS": '["id", "nbBikes", "nbDocks", "nbEmptyDocks", "terminalName"]',
            "FLOAT_COLS": '["lat", "long"]',
            "STRING_COLS": '["installed","locked", "name", "temporary"]',
            "OUTPUT_FILE": "./files/cycle_trips_data_output.csv",
            "GCS_BUCKET": "{{ var.json.london_bicycles.storage_bucket }}",
            "TARGET_GCS_PATH": "london_bicycle/cycle_trips_data_output.csv",
            "PIPELINE": "London Cycle Trips Dataset",
        },
        resources={
            "limit_memory": "8G",
            "limit_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    trips_csv_transform
