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


resource "google_bigquery_dataset" "travel_impact_model" {
  dataset_id  = "travel_impact_model"
  project     = var.project_id
  description = "Travel Impact Model Data"
}

data "google_iam_policy" "bq_ds__travel_impact_model" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["travel_impact_model"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "travel_impact_model" {
  dataset_id  = google_bigquery_dataset.travel_impact_model.dataset_id
  policy_data = data.google_iam_policy.bq_ds__travel_impact_model.policy_data
}
output "bigquery_dataset-travel_impact_model-dataset_id" {
  value = google_bigquery_dataset.travel_impact_model.dataset_id
}

resource "google_storage_bucket" "travel-impact-model" {
  name                        = "${var.bucket_name_prefix}-travel-impact-model"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

data "google_iam_policy" "storage_bucket__travel-impact-model" {
  dynamic "binding" {
    for_each = var.iam_policies["storage_buckets"]["travel-impact-model"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_storage_bucket_iam_policy" "travel-impact-model" {
  bucket      = google_storage_bucket.travel-impact-model.name
  policy_data = data.google_iam_policy.storage_bucket__travel-impact-model.policy_data
}
output "storage_bucket-travel-impact-model-name" {
  value = google_storage_bucket.travel-impact-model.name
}
