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


resource "google_bigquery_dataset" "nces_ipeds" {
  dataset_id  = "nces_ipeds"
  project     = var.project_id
  description = "The National Center for Education Statistics (NCES) collects, analyzes and makes available data related to education in the U.S. and other nations.\nThe Integrated Postsecondary Education Data System (IPEDS) contains information on U.S. colleges, universities, and technical and vocational institutions."
}

data "google_iam_policy" "bq_ds__nces_ipeds" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["nces_ipeds"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "nces_ipeds" {
  dataset_id  = google_bigquery_dataset.nces_ipeds.dataset_id
  policy_data = data.google_iam_policy.bq_ds__nces_ipeds.policy_data
}
output "bigquery_dataset-nces_ipeds-dataset_id" {
  value = google_bigquery_dataset.nces_ipeds.dataset_id
}

resource "google_storage_bucket" "nces" {
  name                        = "${var.bucket_name_prefix}-nces"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

output "storage_bucket-nces-name" {
  value = google_storage_bucket.nces.name
}
