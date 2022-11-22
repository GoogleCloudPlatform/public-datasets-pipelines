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
        bash_command="gsutil cp -R gs://pdp-feeds-staging/Libraries/libraries-1.4.0-2018-12-22/versions-1.4.0-2018-12-22.csv gs://{{ var.value.composer_bucket }}/data/libraries_io/versions/versions.csv\n",
    )

    # Run CSV transform within kubernetes pod
    transform_versions = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_versions",
        startup_timeout_seconds=600,
        name="versions",
        namespace="composer",
        service_account_name="datasets",
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
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
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

    bash_gcs_to_gcs >> transform_versions >> load_versions_to_bq
