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


resource "google_bigquery_table" "google_dei_dar_intersectional_attrition_index" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_intersectional_attrition_index"
  description = "This table contains the attrition index score of Googlers in the U.S. cut by race and gender combined. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_intersectional_attrition_index-table_id" {
  value = google_bigquery_table.google_dei_dar_intersectional_attrition_index.table_id
}

output "bigquery_table-google_dei_dar_intersectional_attrition_index-id" {
  value = google_bigquery_table.google_dei_dar_intersectional_attrition_index.id
}

resource "google_bigquery_table" "google_dei_dar_intersectional_hiring" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_intersectional_hiring"
  description = "This table contains the breakdown of Googlers hired in the U.S. cut by race and gender combined. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_intersectional_hiring-table_id" {
  value = google_bigquery_table.google_dei_dar_intersectional_hiring.table_id
}

output "bigquery_table-google_dei_dar_intersectional_hiring-id" {
  value = google_bigquery_table.google_dei_dar_intersectional_hiring.id
}

resource "google_bigquery_table" "google_dei_dar_intersectional_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_intersectional_representation"
  description = "This table contains the representation of Googlers in the U.S. cut by race and gender combined. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_intersectional_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_intersectional_representation.table_id
}

output "bigquery_table-google_dei_dar_intersectional_representation-id" {
  value = google_bigquery_table.google_dei_dar_intersectional_representation.id
}

resource "google_bigquery_table" "google_dei_dar_intersectional_exits_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_intersectional_exits_representation"
  description = "This table contains the breakdown of Googler exits in the U.S. cut by race and gender combined. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_intersectional_exits_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_intersectional_exits_representation.table_id
}

output "bigquery_table-google_dei_dar_intersectional_exits_representation-id" {
  value = google_bigquery_table.google_dei_dar_intersectional_exits_representation.id
}

resource "google_bigquery_table" "google_dei_dar_non_intersectional_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_non_intersectional_representation"
  description = "This table contains the representation of Googlers in the U.S. cut by race and gender separately and the representation of global Googlers cut by gender. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_non_intersectional_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_representation.table_id
}

output "bigquery_table-google_dei_dar_non_intersectional_representation-id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_representation.id
}

resource "google_bigquery_table" "google_dei_dar_non_intersectional_exits_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_non_intersectional_exits_representation"
  description = "This table contains the breakdown of Googler exits in the U.S. cut by race and gender separately and the breakdown of global Googler exits cut by gender. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_non_intersectional_exits_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_exits_representation.table_id
}

output "bigquery_table-google_dei_dar_non_intersectional_exits_representation-id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_exits_representation.id
}

resource "google_bigquery_table" "google_dei_dar_non_intersectional_attrition_index" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_non_intersectional_attrition_index"
  description = "This table contains the attrition index score of Googlers in the U.S. cut by race and gender separately and the attrition index score of global Googlers cut by gender. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_non_intersectional_attrition_index-table_id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_attrition_index.table_id
}

output "bigquery_table-google_dei_dar_non_intersectional_attrition_index-id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_attrition_index.id
}

resource "google_bigquery_table" "google_dei_dar_non_intersectional_hiring" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_non_intersectional_hiring"
  description = "This table contains the breakdown of Googlers hired in the U.S. cut by race and gender separately and the hiring breakdown of global Googlers cut by gender. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_non_intersectional_hiring-table_id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_hiring.table_id
}

output "bigquery_table-google_dei_dar_non_intersectional_hiring-id" {
  value = google_bigquery_table.google_dei_dar_non_intersectional_hiring.id
}

resource "google_bigquery_table" "google_dei_dar_region_non_intersectional_attrition_index" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_region_non_intersectional_attrition_index"
  description = "This table contains the attrition index score of Googlers by region (Americas, APAC, and EMEA) cut by gender. \"Americas\" includes all countries in North and South America in which we operate, excluding the U.S. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_region_non_intersectional_attrition_index-table_id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_attrition_index.table_id
}

output "bigquery_table-google_dei_dar_region_non_intersectional_attrition_index-id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_attrition_index.id
}

resource "google_bigquery_table" "google_dei_dar_region_non_intersectional_hiring" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_region_non_intersectional_hiring"
  description = "This table contains the breakdown of Googlers hired by region (Americas, APAC, and EMEA) cut by gender. \"Americas\" includes all countries in North and South America in which we operate, excluding the U.S. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_region_non_intersectional_hiring-table_id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_hiring.table_id
}

output "bigquery_table-google_dei_dar_region_non_intersectional_hiring-id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_hiring.id
}

resource "google_bigquery_table" "google_dei_dar_region_non_intersectional_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_region_non_intersectional_representation"
  description = "This table contains the representation of Googlers by region (Americas, APAC, and EMEA) cut by race and gender. \"Americas\" includes all countries in North and South America in which we operate, excluding the U.S. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_region_non_intersectional_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_representation.table_id
}

output "bigquery_table-google_dei_dar_region_non_intersectional_representation-id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_representation.id
}

resource "google_bigquery_table" "google_dei_dar_region_non_intersectional_exits_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_region_non_intersectional_exits_representation"
  description = "This table contains the breakdown of Googler exits by region (Americas, APAC, and EMEA) cut by gender. \u201cAmericas\u201d includes all countries in North and South America in which we operate, excluding the U.S. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_region_non_intersectional_exits_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_exits_representation.table_id
}

output "bigquery_table-google_dei_dar_region_non_intersectional_exits_representation-id" {
  value = google_bigquery_table.google_dei_dar_region_non_intersectional_exits_representation.id
}

resource "google_bigquery_table" "google_dei_dar_selfid_representation" {
  project     = var.project_id
  dataset_id  = "google_dei"
  table_id    = "dar_selfid_representation"
  description = "This table contains the representation of Googlers globally who identify as LGBTQ+, members of the military or veterans, people with disabilities, or non-binary genders. Some data may be intentionally redacted due to security and privacy restrictions regarding smaller n-counts. In those cases, the data is displayed as a null value."
  depends_on = [
    google_bigquery_dataset.google_dei
  ]
}

output "bigquery_table-google_dei_dar_selfid_representation-table_id" {
  value = google_bigquery_table.google_dei_dar_selfid_representation.table_id
}

output "bigquery_table-google_dei_dar_selfid_representation-id" {
  value = google_bigquery_table.google_dei_dar_selfid_representation.id
}
