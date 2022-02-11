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


resource "google_bigquery_dataset" "travel_sustainability" {
  dataset_id  = "travel_sustainability"
  project     = var.project_id
  description = "Travel Sustainability"
}

output "bigquery_dataset-travel_sustainability-dataset_id" {
  value = google_bigquery_dataset.travel_sustainability.dataset_id
}

resource "google_storage_bucket" "travel-sustainability" {
  name                        = "${var.bucket_name_prefix}-travel-sustainability"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

output "storage_bucket-travel-sustainability-name" {
  value = google_storage_bucket.travel-sustainability.name
}
