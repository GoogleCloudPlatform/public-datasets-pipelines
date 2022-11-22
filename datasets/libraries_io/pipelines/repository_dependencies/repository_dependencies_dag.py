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
    dag_id="libraries_io.repository_dependencies",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil cp -R gs://pdp-feeds-staging/Libraries/libraries-1.4.0-2018-12-22/repository_dependencies-1.4.0-2018-12-22.csv gs://{{ var.value.composer_bucket }}/data/libraries_io/repository_dependencies/repository_dependencies.csv\nsplit -l 37000000 --additional-suffix=.csv /home/airflow/gcs/data/libraries_io/repository_dependencies/repository_dependencies.csv /home/airflow/gcs/data/libraries_io/repository_dependencies/\nrm /home/airflow/gcs/data/libraries_io/repository_dependencies/repository_dependencies.csv\n",
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/aa.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_1.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_1.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_2 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_2",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ab.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_2.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_2.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_3 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_3",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ac.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_3.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_3.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_4 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_4",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ad.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_4.csv",
            "CHUNKSIZE": "100000",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_4 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_4",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_4.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_5 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_5",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ae.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_5.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_5 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_5",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_5.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_6 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_6",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/af.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_6.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_6 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_6",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_6.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_7 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_7",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ag.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_7.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_7 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_7",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_7.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_8 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_8",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ah.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_8.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_8 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_8",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_8.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_9 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_9",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ai.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_9.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_9 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_9",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_9.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_11 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_11",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/ak.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_11.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_11 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_11",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_11.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_repository_dependencies_10 = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_repository_dependencies_10",
        startup_timeout_seconds=600,
        name="repository_dependencies",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/repository_dependencies/aj.csv",
            "SOURCE_FILE": "files/repository_dependencies.csv",
            "TARGET_FILE": "files/data_repository_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/repository_dependencies/data_repository_dependencies_10.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "repository_dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Host Type":"host_type","Repository Name with Owner":"repository_name_with_owner","Repository ID":"repository_id", "Manifest Platform":"manifest_platform","Manifest Filepath":"manifest_filepath","Git branch":"git_branch", "Manifest kind":"manifest_kind","Optional":"optional","Dependency Project Name":"dependency_project_name", "Dependency Requirements":"dependency_requirements","Dependency Kind":"dependency_kind","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","host_type","repository_name_with_owner","repository_id","manifest_platform","manifest_filepath","git_branch", "manifest_kind","optional","dependency_project_name","dependency_requirements","dependency_kind","dependency_project_id"]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_repository_dependencies_to_bq_10 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_repository_dependencies_to_bq_10",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/libraries_io/repository_dependencies/data_repository_dependencies_10.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.repository_dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the repository dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "host_type",
                "type": "string",
                "description": "Which website the dependencys repository is hosted on, either GitHub, GitLab or Bitbucket.",
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
                "description": "The unique primary key of the repository for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "manifest_platform",
                "type": "string",
                "description": "Which package manager the dependency listed in the manifest should use.",
                "mode": "nullable",
            },
            {
                "name": "manifest_filepath",
                "type": "string",
                "description": "Path to the file where the dependency is declared within the repository.",
                "mode": "nullable",
            },
            {
                "name": "git_branch",
                "type": "string",
                "description": "Which branch was the manifest loaded from the repository.",
                "mode": "nullable",
            },
            {
                "name": "manifest_kind",
                "type": "string",
                "description": "Either manifest or lockfile, manifests are written by humans, lockfiles contain full resolved dependency tree.",
                "mode": "nullable",
            },
            {
                "name": "optional",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "dependency_project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
        ],
    )

    (
        bash_gcs_to_gcs
        >> [
            transform_repository_dependencies,
            transform_repository_dependencies_2,
            transform_repository_dependencies_3,
            transform_repository_dependencies_4,
            transform_repository_dependencies_5,
            transform_repository_dependencies_6,
            transform_repository_dependencies_7,
            transform_repository_dependencies_8,
            transform_repository_dependencies_9,
            transform_repository_dependencies_10,
            transform_repository_dependencies_11,
        ]
        >> load_repository_dependencies_to_bq
        >> load_repository_dependencies_to_bq_2
        >> load_repository_dependencies_to_bq_3
        >> load_repository_dependencies_to_bq_4
        >> load_repository_dependencies_to_bq_5
        >> load_repository_dependencies_to_bq_6
        >> load_repository_dependencies_to_bq_7
        >> load_repository_dependencies_to_bq_8
        >> load_repository_dependencies_to_bq_9
        >> load_repository_dependencies_to_bq_10
        >> load_repository_dependencies_to_bq_11
    )
