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


resource "google_bigquery_dataset" "google_trends" {
  dataset_id  = "google_trends"
  project     = var.project_id
  description = "The Google Trends dataset will provide critical signals that individual users and businesses alike can leverage to make better data-driven decisions. This dataset simplifies the manual interaction with the existing Google Trends UI by automating and exposing anonymized, aggregated, and indexed search data in BigQuery."
}

output "bigquery_dataset-google_trends-dataset_id" {
  value = google_bigquery_dataset.google_trends.dataset_id
}
