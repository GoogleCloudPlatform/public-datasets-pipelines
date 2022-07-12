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


resource "google_storage_bucket" "cfe_calculator" {
  name                        = "${var.bucket_name_prefix}-cfe_calculator"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

data "google_iam_policy" "storage_bucket__cfe_calculator" {
  dynamic "binding" {
    for_each = var.iam_policies["storage_buckets"]["cfe_calculator"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_storage_bucket_iam_policy" "cfe_calculator" {
  bucket      = google_storage_bucket.cfe_calculator.name
  policy_data = data.google_iam_policy.storage_bucket__cfe_calculator.policy_data
}
output "storage_bucket-cfe_calculator-name" {
  value = google_storage_bucket.cfe_calculator.name
}

resource "google_bigquery_dataset" "cfe_calculator" {
  dataset_id  = "cfe_calculator"
  project     = var.project_id
  description = "OEDI commercial and residential hourly load"
}

output "bigquery_dataset-cfe_calculator-dataset_id" {
  value = google_bigquery_dataset.cfe_calculator.dataset_id
}
