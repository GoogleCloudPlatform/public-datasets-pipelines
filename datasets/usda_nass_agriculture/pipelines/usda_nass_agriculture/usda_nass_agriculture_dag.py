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
    "start_date": "2022-12-06",
}


with DAG(
    dag_id="usda_nass_agriculture.usda_nass_agriculture",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Download data using the kubernetes pod
    kub_download = kubernetes_pod.KubernetesPodOperator(
        task_id="kub_download",
        startup_timeout_seconds=1000,
        name="download_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.usda_nass_agriculture.container_registry.run_script_kub }}",
        env_vars={
            "DIRECTORY": "quickstats",
            "HOST": "ftp.nass.usda.gov",
            "GCS_BUCKET": "us-central1-dev-v2-cd7f5f38-bucket",
            "GCS_PATH": "data/usda_nass_agriculture/raw_files/",
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    # Unzip data
    bash_unzip = bash.BashOperator(
        task_id="bash_unzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/usda_nass_agriculture/raw_files/*.gz ;",
    )

    # ETL within the kubernetes pod
    kub_csv_transform = kubernetes_pod.KubernetesPodOperator(
        task_id="kub_csv_transform",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.usda_nass_agriculture.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_PATH": "data/usda_nass_agriculture/raw_files/",
            "DESTINATION_GCS_PATH": "data/usda_nass_agriculture/transformed_files/",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "usda_nass_agriculture",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SCHEMA_FILEPATH": "schema.json",
            "RENAME_MAPPINGS": '{"SOURCE_DESC": "source_desc",\n "SECTOR_DESC": "sector_desc",\n "GROUP_DESC": "group_desc",\n "COMMODITY_DESC": "commodity_desc",\n "CLASS_DESC": "class_desc",\n "PRODN_PRACTICE_DESC": "prodn_practice_desc",\n "UTIL_PRACTICE_DESC": "util_practice_desc",\n "STATISTICCAT_DESC": "statisticcat_desc",\n "UNIT_DESC": "unit_desc",\n "SHORT_DESC": "short_desc",\n "DOMAIN_DESC": "domain_desc",\n "DOMAINCAT_DESC": "domaincat_desc",\n "AGG_LEVEL_DESC": "agg_level_desc",\n "STATE_ANSI": "state_ansi",\n "STATE_FIPS_CODE": "state_fips_code",\n "STATE_ALPHA": "state_alpha",\n "STATE_NAME": "state_name",\n "ASD_CODE": "asd_code",\n "ASD_DESC": "asd_desc",\n "COUNTY_ANSI": "county_ansi",\n "COUNTY_CODE": "county_code",\n "COUNTY_NAME": "county_name",\n "REGION_DESC": "region_desc",\n "ZIP_5": "zip_5",\n "WATERSHED_CODE": "watershed_code",\n "WATERSHED_DESC": "watershed_desc",\n "CONGR_DISTRICT_CODE": "congr_district_code",\n "COUNTRY_CODE": "country_code",\n "COUNTRY_NAME": "country_name",\n "LOCATION_DESC": "location_desc",\n "YEAR": "year",\n "FREQ_DESC": "freq_desc",\n "BEGIN_CODE": "begin_code",\n "END_CODE": "end_code",\n "REFERENCE_PERIOD_DESC": "reference_period_desc",\n "WEEK_ENDING": "week_ending",\n "LOAD_TIME": "load_time",\n "VALUE": "value",\n "CV_%": "cv_percent"}',
            "HEADERS": '["source_desc",\n "sector_desc",\n "group_desc",\n "commodity_desc",\n "class_desc",\n "prodn_practice_desc",\n "util_practice_desc",\n "statisticcat_desc",\n "unit_desc",\n "short_desc",\n "domain_desc",\n "domaincat_desc",\n "agg_level_desc",\n "state_ansi",\n "state_fips_code",\n "state_alpha",\n "state_name",\n "asd_code",\n "asd_desc",\n "county_ansi",\n "county_code",\n "county_name",\n "region_desc",\n "zip_5",\n "watershed_code",\n "watershed_desc",\n "congr_district_code",\n "country_code",\n "country_name",\n "location_desc",\n "year",\n "freq_desc",\n "begin_code",\n "end_code",\n "reference_period_desc",\n "week_ending",\n "load_time",\n "value",\n "cv_percent"]',
            "DOWNLOAD_PATH": "",
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    kub_download >> bash_unzip >> kub_csv_transform
