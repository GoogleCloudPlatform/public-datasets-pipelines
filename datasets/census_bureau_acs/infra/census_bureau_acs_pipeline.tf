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


resource "google_bigquery_table" "census_bureau_acs_cbsa_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "cbsa_2019_1yr"
  description = "CBSA 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_cbsa_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_cbsa_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_cbsa_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "cbsa_2020_1yr"
  description = "CBSA 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_cbsa_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_cbsa_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_cbsa_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "cbsa_2021_1yr"
  description = "CBSA 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_cbsa_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_cbsa_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_cbsa_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "cbsa_2019_5yr"
  description = "CBSA 2019 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_cbsa_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_cbsa_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_cbsa_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "cbsa_2020_5yr"
  description = "CBSA 2020 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_cbsa_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_cbsa_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_cbsa_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "cbsa_2021_5yr"
  description = "CBSA 2021 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_cbsa_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_cbsa_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_cbsa_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_censustract_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "censustract_2019_5yr"
  description = "Census tract 2019 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_censustract_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_censustract_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_censustract_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_censustract_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_censustract_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "censustract_2020_5yr"
  description = "Census tract 2020 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_censustract_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_censustract_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_censustract_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_censustract_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_censustract_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "censustract_2021_5yr"
  description = "Census tract 2021 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_censustract_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_censustract_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_censustract_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_censustract_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_congressionaldistrict_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "congressionaldistrict_2019_1yr"
  description = "Congressional district 2019 1 year table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_congressionaldistrict_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "congressionaldistrict_2020_1yr"
  description = "Congressional district 2020 1 year table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_congressionaldistrict_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "congressionaldistrict_2021_1yr"
  description = "Congressional district 2021 1 year table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_congressionaldistrict_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "congressionaldistrict_2019_5yr"
  description = "Congressional district 2019 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_congressionaldistrict_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "congressionaldistrict_2020_5yr"
  description = "Congressional district 2020 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_congressionaldistrict_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "congressionaldistrict_2020_5yr"
  description = "Congressional district 2020 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_congressionaldistrict_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_congressionaldistrict_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_county_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "county_2019_1yr"
  description = "County 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_county_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_county_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_county_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_county_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_county_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "county_2020_1yr"
  description = "County 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_county_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_county_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_county_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_county_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_county_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "county_2021_1yr"
  description = "County 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_county_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_county_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_county_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_county_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_county_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "county_2019_5yr"
  description = "County 2019 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_county_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_county_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_county_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_county_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_county_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "county_2020_5yr"
  description = "County 2020 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_county_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_county_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_county_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_county_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_county_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "county_2021_5yr"
  description = "County 2021 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_county_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_county_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_county_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_county_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_place_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "place_2019_1yr"
  description = "Place 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_place_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_place_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_place_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_place_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_place_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "place_2020_1yr"
  description = "Place 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_place_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_place_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_place_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_place_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_place_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "place_2021_1yr"
  description = "Place 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_place_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_place_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_place_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_place_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_place_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "place_2019_5yr"
  description = "Place 2019 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_place_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_place_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_place_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_place_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_place_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "place_2020_5yr"
  description = "Place 2020 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_place_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_place_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_place_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_place_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_place_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "place_2021_5yr"
  description = "Place 2021 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_place_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_place_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_place_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_place_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_puma_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "puma_2019_1yr"
  description = "PUMA 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_puma_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_puma_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_puma_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_puma_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_puma_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "puma_2020_1yr"
  description = "PUMA 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_puma_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_puma_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_puma_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_puma_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_puma_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "puma_2021_1yr"
  description = "PUMA 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_puma_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_puma_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_puma_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_puma_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_puma_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "puma_2019_5yr"
  description = "PUMA 2019 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_puma_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_puma_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_puma_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_puma_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_puma_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "puma_2020_5yr"
  description = "PUMA 2020 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_puma_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_puma_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_puma_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_puma_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_puma_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "puma_2021_5yr"
  description = "PUMA 2021 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_puma_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_puma_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_puma_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_puma_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2016_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2016_1yr"
  description = "School district elementary 2016 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2016_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2016_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2016_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2016_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2017_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2017_1yr"
  description = "School district elementary 2017 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2017_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2017_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2017_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2017_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2018_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2018_1yr"
  description = "School district elementary 2018 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2018_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2018_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2018_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2018_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2019_1yr"
  description = "School district elementary 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2020_1yr"
  description = "School district elementary 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2021_1yr"
  description = "School district elementary 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2016_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2016_5yr"
  description = "School district elementary 2016 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2016_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2016_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2016_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2016_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2017_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2017_5yr"
  description = "School district elementary 2017 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2017_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2017_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2017_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2017_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2018_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2018_5yr"
  description = "School district elementary 2018 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2018_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2018_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2018_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2018_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2019_5yr"
  description = "School district elementary 2019 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2020_5yr"
  description = "School district elementary 2020 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictelementary_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictelementary_2021_5yr"
  description = "School district elementary 2021 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictelementary_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictelementary_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2016_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2016_1yr"
  description = "School district secondary 2016 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2016_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2016_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2016_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2016_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2017_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2017_1yr"
  description = "School district secondary 2017 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2017_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2017_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2017_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2017_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2018_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2018_1yr"
  description = "School district secondary 2018 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2018_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2018_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2018_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2018_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2019_1yr"
  description = "School district secondary 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2020_1yr"
  description = "School district secondary 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2021_1yr"
  description = "School district secondary 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2016_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2016_5yr"
  description = "School district secondary 2016 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2016_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2016_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2016_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2016_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2017_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2017_5yr"
  description = "School district secondary 2017 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2017_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2017_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2017_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2017_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2018_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2018_5yr"
  description = "School district secondary 2018 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2018_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2018_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2018_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2018_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2019_5yr"
  description = "School district secondary 2019 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2020_5yr"
  description = "School district secondary 2020 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictsecondary_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictsecondary_2021_5yr"
  description = "School district secondary 2021 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictsecondary_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictsecondary_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2016_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2016_1yr"
  description = "School district unified 2016 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2016_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2016_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2016_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2016_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2017_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2017_1yr"
  description = "School district unified 2017 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2017_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2017_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2017_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2017_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2018_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2018_1yr"
  description = "School district unified 2018 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2018_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2018_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2018_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2018_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2019_1yr"
  description = "School district unified 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2020_1yr"
  description = "School district unified 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2021_1yr"
  description = "School district unified 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2016_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2016_5yr"
  description = "School district unified 2016 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2016_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2016_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2016_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2016_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2017_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2017_5yr"
  description = "School district unified 2017 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2017_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2017_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2017_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2017_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2018_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2018_5yr"
  description = "School district unified 2018 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2018_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2018_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2018_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2018_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2019_5yr"
  description = "School district unified 2019 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2020_5yr"
  description = "School district unified 2020 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_schooldistrictunified_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "schooldistrictunified_2021_5yr"
  description = "School district unified 2021 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_schooldistrictunified_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_schooldistrictunified_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_state_2019_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "state_2019_1yr"
  description = "State 2019 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_state_2019_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_state_2019_1yr.table_id
}

