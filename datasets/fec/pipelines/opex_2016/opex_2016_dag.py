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
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="fec.opex_2016",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    opex_2016_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="opex_2016_transform_csv",
        startup_timeout_seconds=600,
        name="opex_2016",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2016/oppexp16.zip",
            "SOURCE_FILE_ZIP_FILE": "files/zip_file.zip",
            "SOURCE_FILE_PATH": "files/",
            "SOURCE_FILE": "files/oppexp.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/opex_2016/data_output.csv",
            "PIPELINE_NAME": "opex_2016",
            "CSV_HEADERS": '["cmte_id","amndt_ind","rpt_yr","rpt_tp","image_num","line_num","form_tp_cd", "sched_tp_cd","name","city","state","zip_code","transaction_dt","transaction_amt","transaction_pgi", "purpose","category","category_desc","memo_cd","memo_text","entity_tp","sub_id","file_num", "tran_id","back_ref_tran_id"]',
        },
        resources={
            "request_memory": "3G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_opex_2016_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_opex_2016_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/opex_2016/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.opex_2016",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "cmte_id",
                "type": "string",
                "description": "Filer Identification Number",
                "mode": "nullable",
            },
            {
                "name": "amndt_ind",
                "type": "string",
                "description": "Amendment Indicator",
                "mode": "nullable",
            },
            {
                "name": "rpt_yr",
                "type": "integer",
                "description": "Report Year",
                "mode": "nullable",
            },
            {
                "name": "rpt_tp",
                "type": "string",
                "description": "Report Type",
                "mode": "nullable",
            },
            {
                "name": "image_num",
                "type": "integer",
                "description": "Image Number",
                "mode": "nullable",
            },
            {
                "name": "line_num",
                "type": "string",
                "description": "Line Number",
                "mode": "nullable",
            },
            {
                "name": "form_tp_cd",
                "type": "string",
                "description": "Form Type",
                "mode": "nullable",
            },
            {
                "name": "sched_tp_cd",
                "type": "string",
                "description": "Schedule Type",
                "mode": "nullable",
            },
            {
                "name": "name",
                "type": "string",
                "description": "Contributor/Lender/Transfer Name",
                "mode": "nullable",
            },
            {
                "name": "city",
                "type": "string",
                "description": "City/Town",
                "mode": "nullable",
            },
            {
                "name": "state",
                "type": "string",
                "description": "State",
                "mode": "nullable",
            },
            {
                "name": "zip_code",
                "type": "string",
                "description": "Zip Code",
                "mode": "nullable",
            },
            {
                "name": "transaction_dt",
                "type": "date",
                "description": "Transaction Date(MMDDYYYY)",
                "mode": "nullable",
            },
            {
                "name": "transaction_amt",
                "type": "float",
                "description": "Transaction Amount",
                "mode": "nullable",
            },
            {
                "name": "transaction_pgi",
                "type": "string",
                "description": "Primary General Indicator",
                "mode": "nullable",
            },
            {
                "name": "purpose",
                "type": "string",
                "description": "Purpose",
                "mode": "nullable",
            },
            {
                "name": "category",
                "type": "string",
                "description": "Disbursement Category Code",
                "mode": "nullable",
            },
            {
                "name": "category_desc",
                "type": "string",
                "description": "Disbursement Category Code Description",
                "mode": "nullable",
            },
            {
                "name": "memo_cd",
                "type": "string",
                "description": "Memo Code",
                "mode": "nullable",
            },
            {
                "name": "memo_text",
                "type": "string",
                "description": "Memo Text",
                "mode": "nullable",
            },
            {
                "name": "entity_tp",
                "type": "string",
                "description": "Entity Type",
                "mode": "nullable",
            },
            {
                "name": "sub_id",
                "type": "integer",
                "description": "FEC Record Number",
                "mode": "required",
            },
            {
                "name": "file_num",
                "type": "integer",
                "description": "File Number / Report ID",
                "mode": "nullable",
            },
            {
                "name": "tran_id",
                "type": "string",
                "description": "Transaction ID",
                "mode": "nullable",
            },
            {
                "name": "back_ref_tran_id",
                "type": "string",
                "description": "Back Reference Transaction ID",
                "mode": "nullable",
            },
        ],
    )

    opex_2016_transform_csv >> load_opex_2016_to_bq
