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
    dag_id="cms_medicare.physicians_and_other_supplier_2014",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    physicians_2014_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="physicians_2014_transform_csv",
        startup_timeout_seconds=600,
        name="cms_medicare_physicians_and_other_supplier_2014",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.cms_medicare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "http://download.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Medicare_Provider_Util_Payment_PUF_CY2014.zip",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cms_medicare/physicians_and_other_supplier_2014/data_output.csv",
            "CSV_HEADERS": '["npi","nppes_provider_last_org_name","nppes_provider_first_name","nppes_provider_mi","nppes_credentials","nppes_provider_gender","nppes_entity_code","nppes_provider_street1","nppes_provider_street2","nppes_provider_city","nppes_provider_zip","nppes_provider_state","nppes_provider_country","provider_type","medicare_participation_indicator","place_of_service","hcpcs_code","hcpcs_description","hcpcs_drug_indicator","line_srvc_cnt","bene_unique_cnt","bene_day_srvc_cnt","average_medicare_allowed_amt","average_submitted_chrg_amt","average_medicare_payment_amt","average_medicare_standard_amt"]',
            "RENAME_MAPPINGS": '{"npi": "npi","nppes_provider_last_org_name": "nppes_provider_last_org_name","nppes_provider_first_name": "nppes_provider_first_name","nppes_provider_mi": "nppes_provider_mi","nppes_credentials": "nppes_credentials","nppes_provider_gender": "nppes_provider_gender","nppes_entity_code": "nppes_entity_code","nppes_provider_street1": "nppes_provider_street1","nppes_provider_street2":"nppes_provider_street2","nppes_provider_city": "nppes_provider_city","nppes_provider_zip": "nppes_provider_zip","nppes_provider_state": "nppes_provider_state","nppes_provider_country": "nppes_provider_country","provider_type": "provider_type","medicare_participation_indicator": "medicare_participation_indicator","place_of_service": "place_of_service","hcpcs_code": "hcpcs_code","hcpcs_description": "hcpcs_description","hcpcs_drug_indicator": "hcpcs_drug_indicator","line_srvc_cnt": "line_srvc_cnt","bene_unique_cnt": "bene_unique_cnt","bene_day_srvc_cnt": "bene_day_srvc_cnt","average_Medicare_allowed_amt": "average_medicare_allowed_amt","average_submitted_chrg_amt": "average_submitted_chrg_amt","average_Medicare_payment_amt": "average_medicare_payment_amt","average_Medicare_standard_amt": "average_medicare_standard_amt"}',
            "PIPELINE_NAME": "physicians_and_other_supplier_2014",
        },
        resources={"limit_memory": "4G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_physicians_2014_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_physicians_2014_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/cms_medicare/physicians_and_other_supplier_2014/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="cms_medicare.physicians_and_other_supplier_2014",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "National Provider Identifier",
                "name": "npi",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "Last Name/Organization Name of the Provider",
                "name": "nppes_provider_last_org_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "First Name of the Provider",
                "name": "nppes_provider_first_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Middle Initial of the Provider",
                "name": "nppes_provider_mi",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Credentials of the Provider",
                "name": "nppes_credentials",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Gender of the Provider",
                "name": "nppes_provider_gender",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "Entity Type of the Provider",
                "name": "nppes_entity_code",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Street Address 1 of the Provider",
                "name": "nppes_provider_street1",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Street Address 2 of the Provider",
                "name": "nppes_provider_street2",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "City of the Provider",
                "name": "nppes_provider_city",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Zip Code of the Provider",
                "name": "nppes_provider_zip",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "State Code of the Provider",
                "name": "nppes_provider_state",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Country Code of the Provider",
                "name": "nppes_provider_country",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Provider Type of the Provider",
                "name": "provider_type",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Medicare Participation Indicator",
                "name": "medicare_participation_indicator",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Place of Service",
                "name": "place_of_service",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "HCPCS Code",
                "name": "hcpcs_code",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "HCPCS Description",
                "name": "hcpcs_description",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Identifies HCPCS As Drug Included in the ASP Drug List",
                "name": "hcpcs_drug_indicator",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "Number of Services",
                "name": "line_srvc_cnt",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "Number of Medicare Beneficiaries",
                "name": "bene_unique_cnt",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "Number of Distinct Medicare Beneficiary/Per Day Services",
                "name": "bene_day_srvc_cnt",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "Average Medicare Allowed Amount",
                "name": "average_medicare_allowed_amt",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "Average Submitted Charge Amount",
                "name": "average_submitted_chrg_amt",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "Average Medicare Payment Amount",
                "name": "average_medicare_payment_amt",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "Average Medicare Standardized Payment Amount",
                "name": "average_medicare_standard_amt",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
        ],
    )

    physicians_2014_transform_csv >> load_physicians_2014_to_bq
