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


resource "google_bigquery_dataset" "census_bureau_acs" {
  dataset_id  = "census_bureau_acs"
  project     = var.project_id
  description = "American Comunity Survey dataset"
}

output "bigquery_dataset-census_bureau_acs-dataset_id" {
  value = google_bigquery_dataset.census_bureau_acs.dataset_id
}

resource "google_storage_bucket" "census-bureau-acs" {
  name                        = "${var.bucket_name_prefix}-census-bureau-acs"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
}

output "storage_bucket-census-bureau-acs-name" {
  value = google_storage_bucket.census-bureau-acs.name
}
