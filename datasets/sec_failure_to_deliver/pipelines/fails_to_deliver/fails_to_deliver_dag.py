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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="sec_failure_to_deliver.fails_to_deliver",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        startup_timeout_seconds=600,
        name="fails_to_deliver",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.sec_failure_to_deliver.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://pdp-feeds-staging/FTD/",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/sec_failure_to_deliver/fails_to_deliver/data_output.csv",
            "CSV_HEADERS": '["settlement_date","cusip","symbol","total_shares","company_name","share_price"]',
        },
        resources={"limit_memory": "6G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/sec_failure_to_deliver/fails_to_deliver/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="sec_failure_to_deliver.fails_to_deliver",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "settlement_date",
                "type": "DATE",
                "description": "The date of settlement for the failure to deliver",
                "mode": "NULLABLE",
            },
            {
                "name": "cusip",
                "type": "STRING",
                "description": "Unique identification number assigned to stocks and registered bonds in the United States and Canada",
                "mode": "NULLABLE",
            },
            {
                "name": "symbol",
                "type": "STRING",
                "description": "Stock ticker symbol",
                "mode": "NULLABLE",
            },
            {
                "name": "total_shares",
                "type": "INTEGER",
                "description": "The total quantity of shares that were unable to be delivered. This represents the outstanding balance level",
                "mode": "NULLABLE",
            },
            {
                "name": "company_name",
                "type": "STRING",
                "description": "The name of the issuer",
                "mode": "NULLABLE",
            },
            {
                "name": "share_price",
                "type": "FLOAT",
                "description": "The closing price of the stock on the previous day",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
