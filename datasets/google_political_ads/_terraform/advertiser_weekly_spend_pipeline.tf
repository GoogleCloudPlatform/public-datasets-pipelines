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


resource "google_bigquery_table" "advertiser_weekly_spend" {
  project    = var.project_id
  dataset_id = "google_political_ads"
  table_id   = "advertiser_weekly_spend"

  description = "This table contains the information for how much an advertiser spent on political ads during a given week. The table\u0027s primary key is advertiser_id, election_cycle, week_start_date"




  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-advertiser_weekly_spend-table_id" {
  value = google_bigquery_table.advertiser_weekly_spend.table_id
}

output "bigquery_table-advertiser_weekly_spend-id" {
  value = google_bigquery_table.advertiser_weekly_spend.id
}
