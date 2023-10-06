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
    dag_id="census_bureau_international.age_specific_fertility_rates",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="age_specific_fertility_rates",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.census_bureau_international.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '"gs://pdp-feeds-staging/Census/idbzip/IDBext028.csv",\n"gs://pdp-feeds-staging/Census/idbzip/IDBextCTYS.csv"\n',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_bureau_international/age_specific_fertility_rates/data_output.csv",
            "REORDER_HEADERS": '[ "country_code", "country_name", "year", "fertility_rate_15_19", "fertility_rate_20_24",\n  "fertility_rate_25_29", "fertility_rate_30_34", "fertility_rate_35_39", "fertility_rate_40_44",\n  "fertility_rate_45_49", "total_fertility_rate", "gross_reproduction_rate", "sex_ratio_at_birth" ]',
            "TRANSFORM_LIST": '[ "obtain_population", "obtain_country", "reorder_headers" ]',
            "PIPELINE_ENGLISH_NAME": "International Database (Country Names - Fertility Rates) Delivery",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_bureau_international/age_specific_fertility_rates/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.census_bureau_international.container_registry.age_specific_fertility_rates_destination_table }}",
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
                "name": "fertility_rate_15_19",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 15-19 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "fertility_rate_20_24",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 20-24 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "fertility_rate_25_29",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 25-29 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "fertility_rate_30_34",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 30-34 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "fertility_rate_35_39",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 35-39 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "fertility_rate_40_44",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 40-44 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "fertility_rate_45_49",
                "type": "FLOAT",
                "description": "Age specific fertility rate for age 45-49 (births per 1,000 population)",
                "mode": "NULLABLE",
            },
            {
                "name": "total_fertility_rate",
                "type": "FLOAT",
                "description": "Total fertility rate (lifetime births per woman)",
                "mode": "NULLABLE",
            },
            {
                "name": "gross_reproduction_rate",
                "type": "FLOAT",
                "description": "Gross reproduction rate (lifetime female births per woman)",
                "mode": "NULLABLE",
            },
            {
                "name": "sex_ratio_at_birth",
                "type": "FLOAT",
                "description": "Sex ratio at birth (male births per female birth)",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
