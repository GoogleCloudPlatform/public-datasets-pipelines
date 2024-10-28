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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-09-28",
}


with DAG(
    dag_id="fdic.locations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_locations_to_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_locations_to_csv",
        startup_timeout_seconds=600,
        name="locations",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.fdic.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://s3-us-gov-west-1.amazonaws.com/cg-2e5c99a6-e282-42bf-9844-35f5430338a5/downloads/locations.csv",
            "SOURCE_FILE": "files/locations.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fdic/data_output_locations.csv",
            "PIPELINE_NAME": "locations",
            "CSV_HEADERS": '["fdic_certificate_number","institution_name","branch_name","branch_number","main_office","branch_address","branch_city", "zip_code","branch_county","county_fips_code","state","state_name","institution_class","cbsa_fips_code","cbsa_name", "cbsa_division_flag","cbsa_division_fips_code","cbsa_division_name","cbsa_metro_flag","cbsa_metro_fips_code","cbsa_metro_name", "cbsa_micro_flag","csa_flag","csa_fips_code","csa_name","date_established","fdic_uninum","last_updated","service_type","branch_fdic_uninum" ]',
            "RENAME_MAPPINGS": '{"CERT":"fdic_certificate_number","NAME":"institution_name","OFFNAME":"branch_name","OFFNUM":"branch_number", "MAINOFF":"main_office","ADDRESS":"branch_address","CITY":"branch_city","ZIP":"zip_code","COUNTY":"branch_county", "STCNTY":"county_fips_code","STALP":"state","STNAME":"state_name","BKCLASS":"institution_class","CBSA_NO":"cbsa_fips_code","CBSA":"cbsa_name","CBSA_DIV_FLG":"cbsa_division_flag", "CBSA_DIV_NO":"cbsa_division_fips_code","CBSA_DIV":"cbsa_division_name","CBSA_METRO_FLG":"cbsa_metro_flag", "CBSA_METRO":"cbsa_metro_fips_code","CBSA_METRO_NAME":"cbsa_metro_name","CBSA_MICRO_FLG":"cbsa_micro_flag", "CSA_FLG":"csa_flag","CSA_NO":"csa_fips_code","CSA":"csa_name","ESTYMD":"date_established","FI_UNINUM":"fdic_uninum", "RUNDATE":"last_updated","SERVTYPE":"service_type","UNINUM":"branch_fdic_uninum"}',
            "REPLACE_BOOL_LIST": '["main_office","cbsa_division_flag","cbsa_metro_flag","cbsa_micro_flag","csa_flag"]',
            "STRING_TO_INT": "cbsa_division_fips_code",
            "FORMAT_DATE_LIST": '["date_established", "last_updated"]',
            "ZERO_TO_NULL": "cbsa_metro_fips_code",
        },
        container_resources={
            "memory": {"request": "80Gi"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_locations_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_locations_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fdic/data_output_locations.csv"],
        source_format="CSV",
        destination_project_dataset_table="fdic.locations",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "fdic_certificate_number",
                "type": "string",
                "description": "A unique number assigned by the FDIC used to identify institutions and for the issuance of insurance certificates.",
                "mode": "nullable",
            },
            {
                "name": "institution_name",
                "type": "string",
                "description": "The legal name of the institution.",
                "mode": "nullable",
            },
            {
                "name": "branch_name",
                "type": "string",
                "description": "Name of the branch.",
                "mode": "nullable",
            },
            {
                "name": "branch_number",
                "type": "string",
                "description": "The branch's corresponding office number.",
                "mode": "nullable",
            },
            {
                "name": "main_office",
                "type": "boolean",
                "description": "The main office for the institution.",
                "mode": "nullable",
            },
            {
                "name": "branch_address",
                "type": "string",
                "description": "Street address at which the branch is physically located.",
                "mode": "nullable",
            },
            {
                "name": "branch_city",
                "type": "string",
                "description": "City in which branch is physically located.",
                "mode": "nullable",
            },
            {
                "name": "zip_code",
                "type": "string",
                "description": "The first five digits of the full postal zip code representing physical location of the branch.",
                "mode": "nullable",
            },
            {
                "name": "branch_county",
                "type": "string",
                "description": "County where the branch is physically located.",
                "mode": "nullable",
            },
            {
                "name": "county_fips_code",
                "type": "string",
                "description": "A five digit number representing the state and county in which the institution is physically located.  The first two digits represent the FIPS state numeric code and the last three digits represent the FIPS county numeric code.",
                "mode": "nullable",
            },
            {
                "name": "state",
                "type": "string",
                "description": "State abbreviation in which the branch is physically located. The FDIC Act defines state as any State of the United States the District of Columbia and any territory of the United States Puerto Rico Guam American Samoa the Trust Territory of the Pacific Islands the Virgin Island and the Northern Mariana Islands.",
                "mode": "nullable",
            },
            {
                "name": "state_name",
                "type": "string",
                "description": "State in which the  branch is physically located. The FDIC Act defines state as any State of the United States the District of Columbia and any territory of the United States Puerto Rico Guam American Samoa the Trust Territory of the Pacific Islands the Virgin Island and the Northern Mariana Islands.",
                "mode": "nullable",
            },
            {
                "name": "institution_class",
                "type": "string",
                "description": '"A classification code assigned by the FDIC based on the institution\'s charter type (commercial bank or savings institution) charter agent (state or federal) Federal Reserve membership status (Fed member Fed nonmember) and its primary federal regulator (state chartered institutions are subject to both federal and state supervision). N -Commercial bank national (federal) charter and Fed member supervised by the Office of the Comptroller of the Currency (OCC) NM -Commercial bank state charter and Fed nonmember supervised by the FDIC OI - Insured U.S. branch of a foreign chartered institution (IBA) SA - Savings associations state or federal charter supervised by the Office of Thrift Supervision (OTS) SB - Savings banks state charter supervised by the FDIC SM - Commercial bank state charter and Fed member supervised by the Federal Reserve (FRB)"',
                "mode": "nullable",
            },
            {
                "name": "cbsa_fips_code",
                "type": "string",
                "description": "Numeric code of the Core Based Statistical Area (CBSA) as defined by the US Census Bureau Office of Management and Budget.",
                "mode": "nullable",
            },
            {
                "name": "cbsa_name",
                "type": "string",
                "description": "Name of the Core Based Statistical Area (CBSA) as defined by the US Census Bureau Office of Management and Budget.",
                "mode": "nullable",
            },
            {
                "name": "cbsa_division_flag",
                "type": "boolean",
                "description": "A flag indicating member of a Core Based Statistical Division as defined by the US Census Bureau Office of Management and Budget.",
                "mode": "nullable",
            },
            {
                "name": "cbsa_division_fips_code",
                "type": "integer",
                "description": "Numeric code of the Core Based Statistical Division as defined by the US Census Bureau Office of Management and Budget.",
                "mode": "nullable",
            },
            {
                "name": "cbsa_division_name",
                "type": "string",
                "description": "Name of the Core Based Statistical Division as defined by the US Census Bureau Office of Management and Budget.",
                "mode": "nullable",
            },
            {
                "name": "cbsa_metro_flag",
                "type": "boolean",
                "description": "A flag used to indicate whether an branch is in a Metropolitan Statistical Area as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "cbsa_metro_fips_code",
                "type": "string",
                "description": "Numeric code of the Metropolitan Statistical Area as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "cbsa_metro_name",
                "type": "string",
                "description": "Name of the Metropolitan Statistical Area as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "cbsa_micro_flag",
                "type": "boolean",
                "description": "A flag (1=Yes) used to indicate whether an branch is in a Micropolitan Statistical Area as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "csa_flag",
                "type": "boolean",
                "description": "Flag (1=Yes) indicating member of a Combined Statistical Area (CSA) as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "csa_fips_code",
                "type": "string",
                "description": "Numeric code of the Combined Statistical Area (CSA) as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "csa_name",
                "type": "string",
                "description": "Name of the Combined Statistical Area (CSA) as defined by the US Census Bureau Office of Management and Budget",
                "mode": "nullable",
            },
            {
                "name": "date_established",
                "type": "date",
                "description": "The date on which the branch began operations.",
                "mode": "nullable",
            },
            {
                "name": "fdic_uninum",
                "type": "string",
                "description": "This is the FDIC UNINUM of the institution that owns the branch. A UNINUM is a unique sequentially number added to the FDIC database for both banks and branches. There is no pattern imbedded within the number. The FI_UNINUM is updated with every merger or purchase of branches to reflect the most current owner.",
                "mode": "nullable",
            },
            {
                "name": "last_updated",
                "type": "date",
                "description": "The day the institution information was updated.",
                "mode": "nullable",
            },
            {
                "name": "service_type",
                "type": "string",
                "description": '"Define the various types of offices of FDIC-insured institutions. 11 -  Full Service Brick and Mortar Office 12 -  Full Service Retail Office 13 -  Full Service Cyber Office 14 -  Full Service Mobile Office 15 -  Full Service Home/Phone Banking 16 -  Full Service Seasonal Office 21 -  Limited Service Administrative Office 22 -  Limited Service Military Facility 23 -  Limited Service Facility Office 24 -  Limited Service Loan Production Office 25 -  Limited Service Consumer Credit Office 26 -  Limited Service Contractual Office 27 -  Limited Service Messenger Office 28 -  Limited Service Retail Office 29 -  Limited Service Mobile Office 30 -  Limited Service Trust Office"',
                "mode": "nullable",
            },
            {
                "name": "branch_fdic_uninum",
                "type": "string",
                "description": "Unique Identification Number for a Branch Office as assigned by the FDIC",
                "mode": "nullable",
            },
        ],
    )

    transform_locations_to_csv >> load_locations_to_bq
