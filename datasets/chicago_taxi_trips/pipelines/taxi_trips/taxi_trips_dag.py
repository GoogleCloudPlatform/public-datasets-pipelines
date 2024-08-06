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
    dag_id="chicago_taxi_trips.taxi_trips",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Download Taxi Trips dataset
    prepare_source = kubernetes_pod.KubernetesPodOperator(
        task_id="prepare_source",
        name="taxi_trips",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image="{{ var.json.chicago_taxi_trips.container_registry.run_csv_transform_kub }}",
        image_pull_policy="Always",
        env_vars={
            "SOURCE_URL": "https://data.cityofchicago.org/api/views/wrvz-psew/rows.csv",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CSV_GCS_PATH": "data/chicago_taxi_trips/taxi_trips.csv",
            "CSV_HEADERS": '[\n  "unique_key", "taxi_id", "trip_start_timestamp",\n  "trip_end_timestamp", "trip_seconds", "trip_miles",\n  "pickup_census_tract", "dropoff_census_tract",\n  "pickup_community_area", "dropoff_community_area",\n  "fare", "tips", "tolls", "extras",\n  "trip_total", "payment_type", "company",\n  "pickup_latitude", "pickup_longitude",\n  "pickup_location", "dropoff_latitude",\n  "dropoff_longitude", "dropoff_location"\n]',
            "DATA_DTYPES": '{\n  "unique_key": "str", "taxi_id": "str", "trip_start_timestamp": "str",\n  "trip_end_timestamp": "str", "trip_seconds": "str", "trip_miles": "str",\n  "pickup_census_tract": "str", "dropoff_census_tract": "str",\n  "pickup_community_area": "str", "dropoff_community_area": "str",\n  "fare": "str", "tips": "str", "tolls": "str", "extras": "str",\n  "trip_total": "str", "payment_type": "str", "company": "str",\n  "pickup_latitude": "str", "pickup_longitude": "str",\n  "pickup_location": "str", "dropoff_latitude": "str",\n  "dropoff_longitude": "str", "dropoff_location": "str"\n}',
            "NON_NA_COLUMNS": '["unique_key","taxi_id"]',
            "CHUNKSIZE": "1000000",
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    prepare_source
