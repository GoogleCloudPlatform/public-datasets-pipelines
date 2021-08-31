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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="google_political_ads.top_keywords_history",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    top_keywords_history_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="top_keywords_history_transform_csv",
        startup_timeout_seconds=600,
        name="top_keywords_history",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
            "SOURCE_FILE": "files/data.zip",
            "FILE_NAME": "google-political-ads-transparency-bundle/google-political-ads-top-keywords-history.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/top_keywords_history/data_output.csv",
            "PIPELINE_NAME": "top_keywords_history",
            "CSV_HEADERS": '["election_cycle","report_date","keyword_1","spend_usd_1","keyword_2","spend_usd_2","keyword_3","spend_usd_3","keyword_4","spend_usd_4","keyword_5","spend_usd_5","keyword_6","spend_usd_6","region","elections"]',
            "RENAME_MAPPINGS": '{"Election_Cycle": "election_cycle","Report_Date": "report_date","Keyword_1": "keyword_1","Spend_USD_1": "spend_usd_1","Keyword_2": "keyword_2","Spend_USD_2": "spend_usd_2","Keyword_3": "keyword_3","Spend_USD_3": "spend_usd_3","Keyword_4": "keyword_4","Spend_USD_4": "spend_usd_4","Keyword_5": "keyword_5","Spend_USD_5": "spend_usd_5","Keyword_6": "keyword_6","Spend_USD_6": "spend_usd_6","Region": "region","Elections": "elections"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_top_keywords_history_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_top_keywords_history_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/google_political_ads/top_keywords_history/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.top_keywords_history",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "election_cycle",
                "type": "string",
                "description": "[DEPRECATED] This field is deprecated in favor of the Region and Elections field. It will be deleted some time after July 2019.",
                "mode": "nullable",
            },
            {
                "name": "report_date",
                "type": "date",
                "description": "[DEPRECATED] The start date for the week where the spending was reported.",
                "mode": "nullable",
            },
            {
                "name": "keyword_1",
                "type": "string",
                "description": " [DEPRECATED] Keyword with the most spend by advertisers for political ads",
                "mode": "nullable",
            },
            {
                "name": "spend_usd_1",
                "type": "integer",
                "description": "[DEPRECATED] Total spend in USD for Keyword_1.",
                "mode": "nullable",
            },
            {
                "name": "keyword_2",
                "type": "string",
                "description": "[DEPRECATED] Keyword with the next most spend by advertisers for political ads",
                "mode": "nullable",
            },
            {
                "name": "spend_usd_2",
                "type": "integer",
                "description": "[DEPRECATED] Total spend in USD for Keyword_2.",
                "mode": "nullable",
            },
            {
                "name": "keyword_3",
                "type": "string",
                "description": "[DEPRECATED] Keyword with the next most spend by advertisers for political ads",
                "mode": "nullable",
            },
            {
                "name": "spend_usd_3",
                "type": "integer",
                "description": "[DEPRECATED] Total spend in USD for Keyword_3.",
                "mode": "nullable",
            },
            {
                "name": "keyword_4",
                "type": "string",
                "description": "[DEPRECATED] Keyword with the next most spend by advertisers for political ads",
                "mode": "nullable",
            },
            {
                "name": "spend_usd_4",
                "type": "integer",
                "description": "[DEPRECATED] Total spend in USD for Keyword_4.",
                "mode": "nullable",
            },
            {
                "name": "keyword_5",
                "type": "string",
                "description": "[DEPRECATED] Keyword with the next most spend by advertisers for political ads",
                "mode": "nullable",
            },
            {
                "name": "spend_usd_5",
                "type": "integer",
                "description": "[DEPRECATED] Total spend in USD for Keyword_5.",
                "mode": "nullable",
            },
            {
                "name": "keyword_6",
                "type": "string",
                "description": "[DEPRECATED] Keyword with the next most spend by advertisers for political ads",
                "mode": "nullable",
            },
            {
                "name": "spend_usd_6",
                "type": "integer",
                "description": "[DEPRECATED] Total spend in USD for Keyword_6.",
                "mode": "nullable",
            },
            {
                "name": "region",
                "type": "string",
                "description": "[DEPRECATED] The region where advertisers used these keywords.",
                "mode": "nullable",
            },
            {
                "name": "elections",
                "type": "string",
                "description": "[DEPRECATED] The elections during which these keywords were used.",
                "mode": "nullable",
            },
        ],
    )

    top_keywords_history_transform_csv >> load_top_keywords_history_to_bq
