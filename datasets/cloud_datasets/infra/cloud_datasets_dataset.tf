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


resource "google_bigquery_dataset" "_cloud_datasets" {
  dataset_id  = "_cloud_datasets"
  project     = var.project_id
  description = "A dataset dedicated to Google Cloud Datasets Program and its metadata (not a public dataset)"
}

output "bigquery_dataset-_cloud_datasets-dataset_id" {
  value = google_bigquery_dataset._cloud_datasets.dataset_id
}
