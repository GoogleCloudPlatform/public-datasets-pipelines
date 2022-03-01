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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="epa_historical_air_quality.pm10_daily_summary",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 6 * * *",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "epa-hist-air-quality",
            "initial_node_count": 50,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv_and_load_data = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_and_load_data",
        startup_timeout_seconds=600,
        name="load_data",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="epa-hist-air-quality",
        image_pull_policy="Always",
        image="{{ var.json.epa_historical_air_quality.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "{{ var.json.epa_historical_air_quality.pm10_daily_summary.source_url }}",
            "START_YEAR": "1990",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.epa_historical_air_quality.dataset_id }}",
            "TABLE_ID": "{{ var.json.epa_historical_air_quality.pm10_daily_summary.table_id }}",
            "SCHEMA_PATH": "{{ var.json.epa_historical_air_quality.pm10_daily_summary.schema_path }}",
            "CHUNKSIZE": "{{ var.json.epa_historical_air_quality.pm10_daily_summary.chunk_size }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.epa_historical_air_quality.pm10_daily_summary.target_gcs_path }}",
            "PIPELINE_NAME": "epa_historical_air_quality - pm10_daily_summaries",
            "INPUT_CSV_HEADERS": '[ "state_code", "county_code", "site_num", "parameter_code", "poc",\n  "latitude", "longitude", "datum", "parameter_name", "sample_duration",\n  "pollutant_standard", "date_local", "units_of_measure", "event_type", "observation_count",\n  "observation_percent", "arithmetic_mean", "first_max_value", "first_max_hour", "aqi",\n  "method_code", "method_name", "local_site_name", "address", "state_name",\n  "county_name", "city_name", "cbsa_name", "date_of_last_change" ]',
            "DATA_DTYPES": '{ "state_code": "str", "county_code": "str", "site_num": "str", "parameter_code": "int32", "poc": "int32",\n  "latitude": "float64", "longitude": "float64", "datum": "str", "parameter_name": "str", "sample_duration": "str",\n  "pollutant_standard": "str", "date_local": "datetime64[ns]", "units_of_measure": "str", "event_type": "str", "observation_count": "int32",\n  "observation_percent": "float64", "arithmetic_mean": "float64", "first_max_value": "float64", "first_max_hour": "int32", "aqi": "str",\n  "method_code": "str", "method_name": "str", "local_site_name": "str", "address": "str", "state_name": "str",\n  "county_name": "str", "city_name": "str", "cbsa_name": "str", "date_of_last_change": "datetime64[ns]" }',
            "OUTPUT_CSV_HEADERS": '[ "state_code", "county_code", "site_num", "parameter_code", "poc",\n  "latitude", "longitude", "datum", "parameter_name", "sample_duration",\n  "pollutant_standard", "date_local", "units_of_measure", "event_type", "observation_count",\n  "observation_percent", "arithmetic_mean", "first_max_value", "first_max_hour", "aqi",\n  "method_code", "method_name", "local_site_name", "address", "state_name",\n  "county_name", "city_name", "cbsa_name", "date_of_last_change" ]',
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "1",
            "request_ephemeral_storage": "12G",
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="epa-hist-air-quality",
    )

    create_cluster >> transform_csv_and_load_data >> delete_cluster
