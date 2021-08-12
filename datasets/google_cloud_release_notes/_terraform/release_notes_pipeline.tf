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


resource "google_bigquery_table" "release_notes" {
  project    = var.project_id
  dataset_id = "google_cloud_release_notes"
  table_id   = "release_notes"

  description = "This table contains release notes for the majority of generally available Google Cloud products found on cloud.google.com. You can use this BigQuery public dataset to consume release notes programmatically across all products. HTML versions of release notes are available within each product\u0027s documentation and also in a filterable format at https://console.cloud.google.com/release-notes."




  depends_on = [
    google_bigquery_dataset.google_cloud_release_notes
  ]
}

output "bigquery_table-release_notes-table_id" {
  value = google_bigquery_table.release_notes.table_id
}

output "bigquery_table-release_notes-id" {
  value = google_bigquery_table.release_notes.id
}
