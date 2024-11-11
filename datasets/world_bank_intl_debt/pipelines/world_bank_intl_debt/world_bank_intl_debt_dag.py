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
from airflow.providers.google.cloud.operators import kubernetes_engine
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-10-10",
}


with DAG(
    dag_id="world_bank_intl_debt.world_bank_intl_debt",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy the source files
    copy_gcs_to_gcs = bash.BashOperator(
        task_id="copy_gcs_to_gcs",
        bash_command="gsutil cp gs://pdp-feeds-staging/RelayWorldBank/IDS_CSV/IDSCountry-Series.csv gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/ ;\ngsutil cp gs://pdp-feeds-staging/RelayWorldBank/IDS_CSV/IDSCountry.csv gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/ ;\ngsutil cp gs://pdp-feeds-staging/RelayWorldBank/IDS_CSV/IDSSeries.csv gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/ ;\ngsutil cp gs://pdp-feeds-staging/RelayWorldBank/IDS_CSV/IDSSeries-Time.csv gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/ ;\n",
    )
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-world-bank-intl-debt",
            "initial_node_count": 1,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    country_series_definitions_transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="country_series_definitions_transform_csv",
        startup_timeout_seconds=1000,
        name="country_series_definitions",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-world-bank-intl-debt",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_intl_debt.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/IDSCountry-Series.csv",
            "SOURCE_FILE": "files/IDSCountry-Series.csv",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "COLUMN_TO_REMOVE": "Unnamed: 3",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_intl_debt/country_series_definitions/data_output.csv",
            "PIPELINE_NAME": "country_series_definitions",
            "CSV_HEADERS": '["country_code" ,"series_code" ,"description"]',
            "RENAME_MAPPINGS": '{"CountryCode":"country_code","SeriesCode":"series_code","DESCRIPTION":"description"}',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    country_series_definitions_load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="country_series_definitions_load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="data/world_bank_intl_debt/country_series_definitions/data_output.csv",
        source_format="CSV",
        destination_project_dataset_table="world_bank_intl_debt.country_series_definitions",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "country_code", "type": "string", "mode": "nullable"},
            {"name": "series_code", "type": "string", "mode": "nullable"},
            {"name": "description", "type": "string", "mode": "nullable"},
        ],
    )

    # Run CSV transform within kubernetes pod
    country_summary_transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="country_summary_transform_csv",
        startup_timeout_seconds=1000,
        name="country_summary",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-world-bank-intl-debt",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_intl_debt.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/IDSCountry.csv",
            "SOURCE_FILE": "files/IDSCountry.csv",
            "COLUMN_TO_REMOVE": "Unnamed: 31",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_intl_debt/country_summary/data_output.csv",
            "PIPELINE_NAME": "country_summary",
            "CSV_HEADERS": '["country_code","short_name","table_name","long_name","two_alpha_code","currency_unit","special_notes","region","income_group","wb_2_code","national_accounts_base_year","national_accounts_reference_year","sna_price_valuation","lending_category","other_groups","system_of_national_accounts","alternative_conversion_factor","ppp_survey_year","balance_of_payments_manual_in_use","external_debt_reporting_status","system_of_trade","government_accounting_concept","imf_data_dissemination_standard","latest_population_census","latest_household_survey","source_of_most_recent_Income_and_expenditure_data","vital_registration_complete","latest_agricultural_census","latest_industrial_data","latest_trade_data","latest_water_withdrawal_data"]',
            "RENAME_MAPPINGS": '{"Country Code":"country_code","Short Name":"short_name","Table Name":"table_name","Long Name":"long_name","2-alpha code":"two_alpha_code","Currency Unit":"currency_unit","Special Notes":"special_notes","Region":"region","Income Group":"income_group","WB-2 code":"wb_2_code","National accounts base year":"national_accounts_base_year","National accounts reference year":"national_accounts_reference_year","SNA price valuation":"sna_price_valuation","Lending category":"lending_category","Other groups":"other_groups","System of National Accounts":"system_of_national_accounts","Alternative conversion factor":"alternative_conversion_factor","PPP survey year":"ppp_survey_year","Balance of Payments Manual in use":"balance_of_payments_manual_in_use","External debt Reporting status":"external_debt_reporting_status","System of trade":"system_of_trade","Government Accounting concept":"government_accounting_concept","IMF data dissemination standard":"imf_data_dissemination_standard","Latest population census":"latest_population_census","Latest household survey":"latest_household_survey","Source of most recent Income and expenditure data":"source_of_most_recent_Income_and_expenditure_data","Vital registration complete":"vital_registration_complete","Latest agricultural census":"latest_agricultural_census","Latest industrial data":"latest_industrial_data","Latest trade data":"latest_trade_data","Latest water withdrawal data":"latest_water_withdrawal_data"}',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    country_summary_load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="country_summary_load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="data/world_bank_intl_debt/country_summary/data_output.csv",
        source_format="CSV",
        destination_project_dataset_table="world_bank_intl_debt.country_summary",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "country_code", "type": "string", "mode": "nullable"},
            {"name": "short_name", "type": "string", "mode": "nullable"},
            {"name": "table_name", "type": "string", "mode": "nullable"},
            {"name": "long_name", "type": "string", "mode": "nullable"},
            {"name": "two_alpha_code", "type": "string", "mode": "nullable"},
            {"name": "currency_unit", "type": "string", "mode": "nullable"},
            {"name": "special_notes", "type": "string", "mode": "nullable"},
            {"name": "region", "type": "string", "mode": "nullable"},
            {"name": "income_group", "type": "string", "mode": "nullable"},
            {"name": "wb_2_code", "type": "string", "mode": "nullable"},
            {
                "name": "national_accounts_base_year",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "national_accounts_reference_year",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "sna_price_valuation", "type": "string", "mode": "nullable"},
            {"name": "lending_category", "type": "string", "mode": "nullable"},
            {"name": "other_groups", "type": "string", "mode": "nullable"},
            {
                "name": "system_of_national_accounts",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "alternative_conversion_factor",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "ppp_survey_year", "type": "string", "mode": "nullable"},
            {
                "name": "balance_of_payments_manual_in_use",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "external_debt_reporting_status",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "system_of_trade", "type": "string", "mode": "nullable"},
            {
                "name": "government_accounting_concept",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "imf_data_dissemination_standard",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "latest_population_census", "type": "string", "mode": "nullable"},
            {"name": "latest_household_survey", "type": "string", "mode": "nullable"},
            {
                "name": "source_of_most_recent_Income_and_expenditure_data",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "vital_registration_complete",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "latest_agricultural_census",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "latest_industrial_data", "type": "integer", "mode": "nullable"},
            {"name": "latest_trade_data", "type": "integer", "mode": "nullable"},
            {
                "name": "latest_water_withdrawal_data",
                "type": "string",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    series_summary_transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="series_summary_transform_csv",
        startup_timeout_seconds=1000,
        name="series_summary",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-world-bank-intl-debt",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_intl_debt.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/IDSSeries.csv",
            "SOURCE_FILE": "files/IDSSeries.csv",
            "COLUMN_TO_REMOVE": "Unnamed: 20",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_intl_debt/series_summary/data_output.csv",
            "PIPELINE_NAME": "series_summary",
            "CSV_HEADERS": '["series_code" ,"topic" ,"indicator_name" ,"short_definition" ,"long_definition" ,"unit_of_measure" ,"periodicity" ,"base_period" ,"other_notes" ,"aggregation_method" ,"limitations_and_exceptions" ,"notes_from_original_source" ,"general_comments" ,"source" ,"statistical_concept_and_methodology" ,"development_relevance" ,"related_source_links" ,"other_web_links" ,"related_indicators" ,"license_type"]',
            "RENAME_MAPPINGS": '{"Series Code":"series_code" ,"Topic":"topic" ,"Indicator Name":"indicator_name" ,"Short definition":"short_definition" ,"Long definition":"long_definition" ,"Unit of measure":"unit_of_measure" ,"Periodicity":"periodicity" ,"Base Period":"base_period" ,"Other notes":"other_notes" ,"Aggregation method":"aggregation_method" ,"Limitations and exceptions":"limitations_and_exceptions" ,"Notes from original source":"notes_from_original_source" ,"General comments":"general_comments" ,"Source":"source" ,"Statistical concept and methodology":"statistical_concept_and_methodology" ,"Development relevance":"development_relevance" ,"Related source links":"related_source_links" ,"Other web links":"other_web_links" ,"Related indicators":"related_indicators" ,"License Type":"license_type"}',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    series_summary_load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="series_summary_load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="data/world_bank_intl_debt/series_summary/data_output.csv",
        source_format="CSV",
        destination_project_dataset_table="world_bank_intl_debt.series_summary",
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
            {"name": "base_period", "type": "string", "mode": "nullable"},
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

    # Run CSV transform within kubernetes pod
    series_times_transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="series_times_transform_csv",
        startup_timeout_seconds=1000,
        name="series_times",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-world-bank-intl-debt",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_intl_debt.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/world_bank_intl_debt/raw_files/IDSSeries-Time.csv",
            "SOURCE_FILE": "files/IDSSeries-Time.csv",
            "COLUMN_TO_REMOVE": "Unnamed: 3",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_intl_debt/series_times/data_output.csv",
            "PIPELINE_NAME": "series_times",
            "CSV_HEADERS": '["series_code","year","description"]',
            "RENAME_MAPPINGS": '{"SeriesCode" : "series_code" ,"Year" : "year" ,"DESCRIPTION" : "description"}',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    series_times_load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="series_times_load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects="data/world_bank_intl_debt/series_times/data_output.csv",
        source_format="CSV",
        destination_project_dataset_table="world_bank_intl_debt.series_times",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "series_code", "type": "string", "mode": "nullable"},
            {"name": "year", "type": "integer", "mode": "nullable"},
            {"name": "description", "type": "string", "mode": "nullable"},
        ],
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-world-bank-intl-debt",
    )

    (
        [copy_gcs_to_gcs]
        >> create_cluster
        >> [
            country_series_definitions_transform_csv,
            country_summary_transform_csv,
            series_summary_transform_csv,
            series_times_transform_csv,
        ]
        >> delete_cluster
        >> [
            country_series_definitions_load_to_bq,
            country_summary_load_to_bq,
            series_summary_load_to_bq,
            series_times_load_to_bq,
        ]
    )
