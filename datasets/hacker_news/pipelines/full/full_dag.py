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
from airflow.providers.google.cloud.operators import kubernetes_engine
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
    schedule_interval="0 10 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil -m rm -a gs://{{ var.value.composer_bucket }}/data/hacker_news/batch/**\ngsutil cp `gsutil ls gs://hacker-news-backups/*_data.json |sort |tail -n 2 |head -n 1` gs://{{ var.value.composer_bucket }}/data/hacker_news/source_file.json\n",
    )
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-hacker-news",
            "initial_node_count": 2,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv",
        name="generate_output_files",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-hacker-news",
        image_pull_policy="Always",
        image="{{ var.json.hacker_news.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_OBJECT": "data/hacker_news/source_file.json",
            "CHUNK_SIZE": "50000",
            "TARGET_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_LOCAL_DIR": "data/hacker_news/",
            "OUTPUT_CSV_HEADERS": '[ "title", "url", "text", "dead", "by",\n  "score", "time", "timestamp", "type", "id",\n  "parent", "descendants", "ranking", "deleted" ]',
        },
        container_resources={
            "memory": {"request": "48Gi"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-hacker-news",
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/hacker_news/batch/hn_processed_*.csv"],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="hacker_news.full",
        skip_leading_rows=1,
        ignore_unknown_values=True,
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

    (
        bash_gcs_to_gcs
        >> create_cluster
        >> transform_csv
        >> delete_cluster
        >> load_full_to_bq
    )
