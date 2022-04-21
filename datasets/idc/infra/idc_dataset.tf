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


resource "google_storage_bucket" "idc" {
  name                        = "${var.bucket_name_prefix}-idc"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

output "storage_bucket-idc-name" {
  value = google_storage_bucket.idc.name
}

resource "google_bigquery_dataset" "idc_v1" {
  dataset_id  = "idc_v1"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v1 data"
}

output "bigquery_dataset-idc_v1-dataset_id" {
  value = google_bigquery_dataset.idc_v1.dataset_id
}

resource "google_bigquery_dataset" "idc_v2" {
  dataset_id  = "idc_v2"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v2 data"
}

output "bigquery_dataset-idc_v2-dataset_id" {
  value = google_bigquery_dataset.idc_v2.dataset_id
}

resource "google_bigquery_dataset" "idc_v3" {
  dataset_id  = "idc_v3"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v3 data"
}

output "bigquery_dataset-idc_v3-dataset_id" {
  value = google_bigquery_dataset.idc_v3.dataset_id
}

resource "google_bigquery_dataset" "idc_v4" {
  dataset_id  = "idc_v4"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v4 data"
}

output "bigquery_dataset-idc_v4-dataset_id" {
  value = google_bigquery_dataset.idc_v4.dataset_id
}

resource "google_bigquery_dataset" "idc_v5" {
  dataset_id  = "idc_v5"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v5 data"
}

output "bigquery_dataset-idc_v5-dataset_id" {
  value = google_bigquery_dataset.idc_v5.dataset_id
}

resource "google_bigquery_dataset" "idc_v6" {
  dataset_id  = "idc_v6"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v6 data"
}

output "bigquery_dataset-idc_v6-dataset_id" {
  value = google_bigquery_dataset.idc_v6.dataset_id
}

resource "google_bigquery_dataset" "idc_v7" {
  dataset_id  = "idc_v7"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v7 data"
}

output "bigquery_dataset-idc_v7-dataset_id" {
  value = google_bigquery_dataset.idc_v7.dataset_id
}

resource "google_bigquery_dataset" "idc_v8" {
  dataset_id  = "idc_v8"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v8 data"
}

output "bigquery_dataset-idc_v8-dataset_id" {
  value = google_bigquery_dataset.idc_v8.dataset_id
}

resource "google_bigquery_dataset" "idc_current" {
  dataset_id  = "idc_current"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) current data"
}

output "bigquery_dataset-idc_current-dataset_id" {
  value = google_bigquery_dataset.idc_current.dataset_id
}
