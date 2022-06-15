# Copyright 2021 Google LLC
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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="the_general_index.the_general_index",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "the-general-index",
            "initial_node_count": 8,
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

    # Run The General Index Pipeline
    transform_csv_dump_0 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_0",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_0.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_0.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_0.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_0.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_0.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_1 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_1",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_1.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_1.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_1.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_1.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_1.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_2 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_2",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_2.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_2.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_2.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_2.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_2.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_3 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_3",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_3.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_3.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_3.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_3.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_3.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_4 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_4",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_4.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_4.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_4.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_4.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_4.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_5 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_5",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_5.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_5.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_5.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_5.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_5.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_6 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_6",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_6.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_6.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_6.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_6.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_6.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_7 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_7",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_7.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_7.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_7.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_7.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_7.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_8 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_8",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_8.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_8.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_8.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_8.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_8.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_9 = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_9",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_9.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_9.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_9.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_9.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_9.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_a = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_a",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_a.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_a.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_a.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_a.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_a.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_b = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_b",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_b.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_b.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_b.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_b.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_b.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_c = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_c",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_c.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_c.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_c.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_c.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_c.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_d = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_d",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_d.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_d.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_d.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_d.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_d.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_e = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_e",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_e.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_e.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_e.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_e.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_e.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )

    # Run The General Index Pipeline
    transform_csv_dump_f = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv_dump_f",
        name="the_general_index",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="the-general-index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.the_general_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "CHUNKSIZE": "{{ var.json.the_general_index.chunksize }}",
            "DATASET_ID": "{{ var.json.the_general_index.dataset_id }}",
            "TABLE_ID": "{{ var.json.the_general_index.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.the_general_index.schema_path }}",
            "SOURCE_FILE_HEADER_ROWS": "{{ var.json.the_general_index.source_file_header_rows }}",
            "SOURCE_FILE_FOOTER_ROWS": "{{ var.json.the_general_index.source_file_footer_rows }}",
            "PIPELINE_NAME": "{{ var.json.the_general_index.dump_f.pipeline_name }}",
            "SOURCE_URL": "{{ var.json.the_general_index.dump_f.source_url }}",
            "SOURCE_FILE": "{{ var.json.the_general_index.dump_f.source_file }}",
            "TARGET_FILE": "{{ var.json.the_general_index.dump_f.target_file }}",
            "TARGET_GCS_PATH": "{{ var.json.the_general_index.dump_f.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
            "DATA_DTYPES": '{\n  "dkey": "str",\n  "raw_id": "str",\n  "meta_key": "str",\n  "doc_doi": "str",\n  "meta_doi": "str",\n  "doi": "str",\n  "doi_flag": "str",\n  "isbn": "str",\n  "journal": "str",\n  "doc_title": "str",\n  "meta_title": "str",\n  "title": "str",\n  "doc_pub_date": "str",\n  "meta_pub_date": "str",\n  "pub_date": "str",\n  "doc_author": "str",\n  "meta_author": "str",\n  "author": "str",\n  "doc_size": "str",\n  "insert_date": "str",\n  "multi_row_flag": "str"\n}',
            "DATETIME_LIST": '[\n  "insert_date"\n]',
            "NULL_STRING_LIST": '[\n  "dkey",\n  "raw_id",\n  "meta_key",\n  "doc_doi",\n  "meta_doi",\n  "doi",\n  "doi_flag",\n  "isbn",\n  "journal",\n  "doc_title",\n  "meta_title",\n  "title",\n  "doc_pub_date",\n  "meta_pub_date",\n  "pub_date",\n  "doc_author",\n  "meta_author",\n  "author",\n  "doc_size",\n  "insert_date",\n  "multi_row_flag"\n]',
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="the_general_index",
    )

    (
        create_cluster
        >> [
            transform_csv_dump_0,
            transform_csv_dump_1,
            transform_csv_dump_2,
            transform_csv_dump_3,
            transform_csv_dump_4,
            transform_csv_dump_5,
            transform_csv_dump_6,
            transform_csv_dump_7,
            transform_csv_dump_8,
            transform_csv_dump_9,
            transform_csv_dump_a,
            transform_csv_dump_b,
            transform_csv_dump_c,
            transform_csv_dump_d,
            transform_csv_dump_e,
            transform_csv_dump_f,
        ]
        >> delete_cluster
    )
