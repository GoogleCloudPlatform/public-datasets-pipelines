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


resource "google_bigquery_table" "covid19_vaccination_access_facility_boundary_us_all" {
  project    = var.project_id
  dataset_id = "covid19_vaccination_access"
  table_id   = "facility_boundary_us_all"

  description = "This table is formed by combining the data from the individual US tables of drive, transit and walk. It represents the boundaries of areas surrounding vaccination facilities from which people can reach the facility within certain duration. It is computed for 3 travel modes of drive, transit and walk and for predetermined time periods."




  depends_on = [
    google_bigquery_dataset.covid19_vaccination_access
  ]
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_all-table_id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_all.table_id
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_all-id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_all.id
}

resource "google_bigquery_table" "covid19_vaccination_access_facility_boundary_us_drive" {
  project    = var.project_id
  dataset_id = "covid19_vaccination_access"
  table_id   = "facility_boundary_us_drive"

  description = "This table represents the boundaries of areas surrounding vaccination facilities from which people can reach the facility by driving within predetermined time periods."




  depends_on = [
    google_bigquery_dataset.covid19_vaccination_access
  ]
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_drive-table_id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_drive.table_id
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_drive-id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_drive.id
}

resource "google_bigquery_table" "covid19_vaccination_access_facility_boundary_us_transit" {
  project    = var.project_id
  dataset_id = "covid19_vaccination_access"
  table_id   = "facility_boundary_us_transit"

  description = "This table represents the boundaries of areas surrounding vaccination facilities from which people can reach the facility by public transit within predetermined time periods."




  depends_on = [
    google_bigquery_dataset.covid19_vaccination_access
  ]
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_transit-table_id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_transit.table_id
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_transit-id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_transit.id
}

resource "google_bigquery_table" "covid19_vaccination_access_facility_boundary_us_walk" {
  project    = var.project_id
  dataset_id = "covid19_vaccination_access"
  table_id   = "facility_boundary_us_walk"

  description = "This table represents the boundaries of areas surrounding vaccination facilities from which people can reach the facility by walking within predetermined time periods."




  depends_on = [
    google_bigquery_dataset.covid19_vaccination_access
  ]
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_walk-table_id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_walk.table_id
}

output "bigquery_table-covid19_vaccination_access_facility_boundary_us_walk-id" {
  value = google_bigquery_table.covid19_vaccination_access_facility_boundary_us_walk.id
}
