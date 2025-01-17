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
    dag_id="fec.committee_2016",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    committee_2016_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="committee_2016_transform_csv",
        startup_timeout_seconds=600,
        name="committee_2016",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.fec.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2016/cm16.zip",
            "SOURCE_FILE_ZIP_FILE": "files/zip_file.zip",
            "SOURCE_FILE_PATH": "files/",
            "SOURCE_FILE": "files/cm.txt",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fec/committee_2016/data_output.csv",
            "PIPELINE_NAME": "committee_2016",
            "CSV_HEADERS": '["cmte_id","cmte_nm","tres_nm","cmte_st1","cmte_st2","cmte_city","cmte_st","cmte_zip","cmte_dsgn","cmte_tp", "cmte_pty_affiliation","cmte_filing_freq","org_tp","connected_org_nm","cand_id"]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_committee_2016_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_committee_2016_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fec/committee_2016/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="fec.committee_2016",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "cmte_id",
                "type": "string",
                "description": "Committee Identification",
                "mode": "required",
            },
            {
                "name": "cmte_nm",
                "type": "string",
                "description": "Committee Name",
                "mode": "nullable",
            },
            {
                "name": "tres_nm",
                "type": "string",
                "description": "Treasurer's Name",
                "mode": "nullable",
            },
            {
                "name": "cmte_st1",
                "type": "string",
                "description": "Street One",
                "mode": "nullable",
            },
            {
                "name": "cmte_st2",
                "type": "string",
                "description": "Street Two",
                "mode": "nullable",
            },
            {
                "name": "cmte_city",
                "type": "string",
                "description": "City or Town",
                "mode": "nullable",
            },
            {
                "name": "cmte_st",
                "type": "string",
                "description": "State",
                "mode": "nullable",
            },
            {
                "name": "cmte_zip",
                "type": "string",
                "description": "Zip Code",
                "mode": "nullable",
            },
            {
                "name": "cmte_dsgn",
                "type": "string",
                "description": "Committee Designation",
                "mode": "nullable",
            },
            {
                "name": "cmte_tp",
                "type": "string",
                "description": "Committee Type",
                "mode": "nullable",
            },
            {
                "name": "cmte_pty_affiliation",
                "type": "string",
                "description": "Committee Party",
                "mode": "nullable",
            },
            {
                "name": "cmte_filing_freq",
                "type": "string",
                "description": "Filing Frequency",
                "mode": "nullable",
            },
            {
                "name": "org_tp",
                "type": "string",
                "description": "Interest Group Category",
                "mode": "nullable",
            },
            {
                "name": "connected_org_nm",
                "type": "string",
                "description": "Connected Organization's Name",
                "mode": "nullable",
            },
            {
                "name": "cand_id",
                "type": "string",
                "description": "Candidate Identification",
                "mode": "nullable",
            },
        ],
    )

    committee_2016_transform_csv >> load_committee_2016_to_bq
