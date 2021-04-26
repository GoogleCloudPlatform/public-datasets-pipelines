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


resource "google_bigquery_dataset" "covid19_tracking" {
  dataset_id = "covid19_tracking"
  project    = var.project_id
}

output "bigquery_dataset-covid19_tracking-dataset_id" {
  value = google_bigquery_dataset.covid19_tracking.dataset_id
}

resource "google_storage_bucket" "covid19_tracking-dev-processing" {
  name                        = "${var.project_num}-covid19_tracking-dev-processing"
  force_destroy               = true
  uniform_bucket_level_access = true
}

output "storage_bucket-processing-name" {
  value = google_storage_bucket.covid19_tracking-dev-processing.name
}

resource "google_storage_bucket" "covid19_tracking-dev-destination" {
  name                        = "${var.project_num}-covid19_tracking-dev-destination"
  force_destroy               = true
  uniform_bucket_level_access = true
}

output "storage_bucket-destination-name" {
  value = google_storage_bucket.covid19_tracking-dev-destination.name
}
