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
    dag_id="cms_medicare.inpatient_charges",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    inpatient_2011_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="inpatient_2011_transform_csv",
        startup_timeout_seconds=600,
        name="cms_medicare_inpatient_charges_2011",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cms_medicare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Inpatient_Data_2011_CSV.zip",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cms_medicare/inpatient_charges_2011/data_output.csv",
            "CSV_HEADERS": '["provider_id","provider_name","provider_street_address","provider_city","provider_state","provider_zipcode","drg_definition","hospital_referral_region_description","total_discharges","average_covered_charges","average_total_payments","average_medicare_payments"]',
            "RENAME_MAPPINGS": '{"Provider Id": "provider_id","Provider Name": "provider_name","Provider Street Address": "provider_street_address","Provider City": "provider_city","Provider State": "provider_state","Provider Zip Code": "provider_zipcode","DRG Definition": "drg_definition","Hospital Referral Region (HRR) Description": "hospital_referral_region_description","Total Discharges": "total_discharges","Average Covered Charges": "average_covered_charges","Average Total Payments": "average_total_payments","Average Medicare Payments": "average_medicare_payments"}',
            "PIPELINE_NAME": "inpatient_charges_2011",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Run CSV transform within kubernetes pod
    inpatient_2012_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="inpatient_2012_transform_csv",
        startup_timeout_seconds=600,
        name="cms_medicare_inpatient_charges_2012",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cms_medicare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Inpatient_Data_2012_CSV.zip",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cms_medicare/inpatient_charges_2012/data_output.csv",
            "CSV_HEADERS": '["provider_id","provider_name","provider_street_address","provider_city","provider_state","provider_zipcode","drg_definition","hospital_referral_region_description","total_discharges","average_covered_charges","average_total_payments","average_medicare_payments"]',
            "RENAME_MAPPINGS": '{"Provider Id": "provider_id","Provider Name": "provider_name","Provider Street Address": "provider_street_address","Provider City": "provider_city","Provider State": "provider_state","Provider Zip Code": "provider_zipcode","DRG Definition": "drg_definition","Hospital Referral Region (HRR) Description": "hospital_referral_region_description","Total Discharges": "total_discharges","Average Covered Charges": "average_covered_charges","Average Total Payments": "average_total_payments","Average Medicare Payments": "average_medicare_payments"}',
            "PIPELINE_NAME": "inpatient_charges_2012",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Run CSV transform within kubernetes pod
    inpatient_2013_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="inpatient_2013_transform_csv",
        startup_timeout_seconds=600,
        name="cms_medicare_inpatient_charges_2013",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cms_medicare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Inpatient_Data_2013_CSV.zip",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cms_medicare/inpatient_charges_2013/data_output.csv",
            "CSV_HEADERS": '["provider_id","provider_name","provider_street_address","provider_city","provider_state","provider_zipcode","drg_definition","hospital_referral_region_description","total_discharges","average_covered_charges","average_total_payments","average_medicare_payments"]',
            "RENAME_MAPPINGS": '{"Provider Id": "provider_id","Provider Name": "provider_name","Provider Street Address": "provider_street_address","Provider City": "provider_city","Provider State": "provider_state","Provider Zip Code": "provider_zipcode","DRG Definition": "drg_definition","Hospital Referral Region (HRR) Description": "hospital_referral_region_description","Total Discharges": "total_discharges","Average Covered Charges": "average_covered_charges","Average Total Payments": "average_total_payments","Average Medicare Payments": "average_medicare_payments"}',
            "PIPELINE_NAME": "inpatient_charges_2013",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Run CSV transform within kubernetes pod
    inpatient_2014_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="inpatient_2014_transform_csv",
        startup_timeout_seconds=600,
        name="cms_medicare_inpatient_charges_2014",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cms_medicare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Inpatient_Data_2014_CSV.zip",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cms_medicare/inpatient_charges_2014/data_output.csv",
            "CSV_HEADERS": '["provider_id","provider_name","provider_street_address","provider_city","provider_state","provider_zipcode","drg_definition","hospital_referral_region_description","total_discharges","average_covered_charges","average_total_payments","average_medicare_payments"]',
            "RENAME_MAPPINGS": '{"Provider Id": "provider_id","Provider Name": "provider_name","Provider Street Address": "provider_street_address","Provider City": "provider_city","Provider State": "provider_state","Provider Zip Code": "provider_zipcode","DRG Definition": "drg_definition","Hospital Referral Region (HRR) Description": "hospital_referral_region_description","Total Discharges": "total_discharges","Average Covered Charges": "average_covered_charges","Average Total Payments": "average_total_payments","Average Medicare Payments": "average_medicare_payments"}',
            "PIPELINE_NAME": "inpatient_charges_2014",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Run CSV transform within kubernetes pod
    inpatient_2015_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="inpatient_2015_transform_csv",
        startup_timeout_seconds=600,
        name="cms_medicare_inpatient_charges_2015",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cms_medicare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Downloads/Inpatient_Data_2015_CSV.zip",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cms_medicare/inpatient_charges_2015/data_output.csv",
            "CSV_HEADERS": '["provider_id","provider_name","provider_street_address","provider_city","provider_state","provider_zipcode","drg_definition","hospital_referral_region_description","total_discharges","average_covered_charges","average_total_payments","average_medicare_payments"]',
            "RENAME_MAPPINGS": '{"Provider Id": "provider_id","Provider Name": "provider_name","Provider Street Address": "provider_street_address","Provider City": "provider_city","Provider State": "provider_state","Provider Zip Code": "provider_zipcode","DRG Definition": "drg_definition","Hospital Referral Region (HRR) Description": "hospital_referral_region_description","Total Discharges": "total_discharges","Average Covered Charges": "average_covered_charges","Average Total Payments": "average_total_payments","Average Medicare Payments": "average_medicare_payments"}',
            "PIPELINE_NAME": "inpatient_charges_2015",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_inpatient_2011_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_inpatient_2011_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/cms_medicare/inpatient_charges_2011/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="cms_medicare.inpatient_charges_2011",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "The CMS Certification Number (CCN) of the provider billing for outpatient hospital services",
                "name": "provider_id",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The name of the provider",
                "name": "provider_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The street address in which the provider is physically located",
                "name": "provider_street_address",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The city in which the provider is physically located",
                "name": "provider_city",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The state in which the provider is physically located",
                "name": "provider_state",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The zip code in which the provider is physically located",
                "name": "provider_zipcode",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The code and description identifying the MS-DRG. MS-DRGs are a classification system that groups similar clinical conditions (diagnoses) and the procedures furnished by the hospital during the stay",
                "name": "drg_definition",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The Hospital Referral Region (HRR) in which the provider is physically located",
                "name": "hospital_referral_region_description",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The number of discharges billed by the provider for inpatient hospital services",
                "name": "total_discharges",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The provider's average charge for services covered by Medicare for all discharges in the MS-DRG. These will vary from hospital to hospital because of differences in hospital charge structures",
                "name": "average_covered_charges",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average total payments to all providers for the MS-DRG including the MSDRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Also included 5 in average total payments are co-payment and deductible amounts that the patient is responsible for and any additional payments by third parties for coordination of benefits",
                "name": "average_total_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average amount that Medicare pays to the provider for Medicare's share of the MS-DRG. Average Medicare payment amounts include the MS-DRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Medicare payments DO NOT include beneficiary co-payments and deductible amounts nor any additional payments from third parties for coordination of benefits",
                "name": "average_medicare_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_inpatient_2012_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_inpatient_2012_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/cms_medicare/inpatient_charges_2012/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="cms_medicare.inpatient_charges_2012",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "The CMS Certification Number (CCN) of the provider billing for outpatient hospital services",
                "name": "provider_id",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The name of the provider",
                "name": "provider_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The street address in which the provider is physically located",
                "name": "provider_street_address",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The city in which the provider is physically located",
                "name": "provider_city",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The state in which the provider is physically located",
                "name": "provider_state",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The zip code in which the provider is physically located",
                "name": "provider_zipcode",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The code and description identifying the MS-DRG. MS-DRGs are a classification system that groups similar clinical conditions (diagnoses) and the procedures furnished by the hospital during the stay",
                "name": "drg_definition",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The Hospital Referral Region (HRR) in which the provider is physically located",
                "name": "hospital_referral_region_description",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The number of discharges billed by the provider for inpatient hospital services",
                "name": "total_discharges",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The provider's average charge for services covered by Medicare for all discharges in the MS-DRG. These will vary from hospital to hospital because of differences in hospital charge structures",
                "name": "average_covered_charges",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average total payments to all providers for the MS-DRG including the MSDRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Also included 5 in average total payments are co-payment and deductible amounts that the patient is responsible for and any additional payments by third parties for coordination of benefits",
                "name": "average_total_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average amount that Medicare pays to the provider for Medicare's share of the MS-DRG. Average Medicare payment amounts include the MS-DRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Medicare payments DO NOT include beneficiary co-payments and deductible amounts nor any additional payments from third parties for coordination of benefits",
                "name": "average_medicare_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_inpatient_2013_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_inpatient_2013_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/cms_medicare/inpatient_charges_2013/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="cms_medicare.inpatient_charges_2013",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "The CMS Certification Number (CCN) of the provider billing for outpatient hospital services",
                "name": "provider_id",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The name of the provider",
                "name": "provider_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The street address in which the provider is physically located",
                "name": "provider_street_address",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The city in which the provider is physically located",
                "name": "provider_city",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The state in which the provider is physically located",
                "name": "provider_state",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The zip code in which the provider is physically located",
                "name": "provider_zipcode",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The code and description identifying the MS-DRG. MS-DRGs are a classification system that groups similar clinical conditions (diagnoses) and the procedures furnished by the hospital during the stay",
                "name": "drg_definition",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The Hospital Referral Region (HRR) in which the provider is physically located",
                "name": "hospital_referral_region_description",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The number of discharges billed by the provider for inpatient hospital services",
                "name": "total_discharges",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The provider's average charge for services covered by Medicare for all discharges in the MS-DRG. These will vary from hospital to hospital because of differences in hospital charge structures",
                "name": "average_covered_charges",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average total payments to all providers for the MS-DRG including the MSDRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Also included 5 in average total payments are co-payment and deductible amounts that the patient is responsible for and any additional payments by third parties for coordination of benefits",
                "name": "average_total_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average amount that Medicare pays to the provider for Medicare's share of the MS-DRG. Average Medicare payment amounts include the MS-DRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Medicare payments DO NOT include beneficiary co-payments and deductible amounts nor any additional payments from third parties for coordination of benefits",
                "name": "average_medicare_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_inpatient_2014_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_inpatient_2014_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/cms_medicare/inpatient_charges_2014/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="cms_medicare.inpatient_charges_2014",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "The CMS Certification Number (CCN) of the provider billing for outpatient hospital services",
                "name": "provider_id",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The name of the provider",
                "name": "provider_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The street address in which the provider is physically located",
                "name": "provider_street_address",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The city in which the provider is physically located",
                "name": "provider_city",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The state in which the provider is physically located",
                "name": "provider_state",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The zip code in which the provider is physically located",
                "name": "provider_zipcode",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The code and description identifying the MS-DRG. MS-DRGs are a classification system that groups similar clinical conditions (diagnoses) and the procedures furnished by the hospital during the stay",
                "name": "drg_definition",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The Hospital Referral Region (HRR) in which the provider is physically located",
                "name": "hospital_referral_region_description",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The number of discharges billed by the provider for inpatient hospital services",
                "name": "total_discharges",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The provider's average charge for services covered by Medicare for all discharges in the MS-DRG. These will vary from hospital to hospital because of differences in hospital charge structures",
                "name": "average_covered_charges",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average total payments to all providers for the MS-DRG including the MSDRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Also included 5 in average total payments are co-payment and deductible amounts that the patient is responsible for and any additional payments by third parties for coordination of benefits",
                "name": "average_total_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average amount that Medicare pays to the provider for Medicare's share of the MS-DRG. Average Medicare payment amounts include the MS-DRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Medicare payments DO NOT include beneficiary co-payments and deductible amounts nor any additional payments from third parties for coordination of benefits",
                "name": "average_medicare_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_inpatient_2015_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_inpatient_2015_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/cms_medicare/inpatient_charges_2015/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="cms_medicare.inpatient_charges_2015",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "The CMS Certification Number (CCN) of the provider billing for outpatient hospital services",
                "name": "provider_id",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The name of the provider",
                "name": "provider_name",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The street address in which the provider is physically located",
                "name": "provider_street_address",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The city in which the provider is physically located",
                "name": "provider_city",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The state in which the provider is physically located",
                "name": "provider_state",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The zip code in which the provider is physically located",
                "name": "provider_zipcode",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The code and description identifying the MS-DRG. MS-DRGs are a classification system that groups similar clinical conditions (diagnoses) and the procedures furnished by the hospital during the stay",
                "name": "drg_definition",
                "type": "STRING",
                "mode": "REQUIRED",
            },
            {
                "description": "The Hospital Referral Region (HRR) in which the provider is physically located",
                "name": "hospital_referral_region_description",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {
                "description": "The number of discharges billed by the provider for inpatient hospital services",
                "name": "total_discharges",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "description": "The provider's average charge for services covered by Medicare for all discharges in the MS-DRG. These will vary from hospital to hospital because of differences in hospital charge structures",
                "name": "average_covered_charges",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average total payments to all providers for the MS-DRG including the MSDRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Also included 5 in average total payments are co-payment and deductible amounts that the patient is responsible for and any additional payments by third parties for coordination of benefits",
                "name": "average_total_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {
                "description": "The average amount that Medicare pays to the provider for Medicare's share of the MS-DRG. Average Medicare payment amounts include the MS-DRG amount, teaching, disproportionate share, capital, and outlier payments for all cases. Medicare payments DO NOT include beneficiary co-payments and deductible amounts nor any additional payments from third parties for coordination of benefits",
                "name": "average_medicare_payments",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
        ],
    )

    inpatient_2011_transform_csv >> load_inpatient_2011_to_bq
    inpatient_2012_transform_csv >> load_inpatient_2012_to_bq
    inpatient_2013_transform_csv >> load_inpatient_2013_to_bq
    inpatient_2014_transform_csv >> load_inpatient_2014_to_bq
    inpatient_2015_transform_csv >> load_inpatient_2015_to_bq
