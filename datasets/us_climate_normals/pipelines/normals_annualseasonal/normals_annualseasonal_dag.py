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
    dag_id="us_climate_normals.normals_annualseasonal",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 3 1 */3 *",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "us-climate-normals-annualseasonal",
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
    annualseasonal_load = kubernetes_engine.GKEStartPodOperator(
        task_id="annualseasonal_load",
        startup_timeout_seconds=600,
        name="load_us_climate_normals",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="us-climate-normals-annualseasonal",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.us_climate_normals.container_registry.dataset_id }}",
            "CHUNKSIZE": "500000",
            "CURRENT_DATA_TABLE_ID": "{{ var.json.us_climate_normals.normals_annualseasonal.destination_dataset_table_current }}",
            "HISTORICAL_DATA_TABLE_ID": "{{ var.json.us_climate_normals.normals_annualseasonal.destination_dataset_table_historical }}",
            "DATA_FILE_SURR_KEY_FIELD": "{{ var.json.us_climate_normals.normals_annualseasonal.data_file_surr_key_field }}",
            "DEST_FOLDER": "{{ var.json.us_climate_normals.container_registry.dest_folder }}",
            "SCHEMA_FILEPATH": "{{ var.json.us_climate_normals.normals_annualseasonal.schema_filepath }}",
            "SOURCE_BUCKET": "{{ var.json.us_climate_normals.container_registry.source_gcs_bucket }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CURRENT_DATA_TARGET_GCS_PATH": "{{ var.json.us_climate_normals.normals_annualseasonal.current_data_target_gcs_path }}",
            "HISTORICAL_DATA_TARGET_GCS_PATH": "{{ var.json.us_climate_normals.normals_annualseasonal.historical_data_target_gcs_path }}",
            "DEST_CURRENT_DATA_FOLDER_NAME": "{{ var.json.us_climate_normals.container_registry.dest_current_data_folder_name }}",
            "DEST_HISTORICAL_FOLDER_NAME": "{{ var.json.us_climate_normals.container_registry.dest_historical_data_folder_name }}",
            "SOURCE_BUCKET_CURRENT_DATA_FOLDER_NAME": "{{ var.json.us_climate_normals.normals_annualseasonal.source_bucket_current_data_folder_name }}",
            "DATA_ROOT_FOLDER": "normals-annualseasonal",
            "HIST_FOLDERS_LIST": '["1981-2010", "1991-2020", "2006-2020"]',
            "PIPELINE_NAME": "US Climate Normals Hourly Load",
            "INPUT_CSV_HEADERS": '[ "station",\n  "latitude",\n  "longitude",\n  "elevation",\n  "name",\n  "ann-prcp-avgnds-ge001hi", "ann-prcp-avgnds-ge001hi_attributes",\n  "ann-prcp-avgnds-ge010hi", "ann-prcp-avgnds-ge010hi_attributes",\n  "ann-prcp-avgnds-ge050hi", "ann-prcp-avgnds-ge050hi_attributes",\n  "ann-prcp-avgnds-ge100hi", "ann-prcp-avgnds-ge100hi_attributes",\n  "ann-prcp-normal", "ann-prcp-normal_attributes",\n  "ann-snow-avgnds-ge001ti", "ann-snow-avgnds-ge001ti_attributes",\n  "ann-snow-avgnds-ge010ti", "ann-snow-avgnds-ge010ti_attributes",\n  "ann-snow-avgnds-ge030ti", "ann-snow-avgnds-ge030ti_attributes",\n  "ann-snow-avgnds-ge050ti", "ann-snow-avgnds-ge050ti_attributes",\n  "ann-snow-avgnds-ge100ti", "ann-snow-avgnds-ge100ti_attributes",\n  "ann-snow-normal", "ann-snow-normal_attributes",\n  "djf-prcp-avgnds-ge001hi", "djf-prcp-avgnds-ge001hi_attributes",\n  "djf-prcp-avgnds-ge010hi", "djf-prcp-avgnds-ge010hi_attributes",\n  "djf-prcp-avgnds-ge050hi", "djf-prcp-avgnds-ge050hi_attributes",\n  "djf-prcp-avgnds-ge100hi", "djf-prcp-avgnds-ge100hi_attributes",\n  "djf-prcp-normal", "djf-prcp-normal_attributes",\n  "djf-snow-avgnds-ge001ti", "djf-snow-avgnds-ge001ti_attributes",\n  "djf-snow-avgnds-ge010ti", "djf-snow-avgnds-ge010ti_attributes",\n  "djf-snow-avgnds-ge030ti", "djf-snow-avgnds-ge030ti_attributes",\n  "djf-snow-avgnds-ge050ti", "djf-snow-avgnds-ge050ti_attributes",\n  "djf-snow-avgnds-ge100ti", "djf-snow-avgnds-ge100ti_attributes",\n  "djf-snow-normal", "djf-snow-normal_attributes",\n  "djf-snwd-avgnds-ge001wi", "djf-snwd-avgnds-ge001wi_attributes",\n  "djf-snwd-avgnds-ge003wi", "djf-snwd-avgnds-ge003wi_attributes",\n  "djf-snwd-avgnds-ge005wi", "djf-snwd-avgnds-ge005wi_attributes",\n  "djf-snwd-avgnds-ge010wi", "djf-snwd-avgnds-ge010wi_attributes",\n  "jja-prcp-avgnds-ge001hi", "jja-prcp-avgnds-ge001hi_attributes",\n  "jja-prcp-avgnds-ge010hi", "jja-prcp-avgnds-ge010hi_attributes",\n  "jja-prcp-avgnds-ge050hi", "jja-prcp-avgnds-ge050hi_attributes",\n  "jja-prcp-avgnds-ge100hi", "jja-prcp-avgnds-ge100hi_attributes",\n  "jja-prcp-normal", "jja-prcp-normal_attributes",\n  "jja-snow-avgnds-ge001ti", "jja-snow-avgnds-ge001ti_attributes",\n  "jja-snow-avgnds-ge010ti", "jja-snow-avgnds-ge010ti_attributes",\n  "jja-snow-avgnds-ge030ti", "jja-snow-avgnds-ge030ti_attributes",\n  "jja-snow-avgnds-ge050ti", "jja-snow-avgnds-ge050ti_attributes",\n  "jja-snow-avgnds-ge100ti", "jja-snow-avgnds-ge100ti_attributes",\n  "jja-snow-normal", "jja-snow-normal_attributes",\n  "jja-snwd-avgnds-ge001wi", "jja-snwd-avgnds-ge001wi_attributes",\n  "jja-snwd-avgnds-ge003wi", "jja-snwd-avgnds-ge003wi_attributes",\n  "jja-snwd-avgnds-ge005wi", "jja-snwd-avgnds-ge005wi_attributes",\n  "jja-snwd-avgnds-ge010wi", "jja-snwd-avgnds-ge010wi_attributes",\n  "mam-prcp-normal", "mam-prcp-normal_attributes",\n  "mam-snow-normal", "mam-snow-normal_attributes",\n  "mam-snwd-avgnds-ge005wi", "mam-snwd-avgnds-ge005wi_attributes",\n  "son-prcp-avgnds-ge001hi", "son-prcp-avgnds-ge001hi_attributes",\n  "son-prcp-avgnds-ge010hi", "son-prcp-avgnds-ge010hi_attributes",\n  "son-prcp-avgnds-ge050hi", "son-prcp-avgnds-ge050hi_attributes",\n  "son-prcp-avgnds-ge100hi", "son-prcp-avgnds-ge100hi_attributes",\n  "son-prcp-normal", "son-prcp-normal_attributes",\n  "son-snow-avgnds-ge001ti", "son-snow-avgnds-ge001ti_attributes",\n  "son-snow-avgnds-ge010ti", "son-snow-avgnds-ge010ti_attributes",\n  "son-snow-avgnds-ge030ti", "son-snow-avgnds-ge030ti_attributes",\n  "son-snow-avgnds-ge050ti", "son-snow-avgnds-ge050ti_attributes",\n  "son-snow-avgnds-ge100ti", "son-snow-avgnds-ge100ti_attributes",\n  "son-snow-normal", "son-snow-normal_attributes",\n  "son-snwd-avgnds-ge001wi", "son-snwd-avgnds-ge001wi_attributes",\n  "son-snwd-avgnds-ge003wi", "son-snwd-avgnds-ge003wi_attributes",\n  "son-snwd-avgnds-ge005wi", "son-snwd-avgnds-ge005wi_attributes",\n  "son-snwd-avgnds-ge010wi", "son-snwd-avgnds-ge010wi_attributes" ]',
            "DATA_DTYPE": '{ "station": "str", "date": "str",\n  "latitude": "float64", "longitude": "float64",\n  "elevation": "float64", "name": "str",\n  "ann-prcp-avgnds-ge001hi": "str", "ann-prcp-avgnds-ge001hi_attributes": "str",\n  "ann-prcp-avgnds-ge010hi": "str", "ann-prcp-avgnds-ge010hi_attributes": "str",\n  "ann-prcp-avgnds-ge050hi": "str", "ann-prcp-avgnds-ge050hi_attributes": "str",\n  "ann-prcp-avgnds-ge100hi": "str", "ann-prcp-avgnds-ge100hi_attributes": "str",\n  "ann-prcp-normal": "str", "ann-prcp-normal_attributes": "str",\n  "ann-snow-avgnds-ge001ti": "str", "ann-snow-avgnds-ge001ti_attributes": "str",\n  "ann-snow-avgnds-ge010ti": "str", "ann-snow-avgnds-ge010ti_attributes": "str",\n  "ann-snow-avgnds-ge030ti": "str", "ann-snow-avgnds-ge030ti_attributes": "str",\n  "ann-snow-avgnds-ge050ti": "str", "ann-snow-avgnds-ge050ti_attributes": "str",\n  "ann-snow-avgnds-ge100ti": "str", "ann-snow-avgnds-ge100ti_attributes": "str",\n  "ann-snow-normal": "str", "ann-snow-normal_attributes": "str",\n  "djf-prcp-avgnds-ge001hi": "str", "djf-prcp-avgnds-ge001hi_attributes": "str",\n  "djf-prcp-avgnds-ge010hi": "str", "djf-prcp-avgnds-ge010hi_attributes": "str",\n  "djf-prcp-avgnds-ge050hi": "str", "djf-prcp-avgnds-ge050hi_attributes": "str",\n  "djf-prcp-avgnds-ge100hi": "str", "djf-prcp-avgnds-ge100hi_attributes": "str",\n  "djf-prcp-normal": "str", "djf-prcp-normal_attributes": "str",\n  "djf-snow-avgnds-ge001ti": "str", "djf-snow-avgnds-ge001ti_attributes": "str",\n  "djf-snow-avgnds-ge010ti": "str", "djf-snow-avgnds-ge010ti_attributes": "str",\n  "djf-snow-avgnds-ge030ti": "str", "djf-snow-avgnds-ge030ti_attributes": "str",\n  "djf-snow-avgnds-ge050ti": "str", "djf-snow-avgnds-ge050ti_attributes": "str",\n  "djf-snow-avgnds-ge100ti": "str", "djf-snow-avgnds-ge100ti_attributes": "str",\n  "djf-snow-normal": "str", "djf-snow-normal_attributes": "str",\n  "djf-snwd-avgnds-ge001wi": "str", "djf-snwd-avgnds-ge001wi_attributes": "str",\n  "djf-snwd-avgnds-ge003wi": "str", "djf-snwd-avgnds-ge003wi_attributes": "str",\n  "djf-snwd-avgnds-ge005wi": "str", "djf-snwd-avgnds-ge005wi_attributes": "str",\n  "djf-snwd-avgnds-ge010wi": "str", "djf-snwd-avgnds-ge010wi_attributes": "str",\n  "jja-prcp-avgnds-ge001hi": "str", "jja-prcp-avgnds-ge001hi_attributes": "str",\n  "jja-prcp-avgnds-ge010hi": "str", "jja-prcp-avgnds-ge010hi_attributes": "str",\n  "jja-prcp-avgnds-ge050hi": "str", "jja-prcp-avgnds-ge050hi_attributes": "str",\n  "jja-prcp-avgnds-ge100hi": "str", "jja-prcp-avgnds-ge100hi_attributes": "str",\n  "jja-prcp-normal": "str", "jja-prcp-normal_attributes": "str",\n  "jja-snow-avgnds-ge001ti": "str", "jja-snow-avgnds-ge001ti_attributes": "str",\n  "jja-snow-avgnds-ge010ti": "str", "jja-snow-avgnds-ge010ti_attributes": "str",\n  "jja-snow-avgnds-ge030ti": "str", "jja-snow-avgnds-ge030ti_attributes": "str",\n  "jja-snow-avgnds-ge050ti": "str", "jja-snow-avgnds-ge050ti_attributes": "str",\n  "jja-snow-avgnds-ge100ti": "str", "jja-snow-avgnds-ge100ti_attributes": "str",\n  "jja-snow-normal": "str", "jja-snow-normal_attributes": "str",\n  "jja-snwd-avgnds-ge001wi": "str", "jja-snwd-avgnds-ge001wi_attributes": "str",\n  "jja-snwd-avgnds-ge003wi": "str", "jja-snwd-avgnds-ge003wi_attributes": "str",\n  "jja-snwd-avgnds-ge005wi": "str", "jja-snwd-avgnds-ge005wi_attributes": "str",\n  "jja-snwd-avgnds-ge010wi": "str", "jja-snwd-avgnds-ge010wi_attributes": "str",\n  "mam-prcp-normal": "str", "mam-prcp-normal_attributes": "str",\n  "mam-snow-normal": "str", "mam-snow-normal_attributes": "str",\n  "mam-snwd-avgnds-ge005wi": "str", "mam-snwd-avgnds-ge005wi_attributes": "str",\n  "son-prcp-avgnds-ge001hi": "str", "son-prcp-avgnds-ge001hi_attributes": "str",\n  "son-prcp-avgnds-ge010hi": "str", "son-prcp-avgnds-ge010hi_attributes": "str",\n  "son-prcp-avgnds-ge050hi": "str", "son-prcp-avgnds-ge050hi_attributes": "str",\n  "son-prcp-avgnds-ge100hi": "str", "son-prcp-avgnds-ge100hi_attributes": "str",\n  "son-prcp-normal": "str", "son-prcp-normal_attributes": "str",\n  "son-snow-avgnds-ge001ti": "str", "son-snow-avgnds-ge001ti_attributes": "str",\n  "son-snow-avgnds-ge010ti": "str", "son-snow-avgnds-ge010ti_attributes": "str",\n  "son-snow-avgnds-ge030ti": "str", "son-snow-avgnds-ge030ti_attributes": "str",\n  "son-snow-avgnds-ge050ti": "str", "son-snow-avgnds-ge050ti_attributes": "str",\n  "son-snow-avgnds-ge100ti": "str", "son-snow-avgnds-ge100ti_attributes": "str",\n  "son-snow-normal": "str", "son-snow-normal_attributes": "str",\n  "son-snwd-avgnds-ge001wi": "str", "son-snwd-avgnds-ge001wi_attributes": "str",\n  "son-snwd-avgnds-ge003wi": "str", "son-snwd-avgnds-ge003wi_attributes": "str",\n  "son-snwd-avgnds-ge005wi": "str", "son-snwd-avgnds-ge005wi_attributes": "str",\n  "son-snwd-avgnds-ge010wi": "str", "son-snwd-avgnds-ge010wi_attributes": "str" ]',
            "INT_COL_LIST": '[ "ann-prcp-avgnds-ge001hi",\n  "ann-prcp-avgnds-ge010hi",\n  "ann-prcp-avgnds-ge050hi",\n  "ann-prcp-avgnds-ge100hi",\n  "ann-prcp-normal",\n  "ann-snow-avgnds-ge001ti",\n  "ann-snow-avgnds-ge010ti",\n  "ann-snow-avgnds-ge030ti",\n  "ann-snow-avgnds-ge050ti",\n  "ann-snow-avgnds-ge100ti",\n  "ann-snow-normal",\n  "djf-prcp-avgnds-ge001hi",\n  "djf-prcp-avgnds-ge010hi",\n  "djf-prcp-avgnds-ge050hi",\n  "djf-prcp-avgnds-ge100hi",\n  "djf-prcp-normal",\n  "djf-snow-avgnds-ge001ti",\n  "djf-snow-avgnds-ge010ti",\n  "djf-snow-avgnds-ge030ti",\n  "djf-snow-avgnds-ge050ti",\n  "djf-snow-avgnds-ge100ti",\n  "djf-snow-normal",\n  "djf-snwd-avgnds-ge001wi",\n  "djf-snwd-avgnds-ge003wi",\n  "djf-snwd-avgnds-ge005wi",\n  "djf-snwd-avgnds-ge010wi",\n  "jja-prcp-avgnds-ge001hi",\n  "jja-prcp-avgnds-ge010hi",\n  "jja-prcp-avgnds-ge050hi",\n  "jja-prcp-avgnds-ge100hi",\n  "jja-prcp-normal",\n  "jja-snow-avgnds-ge001ti",\n  "jja-snow-avgnds-ge010ti",\n  "jja-snow-avgnds-ge030ti",\n  "jja-snow-avgnds-ge050ti",\n  "jja-snow-avgnds-ge100ti",\n  "jja-snow-normal",\n  "jja-snwd-avgnds-ge001wi",\n  "jja-snwd-avgnds-ge003wi",\n  "jja-snwd-avgnds-ge005wi",\n  "jja-snwd-avgnds-ge010wi",\n  "mam-prcp-normal",\n  "mam-snow-normal",\n  "mam-snwd-avgnds-ge005wi",\n  "son-prcp-avgnds-ge001hi",\n  "son-prcp-avgnds-ge010hi",\n  "son-prcp-avgnds-ge050hi",\n  "son-prcp-avgnds-ge100hi",\n  "son-prcp-normal",\n  "son-snow-avgnds-ge001ti",\n  "son-snow-avgnds-ge010ti",\n  "son-snow-avgnds-ge030ti",\n  "son-snow-avgnds-ge050ti",\n  "son-snow-avgnds-ge100ti",\n  "son-snow-normal",\n  "son-snwd-avgnds-ge001wi",\n  "son-snwd-avgnds-ge003wi",\n  "son-snwd-avgnds-ge005wi",\n  "son-snwd-avgnds-ge010wi" ]',
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
        name="us-climate-normals-annualseasonal",
    )

    create_cluster >> annualseasonal_load >> delete_cluster
