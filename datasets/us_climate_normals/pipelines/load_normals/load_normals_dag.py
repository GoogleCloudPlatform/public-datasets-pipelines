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
from airflow.operators import bash
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="us_climate_normals.us_climate_normals",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 2 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy over to pod, the source data and structure from GCS
    download_source_from_gcs = bash.BashOperator(
        task_id="download_source_from_gcs",
        bash_command="mkdir -p /home/airflow/gcs/data/us_climate_normals/schema ;\nmkdir -p /home/airflow/gcs/data/us_climate_normals ;\ngsutil -m cp -r gs://normals/* gs://{{ var.value.composer_bucket }}/data/us_climate_normals ;\n",
    )

    # Run CSV transform within kubernetes pod
    load_hourly_data_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="load_hourly_data_to_bq",
        startup_timeout_seconds=600,
        name="load_us_climate_normals_hourly_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "US Climate Normals - Hourly",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "us_climate_normals",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TABLE_PREFIX": "normals_hourly",
            "SOURCE_LOCAL_FOLDER_ROOT": "files/us_climate_normals",
            "ROOT_GCS_FOLDER": "data/us_climate_normals",
            "ROOT_PIPELINE_GS_FOLDER": "normals-hourly",
            "FOLDERS_LIST": '[\n  "",\n  "1981-2010",\n  "1991-2020",\n  "2006-2020"\n]',
        },
        resources={
            "request_memory": "12G",
            "request_cpu": "1",
            "request_ephemeral_storage": "16G",
        },
    )

    # Run CSV transform within kubernetes pod
    load_daily_data_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="load_daily_data_to_bq",
        startup_timeout_seconds=600,
        name="load_us_climate_normals_daily_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "US Climate Normals - Daily",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "us_climate_normals",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TABLE_PREFIX": "normals_daily",
            "SOURCE_LOCAL_FOLDER_ROOT": "files/us_climate_normals",
            "ROOT_GCS_FOLDER": "data/us_climate_normals",
            "ROOT_PIPELINE_GS_FOLDER": "normals-daily",
            "FOLDERS_LIST": '[\n  "",\n  "1981-2010",\n  "1991-2020",\n  "2006-2020"\n]',
        },
        resources={
            "request_memory": "12G",
            "request_cpu": "1",
            "request_ephemeral_storage": "16G",
        },
    )

    # Run CSV transform within kubernetes pod
    load_monthly_data_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="load_monthly_data_to_bq",
        startup_timeout_seconds=600,
        name="load_us_climate_normals_monthly_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "US Climate Normals - Monthly",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "us_climate_normals",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TABLE_PREFIX": "normals_monthly",
            "SOURCE_LOCAL_FOLDER_ROOT": "files/us_climate_normals",
            "ROOT_GCS_FOLDER": "data/us_climate_normals",
            "ROOT_PIPELINE_GS_FOLDER": "normals-monthly",
            "FOLDERS_LIST": '[\n  "",\n  "1981-2010",\n  "1991-2020",\n  "2006-2020"\n]',
        },
        resources={
            "request_memory": "12G",
            "request_cpu": "1",
            "request_ephemeral_storage": "16G",
        },
    )

    # Run CSV transform within kubernetes pod
    load_annual_data_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="load_annual_data_to_bq",
        startup_timeout_seconds=600,
        name="load_us_climate_normals_annual_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.us_climate_normals.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "US Climate Normals - Annual",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "us_climate_normals",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TABLE_PREFIX": "normals_annualseasonal",
            "SOURCE_LOCAL_FOLDER_ROOT": "files/us_climate_normals",
            "ROOT_GCS_FOLDER": "data/us_climate_normals",
            "ROOT_PIPELINE_GS_FOLDER": "normals-annualseasonal",
            "FOLDERS_LIST": '[\n  "",\n  "1981-2010",\n  "1991-2020",\n  "2006-2020"\n]',
        },
        resources={
            "request_memory": "12G",
            "request_cpu": "1",
            "request_ephemeral_storage": "16G",
        },
    )

    download_source_from_gcs >> [
        load_hourly_data_to_bq,
        load_daily_data_to_bq,
        load_monthly_data_to_bq,
        load_annual_data_to_bq,
    ]
