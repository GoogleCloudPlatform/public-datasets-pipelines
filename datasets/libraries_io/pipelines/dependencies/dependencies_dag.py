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
    dag_id="libraries_io.dependencies",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-libraries-io-dependencies",
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

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="if test -f /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz;\nthen\n    mkdir /home/airflow/gcs/data/libraries_io/dependencies/\n    cp /home/airflow/gcs/data/libraries_io/libraries-1.4.0-2018-12-22/dependencies-1.4.0-2018-12-22.csv /home/airflow/gcs/data/libraries_io/dependencies/dependencies.csv\n    split -l 40000000 --additional-suffix=.csv /home/airflow/gcs/data/libraries_io/dependencies/dependencies.csv /home/airflow/gcs/data/libraries_io/dependencies/\n    rm /home/airflow/gcs/data/libraries_io/dependencies/dependencies.csv\nelse\n    mkdir /home/airflow/gcs/data/libraries_io/\n    curl -o /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz -L https://zenodo.org/record/2536573/files/Libraries.io-open-data-1.4.0.tar.gz\n    tar -xf /home/airflow/gcs/data/libraries_io/lib-1.6.0.tar.gz -C /home/airflow/gcs/data/libraries_io/\n    mkdir /home/airflow/gcs/data/libraries_io/dependencies/\n    cp /home/airflow/gcs/data/libraries_io/libraries-1.4.0-2018-12-22/dependencies-1.4.0-2018-12-22.csv /home/airflow/gcs/data/libraries_io/dependencies/dependencies.csv\n    split -l 40000000 --additional-suffix=.csv /home/airflow/gcs/data/libraries_io/dependencies/dependencies.csv /home/airflow/gcs/data/libraries_io/dependencies/\n    rm /home/airflow/gcs/data/libraries_io/dependencies/dependencies.c\nfi\n",
    )

    # Run CSV transform within kubernetes pod
    transform_dependencies = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_dependencies",
        startup_timeout_seconds=600,
        name="dependencies",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-dependencies",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/dependencies/aa.csv",
            "SOURCE_FILE": "files/dependencies.csv",
            "TARGET_FILE": "files/data_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/dependencies/data_dependencies_1.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Platform":"platform","Project Name":"project_name","Project ID":"project_id","Version Number":"version_number", "Version ID":"version_id","Dependency Name":"dependency_name","Dependency Platform":"dependency_platform", "Dependency Kind":"dependency_kind","Optional Dependency":"optional_dependency", "Dependency Requirements":"dependency_requirements","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","platform","project_name","project_id","version_number","version_id","dependency_name","dependency_platform", "dependency_kind","optional_dependency","dependency_requirements","dependency_project_id"]',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_dependencies_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_dependencies_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/dependencies/data_dependencies_1.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "platform",
                "type": "string",
                "description": "The name of the Package manager the dependency is available on.",
                "mode": "nullable",
            },
            {
                "name": "project_name",
                "type": "string",
                "description": "The name of the project the dependency belongs to.",
                "mode": "nullable",
            },
            {
                "name": "project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "version_number",
                "type": "string",
                "description": "The number of the version that the dependency belongs to.",
                "mode": "nullable",
            },
            {
                "name": "version_id",
                "type": "integer",
                "description": "The unique primary key of the version for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "dependency_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_platform",
                "type": "string",
                "description": "The name of the package manager that the project that the dependency specifies is available from (only different for Atom).",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "optional_dependency",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
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
    transform_dependencies_2 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_dependencies_2",
        startup_timeout_seconds=600,
        name="dependencies",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-dependencies",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/dependencies/ab.csv",
            "SOURCE_FILE": "files/dependencies.csv",
            "TARGET_FILE": "files/data_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/dependencies/data_dependencies_2.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Platform":"platform","Project Name":"project_name","Project ID":"project_id","Version Number":"version_number", "Version ID":"version_id","Dependency Name":"dependency_name","Dependency Platform":"dependency_platform", "Dependency Kind":"dependency_kind","Optional Dependency":"optional_dependency", "Dependency Requirements":"dependency_requirements","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","platform","project_name","project_id","version_number","version_id","dependency_name","dependency_platform", "dependency_kind","optional_dependency","dependency_requirements","dependency_project_id"]',
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_dependencies_to_bq_2 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_dependencies_to_bq_2",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/dependencies/data_dependencies_2.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_APPEND",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "platform",
                "type": "string",
                "description": "The name of the Package manager the dependency is available on.",
                "mode": "nullable",
            },
            {
                "name": "project_name",
                "type": "string",
                "description": "The name of the project the dependency belongs to.",
                "mode": "nullable",
            },
            {
                "name": "project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "version_number",
                "type": "string",
                "description": "The number of the version that the dependency belongs to.",
                "mode": "nullable",
            },
            {
                "name": "version_id",
                "type": "integer",
                "description": "The unique primary key of the version for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "dependency_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_platform",
                "type": "string",
                "description": "The name of the package manager that the project that the dependency specifies is available from (only different for Atom).",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "optional_dependency",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
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
    transform_dependencies_3 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_dependencies_3",
        startup_timeout_seconds=600,
        name="dependencies",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-libraries-io-dependencies",
        image_pull_policy="Always",
        image="{{ var.json.libraries_io.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/libraries_io/dependencies/ac.csv",
            "SOURCE_FILE": "files/dependencies.csv",
            "TARGET_FILE": "files/data_dependencies.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/libraries_io/dependencies/data_dependencies_3.csv",
            "CHUNKSIZE": "100000",
            "PIPELINE_NAME": "dependencies",
            "RENAME_MAPPINGS": '{"ID":"id","Platform":"platform","Project Name":"project_name","Project ID":"project_id","Version Number":"version_number", "Version ID":"version_id","Dependency Name":"dependency_name","Dependency Platform":"dependency_platform", "Dependency Kind":"dependency_kind","Optional Dependency":"optional_dependency", "Dependency Requirements":"dependency_requirements","Dependency Project ID":"dependency_project_id"}',
            "CSV_HEADERS": '["id","platform","project_name","project_id","version_number","version_id","dependency_name","dependency_platform", "dependency_kind","optional_dependency","dependency_requirements","dependency_project_id"]',
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
        name="pdp-libraries-io-dependencies",
    )

    # Task to load CSV data to a BigQuery table
    load_dependencies_to_bq_3 = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_dependencies_to_bq_3",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/libraries_io/dependencies/data_dependencies_3.csv"],
        source_format="CSV",
        destination_project_dataset_table="libraries_io.dependencies",
        skip_leading_rows=2,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "id",
                "type": "integer",
                "description": "The unique primary key of the dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "platform",
                "type": "string",
                "description": "The name of the Package manager the dependency is available on.",
                "mode": "nullable",
            },
            {
                "name": "project_name",
                "type": "string",
                "description": "The name of the project the dependency belongs to.",
                "mode": "nullable",
            },
            {
                "name": "project_id",
                "type": "integer",
                "description": "The unique primary key of the project for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "version_number",
                "type": "string",
                "description": "The number of the version that the dependency belongs to.",
                "mode": "nullable",
            },
            {
                "name": "version_id",
                "type": "integer",
                "description": "The unique primary key of the version for this dependency in the Libraries.io database.",
                "mode": "nullable",
            },
            {
                "name": "dependency_name",
                "type": "string",
                "description": "The name of the project that the dependency specifies.",
                "mode": "nullable",
            },
            {
                "name": "dependency_platform",
                "type": "string",
                "description": "The name of the package manager that the project that the dependency specifies is available from (only different for Atom).",
                "mode": "nullable",
            },
            {
                "name": "dependency_kind",
                "type": "string",
                "description": "The type of dependency, often declared for the phase of usage, e.g. runtime, test, development, build.",
                "mode": "nullable",
            },
            {
                "name": "optional_dependency",
                "type": "string",
                "description": "Is the dependency optional?.",
                "mode": "nullable",
            },
            {
                "name": "dependency_requirements",
                "type": "string",
                "description": "The version or range of versions that the dependency specifies, resolution of that to a particular version is package manager specific.",
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
        >> create_cluster
        >> [transform_dependencies, transform_dependencies_2, transform_dependencies_3]
        >> delete_cluster
        >> load_dependencies_to_bq
        >> load_dependencies_to_bq_2
        >> load_dependencies_to_bq_3
    )
