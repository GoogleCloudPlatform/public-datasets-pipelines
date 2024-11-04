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
    "start_date": "2022-11-15",
}


with DAG(
    dag_id="libraries_io.versions",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="if test -f /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz;\nthen\n    mkdir /home/airflow/gcs/data/libraries_io/versions/\n    cp /home/airflow/gcs/data/libraries_io/libraries-1.4.0-2018-12-22/versions-1.4.0-2018-12-22.csv /home/airflow/gcs/data/libraries_io/versions/versions.csv\nelse\n    mkdir /home/airflow/gcs/data/libraries_io/\n    curl -o /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz -L https://zenodo.org/record/2536573/files/Libraries.io-open-data-1.4.0.tar.gz\n    tar -xf /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz -C /home/airflow/gcs/data/libraries_io/\n    mkdir /home/airflow/gcs/data/libraries_io/versions/\n    cp /home/airflow/gcs/data/libraries_io/libraries-1.4.0-2018-12-22/versions-1.4.0-2018-12-22.csv /home/airflow/gcs/data/libraries_io/versions/versions.csv\nfi\n",
    )
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-libraries-io-versions",
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
    transform_versions = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_versions",
        startup_timeout_seconds=600,
        name="versions",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-versions",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/versions/versions.csv",
            "SOURCE_FILE": "files/versions.csv",
            "TARGET_FILE": "files/data_versions.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/versions/data_versions.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "versions",
            "RENAME_MAPPINGS": '{"ID":"id","Platform":"platform","Project Name":"project_name","Project ID":"project_id","Number":"number", "Published Timestamp":"published_timestamp","Created Timestamp":"created_timestamp","Updated Timestamp":"updated_timestamp"}',
            "CSV_HEADERS": '["id","platform","project_name","project_id","number","published_timestamp","created_timestamp","updated_timestamp"]',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_versions_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_versions_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/versions/data_versions.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.versions",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the version in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "platform",
                "type": "string",
                "description": "The name of the Package manager the version is available on.",
                "mode": "nullable",
            },
            {
                "name": "project_name",
                "type": "string",
                "description": "The name of the project the version belongs to.",
                "mode": "nullable",
            },
            {
                "name": "project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this version in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "number",
                "type": "string",
                "description": "The number of the release often confirms to semantic versioning.",
                "mode": "nullable",
            },
            {
                "name": "published_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the version was published.",
                "mode": "nullable",
            },
            {
                "name": "created_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the version was first detected by Libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "updated_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the version was last saved by Libraries.io.",
                "mode": "nullable",
            },
        ],
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-libraries-io-versions",
    )

    (
        bash_gcs_to_gcs
        >> create_cluster
        >> transform_versions
        >> delete_cluster
        >> load_versions_to_bq
    )
