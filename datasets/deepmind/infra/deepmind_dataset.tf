/**
 * Copyright 2022 Google LLC
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


resource "google_storage_bucket" "deepmind-alphafold" {
  name                        = "${var.bucket_name_prefix}-deepmind-alphafold"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

data "google_iam_policy" "storage_bucket__deepmind-alphafold" {
  dynamic "binding" {
    for_each = var.iam_policies["storage_buckets"]["deepmind-alphafold"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_storage_bucket_iam_policy" "deepmind-alphafold" {
  bucket      = google_storage_bucket.deepmind-alphafold.name
  policy_data = data.google_iam_policy.storage_bucket__deepmind-alphafold.policy_data
}
output "storage_bucket-deepmind-alphafold-name" {
  value = google_storage_bucket.deepmind-alphafold.name
}

resource "google_storage_bucket" "deepmind-alphafold-v4" {
  name                        = "${var.bucket_name_prefix}-deepmind-alphafold-v4"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

data "google_iam_policy" "storage_bucket__deepmind-alphafold-v4" {
  dynamic "binding" {
    for_each = var.iam_policies["storage_buckets"]["deepmind-alphafold-v4"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_storage_bucket_iam_policy" "deepmind-alphafold-v4" {
  bucket      = google_storage_bucket.deepmind-alphafold-v4.name
  policy_data = data.google_iam_policy.storage_bucket__deepmind-alphafold-v4.policy_data
}
output "storage_bucket-deepmind-alphafold-v4-name" {
  value = google_storage_bucket.deepmind-alphafold-v4.name
}

resource "google_bigquery_dataset" "deepmind_alphafold" {
  dataset_id  = "deepmind_alphafold"
  project     = var.project_id
  description = "Metadata for the AlphaFold Protein Structure Database"
}

data "google_iam_policy" "bq_ds__deepmind_alphafold" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["deepmind_alphafold"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "deepmind_alphafold" {
  dataset_id  = google_bigquery_dataset.deepmind_alphafold.dataset_id
  policy_data = data.google_iam_policy.bq_ds__deepmind_alphafold.policy_data
}
output "bigquery_dataset-deepmind_alphafold-dataset_id" {
  value = google_bigquery_dataset.deepmind_alphafold.dataset_id
}
