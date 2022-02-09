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
    dag_id="world_bank_intl_debt.country_summary",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    country_summary_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="country_summary_transform_csv",
        startup_timeout_seconds=600,
        name="country_summary",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.world_bank_intl_debt.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://pdp-feeds-staging/RelayWorldBank/IDS_CSV/IDSCountry.csv",
            "SOURCE_FILE": "files/data.csv",
            "COLUMN_TO_REMOVE": "Unnamed: 31",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/world_bank_intl_debt/country_summary/data_output.csv",
            "PIPELINE_NAME": "country_summary",
            "CSV_HEADERS": '["country_code","short_name","table_name","long_name","two_alpha_code","currency_unit","special_notes","region","income_group","wb_2_code","national_accounts_base_year","national_accounts_reference_year","sna_price_valuation","lending_category","other_groups","system_of_national_accounts","alternative_conversion_factor","ppp_survey_year","balance_of_payments_manual_in_use","external_debt_reporting_status","system_of_trade","government_accounting_concept","imf_data_dissemination_standard","latest_population_census","latest_household_survey","source_of_most_recent_Income_and_expenditure_data","vital_registration_complete","latest_agricultural_census","latest_industrial_data","latest_trade_data","latest_water_withdrawal_data"]',
            "RENAME_MAPPINGS": '{"Country Code":"country_code","Short Name":"short_name","Table Name":"table_name","Long Name":"long_name","2-alpha code":"two_alpha_code","Currency Unit":"currency_unit","Special Notes":"special_notes","Region":"region","Income Group":"income_group","WB-2 code":"wb_2_code","National accounts base year":"national_accounts_base_year","National accounts reference year":"national_accounts_reference_year","SNA price valuation":"sna_price_valuation","Lending category":"lending_category","Other groups":"other_groups","System of National Accounts":"system_of_national_accounts","Alternative conversion factor":"alternative_conversion_factor","PPP survey year":"ppp_survey_year","Balance of Payments Manual in use":"balance_of_payments_manual_in_use","External debt Reporting status":"external_debt_reporting_status","System of trade":"system_of_trade","Government Accounting concept":"government_accounting_concept","IMF data dissemination standard":"imf_data_dissemination_standard","Latest population census":"latest_population_census","Latest household survey":"latest_household_survey","Source of most recent Income and expenditure data":"source_of_most_recent_Income_and_expenditure_data","Vital registration complete":"vital_registration_complete","Latest agricultural census":"latest_agricultural_census","Latest industrial data":"latest_industrial_data","Latest trade data":"latest_trade_data"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_country_summary_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_country_summary_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/world_bank_intl_debt/country_summary/data_output.csv"],
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
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    country_summary_transform_csv >> load_country_summary_to_bq
