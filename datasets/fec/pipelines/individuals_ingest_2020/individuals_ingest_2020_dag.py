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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery, gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="fec.individuals_ingest_2020",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to archive the CSV file in the destination bucket
    download_zip_file_to_composer_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="download_zip_file_to_composer_bucket",
        source_bucket="pdp-feeds-staging",
        source_object="FEC/unzipped/indiv20",
        destination_bucket="{{ var.value.composer_bucket }}",
        destination_object="data/fec/individuals/indiv20.txt",
        move_object=False,
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20.txt",
            "SOURCE_FILE": "files/indiv20.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest.csv",
            "PIPELINE_NAME": "individuals_ingest_2020",
            "CSV_HEADERS": '["cmte_id","amndt_ind","rpt_tp","transaction_pgi","image_num","transaction_tp","entity_tp","name","city","state", "zip_code","employer","occupation","transaction_dt","transaction_amt","other_id","tran_id","file_num", "memo_cd","memo_text","sub_id"]',
            "RENAME_MAPPINGS": '{"0":"cmte_id","1":"amndt_ind","2":"rpt_tp","3":"transaction_pgi","4":"image_num","5":"transaction_tp", "6":"entity_tp","7":"name","8":"city","9":"state","10":"zip_code","11":"employer", "12":"occupation","13":"transaction_dt","14":"transaction_amt","15":"other_id","16":"tran_id", "17":"file_num","18":"memo_cd","19":"memo_text","20":"sub_id"}',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_individuals_ingest_2020_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
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
                "name": "rpt_tp",
                "type": "string",
                "description": "Report Type",
                "mode": "nullable",
            },
            {
                "name": "transaction_pgi",
                "type": "string",
                "description": "Primary-General Indicator",
                "mode": "nullable",
            },
            {
                "name": "image_num",
                "type": "integer",
                "description": "Image Number",
                "mode": "nullable",
            },
            {
                "name": "transaction_tp",
                "type": "string",
                "description": "Transaction Type",
                "mode": "nullable",
            },
            {
                "name": "entity_tp",
                "type": "string",
                "description": "Entity Type",
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
                "name": "employer",
                "type": "string",
                "description": "Employer",
                "mode": "nullable",
            },
            {
                "name": "occupation",
                "type": "string",
                "description": "Occupation",
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
                "name": "other_id",
                "type": "string",
                "description": "Other Identification Number",
                "mode": "nullable",
            },
            {
                "name": "tran_id",
                "type": "string",
                "description": "Transaction ID",
                "mode": "nullable",
            },
            {
                "name": "file_num",
                "type": "integer",
                "description": "File Number / Report ID",
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
                "name": "sub_id",
                "type": "integer",
                "description": "FEC Record Number",
                "mode": "required",
            },
        ],
    )

    (
        download_zip_file_to_composer_bucket
        >> individuals_ingest_2020_transform_csv
        >> load_individuals_ingest_2020_to_bq
    )
