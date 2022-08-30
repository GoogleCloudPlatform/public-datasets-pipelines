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
            "INPUT_CSV_HEADERS": '[ "station", "date",\n  "latitude", "longitude",\n  "elevation", "name",\n  "hly-cldh-normal", "hly-cldh-normal_attributes",\n  "hly-clod-pctbkn", "hly-clod-pctbkn_attributes",\n  "hly-clod-pctclr", "hly-clod-pctclr_attributes",\n  "hly-clod-pctfew", "hly-clod-pctfew_attributes",\n  "hly-clod-pctovc", "hly-clod-pctovc_attributes",\n  "hly-clod-pctsct","hly-clod-pctsct_attributes",\n  "hly-dewp-10pctl","hly-dewp-10pctl_attributes",\n  "hly-dewp-90pctl","hly-dewp-90pctl_attributes",\n  "hly-dewp-normal","hly-dewp-normal_attributes",\n  "hly-hidx-normal","hly-hidx-normal_attributes",\n  "hly-htdh-normal","hly-htdh-normal_attributes",\n  "hly-pres-10pctl","hly-pres-10pctl_attributes",\n  "hly-pres-90pctl","hly-pres-90pctl_attributes",\n  "hly-pres-normal","hly-pres-normal_attributes",\n  "hly-temp-10pctl","hly-temp-10pctl_attributes",\n  "hly-temp-90pctl","hly-temp-90pctl_attributes",\n  "hly-temp-normal","hly-temp-normal_attributes",\n  "hly-wchl-normal","hly-wchl-normal_attributes",\n  "hly-wind-1stdir","hly-wind-1stdir_attributes",\n  "hly-wind-1stpct","hly-wind-1stpct_attributes",\n  "hly-wind-2nddir","hly-wind-2nddir_attributes",\n  "hly-wind-2ndpct","hly-wind-2ndpct_attributes",\n  "hly-wind-avgspd","hly-wind-avgspd_attributes",\n  "hly-wind-pctclm","hly-wind-pctclm_attributes",\n  "hly-wind-vctdir","hly-wind-vctdir_attributes",\n  "hly-wind-vctspd","hly-wind-vctspd_attributes" ]',
            "DATA_DTYPE": '{ "station": "str", "date": "str",\n  "latitude": "float64", "longitude": "float64",\n  "elevation": "float64", "name": "str",\n  "hly-cldh-normal": "str", "hly-cldh-normal_attributes": "str",\n  "hly-clod-pctbkn": "str", "hly-clod-pctbkn_attributes": "str",\n  "hly-clod-pctclr": "str", "hly-clod-pctclr_attributes": "str",\n  "hly-clod-pctfew": "str", "hly-clod-pctfew_attributes": "str",\n  "hly-clod-pctovc": "str", "hly-clod-pctovc_attributes": "str",\n  "hly-clod-pctsct": "str","hly-clod-pctsct_attributes": "str",\n  "hly-dewp-10pctl": "str","hly-dewp-10pctl_attributes": "str",\n  "hly-dewp-90pctl": "str","hly-dewp-90pctl_attributes": "str",\n  "hly-dewp-normal": "str","hly-dewp-normal_attributes": "str",\n  "hly-hidx-normal": "str","hly-hidx-normal_attributes": "str",\n  "hly-htdh-normal": "str","hly-htdh-normal_attributes": "str",\n  "hly-pres-10pctl": "str","hly-pres-10pctl_attributes": "str",\n  "hly-pres-90pctl": "str","hly-pres-90pctl_attributes": "str",\n  "hly-pres-normal": "str","hly-pres-normal_attributes": "str",\n  "hly-temp-10pctl": "str","hly-temp-10pctl_attributes": "str",\n  "hly-temp-90pctl": "str","hly-temp-90pctl_attributes": "str",\n  "hly-temp-normal": "str","hly-temp-normal_attributes": "str",\n  "hly-wchl-normal": "str","hly-wchl-normal_attributes": "str",\n  "hly-wind-1stdir": "str","hly-wind-1stdir_attributes": "str",\n  "hly-wind-1stpct": "str","hly-wind-1stpct_attributes": "str",\n  "hly-wind-2nddir": "str","hly-wind-2nddir_attributes": "str",\n  "hly-wind-2ndpct": "str","hly-wind-2ndpct_attributes": "str",\n  "hly-wind-avgspd": "str","hly-wind-avgspd_attributes": "str",\n  "hly-wind-pctclm": "str","hly-wind-pctclm_attributes": "str",\n  "hly-wind-vctdir": "str","hly-wind-vctdir_attributes": "str",\n  "hly-wind-vctspd": "str","hly-wind-vctspd_attributes": "str" }',
            "INT_COL_LIST": '[ "hly-cldh-normal",\n  "hly-clod-pctbkn",\n  "hly-clod-pctclr",\n  "hly-clod-pctfew",\n  "hly-clod-pctovc",\n  "hly-clod-pctsct",\n  "hly-dewp-10pctl",\n  "hly-dewp-90pctl",\n  "hly-dewp-normal",\n  "hly-hidx-normal",\n  "hly-htdh-normal",\n  "hly-pres-10pctl",\n  "hly-pres-90pctl",\n  "hly-pres-normal",\n  "hly-temp-10pctl",\n  "hly-temp-90pctl",\n  "hly-temp-normal",\n  "hly-wchl-normal",\n  "hly-wind-1stdir",\n  "hly-wind-1stpct",\n  "hly-wind-2nddir",\n  "hly-wind-2ndpct",\n  "hly-wind-avgspd",\n  "hly-wind-pctclm",\n  "hly-wind-vctdir",\n  "hly-wind-vctspd" ]',
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
