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
    dag_id="epa_historical_air_quality.co_hourly_summary",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 1 * * *",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "epa-hist-air-quality--co_hourly",
            "initial_node_count": 1,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-8",
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
        cluster_name="epa-hist-air-quality--co_hourly",
        image_pull_policy="Always",
        image="{{ var.json.epa_historical_air_quality.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "{{ var.json.epa_historical_air_quality.co_hourly_summary.source_url }}",
            "START_YEAR": "1980",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.epa_historical_air_quality.dataset_id }}",
            "TABLE_ID": "{{ var.json.epa_historical_air_quality.co_hourly_summary.table_id }}",
            "SCHEMA_PATH": "{{ var.json.epa_historical_air_quality.co_hourly_summary.schema_path }}",
            "CHUNKSIZE": "{{ var.json.epa_historical_air_quality.co_hourly_summary.chunk_size }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.epa_historical_air_quality.co_hourly_summary.target_gcs_path }}",
            "PIPELINE_NAME": "epa_historical_air_quality - co_hourly_summaries",
            "INPUT_CSV_HEADERS": '[ "state_code", "county_code", "site_num", "parameter_code", "poc",\n  "latitude", "longitude", "datum", "parameter_name", "date_local",\n  "time_local", "date_gmt", "time_gmt", "sample_measurement", "units_of_measure",\n  "mdl", "uncertainty", "qualifier", "method_type", "method_code",\n  "method_name", "state_name", "county_name", "date_of_last_change" ]',
            "DATA_DTYPES": '{ "state_code": "str", "county_code": "str", "site_num": "str", "parameter_code": "int32", "poc": "int32",\n  "latitude": "str", "longitude": "str", "datum": "str", "parameter_name": "str", "date_local": "datetime64[ns]", "time_local": "str",\n  "date_gmt": "datetime64[ns]", "time_gmt": "str", "sample_measurement": "str", "units_of_measure": "str",\n  "mdl": "float64", "uncertainty": "str", "qualifier": "str", "method_type": "str", "method_code": "str",\n  "method_name": "str", "state_name": "str", "date_of_last_change": "datetime64[ns]" }',
            "OUTPUT_CSV_HEADERS": '[ "state_code", "county_code", "site_num", "parameter_code", "poc",\n  "latitude", "longitude", "datum", "parameter_name", "date_local",\n  "time_local", "date_gmt", "time_gmt", "sample_measurement", "units_of_measure",\n  "mdl", "uncertainty", "qualifier", "method_type", "method_code",\n  "method_name", "state_name", "county_name", "date_of_last_change" ]',
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
        name="epa-hist-air-quality--co_hourly",
    )

    create_cluster >> transform_csv_and_load_data >> delete_cluster