output "bigquery_table-census_bureau_acs_state_2019_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_state_2019_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_state_2020_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "state_2020_1yr"
  description = "State 2020 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_state_2020_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_state_2020_1yr.table_id
}

output "bigquery_table-census_bureau_acs_state_2020_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_state_2020_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_state_2021_1yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "state_2021_1yr"
  description = "State 2021 1 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_state_2021_1yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_state_2021_1yr.table_id
}

output "bigquery_table-census_bureau_acs_state_2021_1yr-id" {
  value = google_bigquery_table.census_bureau_acs_state_2021_1yr.id
}

resource "google_bigquery_table" "census_bureau_acs_state_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "state_2019_5yr"
  description = "State 2019 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_state_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_state_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_state_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_state_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_state_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "state_2020_5yr"
  description = "State 2020 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_state_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_state_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_state_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_state_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_state_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "state_2021_5yr"
  description = "State 2021 5 year report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_state_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_state_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_state_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_state_2021_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_zcta_2019_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "zcta_2019_5yr"
  description = "ZCTA 2019 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_zcta_2019_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_zcta_2019_5yr.table_id
}

output "bigquery_table-census_bureau_acs_zcta_2019_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_zcta_2019_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_zcta_2020_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "zcta_2020_5yr"
  description = "ZCTA 2020 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_zcta_2020_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_zcta_2020_5yr.table_id
}

output "bigquery_table-census_bureau_acs_zcta_2020_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_zcta_2020_5yr.id
}

resource "google_bigquery_table" "census_bureau_acs_zcta_2021_5yr" {
  project     = var.project_id
  dataset_id  = "census_bureau_acs"
  table_id    = "zcta_2021_5yr"
  description = "ZCTA 2021 5 years report table"
  depends_on = [
    google_bigquery_dataset.census_bureau_acs
  ]
}

output "bigquery_table-census_bureau_acs_zcta_2021_5yr-table_id" {
  value = google_bigquery_table.census_bureau_acs_zcta_2021_5yr.table_id
}

output "bigquery_table-census_bureau_acs_zcta_2021_5yr-id" {
  value = google_bigquery_table.census_bureau_acs_zcta_2021_5yr.id
}
