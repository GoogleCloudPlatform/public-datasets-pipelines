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
    dag_id="world_bank_health_population.country_series_definitions",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    country_series_definitions_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="country_series_definitions_transform_csv",
        startup_timeout_seconds=600,
        name="country_series_definitions",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_health_population.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://pdp-feeds-staging/RelayWorldBank/hnp_stats_csv/HNP_StatsCountry-Series.csv",
            "SOURCE_FILE": "files/data.csv",
            "COLUMN_TO_REMOVE": "Unnamed: 3",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_health_population/country_series_definitions/data_output.csv",
            "PIPELINE_NAME": "country_series_definitions",
            "CSV_HEADERS": '["country_code" ,"series_code" ,"description"]',
            "RENAME_MAPPINGS": '{"CountryCode":"country_code","SeriesCode":"series_code","DESCRIPTION":"description"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_country_series_definitions_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_country_series_definitions_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/world_bank_health_population/country_series_definitions/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="world_bank_health_population.country_series_definitions",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "country_code", "type": "string", "mode": "nullable"},
            {"name": "series_code", "type": "string", "mode": "nullable"},
            {"name": "description", "type": "string", "mode": "nullable"},
        ],
    )

    country_series_definitions_transform_csv >> load_country_series_definitions_to_bq
