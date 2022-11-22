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
    dag_id="libraries_io.projects",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil cp -R gs://pdp-feeds-staging/Libraries/libraries-1.4.0-2018-12-22/projects-1.4.0-2018-12-22.csv gs://{{ var.value.composer_bucket }}/data/libraries_io/projects/projects.csv\n",
    )

    # Run CSV transform within kubernetes pod
    transform_projects = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_projects",
        startup_timeout_seconds=600,
        name="projects",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/projects/projects.csv",
            "SOURCE_FILE": "files/projects.csv",
            "TARGET_FILE": "files/data_projects.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/projects/data_projects.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "projects",
            "CSV_HEADERS": '["id","platform","name","created_timestamp","updated_timestamp","description","keywords","homepage_url","licenses", "repository_url","versions_count","sourcerank","latest_release_publish_timestamp","latest_release_number", "package_manager_id","dependent_projects_count","language","status","last_synced_timestamp", "dependent_repositories_count","repository_id"]',
            "RENAME_MAPPINGS": '{"ID":"id","Platform":"platform","Name":"name","Created Timestamp":"created_timestamp","Updated Timestamp":"updated_timestamp", "Description":"description","Keywords":"keywords","Homepage URL":"homepage_url","Licenses":"licenses","Repository URL":"repository_url", "Versions Count":"versions_count","SourceRank":"sourcerank","Latest Release Publish Timestamp":"latest_release_publish_timestamp", "Latest Release Number":"latest_release_number","Package Manager ID":"package_manager_id","Dependent Projects Count":"dependent_projects_count", "Language":"language","Status":"status","Last synced Timestamp":"last_synced_timestamp","Dependent Repositories Count":"dependent_repositories_count", "Repository ID":"repository_id"}',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_projects_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_projects_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/projects/data_projects.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.projects",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the project in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "platform",
                "type": "string",
                "description": "The name of the Package manager the project is available on.",
                "mode": "nullable",
            },
            {
                "name": "name",
                "type": "string",
                "description": "The name of the project, unique by Platform (case sensitive).",
                "mode": "nullable",
            },
            {
                "name": "created_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when Libraries.io first discovered the project.",
                "mode": "nullable",
            },
            {
                "name": "updated_timestamp",
                "type": "timestamp",
                "description": "The timestamp of when Libraries.io last saved a change to the project.",
                "mode": "nullable",
            },
            {
                "name": "description",
                "type": "string",
                "description": "Description provided by the package manager, falling back to description from repository if empty.",
                "mode": "nullable",
            },
            {
                "name": "keywords",
                "type": "string",
                "description": "Comma separated array of keywords if supported by package manager.",
                "mode": "nullable",
            },
            {
                "name": "homepage_url",
                "type": "string",
                "description": "URL of webpage or repository as provided by package managers that support it.",
                "mode": "nullable",
            },
            {
                "name": "licenses",
                "type": "string",
                "description": 'Comma separated array of SPDX identifiers for licenses declared in package manager meta data or submitted manually by Libraries.io user via "project suggection" feature.',
                "mode": "nullable",
            },
            {
                "name": "repository_url",
                "type": "string",
                "description": 'URL of source code repository declared in package manager metadata or submitted manually by Libraries.io user via "project suggection" feature.',
                "mode": "nullable",
            },
            {
                "name": "versions_count",
                "type": "integer",
                "description": "Number of published versions of the project found by Libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "sourcerank",
                "type": "integer",
                "description": "Libraries.io defined score based on quality, popularity and community metrics.",
                "mode": "nullable",
            },
            {
                "name": "latest_release_publish_timestamp",
                "type": "timestamp",
                "description": "Time of the latest release detected by Libraries.io (ordered by semver, falling back to publish date for invalid semver).",
                "mode": "nullable",
            },
            {
                "name": "latest_release_number",
                "type": "string",
                "description": "Version number of the latest release detected by Libraries.io (ordered by semver, falling back to publish date for invalid semver).",
                "mode": "nullable",
            },
            {
                "name": "package_manager_id",
                "type": "integer",
                "description": "Unique ID of project from package manager API, only currently used by PlatformIO.",
                "mode": "nullable",
            },
            {
                "name": "dependent_projects_count",
                "type": "integer",
                "description": "Number of other projects that declare the project as a dependency in one or more of their versions.",
                "mode": "nullable",
            },
            {
                "name": "language",
                "type": "string",
                "description": "Primary programming language the project is written in, pulled from the repository if source is hosted on GitHub.",
                "mode": "nullable",
            },
            {
                "name": "status",
                "type": "string",
                "description": 'Either Active, Deprecated, Unmaintained, Help Wanted, Removed, no value also means active. Updated when detected by Libraries.io or submitted manually by Libraries.io user via "project suggection" feature.',
                "mode": "nullable",
            },
            {
                "name": "last_synced_timestamp",
                "type": "timestamp",
                "description": "Timestamp of when Libraries.io last synced the project from it's package manager API.",
                "mode": "nullable",
            },
            {
                "name": "dependent_repositories_count",
                "type": "integer",
                "description": "The total count of open source repositories that list the project as a dependency as detected by Libraries.io.",
                "mode": "nullable",
            },
            {
                "name": "repository_id",
                "type": "integer",
                "description": "The unique primary key of the repository for this project in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    bash_gcs_to_gcs >> transform_projects >> load_projects_to_bq
