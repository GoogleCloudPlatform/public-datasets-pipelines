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


resource "google_bigquery_table" "creative_stats" {
  project    = var.project_id
  dataset_id = "google_political_ads"
  table_id   = "creative_stats"

  description = "This table contains the information for election ads that have appeared on Google Ads Services. Ad-level targeting data was added to this file in April 2020. ad_id is referenced from: campaign_targeting.ads_list Data that was previously available in the `google_political_ads.campaign_targeting` table has been deprecated and removed in favor of this table."




  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-creative_stats-table_id" {
  value = google_bigquery_table.creative_stats.table_id
}

output "bigquery_table-creative_stats-id" {
  value = google_bigquery_table.creative_stats.id
}
