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


resource "google_bigquery_table" "advertiser_stats" {
  project    = var.project_id
  dataset_id = "google_political_ads"
  table_id   = "advertiser_stats"

  description = "This table contains the information about advertisers who have run an election ad on Google Ads Services with at least one impression. The table\u0027s primary key is advertiser_id. This table relates to the others in this dataset, with the following connections between columns: advertiser_id is referenced from: advertiser_weekly_spend.advertiser_id campaign_targeting.advertiser_id creative_stats.advertiser_id advertiser_name is referenced from: advertiser_weekly_spend.advertiser_name campaign_targeting.advertiser_name advertiser_id.advertiser_name"




  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-advertiser_stats-table_id" {
  value = google_bigquery_table.advertiser_stats.table_id
}

output "bigquery_table-advertiser_stats-id" {
  value = google_bigquery_table.advertiser_stats.id
}
