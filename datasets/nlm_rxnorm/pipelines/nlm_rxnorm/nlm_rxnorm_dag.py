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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2023-03-01",
}


with DAG(
    dag_id="nlm_rxnorm.nlm_rxnorm",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="59 00 * * 6",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pubds-nlm-rxnorm",
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

    # Download all NLM RXNorm files
    download_source_files = kubernetes_engine.GKEStartPodOperator(
        task_id="download_source_files",
        name="download_source_files",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - DOWNLOAD FILES ONLY",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "DOWNLOAD_ONLY",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN ATOM Archive Load Process
    process_rxnatomarchive = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxnatomarchive",
        name="process_rxnatomarchive",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxnatomarchive data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxnatomarchive",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN CONSO Load Process
    process_rxnconso = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxnconso",
        name="process_rxnconso",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxnconso data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxnconso",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN CUI Load Process
    process_rxncui = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxncui",
        name="process_rxncui",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxncui data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxncui",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN CUI CHANGE Load Process
    process_rxncuichange = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxncuichange",
        name="process_rxncuichange",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxncuichange data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxncuichange",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN DOC Load Process
    process_rxndoc = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxndoc",
        name="process_rxndoc",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxndoc data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxndoc",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN REL Load Process
    process_rxnrel = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxnrel",
        name="process_rxnrel",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxnrel data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxnrel",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN SAB Load Process
    process_rxnsab = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxnsab",
        name="process_rxnsab",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxnsab data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxnsab",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN SAT Load Process
    process_rxnsat = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxnsat",
        name="process_rxnsat",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxnsat data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxnsat",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )

    # Execute RXN STY Load Process
    process_rxnsty = kubernetes_engine.GKEStartPodOperator(
        task_id="process_rxnsty",
        name="process_rxnsty",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-nlm-rxnorm",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.nlm_rxnorm.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "NLM RXNORM Pipeline - Process rxnsty data",
            "SOURCE_URL": "https://uts-ws.nlm.nih.gov/download?url=https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_~file_date~.zip&apiKey=~api_key~",
            "PROCESS_FILEGROUP": "rxnsty",
            "ZIP_PATH": "./files",
            "API_KEY": "{{ var.json.nlm_rxnorm.api_key }}",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nlm_rxnorm",
            "SCHEMA_FILEPATH": "data/nlm_rxnorm/schema",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "nlm_rxnorm",
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pubds-nlm-rxnorm",
    )

    (
        create_cluster
        >> download_source_files
        >> [
            process_rxnatomarchive,
            process_rxnconso,
            process_rxncui,
            process_rxncuichange,
            process_rxndoc,
            process_rxnrel,
            process_rxnsab,
            process_rxnsat,
            process_rxnsty,
        ]
        >> delete_cluster
    )
