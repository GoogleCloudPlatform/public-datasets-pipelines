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
    "start_date": "2022-11-07",
}


with DAG(
    dag_id="covid19_jhu_csse.covid19_jhu_csse",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Download data
    bash_download = bash.BashOperator(
        task_id="bash_download",
        bash_command="wget -q -O - https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv |gcloud storage cp - gs://{{ var.value.composer_bucket }}/data/covid19_jhu_csse/raw_files/confirmed_cases.csv ; wget -q -O - https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv |gcloud storage cp - gs://{{ var.value.composer_bucket }}/data/covid19_jhu_csse/raw_files/deaths.csv ; wget -q -O - https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv |gcloud storage cp - gs://{{ var.value.composer_bucket }}/data/covid19_jhu_csse/raw_files/recovered_cases.csv ;",
    )

    # ETL within the kubernetes pod
    kub_csv_transform = kubernetes_pod.KubernetesPodOperator(
        task_id="kub_csv_transform",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.covid19_jhu_csse.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_PATH": "data/covid19_jhu_csse/raw_files/",
            "DESTINATION_GCS_PATH": "data/covid19_jhu_csse/transformed_files/",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "covid19_jhu_csse",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SCHEMA_FILEPATH": "covid19_jhu_csse_schema.json",
            "RENAME_MAPPINGS": '{"Province/State":"province_or_state","Country/Region":"country_or_region","Lat":"latitude","Long":"longitude"}',
            "ADD_HEADER": "location_geom",
            "DOWNLOAD_PATH": "",
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    bash_download >> kub_csv_transform
