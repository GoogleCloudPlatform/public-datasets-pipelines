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


resource "google_bigquery_table" "last_updated" {
  project    = var.project_id
  dataset_id = "google_political_ads"
  table_id   = "last_updated"

  description = "This table contains the information of the latest updated date for the Political Ads report. All dates provided are per UTC time zone."




  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-last_updated-table_id" {
  value = google_bigquery_table.last_updated.table_id
}

output "bigquery_table-last_updated-id" {
  value = google_bigquery_table.last_updated.id
}
