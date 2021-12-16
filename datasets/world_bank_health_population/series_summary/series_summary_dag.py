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
    dag_id="world_bank_health_population.series_summary",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    series_summary_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="series_summary_transform_csv",
        startup_timeout_seconds=600,
        name="series_summary",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_health_population.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://pdp-feeds-staging/RelayWorldBank/hnp_stats_csv/HNP_StatsSeries.csv",
            "SOURCE_FILE": "files/data.csv",
            "COLUMN_TO_REMOVE": "Unnamed: 20",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_health_population/series_summary/data_output.csv",
            "PIPELINE_NAME": "series_summary",
            "CSV_HEADERS": '["series_code" ,"topic" ,"indicator_name" ,"short_definition" ,"long_definition" ,"unit_of_measure" ,"periodicity" ,"base_period" ,"other_notes" ,"aggregation_method" ,"limitations_and_exceptions" ,"notes_from_original_source" ,"general_comments" ,"source" ,"statistical_concept_and_methodology" ,"development_relevance" ,"related_source_links" ,"other_web_links" ,"related_indicators" ,"license_type"]',
            "RENAME_MAPPINGS": '{"Series Code":"series_code" ,"Topic":"topic" ,"Indicator Name":"indicator_name" ,"Short definition":"short_definition" ,"Long definition":"long_definition" ,"Unit of measure":"unit_of_measure" ,"Periodicity":"periodicity" ,"Base Period":"base_period" ,"Other notes":"other_notes" ,"Aggregation method":"aggregation_method" ,"Limitations and exceptions":"limitations_and_exceptions" ,"Notes from original source":"notes_from_original_source" ,"General comments":"general_comments" ,"Source":"source" ,"Statistical concept and methodology":"statistical_concept_and_methodology" ,"Development relevance":"development_relevance" ,"Related source links":"related_source_links" ,"Other web links":"other_web_links" ,"Related indicators":"related_indicators" ,"License Type":"license_type"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_series_summary_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_series_summary_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/world_bank_health_population/series_summary/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="world_bank_health_population.series_summary",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "series_code", "type": "string", "mode": "nullable"},
            {"name": "topic", "type": "string", "mode": "nullable"},
            {"name": "indicator_name", "type": "string", "mode": "nullable"},
            {"name": "short_definition", "type": "string", "mode": "nullable"},
            {"name": "long_definition", "type": "string", "mode": "nullable"},
            {"name": "unit_of_measure", "type": "string", "mode": "nullable"},
            {"name": "periodicity", "type": "string", "mode": "nullable"},
            {"name": "base_period", "type": "integer", "mode": "nullable"},
            {"name": "other_notes", "type": "string", "mode": "nullable"},
            {"name": "aggregation_method", "type": "string", "mode": "nullable"},
            {
                "name": "limitations_and_exceptions",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "notes_from_original_source",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "general_comments", "type": "string", "mode": "nullable"},
            {"name": "source", "type": "string", "mode": "nullable"},
            {
                "name": "statistical_concept_and_methodology",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "development_relevance", "type": "string", "mode": "nullable"},
            {"name": "related_source_links", "type": "string", "mode": "nullable"},
            {"name": "other_web_links", "type": "string", "mode": "nullable"},
            {"name": "related_indicators", "type": "string", "mode": "nullable"},
            {"name": "license_type", "type": "string", "mode": "nullable"},
        ],
    )

    series_summary_transform_csv >> load_series_summary_to_bq
