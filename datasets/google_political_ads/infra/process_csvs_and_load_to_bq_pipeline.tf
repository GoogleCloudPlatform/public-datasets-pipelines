/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


resource "google_bigquery_table" "google_political_ads_advertiser_declared_stats" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "advertiser_declared_stats"
  description = "Certain California and New Zealand advertisers are required to submit additional data about themselves. The advertiser is responsible for the accuracy of this information, which Google has not confirmed. For California, this information is provided from our express notification process required for certain California advertisers, which is separate from our verification process. For New Zealand, this information is provided during our verification process."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_advertiser_declared_stats-table_id" {
  value = google_bigquery_table.google_political_ads_advertiser_declared_stats.table_id
}

output "bigquery_table-google_political_ads_advertiser_declared_stats-id" {
  value = google_bigquery_table.google_political_ads_advertiser_declared_stats.id
}

resource "google_bigquery_table" "google_political_ads_advertiser_geo_spend" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "advertiser_geo_spend"
  description = "This file contains total US advertiser spend on political ads, per US state and the District of Columbia."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_advertiser_geo_spend-table_id" {
  value = google_bigquery_table.google_political_ads_advertiser_geo_spend.table_id
}

output "bigquery_table-google_political_ads_advertiser_geo_spend-id" {
  value = google_bigquery_table.google_political_ads_advertiser_geo_spend.id
}

resource "google_bigquery_table" "google_political_ads_advertiser_stats" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "advertiser_stats"
  description = "This table contains the information about advertisers who have run an election ad on Google Ads Services with at least one impression. The table\u0027s primary key is advertiser_id. This table relates to the others in this dataset, with the following connections between columns: advertiser_id is referenced from: advertiser_weekly_spend.advertiser_id campaign_targeting.advertiser_id creative_stats.advertiser_id advertiser_name is referenced from: advertiser_weekly_spend.advertiser_name campaign_targeting.advertiser_name advertiser_id.advertiser_name"
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_advertiser_stats-table_id" {
  value = google_bigquery_table.google_political_ads_advertiser_stats.table_id
}

output "bigquery_table-google_political_ads_advertiser_stats-id" {
  value = google_bigquery_table.google_political_ads_advertiser_stats.id
}

resource "google_bigquery_table" "google_political_ads_advertiser_weekly_spend" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "advertiser_weekly_spend"
  description = "This table contains the information for how much an advertiser spent on political ads during a given week. The table\u0027s primary key is advertiser_id, election_cycle, week_start_date"
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_advertiser_weekly_spend-table_id" {
  value = google_bigquery_table.google_political_ads_advertiser_weekly_spend.table_id
}

output "bigquery_table-google_political_ads_advertiser_weekly_spend-id" {
  value = google_bigquery_table.google_political_ads_advertiser_weekly_spend.id
}

resource "google_bigquery_table" "google_political_ads_campaign_targeting" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "campaign_targeting"
  description = "This table was deprecated and ad-level targeting information was made available in the `google_political_ads.creative_stats` BigQuery table, effective April 2020. This table contains the information related to ad campaigns run by advertisers."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_campaign_targeting-table_id" {
  value = google_bigquery_table.google_political_ads_campaign_targeting.table_id
}

output "bigquery_table-google_political_ads_campaign_targeting-id" {
  value = google_bigquery_table.google_political_ads_campaign_targeting.id
}

resource "google_bigquery_table" "google_political_ads_creative_stats" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "creative_stats"
  description = "This table contains the information for election ads that have appeared on Google Ads Services. Ad-level targeting data was added to this file in April 2020. ad_id is referenced from: campaign_targeting.ads_list Data that was previously available in the `google_political_ads.campaign_targeting` table has been deprecated and removed in favor of this table."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_creative_stats-table_id" {
  value = google_bigquery_table.google_political_ads_creative_stats.table_id
}

output "bigquery_table-google_political_ads_creative_stats-id" {
  value = google_bigquery_table.google_political_ads_creative_stats.id
}

resource "google_bigquery_table" "google_political_ads_geo_spend" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "geo_spend"
  description = "This table contains the information for how much is spent buying election ads on Google Ads Services. The data is aggregated by Congressional district. The primary key is state, congressional_district."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_geo_spend-table_id" {
  value = google_bigquery_table.google_political_ads_geo_spend.table_id
}

output "bigquery_table-google_political_ads_geo_spend-id" {
  value = google_bigquery_table.google_political_ads_geo_spend.id
}

resource "google_bigquery_table" "google_political_ads_last_updated" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "last_updated"
  description = "This table contains the information of the latest updated date for the Political Ads report. All dates provided are per UTC time zone."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_last_updated-table_id" {
  value = google_bigquery_table.google_political_ads_last_updated.table_id
}

output "bigquery_table-google_political_ads_last_updated-id" {
  value = google_bigquery_table.google_political_ads_last_updated.id
}

resource "google_bigquery_table" "google_political_ads_top_keywords_history" {
  project     = var.project_id
  dataset_id  = "google_political_ads"
  table_id    = "top_keywords_history"
  description = "The \"Top Keywords\" section of the US report was removed and updates to this table were terminated in December 2019. The table reflects historical data. This table contains the information for the top six keywords on which political advertisers have spent money during an election cycle. This data is only provided for US elections. The primary key is election_cycle, report_date."
  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-google_political_ads_top_keywords_history-table_id" {
  value = google_bigquery_table.google_political_ads_top_keywords_history.table_id
}

output "bigquery_table-google_political_ads_top_keywords_history-id" {
  value = google_bigquery_table.google_political_ads_top_keywords_history.id
}
