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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-06-10",
}


with DAG(
    dag_id="uniref50.uniref50",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `uniref50.fasta` to gcs
    download_zip_file = bash.BashOperator(
        task_id="download_zip_file",
        bash_command='mkdir -p $data_dir/uniref\ncurl -o $data_dir/uniref/uniref50.fasta.gz -L $uniref50\ngunzip $data_dir/uniref/uniref50.fasta.gz\nawk \u0027BEGIN {n_seq=0;} /^\u003e/ {if(n_seq%10000000==0){file=sprintf("/home/airflow/gcs/data/uniref50/uniref/myseq%d.fa",n_seq);}\nprint \u003e\u003e file; n_seq++; next;} { print \u003e\u003e file; }\u0027 \u003c $data_dir/uniref/uniref50.fasta\nawk \u0027BEGIN {n_seq=0;} /^\u003e/ {if(n_seq%3500000==0){file=sprintf("/home/airflow/gcs/data/uniref50/uniref/myseq_1%d.fa",n_seq);}\nprint \u003e\u003e file; n_seq++; next;} { print \u003e\u003e file; }\u0027 \u003c $data_dir/uniref/myseq0.fa\nrm $data_dir/uniref/uniref50.fasta.gz\nrm $data_dir/uniref/uniref50.fasta\nrm $data_dir/uniref/myseq0.fa\n',
        env={
            "data_dir": "/home/airflow/gcs/data/uniref50",
            "uniref50": "https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz",
        },
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_1 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_1",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq_10.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_1.csv",
            "PIPELINE_NAME": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "TABLE_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_1 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_1",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_1.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_2 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_2",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq_13500000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_2.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_2.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_3 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_3",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq_17000000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_3.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_3.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_4 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_4",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq10000000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_4.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_4 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_4",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_4.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_5 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_5",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq20000000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_5.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_5 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_5",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_5.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_6 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_6",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq30000000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_6.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_6 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_6",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_6.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_7 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_7",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq40000000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_7.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_7 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_7",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_7.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    uniref50_transform_csv_8 = kubernetes_pod.KubernetesPodOperator(
        task_id="uniref50_transform_csv_8",
        startup_timeout_seconds=600,
        name="uniref50",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/uniref50/uniref/myseq50000000.fa",
            "SOURCE_FILE": "files/uniref50.fa",
            "BATCH_FILE": "files/batch.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref/data_output_8.csv",
            "PIPELINE_NAME": "uniref50",
            "TABLE_ID": "uniref50",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_uniref50_to_bq_8 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_uniref50_to_bq_8",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/uniref50/uniref/data_output_8.csv"],
        source_format="CSV",
        destination_project_dataset_table="uniref50.uniref50",
        skip_leading_rows=0,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "ClusterID",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "ClusterName",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "Size", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Organism",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "TaxID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {"name": "RepID", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "Sequence",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    (
        download_zip_file
        >> [
            uniref50_transform_csv_1,
            uniref50_transform_csv_2,
            uniref50_transform_csv_3,
            uniref50_transform_csv_4,
            uniref50_transform_csv_5,
            uniref50_transform_csv_6,
            uniref50_transform_csv_7,
            uniref50_transform_csv_8,
        ]
        >> load_uniref50_to_bq_1
        >> load_uniref50_to_bq_2
        >> load_uniref50_to_bq_3
        >> load_uniref50_to_bq_4
        >> load_uniref50_to_bq_5
        >> load_uniref50_to_bq_6
        >> load_uniref50_to_bq_7
        >> load_uniref50_to_bq_8
    )
