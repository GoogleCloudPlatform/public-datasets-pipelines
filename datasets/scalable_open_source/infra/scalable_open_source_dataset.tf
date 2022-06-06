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


resource "google_bigquery_dataset" "deps_dev_v1" {
  dataset_id = "deps_dev_v1"
  project    = var.project_id
}

data "google_iam_policy" "bq_ds__deps_dev_v1" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["deps_dev_v1"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "deps_dev_v1" {
  dataset_id  = google_bigquery_dataset.deps_dev_v1.dataset_id
  policy_data = data.google_iam_policy.bq_ds__deps_dev_v1.policy_data
}
output "bigquery_dataset-deps_dev_v1-dataset_id" {
  value = google_bigquery_dataset.deps_dev_v1.dataset_id
}
