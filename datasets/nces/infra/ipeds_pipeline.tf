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


resource "google_bigquery_table" "nces_ipeds_c2020_a" {
  project    = var.project_id
  dataset_id = "nces_ipeds"
  table_id   = "c2020_a"
  depends_on = [
    google_bigquery_dataset.nces_ipeds
  ]
}

output "bigquery_table-nces_ipeds_c2020_a-table_id" {
  value = google_bigquery_table.nces_ipeds_c2020_a.table_id
}

output "bigquery_table-nces_ipeds_c2020_a-id" {
  value = google_bigquery_table.nces_ipeds_c2020_a.id
}

resource "google_bigquery_table" "nces_ipeds_c2020_a_dict_frequencies" {
  project    = var.project_id
  dataset_id = "nces_ipeds"
  table_id   = "c2020_a_dict_frequencies"
  depends_on = [
    google_bigquery_dataset.nces_ipeds
  ]
}

output "bigquery_table-nces_ipeds_c2020_a_dict_frequencies-table_id" {
  value = google_bigquery_table.nces_ipeds_c2020_a_dict_frequencies.table_id
}

output "bigquery_table-nces_ipeds_c2020_a_dict_frequencies-id" {
  value = google_bigquery_table.nces_ipeds_c2020_a_dict_frequencies.id
}

resource "google_bigquery_table" "nces_ipeds_hd2020" {
  project    = var.project_id
  dataset_id = "nces_ipeds"
  table_id   = "hd2020"
  depends_on = [
    google_bigquery_dataset.nces_ipeds
  ]
}

output "bigquery_table-nces_ipeds_hd2020-table_id" {
  value = google_bigquery_table.nces_ipeds_hd2020.table_id
}

output "bigquery_table-nces_ipeds_hd2020-id" {
  value = google_bigquery_table.nces_ipeds_hd2020.id
}

resource "google_bigquery_table" "nces_ipeds_hd2020_dict_frequencies" {
  project    = var.project_id
  dataset_id = "nces_ipeds"
  table_id   = "hd2020_dict_frequencies"
  depends_on = [
    google_bigquery_dataset.nces_ipeds
  ]
}

output "bigquery_table-nces_ipeds_hd2020_dict_frequencies-table_id" {
  value = google_bigquery_table.nces_ipeds_hd2020_dict_frequencies.table_id
}

output "bigquery_table-nces_ipeds_hd2020_dict_frequencies-id" {
  value = google_bigquery_table.nces_ipeds_hd2020_dict_frequencies.id
}

resource "google_bigquery_table" "nces_ipeds_ic2020" {
  project    = var.project_id
  dataset_id = "nces_ipeds"
  table_id   = "ic2020"
  depends_on = [
    google_bigquery_dataset.nces_ipeds
  ]
}

output "bigquery_table-nces_ipeds_ic2020-table_id" {
  value = google_bigquery_table.nces_ipeds_ic2020.table_id
}

output "bigquery_table-nces_ipeds_ic2020-id" {
  value = google_bigquery_table.nces_ipeds_ic2020.id
}

resource "google_bigquery_table" "nces_ipeds_ic2020_dict_frequencies" {
  project    = var.project_id
  dataset_id = "nces_ipeds"
  table_id   = "ic2020_dict_frequencies"
  depends_on = [
    google_bigquery_dataset.nces_ipeds
  ]
}

output "bigquery_table-nces_ipeds_ic2020_dict_frequencies-table_id" {
  value = google_bigquery_table.nces_ipeds_ic2020_dict_frequencies.table_id
}

output "bigquery_table-nces_ipeds_ic2020_dict_frequencies-id" {
  value = google_bigquery_table.nces_ipeds_ic2020_dict_frequencies.id
}
