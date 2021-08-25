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
    dag_id="google_political_ads.campaign_targeting",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    campaign_targeting_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="campaign_targeting_transform_csv",
        startup_timeout_seconds=600,
        name="campaign_targeting",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
            "SOURCE_FILE": "files/data.zip",
            "FILE_NAME": "google-political-ads-transparency-bundle/google-political-ads-campaign-targeting.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/campaign_targeting/data_output.csv",
            "PIPELINE_NAME": "campaign_targeting",
            "CSV_HEADERS": '["campaign_id","age_targeting","gender_targeting","geo_targeting_included","geo_targeting_excluded","start_date","end_date","ads_list","advertiser_id","advertiser_name"]',
            "RENAME_MAPPINGS": '{"Campaign_ID": "campaign_id","Age_Targeting": "age_targeting","Gender_Targeting": "gender_targeting","Geo_Targeting_Included": "geo_targeting_included","Geo_Targeting_Excluded": "geo_targeting_excluded","Start_Date": "start_date","End_Date": "end_date","Ads_List": "ads_list","Advertiser_ID": "advertiser_id","Advertiser_Name": "advertiser_name"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_campaign_targeting_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_campaign_targeting_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/google_political_ads/campaign_targeting/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.campaign_targeting",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "campaign_id",
                "type": "string",
                "description": "[DEPRECATED] Unique ID for a political ad campaign.",
                "mode": "nullable",
            },
            {
                "name": "age_targeting",
                "type": "string",
                "description": "[DEPRECATED] Age ranges included in the campaign's targeting.",
                "mode": "nullable",
            },
            {
                "name": "gender_targeting",
                "type": "string",
                "description": "[DEPRECATED] Genders included in the campaign's targeting",
                "mode": "nullable",
            },
            {
                "name": "geo_targeting_included",
                "type": "string",
                "description": "[DEPRECATED] Geographic locations included in the campaign's targeting.",
                "mode": "nullable",
            },
            {
                "name": "geo_targeting_excluded",
                "type": "string",
                "description": "[DEPRECATED] Geographic locations excluded from the campaign's targeting.",
                "mode": "nullable",
            },
            {
                "name": "start_date",
                "type": "date",
                "description": "[DEPRECATED] Start date for the campaign.",
                "mode": "nullable",
            },
            {
                "name": "end_date",
                "type": "date",
                "description": "[DEPRECATED] End date for the campaign.",
                "mode": "nullable",
            },
            {
                "name": "ads_list",
                "type": "string",
                "description": "[DEPRECATED] List of Ad_IDs for the campaign.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_id",
                "type": "string",
                "description": "[DEPRECATED] ID of the advertiser who purchased the ad.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_name",
                "type": "string",
                "description": "[DEPRECATED] Name of advertiser.",
                "mode": "nullable",
            },
        ],
    )

    campaign_targeting_transform_csv >> load_campaign_targeting_to_bq
