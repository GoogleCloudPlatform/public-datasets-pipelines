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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-10-04",
}


with DAG(
    dag_id="world_bank_health_population.world_bank_health_population",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy the source files
    copy_gcs_to_gcs = bash.BashOperator(
        task_id="copy_gcs_to_gcs",
        bash_command="gsutil cp gs://pdp-feeds-staging/RelayWorldBank/hnp_stats_csv/HNP_StatsCountry-Series.csv gs://{{ var.value.composer_bucket }}/data/world_bank_health_population/raw_files/ ; gsutil cp gs://pdp-feeds-staging/RelayWorldBank/hnp_stats_csv/HNP_StatsCountry.csv gs://{{ var.value.composer_bucket }}/data/world_bank_health_population/raw_files/ ; gsutil cp gs://pdp-feeds-staging/RelayWorldBank/hnp_stats_csv/HNP_StatsSeries.csv gs://{{ var.value.composer_bucket }}/data/world_bank_health_population/raw_files/ ; gsutil cp gs://pdp-feeds-staging/RelayWorldBank/hnp_stats_csv/HNP_StatsSeries-Time.csv gs://{{ var.value.composer_bucket }}/data/world_bank_health_population/raw_files/ ;",
    )

    # Run CSV transform within kubernetes pod
    country_series_definitions_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="country_series_definitions_transform_csv",
        startup_timeout_seconds=1000,
        name="country_series_definitions",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_health_population.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "{{ var.json.world_bank_health_population.country_series_definitions.source_url}} ",
            "SOURCE_FILE": "files/data.csv",
            "COLUMN_TO_REMOVE": "{{ var.json.world_bank_health_population.country_series_definitions.column_to_remove }}",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.world_bank_health_population.country_series_definitions.target_gcs_path }}",
            "PIPELINE_NAME": "country_series_definitions",
            "CSV_HEADERS": '["country_code" ,"series_code" ,"description"]',
            "RENAME_MAPPINGS": '{"CountryCode":"country_code","SeriesCode":"series_code","DESCRIPTION":"description"}',
        },
    )

    # Task to load CSV data to a BigQuery table
    country_series_definitions_load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="country_series_definitions_load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="{{ var.json.world_bank_health_population.country_series_definitions.source_objects }}",
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

    (
        [copy_gcs_to_gcs]
        >> country_series_definitions_transform_csv
        >> country_series_definitions_load_to_bq
    )
