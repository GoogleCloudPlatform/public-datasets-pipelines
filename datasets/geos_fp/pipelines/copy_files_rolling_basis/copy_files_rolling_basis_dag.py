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
from airflow.providers.google.cloud.operators import gcs, kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-06-01",
}


with DAG(
    dag_id="geos_fp.copy_files_rolling_basis",
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
            "name": "geos-fp--copy-files-rolling-basis",
            "initial_node_count": 8,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-small",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Copy files to GCS on the specified date
    copy_files_dated_today = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "0",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on the specified date
    copy_files_dated_today_minus_1_day = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_1_day",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "1",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on the specified date
    copy_files_dated_today_minus_2_days = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_2_days",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "2",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        resources={"request_memory": "1G", "request_cpu": "1"},
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on a 10-day rolling basis
    copy_files_dated_today_minus_3_days = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_3_days",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "3",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        resources={"request_memory": "1G", "request_cpu": "1"},
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on a 10-day rolling basis
    copy_files_dated_today_minus_4_days = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_4_days",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "4",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        resources={"request_memory": "1G", "request_cpu": "1"},
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on a 10-day rolling basis
    copy_files_dated_today_minus_5_days = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_5_days",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "5",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        resources={"request_memory": "1G", "request_cpu": "1"},
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on a 10-day rolling basis
    copy_files_dated_today_minus_6_days = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_6_days",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "6",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        resources={"request_memory": "1G", "request_cpu": "1"},
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Copy files to GCS on a 10-day rolling basis
    copy_files_dated_today_minus_7_days = kubernetes_engine.GKEStartPodOperator(
        task_id="copy_files_dated_today_minus_7_days",
        name="geosfp",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="geos-fp--copy-files-rolling-basis",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.rolling_copy }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY_DIFF": "7",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "BATCH_SIZE": "10",
        },
        resources={"request_memory": "1G", "request_cpu": "1"},
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )

    # Deletes GCS data more than 7 days ago
    delete_old_data = gcs.GCSDeleteObjectsOperator(
        task_id="delete_old_data",
        bucket_name="{{ var.json.geos_fp.destination_bucket }}",
        prefix="{{ macros.ds_format(macros.ds_add(ds, -8), \u0027%Y-%m-%d\u0027, \u0027Y%Y/M%m/D%d\u0027) }}",
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="geos-fp--copy-files-rolling-basis",
    )

    delete_old_data
    create_cluster >> copy_files_dated_today >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_1_day >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_2_days >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_3_days >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_4_days >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_5_days >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_6_days >> delete_cluster
    create_cluster >> copy_files_dated_today_minus_7_days >> delete_cluster
