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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery, gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="multilingual_spoken_words_corpus.multilingual_spoken_words_corpus",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@quarterly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a GCS to GCS
    copy_metadata_file_to_gcs = gcs_to_gcs.GCSToGCSOperator(
        task_id="copy_metadata_file_to_gcs",
        source_bucket="{{ var.json.multilingual_spoken_words_corpus.source_bucket }}",
        source_object="metadata.json.gz",
        destination_bucket="{{ var.value.composer_bucket }}",
        destination_object="data/multilingual_spoken_words_corpus/metadata.json.gz",
        move_object=False,
    )

    # Task to unzip tar file
    unzip_metadata_gz = bash.BashOperator(
        task_id="unzip_metadata_gz",
        bash_command="echo Unzipping $data_dir/$source_file...\ngunzip -c $data_dir/$source_file \u003e $data_dir/metadata.json\necho Successfully unzipped .gz file to specified file metadata.json\n",
        env={
            "data_dir": "/home/airflow/gcs/data/multilingual_spoken_words_corpus",
            "source_file": "metadata.json.gz",
        },
    )
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-multilingual-spoken-words-corpus",
            "initial_node_count": 1,
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
    metadata_csv_transform = kubernetes_engine.GKEStartPodOperator(
        task_id="metadata_csv_transform",
        startup_timeout_seconds=600,
        name="metadata_csv_transform",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-multilingual-spoken-words-corpus",
        image_pull_policy="Always",
        image="{{ var.json.multilingual_spoken_words_corpus.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/multilingual_spoken_words_corpus/metadata.json",
            "SOURCE_FILE": "./files/metadata.json",
            "TARGET_CSV_FILE": "./files/metadata_data_output.csv",
            "COLUMNS": '["lang_abbr", "language", "number_of_words","word", "word_count", "filename"]',
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/multilingual_spoken_words_corpus/metadata_data_output.csv",
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-multilingual-spoken-words-corpus",
    )

    # Task to load CSV data to a BigQuery table
    load_metadata_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_metadata_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/multilingual_spoken_words_corpus/metadata_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="multilingual_spoken_words_corpus.metadata",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "lang_abbr",
                "type": "string",
                "description": "It consists of language abbrevation.",
                "mode": "nullable",
            },
            {
                "name": "language",
                "type": "string",
                "description": "It consists of language name.",
                "mode": "nullable",
            },
            {
                "name": "number_of_words",
                "type": "integer",
                "description": "It consists count of total number of words for corresponding language.",
                "mode": "nullable",
            },
            {
                "name": "word",
                "type": "string",
                "description": "It contains words of each corresponding language.",
                "mode": "nullable",
            },
            {
                "name": "word_count",
                "type": "integer",
                "description": "It consists word count for each word in corresponding language",
                "mode": "nullable",
            },
            {
                "name": "filename",
                "type": "string",
                "description": "It consists filenames for corresponding word in specific language.",
                "mode": "nullable",
            },
        ],
    )

    (
        copy_metadata_file_to_gcs
        >> unzip_metadata_gz
        >> create_cluster
        >> metadata_csv_transform
        >> delete_cluster
        >> load_metadata_to_bq
    )
