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

    # Run CSV transform within kubernetes pod
    hacker_news_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="hacker_news_transform_csv",
        name="full",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/hacker_news/output.csv",
            "CHUNKSIZE": "500000",
            "CSV_HEADERS": '["title", "url", "text", "dead", "by", "score", "time", "timestamp", "type", "id","parent", "descendants", "ranking", "deleted"]',
            "DATA_DTYPES": '{\n  "title": "str",\n  "url": "str",\n  "text": "str",\n  "dead": "str",\n  "by": "str",\n  "score": "str",\n  "time": "str",\n  "timestamp": "str",\n  "type": "str",\n  "id": "str",\n  "parent": "str",\n  "descendants": "str",\n  "ranking": "str",\n  "deleted": "str"\n}',
        },
        container_resources={
            "memory": {"request": "32Gi"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/batch/hacker_news_*.csv"],
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

    hacker_news_transform_csv >> load_full_to_bq
