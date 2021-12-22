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


resource "google_bigquery_dataset" "sec_failure_to_deliver" {
  dataset_id  = "sec_failure_to_deliver"
  project     = var.project_id
  description = "sec_failure_to_deliver datasets"
}

output "bigquery_dataset-sec_failure_to_deliver-dataset_id" {
  value = google_bigquery_dataset.sec_failure_to_deliver.dataset_id
}

resource "google_storage_bucket" "sec-failure-to-deliver" {
  name                        = "${var.bucket_name_prefix}-sec-failure-to-deliver"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
}

output "storage_bucket-sec-failure-to-deliver-name" {
  value = google_storage_bucket.sec-failure-to-deliver.name
}
