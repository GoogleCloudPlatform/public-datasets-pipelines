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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery, gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-08-13",
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

    # Task to split the text file
    split_file = bash.BashOperator(
        task_id="split_file",
        bash_command='split -l 23000000 --additional-suffix=.txt "$data_dir/individuals/indiv20.txt" "$data_dir/individuals/indiv20_"\n',
        env={"data_dir": "/home/airflow/gcs/data/fec"},
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_1 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_1",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_aa.txt",
            "SOURCE_FILE": "files/indiv20_aa.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_1.csv",
            "CHUNKSIZE": "1000000",
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
    load_individuals_ingest_2020_to_bq_1 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_1",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_1.csv"],
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_2 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_2",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ab.txt",
            "SOURCE_FILE": "files/indiv20_ab.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_2.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_2.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_3 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_3",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ac.txt",
            "SOURCE_FILE": "files/indiv20_ac.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_3.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_3.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_4 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_4",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ad.txt",
            "SOURCE_FILE": "files/indiv20_ad.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_4.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_4 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_4",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_4.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_5 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_5",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ae.txt",
            "SOURCE_FILE": "files/indiv20_ae.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_5.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_5 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_5",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_5.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_6 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_6",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_af.txt",
            "SOURCE_FILE": "files/indiv20_af.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_6.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_6 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_6",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_6.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_7 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_7",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ag.txt",
            "SOURCE_FILE": "files/indiv20_ag.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_7.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_7 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_7",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_7.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_8 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_8",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ah.txt",
            "SOURCE_FILE": "files/indiv20_ah.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_8.csv",
            "CHUNKSIZE": "100000",
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
    load_individuals_ingest_2020_to_bq_8 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_8",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_8.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    individuals_ingest_2020_transform_csv_9 = kubernetes_pod.KubernetesPodOperator(
        task_id="individuals_ingest_2020_transform_csv_9",
        startup_timeout_seconds=600,
        name="individuals_ingest_2020",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/fec/individuals/indiv20_ai.txt",
            "SOURCE_FILE": "files/indiv20_ai.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/individuals/data_output_ingest_9.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "individuals_ingest_2020",
            "CSV_HEADERS": '["cmte_id","amndt_ind","rpt_tp","transaction_pgi","image_num","transaction_tp","entity_tp","name","city","state", "zip_code","employer","occupation","transaction_dt","transaction_amt","other_id","tran_id","file_num", "memo_cd","memo_text","sub_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_individuals_ingest_2020_to_bq_9 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_individuals_ingest_2020_to_bq_9",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/individuals/data_output_ingest_9.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.individuals_ingest_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
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
                "mode": "nullable",
            },
        ],
    )

    (
        download_zip_file_to_composer_bucket
        >> split_file
        >> [
            individuals_ingest_2020_transform_csv_1,
            individuals_ingest_2020_transform_csv_2,
            individuals_ingest_2020_transform_csv_3,
            individuals_ingest_2020_transform_csv_4,
            individuals_ingest_2020_transform_csv_5,
            individuals_ingest_2020_transform_csv_6,
            individuals_ingest_2020_transform_csv_7,
            individuals_ingest_2020_transform_csv_8,
            individuals_ingest_2020_transform_csv_9,
        ]
        >> load_individuals_ingest_2020_to_bq_1
        >> load_individuals_ingest_2020_to_bq_2
        >> load_individuals_ingest_2020_to_bq_3
        >> load_individuals_ingest_2020_to_bq_4
        >> load_individuals_ingest_2020_to_bq_5
        >> load_individuals_ingest_2020_to_bq_6
        >> load_individuals_ingest_2020_to_bq_7
        >> load_individuals_ingest_2020_to_bq_8
        >> load_individuals_ingest_2020_to_bq_9
    )
