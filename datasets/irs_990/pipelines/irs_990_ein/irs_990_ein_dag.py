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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="irs_990.irs_990_ein",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to download source files
    download_source_files = bash.BashOperator(
        task_id="download_source_files",
        bash_command="mkdir -p $data_dir\ncurl -o $data_dir/eo1.csv -L https://www.irs.gov/pub/irs-soi/eo1.csv\ncurl -o $data_dir/eo2.csv -L https://www.irs.gov/pub/irs-soi/eo2.csv\ncurl -o $data_dir/eo3.csv -L https://www.irs.gov/pub/irs-soi/eo3.csv\ncurl -o $data_dir/eo4.csv -L https://www.irs.gov/pub/irs-soi/eo4.csv\ncurl -o $data_dir/eo_pr.csv -L https://www.irs.gov/pub/irs-soi/eo_pr.csv\ncurl -o $data_dir/eo_xx.csv -L https://www.irs.gov/pub/irs-soi/eo_xx.csv\n",
        env={"data_dir": "/home/airflow/gcs/data/irs_990/source"},
    )

    # Task to transform csv files
    transform_source_files = bash.BashOperator(
        task_id="transform_source_files",
        bash_command="mkdir -p $dst_dir\nfor file in $src_dir/*;\ndo\n  echo Transforming $file and writing output to $dst_dir/$(basename $file) .\n  sed \u00271s/[A-Z]/\\L\u0026/g\u0027 $file \u003e $dst_dir/$(basename $file);\ndone\n",
        env={
            "src_dir": "/home/airflow/gcs/data/irs_990/source",
            "dst_dir": "/home/airflow/gcs/data/irs_990/output",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_irs_990_ein_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_irs_990_ein_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/irs_990/output/eo*.csv"],
        source_format="CSV",
        destination_project_dataset_table="irs_990.irs_990_ein",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "ein",
                "type": "string",
                "description": "Employer Identification Number (EIN)",
                "mode": "required",
            },
            {
                "name": "name",
                "type": "string",
                "description": "Primary Name of Organization",
                "mode": "nullable",
            },
            {
                "name": "ico",
                "type": "string",
                "description": "In Care of Name",
                "mode": "nullable",
            },
            {
                "name": "street",
                "type": "string",
                "description": "Street Address",
                "mode": "nullable",
            },
            {
                "name": "city",
                "type": "string",
                "description": "City",
                "mode": "nullable",
            },
            {
                "name": "state",
                "type": "string",
                "description": "State",
                "mode": "nullable",
            },
            {
                "name": "zip",
                "type": "string",
                "description": "Zip Code",
                "mode": "nullable",
            },
            {
                "name": "group",
                "type": "integer",
                "description": "Group Exemption Number",
                "mode": "nullable",
            },
            {
                "name": "subsection",
                "type": "integer",
                "description": "Subsection Code",
                "mode": "nullable",
            },
            {
                "name": "affiliation",
                "type": "integer",
                "description": "Affiliation Code",
                "mode": "nullable",
            },
            {
                "name": "classification",
                "type": "integer",
                "description": "Classification Code(s)",
                "mode": "nullable",
            },
            {
                "name": "ruling",
                "type": "integer",
                "description": "Ruling Date",
                "mode": "nullable",
            },
            {
                "name": "deductibility",
                "type": "integer",
                "description": "Deductibility Code",
                "mode": "nullable",
            },
            {
                "name": "foundation",
                "type": "integer",
                "description": "Foundation Code",
                "mode": "nullable",
            },
            {
                "name": "activity",
                "type": "integer",
                "description": "Activity Codes",
                "mode": "nullable",
            },
            {
                "name": "organization",
                "type": "integer",
                "description": "Organization Code",
                "mode": "nullable",
            },
            {
                "name": "status",
                "type": "integer",
                "description": "Exempt Organization Status Code",
                "mode": "nullable",
            },
            {
                "name": "tax_period",
                "type": "integer",
                "description": "Tax Period",
                "mode": "nullable",
            },
            {
                "name": "asset_cd",
                "type": "integer",
                "description": "Asset Code",
                "mode": "nullable",
            },
            {
                "name": "income_cd",
                "type": "integer",
                "description": "Income Code",
                "mode": "nullable",
            },
            {
                "name": "filing_req_cd",
                "type": "integer",
                "description": "Filing Requirement Code",
                "mode": "nullable",
            },
            {
                "name": "pf_filing_req_cd",
                "type": "integer",
                "description": "PF Filing Requirement Code",
                "mode": "nullable",
            },
            {
                "name": "acct_pd",
                "type": "integer",
                "description": "Accounting Period",
                "mode": "nullable",
            },
            {
                "name": "asset_amt",
                "type": "integer",
                "description": "Asset Amount",
                "mode": "nullable",
            },
            {
                "name": "income_amt",
                "type": "integer",
                "description": "Income Amount (includes negative sign if amount is negative)",
                "mode": "nullable",
            },
            {
                "name": "revenue_amt",
                "type": "integer",
                "description": "Form 990 Revenue Amount (includes negative sign if amount is negative)",
                "mode": "nullable",
            },
            {
                "name": "ntee_cd",
                "type": "string",
                "description": "National Taxonomy of Exempt Entities (NTEE) Code",
                "mode": "nullable",
            },
            {
                "name": "sort_name",
                "type": "string",
                "description": "Sort Name (Secondary Name Line)",
                "mode": "nullable",
            },
        ],
    )

    download_source_files >> transform_source_files >> load_irs_990_ein_to_bq
