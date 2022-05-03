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
    dag_id="noaa.noaa",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 1 0 0 6",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "noaa",
            "initial_node_count": 2,
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

    # Run NOAA load processes
    ghcnd_by_year = kubernetes_engine.GKEStartPodOperator(
        task_id="ghcnd_by_year",
        name="noaa.ghcnd_by_year",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.ghcnd_by_year.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.ghcnd_by_year.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.ghcnd_by_year.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.ghcnd_by_year.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.ghcnd_by_year.chunksize }}",
            "FTP_HOST": "{{ var.json.noaa.ghcnd_by_year.ftp_host }}",
            "FTP_DIR": "{{ var.json.noaa.ghcnd_by_year.ftp_dir }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.ghcnd_by_year.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.ghcnd_by_year.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.ghcnd_by_year.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.ghcnd_by_year.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.ghcnd_by_year.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": ",",
            "FTP_BATCH_SIZE": "{{ var.json.noaa.ghcnd_by_year.ftp_batch_size }}",
            "FTP_BATCH_SLEEP_TIME": "{{ var.json.noaa.ghcnd_by_year.ftp_batch_sleep_time }}",
            "FULL_DATA_LOAD": "{{ var.json.noaa.ghcnd_by_year.full_data_load }}",
            "START_YEAR": "{{ var.json.noaa.ghcnd_by_year.start_year }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.ghcnd_by_year.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.ghcnd_by_year.delete_target_file }}",
            "INPUT_CSV_HEADERS": '[\n  "id",\n  "date",\n  "element",\n  "value",\n  "mflag",\n  "qflag",\n  "sflag",\n  "time"\n]',
            "DATA_DTYPES": '{\n  "id": "str",\n  "date": "str",\n  "element": "str",\n  "value": "str",\n  "mflag": "str",\n  "qflag": "str",\n  "sflag": "str",\n  "time": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "id",\n  "date",\n  "element",\n  "value",\n  "mflag",\n  "qflag",\n  "sflag",\n  "time",\n  "source_url",\n  "etl_timestamp"\n]',
            "NULL_ROWS_LIST": '[\n  "id"\n]',
            "DATE_FORMAT_LIST": '[\n  "date"\n]',
        },
        resources={"request_ephemeral_storage": "16G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    ghcnd_countries = kubernetes_engine.GKEStartPodOperator(
        task_id="ghcnd_countries",
        name="noaa.ghcnd_countries",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.ghcnd_countries.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.ghcnd_countries.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.ghcnd_countries.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.ghcnd_countries.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.ghcnd_countries.chunksize }}",
            "FTP_HOST": "{{ var.json.noaa.ghcnd_countries.ftp_host }}",
            "FTP_DIR": "{{ var.json.noaa.ghcnd_countries.ftp_dir }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.ghcnd_countries.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.ghcnd_countries.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.ghcnd_countries.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.ghcnd_countries.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.ghcnd_countries.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.ghcnd_countries.input_field_delimiter }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.ghcnd_countries.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.ghcnd_countries.delete_target_file }}",
            "INPUT_CSV_HEADERS": '[\n  "textdata"\n]',
            "DATA_DTYPES": '{\n  "textdata": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "code",\n  "name",\n  "source_url",\n  "etl_timestamp"\n]',
            "SLICE_COLUMN_LIST": '{\n  "code": ["textdata", "0", "2"],\n  "name": ["textdata", "3", ""]\n}',
        },
        resources={"request_ephemeral_storage": "4G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    ghcnd_inventory = kubernetes_engine.GKEStartPodOperator(
        task_id="ghcnd_inventory",
        name="noaa.ghcnd_inventory",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.ghcnd_inventory.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.ghcnd_inventory.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.ghcnd_inventory.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.ghcnd_inventory.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.ghcnd_inventory.chunksize }}",
            "FTP_HOST": "{{ var.json.noaa.ghcnd_inventory.ftp_host }}",
            "FTP_DIR": "{{ var.json.noaa.ghcnd_inventory.ftp_dir }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.ghcnd_inventory.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.ghcnd_inventory.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.ghcnd_inventory.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.ghcnd_inventory.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.ghcnd_inventory.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.ghcnd_inventory.input_field_delimiter }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.ghcnd_inventory.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.ghcnd_inventory.delete_target_file }}",
            "INPUT_CSV_HEADERS": '[\n  "textdata"\n]',
            "DATA_DTYPES": '{\n  "textdata": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "id",\n  "latitude",\n  "longitude",\n  "element",\n  "firstyear",\n  "lastyear",\n  "source_url",\n  "etl_timestamp"\n]',
            "SLICE_COLUMN_LIST": '{\n  "id": ["textdata", "0", "11"],\n  "latitude": ["textdata", "12", "20"],\n  "longitude": ["textdata", "21", "30"],\n  "element": ["textdata", "31", "35"],\n  "firstyear": ["textdata", "36", "40"],\n  "lastyear": ["textdata", "41", "45"]\n}',
        },
        resources={"request_ephemeral_storage": "4G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    ghcnd_states = kubernetes_engine.GKEStartPodOperator(
        task_id="ghcnd_states",
        name="noaa.ghcnd_states",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.ghcnd_states.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.ghcnd_states.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.ghcnd_states.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.ghcnd_states.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.ghcnd_states.chunksize }}",
            "FTP_HOST": "{{ var.json.noaa.ghcnd_states.ftp_host }}",
            "FTP_DIR": "{{ var.json.noaa.ghcnd_states.ftp_dir }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.ghcnd_states.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.ghcnd_states.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.ghcnd_states.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.ghcnd_states.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.ghcnd_states.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.ghcnd_states.input_field_delimiter }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.ghcnd_states.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.ghcnd_states.delete_target_file }}",
            "INPUT_CSV_HEADERS": '[\n  "textdata"\n]',
            "DATA_DTYPES": '{\n  "textdata": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "code",\n  "name",\n  "source_url",\n  "etl_timestamp"\n]',
            "SLICE_COLUMN_LIST": '{\n  "code": ["textdata", "0", "2"],\n  "name": ["textdata", "3", ""]\n}',
        },
        resources={"request_ephemeral_storage": "4G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    ghcnd_stations = kubernetes_engine.GKEStartPodOperator(
        task_id="ghcnd_stations",
        name="noaa.ghcnd_stations",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.ghcnd_stations.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.ghcnd_stations.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.ghcnd_stations.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.ghcnd_stations.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.ghcnd_stations.chunksize }}",
            "FTP_HOST": "{{ var.json.noaa.ghcnd_stations.ftp_host }}",
            "FTP_DIR": "{{ var.json.noaa.ghcnd_stations.ftp_dir }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.ghcnd_stations.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.ghcnd_stations.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.ghcnd_stations.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.ghcnd_stations.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.ghcnd_stations.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.ghcnd_stations.input_field_delimiter }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.ghcnd_stations.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.ghcnd_stations.delete_target_file }}",
            "INPUT_CSV_HEADERS": '[\n  "textdata"\n]',
            "DATA_DTYPES": '{\n  "textdata": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "id",\n  "latitude",\n  "longitude",\n  "elevation",\n  "state",\n  "name",\n  "gsn_flag",\n  "hcn_cm_flag",\n  "wmoid",\n  "source_url",\n  "etl_timestamp"\n]',
            "SLICE_COLUMN_LIST": '{\n  "id": ["textdata", "0", "11"],\n  "latitude": ["textdata", "12", "20"],\n  "longitude": ["textdata", "21", "30"],\n  "elevation": ["textdata", "31", "37"],\n  "state": ["textdata", "38", "40"],\n  "name": ["textdata", "41", "71"],\n  "gsn_flag": ["textdata", "72", "75"],\n  "hcn_cm_flag": ["textdata", "76", "79"],\n  "wmoid": ["textdata", "80", "85"]\n}',
        },
        resources={"request_ephemeral_storage": "4G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    gsod_stations = kubernetes_engine.GKEStartPodOperator(
        task_id="gsod_stations",
        name="noaa.gsod_stations",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.gsod_stations.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.gsod_stations.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.gsod_stations.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.gsod_stations.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.gsod_stations.chunksize }}",
            "FTP_HOST": "{{ var.json.noaa.gsod_stations.ftp_host }}",
            "FTP_DIR": "{{ var.json.noaa.gsod_stations.ftp_dir }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.gsod_stations.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.gsod_stations.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.gsod_stations.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.gsod_stations.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.gsod_stations.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.gsod_stations.input_field_delimiter }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.gsod_stations.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.gsod_stations.delete_target_file }}",
            "NUMBER_OF_HEADER_ROWS": "{{ var.json.noaa.gsod_stations.number_of_header_rows }}",
            "REGEX_LIST": '{\n  "lat": ["^(-[0]+)(.*)", "-$2", "True"],\n  "lat": ["^(\\\\s+)$", "", "True"],\n  "lat": ["^(\\\\+\\\\d+\\\\.\\\\d+[0-9])\\\\s+", "$1", "True"],\n  "lat": ["^(-\\\\d+\\\\.\\\\d+[0-9])\\\\s+", "$1", "True"],\n  "lat": ["nan", "", "False"],\n  "lon": ["^(-[0]+)(.*)", "-$2", "True"],\n  "lon": ["^(\\\\s+)$", "", "True"],\n  "lon": ["^(\\\\+\\\\d+\\\\.\\\\d+[0-9])\\\\s+", "$1", "True"],\n  "lon": ["^(-\\\\d+\\\\.\\\\d+[0-9])\\\\s+", "$1", "True"],\n  "lon": ["nan", "", "False"],\n  "usaf": ["(\\\\d{1,})(\\\\s{1,})$", "$1", "True"],\n  "name": ["^\\\\s{1,}([a-zA-Z]\\\\D+)", "$1", "True"],\n  "name": ["^(\\\\D+[a-zA-Z])\\\\s{1,}$", "$1", "True"],\n  "name": ["^(\\\\s+)$", "", "True"],\n  "call": ["^(\\\\s+)$", "", "True"],\n  "call": ["^([a-zA-Z]+)\\\\s+", "$1", "True"],\n  "elev": ["^(\\\\s+)$", "", "True"],\n  "state": ["^(\\\\s+)$", "", "True"],\n  "country": ["^(\\\\s+)$", "", "True"]\n}',
            "INPUT_CSV_HEADERS": '[\n  "textdata"\n]',
            "DATA_DTYPES": '{\n  "textdata": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "usaf",\n  "wban",\n  "name",\n  "country",\n  "state",\n  "call",\n  "lat",\n  "lon",\n  "elev",\n  "begin",\n  "end",\n  "source_url",\n  "etl_timestamp"\n]',
            "NULL_ROWS_LIST": '[\n  "usaf"\n]',
            "SLICE_COLUMN_LIST": '{\n  "usaf": ["textdata", "0", "6"],\n  "wban": ["textdata", "7", "12"],\n  "name": ["textdata", "13", "42"],\n  "country": ["textdata", "43", "45"],\n  "state": ["textdata", "48", "50"],\n  "call": ["textdata", "51", "56"],\n  "lat": ["textdata", "57", "64"],\n  "lon": ["textdata", "65", "74"],\n  "elev": ["textdata", "75", "81"],\n  "begin": ["textdata", "82", "90"],\n  "end": ["textdata", "91", "99"]\n}',
        },
        resources={"request_ephemeral_storage": "4G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    ghcnd_hurricanes = kubernetes_engine.GKEStartPodOperator(
        task_id="ghcnd_hurricanes",
        name="noaa.ghcnd_hurricanes",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.ghcnd_hurricanes.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.ghcnd_hurricanes.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.ghcnd_hurricanes.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.ghcnd_hurricanes.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.ghcnd_hurricanes.chunksize }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.ghcnd_hurricanes.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.ghcnd_hurricanes.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.ghcnd_hurricanes.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.ghcnd_hurricanes.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.ghcnd_hurricanes.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.ghcnd_hurricanes.input_field_delimiter }}",
            "NUMBER_OF_HEADER_ROWS": "{{ var.json.noaa.ghcnd_hurricanes.number_of_header_rows }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.ghcnd_hurricanes.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.ghcnd_hurricanes.delete_target_file }}",
            "INPUT_CSV_HEADERS": '[\n  "sid",\n  "season",\n  "number",\n  "basin",\n  "subbasin",\n  "name",\n  "iso_time",\n  "nature",\n  "lat",\n  "lon",\n  "wmo_wind",\n  "wmo_pres",\n  "wmo_agency",\n  "track_type",\n  "dist2land",\n  "landfall",\n  "iflag",\n  "usa_agency",\n  "usa_atcf_id",\n  "usa_lat",\n  "usa_lon",\n  "usa_record",\n  "usa_status",\n  "usa_wind",\n  "usa_pres",\n  "usa_sshs",\n  "usa_r34_ne",\n  "usa_r34_se",\n  "usa_r34_sw",\n  "usa_r34_nw",\n  "usa_r50_ne",\n  "usa_r50_se",\n  "usa_r50_sw",\n  "usa_r50_nw",\n  "usa_r64_ne",\n  "usa_r64_se",\n  "usa_r64_sw",\n  "usa_r64_nw",\n  "usa_poci",\n  "usa_roci",\n  "usa_rmw",\n  "usa_eye",\n  "tokyo_lat",\n  "tokyo_lon",\n  "tokyo_grade",\n  "tokyo_wind",\n  "tokyo_pres",\n  "tokyo_r50_dir",\n  "tokyo_r50_long",\n  "tokyo_r50_short",\n  "tokyo_r30_dir",\n  "tokyo_r30_long",\n  "tokyo_r30_short",\n  "tokyo_land",\n  "cma_lat",\n  "cma_lon",\n  "cma_cat",\n  "cma_wind",\n  "cma_pres",\n  "hko_lat",\n  "hko_lon",\n  "hko_cat",\n  "hko_wind",\n  "hko_pres",\n  "newdelhi_lat",\n  "newdelhi_lon",\n  "newdelhi_grade",\n  "newdelhi_wind",\n  "newdelhi_pres",\n  "newdelhi_ci",\n  "newdelhi_dp",\n  "newdelhi_poci",\n  "reunion_lat",\n  "reunion_lon",\n  "reunion_type",\n  "reunion_wind",\n  "reunion_pres",\n  "reunion_tnum",\n  "reunion_ci",\n  "reunion_rmw",\n  "reunion_r34_ne",\n  "reunion_r34_se",\n  "reunion_r34_sw",\n  "reunion_r34_nw",\n  "reunion_r50_ne",\n  "reunion_r50_se",\n  "reunion_r50_sw",\n  "reunion_r50_nw",\n  "reunion_r64_ne",\n  "reunion_r64_se",\n  "reunion_r64_sw",\n  "reunion_r64_nw",\n  "bom_lat",\n  "bom_lon",\n  "bom_type",\n  "bom_wind",\n  "bom_pres",\n  "bom_tnum",\n  "bom_ci",\n  "bom_rmw",\n  "bom_r34_ne",\n  "bom_r34_se",\n  "bom_r34_sw",\n  "bom_r34_nw",\n  "bom_r50_ne",\n  "bom_r50_se",\n  "bom_r50_sw",\n  "bom_r50_nw",\n  "bom_r64_ne",\n  "bom_r64_se",\n  "bom_r64_sw",\n  "bom_r64_nw",\n  "bom_roci",\n  "bom_poci",\n  "bom_eye",\n  "bom_pos_method",\n  "bom_pres_method",\n  "nadi_lat",\n  "nadi_lon",\n  "nadi_cat",\n  "nadi_wind",\n  "nadi_pres",\n  "wellington_lat",\n  "wellington_lon",\n  "wellington_wind",\n  "wellington_pres",\n  "ds824_lat",\n  "ds824_lon",\n  "ds824_stage",\n  "ds824_wind",\n  "ds824_pres",\n  "td9636_lat",\n  "td9636_lon",\n  "td9636_stage",\n  "td9636_wind",\n  "td9636_pres",\n  "td9635_lat",\n  "td9635_lon",\n  "td9635_wind",\n  "td9635_pres",\n  "td9635_roci",\n  "neumann_lat",\n  "neumann_lon",\n  "neumann_class",\n  "neumann_wind",\n  "neumann_pres",\n  "mlc_lat",\n  "mlc_lon",\n  "mlc_class",\n  "mlc_wind",\n  "mlc_pres",\n  "usa_gust",\n  "bom_gust",\n  "bom_gust_per",\n  "reunion_gust",\n  "reunion_gust_per",\n  "usa_seahgt",\n  "usa_searad_ne",\n  "usa_searad_se",\n  "usa_searad_sw",\n  "usa_searad_nw",\n  "storm_speed",\n  "storm_dir"\n]',
            "REORDER_HEADERS_LIST": '[\n  "sid",\n  "season",\n  "number",\n  "basin",\n  "subbasin",\n  "name",\n  "iso_time",\n  "nature",\n  "latitude",\n  "longitude",\n  "wmo_wind",\n  "wmo_pressure",\n  "wmo_agency",\n  "track_type",\n  "dist2land",\n  "landfall",\n  "iflag",\n  "usa_agency",\n  "usa_latitude",\n  "usa_longitude",\n  "usa_record",\n  "usa_status",\n  "usa_wind",\n  "usa_pressure",\n  "usa_sshs",\n  "usa_r34_ne",\n  "usa_r34_se",\n  "usa_r34_sw",\n  "usa_r34_nw",\n  "usa_r50_ne",\n  "usa_r50_se",\n  "usa_r50_sw",\n  "usa_r50_nw",\n  "usa_r64_ne",\n  "usa_r64_se",\n  "usa_r64_sw",\n  "usa_r64_nw",\n  "usa_poci",\n  "usa_roci",\n  "usa_rmw",\n  "usa_eye",\n  "tokyo_latitude",\n  "tokyo_longitude",\n  "tokyo_grade",\n  "tokyo_wind",\n  "tokyo_pressure",\n  "tokyo_r50_dir",\n  "tokyo_r50_longitude",\n  "tokyo_r50_short",\n  "tokyo_r30_dir",\n  "tokyo_r30_long",\n  "tokyo_r30_short",\n  "tokyo_land",\n  "cma_latitude",\n  "cma_longitude",\n  "cma_cat",\n  "cma_wind",\n  "cma_pressure",\n  "hko_latitude",\n  "hko_longitude",\n  "hko_cat",\n  "hko_wind",\n  "hko_pressure",\n  "newdelhi_latitude",\n  "newdelhi_longitude",\n  "newdelhi_grade",\n  "newdelhi_wind",\n  "newdelhi_pressure",\n  "newdelhi_ci",\n  "newdelhi_dp",\n  "newdelhi_poci",\n  "reunion_latitude",\n  "reunion_longitude",\n  "reunion_type",\n  "reunion_wind",\n  "reunion_pressure",\n  "reunion_tnum",\n  "reunion_ci",\n  "reunion_rmw",\n  "reunion_r34_ne",\n  "reunion_r34_se",\n  "reunion_r34_sw",\n  "reunion_r34_nw",\n  "reunion_r50_ne",\n  "reunion_r50_se",\n  "reunion_r50_sw",\n  "reunion_r50_nw",\n  "reunion_r64_ne",\n  "reunion_r64_se",\n  "reunion_r64_sw",\n  "reunion_r64_nw",\n  "bom_latitude",\n  "bom_longitude",\n  "bom_type",\n  "bom_wind",\n  "bom_pressure",\n  "bom_tnum",\n  "bom_ci",\n  "bom_rmw",\n  "bom_r34_ne",\n  "bom_r34_se",\n  "bom_r34_sw",\n  "bom_r34_nw",\n  "bom_r50_ne",\n  "bom_r50_se",\n  "bom_r50_sw",\n  "bom_r50_nw",\n  "bom_r64_ne",\n  "bom_r64_se",\n  "bom_r64_sw",\n  "bom_r64_nw",\n  "bom_roci",\n  "bom_poci",\n  "bom_eye",\n  "bom_pos_method",\n  "bom_pressure_method",\n  "wellington_latitude",\n  "wellington_longitude",\n  "wellington_wind",\n  "wellington_pressure",\n  "nadi_latitude",\n  "nadi_longitude",\n  "nadi_cat",\n  "nadi_wind",\n  "nadi_pressure",\n  "ds824_latitude",\n  "ds824_longitude",\n  "ds824_stage",\n  "ds824_wind",\n  "ds824_pressure",\n  "td9636_latitude",\n  "td9636_longitude",\n  "td9636_stage",\n  "td9636_wind",\n  "td9636_pressure",\n  "td9635_latitude",\n  "td9635_longitude",\n  "td9635_wind",\n  "td9635_pressure",\n  "td9635_roci",\n  "neumann_latitude",\n  "neumann_longitude",\n  "neumann_class",\n  "neumann_wind",\n  "neumann_pressure",\n  "mlc_latitude",\n  "mlc_longitude",\n  "mlc_class",\n  "mlc_wind",\n  "mlc_pressure",\n  "usa_atcf_id",\n  "source_url",\n  "etl_timestamp"\n]',
            "RENAME_HEADERS_LIST": '{\n  "lat": "latitude",\n  "lon": "longitude",\n  "wmo_pres": "wmo_pressure",\n  "usa_lat": "usa_latitude",\n  "usa_lon": "usa_longitude",\n  "usa_pres": "usa_pressure",\n  "tokyo_lat": "tokyo_latitude",\n  "tokyo_lon": "tokyo_longitude",\n  "tokyo_pres": "tokyo_pressure",\n  "tokyo_r50_long": "tokyo_r50_longitude",\n  "cma_lat": "cma_latitude",\n  "cma_lon": "cma_longitude",\n  "cma_pres": "cma_pressure",\n  "hko_lat": "hko_latitude",\n  "hko_lon": "hko_longitude",\n  "hko_pres": "hko_pressure",\n  "newdelhi_lat": "newdelhi_latitude",\n  "newdelhi_lon": "newdelhi_longitude",\n  "newdelhi_pres": "newdelhi_pressure",\n  "reunion_lat": "reunion_latitude",\n  "reunion_lon": "reunion_longitude",\n  "reunion_pres": "reunion_pressure",\n  "bom_lat": "bom_latitude",\n  "bom_lon": "bom_longitude",\n  "bom_pres": "bom_pressure",\n  "bom_pres_method": "bom_pressure_method",\n  "wellington_lat": "wellington_latitude",\n  "wellington_lon": "wellington_longitude",\n  "wellington_pres": "wellington_pressure",\n  "nadi_lat": "nadi_latitude",\n  "nadi_lon": "nadi_longitude",\n  "nadi_pres": "nadi_pressure",\n  "ds824_lat": "ds824_latitude",\n  "ds824_lon": "ds824_longitude",\n  "ds824_pres": "ds824_pressure",\n  "td9636_lat": "td9636_latitude",\n  "td9636_lon": "td9636_longitude",\n  "td9636_pres": "td9636_pressure",\n  "td9635_lat": "td9635_latitude",\n  "td9635_lon": "td9635_longitude",\n  "td9635_pres": "td9635_pressure",\n  "neumann_lat": "neumann_latitude",\n  "neumann_lon": "neumann_longitude",\n  "neumann_pres": "neumann_pressure",\n  "mlc_lat": "mlc_latitude",\n  "mlc_lon": "mlc_longitude",\n  "mlc_pres": "mlc_pressure"\n}',
        },
        resources={"request_ephemeral_storage": "16G", "limit_cpu": "3"},
    )

    # Run NOAA load processes
    lightning_strikes_by_year = kubernetes_engine.GKEStartPodOperator(
        task_id="lightning_strikes_by_year",
        name="noaa.lightning_strikes_by_year",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="noaa",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "{{ var.json.noaa.lightning_strikes_by_year.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.noaa.lightning_strikes_by_year.source_url }}",
            "SOURCE_FILE": "{{ var.json.noaa.lightning_strikes_by_year.source_file }}",
            "TARGET_FILE": "{{ var.json.noaa.lightning_strikes_by_year.target_file }}",
            "CHUNKSIZE": "{{ var.json.noaa.lightning_strikes_by_year.chunksize }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.noaa.lightning_strikes_by_year.dataset_id }}",
            "TABLE_ID": "{{ var.json.noaa.lightning_strikes_by_year.table_id }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.lightning_strikes_by_year.target_gcs_path }}",
            "SCHEMA_PATH": "{{ var.json.noaa.lightning_strikes_by_year.schema_path }}",
            "DROP_DEST_TABLE": "{{ var.json.noaa.lightning_strikes_by_year.drop_dest_table }}",
            "INPUT_FIELD_DELIMITER": "{{ var.json.noaa.lightning_strikes_by_year.input_field_delimiter }}",
            "REMOVE_SOURCE_FILE": "{{ var.json.noaa.lightning_strikes_by_year.remove_source_file }}",
            "DELETE_TARGET_FILE": "{{ var.json.noaa.lightning_strikes_by_year.delete_target_file }}",
            "START_YEAR": "{{ var.json.noaa.lightning_strikes_by_year.start_year }}",
            "NUMBER_OF_HEADER_ROWS": "{{ var.json.noaa.lightning_strikes_by_year.number_of_header_rows }}",
            "INT_DATE_LIST": '{\n  "date": "day_int"\n}',
            "GEN_LOCATION_LIST": '{\n  "center_point_geom": ["centerlon", "centerlat"]\n}',
            "INPUT_CSV_HEADERS": '[\n  "ZDAY",\n  "CENTERLON",\n  "CENTERLAT",\n  "TOTAL_COUNT"\n]',
            "DATA_DTYPES": '{\n  "ZDAY": "str",\n  "CENTERLON": "str",\n  "CENTERLAT": "str",\n  "TOTAL_COUNT": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "date",\n  "number_of_strikes",\n  "center_point_geom",\n  "source_url",\n  "etl_timestamp"\n]',
            "RENAME_HEADERS_LIST": '{\n  "zday": "day_int",\n  "total_count": "number_of_strikes"\n}',
        },
        resources={"request_ephemeral_storage": "16G", "limit_cpu": "3"},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="noaa",
    )

    (
        create_cluster
        >> [
            ghcnd_by_year,
            ghcnd_countries,
            ghcnd_inventory,
            ghcnd_states,
            ghcnd_stations,
            gsod_stations,
            ghcnd_hurricanes,
            lightning_strikes_by_year,
        ]
        >> delete_cluster
    )
