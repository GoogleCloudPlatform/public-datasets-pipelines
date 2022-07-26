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
    dag_id="census_bureau_international.midyear_population_age_sex",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="midyear_population_age_sex",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.census_bureau_international.container_registry.run_csv_transform_kub_midyear_population_age_sex }}",
        env_vars={
            "SOURCE_URL": '"gs://pdp-feeds-staging/Census/idbzip/IDBext194.csv",\n"gs://pdp-feeds-staging/Census/idbzip/IDBextCTYS.csv"\n',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_bureau_international/midyear_population_age_sex/data_output.csv",
            "TRANSFORM_LIST": '[ "obtain_population", "obtain_country", "resolve_sex", "reorder_headers" ]',
            "REORDER_HEADERS": '[ "country_code", "country_name", "year", "sex", "max_age",\n  "population_age_0", "population_age_1", "population_age_2", "population_age_3", "population_age_4",\n  "population_age_5", "population_age_6", "population_age_7", "population_age_8", "population_age_9",\n  "population_age_10", "population_age_11", "population_age_12", "population_age_13", "population_age_14",\n  "population_age_15", "population_age_16", "population_age_17", "population_age_18", "population_age_19",\n  "population_age_20", "population_age_21", "population_age_22", "population_age_23", "population_age_24",\n  "population_age_25", "population_age_26", "population_age_27", "population_age_28", "population_age_29",\n  "population_age_30", "population_age_31", "population_age_32", "population_age_33", "population_age_34",\n  "population_age_35", "population_age_36", "population_age_37", "population_age_38", "population_age_39",\n  "population_age_40", "population_age_41", "population_age_42", "population_age_43", "population_age_44",\n  "population_age_45", "population_age_46", "population_age_47", "population_age_48", "population_age_49",\n  "population_age_50", "population_age_51", "population_age_52", "population_age_53", "population_age_54",\n  "population_age_55", "population_age_56", "population_age_57", "population_age_58", "population_age_59",\n  "population_age_60", "population_age_61", "population_age_62", "population_age_63", "population_age_64",\n  "population_age_65", "population_age_66", "population_age_67", "population_age_68", "population_age_69",\n  "population_age_70", "population_age_71", "population_age_72", "population_age_73", "population_age_74",\n  "population_age_75", "population_age_76", "population_age_77", "population_age_78", "population_age_79",\n  "population_age_80", "population_age_81", "population_age_82", "population_age_83", "population_age_84",\n  "population_age_85", "population_age_86", "population_age_87", "population_age_88", "population_age_89",\n  "population_age_90", "population_age_91", "population_age_92", "population_age_93", "population_age_94",\n  "population_age_95", "population_age_96", "population_age_97", "population_age_98", "population_age_99",\n  "population_age_100" ]',
            "PIPELINE_ENGLISH_NAME": '"International Database (Country Names - Midyear Population, by Age and Sex) Delivery"',
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_bureau_international/midyear_population_age_sex/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.census_bureau_international.container_registry.midyear_population_age_sex_destination_table }}",
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
                "name": "max_age",
                "type": "INTEGER",
                "description": "The last age in the distribution with a value greater than zero",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_0",
                "type": "INTEGER",
                "description": "Population at Age 0",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_1",
                "type": "INTEGER",
                "description": "Population at Age 1",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_2",
                "type": "INTEGER",
                "description": "Population at Age 2",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_3",
                "type": "INTEGER",
                "description": "Population at Age 3",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_4",
                "type": "INTEGER",
                "description": "Population at Age 4",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_5",
                "type": "INTEGER",
                "description": "Population at Age 5",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_6",
                "type": "INTEGER",
                "description": "Population at Age 6",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_7",
                "type": "INTEGER",
                "description": "Population at Age 7",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_8",
                "type": "INTEGER",
                "description": "Population at Age 8",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_9",
                "type": "INTEGER",
                "description": "Population at Age 9",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_10",
                "type": "INTEGER",
                "description": "Population at Age 10",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_11",
                "type": "INTEGER",
                "description": "Population at Age 11",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_12",
                "type": "INTEGER",
                "description": "Population at Age 12",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_13",
                "type": "INTEGER",
                "description": "Population at Age 13",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_14",
                "type": "INTEGER",
                "description": "Population at Age 14",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_15",
                "type": "INTEGER",
                "description": "Population at Age 15",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_16",
                "type": "INTEGER",
                "description": "Population at Age 16",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_17",
                "type": "INTEGER",
                "description": "Population at Age 17",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_18",
                "type": "INTEGER",
                "description": "Population at Age 18",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_19",
                "type": "INTEGER",
                "description": "Population at Age 19",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_20",
                "type": "INTEGER",
                "description": "Population at Age 20",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_21",
                "type": "INTEGER",
                "description": "Population at Age 21",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_22",
                "type": "INTEGER",
                "description": "Population at Age 22",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_23",
                "type": "INTEGER",
                "description": "Population at Age 23",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_24",
                "type": "INTEGER",
                "description": "Population at Age 24",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_25",
                "type": "INTEGER",
                "description": "Population at Age 25",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_26",
                "type": "INTEGER",
                "description": "Population at Age 26",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_27",
                "type": "INTEGER",
                "description": "Population at Age 27",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_28",
                "type": "INTEGER",
                "description": "Population at Age 28",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_29",
                "type": "INTEGER",
                "description": "Population at Age 29",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_30",
                "type": "INTEGER",
                "description": "Population at Age 30",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_31",
                "type": "INTEGER",
                "description": "Population at Age 31",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_32",
                "type": "INTEGER",
                "description": "Population at Age 32",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_33",
                "type": "INTEGER",
                "description": "Population at Age 33",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_34",
                "type": "INTEGER",
                "description": "Population at Age 34",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_35",
                "type": "INTEGER",
                "description": "Population at Age 35",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_36",
                "type": "INTEGER",
                "description": "Population at Age 36",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_37",
                "type": "INTEGER",
                "description": "Population at Age 37",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_38",
                "type": "INTEGER",
                "description": "Population at Age 38",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_39",
                "type": "INTEGER",
                "description": "Population at Age 39",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_40",
                "type": "INTEGER",
                "description": "Population at Age 40",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_41",
                "type": "INTEGER",
                "description": "Population at Age 41",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_42",
                "type": "INTEGER",
                "description": "Population at Age 42",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_43",
                "type": "INTEGER",
                "description": "Population at Age 43",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_44",
                "type": "INTEGER",
                "description": "Population at Age 44",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_45",
                "type": "INTEGER",
                "description": "Population at Age 45",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_46",
                "type": "INTEGER",
                "description": "Population at Age 46",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_47",
                "type": "INTEGER",
                "description": "Population at Age 47",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_48",
                "type": "INTEGER",
                "description": "Population at Age 48",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_49",
                "type": "INTEGER",
                "description": "Population at Age 49",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_50",
                "type": "INTEGER",
                "description": "Population at Age 50",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_51",
                "type": "INTEGER",
                "description": "Population at Age 51",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_52",
                "type": "INTEGER",
                "description": "Population at Age 52",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_53",
                "type": "INTEGER",
                "description": "Population at Age 53",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_54",
                "type": "INTEGER",
                "description": "Population at Age 54",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_55",
                "type": "INTEGER",
                "description": "Population at Age 55",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_56",
                "type": "INTEGER",
                "description": "Population at Age 56",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_57",
                "type": "INTEGER",
                "description": "Population at Age 57",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_58",
                "type": "INTEGER",
                "description": "Population at Age 58",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_59",
                "type": "INTEGER",
                "description": "Population at Age 59",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_60",
                "type": "INTEGER",
                "description": "Population at Age 60",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_61",
                "type": "INTEGER",
                "description": "Population at Age 61",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_62",
                "type": "INTEGER",
                "description": "Population at Age 62",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_63",
                "type": "INTEGER",
                "description": "Population at Age 63",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_64",
                "type": "INTEGER",
                "description": "Population at Age 64",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_65",
                "type": "INTEGER",
                "description": "Population at Age 65",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_66",
                "type": "INTEGER",
                "description": "Population at Age 66",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_67",
                "type": "INTEGER",
                "description": "Population at Age 67",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_68",
                "type": "INTEGER",
                "description": "Population at Age 68",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_69",
                "type": "INTEGER",
                "description": "Population at Age 69",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_70",
                "type": "INTEGER",
                "description": "Population at Age 70",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_71",
                "type": "INTEGER",
                "description": "Population at Age 71",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_72",
                "type": "INTEGER",
                "description": "Population at Age 72",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_73",
                "type": "INTEGER",
                "description": "Population at Age 73",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_74",
                "type": "INTEGER",
                "description": "Population at Age 74",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_75",
                "type": "INTEGER",
                "description": "Population at Age 75",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_76",
                "type": "INTEGER",
                "description": "Population at Age 76",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_77",
                "type": "INTEGER",
                "description": "Population at Age 77",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_78",
                "type": "INTEGER",
                "description": "Population at Age 78",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_79",
                "type": "INTEGER",
                "description": "Population at Age 79",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_80",
                "type": "INTEGER",
                "description": "Population at Age 80",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_81",
                "type": "INTEGER",
                "description": "Population at Age 81",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_82",
                "type": "INTEGER",
                "description": "Population at Age 82",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_83",
                "type": "INTEGER",
                "description": "Population at Age 83",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_84",
                "type": "INTEGER",
                "description": "Population at Age 84",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_85",
                "type": "INTEGER",
                "description": "Population at Age 85",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_86",
                "type": "INTEGER",
                "description": "Population at Age 86",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_87",
                "type": "INTEGER",
                "description": "Population at Age 87",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_88",
                "type": "INTEGER",
                "description": "Population at Age 88",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_89",
                "type": "INTEGER",
                "description": "Population at Age 89",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_90",
                "type": "INTEGER",
                "description": "Population at Age 90",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_91",
                "type": "INTEGER",
                "description": "Population at Age 91",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_92",
                "type": "INTEGER",
                "description": "Population at Age 92",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_93",
                "type": "INTEGER",
                "description": "Population at Age 93",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_94",
                "type": "INTEGER",
                "description": "Population at Age 94",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_95",
                "type": "INTEGER",
                "description": "Population at Age 95",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_96",
                "type": "INTEGER",
                "description": "Population at Age 96",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_97",
                "type": "INTEGER",
                "description": "Population at Age 97",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_98",
                "type": "INTEGER",
                "description": "Population at Age 98",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_99",
                "type": "INTEGER",
                "description": "Population at Age 99",
                "mode": "NULLABLE",
            },
            {
                "name": "population_age_100",
                "type": "INTEGER",
                "description": "Population at Age 100",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
