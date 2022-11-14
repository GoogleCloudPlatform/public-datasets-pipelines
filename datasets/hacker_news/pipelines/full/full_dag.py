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
    "start_date": "2022-10-31",
}


with DAG(
    dag_id="hacker_news.full",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil cp -R gs://pdp-feeds-staging/Hacker_News/output/output.csv gs://{{ var.value.composer_bucket }}/data/hacker_news/\nsplit -dl 7000000 --additional-suffix=.csv /home/airflow/gcs/data/hacker_news/output.csv /home/airflow/gcs/data/hacker_news/\n",
    )

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv_1 = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv_1",
        startup_timeout_seconds=600,
        name="full",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/00.csv",
            "SOURCE_FILE": "files/00.csv",
            "SOURCE_STORAGE_FILE": "files/storage1.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/hacker_news/data_output_1.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "full",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time", "timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_1 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_1",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/data_output_1.csv"],
        source_format="CSV",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "title",
                "type": "string",
                "description": "Story title",
                "mode": "nullable",
            },
            {
                "name": "url",
                "type": "string",
                "description": "Story url",
                "mode": "nullable",
            },
            {
                "name": "text",
                "type": "string",
                "description": "Story or comment text",
                "mode": "nullable",
            },
            {
                "name": "dead",
                "type": "boolean",
                "description": "Is dead?",
                "mode": "nullable",
            },
            {
                "name": "by",
                "type": "string",
                "description": "The username of the item's author.",
                "mode": "nullable",
            },
            {
                "name": "score",
                "type": "integer",
                "description": "Story score",
                "mode": "nullable",
            },
            {
                "name": "time",
                "type": "integer",
                "description": "Unix time",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Timestamp for the unix time",
                "mode": "nullable",
            },
            {
                "name": "type",
                "type": "string",
                "description": "type of details (comment comment_ranking poll story job pollopt)",
                "mode": "nullable",
            },
            {
                "name": "id",
                "type": "integer",
                "description": "The item's unique id.",
                "mode": "nullable",
            },
            {
                "name": "parent",
                "type": "integer",
                "description": "Parent comment ID",
                "mode": "nullable",
            },
            {
                "name": "descendants",
                "type": "integer",
                "description": "Number of story or poll descendants",
                "mode": "nullable",
            },
            {
                "name": "ranking",
                "type": "integer",
                "description": "Comment ranking",
                "mode": "nullable",
            },
            {
                "name": "deleted",
                "type": "boolean",
                "description": "Is deleted?",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv_2 = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv_2",
        startup_timeout_seconds=600,
        name="full",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/01.csv",
            "SOURCE_FILE": "files/01.csv",
            "SOURCE_STORAGE_FILE": "files/storage2.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/hacker_news/data_output_2.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "full",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time","timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/data_output_2.csv"],
        source_format="CSV",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "title",
                "type": "string",
                "description": "Story title",
                "mode": "nullable",
            },
            {
                "name": "url",
                "type": "string",
                "description": "Story url",
                "mode": "nullable",
            },
            {
                "name": "text",
                "type": "string",
                "description": "Story or comment text",
                "mode": "nullable",
            },
            {
                "name": "dead",
                "type": "boolean",
                "description": "Is dead?",
                "mode": "nullable",
            },
            {
                "name": "by",
                "type": "string",
                "description": "The username of the item's author.",
                "mode": "nullable",
            },
            {
                "name": "score",
                "type": "integer",
                "description": "Story score",
                "mode": "nullable",
            },
            {
                "name": "time",
                "type": "integer",
                "description": "Unix time",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Timestamp for the unix time",
                "mode": "nullable",
            },
            {
                "name": "type",
                "type": "string",
                "description": "type of details (comment comment_ranking poll story job pollopt)",
                "mode": "nullable",
            },
            {
                "name": "id",
                "type": "integer",
                "description": "The item's unique id.",
                "mode": "nullable",
            },
            {
                "name": "parent",
                "type": "integer",
                "description": "Parent comment ID",
                "mode": "nullable",
            },
            {
                "name": "descendants",
                "type": "integer",
                "description": "Number of story or poll descendants",
                "mode": "nullable",
            },
            {
                "name": "ranking",
                "type": "integer",
                "description": "Comment ranking",
                "mode": "nullable",
            },
            {
                "name": "deleted",
                "type": "boolean",
                "description": "Is deleted?",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv_3 = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv_3",
        startup_timeout_seconds=600,
        name="full",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/02.csv",
            "SOURCE_FILE": "files/02.csv",
            "SOURCE_STORAGE_FILE": "files/storage3.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/hacker_news/data_output_3.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "full",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time","timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/data_output_3.csv"],
        source_format="CSV",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "title",
                "type": "string",
                "description": "Story title",
                "mode": "nullable",
            },
            {
                "name": "url",
                "type": "string",
                "description": "Story url",
                "mode": "nullable",
            },
            {
                "name": "text",
                "type": "string",
                "description": "Story or comment text",
                "mode": "nullable",
            },
            {
                "name": "dead",
                "type": "boolean",
                "description": "Is dead?",
                "mode": "nullable",
            },
            {
                "name": "by",
                "type": "string",
                "description": "The username of the item's author.",
                "mode": "nullable",
            },
            {
                "name": "score",
                "type": "integer",
                "description": "Story score",
                "mode": "nullable",
            },
            {
                "name": "time",
                "type": "integer",
                "description": "Unix time",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Timestamp for the unix time",
                "mode": "nullable",
            },
            {
                "name": "type",
                "type": "string",
                "description": "type of details (comment comment_ranking poll story job pollopt)",
                "mode": "nullable",
            },
            {
                "name": "id",
                "type": "integer",
                "description": "The item's unique id.",
                "mode": "nullable",
            },
            {
                "name": "parent",
                "type": "integer",
                "description": "Parent comment ID",
                "mode": "nullable",
            },
            {
                "name": "descendants",
                "type": "integer",
                "description": "Number of story or poll descendants",
                "mode": "nullable",
            },
            {
                "name": "ranking",
                "type": "integer",
                "description": "Comment ranking",
                "mode": "nullable",
            },
            {
                "name": "deleted",
                "type": "boolean",
                "description": "Is deleted?",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv_4 = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv_4",
        startup_timeout_seconds=600,
        name="full",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/03.csv",
            "SOURCE_FILE": "files/03.csv",
            "SOURCE_STORAGE_FILE": "files/storage4.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/hacker_news/data_output_4.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "full",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time","timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_4 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_4",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/data_output_4.csv"],
        source_format="CSV",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "title",
                "type": "string",
                "description": "Story title",
                "mode": "nullable",
            },
            {
                "name": "url",
                "type": "string",
                "description": "Story url",
                "mode": "nullable",
            },
            {
                "name": "text",
                "type": "string",
                "description": "Story or comment text",
                "mode": "nullable",
            },
            {
                "name": "dead",
                "type": "boolean",
                "description": "Is dead?",
                "mode": "nullable",
            },
            {
                "name": "by",
                "type": "string",
                "description": "The username of the item's author.",
                "mode": "nullable",
            },
            {
                "name": "score",
                "type": "integer",
                "description": "Story score",
                "mode": "nullable",
            },
            {
                "name": "time",
                "type": "integer",
                "description": "Unix time",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Timestamp for the unix time",
                "mode": "nullable",
            },
            {
                "name": "type",
                "type": "string",
                "description": "type of details (comment comment_ranking poll story job pollopt)",
                "mode": "nullable",
            },
            {
                "name": "id",
                "type": "integer",
                "description": "The item's unique id.",
                "mode": "nullable",
            },
            {
                "name": "parent",
                "type": "integer",
                "description": "Parent comment ID",
                "mode": "nullable",
            },
            {
                "name": "descendants",
                "type": "integer",
                "description": "Number of story or poll descendants",
                "mode": "nullable",
            },
            {
                "name": "ranking",
                "type": "integer",
                "description": "Comment ranking",
                "mode": "nullable",
            },
            {
                "name": "deleted",
                "type": "boolean",
                "description": "Is deleted?",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv_5 = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv_5",
        startup_timeout_seconds=600,
        name="full",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/05.csv",
            "SOURCE_FILE": "files/04.csv",
            "SOURCE_STORAGE_FILE": "files/storage5.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/hacker_news/data_output_5.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "full",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time","timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_5 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_5",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/data_output_5.csv"],
        source_format="CSV",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "title",
                "type": "string",
                "description": "Story title",
                "mode": "nullable",
            },
            {
                "name": "url",
                "type": "string",
                "description": "Story url",
                "mode": "nullable",
            },
            {
                "name": "text",
                "type": "string",
                "description": "Story or comment text",
                "mode": "nullable",
            },
            {
                "name": "dead",
                "type": "boolean",
                "description": "Is dead?",
                "mode": "nullable",
            },
            {
                "name": "by",
                "type": "string",
                "description": "The username of the item's author.",
                "mode": "nullable",
            },
            {
                "name": "score",
                "type": "integer",
                "description": "Story score",
                "mode": "nullable",
            },
            {
                "name": "time",
                "type": "integer",
                "description": "Unix time",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Timestamp for the unix time",
                "mode": "nullable",
            },
            {
                "name": "type",
                "type": "string",
                "description": "type of details (comment comment_ranking poll story job pollopt)",
                "mode": "nullable",
            },
            {
                "name": "id",
                "type": "integer",
                "description": "The item's unique id.",
                "mode": "nullable",
            },
            {
                "name": "parent",
                "type": "integer",
                "description": "Parent comment ID",
                "mode": "nullable",
            },
            {
                "name": "descendants",
                "type": "integer",
                "description": "Number of story or poll descendants",
                "mode": "nullable",
            },
            {
                "name": "ranking",
                "type": "integer",
                "description": "Comment ranking",
                "mode": "nullable",
            },
            {
                "name": "deleted",
                "type": "boolean",
                "description": "Is deleted?",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv_6 = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv_6",
        startup_timeout_seconds=600,
        name="full",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/05.csv",
            "SOURCE_FILE": "files/05.csv",
            "SOURCE_STORAGE_FILE": "files/storage6.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/hacker_news/data_output_6.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "full",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time","timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_6 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_6",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/data_output_6.csv"],
        source_format="CSV",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "title",
                "type": "string",
                "description": "Story title",
                "mode": "nullable",
            },
            {
                "name": "url",
                "type": "string",
                "description": "Story url",
                "mode": "nullable",
            },
            {
                "name": "text",
                "type": "string",
                "description": "Story or comment text",
                "mode": "nullable",
            },
            {
                "name": "dead",
                "type": "boolean",
                "description": "Is dead?",
                "mode": "nullable",
            },
            {
                "name": "by",
                "type": "string",
                "description": "The username of the item's author.",
                "mode": "nullable",
            },
            {
                "name": "score",
                "type": "integer",
                "description": "Story score",
                "mode": "nullable",
            },
            {
                "name": "time",
                "type": "integer",
                "description": "Unix time",
                "mode": "nullable",
            },
            {
                "name": "timestamp",
                "type": "timestamp",
                "description": "Timestamp for the unix time",
                "mode": "nullable",
            },
            {
                "name": "type",
                "type": "string",
                "description": "type of details (comment comment_ranking poll story job pollopt)",
                "mode": "nullable",
            },
            {
                "name": "id",
                "type": "integer",
                "description": "The item's unique id.",
                "mode": "nullable",
            },
            {
                "name": "parent",
                "type": "integer",
                "description": "Parent comment ID",
                "mode": "nullable",
            },
            {
                "name": "descendants",
                "type": "integer",
                "description": "Number of story or poll descendants",
                "mode": "nullable",
            },
            {
                "name": "ranking",
                "type": "integer",
                "description": "Comment ranking",
                "mode": "nullable",
            },
            {
                "name": "deleted",
                "type": "boolean",
                "description": "Is deleted?",
                "mode": "nullable",
            },
        ],
    )

    (
        bash_gcs_to_gcs
        >> [
            hacker_news_transform_csv_1,
            hacker_news_transform_csv_2,
            hacker_news_transform_csv_3,
            hacker_news_transform_csv_4,
            hacker_news_transform_csv_5,
            hacker_news_transform_csv_6,
        ]
        >> load_full_to_bq_1
        >> load_full_to_bq_2
        >> load_full_to_bq_3
        >> load_full_to_bq_4
        >> load_full_to_bq_5
        >> load_full_to_bq_6
    )
