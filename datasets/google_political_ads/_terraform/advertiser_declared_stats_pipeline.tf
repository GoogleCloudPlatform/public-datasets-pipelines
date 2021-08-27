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


resource "google_bigquery_table" "advertiser_declared_stats" {
  project    = var.project_id
  dataset_id = "google_political_ads"
  table_id   = "advertiser_declared_stats"

  description = "Certain California and New Zealand advertisers are required to submit additional data about themselves. The advertiser is responsible for the accuracy of this information, which Google has not confirmed. For California, this information is provided from our express notification process required for certain California advertisers, which is separate from our verification process. For New Zealand, this information is provided during our verification process."




  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-advertiser_declared_stats-table_id" {
  value = google_bigquery_table.advertiser_declared_stats.table_id
}

output "bigquery_table-advertiser_declared_stats-id" {
  value = google_bigquery_table.advertiser_declared_stats.id
}
