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
from airflow.contrib.operators import kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-06-01",
}


with DAG(
    dag_id="geos_fp.copy_files_rolling_basis",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy files to GCS on a 10-day rolling basis
    copy_files_in_last_n_days = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="copy_files_in_last_n_days",
        name="geosfp",
        namespace="default",
        image="{{ var.json.geos_fp.container_registry.crawl_and_download }}",
        image_pull_policy="Always",
        env_vars={
            "BASE_URL": "https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/das",
            "TODAY": "{{ ds }}",
            "DOWNLOAD_DIR": "/geos_fp/data",
            "MANIFEST_PATH": "/geos_fp/manifest.txt",
            "TARGET_BUCKET": "{{ var.json.geos_fp.destination_bucket }}",
            "DAYS_ROLLING": "10",
            "BATCH_SIZE": "50",
        },
        resources={"request_memory": "4G", "request_cpu": "4"},
    )

    copy_files_in_last_n_days
