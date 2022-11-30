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


resource "google_bigquery_table" "nih_gudid_contacts" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "contacts"
  description = "National Library of Medicine for historic data - contacts dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_contacts-table_id" {
  value = google_bigquery_table.nih_gudid_contacts.table_id
}

output "bigquery_table-nih_gudid_contacts-id" {
  value = google_bigquery_table.nih_gudid_contacts.id
}

resource "google_bigquery_table" "nih_gudid_device" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "device"
  description = "National Library of Medicine for historic data - device dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_device-table_id" {
  value = google_bigquery_table.nih_gudid_device.table_id
}

output "bigquery_table-nih_gudid_device-id" {
  value = google_bigquery_table.nih_gudid_device.id
}

resource "google_bigquery_table" "nih_gudid_device_sizes" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "device_sizes"
  description = "National Library of Medicine for historic data - device_sizes dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_device_sizes-table_id" {
  value = google_bigquery_table.nih_gudid_device_sizes.table_id
}

output "bigquery_table-nih_gudid_device_sizes-id" {
  value = google_bigquery_table.nih_gudid_device_sizes.id
}

resource "google_bigquery_table" "nih_gudid_environmental_conditions" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "environmental_conditions"
  description = "National Library of Medicine for historic data - environmental_conditions dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_environmental_conditions-table_id" {
  value = google_bigquery_table.nih_gudid_environmental_conditions.table_id
}

output "bigquery_table-nih_gudid_environmental_conditions-id" {
  value = google_bigquery_table.nih_gudid_environmental_conditions.id
}

resource "google_bigquery_table" "nih_gudid_gmdn_terms" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "gmdn_terms"
  description = "National Library of Medicine for historic data - gmdn_terms dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_gmdn_terms-table_id" {
  value = google_bigquery_table.nih_gudid_gmdn_terms.table_id
}

output "bigquery_table-nih_gudid_gmdn_terms-id" {
  value = google_bigquery_table.nih_gudid_gmdn_terms.id
}

resource "google_bigquery_table" "nih_gudid_identifiers" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "identifiers"
  description = "National Library of Medicine for historic data - identifiers dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_identifiers-table_id" {
  value = google_bigquery_table.nih_gudid_identifiers.table_id
}

output "bigquery_table-nih_gudid_identifiers-id" {
  value = google_bigquery_table.nih_gudid_identifiers.id
}

resource "google_bigquery_table" "nih_gudid_premarket_submissions" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "premarket_submissions"
  description = "National Library of Medicine for historic data - premarket_submissions dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_premarket_submissions-table_id" {
  value = google_bigquery_table.nih_gudid_premarket_submissions.table_id
}

output "bigquery_table-nih_gudid_premarket_submissions-id" {
  value = google_bigquery_table.nih_gudid_premarket_submissions.id
}

resource "google_bigquery_table" "nih_gudid_product_codes" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "product_codes"
  description = "National Library of Medicine for historic data - product_codes dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_product_codes-table_id" {
  value = google_bigquery_table.nih_gudid_product_codes.table_id
}

output "bigquery_table-nih_gudid_product_codes-id" {
  value = google_bigquery_table.nih_gudid_product_codes.id
}

resource "google_bigquery_table" "nih_gudid_sterilization_method_types" {
  project     = var.project_id
  dataset_id  = "nih_gudid"
  table_id    = "sterilization_method_types"
  description = "National Library of Medicine for historic data - sterilization_method_types dataset"
  depends_on = [
    google_bigquery_dataset.nih_gudid
  ]
}

output "bigquery_table-nih_gudid_sterilization_method_types-table_id" {
  value = google_bigquery_table.nih_gudid_sterilization_method_types.table_id
}

output "bigquery_table-nih_gudid_sterilization_method_types-id" {
  value = google_bigquery_table.nih_gudid_sterilization_method_types.id
}
