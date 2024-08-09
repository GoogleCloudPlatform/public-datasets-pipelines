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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="census_bureau_international.mortality_life_expectancy",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="mortality_life_expectancy",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.census_bureau_international.container_registry.run_csv_transform_kub_mortality_life_expectancy }}",
        env_vars={
            "SOURCE_URL": '"gs://pdp-feeds-staging/Census/idbzip/IDBext010.csv",\n"gs://pdp-feeds-staging/Census/idbzip/IDBextCTYS.csv"\n',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_bureau_international/mortality_life_expectancy/data_output.csv",
            "TRANSFORM_LIST": '[ "obtain_population", "obtain_country", "reorder_headers" ]',
            "REORDER_HEADERS": '[ "country_code", "country_name", "year", "infant_mortality", "infant_mortality_male",\n  "infant_mortality_female", "life_expectancy", "life_expectancy_male", "life_expectancy_female", "mortality_rate_under5",\n  "mortality_rate_under5_male", "mortality_rate_under5_female", "mortality_rate_1to4", "mortality_rate_1to4_male", "mortality_rate_1to4_female" ]',
            "PIPELINE_ENGLISH_NAME": "International Database (Life Expectancy - Country Names) Delivery",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_bureau_international/mortality_life_expectancy/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.census_bureau_international.container_registry.mortality_life_expectancy_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "country_code",
                "type": "STRING",
                "description": "Federal Information Processing Standard (FIPS) country/area code",
                "mode": "REQUIRED",
            },
            {
                "name": "country_name",
                "type": "STRING",
                "description": "Country or area name",
                "mode": "NULLABLE",
            },
            {
                "name": "year",
                "type": "INTEGER",
                "description": "Year",
                "mode": "REQUIRED",
            },
            {
                "name": "infant_mortality",
                "type": "FLOAT",
                "description": "Both sexes infant mortality rate (infant deaths per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "infant_mortality_male",
                "type": "FLOAT",
                "description": "Male infant mortality rate (infant deaths per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "infant_mortality_female",
                "type": "FLOAT",
                "description": "Female infant mortality rate (infant deaths per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "life_expectancy",
                "type": "FLOAT",
                "description": "Both sexes life expectancy at birth (years)",
                "mode": "NULLABLE",
            },
            {
                "name": "life_expectancy_male",
                "type": "FLOAT",
                "description": "Male life expectancy at birth (years)",
                "mode": "NULLABLE",
            },
            {
                "name": "life_expectancy_female",
                "type": "FLOAT",
                "description": "Female life expectancy at birth (years)",
                "mode": "NULLABLE",
            },
            {
                "name": "mortality_rate_under5",
                "type": "FLOAT",
                "description": "Both sexes under-5 mortality rate (probability of dying between ages 0 and 5)",
                "mode": "NULLABLE",
            },
            {
                "name": "mortality_rate_under5_male",
                "type": "FLOAT",
                "description": "Male sexes under-5 mortality rate (probability of dying between ages 0 and 5)",
                "mode": "NULLABLE",
            },
            {
                "name": "mortality_rate_under5_female",
                "type": "FLOAT",
                "description": "Female sexes under-5 mortality rate (probability of dying between ages 0 and 5)",
                "mode": "NULLABLE",
            },
            {
                "name": "mortality_rate_1to4",
                "type": "FLOAT",
                "description": "Both sexes child mortality rate (probability of dying between ages 1 and 4)",
                "mode": "NULLABLE",
            },
            {
                "name": "mortality_rate_1to4_male",
                "type": "FLOAT",
                "description": "Male sexes child mortality rate (probability of dying between ages 1 and 4)",
                "mode": "NULLABLE",
            },
            {
                "name": "mortality_rate_1to4_female",
                "type": "FLOAT",
                "description": "Female sexes child mortality rate (probability of dying between ages 1 and 4)",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
