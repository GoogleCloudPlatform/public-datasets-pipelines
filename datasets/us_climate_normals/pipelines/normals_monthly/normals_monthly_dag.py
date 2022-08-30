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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="us_climate_normals.normals_monthly",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 1 1 * *",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "us-climate-normals-monthly",
            "initial_node_count": 2,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-4",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    monthly_load = kubernetes_engine.GKEStartPodOperator(
        task_id="monthly_load",
        startup_timeout_seconds=600,
        name="load_us_climate_normals",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="us-climate-normals-monthly",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.us_climate_normals.container_registry.dataset_id }}",
            "CHUNKSIZE": "500000",
            "CURRENT_DATA_TABLE_ID": "{{ var.json.us_climate_normals.normals_monthly.destination_dataset_table_current }}",
            "HISTORICAL_DATA_TABLE_ID": "{{ var.json.us_climate_normals.normals_monthly.destination_dataset_table_historical }}",
            "DATA_FILE_SURR_KEY_FIELD": "{{ var.json.us_climate_normals.normals_monthly.data_file_surr_key_field }}",
            "DEST_FOLDER": "{{ var.json.us_climate_normals.container_registry.dest_folder }}",
            "SCHEMA_FILEPATH": "{{ var.json.us_climate_normals.normals_monthly.schema_filepath }}",
            "SOURCE_BUCKET": "{{ var.json.us_climate_normals.container_registry.source_gcs_bucket }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CURRENT_DATA_TARGET_GCS_PATH": "{{ var.json.us_climate_normals.normals_monthly.current_data_target_gcs_path }}",
            "HISTORICAL_DATA_TARGET_GCS_PATH": "{{ var.json.us_climate_normals.normals_monthly.historical_data_target_gcs_path }}",
            "DEST_CURRENT_DATA_FOLDER_NAME": "{{ var.json.us_climate_normals.container_registry.dest_current_data_folder_name }}",
            "DEST_HISTORICAL_FOLDER_NAME": "{{ var.json.us_climate_normals.container_registry.dest_historical_data_folder_name }}",
            "SOURCE_BUCKET_CURRENT_DATA_FOLDER_NAME": "{{ var.json.us_climate_normals.normals_monthly.source_bucket_current_data_folder_name }}",
            "DATA_ROOT_FOLDER": "normals-monthly",
            "HIST_FOLDERS_LIST": '["1981-2010", "1991-2020", "2006-2020"]',
            "PIPELINE_NAME": "US Climate Normals Monthly Load",
            "INPUT_CSV_HEADERS": '[ "station",\n  "date",\n  "latitude",\n  "longitude",\n  "elevation",\n  "name",\n  "mly-prcp-25pctl", "mly-prcp-25pctl_attributes",\n  "mly-prcp-50pctl", "mly-prcp-50pctl_attributes",\n  "mly-prcp-75pctl", "mly-prcp-75pctl_attributes",\n  "mly-prcp-avgnds-ge001hi", "mly-prcp-avgnds-ge001hi_attributes",\n  "mly-prcp-avgnds-ge010hi", "mly-prcp-avgnds-ge010hi_attributes",\n  "mly-prcp-avgnds-ge050hi", "mly-prcp-avgnds-ge050hi_attributes",\n  "mly-prcp-avgnds-ge100hi", "mly-prcp-avgnds-ge100hi_attributes",\n  "mly-prcp-normal", "mly-prcp-normal_attributes",\n  "mly-snow-25pctl", "mly-snow-25pctl_attributes",\n  "mly-snow-50pctl", "mly-snow-50pctl_attributes",\n  "mly-snow-75pctl", "mly-snow-75pctl_attributes",\n  "mly-snow-avgnds-ge001ti", "mly-snow-avgnds-ge001ti_attributes",\n  "mly-snow-avgnds-ge010ti", "mly-snow-avgnds-ge010ti_attributes",\n  "mly-snow-avgnds-ge030ti", "mly-snow-avgnds-ge030ti_attributes",\n  "mly-snow-avgnds-ge050ti", "mly-snow-avgnds-ge050ti_attributes",\n  "mly-snow-avgnds-ge100ti", "mly-snow-avgnds-ge100ti_attributes",\n  "mly-snow-normal", "mly-snow-normal_attributes",\n  "mly-snwd-avgnds-ge001wi", "mly-snwd-avgnds-ge001wi_attributes",\n  "mly-snwd-avgnds-ge003wi", "mly-snwd-avgnds-ge003wi_attributes",\n  "mly-snwd-avgnds-ge005wi", "mly-snwd-avgnds-ge005wi_attributes",\n  "mly-snwd-avgnds-ge010wi", "mly-snwd-avgnds-ge010wi_attributes" ]',
            "DATA_DTYPE": '{ "station": "str", "date": "str",\n  "latitude": "float64", "longitude": "float64",\n  "elevation": "float64", "name": "str",\n  "mly-prcp-25pctl": "str", "mly-prcp-25pctl_attributes": "str",\n  "mly-prcp-50pctl": "str", "mly-prcp-50pctl_attributes": "str",\n  "mly-prcp-75pctl": "str", "mly-prcp-75pctl_attributes": "str",\n  "mly-prcp-avgnds-ge001hi": "str", "mly-prcp-avgnds-ge001hi_attributes": "str",\n  "mly-prcp-avgnds-ge010hi": "str", "mly-prcp-avgnds-ge010hi_attributes": "str",\n  "mly-prcp-avgnds-ge050hi": "str", "mly-prcp-avgnds-ge050hi_attributes": "str",\n  "mly-prcp-avgnds-ge100hi": "str", "mly-prcp-avgnds-ge100hi_attributes": "str",\n  "mly-prcp-normal": "str", "mly-prcp-normal_attributes": "str",\n  "mly-snow-25pctl": "str", "mly-snow-25pctl_attributes": "str",\n  "mly-snow-50pctl": "str", "mly-snow-50pctl_attributes": "str",\n  "mly-snow-75pctl": "str", "mly-snow-75pctl_attributes": "str",\n  "mly-snow-avgnds-ge001ti": "str", "mly-snow-avgnds-ge001ti_attributes": "str",\n  "mly-snow-avgnds-ge010ti": "str", "mly-snow-avgnds-ge010ti_attributes": "str",\n  "mly-snow-avgnds-ge030ti": "str", "mly-snow-avgnds-ge030ti_attributes": "str",\n  "mly-snow-avgnds-ge050ti": "str", "mly-snow-avgnds-ge050ti_attributes": "str",\n  "mly-snow-avgnds-ge100ti": "str", "mly-snow-avgnds-ge100ti_attributes": "str",\n  "mly-snow-normal": "str", "mly-snow-normal_attributes": "str",\n  "mly-snwd-avgnds-ge001wi": "str", "mly-snwd-avgnds-ge001wi_attributes": "str",\n  "mly-snwd-avgnds-ge003wi": "str", "mly-snwd-avgnds-ge003wi_attributes": "str",\n  "mly-snwd-avgnds-ge005wi": "str", "mly-snwd-avgnds-ge005wi_attributes": "str",\n  "mly-snwd-avgnds-ge010wi": "str", "mly-snwd-avgnds-ge010wi_attributes": "str" ]',
            "INT_COL_LIST": '[ "mly-prcp-25pctl",\n  "mly-prcp-50pctl",\n  "mly-prcp-75pctl",\n  "mly-prcp-avgnds-ge001hi",\n  "mly-prcp-avgnds-ge010hi",\n  "mly-prcp-avgnds-ge050hi",\n  "mly-prcp-avgnds-ge100hi",\n  "mly-prcp-normal",\n  "mly-snow-25pctl",\n  "mly-snow-50pctl",\n  "mly-snow-75pctl",\n  "mly-snow-avgnds-ge001ti",\n  "mly-snow-avgnds-ge010ti",\n  "mly-snow-avgnds-ge030ti",\n  "mly-snow-avgnds-ge050ti",\n  "mly-snow-avgnds-ge100ti",\n  "mly-snow-normal",\n  "mly-snwd-avgnds-ge001wi",\n  "mly-snwd-avgnds-ge003wi",\n  "mly-snwd-avgnds-ge005wi",\n  "mly-snwd-avgnds-ge010wi" ]',
        },
        resources={
            "request_memory": "12G",
            "request_cpu": "1",
            "request_ephemeral_storage": "16G",
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="us-climate-normals-monthly",
    )

    create_cluster >> monthly_load >> delete_cluster
