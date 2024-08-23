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
    dag_id="clemson_dice_traffic_vision.clemson_dice_traffic_vision",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transfer_source = kubernetes_pod.KubernetesPodOperator(
        task_id="transfer_source",
        startup_timeout_seconds=600,
        name="transfer_source",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.clemson_dice_traffic_vision.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL_GCS": "gs://{{ var.value.composer_bucket }}/data/trafficvision/files",
            "SOURCE_FILE_BATCH_LENGTH": "2000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/trafficvision/load_files",
            "TARGET_ROOT_PATH": "data/trafficvision",
            "TARGET_SOURCE_FOLDER": "files",
            "TARGET_UNPACK_FOLDER": "unpack",
            "TARGET_LOAD_FOLDER": "load_files",
            "TARGET_BATCH_FOLDER": "batch_metadata",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "PIPELINE_NAME": "transfer_source",
        },
        resources={
            "request_memory": "24G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run CSV transform within kubernetes pod
    transform_clemson_dice_data = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_clemson_dice_data",
        startup_timeout_seconds=600,
        name="transform_clemson_dice_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.clemson_dice_traffic_vision.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL_GCS": "gs://{{ var.value.composer_bucket }}/data/trafficvision/files",
            "SOURCE_FILE_BATCH_LENGTH": "2000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/trafficvision/load_files",
            "TARGET_ROOT_PATH": "data/trafficvision",
            "TARGET_SOURCE_FOLDER": "files",
            "TARGET_UNPACK_FOLDER": "unpack",
            "TARGET_LOAD_FOLDER": "load_files",
            "TARGET_BATCH_FOLDER": "batch_metadata",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "PIPELINE_NAME": "generate_batch_metadata_files",
        },
        resources={
            "request_memory": "24G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run CSV transform within kubernetes pod
    run_batch_data_group_ord_1 = kubernetes_pod.KubernetesPodOperator(
        task_id="run_batch_data_group_ord_1",
        startup_timeout_seconds=600,
        name="run_batch_data_group_ord_1",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.clemson_dice_traffic_vision.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL_GCS": "gs://{{ var.value.composer_bucket }}/data/trafficvision/files",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/trafficvision",
            "TARGET_ROOT_PATH": "trafficvision",
            "TARGET_SOURCE_FOLDER": "files",
            "TARGET_UNPACK_FOLDER": "unpack",
            "TARGET_LOAD_FOLDER": "load_files",
            "TARGET_BATCH_FOLDER": "batch_metadata",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "PIPELINE_NAME": "run_batch_data",
            "BATCH_GROUP_SIZE": "2",
            "BATCH_ORDINAL": "1",
        },
        resources={
            "request_memory": "24G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    # Run CSV transform within kubernetes pod
    run_batch_data_group_ord_2 = kubernetes_pod.KubernetesPodOperator(
        task_id="run_batch_data_group_ord_2",
        startup_timeout_seconds=600,
        name="run_batch_data_group_ord_2",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.clemson_dice_traffic_vision.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL_GCS": "gs://{{ var.value.composer_bucket }}/data/trafficvision/files",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/trafficvision",
            "TARGET_ROOT_PATH": "trafficvision",
            "TARGET_SOURCE_FOLDER": "files",
            "TARGET_UNPACK_FOLDER": "unpack",
            "TARGET_LOAD_FOLDER": "load_files",
            "TARGET_BATCH_FOLDER": "batch_metadata",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "PIPELINE_NAME": "run_batch_data",
            "BATCH_GROUP_SIZE": "2",
            "BATCH_ORDINAL": "2",
        },
        resources={
            "request_memory": "24G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    # Load JSON metadata files to BQ
    load_json_metadata_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_json_metadata_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/trafficvision/load_files/out*.log"],
        source_format="NEWLINE_DELIMITED_JSON",
        destination_project_dataset_table="clemson_dice.traffic_vision",
        write_disposition="WRITE_TRUNCATE",
    )

    (
        transfer_source
        >> transform_clemson_dice_data
        >> [run_batch_data_group_ord_1, run_batch_data_group_ord_2]
        >> load_json_metadata_to_bq
    )
