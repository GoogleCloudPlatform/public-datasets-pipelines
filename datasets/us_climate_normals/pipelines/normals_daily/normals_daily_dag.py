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
    dag_id="us_climate_normals.normals_daily",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 2 * * *",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "us-climate-normals-daily",
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
    daily_load = kubernetes_engine.GKEStartPodOperator(
        task_id="daily_load",
        startup_timeout_seconds=600,
        name="load_us_climate_normals",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="us-climate-normals-daily",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.us_climate_normals.container_registry.dataset_id }}",
            "CHUNKSIZE": "500000",
            "CURRENT_DATA_TABLE_ID": "{{ var.json.us_climate_normals.normals_daily.destination_dataset_table_current }}",
            "HISTORICAL_DATA_TABLE_ID": "{{ var.json.us_climate_normals.normals_daily.destination_dataset_table_historical }}",
            "DATA_FILE_SURR_KEY_FIELD": "{{ var.json.us_climate_normals.normals_daily.data_file_surr_key_field }}",
            "DEST_FOLDER": "{{ var.json.us_climate_normals.container_registry.dest_folder }}",
            "SCHEMA_FILEPATH": "{{ var.json.us_climate_normals.normals_daily.schema_filepath }}",
            "SOURCE_BUCKET": "{{ var.json.us_climate_normals.container_registry.source_gcs_bucket }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CURRENT_DATA_TARGET_GCS_PATH": "{{ var.json.us_climate_normals.normals_daily.current_data_target_gcs_path }}",
            "HISTORICAL_DATA_TARGET_GCS_PATH": "{{ var.json.us_climate_normals.normals_daily.historical_data_target_gcs_path }}",
            "DEST_CURRENT_DATA_FOLDER_NAME": "{{ var.json.us_climate_normals.container_registry.dest_current_data_folder_name }}",
            "DEST_HISTORICAL_FOLDER_NAME": "{{ var.json.us_climate_normals.container_registry.dest_historical_data_folder_name }}",
            "SOURCE_BUCKET_CURRENT_DATA_FOLDER_NAME": "{{ var.json.us_climate_normals.normals_daily.source_bucket_current_data_folder_name }}",
            "DATA_ROOT_FOLDER": "normals-daily",
            "HIST_FOLDERS_LIST": '["1981-2010", "1991-2020", "2006-2020"]',
            "PIPELINE_NAME": "US Climate Normals Daily Load",
            "INPUT_CSV_HEADERS": '[ "station",\n  "date",\n  "latitude",\n  "longitude",\n  "elevation",\n  "name",\n  "dly_prcp_25pctl", "dly_prcp_25pctl_attributes",\n  "dly_prcp_50pctl", "dly_prcp_50pctl_attributes",\n  "dly_prcp_75pctl", "dly_prcp_75pctl_attributes",\n  "dly_prcp_pctall_ge001hi", "dly_prcp_pctall_ge001hi_attributes",\n  "dly_prcp_pctall_ge010hi", "dly_prcp_pctall_ge010hi_attributes",\n  "dly_prcp_pctall_ge050hi", "dly_prcp_pctall_ge050hi_attributes",\n  "dly_prcp_pctall_ge100hi", "dly_prcp_pctall_ge100hi_attributes",\n  "dly_snow_pctall_ge001ti", "dly_snow_pctall_ge001ti_attributes",\n  "dly_snow_pctall_ge010ti", "dly_snow_pctall_ge010ti_attributes",\n  "dly_snow_pctall_ge030ti", "dly_snow_pctall_ge030ti_attributes",\n  "dly_snow_pctall_ge050ti", "dly_snow_pctall_ge050ti_attributes",\n  "dly_snow_pctall_ge100ti", "dly_snow_pctall_ge100ti_attributes",\n  "dly_snwd_pctall_ge001wi", "dly_snwd_pctall_ge001wi_attributes",\n  "dly_snwd_pctall_ge003wi", "dly_snwd_pctall_ge003wi_attributes",\n  "dly_snwd_pctall_ge005wi", "dly_snwd_pctall_ge005wi_attributes",\n  "dly_snwd_pctall_ge010wi", "dly_snwd_pctall_ge010wi_attributes",\n  "mtd_prcp_normal", "mtd_prcp_normal_attributes",\n  "mtd_snow_normal", "mtd_snow_normal_attributes",\n  "ytd_prcp_normal", "ytd_prcp_normal_attributes",\n  "ytd_snow_normal", "ytd_snow_normal_attributes" ]',
            "DATA_DTYPE": '{ "station": "str", "date": "str",\n  "latitude": "float64", "longitude": "float64",\n  "elevation": "float64", "name": "str",\n  "dly_prcp_25pctl": "str", "dly_prcp_25pctl_attributes": "str",\n  "dly_prcp_50pctl": "str", "dly_prcp_50pctl_attributes": "str",\n  "dly_prcp_75pctl": "str", "dly_prcp_75pctl_attributes": "str",\n  "dly_prcp_pctall_ge001hi": "str", "dly_prcp_pctall_ge001hi_attributes": "str",\n  "dly_prcp_pctall_ge010hi": "str", "dly_prcp_pctall_ge010hi_attributes": "str",\n  "dly_prcp_pctall_ge050hi": "str", "dly_prcp_pctall_ge050hi_attributes": "str",\n  "dly_prcp_pctall_ge100hi": "str", "dly_prcp_pctall_ge100hi_attributes": "str",\n  "dly_snow_pctall_ge001ti": "str", "dly_snow_pctall_ge001ti_attributes": "str",\n  "dly_snow_pctall_ge010ti": "str", "dly_snow_pctall_ge010ti_attributes": "str",\n  "dly_snow_pctall_ge030ti": "str", "dly_snow_pctall_ge030ti_attributes": "str",\n  "dly_snow_pctall_ge050ti": "str", "dly_snow_pctall_ge050ti_attributes": "str",\n  "dly_snow_pctall_ge100ti": "str", "dly_snow_pctall_ge100ti_attributes": "str",\n  "dly_snwd_pctall_ge001wi": "str", "dly_snwd_pctall_ge001wi_attributes": "str",\n  "dly_snwd_pctall_ge003wi": "str", "dly_snwd_pctall_ge003wi_attributes": "str",\n  "dly_snwd_pctall_ge005wi": "str", "dly_snwd_pctall_ge005wi_attributes": "str",\n  "dly_snwd_pctall_ge010wi": "str", "dly_snwd_pctall_ge010wi_attributes": "str",\n  "mtd_prcp_normal": "str", "mtd_prcp_normal_attributes": "str",\n  "mtd_snow_normal": "str", "mtd_snow_normal_attributes": "str",\n  "ytd_prcp_normal": "str", "ytd_prcp_normal_attributes": "str",\n  "ytd_snow_normal": "str", "ytd_snow_normal_attributes": "str" ]',
            "INT_COL_LIST": '[ "dly_prcp_25pctl",\n  "dly_prcp_50pctl",\n  "dly_prcp_75pctl",\n  "dly_prcp_pctall_ge001hi",\n  "dly_prcp_pctall_ge010hi",\n  "dly_prcp_pctall_ge050hi",\n  "dly_prcp_pctall_ge100hi",\n  "dly_snow_pctall_ge001ti",\n  "dly_snow_pctall_ge010ti",\n  "dly_snow_pctall_ge030ti",\n  "dly_snow_pctall_ge050ti",\n  "dly_snow_pctall_ge100ti",\n  "dly_snwd_pctall_ge001wi",\n  "dly_snwd_pctall_ge003wi",\n  "dly_snwd_pctall_ge005wi",\n  "dly_snwd_pctall_ge010wi",\n  "mtd_prcp_normal",\n  "mtd_snow_normal",\n  "ytd_prcp_normal",\n  "ytd_snow_normal" ]',
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
        name="us-climate-normals-daily",
    )

    create_cluster >> daily_load >> delete_cluster
