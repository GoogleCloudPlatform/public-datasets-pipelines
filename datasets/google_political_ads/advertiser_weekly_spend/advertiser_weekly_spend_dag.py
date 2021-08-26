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
    dag_id="google_political_ads.advertiser_weekly_spend",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    advertiser_weekly_spend_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="advertiser_weekly_spend_transform_csv",
        startup_timeout_seconds=600,
        name="advertiser_weekly_spend",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
            "SOURCE_FILE": "files/data.zip",
            "FILE_NAME": "google-political-ads-transparency-bundle/google-political-ads-advertiser-weekly-spend.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/advertiser_weekly_spend/data_output.csv",
            "PIPELINE_NAME": "advertiser_weekly_spend",
            "CSV_HEADERS": '["advertiser_id","advertiser_name","election_cycle","week_start_date","spend_usd","spend_eur","spend_inr","spend_bgn","spend_hrk","spend_czk","spend_dkk","spend_huf","spend_pln","spend_ron","spend_sek","spend_gbp","spend_nzd"]',
            "RENAME_MAPPINGS": '{"Advertiser_ID": "advertiser_id","Advertiser_Name": "advertiser_name","Election_Cycle": "election_cycle","Week_Start_Date": "week_start_date","Spend_USD": "spend_usd","Spend_EUR": "spend_eur","Spend_INR": "spend_inr","Spend_BGN": "spend_bgn","Spend_HRK": "spend_hrk","Spend_CZK": "spend_czk","Spend_DKK": "spend_dkk","Spend_HUF": "spend_huf","Spend_PLN": "spend_pln","Spend_RON": "spend_ron","Spend_SEK": "spend_sek","Spend_GBP": "spend_gbp","Spend_NZD": "spend_nzd"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_advertiser_weekly_spend_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_advertiser_weekly_spend_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/google_political_ads/advertiser_weekly_spend/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.advertiser_weekly_spend",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "advertiser_id",
                "type": "string",
                "description": "Unique ID for an advertiser verified to run election ads on Google Ads Services.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_name",
                "type": "string",
                "description": "Name of advertiser.",
                "mode": "nullable",
            },
            {
                "name": "election_cycle",
                "type": "string",
                "description": "[DEPRECATED] This field is deprecated in favor of the Elections column in advertiser_stats table. It will be deleted some time after July 2019.",
                "mode": "nullable",
            },
            {
                "name": "week_start_date",
                "type": "date",
                "description": "The start date for the week where spending occurred.",
                "mode": "nullable",
            },
            {
                "name": "spend_usd",
                "type": "integer",
                "description": "The amount in USD spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_eur",
                "type": "integer",
                "description": "The amount in EUR spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_inr",
                "type": "integer",
                "description": "The amount in INR spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_bgn",
                "type": "integer",
                "description": "The amount in BGN spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_hrk",
                "type": "integer",
                "description": "The amount in HRK spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_czk",
                "type": "integer",
                "description": "The amount in CZK spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_dkk",
                "type": "integer",
                "description": "The amount in DKK spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_huf",
                "type": "integer",
                "description": "The amount in HUF spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_pln",
                "type": "integer",
                "description": "The amount in PLN spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_ron",
                "type": "integer",
                "description": "The amount in RON spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_sek",
                "type": "integer",
                "description": "The amount in SEK spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_gbp",
                "type": "integer",
                "description": "The amount in GBP spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_nzd",
                "type": "integer",
                "description": "The amount in NZD spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
        ],
    )

    advertiser_weekly_spend_transform_csv >> load_advertiser_weekly_spend_to_bq
