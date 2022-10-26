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


resource "google_bigquery_table" "noaa_ghcnd_by_year" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "ghcnd_by_year"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_ghcnd_by_year-table_id" {
  value = google_bigquery_table.noaa_ghcnd_by_year.table_id
}

output "bigquery_table-noaa_ghcnd_by_year-id" {
  value = google_bigquery_table.noaa_ghcnd_by_year.id
}

resource "google_bigquery_table" "noaa_ghcnd_countries" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "ghcnd_countries"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_ghcnd_countries-table_id" {
  value = google_bigquery_table.noaa_ghcnd_countries.table_id
}

output "bigquery_table-noaa_ghcnd_countries-id" {
  value = google_bigquery_table.noaa_ghcnd_countries.id
}

resource "google_bigquery_table" "noaa_ghcnd_inventory" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "ghcnd_inventory"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_ghcnd_inventory-table_id" {
  value = google_bigquery_table.noaa_ghcnd_inventory.table_id
}

output "bigquery_table-noaa_ghcnd_inventory-id" {
  value = google_bigquery_table.noaa_ghcnd_inventory.id
}

resource "google_bigquery_table" "noaa_ghcnd_states" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "ghcnd_states"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_ghcnd_states-table_id" {
  value = google_bigquery_table.noaa_ghcnd_states.table_id
}

output "bigquery_table-noaa_ghcnd_states-id" {
  value = google_bigquery_table.noaa_ghcnd_states.id
}

resource "google_bigquery_table" "noaa_ghcnd_stations" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "ghcnd_stations"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_ghcnd_stations-table_id" {
  value = google_bigquery_table.noaa_ghcnd_stations.table_id
}

output "bigquery_table-noaa_ghcnd_stations-id" {
  value = google_bigquery_table.noaa_ghcnd_stations.id
}

resource "google_bigquery_table" "noaa_gsod_stations" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "gsod_stations"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_gsod_stations-table_id" {
  value = google_bigquery_table.noaa_gsod_stations.table_id
}

output "bigquery_table-noaa_gsod_stations-id" {
  value = google_bigquery_table.noaa_gsod_stations.id
}

resource "google_bigquery_table" "noaa_hurricanes" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "hurricanes"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_hurricanes-table_id" {
  value = google_bigquery_table.noaa_hurricanes.table_id
}

output "bigquery_table-noaa_hurricanes-id" {
  value = google_bigquery_table.noaa_hurricanes.id
}

resource "google_bigquery_table" "noaa_lightning_strikes_by_year" {
  project     = var.project_id
  dataset_id  = "noaa"
  table_id    = "lightning_strikes_by_year"
  description = "noaaspc"
  depends_on = [
    google_bigquery_dataset.noaa
  ]
}

output "bigquery_table-noaa_lightning_strikes_by_year-table_id" {
  value = google_bigquery_table.noaa_lightning_strikes_by_year.table_id
}

output "bigquery_table-noaa_lightning_strikes_by_year-id" {
  value = google_bigquery_table.noaa_lightning_strikes_by_year.id
}
