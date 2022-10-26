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


resource "google_bigquery_dataset" "bls" {
  dataset_id  = "bls"
  project     = var.project_id
  description = "Overview: This dataset includes economic statistics on inflation, prices, unemployment, and pay \u0026 benefits provided by the Bureau of Labor Statistics (BLS).\n\nUpdate frequency: Monthly\n\nDataset source: U.S. Bureau of Labor Statistics\n\nTerms of use: This dataset is publicly available for anyone to use under the following terms provided by the Dataset Source - http://www.data.gov/privacy-policy#data_policy - and is provided \"AS IS\" without any warranty, express or implied, from Google. Google disclaims all liability for any damages, direct or indirect, resulting from the use of the dataset.\n\nSee the GCP Marketplace listing for more details and sample queries: https://console.cloud.google.com/marketplace/details/bls-public-data/bureau-of-labor-statistics"
}

output "bigquery_dataset-bls-dataset_id" {
  value = google_bigquery_dataset.bls.dataset_id
}

resource "google_storage_bucket" "bls" {
  name                        = "${var.bucket_name_prefix}-bls"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

data "google_iam_policy" "storage_bucket__bls" {
  dynamic "binding" {
    for_each = var.iam_policies["storage_buckets"]["bls"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_storage_bucket_iam_policy" "bls" {
  bucket      = google_storage_bucket.bls.name
  policy_data = data.google_iam_policy.storage_bucket__bls.policy_data
}
output "storage_bucket-bls-name" {
  value = google_storage_bucket.bls.name
}
