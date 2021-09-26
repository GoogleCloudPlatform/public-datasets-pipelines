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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="census_bureau_international.midyear_population_5yr_age_sex",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    midyear_population_5yr_age_sex_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="midyear_population_5yr_age_sex_transform_csv",
        startup_timeout_seconds=600,
        name="midyear_population_5yr_age_sex",
        namespace="default",
        affinity={
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    "values": ["pool-e2-standard-4"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        image_pull_policy="Always",
        image="{{ var.json.census_bureau_international.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '["gs://pdp-feeds-staging/Census/idbzip/IDBext094.csv","gs://pdp-feeds-staging/Census/idbzip/IDBextCTYS.csv"]',
            "SOURCE_FILE": '["files/data1.csv","files/data2.csv"]',
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_bureau_international/midyear_population_5yr_age_sex/data_output.csv",
            "PIPELINE_NAME": "midyear_population_5yr_age_sex",
            "FILE_PATH": "files/",
            "CSV_HEADERS": '["country_code","country_name","year","total_flag","starting_age","age_group_indicator","ending_age","midyear_population","midyear_population_male","midyear_population_female"]',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_midyear_population_5yr_age_sex_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_midyear_population_5yr_age_sex_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_bureau_international/midyear_population_5yr_age_sex/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="census_bureau_international.midyear_population_5yr_age_sex",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "country_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "country_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "year", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "total_flag", "type": "STRING", "mode": "NULLABLE"},
            {"name": "starting_age", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "age_group_indicator", "type": "STRING", "mode": "NULLABLE"},
            {"name": "ending_age", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "midyear_population", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "midyear_population_male", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "midyear_population_female",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
        ],
    )

    midyear_population_5yr_age_sex_transform_csv >> load_midyear_population_5yr_age_sex_to_bq
