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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="fec.candidate_committee_2018",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    candidate_committee_2018_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="candidate_committee_2018_transform_csv",
        startup_timeout_seconds=600,
        name="candidate_committee_2018",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2018/ccl18.zip",
            "SOURCE_FILE_ZIP_FILE": "files/zip_file.zip",
            "SOURCE_FILE_PATH": "files/",
            "SOURCE_FILE": "files/ccl.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/candidate_committee_2018/data_output.csv",
            "PIPELINE_NAME": "candidate_committee_2018",
            "CSV_HEADERS": '["cand_id","cand_election_yr","fec_election_yr","cmte_id","cmte_tp","cmte_design","linkage_id"]',
        },
        resources={
            "request_memory": "3G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_candidate_committee_2018_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_candidate_committee_2018_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/candidate_committee_2018/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.candidate_committee_2018",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "cand_id",
                "type": "string",
                "description": "Candidate Identification",
                "mode": "nullable",
            },
            {
                "name": "cand_election_yr",
                "type": "integer",
                "description": "Candidate Election Year",
                "mode": "nullable",
            },
            {
                "name": "fec_election_yr",
                "type": "integer",
                "description": "FEC Election Year",
                "mode": "nullable",
            },
            {
                "name": "cmte_id",
                "type": "string",
                "description": "Committee Identification",
                "mode": "nullable",
            },
            {
                "name": "cmte_tp",
                "type": "string",
                "description": "Committee Type",
                "mode": "nullable",
            },
            {
                "name": "cmte_design",
                "type": "string",
                "description": "Committee Designation",
                "mode": "nullable",
            },
            {
                "name": "linkage_id",
                "type": "integer",
                "description": "Linkage ID",
                "mode": "nullable",
            },
        ],
    )

    candidate_committee_2018_transform_csv >> load_candidate_committee_2018_to_bq
