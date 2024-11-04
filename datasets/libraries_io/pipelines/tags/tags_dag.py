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
    dag_id="libraries_io.tags",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="if test -f /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz;\nthen\n    mkdir /home/airflow/gcs/data/libraries_io/tags/\n    cp /home/airflow/gcs/data/libraries_io/libraries-1.4.0-2018-12-22/tags-1.4.0-2018-12-22.csv /home/airflow/gcs/data/libraries_io/tags/tags.csv\n    split -l 20000000 --additional-suffix=.csv /home/airflow/gcs/data/libraries_io/tags/tags.csv /home/airflow/gcs/data/libraries_io/tags/\n    rm /home/airflow/gcs/data/libraries_io/tags/tags.csv\nelse\n    mkdir /home/airflow/gcs/data/libraries_io/\n    curl -o /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz -L https://zenodo.org/record/2536573/files/Libraries.io-open-data-1.4.0.tar.gz\n    tar -xf /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz -C /home/airflow/gcs/data/libraries_io/\n    mkdir /home/airflow/gcs/data/libraries_io/tags/\n    cp /home/airflow/gcs/data/libraries_io/libraries-1.4.0-2018-12-22/tags-1.4.0-2018-12-22.csv /home/airflow/gcs/data/libraries_io/tags/tags.csv\n    split -l 20000000 --additional-suffix=.csv /home/airflow/gcs/data/libraries_io/tags/tags.csv /home/airflow/gcs/data/libraries_io/tags/\n    rm /home/airflow/gcs/data/libraries_io/tags/tags.csv\nfi\n",
    )
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-libraries-io-tags",
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
    transform_tags = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_tags",
        startup_timeout_seconds=600,
        name="tags",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-tags",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/tags/aa.csv",
            "SOURCE_FILE": "files/tags.csv",
            "TARGET_FILE": "files/data_tags.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/tags/data_tags_1.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "tags",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Tag Name":"tag_name","Tag git sha":"tag_git_sha","Tag Published Timestamp":"tag_published_timestamp", "Tag Created Timestamp":"tag_created_timestamp","Tag Updated Timestamp":"tag_updated_timestamp"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","tag_name","tag_git_sha","tag_published_timestamp","tag_created_timestamp","tag_updated_timestamp"]',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_tags_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tags_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/tags/data_tags_1.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.tags",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the tag in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the tags repository is hosted on, either GitHub, GitLab or Bitbucket.",
                "mode": "nullable",
            },
            {
                "name": "repository_name_with_owner",
                "type": "string",
                "description": "The repository name and owner seperated by a slash, also maps to the url slug on the given repository host e.g. librariesio/libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "repository_id",
                "type": "integer",
                "description": "The unique primary key of the repository for this tag in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "tag_name",
                "type": "string",
                "description": "The name of the tag often is a version number but could be any freeform string.",
                "mode": "nullable",
            },
            {
                "name": "tag_git_sha",
                "type": "string",
                "description": "Sha of the object that the tag is pointing at in the repository.",
                "mode": "nullable",
            },
            {
                "name": "tag_published_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was published.",
                "mode": "nullable",
            },
            {
                "name": "tag_created_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was first saved by Libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "tag_updated_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was last saved by Libraries.io.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_tags_2 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_tags_2",
        startup_timeout_seconds=600,
        name="tags",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-tags",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/tags/ab.csv",
            "SOURCE_FILE": "files/tags.csv",
            "TARGET_FILE": "files/data_tags.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/tags/data_tags_2.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "tags",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Tag Name":"tag_name","Tag git sha":"tag_git_sha","Tag Published Timestamp":"tag_published_timestamp", "Tag Created Timestamp":"tag_created_timestamp","Tag Updated Timestamp":"tag_updated_timestamp"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","tag_name","tag_git_sha","tag_published_timestamp","tag_created_timestamp","tag_updated_timestamp"]',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_tags_to_bq_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tags_to_bq_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/tags/data_tags_2.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.tags",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the tag in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the tags repository is hosted on, either GitHub, GitLab or Bitbucket.",
                "mode": "nullable",
            },
            {
                "name": "repository_name_with_owner",
                "type": "string",
                "description": "The repository name and owner seperated by a slash, also maps to the url slug on the given repository host e.g. librariesio/libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "repository_id",
                "type": "integer",
                "description": "The unique primary key of the repository for this tag in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "tag_name",
                "type": "string",
                "description": "The name of the tag often is a version number but could be any freeform string.",
                "mode": "nullable",
            },
            {
                "name": "tag_git_sha",
                "type": "string",
                "description": "Sha of the object that the tag is pointing at in the repository.",
                "mode": "nullable",
            },
            {
                "name": "tag_published_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was published.",
                "mode": "nullable",
            },
            {
                "name": "tag_created_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was first saved by Libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "tag_updated_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was last saved by Libraries.io.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_tags_3 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_tags_3",
        startup_timeout_seconds=600,
        name="tags",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-tags",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/tags/ac.csv",
            "SOURCE_FILE": "files/tags.csv",
            "TARGET_FILE": "files/data_tags.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/tags/data_tags_3.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "tags",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Tag Name":"tag_name","Tag git sha":"tag_git_sha","Tag Published Timestamp":"tag_published_timestamp", "Tag Created Timestamp":"tag_created_timestamp","Tag Updated Timestamp":"tag_updated_timestamp"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","tag_name","tag_git_sha","tag_published_timestamp","tag_created_timestamp","tag_updated_timestamp"]',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_tags_to_bq_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tags_to_bq_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/tags/data_tags_3.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.tags",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the tag in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the tags repository is hosted on, either GitHub, GitLab or Bitbucket.",
                "mode": "nullable",
            },
            {
                "name": "repository_name_with_owner",
                "type": "string",
                "description": "The repository name and owner seperated by a slash, also maps to the url slug on the given repository host e.g. librariesio/libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "repository_id",
                "type": "integer",
                "description": "The unique primary key of the repository for this tag in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "tag_name",
                "type": "string",
                "description": "The name of the tag often is a version number but could be any freeform string.",
                "mode": "nullable",
            },
            {
                "name": "tag_git_sha",
                "type": "string",
                "description": "Sha of the object that the tag is pointing at in the repository.",
                "mode": "nullable",
            },
            {
                "name": "tag_published_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was published.",
                "mode": "nullable",
            },
            {
                "name": "tag_created_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was first saved by Libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "tag_updated_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when the tag was last saved by Libraries.io.",
                "mode": "nullable",
            },
        ],
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-libraries-io-tags",
    )

    (
        bash_gcs_to_gcs
        >> create_cluster
        >> [transform_tags, transform_tags_2, transform_tags_3]
        >> delete_cluster
        >> [load_tags_to_bq, load_tags_to_bq_2, load_tags_to_bq_3]
    )
