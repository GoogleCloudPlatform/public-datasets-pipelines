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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery, gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="google_political_ads.process_csvs_and_load_to_bq",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 */3 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to archive the CSV file in the destination bucket
    download_zip_file_to_composer_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="download_zip_file_to_composer_bucket",
        source_bucket="political-csv",
        source_object="google-political-ads-transparency-bundle.zip",
        destination_bucket="{{ var.value.composer_bucket }}",
        destination_object="data/google_political_ads/google-political-ads-transparency-bundle.zip",
        impersonation_chain="{{ var.json.google_political_ads.service_account }}",
        move_object=False,
    )
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-google-political-ads",
            "initial_node_count": 2,
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

    # Run CSV transform within kubernetes pod
    transform_advertiser_declared_stats_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_advertiser_declared_stats_csv",
        startup_timeout_seconds=600,
        name="advertiser_declared_stats",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-advertiser-declared-stats.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/advertiser_declared_stats/data_output.csv",
            "TABLE_NAME": "advertiser_declared_stats",
            "CSV_HEADERS": '[\n  "advertiser_id",\n  "advertiser_declared_name",\n  "region",\n  "advertiser_declared_regulatory_id",\n  "advertiser_declared_scope",\n  "advertiser_declared_promoter_name",\n  "advertiser_declared_promoter_address"\n]',
            "RENAME_MAPPINGS": '{\n  "Advertiser_ID": "advertiser_id",\n  "Region": "region",\n  "Advertiser_Declared_Name": "advertiser_declared_name",\n  "Advertiser_Declared_Regulatory_ID": "advertiser_declared_regulatory_id",\n  "Advertiser_Declared_Scope": "advertiser_declared_scope",\n  "Advertiser_Declared_Promoter_Name": "advertiser_declared_promoter_name",\n  "Advertiser_Declared_Promoter_Address": "advertiser_declared_promoter_address"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_advertiser_declared_stats_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_advertiser_declared_stats_to_bq",
        bucket="{{ var.value.composer_bucket }}",
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
                "name": "region",
                "type": "string",
                "description": "Advertiser region.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_name",
                "type": "string",
                "description": "The advertiser's committee declared name.",
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
                "description": "The New Zealand advertiser's declared Promoter Statement name.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_declared_promoter_address",
                "type": "string",
                "description": "The New Zealand advertiser's declared Promoter Statement address.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_advertiser_geo_spend_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_advertiser_geo_spend_csv",
        startup_timeout_seconds=600,
        name="advertiser_geo_spend",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-advertiser-geo-spend.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/advertiser_geo_spend/data_output.csv",
            "TABLE_NAME": "advertiser_geo_spend",
            "CSV_HEADERS": '[\n  "advertiser_id",\n  "advertiser_name",\n  "country",\n  "country_subdivision_primary",\n  "spend_usd",\n  "spend_eur",\n  "spend_inr",\n  "spend_bgn",\n  "spend_hrk",\n  "spend_czk",\n  "spend_dkk",\n  "spend_huf",\n  "spend_pln",\n  "spend_ron",\n  "spend_sek",\n  "spend_gbp",\n  "spend_nzd",\n  "spend_ils",\n  "spend_aud",\n  "spend_twd",\n  "spend_brl",\n  "spend_ars",\n  "spend_zar",\n  "spend_clp"\n]',
            "RENAME_MAPPINGS": '{\n  "Advertiser_ID": "advertiser_id",\n  "Advertiser_Name": "advertiser_name",\n  "Country": "country",\n  "Country_Subdivision_Primary": "country_subdivision_primary",\n  "Spend_USD": "spend_usd",\n  "Spend_EUR": "spend_eur",\n  "Spend_INR": "spend_inr",\n  "Spend_BGN": "spend_bgn",\n  "Spend_HRK": "spend_hrk",\n  "Spend_CZK": "spend_czk",\n  "Spend_DKK": "spend_dkk",\n  "Spend_HUF": "spend_huf",\n  "Spend_PLN": "spend_pln",\n  "Spend_RON": "spend_ron",\n  "Spend_SEK": "spend_sek",\n  "Spend_GBP": "spend_gbp",\n  "Spend_NZD": "spend_nzd",\n  "Spend_ILS": "spend_ils",\n  "Spend_AUD": "spend_aud",\n  "Spend_TWD": "spend_twd",\n  "Spend_BRL": "spend_brl",\n  "Spend_ARS": "spend_ars",\n  "Spend_ZAR": "spend_zar",\n  "Spend_CLP": "spend_clp"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_advertiser_geo_spend_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_advertiser_geo_spend_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/google_political_ads/advertiser_geo_spend/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.advertiser_geo_spend",
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
                "description": "Name of the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "country",
                "type": "string",
                "description": 'The country where election ads were served specified in the ISO 3166-1 alpha-2 standard code. For example: "US" for United States.',
                "mode": "nullable",
            },
            {
                "name": "country_subdivision_primary",
                "type": "string",
                "description": 'The primary subdivision of the country where election ads were served specified by the ISO 3166-2 standard code. For example: "US-CA" for California state in United States',
                "mode": "nullable",
            },
            {
                "name": "spend_usd",
                "type": "integer",
                "description": "Total amount in USD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_eur",
                "type": "integer",
                "description": "Total amount in EUR spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_inr",
                "type": "integer",
                "description": "Total amount in INR spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_bgn",
                "type": "integer",
                "description": "Total amount in BGN spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_hrk",
                "type": "integer",
                "description": "Total amount in HRK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_czk",
                "type": "integer",
                "description": "Total amount in CZK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_dkk",
                "type": "integer",
                "description": "Total amount in DKK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_huf",
                "type": "integer",
                "description": "Total amount in HUF spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_pln",
                "type": "integer",
                "description": "Total amount in PLN spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_ron",
                "type": "integer",
                "description": "Total amount in RON spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_sek",
                "type": "integer",
                "description": "Total amount in SEK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_gbp",
                "type": "integer",
                "description": "Total amount in GBP spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_nzd",
                "type": "integer",
                "description": "Total amount in NZD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_ils",
                "type": "integer",
                "description": "Total amount in ILS spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_aud",
                "type": "integer",
                "description": "Total amount in AUD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_twd",
                "type": "integer",
                "description": "Total amount in TWD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_brl",
                "type": "integer",
                "description": "Total amount in BRL spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_ars",
                "type": "integer",
                "description": "Total amount in ARS spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_zar",
                "type": "integer",
                "description": "Total amount in ZAR spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_clp",
                "type": "integer",
                "description": "Total amount in CLP spent on election ads in this region.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_advertiser_stats_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_advertiser_stats_csv",
        startup_timeout_seconds=600,
        name="advertiser_stats",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-advertiser-stats.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/advertiser_stats/data_output.csv",
            "TABLE_NAME": "advertiser_stats",
            "CSV_HEADERS": '[\n  "advertiser_id",\n  "advertiser_name",\n  "public_ids_list",\n  "regions",\n  "elections",\n  "total_creatives",\n  "spend_usd",\n  "spend_eur",\n  "spend_inr",\n  "spend_bgn",\n  "spend_hrk",\n  "spend_czk",\n  "spend_dkk",\n  "spend_huf",\n  "spend_pln",\n  "spend_ron",\n  "spend_sek",\n  "spend_gbp",\n  "spend_nzd",\n  "spend_ils",\n  "spend_aud",\n  "spend_twd",\n  "spend_brl",\n  "spend_ars",\n  "spend_zar",\n  "spend_clp"\n]',
            "RENAME_MAPPINGS": '{\n  "Advertiser_ID": "advertiser_id",\n  "Advertiser_Name": "advertiser_name",\n  "Public_IDs_List": "public_ids_list",\n  "Regions": "regions",\n  "Elections": "elections",\n  "Total_Creatives": "total_creatives",\n  "Spend_USD": "spend_usd",\n  "Spend_EUR": "spend_eur",\n  "Spend_INR": "spend_inr",\n  "Spend_BGN": "spend_bgn",\n  "Spend_HRK": "spend_hrk",\n  "Spend_CZK": "spend_czk",\n  "Spend_DKK": "spend_dkk",\n  "Spend_HUF": "spend_huf",\n  "Spend_PLN": "spend_pln",\n  "Spend_RON": "spend_ron",\n  "Spend_SEK": "spend_sek",\n  "Spend_GBP": "spend_gbp",\n  "Spend_NZD": "spend_nzd",\n  "Spend_ILS": "spend_ils",\n  "Spend_AUD": "spend_aud",\n  "Spend_TWD": "spend_twd",\n  "Spend_BRL": "spend_brl",\n  "Spend_ARS": "spend_ars",\n  "Spend_ZAR": "spend_zar",\n  "Spend_CLP": "spend_clp"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_advertiser_stats_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_advertiser_stats_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/google_political_ads/advertiser_stats/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.advertiser_stats",
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
                "name": "public_ids_list",
                "type": "string",
                "description": "List of public IDs used to identify the advertiser if available.",
                "mode": "nullable",
            },
            {
                "name": "regions",
                "type": "string",
                "description": "The list of regions where the ads of this advertiser were served",
                "mode": "nullable",
            },
            {
                "name": "elections",
                "type": "string",
                "description": "The list of elections that this advertiser participated in based on the regions.",
                "mode": "nullable",
            },
            {
                "name": "total_creatives",
                "type": "integer",
                "description": "Total number of election ads the advertiser ran with at least one impression.",
                "mode": "nullable",
            },
            {
                "name": "spend_usd",
                "type": "integer",
                "description": "Total amount in USD spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_eur",
                "type": "integer",
                "description": "Total amount in EUR spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_inr",
                "type": "integer",
                "description": "Total amount in INR spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_bgn",
                "type": "integer",
                "description": "Total amount in BGN spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_hrk",
                "type": "integer",
                "description": "Total amount in HRK spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_czk",
                "type": "integer",
                "description": "Total amount in CZK spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_dkk",
                "type": "integer",
                "description": "Total amount in DKK spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_huf",
                "type": "integer",
                "description": "Total amount in HUF spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_pln",
                "type": "integer",
                "description": "Total amount in PLN spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_ron",
                "type": "integer",
                "description": "Total amount in RON spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_sek",
                "type": "integer",
                "description": "Total amount in SEK spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_gbp",
                "type": "integer",
                "description": "Total amount in GBP spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_nzd",
                "type": "integer",
                "description": "Total amount in NZD spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_ils",
                "type": "integer",
                "description": "Total amount in ILS spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_aud",
                "type": "integer",
                "description": "Total amount in AUD spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_twd",
                "type": "integer",
                "description": "Total amount in TWD spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_brl",
                "type": "integer",
                "description": "Total amount in BRL spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_ars",
                "type": "integer",
                "description": "Total amount in ARS spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_zar",
                "type": "integer",
                "description": "Total amount in ZAR spent on election ads by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_clp",
                "type": "integer",
                "description": "Total amount in CLP spent on election ads by the advertiser.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_advertiser_weekly_spend_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_advertiser_weekly_spend_csv",
        startup_timeout_seconds=600,
        name="advertiser_weekly_spend",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-advertiser-weekly-spend.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/advertiser_weekly_spend/data_output.csv",
            "TABLE_NAME": "advertiser_weekly_spend",
            "CSV_HEADERS": '[\n  "advertiser_id",\n  "advertiser_name",\n  "election_cycle",\n  "week_start_date",\n  "spend_usd",\n  "spend_eur",\n  "spend_inr",\n  "spend_bgn",\n  "spend_hrk",\n  "spend_czk",\n  "spend_dkk",\n  "spend_huf",\n  "spend_pln",\n  "spend_ron",\n  "spend_sek",\n  "spend_gbp",\n  "spend_nzd",\n  "spend_ils",\n  "spend_aud",\n  "spend_twd",\n  "spend_brl",\n  "spend_ars",\n  "spend_zar",\n  "spend_clp"\n]',
            "RENAME_MAPPINGS": '{\n  "Advertiser_ID": "advertiser_id",\n  "Advertiser_Name": "advertiser_name",\n  "Election_Cycle": "election_cycle",\n  "Week_Start_Date": "week_start_date",\n  "Spend_USD": "spend_usd",\n  "Spend_EUR": "spend_eur",\n  "Spend_INR": "spend_inr",\n  "Spend_BGN": "spend_bgn",\n  "Spend_HRK": "spend_hrk",\n  "Spend_CZK": "spend_czk",\n  "Spend_DKK": "spend_dkk",\n  "Spend_HUF": "spend_huf",\n  "Spend_PLN": "spend_pln",\n  "Spend_RON": "spend_ron",\n  "Spend_SEK": "spend_sek",\n  "Spend_GBP": "spend_gbp",\n  "Spend_NZD": "spend_nzd",\n  "Spend_ILS": "spend_ils",\n  "Spend_AUD": "spend_aud",\n  "Spend_TWD": "spend_twd",\n  "Spend_BRL": "spend_brl",\n  "Spend_ARS": "spend_ars",\n  "Spend_ZAR": "spend_zar",\n  "Spend_CLP": "spend_clp"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_advertiser_weekly_spend_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_advertiser_weekly_spend_to_bq",
        bucket="{{ var.value.composer_bucket }}",
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
            {
                "name": "spend_ils",
                "type": "integer",
                "description": "The amount in ILS spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_aud",
                "type": "integer",
                "description": "The amount in AUD spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_twd",
                "type": "integer",
                "description": "The amount in TWD spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_brl",
                "type": "integer",
                "description": "The amount in BRL spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_ars",
                "type": "integer",
                "description": "The amount in ARS spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_zar",
                "type": "integer",
                "description": "The amount in ZAR spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
            {
                "name": "spend_clp",
                "type": "integer",
                "description": "The amount in CLP spent on election ads during the given week by the advertiser.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_campaign_targeting_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_campaign_targeting_csv",
        startup_timeout_seconds=600,
        name="campaign_targeting",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-campaign-targeting.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/campaign_targeting/data_output.csv",
            "TABLE_NAME": "campaign_targeting",
            "CSV_HEADERS": '[\n  "campaign_id",\n  "age_targeting",\n  "gender_targeting",\n  "geo_targeting_included",\n  "geo_targeting_excluded",\n  "start_date",\n  "end_date",\n  "ads_list",\n  "advertiser_id",\n  "advertiser_name"\n]',
            "RENAME_MAPPINGS": '{\n  "Campaign_ID": "campaign_id",\n  "Age_Targeting": "age_targeting",\n  "Gender_Targeting": "gender_targeting",\n  "Geo_Targeting_Included": "geo_targeting_included",\n  "Geo_Targeting_Excluded": "geo_targeting_excluded",\n  "Start_Date": "start_date",\n  "End_Date": "end_date",\n  "Ads_List": "ads_list",\n  "Advertiser_ID": "advertiser_id",\n  "Advertiser_Name": "advertiser_name"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_campaign_targeting_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_campaign_targeting_to_bq",
        bucket="{{ var.value.composer_bucket }}",
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

    # Run CSV transform within kubernetes pod
    transform_creative_stats_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_creative_stats_csv",
        startup_timeout_seconds=600,
        name="creative_stats",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-creative-stats.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/creative_stats/data_output.csv",
            "TABLE_NAME": "creative_stats",
            "CSV_HEADERS": '[\n  "ad_id",\n  "ad_url",\n  "ad_type",\n  "regions",\n  "advertiser_id",\n  "advertiser_name",\n  "ad_campaigns_list",\n  "date_range_start",\n  "date_range_end",\n  "num_of_days",\n  "impressions",\n  "spend_usd",\n  "first_served_timestamp",\n  "last_served_timestamp",\n  "age_targeting",\n  "gender_targeting",\n  "geo_targeting_included",\n  "geo_targeting_excluded",\n  "spend_range_min_usd",\n  "spend_range_max_usd",\n  "spend_range_min_eur",\n  "spend_range_max_eur",\n  "spend_range_min_inr",\n  "spend_range_max_inr",\n  "spend_range_min_bgn",\n  "spend_range_max_bgn",\n  "spend_range_min_hrk",\n  "spend_range_max_hrk",\n  "spend_range_min_czk",\n  "spend_range_max_czk",\n  "spend_range_min_dkk",\n  "spend_range_max_dkk",\n  "spend_range_min_huf",\n  "spend_range_max_huf",\n  "spend_range_min_pln",\n  "spend_range_max_pln",\n  "spend_range_min_ron",\n  "spend_range_max_ron",\n  "spend_range_min_sek",\n  "spend_range_max_sek",\n  "spend_range_min_gbp",\n  "spend_range_max_gbp",\n  "spend_range_min_nzd",\n  "spend_range_max_nzd",\n  "spend_range_min_ils",\n  "spend_range_max_ils",\n  "spend_range_min_aud",\n  "spend_range_max_aud",\n  "spend_range_min_twd",\n  "spend_range_max_twd",\n  "spend_range_min_brl",\n  "spend_range_max_brl",\n  "spend_range_min_ars",\n  "spend_range_max_ars",\n  "spend_range_min_zar",\n  "spend_range_max_zar",\n  "spend_range_min_clp",\n  "spend_range_max_clp",\n  "spend_range_min_mxn",\n  "spend_range_max_mxn",\n  "is_funded_by_google_ad_grants"\n]',
            "RENAME_MAPPINGS": '{\n  "Ad_ID": "ad_id",\n  "Ad_URL": "ad_url",\n  "Ad_Type": "ad_type",\n  "Regions": "regions",\n  "Advertiser_ID": "advertiser_id",\n  "Advertiser_Name": "advertiser_name",\n  "Ad_Campaigns_List": "ad_campaigns_list",\n  "Date_Range_Start": "date_range_start",\n  "Date_Range_End": "date_range_end",\n  "Num_of_Days": "num_of_days",\n  "Impressions": "impressions",\n  "Spend_USD": "spend_usd",\n  "Spend_Range_Min_USD": "spend_range_min_usd",\n  "Spend_Range_Max_USD": "spend_range_max_usd",\n  "Spend_Range_Min_EUR": "spend_range_min_eur",\n  "Spend_Range_Max_EUR": "spend_range_max_eur",\n  "Spend_Range_Min_INR": "spend_range_min_inr",\n  "Spend_Range_Max_INR": "spend_range_max_inr",\n  "Spend_Range_Min_BGN": "spend_range_min_bgn",\n  "Spend_Range_Max_BGN": "spend_range_max_bgn",\n  "Spend_Range_Min_HRK": "spend_range_min_hrk",\n  "Spend_Range_Max_HRK": "spend_range_max_hrk",\n  "Spend_Range_Min_CZK": "spend_range_min_czk",\n  "Spend_Range_Max_CZK": "spend_range_max_czk",\n  "Spend_Range_Min_DKK": "spend_range_min_dkk",\n  "Spend_Range_Max_DKK": "spend_range_max_dkk",\n  "Spend_Range_Min_HUF": "spend_range_min_huf",\n  "Spend_Range_Max_HUF": "spend_range_max_huf",\n  "Spend_Range_Min_PLN": "spend_range_min_pln",\n  "Spend_Range_Max_PLN": "spend_range_max_pln",\n  "Spend_Range_Min_RON": "spend_range_min_ron",\n  "Spend_Range_Max_RON": "spend_range_max_ron",\n  "Spend_Range_Min_SEK": "spend_range_min_sek",\n  "Spend_Range_Max_SEK": "spend_range_max_sek",\n  "Spend_Range_Min_GBP": "spend_range_min_gbp",\n  "Spend_Range_Max_GBP": "spend_range_max_gbp",\n  "Spend_Range_Min_NZD": "spend_range_min_nzd",\n  "Spend_Range_Max_NZD": "spend_range_max_nzd",\n  "Spend_Range_Min_ILS": "spend_range_min_ils",\n  "Spend_Range_Max_ILS": "spend_range_max_ils",\n  "Spend_Range_Min_AUD": "spend_range_min_aud",\n  "Spend_Range_Max_AUD": "spend_range_max_aud",\n  "Spend_Range_Min_TWD": "spend_range_min_twd",\n  "Spend_Range_Max_TWD": "spend_range_max_twd",\n  "Spend_Range_Min_BRL": "spend_range_min_brl",\n  "Spend_Range_Max_BRL": "spend_range_max_brl",\n  "Spend_Range_Min_ARS": "spend_range_min_ars",\n  "Spend_Range_Max_ARS": "spend_range_max_ars",\n  "Spend_Range_Min_ZAR": "spend_range_min_zar",\n  "Spend_Range_Max_ZAR": "spend_range_max_zar",\n  "Spend_Range_Min_CLP": "spend_range_min_clp",\n  "Spend_Range_Max_CLP": "spend_range_max_clp",\n  "Age_Targeting": "age_targeting",\n  "Gender_Targeting": "gender_targeting",\n  "Geo_Targeting_Included": "geo_targeting_included",\n  "Geo_Targeting_Excluded": "geo_targeting_excluded",\n  "First_Served_Timestamp": "first_served_timestamp",\n  "Last_Served_Timestamp": "last_served_timestamp",\n  "Spend_Range_Min_MXN": "spend_range_min_mxn",\n  "Spend_Range_Max_MXN": "spend_range_max_mxn",\n  "Is_Funded_By_Google_Ad_Grants": "is_funded_by_google_ad_grants"\n}',
        },
        container_resources={
            "memory": {"request": "16G"},
            "cpu": {"request": "2"},
            "ephemeral-storage": {"request": "10G"},
        },
    )

    # Task to load CSV data to a BigQuery table
    load_creative_stats_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_creative_stats_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/google_political_ads/creative_stats/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.creative_stats",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "ad_id",
                "type": "string",
                "description": "Unique id for a specific election ad.",
                "mode": "nullable",
            },
            {
                "name": "ad_url",
                "type": "string",
                "description": "URL to view the election ad in the election Advertising on Google report.",
                "mode": "nullable",
            },
            {
                "name": "ad_type",
                "type": "string",
                "description": "The type of the ad. Can be TEXT VIDEO or IMAGE.",
                "mode": "nullable",
            },
            {
                "name": "regions",
                "type": "string",
                "description": "The regions that this ad is verified for or were served in.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_id",
                "type": "string",
                "description": "ID of the advertiser who purchased the ad.",
                "mode": "nullable",
            },
            {
                "name": "advertiser_name",
                "type": "string",
                "description": "Name of advertiser.",
                "mode": "nullable",
            },
            {
                "name": "ad_campaigns_list",
                "type": "string",
                "description": "IDs of all election ad campaigns that included the ad.",
                "mode": "nullable",
            },
            {
                "name": "date_range_start",
                "type": "date",
                "description": "First day a election ad ran and had an impression.",
                "mode": "nullable",
            },
            {
                "name": "date_range_end",
                "type": "date",
                "description": "Most recent day a election ad ran and had an impression.",
                "mode": "nullable",
            },
            {
                "name": "num_of_days",
                "type": "integer",
                "description": "Total number of days a election ad ran and had an impression.",
                "mode": "nullable",
            },
            {
                "name": "impressions",
                "type": "string",
                "description": "Number of impressions for the election ad. Impressions are grouped into several buckets ≤ 10k 10k-100k 100k-1M 1M-10M > 10M.",
                "mode": "nullable",
            },
            {
                "name": "spend_usd",
                "type": "string",
                "description": "[DEPRECATED] This field is deprecated in favor of specifying the lower and higher spend bucket bounds in separate Spend_Range_Min and Spend_Range_Max columns.",
                "mode": "nullable",
            },
            {
                "name": "first_served_timestamp",
                "type": "timestamp",
                "description": "The timestamp of the earliest impression for this ad.",
                "mode": "nullable",
            },
            {
                "name": "last_served_timestamp",
                "type": "timestamp",
                "description": "The timestamp of the most recent impression for this ad.",
                "mode": "nullable",
            },
            {
                "name": "age_targeting",
                "type": "string",
                "description": "Age ranges included in the ad's targeting",
                "mode": "nullable",
            },
            {
                "name": "gender_targeting",
                "type": "string",
                "description": "Genders included in the ad's targeting.",
                "mode": "nullable",
            },
            {
                "name": "geo_targeting_included",
                "type": "string",
                "description": "Geographic locations included in the ad's targeting.",
                "mode": "nullable",
            },
            {
                "name": "geo_targeting_excluded",
                "type": "string",
                "description": "Geographic locations excluded in the ad's targeting.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_usd",
                "type": "integer",
                "description": "Lower bound of the amount in USD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_usd",
                "type": "integer",
                "description": "Upper bound of the amount in USD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_eur",
                "type": "integer",
                "description": "Lower bound of the amount in EUR spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_eur",
                "type": "integer",
                "description": "Upper bound of the amount in EUR spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_inr",
                "type": "integer",
                "description": "Lower bound of the amount in INR spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_inr",
                "type": "integer",
                "description": "Upper bound of the amount in INR spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_bgn",
                "type": "integer",
                "description": "Lower bound of the amount in BGN spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_bgn",
                "type": "integer",
                "description": "Upper bound of the amount in BGN spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_czk",
                "type": "integer",
                "description": "Lower bound of the amount in CZK spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_czk",
                "type": "integer",
                "description": "Upper bound of the amount in CZK spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_dkk",
                "type": "integer",
                "description": "Lower bound of the amount in DKK spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_dkk",
                "type": "integer",
                "description": "Upper bound of the amount in DKK spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_huf",
                "type": "integer",
                "description": "Lower bound of the amount in HUF spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_huf",
                "type": "integer",
                "description": "Upper bound of the amount in HUF spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_pln",
                "type": "integer",
                "description": "Lower bound of the amount in PLN spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_pln",
                "type": "integer",
                "description": "Upper bound of the amount in PLN spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_ron",
                "type": "integer",
                "description": "Lower bound of the amount in RON spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_ron",
                "type": "integer",
                "description": "Upper bound of the amount in RON spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_sek",
                "type": "integer",
                "description": "Lower bound of the amount in SEK spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_sek",
                "type": "integer",
                "description": "Upper bound of the amount in SEK spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_gbp",
                "type": "integer",
                "description": "Lower bound of the amount in GBP spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_gbp",
                "type": "integer",
                "description": "Upper bound of the amount in GBP spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_nzd",
                "type": "integer",
                "description": "Lower bound of the amount in NZD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_nzd",
                "type": "integer",
                "description": "Upper bound of the amount in NZD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_ils",
                "type": "integer",
                "description": "Lower bound of the amount in ILS spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_ils",
                "type": "integer",
                "description": "Upper bound of the amount in ILS spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_aud",
                "type": "integer",
                "description": "Lower bound of the amount in AUD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_aud",
                "type": "integer",
                "description": "Upper bound of the amount in AUD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_twd",
                "type": "integer",
                "description": "Lower bound of the amount in TWD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_twd",
                "type": "integer",
                "description": "Upper bound of the amount in TWD spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_brl",
                "type": "integer",
                "description": "Lower bound of the amount in BRL spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_brl",
                "type": "integer",
                "description": "Upper bound of the amount in BRL spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_ars",
                "type": "integer",
                "description": "Lower bound of the amount in ARS spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_ars",
                "type": "integer",
                "description": "Upper bound of the amount in ARS spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_zar",
                "type": "integer",
                "description": "Lower bound of the amount in ZAR spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_zar",
                "type": "integer",
                "description": "Upper bound of the amount in ZAR spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_clp",
                "type": "integer",
                "description": "Lower bound of the amount in CLP spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_clp",
                "type": "integer",
                "description": "Upper bound of the amount in CLP spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_min_mxn",
                "type": "integer",
                "description": "Lower bound of the amount in MXN spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "spend_range_max_mxn",
                "type": "integer",
                "description": "Upper bound of the amount in MXN spent by the advertiser on the election ad.",
                "mode": "nullable",
            },
            {
                "name": "is_funded_by_google_ad_grants",
                "type": "integer",
                "description": "Indicates whether the ad is funded by an in-kind donation through Google Ad Grants. Google ad Grants donates Search advertising to eligible organizations. Google does not endorse these ad.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_geo_spend_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_geo_spend_csv",
        startup_timeout_seconds=600,
        name="geo_spend",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-geo-spend.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/geo_spend/data_output.csv",
            "TABLE_NAME": "geo_spend",
            "CSV_HEADERS": '[\n  "country",\n  "country_subdivision_primary",\n  "country_subdivision_secondary",\n  "spend_usd",\n  "spend_eur",\n  "spend_inr",\n  "spend_bgn",\n  "spend_hrk",\n  "spend_czk",\n  "spend_dkk",\n  "spend_huf",\n  "spend_pln",\n  "spend_ron",\n  "spend_sek",\n  "spend_gbp",\n  "spend_nzd",\n  "spend_ils",\n  "spend_aud",\n  "spend_twd",\n  "spend_brl",\n  "spend_ars",\n  "spend_zar",\n  "spend_clp"\n]',
            "RENAME_MAPPINGS": '{\n  "Country": "country",\n  "Country_Subdivision_Primary": "country_subdivision_primary",\n  "Country_Subdivision_Secondary": "country_subdivision_secondary",\n  "Spend_USD": "spend_usd",\n  "Spend_EUR": "spend_eur",\n  "Spend_INR": "spend_inr",\n  "Spend_BGN": "spend_bgn",\n  "Spend_HRK": "spend_hrk",\n  "Spend_CZK": "spend_czk",\n  "Spend_DKK": "spend_dkk",\n  "Spend_HUF": "spend_huf",\n  "Spend_PLN": "spend_pln",\n  "Spend_RON": "spend_ron",\n  "Spend_SEK": "spend_sek",\n  "Spend_GBP": "spend_gbp",\n  "Spend_NZD": "spend_nzd",\n  "Spend_ILS": "spend_ils",\n  "Spend_AUD": "spend_aud",\n  "Spend_TWD": "spend_twd",\n  "Spend_BRL": "spend_brl",\n  "Spend_ARS": "spend_ars",\n  "Spend_ZAR": "spend_zar",\n  "Spend_CLP": "spend_clp"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_geo_spend_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_geo_spend_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/google_political_ads/geo_spend/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.geo_spend",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "country",
                "type": "string",
                "description": 'The country where election ads were served specified in the ISO 3166-1 alpha-2 standard code. For example "US" for United States.',
                "mode": "nullable",
            },
            {
                "name": "country_subdivision_primary",
                "type": "string",
                "description": 'The primary subdivision of the country where election ads were served specified by the ISO 3166-2 standard code. For example "US-CA" for California state in United States',
                "mode": "nullable",
            },
            {
                "name": "country_subdivision_secondary",
                "type": "string",
                "description": "The name of the secondary subdivision. For example The name of a US congressional district.",
                "mode": "nullable",
            },
            {
                "name": "spend_usd",
                "type": "integer",
                "description": "Total amount in USD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_eur",
                "type": "integer",
                "description": "Total amount in EUR spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_inr",
                "type": "integer",
                "description": "Total amount in INR spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_bgn",
                "type": "integer",
                "description": "Total amount in BGN spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_hrk",
                "type": "integer",
                "description": "Total amount in HRK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_czk",
                "type": "integer",
                "description": "Total amount in CZK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_dkk",
                "type": "integer",
                "description": "Total amount in DKK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_huf",
                "type": "integer",
                "description": "Total amount in HUF spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_pln",
                "type": "integer",
                "description": "Total amount in PLN spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_ron",
                "type": "integer",
                "description": "Total amount in RON spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_sek",
                "type": "integer",
                "description": "Total amount in SEK spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_gbp",
                "type": "integer",
                "description": "Total amount in GBP spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_nzd",
                "type": "integer",
                "description": "Total amount in NZD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_ils",
                "type": "integer",
                "description": "Total amount in ILS spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_aud",
                "type": "integer",
                "description": "Total amount in AUD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_twd",
                "type": "integer",
                "description": "Total amount in TWD spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_brl",
                "type": "integer",
                "description": "Total amount in BRL spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_ars",
                "type": "integer",
                "description": "Total amount in ARS spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_zar",
                "type": "integer",
                "description": "Total amount in ZAR spent on election ads in this region.",
                "mode": "nullable",
            },
            {
                "name": "spend_clp",
                "type": "integer",
                "description": "Total amount in CLP spent on election ads in this region.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_last_updated_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_last_updated_csv",
        startup_timeout_seconds=600,
        name="last_updated",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-updated.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/last_updated/data_output.csv",
            "TABLE_NAME": "last_updated",
            "CSV_HEADERS": '["report_data_updated_time"]',
            "RENAME_MAPPINGS": '{"Report_Data_Updated_Time (PT)": "report_data_updated_time"}',
        },
        container_resources={"memory": {"request": "128M"}, "cpu": {"request": "200m"}},
    )

    # Task to load CSV data to a BigQuery table
    load_last_updated_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_last_updated_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/google_political_ads/last_updated/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.last_updated",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "report_data_updated_time",
                "type": "datetime",
                "description": "The time the report data was most recently updated",
                "mode": "nullable",
            }
        ],
    )

    # Run CSV transform within kubernetes pod
    transform_top_keywords_history_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_top_keywords_history_csv",
        startup_timeout_seconds=600,
        name="top_keywords_history",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-google-political-ads",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/google_political_ads/google-political-ads-transparency-bundle.zip",
            "ZIP_FILE": "files/google-political-ads-transparency-bundle.zip",
            "CSV_FILE": "google-political-ads-top-keywords-history.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/top_keywords_history/data_output.csv",
            "TABLE_NAME": "top_keywords_history",
            "CSV_HEADERS": '[\n  "election_cycle",\n  "report_date",\n  "keyword_1",\n  "spend_usd_1",\n  "keyword_2",\n  "spend_usd_2",\n  "keyword_3",\n  "spend_usd_3",\n  "keyword_4",\n  "spend_usd_4",\n  "keyword_5",\n  "spend_usd_5",\n  "keyword_6",\n  "spend_usd_6",\n  "region",\n  "elections"\n]',
            "RENAME_MAPPINGS": '{\n  "Election_Cycle": "election_cycle",\n  "Report_Date": "report_date",\n  "Keyword_1": "keyword_1",\n  "Spend_USD_1": "spend_usd_1",\n  "Keyword_2": "keyword_2",\n  "Spend_USD_2": "spend_usd_2",\n  "Keyword_3": "keyword_3",\n  "Spend_USD_3": "spend_usd_3",\n  "Keyword_4": "keyword_4",\n  "Spend_USD_4": "spend_usd_4",\n  "Keyword_5": "keyword_5",\n  "Spend_USD_5": "spend_usd_5",\n  "Keyword_6": "keyword_6",\n  "Spend_USD_6": "spend_usd_6",\n  "Region": "region",\n  "Elections": "elections"\n}',
        },
        container_resources={"memory": {"request": "1G"}, "cpu": {"request": "200m"}},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-google-political-ads",
    )

    # Task to load CSV data to a BigQuery table
    load_top_keywords_history_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_top_keywords_history_to_bq",
        bucket="{{ var.value.composer_bucket }}",
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

    download_zip_file_to_composer_bucket >> create_cluster
    (
        create_cluster
        >> [
            transform_advertiser_declared_stats_csv,
            transform_advertiser_geo_spend_csv,
            transform_advertiser_stats_csv,
            transform_advertiser_weekly_spend_csv,
            transform_campaign_targeting_csv,
            transform_creative_stats_csv,
            transform_geo_spend_csv,
            transform_last_updated_csv,
            transform_top_keywords_history_csv,
        ]
        >> delete_cluster
    )
    delete_cluster >> [
        load_advertiser_declared_stats_to_bq,
        load_advertiser_geo_spend_to_bq,
        load_advertiser_stats_to_bq,
        load_advertiser_weekly_spend_to_bq,
        load_campaign_targeting_to_bq,
        load_creative_stats_to_bq,
        load_geo_spend_to_bq,
        load_last_updated_to_bq,
        load_top_keywords_history_to_bq,
    ]
