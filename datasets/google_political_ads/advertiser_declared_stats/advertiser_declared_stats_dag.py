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
    dag_id="google_political_ads.advertiser_declared_stats",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    advertiser_declared_stats_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="advertiser_declared_stats_transform_csv",
        startup_timeout_seconds=600,
        name="advertiser_declared_stats",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
            "SOURCE_FILE": "files/data.zip",
            "FILE_NAME": "google-political-ads-transparency-bundle/*advertiser-declared-stats*",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/advertiser_declared_stats/data_output.csv",
            "PIPELINE_NAME": "advertiser_declared_stats",
            "CSV_HEADERS": '["advertiser_id","advertiser_declared_name","advertiser_declared_regulatory_id","advertiser_declared_scope","advertiser_declared_promoter_name","advertiser_declared_promoter_address"]',
            "RENAME_MAPPINGS": '{"Advertiser_ID" : "advertiser_id","Advertiser_Declared_Name" : "advertiser_declared_name","Advertiser_Declared_Regulatory_ID" : "advertiser_declared_regulatory_id","Advertiser_Declared_Scope" : "advertiser_declared_scope","Advertiser_Declared_Promoter_Name" : "advertiser_declared_promoter_name","Advertiser_Declared_Promoter_Address" : "advertiser_declared_promoter_address"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_advertiser_declared_stats_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_advertiser_declared_stats_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/google_political_ads/advertiser_declared_stats/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.advertiser_declared_stats",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "advertiser_id",
                "type": "string",
                "description": "ID of the advertiser who purchased the ad.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_name",
                "type": "string",
                "description": "The advertiser’s committee declared name.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_regulatory_id",
                "type": "string",
                "description": "Committee declared identification number.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_scope",
                "type": "string",
                "description": "Committee-provided information about the candidate and office or ballot proposition and jurisdiction to which the advertisement refers which is separate from our verification process.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_promoter_name",
                "type": "string",
                "description": "The New Zealand advertiser’s declared Promoter Statement name.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_promoter_address",
                "type": "string",
                "description": "The New Zealand advertiser’s declared Promoter Statement address.",
                "mode": "nullable",
            },
        ],
    )

    advertiser_declared_stats_transform_csv >> load_advertiser_declared_stats_to_bq
