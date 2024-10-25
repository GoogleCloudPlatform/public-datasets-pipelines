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
    dag_id="fec.candidate_2020",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    candidate_2020_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="candidate_2020_transform_csv",
        startup_timeout_seconds=600,
        name="candidate_2020",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.fec.gov/files/bulk-downloads/2020/cn20.zip",
            "SOURCE_FILE_ZIP_FILE": "files/zip_file.zip",
            "SOURCE_FILE_PATH": "files/",
            "SOURCE_FILE": "files/cn.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/candidate_2020/data_output.csv",
            "PIPELINE_NAME": "candidate_2020",
            "CSV_HEADERS": '["cand_id","cand_name","cand_pty_affiliation","cand_election_yr","cand_office_st","cand_office", "cand_office_district","cand_ici","cand_status","cand_pcc","cand_st1","cand_st2","cand_city", "cand_st","cand_zip"]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_candidate_2020_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_candidate_2020_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/candidate_2020/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.candidate_2020",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "cand_id",
                "type": "string",
                "description": "Candidate Identification",
                "mode": "required",
            },
            {
                "name": "cand_name",
                "type": "string",
                "description": "Candidate Name",
                "mode": "nullable",
            },
            {
                "name": "cand_pty_affiliation",
                "type": "string",
                "description": "Party Affiliation",
                "mode": "nullable",
            },
            {
                "name": "cand_election_yr",
                "type": "integer",
                "description": "Year of Election",
                "mode": "nullable",
            },
            {
                "name": "cand_office_st",
                "type": "string",
                "description": "Candidate State",
                "mode": "nullable",
            },
            {
                "name": "cand_office",
                "type": "string",
                "description": "Candidate Office",
                "mode": "nullable",
            },
            {
                "name": "cand_office_district",
                "type": "string",
                "description": "Candidate District",
                "mode": "nullable",
            },
            {
                "name": "cand_ici",
                "type": "string",
                "description": "Incumbent Challenger Status",
                "mode": "nullable",
            },
            {
                "name": "cand_status",
                "type": "string",
                "description": "Candidate Status",
                "mode": "nullable",
            },
            {
                "name": "cand_pcc",
                "type": "string",
                "description": "Principal Campaign Committee",
                "mode": "nullable",
            },
            {
                "name": "cand_st1",
                "type": "string",
                "description": "Mailing Address - Street",
                "mode": "nullable",
            },
            {
                "name": "cand_st2",
                "type": "string",
                "description": "Mailing Address - Street 2",
                "mode": "nullable",
            },
            {
                "name": "cand_city",
                "type": "string",
                "description": "Mailing Address - City",
                "mode": "nullable",
            },
            {
                "name": "cand_st",
                "type": "string",
                "description": "Mailing Address - State",
                "mode": "nullable",
            },
            {
                "name": "cand_zip",
                "type": "string",
                "description": "Mailing Address - Zip Code",
                "mode": "nullable",
            },
        ],
    )

    candidate_2020_transform_csv >> load_candidate_2020_to_bq
