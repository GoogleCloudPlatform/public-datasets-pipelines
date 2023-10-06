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
    dag_id="census_bureau_international.midyear_population_agespecific",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="midyear_population_agespecific",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.census_bureau_international.container_registry.run_csv_transform_kub_midyear_population_agespecific }}",
        env_vars={
            "SOURCE_URL": '"gs://pdp-feeds-staging/Census/merge_age_code/idbzip/IDBext194.csv",\n"gs://pdp-feeds-staging/Census/idbzip/IDBextCTYS.csv"\n',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_bureau_international/midyear_population_agespecific/data_output.csv",
            "TRANSFORM_LIST": '[ "obtain_population", "obtain_country", "unpivot_population_data", "resolve_sex", "reorder_headers" ]',
            "REORDER_HEADERS": '[ "country_code", "country_name", "year", "sex", "max_age",\n  "population_age_0", "population_age_1", "population_age_2", "population_age_3", "population_age_4",\n  "population_age_5", "population_age_6", "population_age_7", "population_age_8", "population_age_9",\n  "population_age_10", "population_age_11", "population_age_12", "population_age_13", "population_age_14",\n  "population_age_15", "population_age_16", "population_age_17", "population_age_18", "population_age_19",\n  "population_age_20", "population_age_21", "population_age_22", "population_age_23", "population_age_24",\n  "population_age_25", "population_age_26", "population_age_27", "population_age_28", "population_age_29",\n  "population_age_30", "population_age_31", "population_age_32", "population_age_33", "population_age_34",\n  "population_age_35", "population_age_36", "population_age_37", "population_age_38", "population_age_39",\n  "population_age_40", "population_age_41", "population_age_42", "population_age_43", "population_age_44",\n  "population_age_45", "population_age_46", "population_age_47", "population_age_48", "population_age_49",\n  "population_age_50", "population_age_51", "population_age_52", "population_age_53", "population_age_54",\n  "population_age_55", "population_age_56", "population_age_57", "population_age_58", "population_age_59",\n  "population_age_60", "population_age_61", "population_age_62", "population_age_63", "population_age_64",\n  "population_age_65", "population_age_66", "population_age_67", "population_age_68", "population_age_69",\n  "population_age_70", "population_age_71", "population_age_72", "population_age_73", "population_age_74",\n  "population_age_75", "population_age_76", "population_age_77", "population_age_78", "population_age_79",\n  "population_age_80", "population_age_81", "population_age_82", "population_age_83", "population_age_84",\n  "population_age_85", "population_age_86", "population_age_87", "population_age_88", "population_age_89",\n  "population_age_90", "population_age_91", "population_age_92", "population_age_93", "population_age_94",\n  "population_age_95", "population_age_96", "population_age_97", "population_age_98", "population_age_99",\n  "population_age_100" ]',
            "PIPELINE_ENGLISH_NAME": '"International Database (Country Names - Midyear Population, by Age and Country Code) Delivery"',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_bureau_international/midyear_population_agespecific/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.census_bureau_international.container_registry.midyear_population_agespecific_destination_table }}",
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
                "name": "sex",
                "type": "STRING",
                "description": "Gender",
                "mode": "NULLABLE",
            },
            {
                "name": "population",
                "type": "INTEGER",
                "description": "Total count of individuals",
                "mode": "NULLABLE",
            },
            {
                "name": "age",
                "type": "INTEGER",
                "description": "Age in years",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
