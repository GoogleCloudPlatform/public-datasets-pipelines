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

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="noaa.noaa_hrrr_arl",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run NOAA load processes - HRRR Failover
    hrrr_arl = kubernetes_pod.KubernetesPodOperator(
        task_id="hrrr_arl",
        startup_timeout_seconds=600,
        name="hrrr_arl",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NOAA HRRR ARL Formatting",
            "SOURCE_URL": '{\n  "noaa_hrrr_arl_formatting": "ftp://arlftp.arlhq.noaa.gov/forecast/~DATE~/"\n}',
            "SOURCE_FILE": "files",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.json.noaa.noaa_hrrr_arl.target_gcs_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.noaa.noaa_hrrr_arl.target_gcs_path }}",
        },
        resources={"limit_memory": "10G", "limit_cpu": "3"},
    )

    hrrr_arl