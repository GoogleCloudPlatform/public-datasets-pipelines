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

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-06-10",
}


with DAG(
    dag_id="uniref50.uniref50",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="5 0 * * 6",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pubds-uniref",
            "initial_node_count": 1,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-highmem-8",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Task to copy `uniref50.fasta` to gcs
    download_zip_file = bash.BashOperator(
        task_id="download_zip_file",
        bash_command='mkdir -p /home/airflow/gcs/data/uniref50/uniref\nrm /home/airflow/gcs/data/uniref50/uniref/*.gz\ncurl --ipv4 https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz -o /home/airflow/gcs/data/uniref50/uniref/uniref50.fasta.gz\ngunzip -c /home/airflow/gcs/data/uniref50/uniref/uniref50.fasta.gz |sed \u0027s/:\u003e/~@/g\u0027 |sed \u0027s/ TaxID=/~@Size=/g\u0027 |sed \u0027s/\u003e\\(UniRef50_[^[:space:]]*[[:space:]]\\)/ClusterID=\\1~@TaxID=/;s/ ~@/~@/\u0027 |sed \u0027s/ RepID=/~@ClusterName=/g\u0027 |sed \u0027s/ Tax=/~@Sequence=/g\u0027 |sed \u0027s/ n=/~@RepID=/g\u0027 |sed \u0027s/ClusterID=//g\u0027 |sed \u0027s/TaxID=//g\u0027 |sed \u0027s/RepID=//g\u0027 |sed \u0027s/Sequence=//g\u0027 |sed \u0027s/Size=//g\u0027 |sed \u0027s/ClusterName=//g\u0027 |sed \u0027/^UniRef50_/ s/$/~@ENDOFHEADERROW/\u0027 |sed \u0027/~@ENDOFHEADERROW/! s/$/-/\u0027 |perl -p -e \u0027s/-\\n/-/g\u0027 |sed \u0027s/\\-UniRef/-\\nUniRef/g\u0027 |perl -p -e \u0027s/ENDOFHEADERROW\\n//g\u0027 |sed \u0027s/~@$//g\u0027 | split -a 3 -d -l 1000000 --numeric-suffixes --filter=\u0027gzip -9 \u003e /home/airflow/gcs/data/uniref50/uniref/$FILE.txt.gz; echo "Compressed to file $FILE.txt.gz"\u0027\n',
    )

    # Run CSV transform within kubernetes pod
    transform_load_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_load_csv",
        startup_timeout_seconds=6000,
        name="uniref",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pubds-uniref",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.uniref50.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "uniref50",
            "DESTINATION_FOLDER": "files",
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_PATH": "data/uniref50/uniref",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/uniref50/uniref",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "uniref50",
            "TABLE_ID": "uniref50",
            "CSV_HEADERS": '[\n  "ClusterID",\n  "ClusterName",\n  "Size",\n  "Organism",\n  "TaxID",\n  "RepID",\n  "Sequence"\n]',
            "DATA_DTYPES": '{\n  "ClusterID": "str",\n  "ClusterName": "str",\n  "Size": "str",\n  "Organism": "str",\n  "TaxID": "str",\n  "RepID": "str",\n  "Sequence": "str"\n}',
            "REORDER_HEADERS_LIST": '[\n  "ClusterID",\n  "RepID",\n  "TaxID",\n  "Sequence",\n  "ClusterName",\n  "Size",\n  "Organism"\n]',
            "FIELD_SEPARATOR": "~@",
            "SCHEMA_PATH": "data/uniref50/uniref50_schema.json",
            "CHUNKSIZE": "100000",
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pubds-uniref",
    )

    create_cluster >> download_zip_file >> transform_load_csv >> delete_cluster
